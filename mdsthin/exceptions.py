#
# Copyright (c) 2024, Massachusetts Institute of Technology All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

EXCEPTION_MAP = {}
EXCEPTION_PREFIX_MAP = {}

def STATUS_OK(status):
    return (status & 1)

def STATUS_NOT_OK(status):
    return not (status & 1)

def STATUS_FACILITY(status):
    return (status >> 16)

def STATUS_MESSAGE(status):
    return (status >> 3) & 0b1111111111111

def STATUS_SEVERITY(status):
    return (status & 0b111)

def getException(status):
    return EXCEPTION_MAP.get(status, MdsException(f'Unknown status: {status}'))

def getExceptionFromError(error):
    if type(error) is str and error.startswith('%'):
        prefix = error.split(',', maxsplit=1)[0]
        return EXCEPTION_PREFIX_MAP.get(prefix, MdsException(error))

    return MdsException(error)

class MdsException(Exception):
    pass

class ServerException(MdsException):
    pass

class ServerNOT_DISPATCHED(ServerException):
    status = 266436616
    prefix = "%SERVER-W-NOT_DISPATCHED"
    def __init__(self):
        Exception.__init__(self, "%SERVER-W-NOT_DISPATCHED, Action not dispatched, depended on failed action")

EXCEPTION_MAP[ServerNOT_DISPATCHED.status] = ServerNOT_DISPATCHED
EXCEPTION_PREFIX_MAP[ServerNOT_DISPATCHED.prefix] = ServerNOT_DISPATCHED

class ServerINVALID_DEPENDENCY(ServerException):
    status = 266436626
    prefix = "%SERVER-E-INVALID_DEPENDENCY"
    def __init__(self):
        Exception.__init__(self, "%SERVER-E-INVALID_DEPENDENCY, Action dependency cannot be evaluated")

EXCEPTION_MAP[ServerINVALID_DEPENDENCY.status] = ServerINVALID_DEPENDENCY
EXCEPTION_PREFIX_MAP[ServerINVALID_DEPENDENCY.prefix] = ServerINVALID_DEPENDENCY

class ServerCANT_HAPPEN(ServerException):
    status = 266436634
    prefix = "%SERVER-E-CANT_HAPPEN"
    def __init__(self):
        Exception.__init__(self, "%SERVER-E-CANT_HAPPEN, Action contains circular dependency or depends on action which was not dispatched")

EXCEPTION_MAP[ServerCANT_HAPPEN.status] = ServerCANT_HAPPEN
EXCEPTION_PREFIX_MAP[ServerCANT_HAPPEN.prefix] = ServerCANT_HAPPEN

class ServerINVSHOT(ServerException):
    status = 266436642
    prefix = "%SERVER-E-INVSHOT"
    def __init__(self):
        Exception.__init__(self, "%SERVER-E-INVSHOT, Invalid shot number, cannot dispatch actions in model")

EXCEPTION_MAP[ServerINVSHOT.status] = ServerINVSHOT
EXCEPTION_PREFIX_MAP[ServerINVSHOT.prefix] = ServerINVSHOT

class ServerABORT(ServerException):
    status = 266436658
    prefix = "%SERVER-E-ABORT"
    def __init__(self):
        Exception.__init__(self, "%SERVER-E-ABORT, Server action was aborted")

EXCEPTION_MAP[ServerABORT.status] = ServerABORT
EXCEPTION_PREFIX_MAP[ServerABORT.prefix] = ServerABORT

class ServerPATH_DOWN(ServerException):
    status = 266436674
    prefix = "%SERVER-E-PATH_DOWN"
    def __init__(self):
        Exception.__init__(self, "%SERVER-E-PATH_DOWN, Path to server lost")

EXCEPTION_MAP[ServerPATH_DOWN.status] = ServerPATH_DOWN
EXCEPTION_PREFIX_MAP[ServerPATH_DOWN.prefix] = ServerPATH_DOWN

class ServerSOCKET_ADDR_ERROR(ServerException):
    status = 266436682
    prefix = "%SERVER-E-SOCKET_ADDR_ERROR"
    def __init__(self):
        Exception.__init__(self, "%SERVER-E-SOCKET_ADDR_ERROR, Cannot obtain ip address socket is bound to")

EXCEPTION_MAP[ServerSOCKET_ADDR_ERROR.status] = ServerSOCKET_ADDR_ERROR
EXCEPTION_PREFIX_MAP[ServerSOCKET_ADDR_ERROR.prefix] = ServerSOCKET_ADDR_ERROR

class ServerINVALID_ACTION_OPERATION(ServerException):
    status = 266436690
    prefix = "%SERVER-E-INVALID_ACTION_OPERATION"
    def __init__(self):
        Exception.__init__(self, "%SERVER-E-INVALID_ACTION_OPERATION, Unknown action operation")

EXCEPTION_MAP[ServerINVALID_ACTION_OPERATION.status] = ServerINVALID_ACTION_OPERATION
EXCEPTION_PREFIX_MAP[ServerINVALID_ACTION_OPERATION.prefix] = ServerINVALID_ACTION_OPERATION

class DevException(MdsException):
    pass

class DevBAD_ENDIDX(DevException):
    status = 662470666
    prefix = "%DEV-E-BAD_ENDIDX"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ENDIDX, Unable to read end index for channel")

EXCEPTION_MAP[DevBAD_ENDIDX.status] = DevBAD_ENDIDX
EXCEPTION_PREFIX_MAP[DevBAD_ENDIDX.prefix] = DevBAD_ENDIDX

class DevBAD_FILTER(DevException):
    status = 662470674
    prefix = "%DEV-E-BAD_FILTER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FILTER, Illegal filter selected")

EXCEPTION_MAP[DevBAD_FILTER.status] = DevBAD_FILTER
EXCEPTION_PREFIX_MAP[DevBAD_FILTER.prefix] = DevBAD_FILTER

class DevBAD_FREQ(DevException):
    status = 662470682
    prefix = "%DEV-E-BAD_FREQ"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FREQ, Illegal digitization frequency selected")

EXCEPTION_MAP[DevBAD_FREQ.status] = DevBAD_FREQ
EXCEPTION_PREFIX_MAP[DevBAD_FREQ.prefix] = DevBAD_FREQ

class DevBAD_GAIN(DevException):
    status = 662470690
    prefix = "%DEV-E-BAD_GAIN"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_GAIN, Illegal gain selected")

EXCEPTION_MAP[DevBAD_GAIN.status] = DevBAD_GAIN
EXCEPTION_PREFIX_MAP[DevBAD_GAIN.prefix] = DevBAD_GAIN

class DevBAD_HEADER(DevException):
    status = 662470698
    prefix = "%DEV-E-BAD_HEADER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_HEADER, Unable to read header selection")

EXCEPTION_MAP[DevBAD_HEADER.status] = DevBAD_HEADER
EXCEPTION_PREFIX_MAP[DevBAD_HEADER.prefix] = DevBAD_HEADER

class DevBAD_HEADER_IDX(DevException):
    status = 662470706
    prefix = "%DEV-E-BAD_HEADER_IDX"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_HEADER_IDX, Unknown header configuration index")

EXCEPTION_MAP[DevBAD_HEADER_IDX.status] = DevBAD_HEADER_IDX
EXCEPTION_PREFIX_MAP[DevBAD_HEADER_IDX.prefix] = DevBAD_HEADER_IDX

class DevBAD_MEMORIES(DevException):
    status = 662470714
    prefix = "%DEV-E-BAD_MEMORIES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MEMORIES, Unable to read number of memory modules")

EXCEPTION_MAP[DevBAD_MEMORIES.status] = DevBAD_MEMORIES
EXCEPTION_PREFIX_MAP[DevBAD_MEMORIES.prefix] = DevBAD_MEMORIES

class DevBAD_MODE(DevException):
    status = 662470722
    prefix = "%DEV-E-BAD_MODE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MODE, Illegal mode selected")

EXCEPTION_MAP[DevBAD_MODE.status] = DevBAD_MODE
EXCEPTION_PREFIX_MAP[DevBAD_MODE.prefix] = DevBAD_MODE

class DevBAD_NAME(DevException):
    status = 662470730
    prefix = "%DEV-E-BAD_NAME"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_NAME, Unable to read module name")

EXCEPTION_MAP[DevBAD_NAME.status] = DevBAD_NAME
EXCEPTION_PREFIX_MAP[DevBAD_NAME.prefix] = DevBAD_NAME

class DevBAD_OFFSET(DevException):
    status = 662470738
    prefix = "%DEV-E-BAD_OFFSET"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_OFFSET, Illegal offset selected")

EXCEPTION_MAP[DevBAD_OFFSET.status] = DevBAD_OFFSET
EXCEPTION_PREFIX_MAP[DevBAD_OFFSET.prefix] = DevBAD_OFFSET

class DevBAD_STARTIDX(DevException):
    status = 662470746
    prefix = "%DEV-E-BAD_STARTIDX"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_STARTIDX, Unable to read start index for channel")

EXCEPTION_MAP[DevBAD_STARTIDX.status] = DevBAD_STARTIDX
EXCEPTION_PREFIX_MAP[DevBAD_STARTIDX.prefix] = DevBAD_STARTIDX

class DevNOT_TRIGGERED(DevException):
    status = 662470754
    prefix = "%DEV-E-NOT_TRIGGERED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NOT_TRIGGERED, Device was not triggered, check wires and triggering device")

EXCEPTION_MAP[DevNOT_TRIGGERED.status] = DevNOT_TRIGGERED
EXCEPTION_PREFIX_MAP[DevNOT_TRIGGERED.prefix] = DevNOT_TRIGGERED

class DevFREQ_TOO_HIGH(DevException):
    status = 662470762
    prefix = "%DEV-E-FREQ_TOO_HIGH"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-FREQ_TOO_HIGH, The frequency is set to high for the requested number of channels")

EXCEPTION_MAP[DevFREQ_TOO_HIGH.status] = DevFREQ_TOO_HIGH
EXCEPTION_PREFIX_MAP[DevFREQ_TOO_HIGH.prefix] = DevFREQ_TOO_HIGH

class DevINVALID_NOC(DevException):
    status = 662470770
    prefix = "%DEV-E-INVALID_NOC"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INVALID_NOC, The NOC (number of channels) requested is greater than the physical number of channels")

EXCEPTION_MAP[DevINVALID_NOC.status] = DevINVALID_NOC
EXCEPTION_PREFIX_MAP[DevINVALID_NOC.prefix] = DevINVALID_NOC

class DevRANGE_MISMATCH(DevException):
    status = 662470778
    prefix = "%DEV-E-RANGE_MISMATCH"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-RANGE_MISMATCH, The range specified on the menu doesn't match the range setting on the device")

EXCEPTION_MAP[DevRANGE_MISMATCH.status] = DevRANGE_MISMATCH
EXCEPTION_PREFIX_MAP[DevRANGE_MISMATCH.prefix] = DevRANGE_MISMATCH

class DevBAD_VERBS(DevException):
    status = 662470794
    prefix = "%DEV-E-BAD_VERBS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_VERBS, Error reading interpreter list (:VERBS)")

EXCEPTION_MAP[DevBAD_VERBS.status] = DevBAD_VERBS
EXCEPTION_PREFIX_MAP[DevBAD_VERBS.prefix] = DevBAD_VERBS

class DevBAD_COMMANDS(DevException):
    status = 662470802
    prefix = "%DEV-E-BAD_COMMANDS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_COMMANDS, Error reading command list")

EXCEPTION_MAP[DevBAD_COMMANDS.status] = DevBAD_COMMANDS
EXCEPTION_PREFIX_MAP[DevBAD_COMMANDS.prefix] = DevBAD_COMMANDS

class DevINV_SETUP(DevException):
    status = 662470906
    prefix = "%DEV-E-INV_SETUP"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INV_SETUP, Device was not properly set up")

EXCEPTION_MAP[DevINV_SETUP.status] = DevINV_SETUP
EXCEPTION_PREFIX_MAP[DevINV_SETUP.prefix] = DevINV_SETUP

class DevPYDEVICE_NOT_FOUND(DevException):
    status = 662470914
    prefix = "%DEV-E-PYDEVICE_NOT_FOUND"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-PYDEVICE_NOT_FOUND, Python device class not found")

EXCEPTION_MAP[DevPYDEVICE_NOT_FOUND.status] = DevPYDEVICE_NOT_FOUND
EXCEPTION_PREFIX_MAP[DevPYDEVICE_NOT_FOUND.prefix] = DevPYDEVICE_NOT_FOUND

class DevPY_INTERFACE_LIBRARY_NOT_FOUND(DevException):
    status = 662470922
    prefix = "%DEV-E-PY_INTERFACE_LIBRARY_NOT_FOUND"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-PY_INTERFACE_LIBRARY_NOT_FOUND, The needed device hardware interface library could not be loaded")

EXCEPTION_MAP[DevPY_INTERFACE_LIBRARY_NOT_FOUND.status] = DevPY_INTERFACE_LIBRARY_NOT_FOUND
EXCEPTION_PREFIX_MAP[DevPY_INTERFACE_LIBRARY_NOT_FOUND.prefix] = DevPY_INTERFACE_LIBRARY_NOT_FOUND

class DevIO_STUCK(DevException):
    status = 662470930
    prefix = "%DEV-E-IO_STUCK"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-IO_STUCK, I/O to Device is stuck. Check network connection and board status")

EXCEPTION_MAP[DevIO_STUCK.status] = DevIO_STUCK
EXCEPTION_PREFIX_MAP[DevIO_STUCK.prefix] = DevIO_STUCK

class DevUNKNOWN_STATE(DevException):
    status = 662470938
    prefix = "%DEV-E-UNKNOWN_STATE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-UNKNOWN_STATE, Device returned unrecognized state string")

EXCEPTION_MAP[DevUNKNOWN_STATE.status] = DevUNKNOWN_STATE
EXCEPTION_PREFIX_MAP[DevUNKNOWN_STATE.prefix] = DevUNKNOWN_STATE

class DevWRONG_TREE(DevException):
    status = 662470946
    prefix = "%DEV-E-WRONG_TREE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-WRONG_TREE, Attempt to digitizerinto different tree than it was armed with")

EXCEPTION_MAP[DevWRONG_TREE.status] = DevWRONG_TREE
EXCEPTION_PREFIX_MAP[DevWRONG_TREE.prefix] = DevWRONG_TREE

class DevWRONG_PATH(DevException):
    status = 662470954
    prefix = "%DEV-E-WRONG_PATH"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-WRONG_PATH, Attempt to store digitizer into different path than it was armed with")

EXCEPTION_MAP[DevWRONG_PATH.status] = DevWRONG_PATH
EXCEPTION_PREFIX_MAP[DevWRONG_PATH.prefix] = DevWRONG_PATH

class DevWRONG_SHOT(DevException):
    status = 662470962
    prefix = "%DEV-E-WRONG_SHOT"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-WRONG_SHOT, Attempt to store digitizer into different shot than it was armed with")

EXCEPTION_MAP[DevWRONG_SHOT.status] = DevWRONG_SHOT
EXCEPTION_PREFIX_MAP[DevWRONG_SHOT.prefix] = DevWRONG_SHOT

class DevOFFLINE(DevException):
    status = 662470970
    prefix = "%DEV-E-OFFLINE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-OFFLINE, Device is not on line. Check network connection")

EXCEPTION_MAP[DevOFFLINE.status] = DevOFFLINE
EXCEPTION_PREFIX_MAP[DevOFFLINE.prefix] = DevOFFLINE

class DevTRIGGERED_NOT_STORED(DevException):
    status = 662470978
    prefix = "%DEV-E-TRIGGERED_NOT_STORED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-TRIGGERED_NOT_STORED, Device was triggered but not stored")

EXCEPTION_MAP[DevTRIGGERED_NOT_STORED.status] = DevTRIGGERED_NOT_STORED
EXCEPTION_PREFIX_MAP[DevTRIGGERED_NOT_STORED.prefix] = DevTRIGGERED_NOT_STORED

