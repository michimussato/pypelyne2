#include "RR_DataTypes_time_SDK.h"
#include "time.h"

#if defined(RR_OS_WIN) 
	//#include <Windows.h>
#elif defined (RR_OS_LINUX)
	//#include <errno.h>
	//#include <sys/stat.h>
	//#include <stdlib.h>
#else
    //#include <errno.h>
    //#include <sys/stat.h>
    //#include <stdlib.h>
    //#include <Carbon/Carbon.h>
#endif


//#####################################################################################
//#######################  _rrTime           #########################################

 qint32 _rrTime::getTime_Start_OffSet()
{if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true); return rrTime_Start_OffSet;};

_rrTime::_rrTime()
{
	value=0;
}

_rrTime::_rrTime(bool currenttime)
{
	if (currenttime) setCurrentTime();
	else value=0;
}

_rrTime::_rrTime(qint64 setTime,bool systemValue)
{
	value=setTime;
	if (rrTime_Start_OffSet==99) testIfOfsetIsRight(true);
	if (!systemValue) value-=rrTime_Start_OffSet;
}


_rrTime::_rrTime(quint32 setTime,bool systemValue)
{
	value=setTime;
	if (rrTime_Start_OffSet==99) testIfOfsetIsRight(true);
	if (!systemValue) value-=rrTime_Start_OffSet;
}

int _rrTime::month() const
{
	tm conv;
	to_tm(conv);
	return (conv.tm_mon+1);
}

int _rrTime::year() const
{
	tm conv;
	to_tm(conv);
	return (conv.tm_year+1900);
}


int _rrTime::dayOfMonth(qint64 offset_days) const
{
	offset_days*=60*60*24;
	offset_days+=value;
	tm conv;

#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	localtime_s(&conv,&offset_days);
#else
    time_t helper;
    helper=offset_days;
    localtime_r(&helper,&conv);
#endif
	return (conv.tm_mday);
}


int _rrTime::weekDay() const
{
	tm conv;
	to_tm(conv);
	int day=(conv.tm_wday-1);
	if (day<0) day+=7;
	if (day<0) day=0; else if (day>6) day=6;
	return day;
}

qint32 _rrTime::rrTime_Start_OffSet=-1;


int _rrTime::testIfOfsetIsRight(bool set)
{
	//we have to use the current day as it is influenced by the daylight saving time
	time_t tempp;
	time (&tempp);
	qint64 vl2= tempp - rrTime_Start_OffSet; 
	tm conv;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	localtime_s(&conv,&vl2);
#else
    time_t helper;
    helper=vl2;
    localtime_r(&helper,&conv);
#endif
	int offset=conv.tm_hour*60*60 +  conv.tm_min*60 + conv.tm_sec -(tempp % (24*60*60)) ;
    if (offset<-12*60*60 -30) offset+=24*60*60; else if (offset>12*60*60+30) offset-=24*60*60;
	if (set) {
		rrTime_Start_OffSet=offset+rrTime_Start_OffSet;
		return testIfOfsetIsRight();
	} else  {
		return offset;
	}
}


/*qint64 _rrTime::valueFixed()
{
	return toLocalTime();
}*/

qint64 _rrTime::toLocalTime()
{
	if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
	return int(value+ rrTime_Start_OffSet);
}

void _rrTime::convertFromLocalTime()
{
	if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
	value-=rrTime_Start_OffSet;
}


int _rrTime::getTotalDays(const qint64 offset_sec) const
{
	if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
	return int((value+offset_sec+ rrTime_Start_OffSet) /(60*60*24));
}

int _rrTime::getDayHour() const
{
	if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
	return int(((value+ rrTime_Start_OffSet) /(60*60)) % 24);
}


int _rrTime::getDaySeconds(qint64 offset_sec) const
{
	if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
	return int((value+offset_sec+ rrTime_Start_OffSet) % (60*60*24));
}

int _rrTime::getDayMinutes() const
{
	if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
	return int(((value+ rrTime_Start_OffSet)/60) % (60*24));
}

void _rrTime::setCurrentTime(const qint64 offset_sec)
{
	time_t tempp;
	time (&tempp);
	value=tempp+offset_sec;
}

_rrTime _rrTime::currentTime()
{
	_rrTime ret(true);
	return ret;
}

