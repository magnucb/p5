TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt

unix {
    LIBS += -lblas -llapack -larmadillo
} else {
LIBS += -LC:/Armadillo/ -larmadillo
LIBS += -LC:/Armadillo/examples/lib_win64 -llapack_win64_MT -lblas_win64_MT
INCLUDEPATH += C:/Armadillo/include
}

SOURCES += main.cpp \
    celestialbody.cpp \
    vec3.cpp \
    verlet.cpp \
    cluster.cpp

HEADERS += \
    celestialbody.h \
    vec3.h \
    verlet.h \
    cluster.h