class DevNO_NAME_SPECIFIED(DevException):
    status = 662470986
    prefix = "%DEV-E-NO_NAME_SPECIFIED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NO_NAME_SPECIFIED, Device name must be specifed - pleas fill it in")

EXCEPTION_MAP[DevNO_NAME_SPECIFIED.status] = DevNO_NAME_SPECIFIED
EXCEPTION_PREFIX_MAP[DevNO_NAME_SPECIFIED.prefix] = DevNO_NAME_SPECIFIED

class DevBAD_ACTIVE_CHAN(DevException):
    status = 662470994
    prefix = "%DEV-E-BAD_ACTIVE_CHAN"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVE_CHAN, Active channels either not available or invalid")

EXCEPTION_MAP[DevBAD_ACTIVE_CHAN.status] = DevBAD_ACTIVE_CHAN
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVE_CHAN.prefix] = DevBAD_ACTIVE_CHAN

class DevBAD_TRIG_SRC(DevException):
    status = 662471002
    prefix = "%DEV-E-BAD_TRIG_SRC"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_TRIG_SRC, Trigger source either not available or invalid")

EXCEPTION_MAP[DevBAD_TRIG_SRC.status] = DevBAD_TRIG_SRC
EXCEPTION_PREFIX_MAP[DevBAD_TRIG_SRC.prefix] = DevBAD_TRIG_SRC

class DevBAD_CLOCK_SRC(DevException):
    status = 662471010
    prefix = "%DEV-E-BAD_CLOCK_SRC"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLOCK_SRC, Clock source either not available or invalid")

EXCEPTION_MAP[DevBAD_CLOCK_SRC.status] = DevBAD_CLOCK_SRC
EXCEPTION_PREFIX_MAP[DevBAD_CLOCK_SRC.prefix] = DevBAD_CLOCK_SRC

class DevBAD_PRE_TRIG(DevException):
    status = 662471018
    prefix = "%DEV-E-BAD_PRE_TRIG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PRE_TRIG, Pre trigger samples either not available or invalid")

EXCEPTION_MAP[DevBAD_PRE_TRIG.status] = DevBAD_PRE_TRIG
EXCEPTION_PREFIX_MAP[DevBAD_PRE_TRIG.prefix] = DevBAD_PRE_TRIG

class DevBAD_POST_TRIG(DevException):
    status = 662471026
    prefix = "%DEV-E-BAD_POST_TRIG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_POST_TRIG, Post trigger samples either not available or invalid")

EXCEPTION_MAP[DevBAD_POST_TRIG.status] = DevBAD_POST_TRIG
EXCEPTION_PREFIX_MAP[DevBAD_POST_TRIG.prefix] = DevBAD_POST_TRIG

class DevBAD_CLOCK_FREQ(DevException):
    status = 662471034
    prefix = "%DEV-E-BAD_CLOCK_FREQ"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLOCK_FREQ, Clock frequency either not available or invalid")

EXCEPTION_MAP[DevBAD_CLOCK_FREQ.status] = DevBAD_CLOCK_FREQ
EXCEPTION_PREFIX_MAP[DevBAD_CLOCK_FREQ.prefix] = DevBAD_CLOCK_FREQ

class DevTRIGGER_FAILED(DevException):
    status = 662471042
    prefix = "%DEV-E-TRIGGER_FAILED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-TRIGGER_FAILED, Device trigger method failed")

EXCEPTION_MAP[DevTRIGGER_FAILED.status] = DevTRIGGER_FAILED
EXCEPTION_PREFIX_MAP[DevTRIGGER_FAILED.prefix] = DevTRIGGER_FAILED

class DevERROR_READING_CHANNEL(DevException):
    status = 662471050
    prefix = "%DEV-E-ERROR_READING_CHANNEL"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-ERROR_READING_CHANNEL, Error reading data for channel from device")

EXCEPTION_MAP[DevERROR_READING_CHANNEL.status] = DevERROR_READING_CHANNEL
EXCEPTION_PREFIX_MAP[DevERROR_READING_CHANNEL.prefix] = DevERROR_READING_CHANNEL

class DevERROR_DOING_INIT(DevException):
    status = 662471058
    prefix = "%DEV-E-ERROR_DOING_INIT"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-ERROR_DOING_INIT, Error sending ARM command to device")

EXCEPTION_MAP[DevERROR_DOING_INIT.status] = DevERROR_DOING_INIT
EXCEPTION_PREFIX_MAP[DevERROR_DOING_INIT.prefix] = DevERROR_DOING_INIT

class DevNORMAL(DevException):
    status = 662471065
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevBAD_FRAMES(DevException):
    status = 662471074
    prefix = "%DEV-E-BAD_FRAMES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FRAMES, Frame count must be less than or equal to 2048")

EXCEPTION_MAP[DevBAD_FRAMES.status] = DevBAD_FRAMES
EXCEPTION_PREFIX_MAP[DevBAD_FRAMES.prefix] = DevBAD_FRAMES

class DevBAD_FRAME_SELECT(DevException):
    status = 662471082
    prefix = "%DEV-E-BAD_FRAME_SELECT"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FRAME_SELECT, Frame interval must be 1,2,4,8,16,32 or 64")

EXCEPTION_MAP[DevBAD_FRAME_SELECT.status] = DevBAD_FRAME_SELECT
EXCEPTION_PREFIX_MAP[DevBAD_FRAME_SELECT.prefix] = DevBAD_FRAME_SELECT

class DevBAD_NUM_STATES(DevException):
    status = 662471090
    prefix = "%DEV-E-BAD_NUM_STATES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_NUM_STATES, Number of states must be between 1 and 4")

EXCEPTION_MAP[DevBAD_NUM_STATES.status] = DevBAD_NUM_STATES
EXCEPTION_PREFIX_MAP[DevBAD_NUM_STATES.prefix] = DevBAD_NUM_STATES

class DevBAD_PERIOD(DevException):
    status = 662471098
    prefix = "%DEV-E-BAD_PERIOD"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PERIOD, Period must be .5,1,2,4,8,16,32,64,128,256,512,1024,2048,4096 or 8192 msec")

EXCEPTION_MAP[DevBAD_PERIOD.status] = DevBAD_PERIOD
EXCEPTION_PREFIX_MAP[DevBAD_PERIOD.prefix] = DevBAD_PERIOD

class DevBAD_PIXEL_SELECT(DevException):
    status = 662471106
    prefix = "%DEV-E-BAD_PIXEL_SELECT"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PIXEL_SELECT, Pixel selection must be an array of 256 boolean values")

EXCEPTION_MAP[DevBAD_PIXEL_SELECT.status] = DevBAD_PIXEL_SELECT
EXCEPTION_PREFIX_MAP[DevBAD_PIXEL_SELECT.prefix] = DevBAD_PIXEL_SELECT

class DevDATA_CORRUPTED(DevException):
    status = 662471114
    prefix = "%DEV-E-DATA_CORRUPTED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-DATA_CORRUPTED, Data in memory is corrupted or framing error detected, no data stored")

EXCEPTION_MAP[DevDATA_CORRUPTED.status] = DevDATA_CORRUPTED
EXCEPTION_PREFIX_MAP[DevDATA_CORRUPTED.prefix] = DevDATA_CORRUPTED

class DevTOO_MANY_FRAMES(DevException):
    status = 662471122
    prefix = "%DEV-E-TOO_MANY_FRAMES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-TOO_MANY_FRAMES, Over 8192 frame start indicators in data read from memory")

EXCEPTION_MAP[DevTOO_MANY_FRAMES.status] = DevTOO_MANY_FRAMES
EXCEPTION_PREFIX_MAP[DevTOO_MANY_FRAMES.prefix] = DevTOO_MANY_FRAMES

class DevNORMAL(DevException):
    status = 662471465
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevINVALID_DATA(DevException):
    status = 662471476
    prefix = "%DEV-F-INVALID_DATA"
    def __init__(self):
        Exception.__init__(self, "%DEV-F-INVALID_DATA, Ignoring invalid data in channel !SL")

EXCEPTION_MAP[DevINVALID_DATA.status] = DevINVALID_DATA
EXCEPTION_PREFIX_MAP[DevINVALID_DATA.prefix] = DevINVALID_DATA

class DevNO_DATA(DevException):
    status = 662471482
    prefix = "%DEV-E-NO_DATA"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NO_DATA, No valid data was found for any channel")

EXCEPTION_MAP[DevNO_DATA.status] = DevNO_DATA
EXCEPTION_PREFIX_MAP[DevNO_DATA.prefix] = DevNO_DATA

class DevINVCLKFRQ(DevException):
    status = 662471866
    prefix = "%DEV-E-INVCLKFRQ"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INVCLKFRQ, Invalid clock frequency")

EXCEPTION_MAP[DevINVCLKFRQ.status] = DevINVCLKFRQ
EXCEPTION_PREFIX_MAP[DevINVCLKFRQ.prefix] = DevINVCLKFRQ

class DevINVDELDUR(DevException):
    status = 662471874
    prefix = "%DEV-E-INVDELDUR"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INVDELDUR, Invalid pulse delay or duration, must be less than 655 seconds")

EXCEPTION_MAP[DevINVDELDUR.status] = DevINVDELDUR
EXCEPTION_PREFIX_MAP[DevINVDELDUR.prefix] = DevINVDELDUR

class DevINVOUTCTR(DevException):
    status = 662471882
    prefix = "%DEV-E-INVOUTCTR"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INVOUTCTR, Invalid output mode selected")

EXCEPTION_MAP[DevINVOUTCTR.status] = DevINVOUTCTR
EXCEPTION_PREFIX_MAP[DevINVOUTCTR.prefix] = DevINVOUTCTR

class DevINVPSEUDODEV(DevException):
    status = 662471890
    prefix = "%DEV-E-INVPSEUDODEV"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INVPSEUDODEV, Invalid pseudo device attached to this decoder channel")

EXCEPTION_MAP[DevINVPSEUDODEV.status] = DevINVPSEUDODEV
EXCEPTION_PREFIX_MAP[DevINVPSEUDODEV.prefix] = DevINVPSEUDODEV

class DevINVTRGMOD(DevException):
    status = 662471898
    prefix = "%DEV-E-INVTRGMOD"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INVTRGMOD, Invalid trigger mode selected")

EXCEPTION_MAP[DevINVTRGMOD.status] = DevINVTRGMOD
EXCEPTION_PREFIX_MAP[DevINVTRGMOD.prefix] = DevINVTRGMOD

class DevNOPSEUDODEV(DevException):
    status = 662471907
    prefix = "%DEV-I-NOPSEUDODEV"
    def __init__(self):
        Exception.__init__(self, "%DEV-I-NOPSEUDODEV, No Pseudo device attached to this channel ... disabling")

EXCEPTION_MAP[DevNOPSEUDODEV.status] = DevNOPSEUDODEV
EXCEPTION_PREFIX_MAP[DevNOPSEUDODEV.prefix] = DevNOPSEUDODEV

class DevTOO_MANY_EVENTS(DevException):
    status = 662471914
    prefix = "%DEV-E-TOO_MANY_EVENTS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-TOO_MANY_EVENTS, More than 16 events used by this decoder")

EXCEPTION_MAP[DevTOO_MANY_EVENTS.status] = DevTOO_MANY_EVENTS
EXCEPTION_PREFIX_MAP[DevTOO_MANY_EVENTS.prefix] = DevTOO_MANY_EVENTS

class DevNORMAL(DevException):
    status = 662472265
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevOVERFLOW(DevException):
    status = 662472275
    prefix = "%DEV-I-OVERFLOW"
    def __init__(self):
        Exception.__init__(self, "%DEV-I-OVERFLOW, Triggers received after overflow")

EXCEPTION_MAP[DevOVERFLOW.status] = DevOVERFLOW
EXCEPTION_PREFIX_MAP[DevOVERFLOW.prefix] = DevOVERFLOW

class DevTRIG_LIM(DevException):
    status = 662472284
    prefix = "%DEV-F-TRIG_LIM"
    def __init__(self):
        Exception.__init__(self, "%DEV-F-TRIG_LIM, Trigger limit possibly exceeded")

EXCEPTION_MAP[DevTRIG_LIM.status] = DevTRIG_LIM
EXCEPTION_PREFIX_MAP[DevTRIG_LIM.prefix] = DevTRIG_LIM

class DevNORMAL(DevException):
    status = 662472665
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevDIGNOTSTRARRAY(DevException):
    status = 662472674
    prefix = "%DEV-E-DIGNOTSTRARRAY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-DIGNOTSTRARRAY, The digitizer names must be an array of strings")

EXCEPTION_MAP[DevDIGNOTSTRARRAY.status] = DevDIGNOTSTRARRAY
EXCEPTION_PREFIX_MAP[DevDIGNOTSTRARRAY.prefix] = DevDIGNOTSTRARRAY

class DevNODIG(DevException):
    status = 662472682
    prefix = "%DEV-E-NODIG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NODIG, The digitizer names must be specified")

EXCEPTION_MAP[DevNODIG.status] = DevNODIG
EXCEPTION_PREFIX_MAP[DevNODIG.prefix] = DevNODIG

class DevMEMNOTSTRARRAY(DevException):
    status = 662472690
    prefix = "%DEV-E-MEMNOTSTRARRAY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-MEMNOTSTRARRAY, The memory names must be an array of strings")

EXCEPTION_MAP[DevMEMNOTSTRARRAY.status] = DevMEMNOTSTRARRAY
EXCEPTION_PREFIX_MAP[DevMEMNOTSTRARRAY.prefix] = DevMEMNOTSTRARRAY

class DevNOMEM(DevException):
    status = 662472698
    prefix = "%DEV-E-NOMEM"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NOMEM, The memory names must be specified")

EXCEPTION_MAP[DevNOMEM.status] = DevNOMEM
EXCEPTION_PREFIX_MAP[DevNOMEM.prefix] = DevNOMEM

class DevPHASE_LOST(DevException):
    status = 662472706
    prefix = "%DEV-E-PHASE_LOST"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-PHASE_LOST, Data phase lost No FERA data stored")

EXCEPTION_MAP[DevPHASE_LOST.status] = DevPHASE_LOST
EXCEPTION_PREFIX_MAP[DevPHASE_LOST.prefix] = DevPHASE_LOST

class DevCONFUSED(DevException):
    status = 662472716
    prefix = "%DEV-F-CONFUSED"
    def __init__(self):
        Exception.__init__(self, "%DEV-F-CONFUSED, Fera Data inconsitant. Data for this point zered")

EXCEPTION_MAP[DevCONFUSED.status] = DevCONFUSED
EXCEPTION_PREFIX_MAP[DevCONFUSED.prefix] = DevCONFUSED

class DevOVER_RUN(DevException):
    status = 662472724
    prefix = "%DEV-F-OVER_RUN"
    def __init__(self):
        Exception.__init__(self, "%DEV-F-OVER_RUN, Possible FERA memory overrun, too many triggers")

EXCEPTION_MAP[DevOVER_RUN.status] = DevOVER_RUN
EXCEPTION_PREFIX_MAP[DevOVER_RUN.prefix] = DevOVER_RUN

class DevOVERFLOW(DevException):
    status = 662472731
    prefix = "%DEV-I-OVERFLOW"
    def __init__(self):
        Exception.__init__(self, "%DEV-I-OVERFLOW, Possible FERA data saturated. Data point zeroed")

EXCEPTION_MAP[DevOVERFLOW.status] = DevOVERFLOW
EXCEPTION_PREFIX_MAP[DevOVERFLOW.prefix] = DevOVERFLOW

class DevNORMAL(DevException):
    status = 662473065
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevDLYCHNG(DevException):
    status = 662473076
    prefix = "%DEV-F-DLYCHNG"
    def __init__(self):
        Exception.__init__(self, "%DEV-F-DLYCHNG, HM650 requested delay can not be processed by hardware")