#ifdef RR_OS_WIN
_rrTime _rrTime::convertStatFileTime(const time_t &tim)
{
    if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
    _rrTime ret;
    ret.value=tim;
    tm conv1;
    ret.to_tm(conv1);
    ret.value=_mkgmtime64(&conv1)-rrTime_Start_OffSet;
    return ret;
}

#else

_rrTime _rrTime::convertStatFileTime(const time_t &tim)
{
    _rrTime ret;
    ret.value=tim;
    return ret;
}
#endif



bool _rrTime::waitTimeIsOver(const qint64 &waitTimeSec,const bool &SetToCurrentTimeIfOver,const _rrTime * const CurrentTime) 
{
	time_t tempp;
	if (CurrentTime!=NULL) tempp=CurrentTime->value;
	else time (&tempp);

	if (tempp>value+waitTimeSec) {
		if (SetToCurrentTimeIfOver) value=tempp;
		return true;
	} else return false;
}



int _rrTime::waitTimeDifference(const qint64 &waitTimeSec,const _rrTime * const CurrentTime) const
{
	time_t tempp;
	if (CurrentTime!=NULL) tempp=CurrentTime->value;
	else time (&tempp);

	return int (value+waitTimeSec - tempp);
}

void _rrTime::to_tm (tm &conv)  const
{
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	localtime_s(&conv,&value);
#else
    time_t helper;
    helper=value;
    localtime_r(&helper,&conv);
#endif
}


void _rrTime::to_tm_Offset (tm &conv,const qint64 &TimeOffset)  const
{
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
    qint64 val=value+TimeOffset;
	localtime_s(&conv,&val);
#else
    time_t helper;
    helper=value+TimeOffset;
    localtime_r(&helper,&conv);
#endif
}

/*
tm _rrTime::to_tm ()
{
	tm conv;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	localtime_s(&conv,&value);
#else
    time_t helper;
    helper=value;
    localtime_r(&helper,&conv);
#endif
	return conv;
}*/



_rrTime::operator tm ()
{
	tm conv;
	to_tm(conv);
	return conv;
}

_rrString8_250 _rrTime::asRR8String() const
{
	tm conv;
	to_tm(conv);

        _rrString8_250 ret;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
        sprintf_s(ret.value,250,"%02d.%02d. %02d:%02d.%02d",conv.tm_mon+1,conv.tm_mday,conv.tm_hour,conv.tm_min,conv.tm_sec);
#else
        sprintf(ret.value,"%02d.%02d. %02d:%02d.%02d",conv.tm_mon+1,conv.tm_mday,conv.tm_hour,conv.tm_min,conv.tm_sec);
#endif
        ret.calcLength();
        return ret;
}

_rrString8_250 _rrTime::asRR8StringDateMonth() const
{
	const char *month_names[] = {
		"Jan", "Feb", "Mar", "Apr", "May", "Jun",
		"Jul", "Aug", "Sep", "Oct", "Nov", "Dec", NULL
	};
	tm conv;
	to_tm(conv);

        _rrString8_250 ret;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
        sprintf_s(ret.value,250,"%02d.%s. ",conv.tm_mday,month_names[conv.tm_mon]);
#else
        sprintf(ret.value,"%02d.%s. ",conv.tm_mday,month_names[conv.tm_mon]);
#endif
        ret.calcLength();
        return ret;
}

_rrString8_250 _rrTime::asRR8StringDateMonthYear() const
{
	const char *month_names[] = {
		"Jan", "Feb", "Mar", "Apr", "May", "Jun",
		"Jul", "Aug", "Sep", "Oct", "Nov", "Dec", NULL
	};
	tm conv;
	to_tm(conv);

    _rrString8_250 ret;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
        sprintf_s(ret.value,250,"%02d.%s.%02d ",conv.tm_mday,month_names[conv.tm_mon],conv.tm_year+1900);
#else
        sprintf(ret.value,"%02d.%s.%02d ",conv.tm_mday,month_names[conv.tm_mon],conv.tm_year+1900);
#endif
        ret.calcLength();
        return ret;
}





#ifdef RR_OS_WIN

#define EPOCH_DIFF 0x019DB1DED53E8000LL /* 116444736000000000 nsecs */
#define RATE_DIFF 10000000 /* 100 nsecs */

