
TEMPLATE = lib
QMAKE_LN_SHLIB = :
CONFIG += 
QMAKE_CFLAGS_WARN_ON += -Wno-unused-parameter -Wno-format-security -Wmissing-field-initializers
  QMAKE_CXXFLAGS_WARN_ON += -Wno-unused-parameter -Wno-format-security
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




  BIT_DEPTH =64

  UI_DIR   += ./GeneratedLx$${BIT_DEPTH}
  RCC_DIR  += ./GeneratedLx$${BIT_DEPTH}
  TARGET = lx_rrImageTga64
  QMAKE_POST_LINK = ../../../../sources/remove_lib_nr.sh $$quote($(DESTDIR)$(TARGET))

  CONFIG(debug, debug|release) {
	DESTDIR = ../../../../_debug/plugins64/image
  DEFINES +=  rrConsoleApp rrPlugin defrrImageTga
  QT       -= core gui
	LIBS +=  -L../../../../_libs -L../../../../
	OBJECTS_DIR = ../../../../../z_compiler_files/debug_lx64_rrImageTga
	MOC_DIR += ./GeneratedLx$${BIT_DEPTH}/debug
	INCLUDEPATH += ./GeneratedLx$${BIT_DEPTH} \
	    ./GeneratedLx$${BIT_DEPTH}/debug
	DEFINES += rrDEBUG
  } else {
	DESTDIR = ../../../../_release/plugins64/image
  DEFINES +=  rrConsoleApp rrPlugin defrrImageTga
  QT       -= core gui
	QMAKE_CXXFLAGS += -ffunction-sections -fdata-sections
	QMAKE_LFLAGS += -Wl,--gc-sections 
	LIBS +=  -L../../../../_libs -L../../../../
	OBJECTS_DIR = ../../../../../z_compiler_files/release_lx64_rrImageTga
	MOC_DIR += ./GeneratedLx$${BIT_DEPTH}/release
	INCLUDEPATH += ./GeneratedLx$${BIT_DEPTH} \
	    ./GeneratedLx$${BIT_DEPTH}/release
	IDE_PLUGIN_RPATH = \$\$ORIGIN/lib
	QMAKE_LFLAGS += -Wl,-z,origin \'-Wl,-rpath,$${IDE_PLUGIN_RPATH}\'
	QMAKE_RPATHDIR =
  }


# Include file(s)
include(__rrImageTga.pri)


