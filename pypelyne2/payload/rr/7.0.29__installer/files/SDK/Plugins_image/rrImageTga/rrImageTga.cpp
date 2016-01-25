#include "rrImageTga.h"

#include <math.h>

//#include <QByteArray>
//#include <QDataStream>
//#include <QDebug>



#pragma pack(1)
struct tgaHeader {
		//read the TGA header
		quint8 LengthOfIdentificationField;
		quint8 ColorMapType;
		quint8 ImageTypeCode; // 2=RLE compresses
		//don't need from here to XOrigin so they're reordered to keep things aligned
		quint8 NumberOfBitsColorMapEntry;
		quint16 IndexColorMapEntry;
		quint16 CountColorMapEntry;
		//entry below should actually be here, not 3 above
		//quint8 NumberOfBitsColorMapEntry;
		quint16 XOrigin;
		quint16 YOrigin;
		quint16 Width;
		quint16 Height;
		quint8 CMESoBPP;
		quint8 Flags;
};
#pragma pack() 

DllExport int imgInfo(rrP::_dataIMG_Info * const data)
{
	data->RRVersion= rrVersion;
	data->QTVersion= qVersion();
    data->MinorID=rrP::MinorID_IMG;


    //Human readable informations about the plugin:
    data->pluginName=       "Targa";
    data->pluginAuthor=     "RR, Alan Jones, Holger Schoenberger";
    data->pluginVersion=    "1.0";

    //Check if the data structure is compatible:
    if (data->StructureID!=rrP::StructureID_IMG) {
        data->StructureID=rrP::StructureID_IMG;
        return rrP::rRRDataVersionConflict;
    } else {
        data->StructureID=rrP::StructureID_IMG;
    }

	data->setDebugCompile();data->supportedFileExt= "*.tga;";
	data->flags=(rrP::IMGFuncDecode8 | rrP::IMGFuncEncode8);
	data->minFileSize= sizeof(tgaHeader)+ 2*1024; //data should be at least 3 kb
	
	return rrP::rSuccessful;
}





DllExport int imgLoadHeader(rrP::_dataIMG_LoadHeader * const data)
{
	if (sizeof(tgaHeader)>sizeof(rrP::_imgPluginBuffer)) return rrP::rRRDataVersionConflict;
	tgaHeader * header;
	header=(tgaHeader *) (data->pluginCustomData->buffer);
	try 
	{
		data->outInfo->infoString = "tga ";
		data->pluginCustomData->readfromFileBuffer(data->in,sizeof(tgaHeader));



		data->outInfo->width = header->Width;
		data->outInfo->height = header->Height;
		data->outInfo->bitDepth = 8;
		int channelCount;
		switch (header->CMESoBPP)
			{
			case(24):
			data->outInfo->hasAlpha = false;
			channelCount = 3;
			data->outInfo->infoString += " RGB";
			break;
			case(32):
			data->outInfo->hasAlpha = true;
			channelCount = 4;
			data->outInfo->infoString += " RGBA";
			break;
			default:
				data->outInfo->infoString += "Unsupported bit depth.";
				return rrP::rUnsupportedFormat;
			}
		
		if ((header->ImageTypeCode != 2) &&  (header->ImageTypeCode != 10)) {
				data->outInfo->infoString += "Unsupported compression.";
				return rrP::rUnsupportedFormat;
		}

        if (header->ImageTypeCode == 2) {
			uint cSize=sizeof(tgaHeader)+ header->LengthOfIdentificationField +  header->Width*header->Height * channelCount;
			uint fSize=data->in->getFileSize();
			if (fSize< cSize)  {
				data->outInfo->infoString += " ERR: File size too small!";
				return rrP::rWrongFileSize;
			} else if (fSize> cSize+1024)  {
				data->outInfo->infoString += " ERR: File size too big!";
				return rrP::rWrongFileSize;
			}
		}

		if (header->ImageTypeCode == 10)
			data->outInfo->infoString += " RLE-compressed";
		else {
			data->outInfo->infoString += " uncompressed";
			data->outInfo->fixedFileSize=true; 
		}
	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;
	}
}



