#include "rrSceneParserArnold.h"

#include <QFile> 
#include <QTextStream>
#include <QStringList>
#include "../../shared_SDK/RR_DataTypes_jobs_SDK.h"
#include "../../shared/RR_DataTypes_Databuffer.h"



DllExport int pInfo(rrP::_dataPARS_Info * const data)
{
	data->RRVersion= rrVersion;
	data->QTVersion= qVersion();
    data->MinorID=rrP::MinorID_PARS;

    //Human readable informations about the plugin:
    data->pluginName=       "Arnold";
    data->pluginAuthor=     "RR, Holger Schoenberger";
    data->pluginVersion=    "1.0";

    //Check if the data structure is compatible:
    if (data->StructureID!=rrP::StructureID_PARS) {
        data->StructureID=rrP::StructureID_PARS;
        return rrP::rRRDataVersionConflict;
    } else {
        data->StructureID=rrP::StructureID_PARS;
    }

	data->setDebugCompile();
	data->supportedFileExt= "*.ass;*.gz;";

	return rrP::rSuccessful;
}



class _fileReader {
public:	
	~_fileReader();
	bool openFile(QString filename);
	QString readLine();
	bool atEnd();
private:
	QFile scnFile;
	QTextStream fStreamIn;
	bool isFileRead;
	bool isCompressed;
	_RR_DataBuffer databuffer;
	qint64 readPosition;
};


_fileReader::~_fileReader()
{
	if (isFileRead) scnFile.close();
}

bool _fileReader::openFile(QString filename)
{
	scnFile.setFileName(filename);
	isCompressed=filename.endsWith(".gz");
	if (isCompressed) {
		readPosition=0;
		return databuffer.LoadGzipFile(filename);
	} else {
		if (!scnFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
			return false ;
		}
		fStreamIn.setDevice(&scnFile);
		isFileRead=true;
	}
	return true; 
}

QString _fileReader::readLine()
{
	if (isCompressed) {
		for (int p=readPosition; p<databuffer.dataSizeUnCompressed; p++) {
			if (databuffer.buf[p]==0x0A) {
				QByteArray dat(&databuffer.buf[readPosition],p-readPosition);
				readPosition=p+1;
				return dat;
			}
		}
		if (databuffer.dataSizeUnCompressed-readPosition==0) return QString();
		QByteArray dat(&databuffer.buf[readPosition],databuffer.dataSizeUnCompressed-readPosition);
		readPosition=databuffer.dataSizeUnCompressed;
		return dat;
	} else
		return fStreamIn.readLine().trimmed();
}



bool _fileReader::atEnd()
{
	if (isCompressed) {
		return readPosition>=databuffer.dataSizeUnCompressed;
	} else {
		return fStreamIn.atEnd();
	}
}