EXCEPTION_MAP[DevDLYCHNG.status] = DevDLYCHNG
EXCEPTION_PREFIX_MAP[DevDLYCHNG.prefix] = DevDLYCHNG

class DevNORMAL(DevException):
    status = 662473465
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevWRONG_POD_TYPE(DevException):
    status = 662473474
    prefix = "%DEV-E-WRONG_POD_TYPE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-WRONG_POD_TYPE, HV40321A n and p can only be used with the HV4032 device")

EXCEPTION_MAP[DevWRONG_POD_TYPE.status] = DevWRONG_POD_TYPE
EXCEPTION_PREFIX_MAP[DevWRONG_POD_TYPE.prefix] = DevWRONG_POD_TYPE

class DevNORMAL(DevException):
    status = 662473865
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevWRONG_POD_TYPE(DevException):
    status = 662473874
    prefix = "%DEV-E-WRONG_POD_TYPE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-WRONG_POD_TYPE, HV1443 can only be used with the HV1440 device")

EXCEPTION_MAP[DevWRONG_POD_TYPE.status] = DevWRONG_POD_TYPE
EXCEPTION_PREFIX_MAP[DevWRONG_POD_TYPE.prefix] = DevWRONG_POD_TYPE

class DevBAD_FRAME(DevException):
    status = 662473882
    prefix = "%DEV-E-BAD_FRAME"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FRAME, HV1440 could not read the frame")

EXCEPTION_MAP[DevBAD_FRAME.status] = DevBAD_FRAME
EXCEPTION_PREFIX_MAP[DevBAD_FRAME.prefix] = DevBAD_FRAME

class DevBAD_RANGE(DevException):
    status = 662473890
    prefix = "%DEV-E-BAD_RANGE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_RANGE, HV1440 could not read the range")

EXCEPTION_MAP[DevBAD_RANGE.status] = DevBAD_RANGE
EXCEPTION_PREFIX_MAP[DevBAD_RANGE.prefix] = DevBAD_RANGE

class DevOUTRNG(DevException):
    status = 662473898
    prefix = "%DEV-E-OUTRNG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-OUTRNG, HV1440 out of range")

EXCEPTION_MAP[DevOUTRNG.status] = DevOUTRNG
EXCEPTION_PREFIX_MAP[DevOUTRNG.prefix] = DevOUTRNG

class DevSTUCK(DevException):
    status = 662473906
    prefix = "%DEV-E-STUCK"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-STUCK, HV1440 not responding with Q")

EXCEPTION_MAP[DevSTUCK.status] = DevSTUCK
EXCEPTION_PREFIX_MAP[DevSTUCK.prefix] = DevSTUCK

class DevBAD_PRE_TRIGGER(DevException):
    status = 662474266
    prefix = "%DEV-E-BAD_PRE_TRIGGER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PRE_TRIGGER, Bad pretrigger specified, specify a value of 0,1,2,3,4,5,6 or 7")

EXCEPTION_MAP[DevBAD_PRE_TRIGGER.status] = DevBAD_PRE_TRIGGER
EXCEPTION_PREFIX_MAP[DevBAD_PRE_TRIGGER.prefix] = DevBAD_PRE_TRIGGER

class DevBAD_ACT_MEMORY(DevException):
    status = 662474274
    prefix = "%DEV-E-BAD_ACT_MEMORY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACT_MEMORY, Bad active memory specified, specify a value of 1,2,3,4,5,6,7 or 8")

EXCEPTION_MAP[DevBAD_ACT_MEMORY.status] = DevBAD_ACT_MEMORY
EXCEPTION_PREFIX_MAP[DevBAD_ACT_MEMORY.prefix] = DevBAD_ACT_MEMORY

class DevBAD_GAIN(DevException):
    status = 662474282
    prefix = "%DEV-E-BAD_GAIN"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_GAIN, Bad gain specified, specify a value of 1,2,4 or 8")

EXCEPTION_MAP[DevBAD_GAIN.status] = DevBAD_GAIN
EXCEPTION_PREFIX_MAP[DevBAD_GAIN.prefix] = DevBAD_GAIN

class DevBAD_WAVE_LENGTH(DevException):
    status = 662474666
    prefix = "%DEV-E-BAD_WAVE_LENGTH"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_WAVE_LENGTH, Bad wave length specified, specify value between 0 and 13000")

EXCEPTION_MAP[DevBAD_WAVE_LENGTH.status] = DevBAD_WAVE_LENGTH
EXCEPTION_PREFIX_MAP[DevBAD_WAVE_LENGTH.prefix] = DevBAD_WAVE_LENGTH

class DevBAD_SLIT_WIDTH(DevException):
    status = 662474674
    prefix = "%DEV-E-BAD_SLIT_WIDTH"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_SLIT_WIDTH, Bad slit width specified, specify value between 0 and 500")

EXCEPTION_MAP[DevBAD_SLIT_WIDTH.status] = DevBAD_SLIT_WIDTH
EXCEPTION_PREFIX_MAP[DevBAD_SLIT_WIDTH.prefix] = DevBAD_SLIT_WIDTH

class DevBAD_NUM_SPECTRA(DevException):
    status = 662474682
    prefix = "%DEV-E-BAD_NUM_SPECTRA"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_NUM_SPECTRA, Bad number of spectra specified, specify value between 1 and 100")

EXCEPTION_MAP[DevBAD_NUM_SPECTRA.status] = DevBAD_NUM_SPECTRA
EXCEPTION_PREFIX_MAP[DevBAD_NUM_SPECTRA.prefix] = DevBAD_NUM_SPECTRA

class DevBAD_GRATING(DevException):
    status = 662474690
    prefix = "%DEV-E-BAD_GRATING"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_GRATING, Bad grating type specified, specify value between 1 and 5")

EXCEPTION_MAP[DevBAD_GRATING.status] = DevBAD_GRATING
EXCEPTION_PREFIX_MAP[DevBAD_GRATING.prefix] = DevBAD_GRATING

class DevBAD_EXPOSURE(DevException):
    status = 662474698
    prefix = "%DEV-E-BAD_EXPOSURE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_EXPOSURE, Bad exposure time specified, specify value between 30 and 3000")

EXCEPTION_MAP[DevBAD_EXPOSURE.status] = DevBAD_EXPOSURE
EXCEPTION_PREFIX_MAP[DevBAD_EXPOSURE.prefix] = DevBAD_EXPOSURE

class DevBAD_FILTER(DevException):
    status = 662474706
    prefix = "%DEV-E-BAD_FILTER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FILTER, Bad neutral density filter specified, specify value between 0 and 5")

EXCEPTION_MAP[DevBAD_FILTER.status] = DevBAD_FILTER
EXCEPTION_PREFIX_MAP[DevBAD_FILTER.prefix] = DevBAD_FILTER

class DevGO_FILE_ERROR(DevException):
    status = 662474714
    prefix = "%DEV-E-GO_FILE_ERROR"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-GO_FILE_ERROR, Error creating new go file")

EXCEPTION_MAP[DevGO_FILE_ERROR.status] = DevGO_FILE_ERROR
EXCEPTION_PREFIX_MAP[DevGO_FILE_ERROR.prefix] = DevGO_FILE_ERROR

class DevDATA_FILE_ERROR(DevException):
    status = 662474722
    prefix = "%DEV-E-DATA_FILE_ERROR"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-DATA_FILE_ERROR, Error opening datafile")

EXCEPTION_MAP[DevDATA_FILE_ERROR.status] = DevDATA_FILE_ERROR
EXCEPTION_PREFIX_MAP[DevDATA_FILE_ERROR.prefix] = DevDATA_FILE_ERROR

class DevNORMAL(DevException):
    status = 662475065
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevERROR(DevException):
    status = 662475074
    prefix = "%DEV-E-ERROR"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-ERROR, IDL returned a non zero error code")

EXCEPTION_MAP[DevERROR.status] = DevERROR
EXCEPTION_PREFIX_MAP[DevERROR.prefix] = DevERROR

class DevBAD_CHAN(DevException):
    status = 662475466
    prefix = "%DEV-E-BAD_CHAN"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CHAN, Error evaluating data for channel !SL")

EXCEPTION_MAP[DevBAD_CHAN.status] = DevBAD_CHAN
EXCEPTION_PREFIX_MAP[DevBAD_CHAN.prefix] = DevBAD_CHAN

class DevBAD_CLOCK(DevException):
    status = 662475474
    prefix = "%DEV-E-BAD_CLOCK"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLOCK, Invalid internal clock range specified")

EXCEPTION_MAP[DevBAD_CLOCK.status] = DevBAD_CLOCK
EXCEPTION_PREFIX_MAP[DevBAD_CLOCK.prefix] = DevBAD_CLOCK

class DevBAD_ITERATIONS(DevException):
    status = 662475482
    prefix = "%DEV-E-BAD_ITERATIONS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ITERATIONS, Invalid number of iterations specified")

EXCEPTION_MAP[DevBAD_ITERATIONS.status] = DevBAD_ITERATIONS
EXCEPTION_PREFIX_MAP[DevBAD_ITERATIONS.prefix] = DevBAD_ITERATIONS

class DevBAD_NOC(DevException):
    status = 662475490
    prefix = "%DEV-E-BAD_NOC"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_NOC, Invalid number of active channels specified")

EXCEPTION_MAP[DevBAD_NOC.status] = DevBAD_NOC
EXCEPTION_PREFIX_MAP[DevBAD_NOC.prefix] = DevBAD_NOC

class DevBAD_SAMPS(DevException):
    status = 662475498
    prefix = "%DEV-E-BAD_SAMPS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_SAMPS, Number of samples specificed invalid")

EXCEPTION_MAP[DevBAD_SAMPS.status] = DevBAD_SAMPS
EXCEPTION_PREFIX_MAP[DevBAD_SAMPS.prefix] = DevBAD_SAMPS

class DevNOT_SORTED(DevException):
    status = 662475866
    prefix = "%DEV-E-NOT_SORTED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NOT_SORTED, Times specified for J412 module were not sorted")

EXCEPTION_MAP[DevNOT_SORTED.status] = DevNOT_SORTED
EXCEPTION_PREFIX_MAP[DevNOT_SORTED.prefix] = DevNOT_SORTED

class DevNO_DATA(DevException):
    status = 662475874
    prefix = "%DEV-E-NO_DATA"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NO_DATA, There were no times specifed for J412 module")

EXCEPTION_MAP[DevNO_DATA.status] = DevNO_DATA
EXCEPTION_PREFIX_MAP[DevNO_DATA.prefix] = DevNO_DATA

class DevBADCYCLES(DevException):
    status = 662475882
    prefix = "%DEV-E-BADCYCLES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BADCYCLES, The number of cycles must be 1 .. 255")

EXCEPTION_MAP[DevBADCYCLES.status] = DevBADCYCLES
EXCEPTION_PREFIX_MAP[DevBADCYCLES.prefix] = DevBADCYCLES

class DevNORMAL(DevException):
    status = 662476265
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevBAD_MEMSIZE(DevException):
    status = 662476274
    prefix = "%DEV-E-BAD_MEMSIZE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MEMSIZE, Memory size must be in 128K, 256K, 512k, 1024K")

EXCEPTION_MAP[DevBAD_MEMSIZE.status] = DevBAD_MEMSIZE
EXCEPTION_PREFIX_MAP[DevBAD_MEMSIZE.prefix] = DevBAD_MEMSIZE

class DevBAD_ACTIVEMEM(DevException):
    status = 662476282
    prefix = "%DEV-E-BAD_ACTIVEMEM"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVEMEM, Active Mem must be power of 2 8K to 1024K")

EXCEPTION_MAP[DevBAD_ACTIVEMEM.status] = DevBAD_ACTIVEMEM
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVEMEM.prefix] = DevBAD_ACTIVEMEM

class DevBAD_ACTIVECHAN(DevException):
    status = 662476290
    prefix = "%DEV-E-BAD_ACTIVECHAN"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVECHAN, Active channels must be in 1,2,4,8,16")

EXCEPTION_MAP[DevBAD_ACTIVECHAN.status] = DevBAD_ACTIVECHAN
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVECHAN.prefix] = DevBAD_ACTIVECHAN

class DevBAD_PTS(DevException):
    status = 662476298
    prefix = "%DEV-E-BAD_PTS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PTS, PTS must be power of 2 32 to 1024K")

EXCEPTION_MAP[DevBAD_PTS.status] = DevBAD_PTS
EXCEPTION_PREFIX_MAP[DevBAD_PTS.prefix] = DevBAD_PTS

class DevBAD_FREQUENCY(DevException):
    status = 662476306
    prefix = "%DEV-E-BAD_FREQUENCY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FREQUENCY, Invalid clock frequency")

EXCEPTION_MAP[DevBAD_FREQUENCY.status] = DevBAD_FREQUENCY
EXCEPTION_PREFIX_MAP[DevBAD_FREQUENCY.prefix] = DevBAD_FREQUENCY

class DevBAD_MASTER(DevException):
    status = 662476314
    prefix = "%DEV-E-BAD_MASTER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MASTER, Master must be 0 or 1")

EXCEPTION_MAP[DevBAD_MASTER.status] = DevBAD_MASTER
EXCEPTION_PREFIX_MAP[DevBAD_MASTER.prefix] = DevBAD_MASTER

class DevBAD_GAIN(DevException):
    status = 662476322
    prefix = "%DEV-E-BAD_GAIN"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_GAIN, Gain must be 1, 2, 4, or 8")

EXCEPTION_MAP[DevBAD_GAIN.status] = DevBAD_GAIN
EXCEPTION_PREFIX_MAP[DevBAD_GAIN.prefix] = DevBAD_GAIN

class DevNORMAL(DevException):
    status = 662476665
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevBAD_CLK_DIVIDE(DevException):
    status = 662476674
    prefix = "%DEV-E-BAD_CLK_DIVIDE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLK_DIVIDE, Clock divide must be one of 1,2,4,10,20,40, or 100")

EXCEPTION_MAP[DevBAD_CLK_DIVIDE.status] = DevBAD_CLK_DIVIDE
EXCEPTION_PREFIX_MAP[DevBAD_CLK_DIVIDE.prefix] = DevBAD_CLK_DIVIDE

class DevBAD_MODE(DevException):
    status = 662476682
    prefix = "%DEV-E-BAD_MODE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MODE, Mode must be in the range of 0 to 4")

EXCEPTION_MAP[DevBAD_MODE.status] = DevBAD_MODE
EXCEPTION_PREFIX_MAP[DevBAD_MODE.prefix] = DevBAD_MODE

class DevBAD_CLK_POLARITY(DevException):
    status = 662476690
    prefix = "%DEV-E-BAD_CLK_POLARITY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLK_POLARITY, Clock polarity must be either 0 (rising) or 1 (falling)")

EXCEPTION_MAP[DevBAD_CLK_POLARITY.status] = DevBAD_CLK_POLARITY
EXCEPTION_PREFIX_MAP[DevBAD_CLK_POLARITY.prefix] = DevBAD_CLK_POLARITY

class DevBAD_STR_POLARITY(DevException):
    status = 662476698
    prefix = "%DEV-E-BAD_STR_POLARITY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_STR_POLARITY, Start polarity must be either 0 (rising) or 1 (falling)")

EXCEPTION_MAP[DevBAD_STR_POLARITY.status] = DevBAD_STR_POLARITY
EXCEPTION_PREFIX_MAP[DevBAD_STR_POLARITY.prefix] = DevBAD_STR_POLARITY

class DevBAD_STP_POLARITY(DevException):
    status = 662476706
    prefix = "%DEV-E-BAD_STP_POLARITY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_STP_POLARITY, Stop polarity must be either 0 (rising) or 1 (falling)")

