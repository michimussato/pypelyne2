#include "rrSceneParserMantra.h"

#include <QFile> 
#include <QTextStream>
#include "../../shared_SDK/RR_DataTypes_jobs_SDK.h"

DllExport int pInfo(rrP::_dataPARS_Info * const data)
{
	data->RRVersion= rrVersion;
	data->QTVersion= qVersion();
    data->MinorID=rrP::MinorID_PARS;

    //Human readable informations about the plugin:
    data->pluginName=       "Mantra_StdA";
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
	data->supportedFileExt= "*.ifd;";

	return rrP::rSuccessful;
}




DllExport int pLoadSceneFile(rrP::_dataPARS_LoadSceneFile * const data)
{
#if (!defined rrDEBUG)
	try {
#endif
	//check for version conflict RRender<>This plugin:
	if (!data->jobs->isVersionSupported()) return rrP::rRRDataVersionConflict; 


	QFile scnFile(*(data->FileName));
	if (!scnFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
		return rrP::rFileFailedToOpen;
	}
	//QTextStream fStreamIn(&scnFile);
	QString line;

	rrJ::_JobBasics *job=NULL;
	if (!data->jobs->getNewJob(job)) return rrP::rMemError;

	job->Soft.name="Mantra_StdA";
	job->SceneName=*(data->FileName);
	QString DatabaseDir;
	DatabaseDir=*(data->FileName);
	if (DatabaseDir.contains(PD)) {
		DatabaseDir.truncate(DatabaseDir.lastIndexOf(PD)+1);
	}
	if (DatabaseDir.contains("Render_Archives")) {
		DatabaseDir.truncate(DatabaseDir.lastIndexOf("Render_Archives"));
	}
	job->SceneDatabaseDir=DatabaseDir;

	job->Layer=rrLayerDefault;
	job->Camera=rrLayerDefault;

    


	QString ShadowName;
	int lineNo=0;
	while (!scnFile.atEnd()) {
		lineNo++;
        QByteArray lineB= scnFile.readLine(20*1024*1024);
		
		if (lineB.startsWith("ray_start geo") && lineB.contains('{')) {
			while (true) {
				lineB=scnFile.read(20*1024*1024);
				if (lineB.count()==0) {
					break;
				}
				int pos=lineB.indexOf("}\n");
				if (pos>=0) {
					scnFile.seek(scnFile.pos()-lineB.count()+pos-50);
					lineB= scnFile.readLine(20*1024*1024);
					lineB.replace('\0',' ');
					break;
				}
			}
		} 
	
		line=QString(lineB).trimmed();
		if (line.isEmpty()) continue;

		if ((lineNo<300) && (line.contains("Houdini Version:",Qt::CaseInsensitive))) {
			line.remove(0,line.indexOf(':')+1);
			line=line.trimmed();
			job->Soft.version=line.left(line.indexOf('.')).toInt();
			line.remove(0,line.indexOf('.')+1);
			if (line.indexOf('.')>=0)
				 job->Soft.setVersionMinor(line.left(line.indexOf('.')));
			else job->Soft.setVersionMinor(line);
			continue;
		}

		if (line.startsWith("ray_image ")) {
			line.truncate(line.lastIndexOf('"'));
			line.remove(0,line.lastIndexOf('"')+1);
			if ( (line.size()<2) ||  ((line.at(1)!=':') && (line.at(0)!='/') )) {
				line="<Database>/"+PDs+line;
			}
			job->ImageFileName=line;
		}
		if (line.startsWith("ray_property image deepresolver shadow filename")) {
			line.remove(0,line.indexOf('"')+1);
			line.truncate(line.indexOf('"'));
			ShadowName=line;
		}
	}
	scnFile.close();

	if (job->ImageFileName.endsWith("null:")) {
		if (ShadowName.isEmpty() || ShadowName.compare("null:",Qt::CaseInsensitive)==0) {
			return rrP::rFileFailedToOpen;
		}
		job->ImageFileName=ShadowName;
	}

	if (job->ImageFileName.isEmpty()) return rrP::rFileFailedToOpen;
	
	job->uiIsSelected=true;
	job->Check_SplitImageFileInto_DirFileExt();

	return rrP::rSuccessful;
#if (!defined rrDEBUG)
	}
	catch (...)
	{
		return rrP::rCError;

	}

#endif
}


