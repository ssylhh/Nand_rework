import os
import csv

from socketPot import socketPot, globalMemory

gv = globalMemory.GlobalVariableT24
# gv = globalMemory.GlobalVariableT26
dc = globalMemory.GlobalDataContainer

def readNANDYB1(pot):
    # PC MODE
    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    # Bridge Reset
    pot.writeTransferMono(cmd = gv.CMD_YB_DDR_BRIDGE_RESET)
    # POT command
    pot.readTransferBurst(cmd = gv.CMD_RD_NAND_YB1, dataType = 'comp')
    # PC MODE clear
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)


def writeNANDYB1(pot):
    # PC MODE
    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    # Erase
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_YB1)
    # Bridge Reset
    pot.writeTransferMono(cmd = gv.CMD_YB_DDR_BRIDGE_RESET)
    # POT command
    pot.writeTransferBurst(cmd = gv.CMD_WR_NAND_YB1, dataType = 'comp')
    # PC MODE clear
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)


def eraseNANDYB1(pot):
    # PC MODE
    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    # POT command
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_YB1)
    # PC MODE clear
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)


# *****************************************************************************

def readNANDOC1Flag(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)

    # if not gv.ASIC_MODEL in ['T26']:
    #     pot.readTransferBurst(cmd = gv.CMD_RD_NAND_OC1_FLAG, dataType = 'setting')
    # else:
    #     pot.readTransferLine(cmd = gv.CMD_RD_NAND_OC1_FLAG, lineNumber = 0, dataType = 'setting')

    pot.readTransferLine(cmd = gv.CMD_RD_NAND_OC1_FLAG, lineNumber = 0, dataType = 'setting')
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)

def writeNANDOC1Flag(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_OC1_FLAG)
    pot.writeTransferLine(cmd = gv.CMD_WR_NAND_OC1_FLAG, lineNumber = 0, dataType = 'setting')
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)

def eraseNANDLGDOC1Flag(pot):
    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_OC1_FLAG)
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE) 


def readNANDLParam(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.readTransferLine(cmd = gv.CMD_RD_NAND_LPARAM, lineNumber = 0, dataType = 'setting')
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)

def writeNANDLParam(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_LPARAM)
    pot.writeTransferLine(cmd = gv.CMD_WR_NAND_LPARAM, lineNumber = 0, dataType = 'setting')
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)

def eraseNANDLParam(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_LPARAM)
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE) 



def readNANDSParam(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.readTransferLine(cmd = gv.CMD_RD_NAND_S_PARAM, lineNumber = 0, dataType = 'setting')
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)

def writeNANDSParam(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_S_PARAM)
    pot.writeTransferLine(cmd = gv.CMD_WR_NAND_S_PARAM, lineNumber = 0, dataType = 'setting')
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)

def eraseNANDSParam(pot):

    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_S_PARAM)
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE) 



    # CMD_RD_NAND_S_PARAM = _getCmdBytes("0x6000")
    # CMD_WR_NAND_S_PARAM = _getCmdBytes("0x6020")
    # CMD_ER_NAND_S_PARAM = _getCmdBytes("0x6040")
    # CMD_RD_NAND_G_PARAM = _getCmdBytes("0x6900")
    # CMD_WR_NAND_G_PARAM = _getCmdBytes("0x6920")
    # CMD_ER_NAND_G_PARAM = _getCmdBytes("0x6940")




# ************************************************************************************


def readNANDLGDVparam(pot):
    # PC MODE
    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    # POT command
    if not gv.ASIC_MODEL in ['T26']:
        pot.readTransferBurst(cmd = gv.CMD_RD_NAND_LGD_VPARAM, dataType = 'setting')
    else:
        pot.readTransferLine(cmd = gv.CMD_RD_NAND_LGD_VPARAM, lineNumber = 0, dataType = 'setting')
    # PC MODE clear
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)


def writeNANDLGDVparam(pot):
    # PC MODE
    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    # POT command
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_LGD_VPARAM)
    # POT command
    if not gv.ASIC_MODEL in ['T26']:
        pot.writeTransferBurst(cmd = gv.CMD_WR_NAND_LGD_VPARAM, dataType = 'setting')
    else:
        pot.writeTransferLine(cmd = gv.CMD_WR_NAND_LGD_VPARAM, lineNumber = 0, dataType = 'setting')
    # PC MODE clear
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)


def eraseNANDLGDVparam(pot):
    # PC MODE
    pot.writeTransferMono(cmd = gv.CMD_SET_PCMODE)
    # POT command
    pot.writeTransferMono(cmd = gv.CMD_ER_NAND_LGD_VPARAM)
    # PC MODE clear
    pot.writeTransferMono(cmd = gv.CMD_CLR_PCMODE)

# *****************************************************************************


