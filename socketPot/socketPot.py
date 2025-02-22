# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:17:27 2020

@author: jaesung.an
"""
import time, timeit, socket, functools, logging
import numpy as np
from typing import Callable, Optional, Union, List

from socketPot import singleton, paramPotCmd, globalMemory


# decorator for retry POT connection more.
def retry(retries = 3, timetosleep = 3):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for cnt in range(retries):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logging.error(f"POT 연결 {cnt+1} 번째 재시도...\n>> Error message : {e}")
                    PotConnection().disconnect()
                    time.sleep(timetosleep)
                    PotConnection().connect()
            raise Exception(f"POT 연결 재시도 모두 실패")
        return wrapper
    return decorator


class TransferSocket:
    r"""
    Transfer Socket class
    =====================
    1. This is the client socket class for transfering POT data.
    2. It must be initiated whenever you want to do transfering any data.

    Provides
    --------
    1. potCmdWr(cmd :bytes, line :int, data :bytearray, chksumFlag :bool = False)
    2. potCmdRd(cmd :bytes, line :int) -> bytearray
    3. potReady() -> None
    """
    def __init__(self) -> None:
        self.gv = globalMemory.GlobalVariableT24
        self.p = paramPotCmd.ParamPotCmd()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM은 TCP socket을 뜻함
        socket.setdefaulttimeout(1)


    def potCmdWr(self, cmd :bytes, line :int, data :bytearray, chksumFlag :bool = False) -> None:
        # socket buffer flushing
        #self.__flushing()
        # header / footer packet formating
        if self.gv.RESOL == 'QUHD':
            header = bytearray([cmd[0], cmd[1], line&0xFF, (self.p.getWLIdx(cmd)<<5) + (line>>8&0x1F)])
            footer = bytearray([0x0, 0x0, self.p.getTconVer()&0xFF, (self.p.getRLIdx(cmd)<<5) + (self.p.getTconVer()>>8&0x1F)])
        elif self.gv.RESOL in ['UHD', 'UHD+', 'FHD', 'QHD+', 'WQHD+']:
            header = bytearray([cmd[0], cmd[1], line&0xFF, (self.p.getWLIdx(cmd)<<4) + (line>>8&0xF)])
            footer = bytearray([0x0, 0x0, self.p.getTconVer()&0xFF, (self.p.getRLIdx(cmd)<<4) + (self.p.getTconVer()>>8&0xF)])
        else:
            logging.error(f"해상도 정보가 없습니다!\n>> self.gv.RESOL : {self.gv.RESOL}")
        # separate the operation by data type
        if self.p.getWLIdx(cmd) in [1, 2]: # 1 line data packet
            if self.gv.POT_LOG_PRINT: logging.info(f"Header packet 전송 : 0x{header.hex()}")
            # if data is insufficient, padding dummy
            dummy = bytearray(self.gv.LINE_LENGTH-len(data))
            data += dummy
            # send header first
            self.socket.send(header)
            # calculate 4byte checksum for Vparameter
            if chksumFlag:
                if self.gv.ASIC_MODEL in ['T20', 'T19']:
                    data[self.gv.LINE_LENGTH-1] = self.p.calChksum(data[0:self.gv.LINE_LENGTH-1])
                elif self.gv.ASIC_MODEL in ['N22']:  
                    temp_lineLength = int(self.gv.LINE_LENGTH/2)
                    chksum4byte = self.p.calChksum4byte(data[0:temp_lineLength-1])
                    data[temp_lineLength-4] = chksum4byte[0]
                    data[temp_lineLength-3] = chksum4byte[1]
                    data[temp_lineLength-2] = chksum4byte[2]
                    data[temp_lineLength-1] = chksum4byte[3]
                elif self.gv.ASIC_MODEL in ['T26']:
                    chksum4byte = self.p.calChksum4byte(data[0:30719])
                    data[30720-4] = chksum4byte[0]
                    data[30720-3] = chksum4byte[1]
                    data[30720-2] = chksum4byte[2]
                    data[30720-1] = chksum4byte[3]
                else:
                    chksum4byte = self.p.calChksum4byte(data[0:self.gv.LINE_LENGTH-1])
                    data[self.gv.LINE_LENGTH-4] = chksum4byte[0]
                    data[self.gv.LINE_LENGTH-3] = chksum4byte[1]
                    data[self.gv.LINE_LENGTH-2] = chksum4byte[2]
                    data[self.gv.LINE_LENGTH-1] = chksum4byte[3]
            # send data + footer packet
            footer[1] = self.p.calSum(data)
            if self.gv.POT_LOG_PRINT: logging.info(f"Write data, Footer packet 전송")
            self.socket.sendall(data + footer)
        else: # mono packet
            # send header first
            if self.gv.POT_LOG_PRINT: logging.info(f"Header packet 전송 : 0x{header.hex()}")
            # send footer packet
            if self.gv.POT_LOG_PRINT: logging.info(f"Footer packet 전송 : 0x{footer.hex()}")
            self.socket.send(header + footer)
        # check ACK packet
        if (cmd == self.gv.CMD_OFF_RS_START): # Off-RS는 ACK skip
            pass
        else:
            # receive ACK packet
            received = bytearray([])
            while True:
                temp = self.socket.recv(1024)
                received += temp
                if len(received) >= 4:
                    for i in range(len(received)):
                        if received[i] != 0:
                            break
                    break
            received = received[i:]
            if self.gv.POT_LOG_PRINT: logging.info(f"ACK packet 응답 : 0x{received.hex()}")
            if received[0] == 0xFF:
                raise Exception(f"POT Board Time out!\n>> ACK packet 응답 : 0x{received.hex()}")
            else:
                self.p.checkAck(received)
        time.sleep(self.gv.PC_COMMAND_DELAY)
        if (cmd == self.gv.CMD_CLR_PCMODE): time.sleep(self.gv.PC_MODE_CLEAR_DELAY)


    def potCmdRd(self, cmd :bytes, line :int) -> bytearray:
        # socket buffer flushing
        #self.__flushing()
        # header / footer packet formating
        if self.gv.RESOL == 'QUHD':
            header = bytearray([cmd[0], cmd[1], line&0xFF, (self.p.getWLIdx(cmd)<<5) + (line>>8&0x1F)])
            footer = bytearray([0x0, 0x0, self.p.getTconVer()&0xFF, (self.p.getRLIdx(cmd)<<5) + (self.p.getTconVer()>>8&0x1F)])
        elif self.gv.RESOL in ['UHD', 'UHD+', 'FHD', 'QHD+', 'WQHD+']:
            header = bytearray([cmd[0], cmd[1], line&0xFF, (self.p.getWLIdx(cmd)<<4) + (line>>8&0xF)])
            footer = bytearray([0x0, 0x0, self.p.getTconVer()&0xFF, (self.p.getRLIdx(cmd)<<4) + (self.p.getTconVer()>>8&0xF)])
        else:
            logging.error(f"해상도 정보가 없습니다!\n>> self.gv.RESOL : {self.gv.RESOL}")
        # send header first
        if self.gv.POT_LOG_PRINT: logging.info(f"Header packet 전송 : 0x{header.hex()}")
        # send footer second
        if self.gv.POT_LOG_PRINT: logging.info(f"Footer packet 전송 : 0x{footer.hex()}")
        self.socket.send(header + footer)
        # receive packet stream
        st = timeit.default_timer()
        received = bytearray([])
        while True:
            temp = self.socket.recv(self.gv.LINE_LENGTH+12)
            received += temp
            delay = timeit.default_timer() - st
            if len(received) >= self.gv.LINE_LENGTH+12 or delay > 120:
                for i in range(len(received)-3):
                    if received[i] == header[0]:
                        break
                received = received[i:]
                break
        # receive remain packet stream
        while True:
            temp = self.socket.recv(self.gv.LINE_LENGTH+12-len(received))
            received += temp
            if len(received) >= self.gv.LINE_LENGTH+12 or delay > 120:
                break
        data = received[4:self.gv.LINE_LENGTH+4]
        footer = received[self.gv.LINE_LENGTH+4:self.gv.LINE_LENGTH+8]
        # footer check
        self.p.checkFooter(data, footer)
        return data


    def potReady(self) -> None:
        try:
            if self.gv.POT_LOG_PRINT: logging.info(f"(PC --> POT) TCP 연결 성공.\n>> Port Number : {self.gv.OP_PORTNUM}")
            # connecting server as client
            self.socket.connect((self.gv.POT_IP, self.gv.OP_PORTNUM))
            # check ACK packet
            received = self.socket.recv(4)
            if received == b'\x00\x04\x00\x00':
                if self.gv.POT_LOG_PRINT: logging.info(f"Ready packet 응답 : 0x{received.hex()}")
            else:
                raise Exception(f"POT ready ACK Fail!\n>> ACK packet 응답 : 0x{received.hex()}")
        except Exception as e:
            logging.error(f"POT Ready state 진입에 실패하였습니다.\n>> POT IP Address : {self.gv.POT_IP}\n>> Port Number : {self.gv.OP_PORTNUM}\n>> Error message : {e}")
            raise
        finally:
            time.sleep(self.gv.POT_CONNECT_DELAY)


    #def __flushing(self):
    #    r"""
    #    Description
    #    -----------
    #    socket buffer flushing
    #    """
    #    self.socket.setblocking(False)
    #    ready = select.select([self.socket], [], [], 0.001)
    #    if ready[0]:
    #        data = self.socket.recv(1024)
    #    self.socket.setblocking(True)