EXCEPTION_MAP[DevBAD_STP_POLARITY.status] = DevBAD_STP_POLARITY
EXCEPTION_PREFIX_MAP[DevBAD_STP_POLARITY.prefix] = DevBAD_STP_POLARITY

class DevBAD_GATED(DevException):
    status = 662476714
    prefix = "%DEV-E-BAD_GATED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_GATED, Gated clock must be either 0 (not gated) or 1 (gated)")

EXCEPTION_MAP[DevBAD_GATED.status] = DevBAD_GATED
EXCEPTION_PREFIX_MAP[DevBAD_GATED.prefix] = DevBAD_GATED

class DevNORMAL(DevException):
    status = 662477065
    prefix = "%DEV-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%DEV-S-NORMAL, Successful completion")

EXCEPTION_MAP[DevNORMAL.status] = DevNORMAL
EXCEPTION_PREFIX_MAP[DevNORMAL.prefix] = DevNORMAL

class DevBAD_ACTIVECHAN(DevException):
    status = 662477074
    prefix = "%DEV-E-BAD_ACTIVECHAN"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVECHAN, Active chans must be 1, 2, or 4")

EXCEPTION_MAP[DevBAD_ACTIVECHAN.status] = DevBAD_ACTIVECHAN
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVECHAN.prefix] = DevBAD_ACTIVECHAN

class DevBAD_ACTIVEMEM(DevException):
    status = 662477082
    prefix = "%DEV-E-BAD_ACTIVEMEM"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVEMEM, Active memory must be power of 2 LE 8192")

EXCEPTION_MAP[DevBAD_ACTIVEMEM.status] = DevBAD_ACTIVEMEM
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVEMEM.prefix] = DevBAD_ACTIVEMEM

class DevBAD_FREQUENCY(DevException):
    status = 662477090
    prefix = "%DEV-E-BAD_FREQUENCY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FREQUENCY, Frequency must be in [0, .02, .05, .1, .2, .5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]")

EXCEPTION_MAP[DevBAD_FREQUENCY.status] = DevBAD_FREQUENCY
EXCEPTION_PREFIX_MAP[DevBAD_FREQUENCY.prefix] = DevBAD_FREQUENCY

class DevBAD_FULL_SCALE(DevException):
    status = 662477098
    prefix = "%DEV-E-BAD_FULL_SCALE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FULL_SCALE, Full Scale must be in [.4096, 1.024, 2.048, 4.096, 10.24, 25.6, 51.2, 102.4]")

EXCEPTION_MAP[DevBAD_FULL_SCALE.status] = DevBAD_FULL_SCALE
EXCEPTION_PREFIX_MAP[DevBAD_FULL_SCALE.prefix] = DevBAD_FULL_SCALE

class DevBAD_MEMORIES(DevException):
    status = 662477106
    prefix = "%DEV-E-BAD_MEMORIES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MEMORIES, Memories must 1 .. 16")

EXCEPTION_MAP[DevBAD_MEMORIES.status] = DevBAD_MEMORIES
EXCEPTION_PREFIX_MAP[DevBAD_MEMORIES.prefix] = DevBAD_MEMORIES

class DevBAD_COUPLING(DevException):
    status = 662477114
    prefix = "%DEV-E-BAD_COUPLING"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_COUPLING, Channel source / coupling must be one of 0 .. 7")

EXCEPTION_MAP[DevBAD_COUPLING.status] = DevBAD_COUPLING
EXCEPTION_PREFIX_MAP[DevBAD_COUPLING.prefix] = DevBAD_COUPLING

class DevBAD_OFFSET(DevException):
    status = 662477122
    prefix = "%DEV-E-BAD_OFFSET"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_OFFSET, Offset must be between 0 and 255")

EXCEPTION_MAP[DevBAD_OFFSET.status] = DevBAD_OFFSET
EXCEPTION_PREFIX_MAP[DevBAD_OFFSET.prefix] = DevBAD_OFFSET

class DevBAD_SEGMENTS(DevException):
    status = 662477130
    prefix = "%DEV-E-BAD_SEGMENTS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_SEGMENTS, Number of segments must be 1 .. 1024")

EXCEPTION_MAP[DevBAD_SEGMENTS.status] = DevBAD_SEGMENTS
EXCEPTION_PREFIX_MAP[DevBAD_SEGMENTS.prefix] = DevBAD_SEGMENTS

class DevBAD_TRIG_DELAY(DevException):
    status = 662477138
    prefix = "%DEV-E-BAD_TRIG_DELAY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_TRIG_DELAY, Trigger delay must be between -8 and 247 in units of 8ths of segment size")

EXCEPTION_MAP[DevBAD_TRIG_DELAY.status] = DevBAD_TRIG_DELAY
EXCEPTION_PREFIX_MAP[DevBAD_TRIG_DELAY.prefix] = DevBAD_TRIG_DELAY

class DevOUTRNG(DevException):
    status = 662477466
    prefix = "%DEV-E-OUTRNG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-OUTRNG, Joerger DAC Channels out of range. Bad chans code !XW")

EXCEPTION_MAP[DevOUTRNG.status] = DevOUTRNG
EXCEPTION_PREFIX_MAP[DevOUTRNG.prefix] = DevOUTRNG

class DevBAD_ACTIVE_CHANS(DevException):
    status = 662477866
    prefix = "%DEV-E-BAD_ACTIVE_CHANS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVE_CHANS, Bad active channels selection")

EXCEPTION_MAP[DevBAD_ACTIVE_CHANS.status] = DevBAD_ACTIVE_CHANS
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVE_CHANS.prefix] = DevBAD_ACTIVE_CHANS

class DevBAD_MASTER(DevException):
    status = 662477874
    prefix = "%DEV-E-BAD_MASTER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MASTER, Bad master selection, must be 0 or 1")

EXCEPTION_MAP[DevBAD_MASTER.status] = DevBAD_MASTER
EXCEPTION_PREFIX_MAP[DevBAD_MASTER.prefix] = DevBAD_MASTER

class DevBAD_EXT_1MHZ(DevException):
    status = 662477882
    prefix = "%DEV-E-BAD_EXT_1MHZ"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_EXT_1MHZ, Bad ext 1mhz selection, must be 0 or 1")

EXCEPTION_MAP[DevBAD_EXT_1MHZ.status] = DevBAD_EXT_1MHZ
EXCEPTION_PREFIX_MAP[DevBAD_EXT_1MHZ.prefix] = DevBAD_EXT_1MHZ

class DevBAD_PTSC(DevException):
    status = 662477890
    prefix = "%DEV-E-BAD_PTSC"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PTSC, Bad PTSC setting")

EXCEPTION_MAP[DevBAD_PTSC.status] = DevBAD_PTSC
EXCEPTION_PREFIX_MAP[DevBAD_PTSC.prefix] = DevBAD_PTSC

class DevBAD_HEADER(DevException):
    status = 662478266
    prefix = "%DEV-E-BAD_HEADER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_HEADER, Invalid header jumper information (e.g. 49414944432)")

EXCEPTION_MAP[DevBAD_HEADER.status] = DevBAD_HEADER
EXCEPTION_PREFIX_MAP[DevBAD_HEADER.prefix] = DevBAD_HEADER

class DevBAD_MEMORIES(DevException):
    status = 662478274
    prefix = "%DEV-E-BAD_MEMORIES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MEMORIES, Invalid number of memories, must be 1 .. 16")

EXCEPTION_MAP[DevBAD_MEMORIES.status] = DevBAD_MEMORIES
EXCEPTION_PREFIX_MAP[DevBAD_MEMORIES.prefix] = DevBAD_MEMORIES

class DevBAD_NOC(DevException):
    status = 662478282
    prefix = "%DEV-E-BAD_NOC"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_NOC, Invalid number of active channels")

EXCEPTION_MAP[DevBAD_NOC.status] = DevBAD_NOC
EXCEPTION_PREFIX_MAP[DevBAD_NOC.prefix] = DevBAD_NOC

class DevBAD_OFFSET(DevException):
    status = 662478290
    prefix = "%DEV-E-BAD_OFFSET"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_OFFSET, Invalid offset must be one of (0, -2048, -4096)")

EXCEPTION_MAP[DevBAD_OFFSET.status] = DevBAD_OFFSET
EXCEPTION_PREFIX_MAP[DevBAD_OFFSET.prefix] = DevBAD_OFFSET

class DevBAD_PTS(DevException):
    status = 662478298
    prefix = "%DEV-E-BAD_PTS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PTS, Invalid pts code, must be 0 .. 7")

EXCEPTION_MAP[DevBAD_PTS.status] = DevBAD_PTS
EXCEPTION_PREFIX_MAP[DevBAD_PTS.prefix] = DevBAD_PTS

class DevFREQ_TOO_HIGH(DevException):
    status = 662478306
    prefix = "%DEV-E-FREQ_TOO_HIGH"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-FREQ_TOO_HIGH, Frequency to high for selected number of channels")

EXCEPTION_MAP[DevFREQ_TOO_HIGH.status] = DevFREQ_TOO_HIGH
EXCEPTION_PREFIX_MAP[DevFREQ_TOO_HIGH.prefix] = DevFREQ_TOO_HIGH

class DevINVALID_NOC(DevException):
    status = 662478314
    prefix = "%DEV-E-INVALID_NOC"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-INVALID_NOC, Invalid number of active channels")

EXCEPTION_MAP[DevINVALID_NOC.status] = DevINVALID_NOC
EXCEPTION_PREFIX_MAP[DevINVALID_NOC.prefix] = DevINVALID_NOC

class DevBADTIME(DevException):
    status = 662478666
    prefix = "%DEV-E-BADTIME"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BADTIME, Could not read time")

EXCEPTION_MAP[DevBADTIME.status] = DevBADTIME
EXCEPTION_PREFIX_MAP[DevBADTIME.prefix] = DevBADTIME

class DevBADFREQ(DevException):
    status = 662478674
    prefix = "%DEV-E-BADFREQ"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BADFREQ, Could not read frequency")

EXCEPTION_MAP[DevBADFREQ.status] = DevBADFREQ
EXCEPTION_PREFIX_MAP[DevBADFREQ.prefix] = DevBADFREQ

class DevBAD_OFFSET(DevException):
    status = 662479066
    prefix = "%DEV-E-BAD_OFFSET"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_OFFSET, Offset for L8828 must be between 0 and 255")

EXCEPTION_MAP[DevBAD_OFFSET.status] = DevBAD_OFFSET
EXCEPTION_PREFIX_MAP[DevBAD_OFFSET.prefix] = DevBAD_OFFSET

class DevBAD_PRETRIG(DevException):
    status = 662479074
    prefix = "%DEV-E-BAD_PRETRIG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PRETRIG, Pre trigger samples for L8828 must be betwwen 0 and 7 eighths")

EXCEPTION_MAP[DevBAD_PRETRIG.status] = DevBAD_PRETRIG
EXCEPTION_PREFIX_MAP[DevBAD_PRETRIG.prefix] = DevBAD_PRETRIG

class DevBAD_ACTIVEMEM(DevException):
    status = 662479082
    prefix = "%DEV-E-BAD_ACTIVEMEM"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVEMEM, ACTIVEMEM must be beteen 16K and 2M")

EXCEPTION_MAP[DevBAD_ACTIVEMEM.status] = DevBAD_ACTIVEMEM
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVEMEM.prefix] = DevBAD_ACTIVEMEM

class DevBAD_CLOCK(DevException):
    status = 662479090
    prefix = "%DEV-E-BAD_CLOCK"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLOCK, Invalid clock frequency specified")

EXCEPTION_MAP[DevBAD_CLOCK.status] = DevBAD_CLOCK
EXCEPTION_PREFIX_MAP[DevBAD_CLOCK.prefix] = DevBAD_CLOCK

class DevBAD_OFFSET(DevException):
    status = 662479466
    prefix = "%DEV-E-BAD_OFFSET"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_OFFSET, Offset for L8828 must be between 0 and 255")

EXCEPTION_MAP[DevBAD_OFFSET.status] = DevBAD_OFFSET
EXCEPTION_PREFIX_MAP[DevBAD_OFFSET.prefix] = DevBAD_OFFSET

class DevBAD_PRETRIG(DevException):
    status = 662479474
    prefix = "%DEV-E-BAD_PRETRIG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PRETRIG, Pre trigger samples for L8828 must be betwwen 0 and 7 eighths")

EXCEPTION_MAP[DevBAD_PRETRIG.status] = DevBAD_PRETRIG
EXCEPTION_PREFIX_MAP[DevBAD_PRETRIG.prefix] = DevBAD_PRETRIG

class DevBAD_ACTIVEMEM(DevException):
    status = 662479482
    prefix = "%DEV-E-BAD_ACTIVEMEM"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVEMEM, ACTIVEMEM must be beteen 16K and 2M")

EXCEPTION_MAP[DevBAD_ACTIVEMEM.status] = DevBAD_ACTIVEMEM
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVEMEM.prefix] = DevBAD_ACTIVEMEM

class DevBAD_CLOCK(DevException):
    status = 662479490
    prefix = "%DEV-E-BAD_CLOCK"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLOCK, Invalid clock frequency specified")

EXCEPTION_MAP[DevBAD_CLOCK.status] = DevBAD_CLOCK
EXCEPTION_PREFIX_MAP[DevBAD_CLOCK.prefix] = DevBAD_CLOCK

class DevBAD_ACTMEM(DevException):
    status = 662479546
    prefix = "%DEV-E-BAD_ACTMEM"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTMEM, ACTMEM value out of range, must be 0-7 where 0=1/8th and 7 = all")

EXCEPTION_MAP[DevBAD_ACTMEM.status] = DevBAD_ACTMEM
EXCEPTION_PREFIX_MAP[DevBAD_ACTMEM.prefix] = DevBAD_ACTMEM

class DevBAD_PRETRIG(DevException):
    status = 662479554
    prefix = "%DEV-E-BAD_PRETRIG"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PRETRIG, PRETRIG value out of range, must be 0-7 where 0 = none and 7 = 7/8 pretrigger samples")

EXCEPTION_MAP[DevBAD_PRETRIG.status] = DevBAD_PRETRIG
EXCEPTION_PREFIX_MAP[DevBAD_PRETRIG.prefix] = DevBAD_PRETRIG

class DevBAD_MODE(DevException):
    status = 662479562
    prefix = "%DEV-E-BAD_MODE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_MODE, MODE value out of range, must be 0 (for normal) or 1 (for burst mode)")

EXCEPTION_MAP[DevBAD_MODE.status] = DevBAD_MODE
EXCEPTION_PREFIX_MAP[DevBAD_MODE.prefix] = DevBAD_MODE

class DevBAD_FREQUENCY(DevException):
    status = 662479570
    prefix = "%DEV-E-BAD_FREQUENCY"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_FREQUENCY, FREQUENCY value out of range, must be 0-4 where 0=3MHz,1=2MHz,2=1MHz,3=100KHz,4=external")

EXCEPTION_MAP[DevBAD_FREQUENCY.status] = DevBAD_FREQUENCY
EXCEPTION_PREFIX_MAP[DevBAD_FREQUENCY.prefix] = DevBAD_FREQUENCY

class DevNODATA(DevException):
    status = 662479868
    prefix = "%DEV-F-NODATA"
    def __init__(self):
        Exception.__init__(self, "%DEV-F-NODATA, No data has been written to memory")

EXCEPTION_MAP[DevNODATA.status] = DevNODATA
EXCEPTION_PREFIX_MAP[DevNODATA.prefix] = DevNODATA

class DevBAD_CLOCK(DevException):
    status = 662479946
    prefix = "%DEV-E-BAD_CLOCK"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLOCK, Bad value specified in INT_CLOCK node, use Setup device to correct")

EXCEPTION_MAP[DevBAD_CLOCK.status] = DevBAD_CLOCK
EXCEPTION_PREFIX_MAP[DevBAD_CLOCK.prefix] = DevBAD_CLOCK

