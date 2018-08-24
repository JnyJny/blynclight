
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

SYSTEM := $(shell uname)

INSTALL_PATH := ../src/blynclight/libs/$(IMPLEMENTATION)

TARGET= libblynclight_api.so

SRC= blynclight_api.c
OBJ= $(SRC:.c=.o)

Darwin_SDK=  embrava-sdk
Linux_SDK=   EmbravaSdkForLinux

ifeq ($(SYSTEM),Darwin)
  SDK_ROOT= $(Darwin_SDK)
  API_DIR= SDK_static_lib
  API_ARCHIVE= $(SDK_ROOT)/$(API_DIR)/libblynclightcontrol.a
  API_OBJS=  blynclightcontrol.o
  LIBS=
endif

ifeq ($(SYSTEM),Linux)
  SDK_ROOT= $(Linux_SDK)
  API_DIR= EmbravaApi
  API_ARCHIVE= $(SDK_ROOT)/$(API_DIR)/libembravaapi.a
  API_OBJS= embravaapi.o hid-libusb.o
  LIBS += -lhidapi-hidraw -lusb-1.0
endif

.PHONY: install

all: install

$(TARGET): $(OBJ) $(API_OBJS)
	$(CC) -o $@ $(API_OBJS) $(OBJ) -fPIC -shared $(LIBS)

$(OBJ): $(SDK_ROOT) $(SRC) $(SRC:.c=.h)
	$(CC) -c $(SRC) -I$(SDK_ROOT)/$(API_DIR) -std=gnu99 -fPIC

$(SDK_ROOT):
	curl -L $(URL) | jar x

$(API_OBJS): $(SDK_ROOT)
	ar x $(API_ARCHIVE) $@

$(INSTALL_PATH):
	mkdir -p $@

install: $(INSTALL_PATH) $(TARGET)
	cp $(TARGET) $(INSTALL_PATH)/$(TARGET)

clean:
	@rm -rf *.o __MACOSX

clobber: clean
	@rm -rf $(Darwin_SDK) $(Linux_SDK) $(TARGET)
