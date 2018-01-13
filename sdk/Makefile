
# Fill out the form at:
#
# https://www.embrava.com/pages/embrava-software-sdk
#
# They will mail you links for Windows, Linux and Mac SDKs.  When you
# receive the SDK URLs, invoke make with the URL for your platform:
#
# $ make -f Makefile URL=https://url/for/the/sdk
#
# The makefile takes apart the static library archive and constructs a
# shared library which can then be used by python.



include Makefile.$(shell uname)

LIB_DIR= ../src/blynclight/libs

install: $(TARGET)
	$(MV) $(TARGET) $(LIB_DIR)/$(shell uname)/$(TARGET)