class PhaseLockSocket:
    r"""
    Phase Lock Socket class
    =======================
    1. This is the client socket class for POT connection phase lock process.
    2. It must be initiated and set phase lock once.

    Provides
    --------
    1. potPLsetting() -> None
    """
    def __init__(self) -> None:
        self.gv = globalMemory.GlobalVariableT24
        self.p = paramPotCmd.ParamPotCmd()
        self.socketPL = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM은 TCP socket을 뜻함
        socket.setdefaulttimeout(1)


    def potPLsetting(self) -> None:
        try:
            # connecting server as client
            if self.gv.POT_LOG_PRINT: logging.info(f"(PC --> POT) TCP 연결 성공.\n>> Port Number : {self.gv.PL_PORTNUM}")
            self.socketPL.connect((self.gv.POT_IP, self.gv.PL_PORTNUM)) # 서버에 연결 요청
            # send phase lock packet
            if self.gv.POT_LOG_PRINT: logging.info(f"Phase Lock 설정 값 전송 : {self.gv.PL_SETTING}")
            self.socketPL.send(bytes(self.gv.PL_SETTING, encoding = 'ascii')) # 메시지 송신
            # receive ACK packet
            received = self.socketPL.recv(8)
            received2str = str(received, encoding = 'ascii')
            if self.gv.POT_LOG_PRINT: logging.info(f"PL 설정 응답 : {received2str}")
        except Exception as e:
            logging.error(f"POT Phase Lock state 진입에 실패했습니다.\n>> POT IP Address : {self.gv.POT_IP}\n>> Port Number : {self.gv.PL_PORTNUM}\n>> Error message : {e}")
            raise
        finally:
            time.sleep(self.gv.POT_CONNECT_DELAY)


