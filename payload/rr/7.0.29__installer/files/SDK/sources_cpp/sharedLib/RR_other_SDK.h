
#ifndef RR_DataTypesOtherSDK_H
#define RR_DataTypesOtherSDK_H

#include "../shared_SDK/RR_defines_SDK.h"
#include "RR_DataTypes_rrString_SDK.h"
#include "RR_DataTypes_time_SDK.h"



struct _rrBytePerc  //used to store precentage data 0-100% in a byte 0-0xFF
{
    quint8 value;
    DllExport_sharedLib _rrBytePerc() {value=0;};
    DllExport_sharedLib inline float toF() const  {return (float(value)/255.0f);};  //result range: 0-1
    DllExport_sharedLib inline float toFperc() const  {return (float(value)/2.55f);};  //result range: 0-100
    DllExport_sharedLib inline quint8 toIperc() const  {return int(float(value)/2.55f + 2.55f/2.0f);};  //result range: 0-100
    DllExport_sharedLib inline void fromF(const float &inF) {if (inF>1.0) value=0xFF; else if (inF<0.0) value=0; value=rrRound(inF*255.0f) & 0xFF; if (value==0 && inF>0.0f) value=1;};
    DllExport_sharedLib inline void fromFPerc(float inF) {inF/=100.0f; fromF(inF);};
    DllExport_sharedLib bool noMaxima() {return (value>0 && value<254); };
    DllExport_sharedLib inline bool	operator >  (_rrBytePerc const &in) {return (value>in.value);};
    DllExport_sharedLib inline bool	operator <  (_rrBytePerc const &in) {return (value<in.value);};
    DllExport_sharedLib inline bool	operator >= (_rrBytePerc const &in) {return (value>=in.value);};
    DllExport_sharedLib inline bool	operator <= (_rrBytePerc const &in) {return (value<=in.value);};
    DllExport_sharedLib inline void	operator -= (_rrBytePerc const &in) {if (in.value>value) value=0; else value-=in.value; };
    DllExport_sharedLib inline void	operator += (_rrBytePerc const &in) {if (value+in.value>0xFF) value=0xFF; else value+=in.value;};
	#ifdef QT_CORE_LIB
    DllExport_sharedLib QString str() const { return QString("%1%").arg(rrRound(value*100.0f/255.0f)); };
	#endif
};

class _cJobThreadInstance;

class _rrCPUValue
{
    friend class _cJobThreadInstance;
    friend struct _RenderStats;
public:
    float valueSystem; //value range 0-1
    float nrCores;
    DllExport_sharedLib _rrCPUValue(const float &invalueSystem,const int &innrCores) {valueSystem=invalueSystem; nrCores=float(innrCores); };
    DllExport_sharedLib _rrCPUValue(const _rrCPUValue &in) {valueSystem=in.valueSystem; nrCores=in.nrCores; };
    DllExport_sharedLib operator _rrBytePerc() const {_rrBytePerc ret; ret.fromF(valueSystem); return ret;};
    DllExport_sharedLib inline float asSystemFloat() {return valueSystem; };
    DllExport_sharedLib inline float asCoreFloat() {return (valueSystem*nrCores); };
    DllExport_sharedLib inline float asSystemPerc() {return valueSystem*100.0f; };
    DllExport_sharedLib inline float asCorePerc() {return (valueSystem*nrCores*100.0f); };
    DllExport_sharedLib inline void clearValue() {valueSystem=0.0f;};
    DllExport_sharedLib inline void clear() {valueSystem=0.0f;};
    DllExport_sharedLib inline void setbyCore(const float &f) {valueSystem=f/nrCores;};
    DllExport_sharedLib inline void setbySystem(const float &f) {valueSystem=f;};
    DllExport_sharedLib inline void setbySystemPerc(const int &f) {valueSystem=float(f)/100.0f;};
    DllExport_sharedLib inline void addbyCore(const float &f) {valueSystem+=f/nrCores;};
    DllExport_sharedLib inline void addbySystem(const float &f) {valueSystem+=f;};
    DllExport_sharedLib inline void addbyCoreProc(const float &f) {valueSystem+=f/100.0f/nrCores;};
    DllExport_sharedLib inline void addbySystemProc(const float &f) {valueSystem+=f/100.0f;};
    DllExport_sharedLib inline void clamp() {if (valueSystem<0.0) valueSystem=0.0f; else if (valueSystem>1.0) valueSystem=1.0f;};
    DllExport_sharedLib inline void	operator =  (_rrCPUValue const &in) {valueSystem=in.valueSystem; nrCores=in.nrCores; };
    DllExport_sharedLib inline void	operator -= (_rrCPUValue const &in) {valueSystem-=in.valueSystem;};
    DllExport_sharedLib inline void	operator += (_rrCPUValue const &in) {valueSystem+=in.valueSystem;};
    DllExport_sharedLib inline void	operator *= (float const &mult) {valueSystem*=mult;};
    DllExport_sharedLib inline void	operator /= (float const &div) {valueSystem/=div;};
    DllExport_sharedLib inline bool	operator >  (_rrCPUValue const &in) {return (valueSystem>in.valueSystem);};
    DllExport_sharedLib inline bool	operator <  (_rrCPUValue const &in) {return (valueSystem<in.valueSystem);};
    DllExport_sharedLib inline bool	operator >= (_rrCPUValue const &in) {return (valueSystem>=in.valueSystem);};
    DllExport_sharedLib inline bool	operator <= (_rrCPUValue const &in) {return (valueSystem<=in.valueSystem);};
    DllExport_sharedLib _rrCPUValue operator -  (_rrCPUValue const &in) const {_rrCPUValue ret(*this); ret-=in; return ret;};
    DllExport_sharedLib _rrCPUValue operator +  (_rrCPUValue const &in) const {_rrCPUValue ret(*this); ret+=in; return ret;};
    DllExport_sharedLib bool  isValid() const {return (valueSystem>=0.0f); };
	#ifdef QT_CORE_LIB
    DllExport_sharedLib QString strSystemPerc() const {return QString("%1%").arg(rrRound(valueSystem*100.0f)); };
    DllExport_sharedLib QString strCorePerc() const {return QString("%1%").arg(rrRound(valueSystem*nrCores*100.0f)); };
    DllExport_sharedLib QString strCoreF() const {return QString("%1").arg(valueSystem*nrCores, 0, 'f',1); };
	#endif

private: 
    _rrCPUValue() { }; 
};






DllExport_sharedLib _rrString25		rr_AppType_asString(const rr_AppType &appType);
DllExport_sharedLib void			rrSleep(int ms);
DllExport_sharedLib unsigned long	z_compressBound_copy (unsigned long sourceLen);


#ifndef rrPlugin
	#ifdef QT_CORE_LIB
	#endif
#endif

DllExport_sharedLib _rrString8_250  rrLastOSError8(int errorCode=-1);
DllExport_sharedLib _rrString500   rrLastOSError(int errorCode=-1);









#endif
