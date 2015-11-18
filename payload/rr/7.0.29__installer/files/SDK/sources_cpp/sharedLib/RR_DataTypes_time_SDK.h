#ifndef RR_DataTypesTIME_H
#define RR_DataTypesTIME_H

#include "../shared_SDK/RR_defines_SDK.h"
#include "RR_DataTypes_rrString_SDK.h"


// replacement for time_t, but 64 bit signed int on all OS (no year 2032 overflow)
class _rrTime
{
public:
    DllExport_sharedLib _rrTime();
    DllExport_sharedLib _rrTime(bool currenttime);
    DllExport_sharedLib _rrTime(qint64  setTime,bool systemValue=true); //systemValue = value is not offsetted as in time_t
    DllExport_sharedLib _rrTime(quint32 setTime,bool systemValue=true);
	DllExport_sharedLib void	fromDate (int day,int month,int year); 
	DllExport_sharedLib void	fromDateTime (int sec, int min, int hour, int day,int month,int year); 
    DllExport_sharedLib void	operator =  (const _rrTime  &t)  {value= t.value;}
    DllExport_sharedLib void	operator += (const _rrTime  &t)  {value+= t.value;}
    DllExport_sharedLib void	operator -= (const _rrTime  &t)  {value-= t.value;}
	DllExport_sharedLib void	operator -= (const qint64    &t)  {value-= t;}
    DllExport_sharedLib bool	operator >= (const _rrTime    &t) const  {return (value>=t.value);}
    DllExport_sharedLib bool	operator <= (const _rrTime    &t) const  {return (value<=t.value);}
    DllExport_sharedLib bool	operator == (const _rrTime    &t) const {return (value==t.value);}
    DllExport_sharedLib bool	operator != (const _rrTime    &t) const {return (value!=t.value);}
    DllExport_sharedLib bool	operator <  (const _rrTime  &t) const {return (value < t.value);}
    DllExport_sharedLib bool	operator >  (const _rrTime  &t) const {return (value > t.value);}
    DllExport_sharedLib _rrTime  operator -  (const qint64   &t) const   {_rrTime ret; ret.value=value- t; return ret;}
    DllExport_sharedLib _rrTime  operator +  (const qint64   &t) const   {_rrTime ret; ret.value=value+ t; return ret;}
    DllExport_sharedLib qint64  operator -  (const _rrTime  &t) {return (value - t.value);}
    DllExport_sharedLib qint64  operator -  (const _rrTime  &t) const {return (value - t.value);}
	DllExport_sharedLib operator tm ();
	DllExport_sharedLib void to_tm (tm &conv) const;
    DllExport_sharedLib void to_tm_Offset (tm &conv, const qint64 &TimeOffset) const;
	#ifdef RR_OS_WIN
	DllExport_sharedLib void	from_FILETIME (unsigned long &dwLowDateTime, unsigned long &dwHighDateTime);
	#endif
	
  #ifdef QT_CORE_LIB
    DllExport_sharedLib QString asString() const;   //month.day hour:minute.sec
    DllExport_sharedLib QString asStringOffset(const qint64 &TimeOffset) const;   //month.day hour:minute.sec
	DllExport_sharedLib QString asStringDateHourMin() const; //day hour:minute
	DllExport_sharedLib QString asStringHourMin() const; //hour:minute
	DllExport_sharedLib QString asStringDate() const; //day  month(as text)
	DllExport_sharedLib QString asStringMonth() const; //month(as text)
	DllExport_sharedLib QString asStringWeekDateMonth()  const; // weekdate  day. month
	DllExport_sharedLib QString asStringweekDay() const; //  day. weekdate
	DllExport_sharedLib QString asStringWeekHourMin() const; //  weekdate day.  hour:minute
	DllExport_sharedLib QString asStringYear()  const;   //day.month.year (year as 09)
	DllExport_sharedLib QString asStringYear2()  const;  //day.month.year (year as 2009)
    DllExport_sharedLib QString asStringMonthYear() const; //month.year
	DllExport_sharedLib QString asStringYearOnly()  const;   //year (year as 09)
    DllExport_sharedLib QString asStringYearOnly2()  const;   //year (year as 2009)
    DllExport_sharedLib inline QString daytimeAsString() const {return asStringHourMinSec();};
	DllExport_sharedLib QString asStringHourMinSec() const;  //hour:minute.sec
	DllExport_sharedLib QString asStringFileName() const; //monthday_hourminutesec
	DllExport_sharedLib QString asStringFileName_TruncSec() const; //monthday_hourminutesec/10
	DllExport_sharedLib QString asStringFileNameDate() const; //yearmonthday
	DllExport_sharedLib QString asStringFileNameHour() const; //yearmonthday_hour
	DllExport_sharedLib QString asStringFileNameYearMinute() const; //yearmonthday_hourMinute
    DllExport_sharedLib QString asStringFileNameYear10Minute() const; //yearmonthday_hour(10th)Minute
	DllExport_sharedLib void	operator =  (const QDate  &dt);
	DllExport_sharedLib void	operator =  (const QDateTime  &dt);