void _rrTime::from_FILETIME (unsigned long &dwLowDateTime, unsigned long &dwHighDateTime)
{
	value = dwHighDateTime;
	value =value <<32;
	value +=dwLowDateTime;
	value -=EPOCH_DIFF;
	value /=RATE_DIFF;

	/*
	unsigned long h,l,pl;
	unsigned long dh,dl,r;
 
 	// Subtract offset from 1601 to 1970 in 100nsec 
 	h = dwHighDateTime;
 	pl = l = dwLowDateTime;
 	h += 0xfe624e9e;
 	l += 0xe4fbaeb0;
 	if (l < pl)	// carry
 		h++;
 
 	if (h >= 10000000)	// Oops! 
	{
 		value=0;	// Error 
		return;
	}
 	
 	// Truncate from 100nsec to 1 second using long division 
 	dh = 10000000 >> 1;		// Divisor * 0x80000000 
 	dl = 10000000 << 31;
 	for (value = 0, r = 0x80000000; r != 0; r >>= 1) {
 		if (dh < h || (dh == h && dl < l)) {	// If dividor is less than dividend 
 			value |= r;	// Accumulate result 
   			pl = l; // Subtract divisor 
 			h -= dh;
 			l -= dl;
 			if (l > pl)	// carry
 				h--;
 		}
 		dl >>= 1;	// Divide divisor by 2
 		dl |= (dh << 31);
 		dh >>= 1;
 	}
 	if (l >= 5000000)	// Round 
 		value++;*/
}
#endif
//#endif


#if (!defined QT_CORE_LIB)

_rrString8_250 _rrTime::asString() const
{
	return asRR8String();
}

_rrString8_250 _rrTime::asStringFileName_TruncSec() const
{

	tm conv;
	to_tm(conv);

        _rrString8_250 ret;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
        sprintf_s(ret.value,250,"%02d%02d_%02d%02d%01d",conv.tm_mon+1,conv.tm_mday,conv.tm_hour,conv.tm_min,conv.tm_sec/10);
#else
        sprintf(ret.value,"%02d%02d_%02d%02d%01d",conv.tm_mon+1,conv.tm_mday,conv.tm_hour,conv.tm_min,conv.tm_sec/10);
#endif
        ret.calcLength();
        return ret;
}


#else

/*_rrTime::_rrTime(const QDateTime  &dt)
{
	value=dt.toTime_t();
}*/


_rrTime::operator QDate () const
{
	tm conv;
	to_tm(conv);
	return QDate(conv.tm_year+1900,conv.tm_mon+1,conv.tm_mday);
}


void _rrTime::fromDateTime (int sec, int min, int hour, int day,int month,int year)
{
	if (month<1) month=1;
	else if (month>12) month=12;
	if (day<1) day=1;
	else if (day>31) day=31;
	if (year<0) year=2014;
	else if (year<100) year+=2000;
	else if (year>3000) year=3000;

	tm timeptr;
	memset(&timeptr,0,sizeof(tm));
	
	timeptr.tm_sec = sec;
	timeptr.tm_min = min;
	timeptr.tm_hour = hour;
	timeptr.tm_mday = day;
	timeptr.tm_mon = month -1;
	timeptr.tm_year = year - 1900;

	if (timeptr.tm_year==0) {
		_rrTime jetzte(true);
		tm conv;
		jetzte.to_tm(conv);
		timeptr.tm_year=conv.tm_year;
		if (timeptr.tm_mday==1 && timeptr.tm_mon==0) {
			timeptr.tm_mday=conv.tm_mday;
			timeptr.tm_mon=conv.tm_mon;
		}
    } else if (timeptr.tm_year<90) {
        timeptr.tm_year+=100;
    }
	value=mktime ( &timeptr );
	//the first run is just to get the daylight flag for that date.
	//as mktime changes the hour.
	//now set the hour again and use that value

	timeptr.tm_sec = sec;
	timeptr.tm_min = min;
	timeptr.tm_hour = hour;
	timeptr.tm_mday = day;
	timeptr.tm_mon = month -1;
	timeptr.tm_year = year - 1900;

	if (timeptr.tm_year==0) {
		_rrTime jetzte(true);
		tm conv;
		jetzte.to_tm(conv);
		timeptr.tm_year=conv.tm_year;
		if (timeptr.tm_mday==1 && timeptr.tm_mon==0) {
			timeptr.tm_mday=conv.tm_mday;
			timeptr.tm_mon=conv.tm_mon;
		}
    } else if (timeptr.tm_year<90) {
        timeptr.tm_year+=100;
    }
	value=mktime ( &timeptr );
}