DllExport int pLoadSceneFile(rrP::_dataPARS_LoadSceneFile * const data)
{
	try 
	{
	//check for version conflict RRender<>This plugin:
	if (!data->jobs->isVersionSupported()) return rrP::rRRDataVersionConflict; 

	if (data->FileName->endsWith(".gz") && !data->FileName->endsWith(".ass.gz"))  return rrP::rUnsupportedFormat;
	_fileReader fileReader;
	if (!fileReader.openFile(*(data->FileName))) return rrP::rFileFailedToOpen;

	rrJ::_JobBasics *job=NULL;
	if (!data->jobs->getNewJob(job)) return rrP::rMemError;

	job->Soft.name="Arnold";
	job->SceneName=*(data->FileName);
	job->Layer=rrLayerDefault;
	job->Camera=rrLayerDefault;
	
	int lineNo=0;
	QString line;
	QString nextLine;
	line=fileReader.readLine();
	int displayMax=0;
	int displayMain=0;
	int displayOutFound=0;
	int currentDisplay=-1;
	struct _dis {
		QString name;
		QString type;
		QString output;
	} displays[30];
	int inblock=0;
	bool inOptions=false;
	bool inDisplay=false;
	int glAppVersMayor=0;
	QString glAppVersMinor="";
    int width=0;
    int height=0;

	while (!fileReader.atEnd()) {
		lineNo++;
		line=nextLine;
		nextLine=fileReader.readLine().trimmed();
		if (line.isEmpty()) continue;
		if (line=="{") inblock++;
		if (line=="}") {
			inblock--;
			if (inblock<=0) {
				inblock=0;
				inOptions=false;
				inDisplay=false;
				currentDisplay=-1;
			}
		}
		if ((lineNo<5) && line.contains("Arnold")) {
			line.remove(0,line.indexOf("Arnold")+1);
			line.remove(0,line.indexOf(' ')+1);
			line.truncate(line.indexOf(' '));
			QString s1,s2;
			s1	=line;
			if (s1.contains("beta",Qt::CaseInsensitive)) {
				s1.remove(s1.indexOf("beta",0,Qt::CaseInsensitive),5);
			}
			if (s1.contains("_sp",Qt::CaseInsensitive)) {
				s1.remove("_sp",Qt::CaseInsensitive);
			}

			if (s1.indexOf('.')>0) {
				s2 = s1.right( s1.size() - s1.indexOf('.')-1);
				s1.truncate(s1.indexOf('.'));
				if (s2.indexOf('.')>0) {
					s2.truncate(s2.indexOf('.'));
				}
				glAppVersMayor=s1.toInt();
				glAppVersMinor=s2;
			} else glAppVersMayor=s1.toInt();
		} else if ((inblock==0) && line.startsWith("options") && nextLine.startsWith("{") && (displayMax==0)) {
			inOptions=true;
        } else if (inOptions &&  line.startsWith("xres")) {
            line.remove(0,line.indexOf(' ')+1);
            width=line.toInt();
        } else if (inOptions &&  line.startsWith("yres")) {
            line.remove(0,line.indexOf(' ')+1);
            height=line.toInt();
		} else if (inOptions &&  line.startsWith("outputs")) {
			inDisplay=true;
			while (line.contains('"')) {
				line.remove(0,line.indexOf('"')+1);
				if (line.contains('"')) {
					QString linePart=line.left(line.indexOf('"'));
					if (linePart.contains(' ')) {
						displayMax++;
						displays[displayMax-1].type=linePart.left(linePart.indexOf(' '));
						linePart.remove(0,linePart.lastIndexOf(' ')+1);
						displays[displayMax-1].name=linePart;
					}
					line.remove(0,line.indexOf('"')+1);
				} else break;
			}
		} else if (inOptions && inDisplay) {
			if (!line.contains('"')) inDisplay=false;
			else
			while (line.contains('"')) {
				line.remove(0,line.indexOf('"')+1);
				if (line.contains('"')) {
					QString linePart=line.left(line.indexOf('"'));
					if (linePart.contains(' ')) {
						displayMax++;
						displays[displayMax-1].type=linePart.left(linePart.indexOf(' '));
						linePart.remove(0,linePart.lastIndexOf(' ')+1);
						displays[displayMax-1].name=linePart;
					}
					line.remove(0,line.indexOf('"')+1);
				} else break;
			}
		}  else if ((inblock==0) &&  line.startsWith("driver_") && nextLine.startsWith("{")) {
			inDisplay=true;
		} else if ((inDisplay) && line.startsWith("name ")) {
			line.remove(0,line.indexOf(' ')+1);
			for (int i=0; i<displayMax; i++) {
                if (line.compare(displays[i].name)==0) {
                    currentDisplay=i;
                    break;
                }
			}
		} else if ((inDisplay) && line.startsWith("filename ") && currentDisplay>=0) {
			line.remove(0,line.indexOf(' ')+1);
			if (line.startsWith('"')) {
				line.remove(0,line.indexOf('"')+1);
				line.truncate(line.indexOf('"'));
			}
			displays[currentDisplay].output=line;
			displayOutFound++;
			if (displayOutFound>=displayMax) break;
		}
	}

	if (displayMax==0) return rrP::rFileFailedToOpen;

	for (int i=0; i<displayMax; i++) {
		if (displays[i].name.startsWith("RGB")) {
			displayMain=i;
			break;
		}
	}


	job->ImageFileName= displays[displayMain].output;
	int maxChannels=0;
	for (int i=0; i<displayMax; i++) {
		if (i!=displayMain) {
			maxChannels++;
			if (maxChannels>rrJ::MaxImageChannels) break;
			job->ImageChannels[maxChannels-1].FileName=displays[i].output;
			job->Check_SplitImageFileInto_DirFileExt_Channel(maxChannels-1);
		}
	}

    job->ImageWidth=width;
    job->ImageHeight=height;
    job->Soft.version=glAppVersMayor;
    job->Soft.setVersionMinor(glAppVersMinor);


	job->uiIsSelected=true;
	if (job->ImageFileName.isEmpty()) return rrP::rFileFailedToOpen;
	
	job->Check_SplitImageFileInto_DirFileExt();

	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;

	}
}