class DevBAD_BLOCKS(DevException):
    status = 662479954
    prefix = "%DEV-E-BAD_BLOCKS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_BLOCKS, Bad value specified in BLOCKS node, use Setup device to correct")

EXCEPTION_MAP[DevBAD_BLOCKS.status] = DevBAD_BLOCKS
EXCEPTION_PREFIX_MAP[DevBAD_BLOCKS.prefix] = DevBAD_BLOCKS

class DevBAD_PTS(DevException):
    status = 662479962
    prefix = "%DEV-E-BAD_PTS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PTS, Bad value specfiied in PTS node, must be an integer value between 1 and 131071")

EXCEPTION_MAP[DevBAD_PTS.status] = DevBAD_PTS
EXCEPTION_PREFIX_MAP[DevBAD_PTS.prefix] = DevBAD_PTS

class DevBAD_CLOCK(DevException):
    status = 662480026
    prefix = "%DEV-E-BAD_CLOCK"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_CLOCK, Bad value specified in INT_CLOCK node, use Setup device to correct")

EXCEPTION_MAP[DevBAD_CLOCK.status] = DevBAD_CLOCK
EXCEPTION_PREFIX_MAP[DevBAD_CLOCK.prefix] = DevBAD_CLOCK

class DevBAD_ACTIVE_CHANS(DevException):
    status = 662480034
    prefix = "%DEV-E-BAD_ACTIVE_CHANS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_ACTIVE_CHANS, Bad value specified in ACTIVE_CHANS node, use Setup device to correct")

EXCEPTION_MAP[DevBAD_ACTIVE_CHANS.status] = DevBAD_ACTIVE_CHANS
EXCEPTION_PREFIX_MAP[DevBAD_ACTIVE_CHANS.prefix] = DevBAD_ACTIVE_CHANS

class DevBAD_PTS(DevException):
    status = 662480042
    prefix = "%DEV-E-BAD_PTS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PTS, Bad value specfiied in PTS node, must be an integer value between 1 and 131071")

EXCEPTION_MAP[DevBAD_PTS.status] = DevBAD_PTS
EXCEPTION_PREFIX_MAP[DevBAD_PTS.prefix] = DevBAD_PTS

class DevCHANNEL_READ_ERROR(DevException):
    status = 662480106
    prefix = "%DEV-E-CHANNEL_READ_ERROR"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-CHANNEL_READ_ERROR, Error reading channel")

EXCEPTION_MAP[DevCHANNEL_READ_ERROR.status] = DevCHANNEL_READ_ERROR
EXCEPTION_PREFIX_MAP[DevCHANNEL_READ_ERROR.prefix] = DevCHANNEL_READ_ERROR

class DevUNHANDLED_EXCEPTION(DevException):
    status = 662480186
    prefix = "%DEV-E-UNHANDLED_EXCEPTION"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-UNHANDLED_EXCEPTION, Python device raised an exception, see log files for more details")

EXCEPTION_MAP[DevUNHANDLED_EXCEPTION.status] = DevUNHANDLED_EXCEPTION
EXCEPTION_PREFIX_MAP[DevUNHANDLED_EXCEPTION.prefix] = DevUNHANDLED_EXCEPTION

class DevNO_SAMPLES(DevException):
    status = 662480266
    prefix = "%DEV-E-NO_SAMPLES"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NO_SAMPLES, Module did not acquire any samples")

EXCEPTION_MAP[DevNO_SAMPLES.status] = DevNO_SAMPLES
EXCEPTION_PREFIX_MAP[DevNO_SAMPLES.prefix] = DevNO_SAMPLES

class DevCANNOT_LOAD_SETTINGS(DevException):
    status = 662480290
    prefix = "%DEV-E-CANNOT_LOAD_SETTINGS"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-CANNOT_LOAD_SETTINGS, Error loading settings from XML or JSON")

EXCEPTION_MAP[DevCANNOT_LOAD_SETTINGS.status] = DevCANNOT_LOAD_SETTINGS
EXCEPTION_PREFIX_MAP[DevCANNOT_LOAD_SETTINGS.prefix] = DevCANNOT_LOAD_SETTINGS

class DevCANNOT_GET_BOARD_STATE(DevException):
    status = 662480298
    prefix = "%DEV-E-CANNOT_GET_BOARD_STATE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-CANNOT_GET_BOARD_STATE, Cannot retrieve state of daq board")

EXCEPTION_MAP[DevCANNOT_GET_BOARD_STATE.status] = DevCANNOT_GET_BOARD_STATE
EXCEPTION_PREFIX_MAP[DevCANNOT_GET_BOARD_STATE.prefix] = DevCANNOT_GET_BOARD_STATE

class DevACQCMD_FAILED(DevException):
    status = 662480306
    prefix = "%DEV-E-ACQCMD_FAILED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-ACQCMD_FAILED, Error executing acqcmd on daq board")

EXCEPTION_MAP[DevACQCMD_FAILED.status] = DevACQCMD_FAILED
EXCEPTION_PREFIX_MAP[DevACQCMD_FAILED.prefix] = DevACQCMD_FAILED

class DevACQ2SH_FAILED(DevException):
    status = 662480314
    prefix = "%DEV-E-ACQ2SH_FAILED"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-ACQ2SH_FAILED, Error executing acq2sh command on daq board")

EXCEPTION_MAP[DevACQ2SH_FAILED.status] = DevACQ2SH_FAILED
EXCEPTION_PREFIX_MAP[DevACQ2SH_FAILED.prefix] = DevACQ2SH_FAILED

class DevBAD_PARAMETER(DevException):
    status = 662480322
    prefix = "%DEV-E-BAD_PARAMETER"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-BAD_PARAMETER, Invalid parameter specified for device")

EXCEPTION_MAP[DevBAD_PARAMETER.status] = DevBAD_PARAMETER
EXCEPTION_PREFIX_MAP[DevBAD_PARAMETER.prefix] = DevBAD_PARAMETER

class DevCOMM_ERROR(DevException):
    status = 662480330
    prefix = "%DEV-E-COMM_ERROR"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-COMM_ERROR, Error communicating with device")

EXCEPTION_MAP[DevCOMM_ERROR.status] = DevCOMM_ERROR
EXCEPTION_PREFIX_MAP[DevCOMM_ERROR.prefix] = DevCOMM_ERROR

class DevCAMERA_NOT_FOUND(DevException):
    status = 662480338
    prefix = "%DEV-E-CAMERA_NOT_FOUND"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-CAMERA_NOT_FOUND, Could not find specified camera on the network")

EXCEPTION_MAP[DevCAMERA_NOT_FOUND.status] = DevCAMERA_NOT_FOUND
EXCEPTION_PREFIX_MAP[DevCAMERA_NOT_FOUND.prefix] = DevCAMERA_NOT_FOUND

class DevNOT_A_PYDEVICE(DevException):
    status = 662480346
    prefix = "%DEV-E-NOT_A_PYDEVICE"
    def __init__(self):
        Exception.__init__(self, "%DEV-E-NOT_A_PYDEVICE, Device is not a python device")

EXCEPTION_MAP[DevNOT_A_PYDEVICE.status] = DevNOT_A_PYDEVICE
EXCEPTION_PREFIX_MAP[DevNOT_A_PYDEVICE.prefix] = DevNOT_A_PYDEVICE

class TreeException(MdsException):
    pass

class TreeALREADY_OFF(TreeException):
    status = 265388075
    prefix = "%TREE-I-ALREADY_OFF"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-ALREADY_OFF, Node is already OFF")

EXCEPTION_MAP[TreeALREADY_OFF.status] = TreeALREADY_OFF
EXCEPTION_PREFIX_MAP[TreeALREADY_OFF.prefix] = TreeALREADY_OFF

class TreeALREADY_ON(TreeException):
    status = 265388083
    prefix = "%TREE-I-ALREADY_ON"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-ALREADY_ON, Node is already ON")

EXCEPTION_MAP[TreeALREADY_ON.status] = TreeALREADY_ON
EXCEPTION_PREFIX_MAP[TreeALREADY_ON.prefix] = TreeALREADY_ON

class TreeALREADY_OPEN(TreeException):
    status = 265388091
    prefix = "%TREE-I-ALREADY_OPEN"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-ALREADY_OPEN, Tree is already OPEN")

EXCEPTION_MAP[TreeALREADY_OPEN.status] = TreeALREADY_OPEN
EXCEPTION_PREFIX_MAP[TreeALREADY_OPEN.prefix] = TreeALREADY_OPEN

class TreeALREADY_THERE(TreeException):
    status = 265388168
    prefix = "%TREE-W-ALREADY_THERE"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-ALREADY_THERE, Node is already in the tree")

EXCEPTION_MAP[TreeALREADY_THERE.status] = TreeALREADY_THERE
EXCEPTION_PREFIX_MAP[TreeALREADY_THERE.prefix] = TreeALREADY_THERE

class TreeBADRECORD(TreeException):
    status = 265388218
    prefix = "%TREE-E-BADRECORD"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-BADRECORD, Data corrupted: cannot read record")

EXCEPTION_MAP[TreeBADRECORD.status] = TreeBADRECORD
EXCEPTION_PREFIX_MAP[TreeBADRECORD.prefix] = TreeBADRECORD

class TreeBOTH_OFF(TreeException):
    status = 265388184
    prefix = "%TREE-W-BOTH_OFF"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-BOTH_OFF, Both this node and its parent are off")

EXCEPTION_MAP[TreeBOTH_OFF.status] = TreeBOTH_OFF
EXCEPTION_PREFIX_MAP[TreeBOTH_OFF.prefix] = TreeBOTH_OFF

class TreeBUFFEROVF(TreeException):
    status = 265388306
    prefix = "%TREE-E-BUFFEROVF"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-BUFFEROVF, Output buffer overflow")

EXCEPTION_MAP[TreeBUFFEROVF.status] = TreeBUFFEROVF
EXCEPTION_PREFIX_MAP[TreeBUFFEROVF.prefix] = TreeBUFFEROVF

class TreeCONGLOMFULL(TreeException):
    status = 265388322
    prefix = "%TREE-E-CONGLOMFULL"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-CONGLOMFULL, Current conglomerate is full")

EXCEPTION_MAP[TreeCONGLOMFULL.status] = TreeCONGLOMFULL
EXCEPTION_PREFIX_MAP[TreeCONGLOMFULL.prefix] = TreeCONGLOMFULL

class TreeCONGLOM_NOT_FULL(TreeException):
    status = 265388330
    prefix = "%TREE-E-CONGLOM_NOT_FULL"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-CONGLOM_NOT_FULL, Current conglomerate is not yet full")

EXCEPTION_MAP[TreeCONGLOM_NOT_FULL.status] = TreeCONGLOM_NOT_FULL
EXCEPTION_PREFIX_MAP[TreeCONGLOM_NOT_FULL.prefix] = TreeCONGLOM_NOT_FULL

class TreeCONTINUING(TreeException):
    status = 265390435
    prefix = "%TREE-I-CONTINUING"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-CONTINUING, Operation continuing: note following error")

EXCEPTION_MAP[TreeCONTINUING.status] = TreeCONTINUING
EXCEPTION_PREFIX_MAP[TreeCONTINUING.prefix] = TreeCONTINUING

class TreeDUPTAG(TreeException):
    status = 265388234
    prefix = "%TREE-E-DUPTAG"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-DUPTAG, Tag name already in use")

EXCEPTION_MAP[TreeDUPTAG.status] = TreeDUPTAG
EXCEPTION_PREFIX_MAP[TreeDUPTAG.prefix] = TreeDUPTAG

class TreeEDITING(TreeException):
    status = 265388434
    prefix = "%TREE-E-EDITING"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-EDITING, Tree file open for edit: operation not permitted")

EXCEPTION_MAP[TreeEDITING.status] = TreeEDITING
EXCEPTION_PREFIX_MAP[TreeEDITING.prefix] = TreeEDITING

class TreeILLEGAL_ITEM(TreeException):
    status = 265388298
    prefix = "%TREE-E-ILLEGAL_ITEM"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-ILLEGAL_ITEM, Invalid item code or part number specified")

EXCEPTION_MAP[TreeILLEGAL_ITEM.status] = TreeILLEGAL_ITEM
EXCEPTION_PREFIX_MAP[TreeILLEGAL_ITEM.prefix] = TreeILLEGAL_ITEM

class TreeILLPAGCNT(TreeException):
    status = 265388242
    prefix = "%TREE-E-ILLPAGCNT"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-ILLPAGCNT, Illegal page count, error mapping tree file")

EXCEPTION_MAP[TreeILLPAGCNT.status] = TreeILLPAGCNT
EXCEPTION_PREFIX_MAP[TreeILLPAGCNT.prefix] = TreeILLPAGCNT

class TreeINVDFFCLASS(TreeException):
    status = 265388346
    prefix = "%TREE-E-INVDFFCLASS"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVDFFCLASS, Invalid data fmt: only CLASS_S can have data in NCI")

EXCEPTION_MAP[TreeINVDFFCLASS.status] = TreeINVDFFCLASS
EXCEPTION_PREFIX_MAP[TreeINVDFFCLASS.prefix] = TreeINVDFFCLASS

class TreeINVDTPUSG(TreeException):
    status = 265388426
    prefix = "%TREE-E-INVDTPUSG"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVDTPUSG, Attempt to store datatype which conflicts with the designated usage of this node")

EXCEPTION_MAP[TreeINVDTPUSG.status] = TreeINVDTPUSG
EXCEPTION_PREFIX_MAP[TreeINVDTPUSG.prefix] = TreeINVDTPUSG

class TreeINVPATH(TreeException):
    status = 265388290
    prefix = "%TREE-E-INVPATH"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVPATH, Invalid tree pathname specified")

EXCEPTION_MAP[TreeINVPATH.status] = TreeINVPATH
EXCEPTION_PREFIX_MAP[TreeINVPATH.prefix] = TreeINVPATH

class TreeINVRECTYP(TreeException):
    status = 265388354
    prefix = "%TREE-E-INVRECTYP"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVRECTYP, Record type invalid for requested operation")

EXCEPTION_MAP[TreeINVRECTYP.status] = TreeINVRECTYP
EXCEPTION_PREFIX_MAP[TreeINVRECTYP.prefix] = TreeINVRECTYP

class TreeINVTREE(TreeException):
    status = 265388226
    prefix = "%TREE-E-INVTREE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVTREE, Invalid tree identification structure")

EXCEPTION_MAP[TreeINVTREE.status] = TreeINVTREE
EXCEPTION_PREFIX_MAP[TreeINVTREE.prefix] = TreeINVTREE

class TreeMAXOPENEDIT(TreeException):
    status = 265388250
    prefix = "%TREE-E-MAXOPENEDIT"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-MAXOPENEDIT, Too many files open for edit")

EXCEPTION_MAP[TreeMAXOPENEDIT.status] = TreeMAXOPENEDIT
EXCEPTION_PREFIX_MAP[TreeMAXOPENEDIT.prefix] = TreeMAXOPENEDIT

class TreeNEW(TreeException):
    status = 265388059
    prefix = "%TREE-I-NEW"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-NEW, New tree created")

EXCEPTION_MAP[TreeNEW.status] = TreeNEW
EXCEPTION_PREFIX_MAP[TreeNEW.prefix] = TreeNEW

class TreeNMN(TreeException):
    status = 265388128
    prefix = "%TREE-W-NMN"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-NMN, No More Nodes")

EXCEPTION_MAP[TreeNMN.status] = TreeNMN
EXCEPTION_PREFIX_MAP[TreeNMN.prefix] = TreeNMN

class TreeNMT(TreeException):
    status = 265388136
    prefix = "%TREE-W-NMT"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-NMT, No More Tags")

EXCEPTION_MAP[TreeNMT.status] = TreeNMT
EXCEPTION_PREFIX_MAP[TreeNMT.prefix] = TreeNMT

class TreeNNF(TreeException):
    status = 265388144
    prefix = "%TREE-W-NNF"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-NNF, Node Not Found")

