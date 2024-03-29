# This file should not be included in the compiled wheel, but should be included in the tarball.

import os, logging
from .stock_pkginit import *

HC_SOURCE_DIR = '../../hub-ctrl'

# Handle environment

if 'CC' in os.environ:
    GCC_CMD = os.environ['CC']

if 'CFLAGS' in os.environ:
    # Example from buildroot: -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -Os -g0 
    COMPILE_ARGS = ( "-Wall -shared -fPIC -flto -fwhole-program -fno-use-linker-plugin "
                     f"{os.environ['CFLAGS']} -o %s %s " )
    HC_CFLAGS = f"-Wall {os.environ['CFLAGS']} -o %s %s -lusb"
else:
    HC_CFLAGS="-Wall -g -O2 -o %s %s -lusb"

HC_COMPILE_CMD=f"{GCC_CMD} {HC_CFLAGS}"

# Duplicated here to bring the correct GCC_CMD over
# Check if the current gcc version supports a particular command-line option
def check_gcc_option(option):
    cmd = "%s %s -S -o /dev/null -xc /dev/null > /dev/null 2>&1" % (
        GCC_CMD, option)
    res = os.system(cmd)
    return res == 0

def build_hub_ctrl():
    srcdir = os.path.dirname(os.path.realpath(__file__))
    hubdir = os.path.join(srcdir, HC_SOURCE_DIR)
    srcfiles = get_abs_files(hubdir, HC_SOURCE_FILES)
    destlib = os.getenv("OVERRIDE_HUBCTRL_OUTPUT",get_abs_files(srcdir, [HC_TARGET])[0])
    logging.debug(f"Looking for {destlib}")
    if check_build_code(srcfiles, destlib):
        logging.info("Building C code module %s", HC_TARGET)
        do_build_code(HC_COMPILE_CMD % (destlib, ' '.join(srcfiles)))

def build_chelper():
    srcdir = os.path.dirname(os.path.realpath(__file__))
    srcfiles = get_abs_files(srcdir, SOURCE_FILES)
    ofiles = get_abs_files(srcdir, OTHER_FILES)
    destlib = os.getenv("OVERRIDE_CHELPER_OUTPUT",get_abs_files(srcdir, [DEST_LIB])[0])
    logging.debug(f"Looking for {destlib}")
    if check_build_code(srcfiles+ofiles+[__file__], destlib):
        if check_gcc_option(SSE_FLAGS):
            cmd = "%s %s %s" % (GCC_CMD, SSE_FLAGS, COMPILE_ARGS)
        else:
            cmd = "%s %s" % (GCC_CMD, COMPILE_ARGS)
        logging.info("Building C code module %s", DEST_LIB)
        build_cmd = cmd % (destlib, ' '.join(srcfiles))
        logging.info(build_cmd)
        do_build_code(build_cmd)