class PotConnection(metaclass = singleton.Singleton):
    r"""
    POT Connection class
    =====================
    1. This is the handler class for using POT command
    2. This is singleton
    3. It must be initiated with callable methods. If you don't need them, make blank functions and input it.

    Provides
    --------
    1. connect() -> None
    2. disconnect() -> None
    3. isConnected() -> bool
    4. writeTransferMono(cmd :Optional[Union[List[bytes], bytes]]) -> None
    5. writeTransferLine(cmd :Optional[Union[List[bytes], bytes]], lineNumber :int, dataType :str) -> None
    6. readTransferLine(cmd :Optional[Union[List[bytes], bytes]], lineNumber :int, dataType :str) -> None
    7. writeTransferBurst(cmd :Optional[Union[List[bytes], bytes]], dataType :str) -> None
    8. readTransferBurst(cmd :Optional[Union[List[bytes], bytes]], dataType :str) -> None
    """
    __s = None # phase lock socket
    __t = None # transfer socket

    def __init__(self,) -> None:
        self.gv = globalMemory.GlobalVariableT24
        self.dc = globalMemory.GlobalDataContainer
        self.p = paramPotCmd.ParamPotCmd()
        # Instantiate
        self.__donePLsetting = False
        self.__doneTrsetting = False
        PotConnection.__s = self.__initPLSocket()
        PotConnection.__t = self.__initTrSocket()


    def connect(self) -> None:
        try:
            PotConnection.__s = self.__initPLSocket()
            PotConnection.__s.potPLsetting()
            self.__donePLsetting = True
            PotConnection.__t = self.__initTrSocket()
            PotConnection.__t.potReady()
            self.__doneTrsetting = True
            logging.info(f"POT 통신이 연결되었습니다.")
        except Exception:
            self.disconnect()
            logging.error(f"POT 통신 연결에 실패하였습니다.")
            raise


    def disconnect(self) -> None:
        try:
            if PotConnection.__s is not None:
                PotConnection.__s.socketPL.close()
                PotConnection.__s = None
                self.__donePLsetting = False
            if PotConnection.__t is not None:
                PotConnection.__t.socket.close()
                PotConnection.__t = None
                self.__doneTrsetting = False
            logging.info(f"POT 통신이 해제되었습니다.")
        except Exception:
            logging.warning(f"POT 통신 해제에 실패하였습니다.")
            raise


    def isConnected(self) -> bool:
        if self.__donePLsetting and self.__doneTrsetting:
            return True
        return False


    def __initPLSocket(self) -> PhaseLockSocket: # Instantiate
        if getattr(self, '__s', None) is None:
            s = PhaseLockSocket()
            logging.info(f"POT Phase Lock Socket 이 생성되었습니다.")
            return s
        else:
            return PotConnection.__s


    def __initTrSocket(self) -> TransferSocket: # Instantiate
        if getattr(self, '__t', None) is None:
            t = TransferSocket()
            logging.info(f"POT Transfer Socket 이 생성되었습니다.")
            return t
        else:
            return PotConnection.__t


    def __checkSocket(self) -> None:
        if self.__donePLsetting is False or self.__doneTrsetting is False:
            self.connect()


    @retry(retries = 3)
    def writeTransferMono(self, cmd :Optional[Union[List[bytes], bytes]]) -> None:
        self.__checkSocket()
        if type(cmd) is list:
            for c in cmd:
                PotConnection.__t.potCmdWr(cmd = c, line = 0, data = 0)
        else:
            PotConnection.__t.potCmdWr(cmd = cmd, line = 0, data = 0)


    @retry(retries = 3)
    def writeTransferLine(self, cmd :Optional[Union[List[bytes], bytes]], lineNumber :int, dataType :str) -> None:
        self.__checkSocket()
        if dataType.lower() == 'os':
            byteArr = self.__os2byteArray(row = lineNumber, isMSB = True)
            # POT socket write command
            PotConnection.__t.potCmdWr(cmd = cmd[0], line = lineNumber, data = byteArr)
            byteArr = self.__os2byteArray(row = lineNumber, isMSB = False)
            # POT socket write command
            PotConnection.__t.potCmdWr(cmd = cmd[1], line = lineNumber, data = byteArr)
        else:
            if dataType.lower() == 'comp':
                byteArr = self.__comp2byteArray(row = lineNumber)
            elif dataType.lower() == 'sen':
                byteArr = self.__sen2byteArray(row = lineNumber)
            elif dataType.lower() == 'oc':
                byteArr = self.__oc2byteArray(row = lineNumber)
            elif dataType.lower() == 'ycb':
                byteArr = self.__ycb2byteArray(row = lineNumber)
            elif dataType.lower() == 'cb':
                byteArr = self.__cb2byteArray(row = lineNumber)
            elif dataType.lower() == 'apg':
                byteArr = self.__apg2byteArray(row = lineNumber)
            elif dataType.lower() == 'setting':
                byteArr = self.__setting2byteArray(order = lineNumber)
            elif dataType.lower() == 'lut':
                byteArr = self.__lut2byteArray(row = lineNumber, cmd = cmd)
            elif dataType.lower() == 'oparam':
                byteArr = self.__oparam2byteArray()
            else:
                raise Exception(f"dataType이 적절하지 않습니다.\n>> dataType : {dataType}")
            # POT socket write command
            if cmd in [self.gv.CMD_WR_TCON_VPARAM, self.gv.CMD_WR_NAND_SET_VPARAM, self.gv.CMD_WR_NAND_LGD_VPARAM] and lineNumber == 0:
                PotConnection.__t.potCmdWr(cmd = cmd, line = lineNumber, data = byteArr, chksumFlag = True)
            else:
                PotConnection.__t.potCmdWr(cmd = cmd, line = lineNumber, data = byteArr)


    @retry(retries = 3)
    def readTransferLine(self, cmd :Optional[Union[List[bytes], bytes]], lineNumber :int, dataType :str) -> None:
        self.__checkSocket()
        if dataType.lower() == 'os':
            byteArr = PotConnection.__t.potCmdRd(cmd = cmd[0], line = lineNumber)
            self.__byteArray2os(row = lineNumber, byteArr = byteArr, isMSB = True)
            byteArr = PotConnection.__t.potCmdRd(cmd = cmd[1], line = lineNumber)
            self.__byteArray2os(row = lineNumber, byteArr = byteArr, isMSB = False)
        else:
            # POT socket read command
            byteArr = PotConnection.__t.potCmdRd(cmd = cmd, line = lineNumber)
            # transform by data type
            if dataType.lower() == 'comp':
                self.__byteArray2comp(row = lineNumber, byteArr = byteArr)
            elif dataType.lower() == 'sen':
                self.__byteArray2sen(row = lineNumber, byteArr = byteArr)
            elif dataType.lower() == 'oc':
                self.__byteArray2oc(row = lineNumber, byteArr = byteArr)
            elif dataType.lower() == 'ycb':
                self.__byteArray2ycb(row = lineNumber, byteArr = byteArr)
            elif dataType.lower() == 'cb':
                self.__byteArray2cb(row = lineNumber, byteArr = byteArr)
            elif dataType.lower() == 'apg':
                self.__byteArray2apg(row = lineNumber, byteArr = byteArr)
            elif dataType.lower() == 'setting':
                self.__byteArray2setting(order = lineNumber, byteArr = byteArr)
            elif dataType.lower() == 'lut':
                self.__byteArray2lut(row = lineNumber, byteArr = byteArr, cmd = cmd)
            elif dataType.lower() == 'oparam':
                self.__byteArray2oparam(byteArr = byteArr)
            else:
                raise Exception(f"dataType이 적절하지 않습니다.\n>> dataType : {dataType}")


    @retry(retries = 3)
    def writeTransferBurst(self, cmd :Optional[Union[List[bytes], bytes]], dataType :str) -> None:
        self.__checkSocket()
        # select total line
        if dataType.lower() == 'setting':
            sline = 0
            nline = self.gv.NUM_OF_VPARAM_LUT
        elif dataType.lower() == 'nand_oc':
            dataType = 'oc'
            if self.gv.ASIC_MODEL in ['T22','T24','K23']:
                sline = 1
            else:
                sline = 0
            nline = self.gv.nrow
        elif dataType.lower() == 'os':
            sline = 0
            nline = 2*self.gv.nrow
        elif dataType.lower() == 'cb':
            sline = 0
            nline = self.gv.CB_LINE
        elif dataType.lower() == 'apg':
            sline = 0
            nline = self.gv.APG_LINE
        else:
            sline = 0
            nline = self.gv.nrow
        # repeat for burst
        if dataType.lower() == 'os':
            for i in range(sline, nline):
                if self.gv.ASIC_MODEL in ['T22','T24','K23']:
                    # run 1frame twice
                    row = int(i/2)
                    if i % 2 == 0: # MSB first
                        isMSB = True
                        cmdWr = cmd[0]
                    else: # LSB
                        isMSB = False
                        cmdWr = cmd[1]
                else:
                    if i < self.gv.nrow:
                        isMSB = True
                        cmdWr = cmd[0]
                        row = i
                    else:
                        isMSB = False
                        cmdWr = cmd[1]
                        row = i - self.gv.nrow
                # transform by data type
                byteArr = self.__os2byteArray(row = row, isMSB = isMSB)
                # POT socket write command
                PotConnection.__t.potCmdWr(cmd = cmdWr, line = row, data = byteArr)
        else:
            for i in range(sline, nline):
                # transform by data type
                if dataType.lower() == 'comp':
                    byteArr = self.__comp2byteArray(row = i)
                elif dataType.lower() == 'sen':
                    byteArr = self.__sen2byteArray(row = i)
                elif dataType.lower() == 'oc':
                    byteArr = self.__oc2byteArray(row = i)
                elif dataType.lower() == 'ycb':
                    byteArr = self.__ycb2byteArray(row = i)
                elif dataType.lower() == 'cb':
                    byteArr = self.__cb2byteArray(row = i)
                elif dataType.lower() == 'apg':
                    byteArr = self.__apg2byteArray(row = i)
                elif dataType.lower() == 'setting':
                    byteArr = self.__setting2byteArray(order = i)
                else:
                    raise Exception(f"dataType이 적절하지 않습니다.\n>> dataType : {dataType}")
                # POT socket write command
                if cmd in [self.gv.CMD_WR_TCON_VPARAM, self.gv.CMD_WR_NAND_SET_VPARAM, self.gv.CMD_WR_NAND_LGD_VPARAM] and i == 0:
                    PotConnection.__t.potCmdWr(cmd = cmd, line = i, data = byteArr, chksumFlag = True)
                else:
                    PotConnection.__t.potCmdWr(cmd = cmd, line = i, data = byteArr)


    @retry(retries = 3)
    def readTransferBurst(self, cmd :Optional[Union[List[bytes], bytes]], dataType :str) -> None:
        self.__checkSocket()
        # select total line
        if dataType.lower() == 'setting':
            sline = 0
            nline = self.gv.NUM_OF_VPARAM_LUT
        elif dataType.lower() == 'nand_oc':
            dataType = 'oc'
            if self.gv.ASIC_MODEL in ['T22','T24','K23']:
                sline = 1
            else:
                sline = 0
            nline = self.gv.nrow
        elif dataType.lower() == 'os':
            sline = 0
            nline = 2*self.gv.nrow
        elif dataType.lower() == 'cb':
            sline = 0
            nline = self.gv.CB_LINE
        elif dataType.lower() == 'apg':
            sline = 0
            nline = self.gv.APG_LINE
        else:
            sline = 0
            nline = self.gv.nrow
        # repeat for burst
        if dataType.lower() == 'os':
            for i in range(sline, nline):
                if self.gv.ASIC_MODEL in ['T22','T24','K23']:
                    # run 1frame twice
                    row = int(i/2)
                    if i % 2 == 0: # MSB first
                        isMSB = True
                        cmdRd = cmd[0]
                    else: # LSB
                        isMSB = False
                        cmdRd = cmd[1]
                else:
                    if i < self.gv.nrow:
                        isMSB = True
                        cmdRd = cmd[0]
                        row = i
                    else:
                        isMSB = False
                        cmdRd = cmd[1]
                        row = i - self.gv.nrow
                # POT socket read command
                byteArr = PotConnection.__t.potCmdRd(cmd = cmdRd, line = row)
                # transform by data type
                self.__byteArray2os(row = row, byteArr = byteArr, isMSB = isMSB)
        else:
            for i in range(sline, nline):
                # POT socket read command
                byteArr = PotConnection.__t.potCmdRd(cmd = cmd, line = i)
                # transform by data type
                if dataType.lower() == 'comp':
                    self.__byteArray2comp(row = i, byteArr = byteArr)
                elif dataType.lower() == 'sen':
                    self.__byteArray2sen(row = i, byteArr = byteArr)
                elif dataType.lower() == 'oc':
                    self.__byteArray2oc(row = i, byteArr = byteArr)
                elif dataType.lower() == 'ycb':
                    self.__byteArray2ycb(row = i, byteArr = byteArr)
                elif dataType.lower() == 'cb':
                    self.__byteArray2cb(row = i, byteArr = byteArr)
                elif dataType.lower() == 'apg':
                    self.__byteArray2apg(row = i, byteArr = byteArr)
                elif dataType.lower() == 'setting':
                    self.__byteArray2setting(order = i, byteArr = byteArr)
                else:
                    raise Exception(f"dataType이 적절하지 않습니다.\n>> dataType : {dataType}")


    def __comp2byteArray(self, row :int) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container comp data to bytearray.
        2. This is one line data process.
        """
        # phi / alpha --> comp formating
        comp = np.empty(self.gv.ncol, np.uint8)
        comp[0::8] = self.dc.rPhiContainer[row, :] & 0b11111111 # Phi LSB 8bit
        comp[1::8] = (self.dc.rAlphaContainer[row, :] << 2) + (self.dc.rPhiContainer[row, :] >> 8) # Alpha 6bit + Phi MSB 2bit
        comp[2::8] = self.dc.wPhiContainer[row, :] & 0b11111111 # Phi LSB 8bit
        comp[3::8] = (self.dc.wAlphaContainer[row, :] << 2) + (self.dc.wPhiContainer[row, :] >> 8) # Alpha 6bit + Phi MSB 2bit
        comp[4::8] = self.dc.gPhiContainer[row, :] & 0b11111111 # Phi LSB 8bit
        comp[5::8] = (self.dc.gAlphaContainer[row, :] << 2) + (self.dc.gPhiContainer[row, :] >> 8) # Alpha 6bit + Phi MSB 2bit
        comp[6::8] = self.dc.bPhiContainer[row, :] & 0b11111111 # Phi LSB 8bit
        comp[7::8] = (self.dc.bAlphaContainer[row, :] << 2) + (self.dc.bPhiContainer[row, :] >> 8) # Alpha 6bit + Phi MSB 2bit
        return bytearray(comp)


    def __byteArray2comp(self, row :int, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container comp data.
        2. This is one line data process.
        """
        # comp --> phi / alpha formating (list comprehension for speed)
        self.dc.rPhiContainer  [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(0, self.gv.ncol, 8)]
        self.dc.rAlphaContainer[row, :] = [byteArr[i] >> 2 for i in range(1, self.gv.ncol, 8)]
        self.dc.wPhiContainer  [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(2, self.gv.ncol, 8)]
        self.dc.wAlphaContainer[row, :] = [byteArr[i] >> 2 for i in range(3, self.gv.ncol, 8)]
        self.dc.gPhiContainer  [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(4, self.gv.ncol, 8)]
        self.dc.gAlphaContainer[row, :] = [byteArr[i] >> 2 for i in range(5, self.gv.ncol, 8)]
        self.dc.bPhiContainer  [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(6, self.gv.ncol, 8)]
        self.dc.bAlphaContainer[row, :] = [byteArr[i] >> 2 for i in range(7, self.gv.ncol, 8)]


    def __byteArray2sen(self, row :int, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container sensing data.
        2. This is one line data process.
        """
        # bytearray --> sensing data formating (list comprehension for speed)
        self.dc.rSensContainer [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(0, self.gv.ncol, 8)] # MSB 2bit + LSB 8bit
        self.dc.wSensContainer [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(2, self.gv.ncol, 8)] # MSB 2bit + LSB 8bit
        self.dc.gSensContainer [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(4, self.gv.ncol, 8)] # MSB 2bit + LSB 8bit
        self.dc.bSensContainer [row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(6, self.gv.ncol, 8)] # MSB 2bit + LSB 8bit


    def __sen2byteArray(self, row :int) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container sensing data to bytearray.
        2. This is one line data process.
        """
        # 10bit sen --> 8bit+8bit sen formating
        sen = np.empty(self.gv.ncol, np.uint8)
        sen[0::8] = self.dc.rSensContainer[row, :] & 0b11111111 # Sen LSB 8bit
        sen[1::8] = self.dc.rSensContainer[row, :] >> 8 # Sen MSB 2bit
        sen[2::8] = self.dc.wSensContainer[row, :] & 0b11111111 # Sen LSB 8bit
        sen[3::8] = self.dc.wSensContainer[row, :] >> 8 # Sen MSB 2bit
        sen[4::8] = self.dc.gSensContainer[row, :] & 0b11111111 # Sen LSB 8bit
        sen[5::8] = self.dc.gSensContainer[row, :] >> 8 # Sen MSB 2bit
        sen[6::8] = self.dc.bSensContainer[row, :] & 0b11111111 # Sen LSB 8bit
        sen[7::8] = self.dc.bSensContainer[row, :] >> 8 # Sen MSB 2bit
        return bytearray(sen)


    def __byteArray2oc(self, row :int, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container OC data.
        2. This is one line data process.
        """
        # bytearray --> OC data formating (list comprehension for speed)
        self.dc.rOCContainer [row, 0::4] = [byteArr[i] for i in range( 0, self.gv.ncol, 32)] # 8bit
        self.dc.rOCContainer [row, 1::4] = [byteArr[i] for i in range( 4, self.gv.ncol, 32)] # 8bit
        self.dc.rOCContainer [row, 2::4] = [byteArr[i] for i in range( 8, self.gv.ncol, 32)] # 8bit
        self.dc.rOCContainer [row, 3::4] = [byteArr[i] for i in range(12, self.gv.ncol, 32)] # 8bit
        self.dc.wOCContainer [row, 0::4] = [byteArr[i] for i in range( 1, self.gv.ncol, 32)] # 8bit
        self.dc.wOCContainer [row, 1::4] = [byteArr[i] for i in range( 5, self.gv.ncol, 32)] # 8bit
        self.dc.wOCContainer [row, 2::4] = [byteArr[i] for i in range( 9, self.gv.ncol, 32)] # 8bit
        self.dc.wOCContainer [row, 3::4] = [byteArr[i] for i in range(13, self.gv.ncol, 32)] # 8bit
        self.dc.gOCContainer [row, 0::4] = [byteArr[i] for i in range( 2, self.gv.ncol, 32)] # 8bit
        self.dc.gOCContainer [row, 1::4] = [byteArr[i] for i in range( 6, self.gv.ncol, 32)] # 8bit
        self.dc.gOCContainer [row, 2::4] = [byteArr[i] for i in range(10, self.gv.ncol, 32)] # 8bit
        self.dc.gOCContainer [row, 3::4] = [byteArr[i] for i in range(14, self.gv.ncol, 32)] # 8bit
        self.dc.bOCContainer [row, 0::4] = [byteArr[i] for i in range( 3, self.gv.ncol, 32)] # 8bit
        self.dc.bOCContainer [row, 1::4] = [byteArr[i] for i in range( 7, self.gv.ncol, 32)] # 8bit
        self.dc.bOCContainer [row, 2::4] = [byteArr[i] for i in range(11, self.gv.ncol, 32)] # 8bit
        self.dc.bOCContainer [row, 3::4] = [byteArr[i] for i in range(15, self.gv.ncol, 32)] # 8bit


    def __oc2byteArray(self, row :int) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container OC data to bytearray.
        2. This is one line data process.
        """
        oc = np.empty(self.gv.ncol, np.uint8)
        oc[ 0::32] = self.dc.rOCContainer [row, 0::4]
        oc[ 4::32] = self.dc.rOCContainer [row, 1::4]
        oc[ 8::32] = self.dc.rOCContainer [row, 2::4]
        oc[12::32] = self.dc.rOCContainer [row, 3::4]
        oc[ 1::32] = self.dc.wOCContainer [row, 0::4]
        oc[ 5::32] = self.dc.wOCContainer [row, 1::4]
        oc[ 9::32] = self.dc.wOCContainer [row, 2::4]
        oc[13::32] = self.dc.wOCContainer [row, 3::4]
        oc[ 2::32] = self.dc.gOCContainer [row, 0::4]
        oc[ 6::32] = self.dc.gOCContainer [row, 1::4]
        oc[10::32] = self.dc.gOCContainer [row, 2::4]
        oc[14::32] = self.dc.gOCContainer [row, 3::4]
        oc[ 3::32] = self.dc.bOCContainer [row, 0::4]
        oc[ 7::32] = self.dc.bOCContainer [row, 1::4]
        oc[11::32] = self.dc.bOCContainer [row, 2::4]
        oc[15::32] = self.dc.bOCContainer [row, 3::4]
        return bytearray(oc)


    def __byteArray2os(self, row :int, byteArr :bytearray, isMSB :bool) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container OS data.
        2. This is one line data process.
        """
        # bytearray --> OS data formating (list comprehension for speed)
        if isMSB:
            self.dc.rOSContainer [row, :] = [(byteArr[i + 1] << 24) + (byteArr[i] << 16) for i in range(0, self.gv.ncol, 8)] # OS[31:24] 8bit + OS[23:16] 8bit
            self.dc.wOSContainer [row, :] = [(byteArr[i + 1] << 24) + (byteArr[i] << 16) for i in range(2, self.gv.ncol, 8)] # OS[31:24] 8bit + OS[23:16] 8bit
            self.dc.gOSContainer [row, :] = [(byteArr[i + 1] << 24) + (byteArr[i] << 16) for i in range(4, self.gv.ncol, 8)] # OS[31:24] 8bit + OS[23:16] 8bit
            self.dc.bOSContainer [row, :] = [(byteArr[i + 1] << 24) + (byteArr[i] << 16) for i in range(6, self.gv.ncol, 8)] # OS[31:24] 8bit + OS[23:16] 8bit
        else:
            self.dc.rOSContainer [row, :] = self.dc.rOSContainer [row, :] + [(byteArr[i + 1] << 8) + byteArr[i] for i in range(0, self.gv.ncol, 8)] # OS[15:8] 8bit + OS[7:0] 8bit
            self.dc.wOSContainer [row, :] = self.dc.wOSContainer [row, :] + [(byteArr[i + 1] << 8) + byteArr[i] for i in range(2, self.gv.ncol, 8)] # OS[15:8] 8bit + OS[7:0] 8bit
            self.dc.gOSContainer [row, :] = self.dc.gOSContainer [row, :] + [(byteArr[i + 1] << 8) + byteArr[i] for i in range(4, self.gv.ncol, 8)] # OS[15:8] 8bit + OS[7:0] 8bit
            self.dc.bOSContainer [row, :] = self.dc.bOSContainer [row, :] + [(byteArr[i + 1] << 8) + byteArr[i] for i in range(6, self.gv.ncol, 8)] # OS[15:8] 8bit + OS[7:0] 8bit


    def __os2byteArray(self, row :int, isMSB :bool) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container OS data to bytearray.
        2. This is one line data process.
        """
        # 32bit OS --> 8bit+8bit+8bit+8bit OS formating
        os = np.empty(self.gv.ncol, np.uint8)
        if isMSB:
            os[0::8] = (self.dc.rOSContainer[row, :] & 0b11111111_00000000_00000000) >> 16 # OS[23:16]
            os[1::8] = (self.dc.rOSContainer[row, :] & 0b11111111_00000000_00000000_00000000) >> 24 # OS[31:24]
            os[2::8] = (self.dc.wOSContainer[row, :] & 0b11111111_00000000_00000000) >> 16 # OS[23:16]
            os[3::8] = (self.dc.wOSContainer[row, :] & 0b11111111_00000000_00000000_00000000) >> 24 # OS[31:24]
            os[4::8] = (self.dc.gOSContainer[row, :] & 0b11111111_00000000_00000000) >> 16 # OS[23:16]
            os[5::8] = (self.dc.gOSContainer[row, :] & 0b11111111_00000000_00000000_00000000) >> 24 # OS[31:24]
            os[6::8] = (self.dc.bOSContainer[row, :] & 0b11111111_00000000_00000000) >> 16 # OS[23:16]
            os[7::8] = (self.dc.bOSContainer[row, :] & 0b11111111_00000000_00000000_00000000) >> 24 # OS[31:24]
        else:
            os[0::8] = self.dc.rOSContainer[row, :] & 0b11111111 # OS[7:0]
            os[1::8] = (self.dc.rOSContainer[row, :] & 0b11111111_00000000) >> 8 # OS[15:8]
            os[2::8] = self.dc.wOSContainer[row, :] & 0b11111111 # OS[7:0]
            os[3::8] = (self.dc.wOSContainer[row, :] & 0b11111111_00000000) >> 8 # OS[15:8]
            os[4::8] = self.dc.gOSContainer[row, :] & 0b11111111 # OS[7:0]
            os[5::8] = (self.dc.gOSContainer[row, :] & 0b11111111_00000000) >> 8 # OS[15:8]
            os[6::8] = self.dc.bOSContainer[row, :] & 0b11111111 # OS[7:0]
            os[7::8] = (self.dc.bOSContainer[row, :] & 0b11111111_00000000) >> 8 # OS[15:8]
        return bytearray(os)


    def __ycb2byteArray(self, row :int) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container ycb data to bytearray.
        2. This is one line data process.
        """
        ycb = np.empty(self.gv.ncol, np.uint8)
        ycb[0::8] = self.dc.rYCBContainer[row, :] & 0b11111111 # YCB LSB 8bit
        ycb[1::8] = self.dc.rYCBContainer[row, :] >> 8 # YCB MSB 2bit
        ycb[2::8] = self.dc.wYCBContainer[row, :] & 0b11111111 # YCB LSB 8bit
        ycb[3::8] = self.dc.wYCBContainer[row, :] >> 8 # YCB MSB 2bit
        ycb[4::8] = self.dc.gYCBContainer[row, :] & 0b11111111 # YCB LSB 8bit
        ycb[5::8] = self.dc.gYCBContainer[row, :] >> 8 # YCB MSB 2bit
        ycb[6::8] = self.dc.bYCBContainer[row, :] & 0b11111111 # YCB LSB 8bit
        ycb[7::8] = self.dc.bYCBContainer[row, :] >> 8 # YCB MSB 2bit
        return bytearray(ycb)


    def __byteArray2ycb(self, row :int, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container ycb data.
        2. This is one line data process.
        """
        # bytearray --> YCB data formating (list comprehension for speed)
        self.dc.rYCBContainer[row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(0, self.gv.ncol, 8)]
        self.dc.wYCBContainer[row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(2, self.gv.ncol, 8)]
        self.dc.gYCBContainer[row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(4, self.gv.ncol, 8)]
        self.dc.bYCBContainer[row, :] = [((byteArr[i + 1] & 0b11) << 8) + byteArr[i] for i in range(6, self.gv.ncol, 8)]


    def __cb2byteArray(self, row :int) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container CB data to bytearray.
        2. This is one line data process.
        """
        # bytearray transfer
        return bytearray(self.dc.CBContainer[row, :].astype(np.uint8))


    def __byteArray2cb(self, row :int, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container CB data.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            LINE_LENGTH = 30720
        else:
            LINE_LENGTH = self.gv.LINE_LENGTH
        # bytearray --> CB data formating (list comprehension for speed)
        self.dc.CBContainer[row, :] = [byteArr[i] for i in range(LINE_LENGTH)]


    def __apg2byteArray(self, row :int) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container APG data to bytearray.
        2. This is one line data process.
        """
        # bytearray transfer
        return bytearray(self.dc.APGContainer[row, :].astype(np.uint8))


    def __byteArray2apg(self, row :int, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container APG data.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            LINE_LENGTH = 30720
        else:
            LINE_LENGTH = self.gv.LINE_LENGTH
        # bytearray --> APG data formating (list comprehension for speed)
        self.dc.APGContainer[row, :] = [byteArr[i] for i in range(LINE_LENGTH)]


    def __byteArray2setting(self, order :int, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container setting LUT.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            lut = self.dc.vParam
            LINE_LENGTH = 30720
        else:
            lut = self.dc.lut[order]
            LINE_LENGTH = self.gv.LINE_LENGTH
        for col in range(0, LINE_LENGTH):
            # Global Data Container update
            lut[col] = byteArr[col]


    def __setting2byteArray(self, order :int) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container setting LUT to bytearray.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            lut = self.dc.vParam
            LINE_LENGTH = 30720
        else:
            lut = self.dc.lut[order]
            LINE_LENGTH = self.gv.LINE_LENGTH
        # bytearray transfer
        byteArr = bytearray(LINE_LENGTH)
        for col in range(0, LINE_LENGTH):
            # Global Data Container
            data = int(lut[col])
            # bytearray
            byteArr[col] = data

        return byteArr


    def __byteArray2lut(self, row :int, byteArr :bytearray, cmd :Optional[Union[List[bytes], bytes]] = None) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Data Container LUT.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            LINE_LENGTH = 30720
        else:
            LINE_LENGTH = self.gv.LINE_LENGTH
        if self.gv.ASIC_MODEL in ['T22','T24','K23']:
            buffer = self.dc.lineBuffer[row]
        else:
            if cmd == self.gv.CMD_RD_NAND_YB_LUTS:
                buffer = self.dc.lut[row]
            else:
                buffer = self.dc.lineBuffer[row]
        for col in range(0, LINE_LENGTH):
            # Global Data Container update
            buffer[col] = byteArr[col]


    def __lut2byteArray(self, row :int, cmd :Optional[Union[List[bytes], bytes]]) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Data Container LUT to bytearray.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            LINE_LENGTH = 30720
        else:
            LINE_LENGTH = self.gv.LINE_LENGTH
        if self.gv.ASIC_MODEL in ['T22','T24','K23']:
            buffer = self.dc.lineBuffer[row]
        else:
            if cmd == self.gv.CMD_WR_NAND_YB_LUTS:
                buffer = self.dc.lut[row]
            else:
                buffer = self.dc.lineBuffer[row]
        # bytearray transfer
        byteArr = bytearray(LINE_LENGTH)
        for col in range(0, LINE_LENGTH):
            # Global Data Container load
            data = int(buffer[col])
            # bytearray save
            byteArr[col] = data
        if cmd == self.gv.CMD_WR_NAND_LPARAM:
            # fix NAND Lparam valid code
            byteArr[0] = self.gv.LPARAM_NAND_VALID
            # insert Lparameter checksum
            byteArr[self.gv.LPARAM_CHKSUM_ADDR] = self.p.calLparamChksum(byteArr[0:self.gv.LPARAM_CHKSUM_ADDR])
        elif cmd == self.gv.CMD_WR_NAND_SET_PDCS_LUT1 or cmd == self.gv.CMD_WR_NAND_SET_PDCS_LUT2:
            chksum4byte = self.p.calChksum4byte(byteArr[0:LINE_LENGTH-1])
            byteArr[LINE_LENGTH-4] = chksum4byte[0]
            byteArr[LINE_LENGTH-3] = chksum4byte[1]
            byteArr[LINE_LENGTH-2] = chksum4byte[2]
            byteArr[LINE_LENGTH-1] = chksum4byte[3]
        return byteArr


    def __byteArray2oparam(self, byteArr :bytearray) -> None:
        r"""
        Description
        -----------
        1. This transfer bytearray to Global Oparam Data Container.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            LINE_LENGTH = 30720
        else:
            LINE_LENGTH = self.gv.LINE_LENGTH
        for col in range(0, LINE_LENGTH):
            # Global Data Container update
            self.dc.oParam[col] = byteArr[col]


    def __oparam2byteArray(self) -> bytearray:
        r"""
        Description
        -----------
        1. This transfer Global Oparam Data Container to bytearray.
        2. This is one line data process.
        """
        if self.gv.ASIC_MODEL in ['T26']:
            LINE_LENGTH = 30720
        else:
            LINE_LENGTH = self.gv.LINE_LENGTH
        # bytearray transfer
        byteArr = bytearray(LINE_LENGTH)
        for col in range(0, LINE_LENGTH):
            # Global Data Container load
            data = int(self.dc.oParam[col])
            # bytearray save
            byteArr[col] = data
        return byteArr