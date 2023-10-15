# This file should not be included in the compiled wheel, but should be included in the tarball.

import os, logging
from .stock_pkginit import *

HC_SOURCE_DIR = '../../hub-ctrl'

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
        do_build_code(cmd % (destlib, ' '.join(srcfiles)))