void decodeRLE(rrP::_imgFileBuffer * const in, rrP::_imgRGBABuffer8 *out, int totalPixels,tgaHeader * header)
	{
	int curPixel = 0;
	
	quint8 packetHeader;
	bool rleEncoded;
	quint8 count;
	
	if (out->hasAlpha)
		{
		rrP::_Rgba8 curPixelValue;
		//it's got an alpha so we can read 32bits in a hit
		//we check it first to save some cycles checking every packet
		while (curPixel < totalPixels)
			{
			in->readUint8( packetHeader );
			//the first bit contains information on whether this packet is RLE encoded
			rleEncoded = (packetHeader >> 7) >0;
			//the other 7 bits are the count
			count = packetHeader & 127;
			
			if (rleEncoded)
				{
				//this packet is run length encoded - so just read a single pixel value and repeat it
				in->readUint32( curPixelValue.col );
				curPixelValue.swapBGR();
				
				//we say <= because there is no use for 0 count packets
				//so the tga spec has count stored as count-1
				for (quint8 i=0; i<=count; i++)
					{
					//the pixel index write function isn't working - so we calculate it by hand for now
					//out->write( curPixel+i, curPixelValue );
					int w = (curPixel+i) % out->width();
					int h = int(floor(((float) curPixel+i)/ (float) out->width()));
					if (header->Flags & 0x20) 
						 out->write(w, h, curPixelValue );
					else out->write(w, header->Height-h-1, curPixelValue );

					}
				}
			else
				{
				//this is a raw packet so we need to read data for each pixel for count pixels
				for (quint8 i=0; i<=count; i++)
					{
					in->readUint32( curPixelValue.col );
					curPixelValue.swapBGR();

//the pixel index write function isn't working - so we calculate it by hand for now
					//out->write( curPixel+i, curPixelValue );
					int w = (curPixel+i) % out->width();
					int h = int(floor(((float)curPixel+i)/ (float) out->width()));
					if (header->Flags & 0x20) 
						 out->write(w, h, curPixelValue );
					else out->write(w, header->Height-h-1, curPixelValue );

					}
				}
			
			curPixel += count+1;
			}
		}
	else
		{
		//no alpha - so read 3 channels
		while (curPixel < totalPixels)
			{
			in->readUint8( packetHeader );
			//the first bit contains information on whether this packet is RLE encoded
			rleEncoded = (packetHeader >> 7)!=0;
			//the other 7 bits are the count
			count = packetHeader & 127;
			rrP::_Rgba8 curPixelValue;
			
			if (rleEncoded)
				{
				//this packet is run length encoded - so just read a single pixel value and repeat it
				in->readUint24(curPixelValue.col);
				curPixelValue.swapBGR();
				//we say <= because there is no use for 0 count packets
				//so the tga spec has count stored as count-1
				for (quint8 i=0; i<=count; i++)
					{
					//the pixel index write function isn't working - so we calculate it by hand for now
					//out->write( curPixel+i, curPixelValue );
					int w = (curPixel+i) % out->width();
					int h = int(floor(((float) curPixel+i)/ (float) out->width()));
					if (header->Flags & 0x20) 
						 out->write(w, h, curPixelValue );
					else out->write(w, header->Height-h-1, curPixelValue );
					}
				}
			else
				{
				//this is a raw packet so we need to read data for each pixel for count pixels
				for (quint8 i=0; i<=count; i++)
					{
					in->readUint24(curPixelValue.col);
					curPixelValue.swapBGR();
					//the pixel index write function isn't working - so we calculate it by hand for now
					//out->write( curPixel+i, curPixelValue );
					int w = (curPixel+i) % out->width();
					int h = int(floor(((float) curPixel+i)/(float) out->width()));
					if (header->Flags & 0x20) 
						 out->write(w, h, curPixelValue );
					else out->write(w, header->Height-h-1, curPixelValue );

					}
				}
			
			curPixel += count+1;
			}
		}
}	

