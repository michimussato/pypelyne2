#include "rrImageArchive.h"
#include "../../shared/RR_font.h"
#include <math.h>

#include <QString>
#include <QList>


struct arcHeader {
	enum _type {arcIFD};
	_type type;
	rrString8_250 version;     
	rrString8_250 date;     
	rrString8_250 output;     
	qint64 fileSize;
};


DllExport int imgInfo(rrP::_dataIMG_Info * const data)
{
   	data->RRVersion= rrVersion;
	data->QTVersion= qVersion();
    data->MinorID=rrP::MinorID_IMG;


    //Human readable informations about the plugin:
    data->pluginName=       "Render Archives";
    data->pluginAuthor=     "RR, Holger Schoenberger";
    data->pluginVersion=    "1.0";

    //Check if the data structure is compatible:
    if (data->StructureID!=rrP::StructureID_IMG) {
        data->StructureID=rrP::StructureID_IMG;
        return rrP::rRRDataVersionConflict;
    } else {
        data->StructureID=rrP::StructureID_IMG;
    }

	data->setDebugCompile(); data->supportedFileExt= "*.ifd;";
	data->flags=(rrP::IMGFuncDecode8);
	data->minFileSize= 350; //data should be at least 300 bytes

	return rrP::rSuccessful;
}




DllExport int imgLoadHeader(rrP::_dataIMG_LoadHeader * const data)
{
	if (data->outInfo->_imgHeaderInfoSize()<sizeof(rrP::_imgHeaderInfo)) return rrP::rRRDataVersionConflict;
	data->in->swapBytes=false;
	arcHeader * header;
	header=(arcHeader *) (data->pluginCustomData->buffer);
	memset(header,0,sizeof(arcHeader));
#if (!defined rrDEBUG)
	try 
#endif
	{
		data->outInfo->bitDepth=8;
		data->outInfo->width=500;
		data->outInfo->height=250;
		data->outInfo->hasAlpha=false;

		data->in->getFileSize();

		header->fileSize=data->in->getFileSize();

		QByteArray buffer(512,0);
		data->in->readBuffer((quint8 *) buffer.data(),350);
		QList<QByteArray> lines=buffer.split('\n');

		header->type=arcHeader::arcIFD;

		data->outInfo->infoString = "Ifd ";
		for (int i=0; i<lines.count(); i++)  {
			QByteArray line=lines.at(i);
			if (line.contains("IFD created by Houdini Version")) {
				line.remove(0,line.indexOf("Houdini Version"));
				header->version=line.constData();
			} else if (line.contains("Generation Time")) {
				line.remove(0,line.indexOf("Generation Time"));
				header->date=line.constData();
			} else if (line.contains("Output driver")) {
				line.remove(0,line.indexOf("Output driver"));
				header->output=line.constData();
			}
		}
		if (header->version.isEmpty()) {
			data->outInfo->infoString += "No Houdini version found";
			return rrP::rUnsupportedFormat;
		}




	return rrP::rLoadEndOfFileOnly;
	}
#if (!defined rrDEBUG)
	catch (...)
	{
		return rrP::rCError;
	}
#endif
}


DllExport int imgDecode8(rrP::_dataIMG_Decode8 * const data)
{
	data->in->swapBytes=false;
	arcHeader * header;
	header=(arcHeader *) (data->pluginCustomData->buffer);

#if (!defined rrDEBUG)
	try 
#endif
	{
		QByteArray buffer(1000,0);
		data->in->readBuffer((quint8 *) buffer.data(),1000);
		QList<QByteArray> lines=buffer.split('\n');
		for (int i=0; i<lines.count(); i++) {
			if (lines.at(i).isEmpty()) {
				lines.removeAt(i);
			}
		}

		rrP::_Rgba8 col;
		col.r=0xFF;
		col.g=0xFF;
		col.b=0xFF;

		rrFont::drawText(*data->out,10,40,QString(header->date),col,20);
		rrFont::drawText(*data->out,10,80,header->version,col,20);
		rrFont::drawText(*data->out,10,120,header->output,col,20);
		rrFont::drawText(*data->out,10,160,"File size: "+rrSpaceTsd(header->fileSize/1024)+"  KiB",col,20);

		if (
			   (!lines.at(lines.count()-1).startsWith("ray_quit\t# }"))
			   )
		{
				col.b=0;
				col.g=0;
				rrFont::drawText(*data->out,10,200,"NOT COMPLETE",col,20);
				return rrP::rDataError;
		} 

	
	return rrP::rSuccessful;
	}
#if (!defined rrDEBUG)
	catch (...)
	{
		return rrP::rCError;
	}
#endif
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





DllExport int imgDecodef(rrP::_dataIMG_Decodef * const data)
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




DllExport int imgEncode8(rrP::_dataIMG_Encode8 * const /*data*/)
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




DllExport int imgEncodef(rrP::_dataIMG_Encodef * const /*data*/)
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