EXCEPTION_MAP[TreeNNF.status] = TreeNNF
EXCEPTION_PREFIX_MAP[TreeNNF.prefix] = TreeNNF

class TreeNODATA(TreeException):
    status = 265388258
    prefix = "%TREE-E-NODATA"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NODATA, No data available for this node")

EXCEPTION_MAP[TreeNODATA.status] = TreeNODATA
EXCEPTION_PREFIX_MAP[TreeNODATA.prefix] = TreeNODATA

class TreeNODNAMLEN(TreeException):
    status = 265388362
    prefix = "%TREE-E-NODNAMLEN"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NODNAMLEN, Node name too long (12 chars max)")

EXCEPTION_MAP[TreeNODNAMLEN.status] = TreeNODNAMLEN
EXCEPTION_PREFIX_MAP[TreeNODNAMLEN.prefix] = TreeNODNAMLEN

class TreeNOEDIT(TreeException):
    status = 265388274
    prefix = "%TREE-E-NOEDIT"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOEDIT, Tree file is not open for edit")

EXCEPTION_MAP[TreeNOEDIT.status] = TreeNOEDIT
EXCEPTION_PREFIX_MAP[TreeNOEDIT.prefix] = TreeNOEDIT

class TreeNOLOG(TreeException):
    status = 265388458
    prefix = "%TREE-E-NOLOG"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOLOG, Experiment pathname (xxx_path) not defined")

EXCEPTION_MAP[TreeNOLOG.status] = TreeNOLOG
EXCEPTION_PREFIX_MAP[TreeNOLOG.prefix] = TreeNOLOG

class TreeNOMETHOD(TreeException):
    status = 265388208
    prefix = "%TREE-W-NOMETHOD"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-NOMETHOD, Method not available for this object")

EXCEPTION_MAP[TreeNOMETHOD.status] = TreeNOMETHOD
EXCEPTION_PREFIX_MAP[TreeNOMETHOD.prefix] = TreeNOMETHOD

class TreeNOOVERWRITE(TreeException):
    status = 265388418
    prefix = "%TREE-E-NOOVERWRITE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOOVERWRITE, Write-once node: overwrite not permitted")

EXCEPTION_MAP[TreeNOOVERWRITE.status] = TreeNOOVERWRITE
EXCEPTION_PREFIX_MAP[TreeNOOVERWRITE.prefix] = TreeNOOVERWRITE

class TreeNORMAL(TreeException):
    status = 265388041
    prefix = "%TREE-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%TREE-S-NORMAL, Normal successful completion")

EXCEPTION_MAP[TreeNORMAL.status] = TreeNORMAL
EXCEPTION_PREFIX_MAP[TreeNORMAL.prefix] = TreeNORMAL

class TreeNOTALLSUBS(TreeException):
    status = 265388067
    prefix = "%TREE-I-NOTALLSUBS"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-NOTALLSUBS, Main tree opened but not all subtrees found/or connected")

EXCEPTION_MAP[TreeNOTALLSUBS.status] = TreeNOTALLSUBS
EXCEPTION_PREFIX_MAP[TreeNOTALLSUBS.prefix] = TreeNOTALLSUBS

class TreeNOTCHILDLESS(TreeException):
    status = 265388282
    prefix = "%TREE-E-NOTCHILDLESS"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOTCHILDLESS, Node must be childless to become subtree reference")

EXCEPTION_MAP[TreeNOTCHILDLESS.status] = TreeNOTCHILDLESS
EXCEPTION_PREFIX_MAP[TreeNOTCHILDLESS.prefix] = TreeNOTCHILDLESS

class TreeNOT_IN_LIST(TreeException):
    status = 265388482
    prefix = "%TREE-E-NOT_IN_LIST"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOT_IN_LIST, Tree being opened was not in the list")

EXCEPTION_MAP[TreeNOT_IN_LIST.status] = TreeNOT_IN_LIST
EXCEPTION_PREFIX_MAP[TreeNOT_IN_LIST.prefix] = TreeNOT_IN_LIST

class TreeNOTMEMBERLESS(TreeException):
    status = 265388402
    prefix = "%TREE-E-NOTMEMBERLESS"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOTMEMBERLESS, Subtree reference can not have members")

EXCEPTION_MAP[TreeNOTMEMBERLESS.status] = TreeNOTMEMBERLESS
EXCEPTION_PREFIX_MAP[TreeNOTMEMBERLESS.prefix] = TreeNOTMEMBERLESS

class TreeNOTOPEN(TreeException):
    status = 265388266
    prefix = "%TREE-E-NOTOPEN"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOTOPEN, No tree file currently open")

EXCEPTION_MAP[TreeNOTOPEN.status] = TreeNOTOPEN
EXCEPTION_PREFIX_MAP[TreeNOTOPEN.prefix] = TreeNOTOPEN

class TreeNOTSON(TreeException):
    status = 265388410
    prefix = "%TREE-E-NOTSON"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOTSON, Subtree reference cannot be a member")

EXCEPTION_MAP[TreeNOTSON.status] = TreeNOTSON
EXCEPTION_PREFIX_MAP[TreeNOTSON.prefix] = TreeNOTSON

class TreeNOT_CONGLOM(TreeException):
    status = 265388386
    prefix = "%TREE-E-NOT_CONGLOM"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOT_CONGLOM, Head node of conglomerate does not contain a DTYPE_CONGLOM record")

EXCEPTION_MAP[TreeNOT_CONGLOM.status] = TreeNOT_CONGLOM
EXCEPTION_PREFIX_MAP[TreeNOT_CONGLOM.prefix] = TreeNOT_CONGLOM

class TreeNOT_OPEN(TreeException):
    status = 265388200
    prefix = "%TREE-W-NOT_OPEN"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-NOT_OPEN, Tree not currently open")

EXCEPTION_MAP[TreeNOT_OPEN.status] = TreeNOT_OPEN
EXCEPTION_PREFIX_MAP[TreeNOT_OPEN.prefix] = TreeNOT_OPEN

class TreeNOWRITEMODEL(TreeException):
    status = 265388442
    prefix = "%TREE-E-NOWRITEMODEL"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOWRITEMODEL, Data for this node can not be written into the MODEL file")

EXCEPTION_MAP[TreeNOWRITEMODEL.status] = TreeNOWRITEMODEL
EXCEPTION_PREFIX_MAP[TreeNOWRITEMODEL.prefix] = TreeNOWRITEMODEL

class TreeNOWRITESHOT(TreeException):
    status = 265388450
    prefix = "%TREE-E-NOWRITESHOT"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOWRITESHOT, Data for this node can not be written into the SHOT file")

EXCEPTION_MAP[TreeNOWRITESHOT.status] = TreeNOWRITESHOT
EXCEPTION_PREFIX_MAP[TreeNOWRITESHOT.prefix] = TreeNOWRITESHOT

class TreeNO_CONTEXT(TreeException):
    status = 265388099
    prefix = "%TREE-I-NO_CONTEXT"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-NO_CONTEXT, There is no active search to end")

EXCEPTION_MAP[TreeNO_CONTEXT.status] = TreeNO_CONTEXT
EXCEPTION_PREFIX_MAP[TreeNO_CONTEXT.prefix] = TreeNO_CONTEXT

class TreeOFF(TreeException):
    status = 265388192
    prefix = "%TREE-W-OFF"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-OFF, Node is OFF")

EXCEPTION_MAP[TreeOFF.status] = TreeOFF
EXCEPTION_PREFIX_MAP[TreeOFF.prefix] = TreeOFF

class TreeON(TreeException):
    status = 265388107
    prefix = "%TREE-I-ON"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-ON, Node is ON")

EXCEPTION_MAP[TreeON.status] = TreeON
EXCEPTION_PREFIX_MAP[TreeON.prefix] = TreeON

class TreeOPEN(TreeException):
    status = 265388115
    prefix = "%TREE-I-OPEN"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-OPEN, Tree is OPEN (no edit)")

EXCEPTION_MAP[TreeOPEN.status] = TreeOPEN
EXCEPTION_PREFIX_MAP[TreeOPEN.prefix] = TreeOPEN

class TreeOPEN_EDIT(TreeException):
    status = 265388123
    prefix = "%TREE-I-OPEN_EDIT"
    def __init__(self):
        Exception.__init__(self, "%TREE-I-OPEN_EDIT, Tree is OPEN for edit")

EXCEPTION_MAP[TreeOPEN_EDIT.status] = TreeOPEN_EDIT
EXCEPTION_PREFIX_MAP[TreeOPEN_EDIT.prefix] = TreeOPEN_EDIT

class TreePARENT_OFF(TreeException):
    status = 265388176
    prefix = "%TREE-W-PARENT_OFF"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-PARENT_OFF, Parent of this node is OFF")

EXCEPTION_MAP[TreePARENT_OFF.status] = TreePARENT_OFF
EXCEPTION_PREFIX_MAP[TreePARENT_OFF.prefix] = TreePARENT_OFF

class TreeREADERR(TreeException):
    status = 265388474
    prefix = "%TREE-E-READERR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-READERR, Error reading record for node")

EXCEPTION_MAP[TreeREADERR.status] = TreeREADERR
EXCEPTION_PREFIX_MAP[TreeREADERR.prefix] = TreeREADERR

class TreeREADONLY(TreeException):
    status = 265388466
    prefix = "%TREE-E-READONLY"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-READONLY, Tree was opened with readonly access")

EXCEPTION_MAP[TreeREADONLY.status] = TreeREADONLY
EXCEPTION_PREFIX_MAP[TreeREADONLY.prefix] = TreeREADONLY

class TreeRESOLVED(TreeException):
    status = 265388049
    prefix = "%TREE-S-RESOLVED"
    def __init__(self):
        Exception.__init__(self, "%TREE-S-RESOLVED, Indirect reference successfully resolved")

EXCEPTION_MAP[TreeRESOLVED.status] = TreeRESOLVED
EXCEPTION_PREFIX_MAP[TreeRESOLVED.prefix] = TreeRESOLVED

class TreeSUCCESS(TreeException):
    status = 265389633
    prefix = "%TREE-S-SUCCESS"
    def __init__(self):
        Exception.__init__(self, "%TREE-S-SUCCESS, Operation successful")

EXCEPTION_MAP[TreeSUCCESS.status] = TreeSUCCESS
EXCEPTION_PREFIX_MAP[TreeSUCCESS.prefix] = TreeSUCCESS

class TreeTAGNAMLEN(TreeException):
    status = 265388370
    prefix = "%TREE-E-TAGNAMLEN"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-TAGNAMLEN, Tagname too long (max 24 chars)")

EXCEPTION_MAP[TreeTAGNAMLEN.status] = TreeTAGNAMLEN
EXCEPTION_PREFIX_MAP[TreeTAGNAMLEN.prefix] = TreeTAGNAMLEN

class TreeTNF(TreeException):
    status = 265388152
    prefix = "%TREE-W-TNF"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-TNF, Tag Not Found")

EXCEPTION_MAP[TreeTNF.status] = TreeTNF
EXCEPTION_PREFIX_MAP[TreeTNF.prefix] = TreeTNF

class TreeTREENF(TreeException):
    status = 265388160
    prefix = "%TREE-W-TREENF"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-TREENF, Tree Not Found")

EXCEPTION_MAP[TreeTREENF.status] = TreeTREENF
EXCEPTION_PREFIX_MAP[TreeTREENF.prefix] = TreeTREENF

class TreeUNRESOLVED(TreeException):
    status = 265388338
    prefix = "%TREE-E-UNRESOLVED"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-UNRESOLVED, Not an indirect node reference: No action taken")

EXCEPTION_MAP[TreeUNRESOLVED.status] = TreeUNRESOLVED
EXCEPTION_PREFIX_MAP[TreeUNRESOLVED.prefix] = TreeUNRESOLVED

class TreeUNSPRTCLASS(TreeException):
    status = 265388314
    prefix = "%TREE-E-UNSPRTCLASS"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-UNSPRTCLASS, Unsupported descriptor class")

EXCEPTION_MAP[TreeUNSPRTCLASS.status] = TreeUNSPRTCLASS
EXCEPTION_PREFIX_MAP[TreeUNSPRTCLASS.prefix] = TreeUNSPRTCLASS

class TreeUNSUPARRDTYPE(TreeException):
    status = 265388394
    prefix = "%TREE-E-UNSUPARRDTYPE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-UNSUPARRDTYPE, Complex data types not supported as members of arrays")

EXCEPTION_MAP[TreeUNSUPARRDTYPE.status] = TreeUNSUPARRDTYPE
EXCEPTION_PREFIX_MAP[TreeUNSUPARRDTYPE.prefix] = TreeUNSUPARRDTYPE

class TreeWRITEFIRST(TreeException):
    status = 265388378
    prefix = "%TREE-E-WRITEFIRST"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-WRITEFIRST, Tree has been modified: write or quit first")

EXCEPTION_MAP[TreeWRITEFIRST.status] = TreeWRITEFIRST
EXCEPTION_PREFIX_MAP[TreeWRITEFIRST.prefix] = TreeWRITEFIRST

class TreeFAILURE(TreeException):
    status = 265392034
    prefix = "%TREE-E-FAILURE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-FAILURE, Operation NOT successful")

EXCEPTION_MAP[TreeFAILURE.status] = TreeFAILURE
EXCEPTION_PREFIX_MAP[TreeFAILURE.prefix] = TreeFAILURE

class TreeLOCK_FAILURE(TreeException):
    status = 265392048
    prefix = "%TREE-W-LOCK_FAILURE"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-LOCK_FAILURE, Error locking file, perhaps NFSLOCKING not enabled on this system")

EXCEPTION_MAP[TreeLOCK_FAILURE.status] = TreeLOCK_FAILURE
EXCEPTION_PREFIX_MAP[TreeLOCK_FAILURE.prefix] = TreeLOCK_FAILURE

class TreeFILE_NOT_FOUND(TreeException):
    status = 265392042
    prefix = "%TREE-E-FILE_NOT_FOUND"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-FILE_NOT_FOUND, File or Directory Not Found")

EXCEPTION_MAP[TreeFILE_NOT_FOUND.status] = TreeFILE_NOT_FOUND
EXCEPTION_PREFIX_MAP[TreeFILE_NOT_FOUND.prefix] = TreeFILE_NOT_FOUND

class TreeCANCEL(TreeException):
    status = 265391232
    prefix = "%TREE-W-CANCEL"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-CANCEL, User canceled operation")

EXCEPTION_MAP[TreeCANCEL.status] = TreeCANCEL
EXCEPTION_PREFIX_MAP[TreeCANCEL.prefix] = TreeCANCEL

class TreeUNSUPTHICKOP(TreeException):
    status = 265391240
    prefix = "%TREE-W-UNSUPTHICKOP"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-UNSUPTHICKOP, Unsupported thick client operation")

EXCEPTION_MAP[TreeUNSUPTHICKOP.status] = TreeUNSUPTHICKOP
EXCEPTION_PREFIX_MAP[TreeUNSUPTHICKOP.prefix] = TreeUNSUPTHICKOP

class TreeNOSEGMENTS(TreeException):
    status = 265392058
    prefix = "%TREE-E-NOSEGMENTS"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOSEGMENTS, No segments exist in this node")

EXCEPTION_MAP[TreeNOSEGMENTS.status] = TreeNOSEGMENTS
EXCEPTION_PREFIX_MAP[TreeNOSEGMENTS.prefix] = TreeNOSEGMENTS

class TreeINVDTYPE(TreeException):
    status = 265392066
    prefix = "%TREE-E-INVDTYPE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVDTYPE, Invalid datatype for data segment")

EXCEPTION_MAP[TreeINVDTYPE.status] = TreeINVDTYPE
EXCEPTION_PREFIX_MAP[TreeINVDTYPE.prefix] = TreeINVDTYPE

