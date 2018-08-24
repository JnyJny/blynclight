
# Fill out the form at:
#
# https://www.embrava.com/pages/embrava-software-sdk
#
# They will mail you links for Windows, Linux and Mac SDKs.  When you
# receive the SDK URLs, invoke make with the URL for your platform:
#
# $ make URL=https://url/for/the/sdk
#
# The makefile takes apart the static library archive and constructs a
# shared library which can then be used by python.

IMPLEMENTATIONS= Linux Darwin

IMPLEMENTATION := $(shell uname)

INSTALL_PATH := ../src/blynclight/libs/$(IMPLEMENTATION)

TARGET= libblynclight_api.so

SRC= blynclight_api.c
OBJ= $(SRC:.c=.o)

Darwin_SDK=  embrava-sdk
Linux_SDK=   EmbravaSdkForLinux

SDKS= $(Darwin_SDK) $(Linux_SDK)

.PHONY: install curl

all: $(IMPLEMENTATION)

Darwin: SDK_ROOT= $(Darwin_SDK)
Darwin: API_DIR= SDK_static_lib
Darwin: API_ARCHIVE= $(SDK_ROOT)/$(API_DIR)/libblynclightcontrol.a
Darwin: API_OBJS=  blynclightcontrol.o
Darwin: LIBS=

Linux: SDK_ROOT= $(Linux_SDK)
Linux: API_DIR= EmbravaApi
Linux: API_ARCHIVE= $(SDK_ROOT)/$(API_DIR)/libembravaapi.a
Linux: API_OBJS= embravaapi.o hid-libusb.o
Linux: LIBS= -lhidapi-hidraw -lusb-1.0

$(IMPLEMENTATIONS): curl install

install: $(INSTALL_PATH) $(TARGET)
	cp $(TARGET) $(INSTALL_PATH)/$(TARGET)

$(INSTALL_PATH):
	mkdir -p $@

$(TARGET): $(OBJ) curl
	$(CC) -o $@ $(API_OBJS) $(OBJ) -fPIC -shared $(LIBS)

$(OBJ): $(SRC) $(SRC:.c=.h)
	$(CC) -c $(SRC) -I$(SDK_ROOT)/$(API_DIR) -std=gnu99 -fPIC

curl:
	curl -L $(URL) | jar x
	ar x $(API_ARCHIVE) $(API_OBJS)

clean:
	rm -rf *.o $(TARGET)

clobber: clean
	rm -rf $(Darwin_SDK) $(Linux_SDK) __MACOSX
