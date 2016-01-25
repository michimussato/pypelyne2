
TEMPLATE = lib
QMAKE_LN_SHLIB = :
CONFIG += 
QMAKE_CFLAGS_WARN_ON += -Wno-unused-parameter -Wno-format-security -Wmissing-field-initializers 
  QMAKE_CXXFLAGS_WARN_ON += -Wno-unused-parameter -Wno-format-security -Wno-unused-private-field  -Wno-invalid-source-encoding
QMAKE_CXXFLAGS += -fno-strict-aliasing
#DEPENDPATH += .


# IDE_PLUGIN_RPATH:
#do the rpath by hand since it's not possible to use ORIGIN in QMAKE_RPATHDIR
# this expands to $ORIGIN (after qmake and make), it does NOT read a qmake var


#--hash-style=sysv
#12.2.2. GCC Compiler Collection
#This release of Fedora has been built with GCC 4.1, which is included
#with the distribution.
#12.2.2.1. Caveats
#Fedora developers have introduced changes in the ELF .hash section
#that provides symbols for dynamic linking. This new .gnu.hash section,
#which is produced with the new default --hash-style=gnu option for
#gcc, serves the same purpose as previous hash sections. It provides,
#however, an approximately 50% increase in dynamic linking speed.
#Binaries and libraries produced with the new hashing function are
#incompatible with older glibc and dynamic linker releases. To use the
#old-style hashing routines for compatibility with older glibc-based
#systems, pass the --hash-style=sysv option instead.




  QMAKE_TARGET.arch = x86_64
  QMAKE_CXXFLAGS_WARN_ON += -Wno-unused-parameter -Wno-format-security -Wno-unused-private-field  -Wno-invalid-source-encoding
  DEFINES +=  rrConsoleApp rrPlugin defrrImageArchive
  QT += 
  QT       -= gui


  QMAKE_INFO_PLIST = 
  QMAKE_POST_LINK = ../../../../sources/remove_lib_nr_osx.sh $$quote($(DESTDIR)$(TARGET))
  UI_DIR   += ./GeneratedMac
  RCC_DIR  += ./GeneratedMac
  TARGET = mac_rrImageArchive

  CONFIG(debug, debug|release) {
	DESTDIR = ../../../../_debug/plugins64/image
	LIBS +=  -L../../../../_libs/osx -L../../../../_release/bin/mac64/lib -framework CoreFoundation -framework ApplicationServices -lz
	OBJECTS_DIR = ../../../../../z_compiler_files/debug_mac64_rrImageArchive
	MOC_DIR += ./GeneratedMac/debug
	INCLUDEPATH += ./GeneratedMac \
	    ./GeneratedMac/debug
	DEFINES += rrDEBUG
  } else {
	DESTDIR = ../../../../_release/plugins64/image
	LIBS +=  -L../../../../_libs/osx -L../../../../_release/bin/mac64/lib -framework CoreFoundation -framework ApplicationServices -lz
	OBJECTS_DIR = ../../../../../z_compiler_files/release_mac64_rrImageArchive
	MOC_DIR += ./GeneratedMac/release
	INCLUDEPATH += ./GeneratedMac \
	    ./GeneratedMac/release
#	IDE_PLUGIN_RPATH = \$\$ORIGIN
#	QMAKE_LFLAGS += -Wl,-z,origin \'-Wl,-rpath,$${IDE_PLUGIN_RPATH}\',--hash-style=sysv
	QMAKE_RPATHDIR =
  }


# Include file(s)
include(__rrImageArchive.pri)