	DllExport_sharedLib operator QDate () const;
  #else
    DllExport_sharedLib _rrString8_250 asString() const;
    DllExport_sharedLib _rrString8_250 asStringFileName_TruncSec() const; //monthday_hourminutesec/10
  #endif 
	DllExport_sharedLib _rrString8_250 asRR8String() const;
    DllExport_sharedLib _rrString8_250 asRR8StringDateMonth() const;
    DllExport_sharedLib _rrString8_250 asRR8StringDateMonthYear() const;  //day.month.year (months as text)
    DllExport_sharedLib int         getDaySeconds(qint64 offset_sec=0) const;
    DllExport_sharedLib int         getDayMinutes() const;
    DllExport_sharedLib int         getDayHour() const;
    DllExport_sharedLib int         getTotalDays(qint64 offset_sec=0) const;
    DllExport_sharedLib int         weekDay() const;
    DllExport_sharedLib int         dayOfMonth(const qint64 offset_days=0) const;
    DllExport_sharedLib int         month() const;
    DllExport_sharedLib int         year() const;
    DllExport_sharedLib void        setCurrentTime(const qint64 offset_sec=0);
    DllExport_sharedLib bool        waitTimeIsOver(const qint64 &waitTimeSec,const bool &SetToCurrentTimeIfOver=false,const _rrTime * const currentTime=NULL);
    DllExport_sharedLib int         waitTimeDifference(const qint64 &waitTimeSec=0,const _rrTime * const currentTime=NULL) const;
    DllExport_sharedLib qint64      toLocalTime();				//time_t is always GMT+0. This returns a time value modified by the current GMT. This way the right hour number can be exported between different time zones.
    DllExport_sharedLib void        convertFromLocalTime();

    DllExport_sharedLib static int  testIfOfsetIsRight(bool set=false);  //return 0  if offset is right
    DllExport_sharedLib static _rrTime currentTime();
    DllExport_sharedLib static  qint32 getTime_Start_OffSet();
    DllExport_sharedLib static _rrTime convertStatFileTime(const time_t &tim);


	qint64 value;

private:
	DllExport_sharedLib static qint32 rrTime_Start_OffSet; //functions that do not use the system function to convert time_t into day+hour+... need to apply this offset.
};





class _rrTime32
{
public:
    DllExport_sharedLib _rrTime32(){value=0;};
    DllExport_sharedLib void	 operator =  (_rrTime  t)  {value= t.value & 0xFFFFFFFF;}
    DllExport_sharedLib void	 setCurrentTime(const qint64 offset_sec=0);
    DllExport_sharedLib operator _rrTime() const {return _rrTime(value,true );};
	DllExport_sharedLib _rrString8_250 asRR8String() const;
	DllExport_sharedLib operator tm ();
	DllExport_sharedLib void	to_tm (tm &conv) const;
    DllExport_sharedLib void	to_tm_Offset (tm &conv, const qint64 &TimeOffset) const;
  #ifdef QT_CORE_LIB
    DllExport_sharedLib QString asString() const;   //month.day hour:minute.sec
    DllExport_sharedLib QString asStringOffset(const qint64 &TimeOffset) const;   //month.day hour:minute.sec
  #endif
	quint32 value;
};



class _rrTime32_localtime
{
public:
	DllExport_sharedLib _rrTime32_localtime() {value=0;};
    DllExport_sharedLib void	 operator =  (_rrTime  t)  {value= t.toLocalTime() & 0xFFFFFFFF;}
    DllExport_sharedLib operator _rrTime() const {return _rrTime(value,false );};
	quint32  value;
};


#endif
