#ifndef RR_DataTypesTIME_H
#define RR_DataTypesTIME_H

#include "RR_DataTypes_other_SDK.h"


// replacement for time_t, but 64 bit signed int on all OS (no year 2032 overflow)
class _rrTime
{
public:
    _rrTime();
    _rrTime(bool currenttime);
    _rrTime(qint64  setTime,bool systemValue=true); //systemValue = value is not offsetted as in time_t
    _rrTime(quint32 setTime,bool systemValue=true);
	void	fromDate (int day,int month,int year); 
	void	fromDateTime (int sec, int min, int hour, int day,int month,int year); 
    void	operator =  (const _rrTime  &t)  {value= t.value;}
    void	operator += (const _rrTime  &t)  {value+= t.value;}
    void	operator -= (const _rrTime  &t)  {value-= t.value;}
	void	operator -= (const qint64    &t)  {value-= t;}
    bool	operator >= (const _rrTime    &t) const  {return (value>=t.value);}
    bool	operator <= (const _rrTime    &t) const  {return (value<=t.value);}
    bool	operator == (const _rrTime    &t) const {return (value==t.value);}
    bool	operator != (const _rrTime    &t) const {return (value!=t.value);}
    bool	operator <  (const _rrTime  &t) const {return (value < t.value);}
    bool	operator >  (const _rrTime  &t) const {return (value > t.value);}
    _rrTime  operator -  (const qint64   &t) const   {_rrTime ret; ret.value=value- t; return ret;}
    _rrTime  operator +  (const qint64   &t) const   {_rrTime ret; ret.value=value+ t; return ret;}
    qint64  operator -  (const _rrTime  &t) {return (value - t.value);}
    qint64  operator -  (const _rrTime  &t) const {return (value - t.value);}
	operator tm ();
	void to_tm (tm &conv) const;
    void to_tm_Offset (tm &conv, const qint64 &TimeOffset) const;
	#ifdef RR_OS_WIN
	void	from_FILETIME (unsigned long &dwLowDateTime, unsigned long &dwHighDateTime);
	#endif
	
  #ifdef QT_CORE_LIB
    QString asString() const;   //month.day hour:minute.sec
    QString asStringOffset(const qint64 &TimeOffset) const;   //month.day hour:minute.sec
	QString asStringDateHourMin() const; //day hour:minute
	QString asStringHourMin() const; //hour:minute
	QString asStringDate() const; //day  month(as text)
	QString asStringMonth() const; //month(as text)
	QString asStringWeekDateMonth()  const; // weekdate  day. month
	QString asStringweekDay() const; //  day. weekdate
	QString asStringWeekHourMin() const; //  weekdate day.  hour:minute
	QString asStringYear()  const;   //day.month.year (year as 09)
	QString asStringYear2()  const;  //day.month.year (year as 2009)
    QString asStringMonthYear() const; //month.year
	QString asStringYearOnly()  const;   //year (year as 09)
    QString asStringYearOnly2()  const;   //year (year as 2009)
    inline QString daytimeAsString() const {return asStringHourMinSec();};
	QString asStringHourMinSec() const;  //hour:minute.sec
	QString asStringFileName() const; //monthday_hourminutesec
	QString asStringFileName_TruncSec() const; //monthday_hourminutesec/10
	QString asStringFileNameDate() const; //yearmonthday
	QString asStringFileNameHour() const; //yearmonthday_hour
	QString asStringFileNameYearMinute() const; //yearmonthday_hourMinute
    QString asStringFileNameYear10Minute() const; //yearmonthday_hour(10th)Minute
	void	operator =  (const QDate  &dt);
	void	operator =  (const QDateTime  &dt);

	operator QDate () const;
	//operator QDateTime () const;
    //_rrTime(const QDateTime  &dt);
  #else
    _rrString8_250 asString() const;
    _rrString8_250 asStringFileName_TruncSec() const; //monthday_hourminutesec/10
  #endif 
	_rrString8_250 asRR8String() const;
    _rrString8_250 asRR8StringDateMonth() const;
    _rrString8_250 asRR8StringDateMonthYear() const;  //day.month.year (months as text)
    int         getDaySeconds(qint64 offset_sec=0) const;
    int         getDayMinutes() const;
    int         getDayHour() const;
    int         getTotalDays(qint64 offset_sec=0) const;
    int         weekDay() const;
    int         dayOfMonth(const qint64 offset_days=0) const;
    int         month() const;
    int         year() const;
    void        setCurrentTime(const qint64 offset_sec=0);
    bool        waitTimeIsOver(const qint64 &waitTimeSec,const bool &SetToCurrentTimeIfOver=false,const _rrTime * const currentTime=NULL);
    int         waitTimeDifference(const qint64 &waitTimeSec=0,const _rrTime * const currentTime=NULL) const;
	//qint64 valueFixed();
    qint64      toLocalTime();				//time_t is always GMT+0. This returns a time value modified by the current GMT. This way the right hour number can be exported between different time zones.
    void        convertFromLocalTime();

    static int  testIfOfsetIsRight(bool set=false);  //return 0  if offset is right
    static _rrTime currentTime();
    static inline qint32 getTime_Start_OffSet(){if (rrTime_Start_OffSet==-1) testIfOfsetIsRight(true); return rrTime_Start_OffSet;};
    static _rrTime convertStatFileTime(const time_t &tim);


	qint64 value;

private:
	static qint32 rrTime_Start_OffSet; //functions that do not use the system function to convert time_t into day+hour+... need to apply this offset.
};





class _rrTime32
{
public:
    _rrTime32(){value=0;};
    void	 operator =  (_rrTime  t)  {value= t.value & 0xFFFFFFFF;}
    void	 setCurrentTime(const qint64 offset_sec=0);
    operator _rrTime() const {return _rrTime(value,true );};
	_rrString8_250 asRR8String() const;
	operator tm ();
	void	to_tm (tm &conv) const;
    void	to_tm_Offset (tm &conv, const qint64 &TimeOffset) const;
  #ifdef QT_CORE_LIB
    QString asString() const;   //month.day hour:minute.sec
    QString asStringOffset(const qint64 &TimeOffset) const;   //month.day hour:minute.sec
  #endif
	quint32 value;
};



class _rrTime32_localtime
{
public:
	_rrTime32_localtime() {value=0;};
    void	 operator =  (_rrTime  t)  {value= t.toLocalTime() & 0xFFFFFFFF;}
    operator _rrTime() const {return _rrTime(value,false );};
	quint32  value;
};


#endif