void _rrTime::fromDate (int day,int month,int year)
{
	tm timeptr;
	if (month<1) month=1;
	else if (month>12) month=12;
	if (day<1) day=1;
	else if (day>31) day=31;
	if (year<0) year=2014;
	else if (year<100) year+=2000;
	else if (year>3000) year=3000;
	
	timeptr.tm_sec = 0;
	timeptr.tm_min = 0;
	timeptr.tm_hour = 0;
	timeptr.tm_mday = day;
	timeptr.tm_mon = month -1;
	timeptr.tm_year = year - 1900;
	value=mktime ( &timeptr );
	//the first run is just to get the daylight flag for that date.
	//as mktime changes the hour.
	//now set the hour again and use that value
	timeptr.tm_sec = 0;
	timeptr.tm_min = 0;
	timeptr.tm_hour = 0;
	timeptr.tm_mday = day;
	timeptr.tm_mon = month-1;
	timeptr.tm_year = year - 1900;
	value=mktime ( &timeptr );

}


void _rrTime::operator =  (const QDate  &dt)
{
	tm timeptr;
	
	timeptr.tm_sec = 0;
	timeptr.tm_min = 0;
	timeptr.tm_hour = 0;
	timeptr.tm_mday = dt.day();
	timeptr.tm_mon = dt.month()-1;
	timeptr.tm_year = dt.year() - 1900;
	value=mktime ( &timeptr );
	//the first run is just to get the daylight flag for that date.
	//as mktime changes the hour.
	//now set the hour again and use that value
	timeptr.tm_sec = 0;
	timeptr.tm_min = 0;
	timeptr.tm_hour = 0;
	timeptr.tm_mday = dt.day();
	timeptr.tm_mon = dt.month()-1;
	timeptr.tm_year = dt.year() - 1900;
	value=mktime ( &timeptr );

}


void	_rrTime::operator =  (const QDateTime  &dt)
{
	tm timeptr;
	memset(&timeptr,0,sizeof(tm));
	
	timeptr.tm_sec = dt.time().second();
	timeptr.tm_min = dt.time().minute();
	timeptr.tm_hour = dt.time().hour();
	timeptr.tm_mday = dt.date().day();
	timeptr.tm_mon = dt.date().month()-1;
	timeptr.tm_year = dt.date().year() - 1900;
	if (timeptr.tm_year==0) {
		_rrTime jetzte(true);
		tm conv;
		jetzte.to_tm(conv);
		timeptr.tm_year=conv.tm_year;
		if (timeptr.tm_mday==1 && timeptr.tm_mon==0) {
			timeptr.tm_mday=conv.tm_mday;
			timeptr.tm_mon=conv.tm_mon;
		}
    } else if (timeptr.tm_year<90) {
        timeptr.tm_year+=100;
    }
	value=mktime ( &timeptr );
	//the first run is just to get the daylight flag for that date.
	//as mktime changes the hour.
	//now set the hour again and use that value



	timeptr.tm_sec = dt.time().second();
	timeptr.tm_min = dt.time().minute();
	timeptr.tm_hour = dt.time().hour();
	timeptr.tm_mday = dt.date().day();
	timeptr.tm_mon = dt.date().month()-1;
	timeptr.tm_year = dt.date().year() - 1900;
	if (timeptr.tm_year==0) {
		_rrTime jetzte(true);
		tm conv;
		jetzte.to_tm(conv);
		timeptr.tm_year=conv.tm_year;
		if (timeptr.tm_mday==1 && timeptr.tm_mon==0) {
			timeptr.tm_mday=conv.tm_mday;
			timeptr.tm_mon=conv.tm_mon;
		}
    } else if (timeptr.tm_year<90) {
        timeptr.tm_year+=100;
    }
	value=mktime ( &timeptr );

}







QString _rrTime::asStringDateHourMin() const
{
	tm conv;
	to_tm(conv);
	return QString("%1. %2:%3").arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0'));
}