class TreeINVSHAPE(TreeException):
    status = 265392074
    prefix = "%TREE-E-INVSHAPE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVSHAPE, Invalid shape for this data segment")

EXCEPTION_MAP[TreeINVSHAPE.status] = TreeINVSHAPE
EXCEPTION_PREFIX_MAP[TreeINVSHAPE.prefix] = TreeINVSHAPE

class TreeINVSHOT(TreeException):
    status = 265392090
    prefix = "%TREE-E-INVSHOT"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVSHOT, Invalid shot number - must be -1 (model), 0 (current), or Positive")

EXCEPTION_MAP[TreeINVSHOT.status] = TreeINVSHOT
EXCEPTION_PREFIX_MAP[TreeINVSHOT.prefix] = TreeINVSHOT

class TreeINVTAG(TreeException):
    status = 265392106
    prefix = "%TREE-E-INVTAG"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-INVTAG, Invalid tagname - must begin with alpha followed by 0-22 alphanumeric or underscores")

EXCEPTION_MAP[TreeINVTAG.status] = TreeINVTAG
EXCEPTION_PREFIX_MAP[TreeINVTAG.prefix] = TreeINVTAG

class TreeNOPATH(TreeException):
    status = 265392114
    prefix = "%TREE-E-NOPATH"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOPATH, No 'treename'_path or default_tree_path environment variables defined. Cannot locate tree files")

EXCEPTION_MAP[TreeNOPATH.status] = TreeNOPATH
EXCEPTION_PREFIX_MAP[TreeNOPATH.prefix] = TreeNOPATH

class TreeTREEFILEREADERR(TreeException):
    status = 265392122
    prefix = "%TREE-E-TREEFILEREADERR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-TREEFILEREADERR, Error reading in tree file contents")

EXCEPTION_MAP[TreeTREEFILEREADERR.status] = TreeTREEFILEREADERR
EXCEPTION_PREFIX_MAP[TreeTREEFILEREADERR.prefix] = TreeTREEFILEREADERR

class TreeMEMERR(TreeException):
    status = 265392130
    prefix = "%TREE-E-MEMERR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-MEMERR, Memory allocation error")

EXCEPTION_MAP[TreeMEMERR.status] = TreeMEMERR
EXCEPTION_PREFIX_MAP[TreeMEMERR.prefix] = TreeMEMERR

class TreeNOCURRENT(TreeException):
    status = 265392138
    prefix = "%TREE-E-NOCURRENT"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOCURRENT, No current shot number set for this tree")

EXCEPTION_MAP[TreeNOCURRENT.status] = TreeNOCURRENT
EXCEPTION_PREFIX_MAP[TreeNOCURRENT.prefix] = TreeNOCURRENT

class TreeFOPENW(TreeException):
    status = 265392146
    prefix = "%TREE-E-FOPENW"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-FOPENW, Error opening file for read-write")

EXCEPTION_MAP[TreeFOPENW.status] = TreeFOPENW
EXCEPTION_PREFIX_MAP[TreeFOPENW.prefix] = TreeFOPENW

class TreeFOPENR(TreeException):
    status = 265392154
    prefix = "%TREE-E-FOPENR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-FOPENR, Error opening file read-only")

EXCEPTION_MAP[TreeFOPENR.status] = TreeFOPENR
EXCEPTION_PREFIX_MAP[TreeFOPENR.prefix] = TreeFOPENR

class TreeFCREATE(TreeException):
    status = 265392162
    prefix = "%TREE-E-FCREATE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-FCREATE, Error creating new file")

EXCEPTION_MAP[TreeFCREATE.status] = TreeFCREATE
EXCEPTION_PREFIX_MAP[TreeFCREATE.prefix] = TreeFCREATE

class TreeCONNECTFAIL(TreeException):
    status = 265392170
    prefix = "%TREE-E-CONNECTFAIL"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-CONNECTFAIL, Error connecting to remote server")

EXCEPTION_MAP[TreeCONNECTFAIL.status] = TreeCONNECTFAIL
EXCEPTION_PREFIX_MAP[TreeCONNECTFAIL.prefix] = TreeCONNECTFAIL

class TreeNCIWRITE(TreeException):
    status = 265392178
    prefix = "%TREE-E-NCIWRITE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NCIWRITE, Error writing node characterisitics to file")

EXCEPTION_MAP[TreeNCIWRITE.status] = TreeNCIWRITE
EXCEPTION_PREFIX_MAP[TreeNCIWRITE.prefix] = TreeNCIWRITE

class TreeDELFAIL(TreeException):
    status = 265392186
    prefix = "%TREE-E-DELFAIL"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-DELFAIL, Error deleting file")

EXCEPTION_MAP[TreeDELFAIL.status] = TreeDELFAIL
EXCEPTION_PREFIX_MAP[TreeDELFAIL.prefix] = TreeDELFAIL

class TreeRENFAIL(TreeException):
    status = 265392194
    prefix = "%TREE-E-RENFAIL"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-RENFAIL, Error renaming file")

EXCEPTION_MAP[TreeRENFAIL.status] = TreeRENFAIL
EXCEPTION_PREFIX_MAP[TreeRENFAIL.prefix] = TreeRENFAIL

class TreeEMPTY(TreeException):
    status = 265392200
    prefix = "%TREE-W-EMPTY"
    def __init__(self):
        Exception.__init__(self, "%TREE-W-EMPTY, Empty string provided")

EXCEPTION_MAP[TreeEMPTY.status] = TreeEMPTY
EXCEPTION_PREFIX_MAP[TreeEMPTY.prefix] = TreeEMPTY

class TreePARSEERR(TreeException):
    status = 265392210
    prefix = "%TREE-E-PARSEERR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-PARSEERR, Invalid node search string")

EXCEPTION_MAP[TreePARSEERR.status] = TreePARSEERR
EXCEPTION_PREFIX_MAP[TreePARSEERR.prefix] = TreePARSEERR

class TreeNCIREAD(TreeException):
    status = 265392218
    prefix = "%TREE-E-NCIREAD"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NCIREAD, Error reading node characteristics from file")

EXCEPTION_MAP[TreeNCIREAD.status] = TreeNCIREAD
EXCEPTION_PREFIX_MAP[TreeNCIREAD.prefix] = TreeNCIREAD

class TreeNOVERSION(TreeException):
    status = 265392226
    prefix = "%TREE-E-NOVERSION"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOVERSION, No version available")

EXCEPTION_MAP[TreeNOVERSION.status] = TreeNOVERSION
EXCEPTION_PREFIX_MAP[TreeNOVERSION.prefix] = TreeNOVERSION

class TreeDFREAD(TreeException):
    status = 265392234
    prefix = "%TREE-E-DFREAD"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-DFREAD, Error reading from datafile")

EXCEPTION_MAP[TreeDFREAD.status] = TreeDFREAD
EXCEPTION_PREFIX_MAP[TreeDFREAD.prefix] = TreeDFREAD

class TreeCLOSEERR(TreeException):
    status = 265392242
    prefix = "%TREE-E-CLOSEERR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-CLOSEERR, Error closing temporary tree file")

EXCEPTION_MAP[TreeCLOSEERR.status] = TreeCLOSEERR
EXCEPTION_PREFIX_MAP[TreeCLOSEERR.prefix] = TreeCLOSEERR

class TreeMOVEERROR(TreeException):
    status = 265392250
    prefix = "%TREE-E-MOVEERROR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-MOVEERROR, Error replacing original treefile with new one")

EXCEPTION_MAP[TreeMOVEERROR.status] = TreeMOVEERROR
EXCEPTION_PREFIX_MAP[TreeMOVEERROR.prefix] = TreeMOVEERROR

class TreeOPENEDITERR(TreeException):
    status = 265392258
    prefix = "%TREE-E-OPENEDITERR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-OPENEDITERR, Error reopening new treefile for write access")

EXCEPTION_MAP[TreeOPENEDITERR.status] = TreeOPENEDITERR
EXCEPTION_PREFIX_MAP[TreeOPENEDITERR.prefix] = TreeOPENEDITERR

class TreeREADONLY_TREE(TreeException):
    status = 265392266
    prefix = "%TREE-E-READONLY_TREE"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-READONLY_TREE, Tree is marked as readonly. No write operations permitted")

EXCEPTION_MAP[TreeREADONLY_TREE.status] = TreeREADONLY_TREE
EXCEPTION_PREFIX_MAP[TreeREADONLY_TREE.prefix] = TreeREADONLY_TREE

class TreeWRITETREEERR(TreeException):
    status = 265392274
    prefix = "%TREE-E-WRITETREEERR"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-WRITETREEERR, Error writing .tree file")

EXCEPTION_MAP[TreeWRITETREEERR.status] = TreeWRITETREEERR
EXCEPTION_PREFIX_MAP[TreeWRITETREEERR.prefix] = TreeWRITETREEERR

class TreeNOWILD(TreeException):
    status = 265392282
    prefix = "%TREE-E-NOWILD"
    def __init__(self):
        Exception.__init__(self, "%TREE-E-NOWILD, No wildcard characters permitted in node specifier")

EXCEPTION_MAP[TreeNOWILD.status] = TreeNOWILD
EXCEPTION_PREFIX_MAP[TreeNOWILD.prefix] = TreeNOWILD

class LibException(MdsException):
    pass

class LibINSVIRMEM(LibException):
    status = 1409556
    prefix = "%LIB-F-INSVIRMEM"
    def __init__(self):
        Exception.__init__(self, "%LIB-F-INSVIRMEM, Insufficient virtual memory")

EXCEPTION_MAP[LibINSVIRMEM.status] = LibINSVIRMEM
EXCEPTION_PREFIX_MAP[LibINSVIRMEM.prefix] = LibINSVIRMEM

class LibINVARG(LibException):
    status = 1409588
    prefix = "%LIB-F-INVARG"
    def __init__(self):
        Exception.__init__(self, "%LIB-F-INVARG, Invalid argument")

EXCEPTION_MAP[LibINVARG.status] = LibINVARG
EXCEPTION_PREFIX_MAP[LibINVARG.prefix] = LibINVARG

class LibINVSTRDES(LibException):
    status = 1409572
    prefix = "%LIB-F-INVSTRDES"
    def __init__(self):
        Exception.__init__(self, "%LIB-F-INVSTRDES, Invalid string descriptor")

EXCEPTION_MAP[LibINVSTRDES.status] = LibINVSTRDES
EXCEPTION_PREFIX_MAP[LibINVSTRDES.prefix] = LibINVSTRDES

class LibKEYNOTFOU(LibException):
    status = 1409788
    prefix = "%LIB-F-KEYNOTFOU"
    def __init__(self):
        Exception.__init__(self, "%LIB-F-KEYNOTFOU, Key not found")

EXCEPTION_MAP[LibKEYNOTFOU.status] = LibKEYNOTFOU
EXCEPTION_PREFIX_MAP[LibKEYNOTFOU.prefix] = LibKEYNOTFOU

class LibNOTFOU(LibException):
    status = 1409652
    prefix = "%LIB-F-NOTFOU"
    def __init__(self):
        Exception.__init__(self, "%LIB-F-NOTFOU, Entity not found")

EXCEPTION_MAP[LibNOTFOU.status] = LibNOTFOU
EXCEPTION_PREFIX_MAP[LibNOTFOU.prefix] = LibNOTFOU

class LibQUEWASEMP(LibException):
    status = 1409772
    prefix = "%LIB-F-QUEWASEMP"
    def __init__(self):
        Exception.__init__(self, "%LIB-F-QUEWASEMP, Queue was empty")

EXCEPTION_MAP[LibQUEWASEMP.status] = LibQUEWASEMP
EXCEPTION_PREFIX_MAP[LibQUEWASEMP.prefix] = LibQUEWASEMP

class LibSTRTRU(LibException):
    status = 1409041
    prefix = "%LIB-S-STRTRU"
    def __init__(self):
        Exception.__init__(self, "%LIB-S-STRTRU, String truncated")

EXCEPTION_MAP[LibSTRTRU.status] = LibSTRTRU
EXCEPTION_PREFIX_MAP[LibSTRTRU.prefix] = LibSTRTRU

class StrException(MdsException):
    pass

class StrMATCH(StrException):
    status = 2393113
    prefix = "%STR-S-MATCH"
    def __init__(self):
        Exception.__init__(self, "%STR-S-MATCH, Strings match")

EXCEPTION_MAP[StrMATCH.status] = StrMATCH
EXCEPTION_PREFIX_MAP[StrMATCH.prefix] = StrMATCH

class StrNOMATCH(StrException):
    status = 2392584
    prefix = "%STR-W-NOMATCH"
    def __init__(self):
        Exception.__init__(self, "%STR-W-NOMATCH, Strings do not match")

EXCEPTION_MAP[StrNOMATCH.status] = StrNOMATCH
EXCEPTION_PREFIX_MAP[StrNOMATCH.prefix] = StrNOMATCH

class StrNOELEM(StrException):
    status = 2392600
    prefix = "%STR-W-NOELEM"
    def __init__(self):
        Exception.__init__(self, "%STR-W-NOELEM, Not enough delimited characters")

EXCEPTION_MAP[StrNOELEM.status] = StrNOELEM
EXCEPTION_PREFIX_MAP[StrNOELEM.prefix] = StrNOELEM

class StrINVDELIM(StrException):
    status = 2392592
    prefix = "%STR-W-INVDELIM"
    def __init__(self):
        Exception.__init__(self, "%STR-W-INVDELIM, Not enough delimited characters")

EXCEPTION_MAP[StrINVDELIM.status] = StrINVDELIM
EXCEPTION_PREFIX_MAP[StrINVDELIM.prefix] = StrINVDELIM

class StrSTRTOOLON(StrException):
    status = 2392180
    prefix = "%STR-F-STRTOOLON"
    def __init__(self):
        Exception.__init__(self, "%STR-F-STRTOOLON, String too long")

EXCEPTION_MAP[StrSTRTOOLON.status] = StrSTRTOOLON
EXCEPTION_PREFIX_MAP[StrSTRTOOLON.prefix] = StrSTRTOOLON

class MDSplusException(MdsException):
    pass

class MDSplusWARNING(MDSplusException):
    status = 65536
    prefix = "%MDSPLUS-W-WARNING"
    def __init__(self):
        Exception.__init__(self, "%MDSPLUS-W-WARNING, Warning")

EXCEPTION_MAP[MDSplusWARNING.status] = MDSplusWARNING
EXCEPTION_PREFIX_MAP[MDSplusWARNING.prefix] = MDSplusWARNING

class MDSplusSUCCESS(MDSplusException):
    status = 65545
    prefix = "%MDSPLUS-S-SUCCESS"
    def __init__(self):
        Exception.__init__(self, "%MDSPLUS-S-SUCCESS, Success")

EXCEPTION_MAP[MDSplusSUCCESS.status] = MDSplusSUCCESS
EXCEPTION_PREFIX_MAP[MDSplusSUCCESS.prefix] = MDSplusSUCCESS

class MDSplusERROR(MDSplusException):
    status = 65554
    prefix = "%MDSPLUS-E-ERROR"
    def __init__(self):
        Exception.__init__(self, "%MDSPLUS-E-ERROR, Error")

EXCEPTION_MAP[MDSplusERROR.status] = MDSplusERROR
EXCEPTION_PREFIX_MAP[MDSplusERROR.prefix] = MDSplusERROR

class MDSplusFATAL(MDSplusException):
    status = 65572
    prefix = "%MDSPLUS-F-FATAL"
    def __init__(self):
        Exception.__init__(self, "%MDSPLUS-F-FATAL, Fatal")

EXCEPTION_MAP[MDSplusFATAL.status] = MDSplusFATAL
EXCEPTION_PREFIX_MAP[MDSplusFATAL.prefix] = MDSplusFATAL

class MDSplusSANDBOX(MDSplusException):
    status = 65578
    prefix = "%MDSPLUS-E-SANDBOX"
    def __init__(self):
        Exception.__init__(self, "%MDSPLUS-E-SANDBOX, Function disabled for security reasons")

