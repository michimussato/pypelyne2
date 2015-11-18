
TEMPLATE = lib
#DEPENDPATH += .
CONFIG += 

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


mac {
  DEFINES +=  QT_XML_LIB rrConsoleApp rrPlugin defrrSceneParserShake
  QT +=  xml
  QT       -= gui



  UI_DIR   += ./GeneratedMac
  RCC_DIR  += ./GeneratedMac
  TARGET = mac_rrSceneParserShake
  CONFIG(debug, debug|release) {
	DESTDIR = ../../../../_debug/plugins/submitter_sceneparser
	LIBS +=  -L../../../../_libs/osx -framework CoreFoundation -framework ApplicationServices -lz
	OBJECTS_DIR = ../../../../z_compiler_files/debug_mac_rrSceneParserShake
	MOC_DIR += ./GeneratedMac/debug
	INCLUDEPATH += ./GeneratedMac \
	    ./GeneratedMac/debug
	DEFINES += rrDEBUG
  } else {
	DESTDIR = ../../../../_release/plugins/submitter_sceneparser
	LIBS +=  -L../../../../_libs/osx -framework CoreFoundation -framework ApplicationServices -lz
	OBJECTS_DIR = ../../../../z_compiler_files/release_mac_rrSceneParserShake
	MOC_DIR += ./GeneratedMac/release
	INCLUDEPATH += ./GeneratedMac \
	    ./GeneratedMac/release
#	IDE_PLUGIN_RPATH = \$\$ORIGIN
#	QMAKE_LFLAGS += -Wl,-z,origin \'-Wl,-rpath,$${IDE_PLUGIN_RPATH}\',--hash-style=sysv
	QMAKE_RPATHDIR =
  }
} else:unix {

  BIT_DEPTH =64

  UI_DIR   += ./GeneratedLx$${BIT_DEPTH}
  RCC_DIR  += ./GeneratedLx$${BIT_DEPTH}
  TARGET = lx_rrSceneParserShake$${BIT_DEPTH}
  CONFIG(debug, debug|release) {
	DESTDIR = ../../../_debug/plugins$${BIT_DEPTH}/submitter_sceneparser
  DEFINES +=  QT_XML_LIB rrConsoleApp rrPlugin defrrSceneParserShake
  QT +=  xml
  QT       -= gui
	LIBS +=  -L../../../_libs
	OBJECTS_DIR = ../../../z_compiler_files/debug_lx$${BIT_DEPTH}_rrSceneParserShake
	MOC_DIR += ./GeneratedLx$${BIT_DEPTH}/debug
	INCLUDEPATH += ./GeneratedLx$${BIT_DEPTH} \
	    ./GeneratedLx$${BIT_DEPTH}/debug
	DEFINES += rrDEBUG
  } else {
	DESTDIR = ../../../_release/plugins$${BIT_DEPTH}/submitter_sceneparser
  DEFINES +=  QT_XML_LIB rrConsoleApp rrPlugin defrrSceneParserShake
  QT +=  xml
  QT       -= gui
	QMAKE_CXXFLAGS += -ffunction-sections -fdata-sections
	QMAKE_LFLAGS += -Wl,--gc-sections 
	LIBS +=  -L../../../_libs
	OBJECTS_DIR = ../../../z_compiler_files/release_lx$${BIT_DEPTH}_rrSceneParserShake
	MOC_DIR += ./GeneratedLx$${BIT_DEPTH}/release
	INCLUDEPATH += ./GeneratedLx$${BIT_DEPTH} \
	    ./GeneratedLx$${BIT_DEPTH}/release
	IDE_PLUGIN_RPATH = \$\$ORIGIN/lib
	QMAKE_LFLAGS += -Wl,-z,origin \'-Wl,-rpath,$${IDE_PLUGIN_RPATH}\'
	QMAKE_RPATHDIR =
  }
} else:win32 {
  DEFINES +=  QT_XML_LIB rrConsoleApp rrPlugin defrrSceneParserShake
  QT +=  xml
  QT       -= gui
  UI_DIR  += ./GeneratedFiles
  RCC_DIR += ./GeneratedFiles
  TARGET = rrSceneParserShake$${BIT_DEPTH}
  CONFIG(debug, debug|release) {
	DESTDIR = ../../../_debug/plugins/submitter_sceneparser
	LIBS +=  -L../../../_libs
	OBJECTS_DIR = ../../../z_compiler_files/debug_mac_rrSceneParserShake
	MOC_DIR += ./GeneratedFiles/debug
	INCLUDEPATH += ./GeneratedFiles \
	    ./GeneratedFiles/debug
	DEFINES += rrDEBUG
  } else {
	DESTDIR = ../../../_release/plugins/submitter_sceneparser
	LIBS +=  -L../../../_libs
	OBJECTS_DIR = ../../../z_compiler_files/release_mac_rrSceneParserShake
	MOC_DIR += ./GeneratedFiles/release
	INCLUDEPATH += ./GeneratedFiles \
	    ./GeneratedFiles/release
  }
}

# Include file(s)
include(rrSceneParserShake.pri)