QString _rrTime::asStringHourMin() const
{
	tm conv;
	to_tm(conv);
	return QString("%1:%2").arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0'));
}


QString _rrTime::asString() const
{
	tm conv;
	to_tm(conv);
	return QString("%1.%2 %3:%4.%5").arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0')).arg(conv.tm_sec,2,10,QChar('0'));
}

QString _rrTime::asStringOffset(const qint64 &TimeOffset) const
{
	tm conv;
	to_tm_Offset(conv,TimeOffset);
	return QString("%1.%2 %3:%4.%5").arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0')).arg(conv.tm_sec,2,10,QChar('0'));
}


QString _rrTime::asStringDate() const
{
	tm conv;
	to_tm(conv);
	const char *month_names[] = {
		"Jan", "Feb", "Mar", "Apr", "May", "Jun",
		"Jul", "Aug", "Sep", "Oct", "Nov", "Dec", NULL
	};

    if (conv.tm_mon<0) return QString("%2. %1").arg(conv.tm_mon).arg(conv.tm_mday,2,10,QChar('0'));
	return QString("%2. %1").arg(month_names[conv.tm_mon]).arg(conv.tm_mday,2,10,QChar('0'));
}


QString _rrTime::asStringMonth() const
{
	tm conv;
	to_tm(conv);
	const char *month_names[] = {
		"Jan", "Feb", "Mar", "Apr", "May", "Jun",
		"Jul", "Aug", "Sep", "Oct", "Nov", "Dec", NULL
	};
	//if (conv.tm_mon>=11 || conv.tm_mon<0) {
	//	conv.tm_mon=conv.tm_mon;
	//}
	return QString("%1").arg(month_names[conv.tm_mon]);
}

QString _rrTime::asStringweekDay() const
{
	tm conv;
	to_tm(conv);
	const char *days[] = {
		"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", NULL
	};
	return QString("%1. %2").arg(conv.tm_mday,2,10,QChar('0')).arg(days[conv.tm_wday]);
}

QString _rrTime::asStringWeekHourMin() const //  weekdate day.  hour:minute
{
	tm conv;
	to_tm(conv);
	const char *days[] = {
		"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", NULL
	};
	return QString("%1 %2.  %3:%4").arg(days[conv.tm_wday]).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0'));
}

QString _rrTime::asStringWeekDateMonth() const
{
	tm conv;
	to_tm(conv);
	const char *month_names[] = {
		"Jan", "Feb", "Mar", "Apr", "May", "Jun",
		"Jul", "Aug", "Sep", "Oct", "Nov", "Dec", NULL
	};
	const char *days[] = {
		"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", NULL
	};

	return QString("%1 %2. %3").arg(days[conv.tm_wday]).arg(conv.tm_mday,2,10,QChar('0')).arg(month_names[conv.tm_mon]);
}

QString _rrTime::asStringMonthYear() const //month.year
{
	tm conv;
	to_tm(conv);
	return QString("%2.%3").arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_year-100,2,10,QChar('0'));
}

QString _rrTime::asStringYearOnly() const
{
	tm conv;
	to_tm(conv);
	return QString("%1").arg(conv.tm_year-100,2,10,QChar('0'));
}

QString _rrTime::asStringYearOnly2() const
{
	tm conv;
	to_tm(conv);
	return QString("%1").arg(conv.tm_year+1900,4,10,QChar('0'));
}


QString _rrTime::asStringYear() const
{
	tm conv;
	to_tm(conv);
	return QString("%1.%2.%3").arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_year-100,2,10,QChar('0'));
}


QString _rrTime::asStringYear2() const
{
	tm conv;
	to_tm(conv);
	return QString("%1.%2.%3").arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_year+1900,4,10,QChar('0'));
}


QString _rrTime::asStringFileName() const
{
	tm conv;
	to_tm(conv);
	return QString("%1%2_%3%4%5").arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0')).arg(conv.tm_sec,2,10,QChar('0'));
}

QString _rrTime::asStringFileName_TruncSec() const
{
	tm conv;
	to_tm(conv);
	return QString("%1%2_%3%4%5").arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0')).arg(conv.tm_sec/10,1,10,QChar('0'));
}