EXCEPTION_MAP[MDSplusSANDBOX.status] = MDSplusSANDBOX
EXCEPTION_PREFIX_MAP[MDSplusSANDBOX.prefix] = MDSplusSANDBOX

class TdiException(MdsException):
    pass

class TdiBREAK(TdiException):
    status = 265519112
    prefix = "%TDI-W-BREAK"
    def __init__(self):
        Exception.__init__(self, "%TDI-W-BREAK, BREAK was not in DO FOR SWITCH or WHILE")

EXCEPTION_MAP[TdiBREAK.status] = TdiBREAK
EXCEPTION_PREFIX_MAP[TdiBREAK.prefix] = TdiBREAK

class TdiCASE(TdiException):
    status = 265519120
    prefix = "%TDI-W-CASE"
    def __init__(self):
        Exception.__init__(self, "%TDI-W-CASE, CASE was not in SWITCH statement")

EXCEPTION_MAP[TdiCASE.status] = TdiCASE
EXCEPTION_PREFIX_MAP[TdiCASE.prefix] = TdiCASE

class TdiCONTINUE(TdiException):
    status = 265519128
    prefix = "%TDI-W-CONTINUE"
    def __init__(self):
        Exception.__init__(self, "%TDI-W-CONTINUE, CONTINUE was not in DO FOR or WHILE")

EXCEPTION_MAP[TdiCONTINUE.status] = TdiCONTINUE
EXCEPTION_PREFIX_MAP[TdiCONTINUE.prefix] = TdiCONTINUE

class TdiEXTRANEOUS(TdiException):
    status = 265519136
    prefix = "%TDI-W-EXTRANEOUS"
    def __init__(self):
        Exception.__init__(self, "%TDI-W-EXTRANEOUS, Some characters were unused, bad number maybe")

EXCEPTION_MAP[TdiEXTRANEOUS.status] = TdiEXTRANEOUS
EXCEPTION_PREFIX_MAP[TdiEXTRANEOUS.prefix] = TdiEXTRANEOUS

class TdiRETURN(TdiException):
    status = 265519144
    prefix = "%TDI-W-RETURN"
    def __init__(self):
        Exception.__init__(self, "%TDI-W-RETURN, Extraneous RETURN statement, not from a FUN")

EXCEPTION_MAP[TdiRETURN.status] = TdiRETURN
EXCEPTION_PREFIX_MAP[TdiRETURN.prefix] = TdiRETURN

class TdiABORT(TdiException):
    status = 265519154
    prefix = "%TDI-E-ABORT"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-ABORT, Program requested abort")

EXCEPTION_MAP[TdiABORT.status] = TdiABORT
EXCEPTION_PREFIX_MAP[TdiABORT.prefix] = TdiABORT

class TdiBAD_INDEX(TdiException):
    status = 265519162
    prefix = "%TDI-E-BAD_INDEX"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-BAD_INDEX, Index or subscript is too small or too big")

EXCEPTION_MAP[TdiBAD_INDEX.status] = TdiBAD_INDEX
EXCEPTION_PREFIX_MAP[TdiBAD_INDEX.prefix] = TdiBAD_INDEX

class TdiBOMB(TdiException):
    status = 265519170
    prefix = "%TDI-E-BOMB"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-BOMB, Bad punctuation, could not compile the text")

EXCEPTION_MAP[TdiBOMB.status] = TdiBOMB
EXCEPTION_PREFIX_MAP[TdiBOMB.prefix] = TdiBOMB

class TdiEXTRA_ARG(TdiException):
    status = 265519178
    prefix = "%TDI-E-EXTRA_ARG"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-EXTRA_ARG, Too many arguments for function, watch commas")

EXCEPTION_MAP[TdiEXTRA_ARG.status] = TdiEXTRA_ARG
EXCEPTION_PREFIX_MAP[TdiEXTRA_ARG.prefix] = TdiEXTRA_ARG

class TdiGOTO(TdiException):
    status = 265519186
    prefix = "%TDI-E-GOTO"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-GOTO, GOTO target label not found")

EXCEPTION_MAP[TdiGOTO.status] = TdiGOTO
EXCEPTION_PREFIX_MAP[TdiGOTO.prefix] = TdiGOTO

class TdiINVCLADSC(TdiException):
    status = 265519194
    prefix = "%TDI-E-INVCLADSC"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-INVCLADSC, Storage class not valid, must be scalar or array")

EXCEPTION_MAP[TdiINVCLADSC.status] = TdiINVCLADSC
EXCEPTION_PREFIX_MAP[TdiINVCLADSC.prefix] = TdiINVCLADSC

class TdiINVCLADTY(TdiException):
    status = 265519202
    prefix = "%TDI-E-INVCLADTY"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-INVCLADTY, Invalid mixture of storage class and data type")

EXCEPTION_MAP[TdiINVCLADTY.status] = TdiINVCLADTY
EXCEPTION_PREFIX_MAP[TdiINVCLADTY.prefix] = TdiINVCLADTY

class TdiINVDTYDSC(TdiException):
    status = 265519210
    prefix = "%TDI-E-INVDTYDSC"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-INVDTYDSC, Storage data type is not valid")

EXCEPTION_MAP[TdiINVDTYDSC.status] = TdiINVDTYDSC
EXCEPTION_PREFIX_MAP[TdiINVDTYDSC.prefix] = TdiINVDTYDSC

class TdiINV_OPC(TdiException):
    status = 265519218
    prefix = "%TDI-E-INV_OPC"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-INV_OPC, Invalid operator code in a function")

EXCEPTION_MAP[TdiINV_OPC.status] = TdiINV_OPC
EXCEPTION_PREFIX_MAP[TdiINV_OPC.prefix] = TdiINV_OPC

class TdiINV_SIZE(TdiException):
    status = 265519226
    prefix = "%TDI-E-INV_SIZE"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-INV_SIZE, Number of elements does not match declaration")

EXCEPTION_MAP[TdiINV_SIZE.status] = TdiINV_SIZE
EXCEPTION_PREFIX_MAP[TdiINV_SIZE.prefix] = TdiINV_SIZE

class TdiMISMATCH(TdiException):
    status = 265519234
    prefix = "%TDI-E-MISMATCH"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-MISMATCH, Shape of arguments does not match")

EXCEPTION_MAP[TdiMISMATCH.status] = TdiMISMATCH
EXCEPTION_PREFIX_MAP[TdiMISMATCH.prefix] = TdiMISMATCH

class TdiMISS_ARG(TdiException):
    status = 265519242
    prefix = "%TDI-E-MISS_ARG"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-MISS_ARG, Missing argument is required for function")

EXCEPTION_MAP[TdiMISS_ARG.status] = TdiMISS_ARG
EXCEPTION_PREFIX_MAP[TdiMISS_ARG.prefix] = TdiMISS_ARG

class TdiNDIM_OVER(TdiException):
    status = 265519250
    prefix = "%TDI-E-NDIM_OVER"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-NDIM_OVER, Number of dimensions is over the allowed 8")

EXCEPTION_MAP[TdiNDIM_OVER.status] = TdiNDIM_OVER
EXCEPTION_PREFIX_MAP[TdiNDIM_OVER.prefix] = TdiNDIM_OVER

class TdiNO_CMPLX(TdiException):
    status = 265519258
    prefix = "%TDI-E-NO_CMPLX"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-NO_CMPLX, There are no complex forms of this function")

EXCEPTION_MAP[TdiNO_CMPLX.status] = TdiNO_CMPLX
EXCEPTION_PREFIX_MAP[TdiNO_CMPLX.prefix] = TdiNO_CMPLX

class TdiNO_OPC(TdiException):
    status = 265519266
    prefix = "%TDI-E-NO_OPC"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-NO_OPC, No support for this function, today")

EXCEPTION_MAP[TdiNO_OPC.status] = TdiNO_OPC
EXCEPTION_PREFIX_MAP[TdiNO_OPC.prefix] = TdiNO_OPC

class TdiNO_OUTPTR(TdiException):
    status = 265519274
    prefix = "%TDI-E-NO_OUTPTR"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-NO_OUTPTR, An output pointer is required")

EXCEPTION_MAP[TdiNO_OUTPTR.status] = TdiNO_OUTPTR
EXCEPTION_PREFIX_MAP[TdiNO_OUTPTR.prefix] = TdiNO_OUTPTR

class TdiNO_SELF_PTR(TdiException):
    status = 265519282
    prefix = "%TDI-E-NO_SELF_PTR"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-NO_SELF_PTR, No $VALUE is defined for signal or validation")

EXCEPTION_MAP[TdiNO_SELF_PTR.status] = TdiNO_SELF_PTR
EXCEPTION_PREFIX_MAP[TdiNO_SELF_PTR.prefix] = TdiNO_SELF_PTR

class TdiNOT_NUMBER(TdiException):
    status = 265519290
    prefix = "%TDI-E-NOT_NUMBER"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-NOT_NUMBER, Value is not a scalar number and must be")

EXCEPTION_MAP[TdiNOT_NUMBER.status] = TdiNOT_NUMBER
EXCEPTION_PREFIX_MAP[TdiNOT_NUMBER.prefix] = TdiNOT_NUMBER

class TdiNULL_PTR(TdiException):
    status = 265519298
    prefix = "%TDI-E-NULL_PTR"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-NULL_PTR, Null pointer where value needed")

EXCEPTION_MAP[TdiNULL_PTR.status] = TdiNULL_PTR
EXCEPTION_PREFIX_MAP[TdiNULL_PTR.prefix] = TdiNULL_PTR

class TdiRECURSIVE(TdiException):
    status = 265519306
    prefix = "%TDI-E-RECURSIVE"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-RECURSIVE, Overly recursive function, calls itself maybe")

EXCEPTION_MAP[TdiRECURSIVE.status] = TdiRECURSIVE
EXCEPTION_PREFIX_MAP[TdiRECURSIVE.prefix] = TdiRECURSIVE

class TdiSIG_DIM(TdiException):
    status = 265519314
    prefix = "%TDI-E-SIG_DIM"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-SIG_DIM, Signal dimension does not match data shape")

EXCEPTION_MAP[TdiSIG_DIM.status] = TdiSIG_DIM
EXCEPTION_PREFIX_MAP[TdiSIG_DIM.prefix] = TdiSIG_DIM

class TdiSYNTAX(TdiException):
    status = 265519322
    prefix = "%TDI-E-SYNTAX"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-SYNTAX, Bad punctuation or misspelled word or number")

EXCEPTION_MAP[TdiSYNTAX.status] = TdiSYNTAX
EXCEPTION_PREFIX_MAP[TdiSYNTAX.prefix] = TdiSYNTAX

class TdiTOO_BIG(TdiException):
    status = 265519330
    prefix = "%TDI-E-TOO_BIG"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-TOO_BIG, Conversion of number lost significant digits")

EXCEPTION_MAP[TdiTOO_BIG.status] = TdiTOO_BIG
EXCEPTION_PREFIX_MAP[TdiTOO_BIG.prefix] = TdiTOO_BIG

class TdiUNBALANCE(TdiException):
    status = 265519338
    prefix = "%TDI-E-UNBALANCE"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-UNBALANCE, Unbalanced () [] {} '' "" or /**/")

EXCEPTION_MAP[TdiUNBALANCE.status] = TdiUNBALANCE
EXCEPTION_PREFIX_MAP[TdiUNBALANCE.prefix] = TdiUNBALANCE

class TdiUNKNOWN_VAR(TdiException):
    status = 265519346
    prefix = "%TDI-E-UNKNOWN_VAR"
    def __init__(self):
        Exception.__init__(self, "%TDI-E-UNKNOWN_VAR, Unknown/undefined variable name")

EXCEPTION_MAP[TdiUNKNOWN_VAR.status] = TdiUNKNOWN_VAR
EXCEPTION_PREFIX_MAP[TdiUNKNOWN_VAR.prefix] = TdiUNKNOWN_VAR

class TdiSTRTOOLON(TdiException):
    status = 265519356
    prefix = "%TDI-F-STRTOOLON"
    def __init__(self):
        Exception.__init__(self, "%TDI-F-STRTOOLON, String is too long (greater than 65535)")

EXCEPTION_MAP[TdiSTRTOOLON.status] = TdiSTRTOOLON
EXCEPTION_PREFIX_MAP[TdiSTRTOOLON.prefix] = TdiSTRTOOLON

class TdiTIMEOUT(TdiException):
    status = 265519364
    prefix = "%TDI-F-TIMEOUT"
    def __init__(self):
        Exception.__init__(self, "%TDI-F-TIMEOUT, Task did not complete in alotted time")

EXCEPTION_MAP[TdiTIMEOUT.status] = TdiTIMEOUT
EXCEPTION_PREFIX_MAP[TdiTIMEOUT.prefix] = TdiTIMEOUT

class ApdException(MdsException):
    pass

class ApdAPD_APPEND(ApdException):
    status = 266141706
    prefix = "%APD-E-APD_APPEND"
    def __init__(self):
        Exception.__init__(self, "%APD-E-APD_APPEND, First argument must be APD or *")

EXCEPTION_MAP[ApdAPD_APPEND.status] = ApdAPD_APPEND
EXCEPTION_PREFIX_MAP[ApdAPD_APPEND.prefix] = ApdAPD_APPEND

class ApdDICT_KEYVALPAIR(ApdException):
    status = 266141714
    prefix = "%APD-E-DICT_KEYVALPAIR"
    def __init__(self):
        Exception.__init__(self, "%APD-E-DICT_KEYVALPAIR, A Dictionary requires an even number of elements")

EXCEPTION_MAP[ApdDICT_KEYVALPAIR.status] = ApdDICT_KEYVALPAIR
EXCEPTION_PREFIX_MAP[ApdDICT_KEYVALPAIR.prefix] = ApdDICT_KEYVALPAIR

class ApdDICT_KEYCLS(ApdException):
    status = 266141722
    prefix = "%APD-E-DICT_KEYCLS"
    def __init__(self):
        Exception.__init__(self, "%APD-E-DICT_KEYCLS, Keys must be scalar, i.e. CLASS_S")

EXCEPTION_MAP[ApdDICT_KEYCLS.status] = ApdDICT_KEYCLS
EXCEPTION_PREFIX_MAP[ApdDICT_KEYCLS.prefix] = ApdDICT_KEYCLS

class TclException(MdsException):
    pass

class TclNORMAL(TclException):
    status = 2752521
    prefix = "%TCL-S-NORMAL"
    def __init__(self):
        Exception.__init__(self, "%TCL-S-NORMAL, Normal successful completion")

EXCEPTION_MAP[TclNORMAL.status] = TclNORMAL
EXCEPTION_PREFIX_MAP[TclNORMAL.prefix] = TclNORMAL

class TclFAILED_ESSENTIAL(TclException):
    status = 2752528
    prefix = "%TCL-W-FAILED_ESSENTIAL"
    def __init__(self):
        Exception.__init__(self, "%TCL-W-FAILED_ESSENTIAL, Essential action failed")

EXCEPTION_MAP[TclFAILED_ESSENTIAL.status] = TclFAILED_ESSENTIAL
EXCEPTION_PREFIX_MAP[TclFAILED_ESSENTIAL.prefix] = TclFAILED_ESSENTIAL

class TclNO_DISPATCH_TABLE(TclException):
    status = 2752536
    prefix = "%TCL-W-NO_DISPATCH_TABLE"
    def __init__(self):
        Exception.__init__(self, "%TCL-W-NO_DISPATCH_TABLE, No dispatch table found. Forgot to do DISPATCH/BUILD?")

EXCEPTION_MAP[TclNO_DISPATCH_TABLE.status] = TclNO_DISPATCH_TABLE
EXCEPTION_PREFIX_MAP[TclNO_DISPATCH_TABLE.prefix] = TclNO_DISPATCH_TABLE