def save_dc_lut_as_ini(dc, file_path):  

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # with open(file_path, "w", encoding="utf-8") as f:
    #     for i, row in enumerate(dc.lut):  
    #         f.write(f"[LUT_{i}]\n")
    #         for index, value in enumerate(row):  
    #             f.write(f"{index}={format(value, 'X')}\n")
    #         f.write("\n")  


    with open(file_path, "w", encoding="utf-8") as f:
        f.write("[LUT_FIRST_ROW]\n")  

        first_row = dc.lut[0]  
        for index, value in enumerate(first_row):  
            f.write(f"{index}={format(int(value), 'X')}\n")  


    # with open(file_path, "w", encoding="utf-8") as f:
    #     for i, row in enumerate(dc.lineBuffer):  
    #         f.write(f"[lineBuffer_{i}]\n")
    #         for index, value in enumerate(row):  
    #             f.write(f"{index}={format(value, 'X')}\n")
    #         f.write("\n")  


def load_dc_lut_from_ini(dc, file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        first_row = []

        for line in f:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):  
                continue  
            if "=" in line:  
                _, value = line.split("=")  
                first_row.append(int(value, 16))  

    dc.lut[0] = first_row


def save_dc_lut_as_csv(dc, file_path, format):    

    os.makedirs(os.path.dirname(file_path), exist_ok=True)  

    if format == "csv":
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in dc.lut:
                writer.writerow(row)
    else:
        print("N.A. format")




# def write_dc_lut_as_ini(dc, file_path):

#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     with open(file_path, "w", encoding="utf-8") as f:
#         for i, row in enumerate(dc.lut):  
#             f.write(f"[LUT_{i}]\n")  
#             for value in row:  
#                 f.write(f"{format(value, 'X')}\n")  # index 없이 값만 저장
#             f.write("\n")  # 섹션 간 구분을 위해 개행 추가


# def save_dc_lut_as_bin(dc, file_path):

#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     with open(file_path, "wb") as f:  
#         for row in dc.lut:
#             byteArr = bytearray(row)  # 리스트를 bytearray로 변환
#             f.write(byteArr)  # 바이너리 데이터 저장

# *****************************************************************************

if __name__ == '__main__':
    pot = socketPot.PotConnection()
    pot.connect()
    # test1 : NAND YB1 read
    #readNANDYB1(pot)
    #print(f"dc.rPhiContainer[0][0]: {dc.rPhiContainer[0][0]}")
    #print(f"dc.rAlphaContainer[0][0]: {dc.rAlphaContainer[0][0]}")


# ****************************************************************************
    # test2 : NAND Vparam read
    # readNANDLGDVparam(pot)
    # readNANDOC1Flag(pot) 

    # # save_dc_lut_as_ini(dc, "output/[LGD_Vpara] rework.ini")
    # save_dc_lut_as_ini(dc, "output/[OC1_Flag] rework.ini")

    # load_dc_lut_from_ini(dc, "output/[OC1_Flag] rework.ini")
    # writeNANDOC1Flag(pot)

    readNANDLParam(pot) 
    save_dc_lut_as_ini(dc, "output/[L Parmeter] rework.ini")

    writeNANDLParam(pot)
    load_dc_lut_from_ini(dc, "output/[L Parmeter] rework.ini")

    # readNANDSParam(pot)
    # save_dc_lut_as_csv(dc, "output/[S Parmeter] rework.csv", format="csv")

    # print(f"dc.lut[0][0]: {dc.lut[0][0]}") # T24
    # print(f"dc.vParam[0]: {dc.vParam[0]}") # T26










# def save_lut_to_ini(self, file_path: str) -> None:

#     # config = configparser.ConfigParser()


#     # lut_data_str = ','.join(map(str, lut[:LINE_LENGTH]))

#     # config['LUT'] = {'order': str(order), 'data': lut_data_str}

#     # 파일 저장
#     with open(file_path, 'w') as configfile:
#         config.write(configfile)

#     print(f"LUT data saved to {file_path}")


# def save_lut_to_ini(self, file_path: str) -> None:

#     # if self.gv.ASIC_MODEL in ['T26']:
#     #     lut = self.dc.vParam
#     #     LINE_LENGTH = 30720
#     # else:
#     #     lut = self.dc.lut
#     #     LINE_LENGTH = self.gv.LINE_LENGTH

#     lut = self.dc.lut
#     LINE_LENGTH = self.gv.LINE_LENGTH


#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     with open(file_path, 'w') as file:
#         for index, row in enumerate(lut):
#             lut_data_str = ','.join(map(str, row[:LINE_LENGTH]))
#             file.write(f"[LUT_{index}]\n")
#             file.write(f"data = {lut_data_str}\n\n")

#     print(f"LUT data saved to {file_path}")



# def save_dc_lut_as_ini(dc, file_path):

#     os.makedirs(os.path.dirname(file_path), exist_ok=True) 

#     with open(file_path, "w", encoding="utf-8") as f:
#         # f.write("[V PARAMETER]\n")  

#         for i in enumerate(dc.lut): 
#             for index, value in enumerate(dc.lut[i]):  
#                 f.write(f"{index}={format(value, 'X')}\n")  