QString _rrTime::asStringFileNameDate() const
{
	tm conv;
	to_tm(conv);
	return QString("%1%2%3").arg(conv.tm_year-100,2,10,QChar('0')).arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0'));
}

QString _rrTime::asStringFileNameHour() const
{
	tm conv;
	to_tm(conv);
	return QString("%1%2%3_%4").arg(conv.tm_year-100,2,10,QChar('0')).arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0'));
}

QString _rrTime::asStringFileNameYearMinute() const
{
	tm conv;
	to_tm(conv);
	return QString("%1%2%3_%4%5").arg(conv.tm_year-100,2,10,QChar('0')).arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0'));
}

QString _rrTime::asStringFileNameYear10Minute() const
{
	tm conv;
	to_tm(conv);
	return QString("%1%2%3_%4%5").arg(conv.tm_year-100,2,10,QChar('0')).arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min/10);
}


/*
QString _rrTime::hms()
{
	return QString("%1:%2.%3").arg((value/3600),2,10,QChar('0')).arg(((value/60)%60),2,10,QChar('0')).arg((value % 3600),2,10,QChar('0'));
}

QString _rrTime::hm()
{
	return QString("%1:%2").arg(value/3600,2,10,QChar('0')).arg((value/60 )%60,2,10,QChar('0'));
}

QString _rrTime::ms()
{
	return QString("%1.%2").arg((value/60 )%60,2,10,QChar('0')).arg(value % 3600,2,10,QChar('0'));
}*/


QString _rrTime::asStringHourMinSec() const
{
	if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true);
	return QString("%3:%4.%5").arg(((value+ rrTime_Start_OffSet) /(60*60)) % 24,2,10,QChar('0')).arg(((value+ rrTime_Start_OffSet) /60) % 60,2,10,QChar('0')).arg(((value+ rrTime_Start_OffSet) % 60),2,10,QChar('0'));
}

#endif
 




void _rrTime32::setCurrentTime(const qint64 offset_sec)
{
	time_t tempp;
	time (&tempp);
	value=(tempp+offset_sec) & 0xFFFFFFFF;
}



void _rrTime32::to_tm (tm &conv)  const
{
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	qint64 helper;
	helper=value;
	localtime_s(&conv,&helper);
#else
    time_t helper;
    helper=value;
    localtime_r(&helper,&conv);
#endif
}


void _rrTime32::to_tm_Offset (tm &conv, const qint64 &TimeOffset)  const
{
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
	qint64 helper;
	helper=value+TimeOffset;
	localtime_s(&conv,&helper);
#else
    time_t helper;
    helper=value+TimeOffset;
    localtime_r(&helper,&conv);
#endif
}



_rrTime32::operator tm ()
{
	tm conv;
	to_tm(conv);
	return conv;
}

_rrString8_250 _rrTime32::asRR8String() const
{
	tm conv;
	to_tm(conv);

        _rrString8_250 ret;
#if (defined(RR_OS_WIN) && defined(_MSC_VER))
        sprintf_s(ret.value,250,"%02d.%02d. %02d:%02d.%02d",conv.tm_mon+1,conv.tm_mday,conv.tm_hour,conv.tm_min,conv.tm_sec);
#else
        sprintf(ret.value,"%02d.%02d. %02d:%02d.%02d",conv.tm_mon+1,conv.tm_mday,conv.tm_hour,conv.tm_min,conv.tm_sec);
#endif
        ret.calcLength();
        return ret;
}



#ifdef QT_CORE_LIB

QString _rrTime32::asString() const
{
	tm conv;
	to_tm(conv);
	return QString("%1.%2 %3:%4.%5").arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0')).arg(conv.tm_sec,2,10,QChar('0'));
}

QString _rrTime32::asStringOffset(const qint64 &TimeOffset) const   //month.day hour:minute.sec
{
	tm conv;
	to_tm_Offset(conv,TimeOffset);
	return QString("%1.%2 %3:%4.%5").arg(conv.tm_mon+1,2,10,QChar('0')).arg(conv.tm_mday,2,10,QChar('0')).arg(conv.tm_hour,2,10,QChar('0')).arg(conv.tm_min,2,10,QChar('0')).arg(conv.tm_sec,2,10,QChar('0'));
}

#endif


