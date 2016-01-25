#include "rrSceneParserShake.h"

#include <QFile> 
#include <QTextStream>
#include "../../shared_SDK/RR_DataTypes_jobs_SDK.h"


DllExport int pInfo(rrP::_dataPARS_Info * const data)
{
	data->RRVersion= rrVersion;
	data->QTVersion= qVersion();
    data->MinorID=rrP::MinorID_PARS;

    //Human readable informations about the plugin:
    data->pluginName=       "Shake";
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
	data->supportedFileExt= "*.shk;";

	return rrP::rSuccessful;
}




DllExport int pLoadSceneFile(rrP::_dataPARS_LoadSceneFile * const data)
{
	try 
	{
	//check for version conflict RRender<>This plugin:
	if (!data->jobs->isVersionSupported()) return rrP::rRRDataVersionConflict; 
	QFile scnFile(*(data->FileName));
	if (!scnFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
		return rrP::rFileFailedToOpen;
	}
	QTextStream fStreamIn(&scnFile);
	QString line;

	int seqStart=1,seqEnd=100,seqStep=1;
	rrJ::_JobBasics *job=NULL;
	int AppVersMayor=2;
	QString AppVersMinor;

	int lineNo=0;
	while (!fStreamIn.atEnd()) {
		lineNo++;
		line=fStreamIn.readLine().trimmed();
		if (line.isEmpty()) continue;
		if ((lineNo<3) && (line.contains("Shake v",Qt::CaseInsensitive))) {
			line.remove(0,line.indexOf("Shake v",0,Qt::CaseInsensitive)+7);
			AppVersMayor=line.left(line.indexOf('.')).toInt();
			line.remove(0,line.indexOf('.')+1);
			if (line.indexOf('.')<line.indexOf(' ')) 
				 AppVersMinor=line.left(line.indexOf('.'));
			else AppVersMinor=line.left(line.indexOf(' '));
			continue;
		}
		if (line.startsWith("//")) continue;
		if (line.contains("SetTimeRange",Qt::CaseInsensitive)) {
			line.remove(0,line.indexOf('"')+1);
			line.truncate(line.indexOf('"'));
			if (line.isEmpty()) continue;
			if (line.contains('-',Qt::CaseInsensitive)) {
				seqStart=line.left(line.indexOf('-')).toInt();
				line.remove(0,line.indexOf('-')+1);
				if (!line.contains('x',Qt::CaseInsensitive)) {
					seqEnd=line.left(line.indexOf('x')).toInt();
					line.remove(0,line.indexOf('x')+1);
					seqStep=line.toInt();
				} else {
					seqEnd=line.toInt();
					seqStep=1;
				}
			} else {
				seqStart=line.toInt();
				seqEnd=seqStart;
				seqStep=1;
			}
			continue;
		}
		if (line.contains("FileOut(",Qt::CaseInsensitive)) { //Ignore Ifcheck
			if (line.endsWith(',')) line+=fStreamIn.readLine().trimmed();
			if (!data->jobs->getNewJob(job)) return rrP::rMemError;
			job->Layer=line.left(line.indexOf('=')).trimmed();
			line.remove(0,line.indexOf('=')+1);
			line.remove(0,line.indexOf('"')+1);
			line.truncate(line.indexOf('"'));
			if (line.contains('#')) {
				job->ImageFileName=line.left(line.indexOf('#'));
				line.remove(0,line.indexOf('#'));
				job->ImageFramePadding=0;
				while ((!line.isEmpty()) && (line.at(0)=='#')) {
					job->ImageFramePadding++;
					line.remove(0,1);
				}
				job->ImageExtension=line;
			} else if (line.contains('@')) {
				job->ImageFileName=line.left(line.indexOf('@'));
				line.remove(0,line.indexOf('@'));
				job->ImageFramePadding=0;
				while ((!line.isEmpty()) && (line.at(0)=='@')) {
					job->ImageFramePadding++;
					line.remove(0,1);
				}
				job->ImageExtension=line;
			} else {
				job->ImageFileName=line;
			}
			/*if (job->ImageFileName.value[1]=='/') {
				QString st;
				st=job->ImageFileName;
				st.remove(0,3);
				st.remove(0,st.indexOf('/')+1);
#ifdef RR_OS_WIN
				if (st.indexOf('/')==1) {
					st.insert(1,':');
				}
#endif
				job->ImageFileName=st;
			}
			*/
			continue;
		}
	}

	scnFile.close();
	QString DatabaseDir;
	DatabaseDir=*(data->FileName);
	if (DatabaseDir.contains(PD)) {
		DatabaseDir.truncate(DatabaseDir.lastIndexOf(PD)+1);
	}


	if (data->jobs->maxJobs>0) {
		rrJ::_JobBasics *jobCopy=NULL;
		if (!data->jobs->getNewJob(jobCopy)) return rrP::rMemError;
		job= data->jobs->at(0);
		if (!job) return rrP::rMemError;
		*jobCopy=*job;
		job->Layer=rrLayerAll;
		job->uiIsSelected=true;
	}


	for (int j=0; j<data->jobs->maxJobs;j++) {
		job= data->jobs->at(j);
		if (!job) return rrP::rMemError;
		job->Soft.name="Shake";
		job->Soft.IsWhichBit=rrX32;
		job->SeqStart=seqStart;
		job->SeqEnd=seqEnd;
		job->SeqStep=seqStep;
		job->Soft.version=AppVersMayor;
		job->Soft.setVersionMinor(AppVersMinor);
		job->SceneName=*(data->FileName);
		job->SceneDatabaseDir=DatabaseDir;
		
		job->Check_SplitImageFileInto_DirFileExt(true);
	}

	return rrP::rSuccessful;
	}
	catch (...)
	{
		return rrP::rCError;

	}
}