DllExport int imgDecode8(rrP::_dataIMG_Decode8 * const data)
{
	if (sizeof(tgaHeader)>sizeof(rrP::_imgPluginBuffer)) return rrP::rRRDataVersionConflict;
	tgaHeader * header;
	header=(tgaHeader *) (data->pluginCustomData->buffer);
	try 
	{
		data->in->setBufPosition( sizeof(tgaHeader)+ header->LengthOfIdentificationField );
		if (header->ImageTypeCode == 2)
			{
			//8 bits per channel RAW
			//quint8 * dataStart = (quint8 *)(data->in->buffer()+18+header->LengthOfIdentificationField);
			//we need to go through a pixel at a time
			//quint32 curPixelValue = 0;
			rrP::_Rgba8 curPixelValue;

			for (int h=0; h<header->Height; h++)
				{
				for (int w=0; w<header->Width; w++)
					{
					if (header->CMESoBPP == 32)
						{
						data->in->readUint32( curPixelValue.col );
						curPixelValue.swapBGR();
						if (header->Flags & 0x20) 
							 data->out->write(w, h, curPixelValue );
						else data->out->write(w, header->Height-h-1, curPixelValue );
						}
					else
						{
						data->in->readUint24( curPixelValue.col );
						curPixelValue.swapBGR();
						if (header->Flags & 0x20) 
							 data->out->write(w, h, curPixelValue );
						else data->out->write(w, header->Height-h-1, curPixelValue );
						}
					}
				}
			}
		else if (header->ImageTypeCode == 10)
			{
			//8 bits per channel RLE
//			int curPixel = 0;
			int totalPixels = header->Width * header->Height;
			
			decodeRLE(data->in, data->out, totalPixels,header );
			}

		return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;
	}
}






DllExport int imgDecode16(rrP::_dataIMG_Decode16 * const /*data*/)
{
	try 
	{


		return rrP::rUnsupportedFormat;




	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;
	}
}




DllExport int imgDecodef(rrP::_dataIMG_Decodef * const /*data*/)
{
	try 
	{


		return rrP::rUnsupportedFormat;




	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;
	}
}




DllExport int imgEncode8(rrP::_dataIMG_Encode8 * const data)
{
	try 
	{
		data->out->ResetBufferSize();
		data->out->setBufPosition(0);
		data->out->swapBytes=false;
		tgaHeader header;
		memset(&header,0,sizeof(header));
		header.ImageTypeCode=2;
		if (data->in->hasAlpha)
			header.CMESoBPP=32;
		else header.CMESoBPP=24;
		header.Width=data->in->width();
		header.Height=data->in->height();
		data->out->writeBuffer((quint8 *) &header,sizeof(header));
		rrP::_Rgba8 pixel;
		if (data->in->hasAlpha) {
			for (int y=data->in->height()-1; y>=0; y--) {
				for (int x=0; x<data->in->width(); x++) {
					data->in->read(pixel,x,y);
					pixel.swapBGR();
					if (!data->out->writeUint32(pixel.col)) {
						return rrP::rFileBuffertoSmall;
					}
				}
			}
		} else {
			for (int y=data->in->height()-1; y>=0; y--) {
				for (int x=0; x<data->in->width(); x++) {
					data->in->read(pixel,x,y);
					pixel.swapBGR();
					if (!data->out->writeUint24(pixel.col)) {
						return rrP::rFileBuffertoSmall;
					}
				}
			}
		}

	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;
	}
}



DllExport int imgEncode16(rrP::_dataIMG_Encode16 * const /*data*/)
{
		
	try 
	{


		return rrP::rUnsupportedFormat;




	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;
	}
}







DllExport int imgEncodef(rrP::_imgFileBuffer * const ,__RRSDK * const)
{
		
	try 
	{


		return rrP::rUnsupportedFormat;




	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;
	}
}


