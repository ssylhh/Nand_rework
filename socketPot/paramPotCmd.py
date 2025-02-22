# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:43:02 2020

@author: jaesung.an
"""
import logging
from typing import List

from socketPot import singleton, globalMemory

class ParamPotCmd(singleton.SingletonInstance):
    r"""
    Parameter POT Command class
    ===========================
    1. This is the subpackage class for checking POT packet format with the parameter value
    2. This is singleton

    Provides
    --------
    1. getWLIdx(self, cmd :bytes) -> int
    2. getRLIdx(self, cmd :bytes) -> int
    3. getTconVer(self) -> int
    4. checkAck(self, received :bytearray) -> None
    5. checkFooter(self, data :bytearray, footer :bytearray)
    6. calChksum(self, data :bytearray) -> int
    7. calSum(self, data :bytearray) -> int
    8. calChksum4byte(self, data :bytearray) -> List[int]
    9. calLparamChksum(self, data :bytearray) -> int
    """
    def __init__(self) -> None:
        self.gv = globalMemory.GlobalVariableT24


    def getWLIdx(self, cmd :bytes) -> int:
        r"""get write length index"""
        if \
        (cmd == self.gv.CMD_TCON_RESET) |\
        (cmd == self.gv.CMD_POWER_RESET) |\
        (cmd == self.gv.CMD_SET_EMERGENCY) |\
        (cmd == self.gv.CMD_CLR_EMERGENCY) |\
        (cmd == self.gv.CMD_SET_PCMODE) |\
        (cmd == self.gv.CMD_CLR_PCMODE) |\
        (cmd == self.gv.CMD_RD_TCON_VPARAM) |\
        (cmd == self.gv.CMD_RD_OPARAM) |\
        (cmd == self.gv.CMD_SEN_AVC) |\
        (cmd == self.gv.CMD_SEN_REF) |\
        (cmd == self.gv.CMD_SEN_SMODE_R) |\
        (cmd == self.gv.CMD_SEN_SMODE_W) |\
        (cmd == self.gv.CMD_SEN_SMODE_G) |\
        (cmd == self.gv.CMD_SEN_SMODE_B) |\
        (cmd == self.gv.CMD_SEN_SMODE_4C) |\
        (cmd == self.gv.CMD_SEN_FMODE_R) |\
        (cmd == self.gv.CMD_SEN_FMODE_W) |\
        (cmd == self.gv.CMD_SEN_FMODE_G) |\
        (cmd == self.gv.CMD_SEN_FMODE_B) |\
        (cmd == self.gv.CMD_SEN_FMODE_4C) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_R) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_W) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_G) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_B) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_4C) |\
        (cmd == self.gv.CMD_RD_NAND_S_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_S_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_G_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_G_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_SET_LPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_SET_LPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_LPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_LPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_SET_VPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_SET_VPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_VPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_VPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_RS1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_RS1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_RS2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_RS2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_BLC1) |\
        (cmd == self.gv.CMD_ER_NAND_BLC1) |\
        (cmd == self.gv.CMD_RD_NAND_BLC2) |\
        (cmd == self.gv.CMD_ER_NAND_BLC2) |\
        (cmd == self.gv.CMD_RD_NAND_YB_INFO1) |\
        (cmd == self.gv.CMD_ER_NAND_YB_INFO1) |\
        (cmd == self.gv.CMD_RD_NAND_YB_INFO2) |\
        (cmd == self.gv.CMD_ER_NAND_YB_INFO2) |\
        (cmd == self.gv.CMD_RD_NAND_CRP1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_CRP1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_CRP2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_CRP2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_CME_PHI1) |\
        (cmd == self.gv.CMD_ER_NAND_CME_PHI1) |\
        (cmd == self.gv.CMD_RD_NAND_CME_PHI2) |\
        (cmd == self.gv.CMD_ER_NAND_CME_PHI2) |\
        (cmd == self.gv.CMD_RD_NAND_CME_ALPHA1) |\
        (cmd == self.gv.CMD_ER_NAND_CME_ALPHA1) |\
        (cmd == self.gv.CMD_RD_NAND_CME_ALPHA2) |\
        (cmd == self.gv.CMD_ER_NAND_CME_ALPHA2) |\
        (cmd == self.gv.CMD_RD_NAND_CB) |\
        (cmd == self.gv.CMD_ER_NAND_CB) |\
        (cmd == self.gv.CMD_RD_NAND_ATCB) |\
        (cmd == self.gv.CMD_ER_NAND_ATCB) |\
        (cmd == self.gv.CMD_RD_NAND_APG) |\
        (cmd == self.gv.CMD_ER_NAND_APG) |\
        (cmd == self.gv.CMD_RD_NAND_GVC) |\
        (cmd == self.gv.CMD_ER_NAND_GVC) |\
        (cmd == self.gv.CMD_RD_NAND_IPA) |\
        (cmd == self.gv.CMD_ER_NAND_IPA) |\
        (cmd == self.gv.CMD_RD_NAND_IPA_PHI) |\
        (cmd == self.gv.CMD_ER_NAND_IPA_PHI) |\
        (cmd == self.gv.CMD_RD_NAND_YB1) |\
        (cmd == self.gv.CMD_ER_NAND_YB1) |\
        (cmd == self.gv.CMD_RD_NAND_YB2) |\
        (cmd == self.gv.CMD_ER_NAND_YB2) |\
        (cmd == self.gv.CMD_RD_NAND_PHI1) |\
        (cmd == self.gv.CMD_ER_NAND_PHI1) |\
        (cmd == self.gv.CMD_RD_NAND_PHI2) |\
        (cmd == self.gv.CMD_ER_NAND_PHI2) |\
        (cmd == self.gv.CMD_RD_NAND_YB_YCB1) |\
        (cmd == self.gv.CMD_ER_NAND_YB_YCB1) |\
        (cmd == self.gv.CMD_RD_NAND_YB_YCB2) |\
        (cmd == self.gv.CMD_ER_NAND_YB_YCB2) |\
        (cmd == self.gv.CMD_RD_NAND_PHI_YCB1) |\
        (cmd == self.gv.CMD_ER_NAND_PHI_YCB1) |\
        (cmd == self.gv.CMD_RD_NAND_PHI_YCB2) |\
        (cmd == self.gv.CMD_ER_NAND_PHI_YCB2) |\
        (cmd == self.gv.CMD_RD_NAND_ALPHA1) |\
        (cmd == self.gv.CMD_ER_NAND_ALPHA1) |\
        (cmd == self.gv.CMD_RD_NAND_ALPHA2) |\
        (cmd == self.gv.CMD_ER_NAND_ALPHA2) |\
        (cmd == self.gv.CMD_RD_NAND_IPA_ALPHA) |\
        (cmd == self.gv.CMD_ER_NAND_IPA_ALPHA) |\
        (cmd == self.gv.CMD_RD_NAND_YCB) |\
        (cmd == self.gv.CMD_ER_NAND_YCB) |\
        (cmd == self.gv.CMD_RD_NAND_RT_REF) |\
        (cmd == self.gv.CMD_ER_NAND_RT_REF) |\
        (cmd == self.gv.CMD_RD_NAND_SET_PDCS_LUT1) |\
        (cmd == self.gv.CMD_ER_NAND_SET_PDCS_LUT1) |\
        (cmd == self.gv.CMD_RD_NAND_SET_PDCS_LUT2) |\
        (cmd == self.gv.CMD_ER_NAND_SET_PDCS_LUT2) |\
        (cmd == self.gv.CMD_RD_NAND_TIMER1) |\
        (cmd == self.gv.CMD_ER_NAND_TIMER1) |\
        (cmd == self.gv.CMD_RD_NAND_TIMER2) |\
        (cmd == self.gv.CMD_ER_NAND_TIMER2) |\
        (cmd == self.gv.CMD_RD_NAND_TEMP1) |\
        (cmd == self.gv.CMD_ER_NAND_TEMP1) |\
        (cmd == self.gv.CMD_RD_NAND_TEMP2) |\
        (cmd == self.gv.CMD_ER_NAND_TEMP2) |\
        (cmd == self.gv.CMD_RD_NAND_OC1_1LINE) |\
        (cmd == self.gv.CMD_ER_NAND_OC1_1LINE) |\
        (cmd == self.gv.CMD_RD_NAND_OC1) |\
        (cmd == self.gv.CMD_ER_NAND_OC1) |\
        (cmd == self.gv.CMD_RD_NAND_OC2_1LINE) |\
        (cmd == self.gv.CMD_ER_NAND_OC2_1LINE) |\
        (cmd == self.gv.CMD_RD_NAND_OC2) |\
        (cmd == self.gv.CMD_ER_NAND_OC2) |\
        (cmd == self.gv.CMD_RD_NAND_OS1_MSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS1_MSB) |\
        (cmd == self.gv.CMD_RD_NAND_OS1_LSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS1_LSB) |\
        (cmd == self.gv.CMD_RD_NAND_OS2_MSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS2_MSB) |\
        (cmd == self.gv.CMD_RD_NAND_OS2_LSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS2_LSB) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TIMER1) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TIMER1) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TIMER2) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TIMER2) |\
        (cmd == self.gv.CMD_RD_NAND_TSLDD_Info) |\
        (cmd == self.gv.CMD_ER_NAND_TSLDD_Info) |\
        (cmd == self.gv.CMD_ER_NAND_OSLB_Info) |\
        (cmd == self.gv.CMD_RD_NAND_OSLB_Info) |\
        (cmd == self.gv.CMD_RD_NAND_OC1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OC1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_OC2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OC2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_OS1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OS1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_OS2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OS2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_SET_OSLB_LUT1) |\
        (cmd == self.gv.CMD_ER_NAND_SET_OSLB_LUT1) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_OSLB_LUT1) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_OSLB_LUT1) |\
        (cmd == self.gv.CMD_RD_NAND_SET_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_SET_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_SET_KMAP_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_SET_KMAP_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_KMAP_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_KMAP_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_ASC_VGAIN_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_ASC_VGAIN_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_SET_WCA_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_WCA_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_WCA_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_WCA_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_SET_GWC) |\
        (cmd == self.gv.CMD_ER_NAND_SET_GWC) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_GWC) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_GWC) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_SET_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_A2T_MAP1) |\
        (cmd == self.gv.CMD_ER_NAND_A2T_MAP1) |\
        (cmd == self.gv.CMD_RD_NAND_A2T_MAP2) |\
        (cmd == self.gv.CMD_ER_NAND_A2T_MAP2) |\
        (cmd == self.gv.CMD_RD_NAND_OSLB_PRNG_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_OSLB_PRNG_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_Y_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_Y_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_ASIC_SCOPE) |\
        (cmd == self.gv.CMD_ER_NAND_ASIC_SCOPE) |\
        (cmd == self.gv.CMD_RD_NAND_OSU_Info1) |\
        (cmd == self.gv.CMD_ER_NAND_OSU_Info1) |\
        (cmd == self.gv.CMD_RD_NAND_OSU_Info2) |\
        (cmd == self.gv.CMD_ER_NAND_OSU_Info2) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_CPS_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_CPS_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_EPM_LUT_IPA) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_EPM_LUT_IPA) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_EPM_LUT_RS1) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_EPM_LUT_RS1) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_EPM_LUT_RS2) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_EPM_LUT_RS2) |\
        (cmd == self.gv.CMD_RD_NAND_YB_LUTS) |\
        (cmd == self.gv.CMD_ER_NAND_YB_LUTS) |\
        (cmd == self.gv.CMD_RD_NAND_F_PARAM_0) |\
        (cmd == self.gv.CMD_ER_NAND_F_PARAM_0) |\
        (cmd == self.gv.CMD_RD_NAND_F_PARAM_1) |\
        (cmd == self.gv.CMD_ER_NAND_F_PARAM_1) |\
        (cmd == self.gv.CMD_RD_NAND_PBI) |\
        (cmd == self.gv.CMD_ER_NAND_PBI) |\
        (cmd == self.gv.CMD_RD_NAND_LTVSC_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_LTVSC_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_DBPC_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_DBPC_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_I_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_I_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_PDM) |\
        (cmd == self.gv.CMD_YB_DDR_BRIDGE_RESET) |\
        (cmd == self.gv.CMD_OSLB_DDR_BRIDGE_RESET) |\
        (cmd == self.gv.CMD_RD_DDR_RT1) |\
        (cmd == self.gv.CMD_RD_DDR_RT2) |\
        (cmd == self.gv.CMD_RD_DDR_ALPHA1) |\
        (cmd == self.gv.CMD_RD_DDR_ALPHA2) |\
        (cmd == self.gv.CMD_RD_DDR_PHI) |\
        (cmd == self.gv.CMD_RD_DDR_PHI) |\
        (cmd == self.gv.CMD_RD_DDR_RT_REF) |\
        (cmd == self.gv.CMD_RD_DDR_YB_BUFFER) |\
        (cmd == self.gv.CMD_RD_DDR_OC) |\
        (cmd == self.gv.CMD_RD_DDR_OS_MSB) |\
        (cmd == self.gv.CMD_RD_DDR_OS_LSB) |\
        (cmd == self.gv.CMD_RD_DDR_OC_BUFFER) |\
        (cmd == self.gv.CMD_RD_DDR_OS_BUFFER_MSB) |\
        (cmd == self.gv.CMD_RD_DDR_OS_BUFFER_LSB) |\
        (cmd == self.gv.CMD_ELVSS_RISE) |\
        (cmd == self.gv.CMD_ELVSS_DROP) |\
        (cmd == self.gv.CMD_PGVDD_EN_RISE) |\
        (cmd == self.gv.CMD_PGVDD_EN_DROP) |\
        (cmd == self.gv.CMD_PGVDD_SEL_RISE) |\
        (cmd == self.gv.CMD_PGVDD_SEL_DROP) |\
        (cmd == self.gv.CMD_OFF_RS_START) |\
        (cmd == self.gv.CMD_OCU_START) |\
        (cmd == self.gv.CMD_OSU_START) |\
        (cmd == self.gv.CMD_ORS_START) |\
        (cmd == self.gv.CMD_GDSD_RS) |\
        (cmd == self.gv.CMD_ADDLD_START) |\
        (cmd == self.gv.CMD_ADDLD_READ) |\
        (cmd == self.gv.CMD_BLACK_FRAME) |\
        (cmd == self.gv.CMD_RD_DTC) |\
        (cmd == self.gv.CMD_RD_ALPHA_DIFF_MAP) |\
        (cmd == self.gv.CMD_PHI_ALPHA_COPY) |\
        (cmd == self.gv.CMD_SCH_DONE_CHECK) |\
        (cmd == self.gv.CMD_PTG_R) |\
        (cmd == self.gv.CMD_PTG_W) |\
        (cmd == self.gv.CMD_PTG_G) |\
        (cmd == self.gv.CMD_PTG_B) |\
        (cmd == self.gv.CMD_PTG_OFF):
            return 0x0
        elif \
        (cmd == self.gv.CMD_WR_TCON_VPARAM) |\
        (cmd == self.gv.CMD_WR_OPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_S_PARAM) |\
        (cmd == self.gv.CMD_WR_NAND_G_PARAM) |\
        (cmd == self.gv.CMD_WR_NAND_SET_LPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_LPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_SET_VPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_VPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_RS1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_RS2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_BLC1) |\
        (cmd == self.gv.CMD_WR_NAND_BLC2) |\
        (cmd == self.gv.CMD_WR_NAND_YB_INFO1) |\
        (cmd == self.gv.CMD_WR_NAND_YB_INFO2) |\
        (cmd == self.gv.CMD_WR_NAND_CRP1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_CRP2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_CME_PHI1) |\
        (cmd == self.gv.CMD_WR_NAND_CME_PHI2) |\
        (cmd == self.gv.CMD_WR_NAND_CME_ALPHA1) |\
        (cmd == self.gv.CMD_WR_NAND_CME_ALPHA2) |\
        (cmd == self.gv.CMD_WR_NAND_CB) |\
        (cmd == self.gv.CMD_WR_NAND_ATCB) |\
        (cmd == self.gv.CMD_WR_NAND_APG) |\
        (cmd == self.gv.CMD_WR_NAND_GVC) |\
        (cmd == self.gv.CMD_WR_NAND_IPA) |\
        (cmd == self.gv.CMD_WR_NAND_IPA_PHI) |\
        (cmd == self.gv.CMD_WR_NAND_IPA_ALPHA) |\
        (cmd == self.gv.CMD_WR_NAND_YB1) |\
        (cmd == self.gv.CMD_WR_NAND_YB2) |\
        (cmd == self.gv.CMD_WR_NAND_YB_YCB1) |\
        (cmd == self.gv.CMD_WR_NAND_YB_YCB2) |\
        (cmd == self.gv.CMD_WR_NAND_PHI1) |\
        (cmd == self.gv.CMD_WR_NAND_PHI2) |\
        (cmd == self.gv.CMD_WR_NAND_PHI_YCB1) |\
        (cmd == self.gv.CMD_WR_NAND_PHI_YCB2) |\
        (cmd == self.gv.CMD_WR_NAND_ALPHA1) |\
        (cmd == self.gv.CMD_WR_NAND_ALPHA2) |\
        (cmd == self.gv.CMD_WR_NAND_YCB) |\
        (cmd == self.gv.CMD_WR_NAND_RT_REF) |\
        (cmd == self.gv.CMD_WR_NAND_SET_PDCS_LUT1) |\
        (cmd == self.gv.CMD_WR_NAND_SET_PDCS_LUT2) |\
        (cmd == self.gv.CMD_WR_NAND_TIMER1) |\
        (cmd == self.gv.CMD_WR_NAND_TIMER2) |\
        (cmd == self.gv.CMD_WR_NAND_TEMP1) |\
        (cmd == self.gv.CMD_WR_NAND_TEMP2) |\
        (cmd == self.gv.CMD_WR_NAND_OC1_1LINE) |\
        (cmd == self.gv.CMD_WR_NAND_OC1) |\
        (cmd == self.gv.CMD_WR_NAND_OC2_1LINE) |\
        (cmd == self.gv.CMD_WR_NAND_OC2) |\
        (cmd == self.gv.CMD_WR_NAND_OS1_MSB) |\
        (cmd == self.gv.CMD_WR_NAND_OS1_LSB) |\
        (cmd == self.gv.CMD_WR_NAND_OS2_MSB) |\
        (cmd == self.gv.CMD_WR_NAND_OS2_LSB) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TIMER1) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TIMER2) |\
        (cmd == self.gv.CMD_WR_NAND_TSLDD_Info) |\
        (cmd == self.gv.CMD_WR_NAND_OSLB_Info) |\
        (cmd == self.gv.CMD_WR_NAND_OC1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_OC2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_OS1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_OS2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_SET_OSLB_LUT1) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_OSLB_LUT1) |\
        (cmd == self.gv.CMD_WR_NAND_SET_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_SET_KMAP_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_KMAP_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_ASC_VGAIN_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_SET_WCA_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_WCA_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_SET_GWC) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_GWC) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_SET_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_A2T_MAP1) |\
        (cmd == self.gv.CMD_WR_NAND_A2T_MAP2) |\
        (cmd == self.gv.CMD_WR_NAND_OSLB_PRNG_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_Y_PARAM) |\
        (cmd == self.gv.CMD_WR_NAND_ASIC_SCOPE) |\
        (cmd == self.gv.CMD_WR_NAND_OSU_Info1) |\
        (cmd == self.gv.CMD_WR_NAND_OSU_Info2) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_CPS_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_EPM_LUT_IPA) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_EPM_LUT_RS1) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_EPM_LUT_RS2) |\
        (cmd == self.gv.CMD_WR_NAND_YB_LUTS) |\
        (cmd == self.gv.CMD_WR_NAND_F_PARAM_0) |\
        (cmd == self.gv.CMD_WR_NAND_F_PARAM_1) |\
        (cmd == self.gv.CMD_WR_NAND_PBI) |\
        (cmd == self.gv.CMD_WR_NAND_LTVSC_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_DBPC_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_I_PARAM) |\
        (cmd == self.gv.CMD_WR_DDR_RT1) |\
        (cmd == self.gv.CMD_WR_DDR_RT2) |\
        (cmd == self.gv.CMD_WR_DDR_ALPHA1) |\
        (cmd == self.gv.CMD_WR_DDR_ALPHA2) |\
        (cmd == self.gv.CMD_WR_DDR_PHI) |\
        (cmd == self.gv.CMD_WR_DDR_RT_REF) |\
        (cmd == self.gv.CMD_WR_DDR_YB_BUFFER) |\
        (cmd == self.gv.CMD_WR_DDR_RT1) |\
        (cmd == self.gv.CMD_WR_DDR_OC) |\
        (cmd == self.gv.CMD_WR_DDR_OS_MSB) |\
        (cmd == self.gv.CMD_WR_DDR_OS_LSB) |\
        (cmd == self.gv.CMD_WR_DDR_OC_BUFFER) |\
        (cmd == self.gv.CMD_WR_DDR_OS_BUFFER_MSB) |\
        (cmd == self.gv.CMD_WR_DDR_OS_BUFFER_LSB):
            if self.gv.ASIC_MODEL in ['T26']:
                if self.gv.RESOL in ['UHD+']:
                    return 0x2
                else:
                    return 0x1
            else:
                if self.gv.RESOL in ['QUHD']:
                    return 0x2
                else:
                    return 0x1
        else:
            raise Exception(f"POT 명령어를 찾을 수 없습니다.\n>> cmd : 0x{cmd.hex()}")


    def getRLIdx(self, cmd :bytes) -> int:
        r"""get read length index"""
        if \
        (cmd == self.gv.CMD_TCON_RESET) |\
        (cmd == self.gv.CMD_POWER_RESET) |\
        (cmd == self.gv.CMD_SET_EMERGENCY) |\
        (cmd == self.gv.CMD_CLR_EMERGENCY) |\
        (cmd == self.gv.CMD_SET_PCMODE) |\
        (cmd == self.gv.CMD_CLR_PCMODE) |\
        (cmd == self.gv.CMD_WR_TCON_VPARAM) |\
        (cmd == self.gv.CMD_WR_OPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_S_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_S_PARAM) |\
        (cmd == self.gv.CMD_WR_NAND_G_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_G_PARAM) |\
        (cmd == self.gv.CMD_WR_NAND_SET_LPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_SET_LPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_LPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_LPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_SET_VPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_SET_VPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_VPARAM) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_VPARAM) |\
        (cmd == self.gv.CMD_WR_NAND_RS1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_RS1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_RS2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_RS2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_BLC1) |\
        (cmd == self.gv.CMD_ER_NAND_BLC1) |\
        (cmd == self.gv.CMD_WR_NAND_BLC2) |\
        (cmd == self.gv.CMD_ER_NAND_BLC2) |\
        (cmd == self.gv.CMD_WR_NAND_YB_INFO1) |\
        (cmd == self.gv.CMD_ER_NAND_YB_INFO1) |\
        (cmd == self.gv.CMD_WR_NAND_YB_INFO2) |\
        (cmd == self.gv.CMD_ER_NAND_YB_INFO2) |\
        (cmd == self.gv.CMD_WR_NAND_CRP1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_CRP1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_CRP2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_CRP2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_CME_PHI1) |\
        (cmd == self.gv.CMD_ER_NAND_CME_PHI1) |\
        (cmd == self.gv.CMD_WR_NAND_CME_PHI2) |\
        (cmd == self.gv.CMD_ER_NAND_CME_PHI2) |\
        (cmd == self.gv.CMD_WR_NAND_CME_ALPHA1) |\
        (cmd == self.gv.CMD_ER_NAND_CME_ALPHA1) |\
        (cmd == self.gv.CMD_WR_NAND_CME_ALPHA2) |\
        (cmd == self.gv.CMD_ER_NAND_CME_ALPHA2) |\
        (cmd == self.gv.CMD_WR_NAND_CB) |\
        (cmd == self.gv.CMD_ER_NAND_CB) |\
        (cmd == self.gv.CMD_WR_NAND_ATCB) |\
        (cmd == self.gv.CMD_ER_NAND_ATCB) |\
        (cmd == self.gv.CMD_WR_NAND_APG) |\
        (cmd == self.gv.CMD_ER_NAND_APG) |\
        (cmd == self.gv.CMD_WR_NAND_GVC) |\
        (cmd == self.gv.CMD_ER_NAND_GVC) |\
        (cmd == self.gv.CMD_WR_NAND_IPA) |\
        (cmd == self.gv.CMD_ER_NAND_IPA) |\
        (cmd == self.gv.CMD_WR_NAND_IPA_PHI) |\
        (cmd == self.gv.CMD_ER_NAND_IPA_PHI) |\
        (cmd == self.gv.CMD_WR_NAND_IPA_ALPHA) |\
        (cmd == self.gv.CMD_ER_NAND_IPA_ALPHA) |\
        (cmd == self.gv.CMD_WR_NAND_YB1) |\
        (cmd == self.gv.CMD_ER_NAND_YB1) |\
        (cmd == self.gv.CMD_WR_NAND_YB2) |\
        (cmd == self.gv.CMD_ER_NAND_YB2) |\
        (cmd == self.gv.CMD_WR_NAND_PHI1) |\
        (cmd == self.gv.CMD_ER_NAND_PHI1) |\
        (cmd == self.gv.CMD_WR_NAND_PHI2) |\
        (cmd == self.gv.CMD_ER_NAND_PHI2) |\
        (cmd == self.gv.CMD_WR_NAND_YB_YCB1) |\
        (cmd == self.gv.CMD_ER_NAND_YB_YCB1) |\
        (cmd == self.gv.CMD_WR_NAND_YB_YCB2) |\
        (cmd == self.gv.CMD_ER_NAND_YB_YCB2) |\
        (cmd == self.gv.CMD_WR_NAND_PHI_YCB1) |\
        (cmd == self.gv.CMD_ER_NAND_PHI_YCB1) |\
        (cmd == self.gv.CMD_WR_NAND_PHI_YCB2) |\
        (cmd == self.gv.CMD_ER_NAND_PHI_YCB2) |\
        (cmd == self.gv.CMD_WR_NAND_ALPHA1) |\
        (cmd == self.gv.CMD_ER_NAND_ALPHA1) |\
        (cmd == self.gv.CMD_WR_NAND_ALPHA2) |\
        (cmd == self.gv.CMD_ER_NAND_ALPHA2) |\
        (cmd == self.gv.CMD_WR_NAND_YCB) |\
        (cmd == self.gv.CMD_ER_NAND_YCB) |\
        (cmd == self.gv.CMD_WR_NAND_RT_REF) |\
        (cmd == self.gv.CMD_ER_NAND_RT_REF) |\
        (cmd == self.gv.CMD_WR_NAND_SET_PDCS_LUT1) |\
        (cmd == self.gv.CMD_ER_NAND_SET_PDCS_LUT1) |\
        (cmd == self.gv.CMD_WR_NAND_SET_PDCS_LUT2) |\
        (cmd == self.gv.CMD_ER_NAND_SET_PDCS_LUT2) |\
        (cmd == self.gv.CMD_WR_NAND_TIMER1) |\
        (cmd == self.gv.CMD_ER_NAND_TIMER1) |\
        (cmd == self.gv.CMD_WR_NAND_TIMER2) |\
        (cmd == self.gv.CMD_ER_NAND_TIMER2) |\
        (cmd == self.gv.CMD_WR_NAND_TEMP1) |\
        (cmd == self.gv.CMD_ER_NAND_TEMP1) |\
        (cmd == self.gv.CMD_WR_NAND_TEMP2) |\
        (cmd == self.gv.CMD_ER_NAND_TEMP2) |\
        (cmd == self.gv.CMD_WR_NAND_OC1_1LINE) |\
        (cmd == self.gv.CMD_ER_NAND_OC1_1LINE) |\
        (cmd == self.gv.CMD_WR_NAND_OC1) |\
        (cmd == self.gv.CMD_ER_NAND_OC1) |\
        (cmd == self.gv.CMD_WR_NAND_OC2_1LINE) |\
        (cmd == self.gv.CMD_ER_NAND_OC2_1LINE) |\
        (cmd == self.gv.CMD_WR_NAND_OC2) |\
        (cmd == self.gv.CMD_ER_NAND_OC2) |\
        (cmd == self.gv.CMD_WR_NAND_OS1_MSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS1_MSB) |\
        (cmd == self.gv.CMD_WR_NAND_OS1_LSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS1_LSB) |\
        (cmd == self.gv.CMD_WR_NAND_OS2_MSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS2_MSB) |\
        (cmd == self.gv.CMD_WR_NAND_OS2_LSB) |\
        (cmd == self.gv.CMD_ER_NAND_OS2_LSB) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TIMER1) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TIMER1) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TIMER2) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TIMER2) |\
        (cmd == self.gv.CMD_WR_NAND_TSLDD_Info) |\
        (cmd == self.gv.CMD_ER_NAND_TSLDD_Info) |\
        (cmd == self.gv.CMD_WR_NAND_OSLB_Info) |\
        (cmd == self.gv.CMD_ER_NAND_OSLB_Info) |\
        (cmd == self.gv.CMD_WR_NAND_OC1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OC1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_OC2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OC2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_OS1_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OS1_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_OS2_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_OS2_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_SET_OSLB_LUT1) |\
        (cmd == self.gv.CMD_ER_NAND_SET_OSLB_LUT1) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_OSLB_LUT1) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_OSLB_LUT1) |\
        (cmd == self.gv.CMD_WR_NAND_SET_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_SET_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_SET_KMAP_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_SET_KMAP_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_KMAP_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_KMAP_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_ASC_VGAIN_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_ASC_VGAIN_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_SET_WCA_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_WCA_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_WCA_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_WCA_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_SET_GWC) |\
        (cmd == self.gv.CMD_ER_NAND_SET_GWC) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_GWC) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_GWC) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_SET_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_SET_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_SET_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_LGD_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_ER_NAND_LGD_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_WR_NAND_A2T_MAP1) |\
        (cmd == self.gv.CMD_ER_NAND_A2T_MAP1) |\
        (cmd == self.gv.CMD_WR_NAND_A2T_MAP2) |\
        (cmd == self.gv.CMD_ER_NAND_A2T_MAP2) |\
        (cmd == self.gv.CMD_WR_NAND_OSLB_PRNG_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_OSLB_PRNG_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_Y_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_Y_PARAM) |\
        (cmd == self.gv.CMD_WR_NAND_ASIC_SCOPE) |\
        (cmd == self.gv.CMD_ER_NAND_ASIC_SCOPE) |\
        (cmd == self.gv.CMD_WR_NAND_OSU_Info1) |\
        (cmd == self.gv.CMD_ER_NAND_OSU_Info1) |\
        (cmd == self.gv.CMD_WR_NAND_OSU_Info2) |\
        (cmd == self.gv.CMD_ER_NAND_OSU_Info2) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_CPS_LUT) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_CPS_LUT) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_EPM_LUT_IPA) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_EPM_LUT_IPA) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_EPM_LUT_RS1) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_EPM_LUT_RS1) |\
        (cmd == self.gv.CMD_WR_NAND_PYB_EPM_LUT_RS2) |\
        (cmd == self.gv.CMD_ER_NAND_PYB_EPM_LUT_RS2) |\
        (cmd == self.gv.CMD_WR_NAND_YB_LUTS) |\
        (cmd == self.gv.CMD_ER_NAND_YB_LUTS) |\
        (cmd == self.gv.CMD_WR_NAND_F_PARAM_0) |\
        (cmd == self.gv.CMD_ER_NAND_F_PARAM_0) |\
        (cmd == self.gv.CMD_WR_NAND_F_PARAM_1) |\
        (cmd == self.gv.CMD_ER_NAND_F_PARAM_1) |\
        (cmd == self.gv.CMD_WR_NAND_PBI) |\
        (cmd == self.gv.CMD_ER_NAND_PBI) |\
        (cmd == self.gv.CMD_WR_NAND_LTVSC_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_LTVSC_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_DBPC_FLAG) |\
        (cmd == self.gv.CMD_ER_NAND_DBPC_FLAG) |\
        (cmd == self.gv.CMD_WR_NAND_I_PARAM) |\
        (cmd == self.gv.CMD_ER_NAND_I_PARAM) |\
        (cmd == self.gv.CMD_YB_DDR_BRIDGE_RESET) |\
        (cmd == self.gv.CMD_OSLB_DDR_BRIDGE_RESET) |\
        (cmd == self.gv.CMD_WR_DDR_RT1) |\
        (cmd == self.gv.CMD_WR_DDR_RT2) |\
        (cmd == self.gv.CMD_WR_DDR_ALPHA1) |\
        (cmd == self.gv.CMD_WR_DDR_ALPHA2) |\
        (cmd == self.gv.CMD_WR_DDR_PHI) |\
        (cmd == self.gv.CMD_WR_DDR_RT_REF) |\
        (cmd == self.gv.CMD_WR_DDR_YB_BUFFER) |\
        (cmd == self.gv.CMD_WR_DDR_OC) |\
        (cmd == self.gv.CMD_WR_DDR_OS_MSB) |\
        (cmd == self.gv.CMD_WR_DDR_OS_LSB) |\
        (cmd == self.gv.CMD_WR_DDR_OC_BUFFER) |\
        (cmd == self.gv.CMD_WR_DDR_OS_BUFFER_MSB) |\
        (cmd == self.gv.CMD_WR_DDR_OS_BUFFER_LSB) |\
        (cmd == self.gv.CMD_ELVSS_RISE) |\
        (cmd == self.gv.CMD_ELVSS_DROP) |\
        (cmd == self.gv.CMD_PGVDD_EN_RISE) |\
        (cmd == self.gv.CMD_PGVDD_EN_DROP) |\
        (cmd == self.gv.CMD_PGVDD_SEL_RISE) |\
        (cmd == self.gv.CMD_PGVDD_SEL_DROP) |\
        (cmd == self.gv.CMD_OFF_RS_START) |\
        (cmd == self.gv.CMD_OCU_START) |\
        (cmd == self.gv.CMD_OSU_START) |\
        (cmd == self.gv.CMD_ORS_START) |\
        (cmd == self.gv.CMD_GDSD_RS) |\
        (cmd == self.gv.CMD_ADDLD_START) |\
        (cmd == self.gv.CMD_BLACK_FRAME) |\
        (cmd == self.gv.CMD_RD_ALPHA_DIFF_MAP) |\
        (cmd == self.gv.CMD_RD_DTC) |\
        (cmd == self.gv.CMD_PHI_ALPHA_COPY) |\
        (cmd == self.gv.CMD_SCH_DONE_CHECK) |\
        (cmd == self.gv.CMD_PTG_R) |\
        (cmd == self.gv.CMD_PTG_W) |\
        (cmd == self.gv.CMD_PTG_G) |\
        (cmd == self.gv.CMD_PTG_B) |\
        (cmd == self.gv.CMD_PTG_OFF):
            return 0x0
        elif \
        (cmd == self.gv.CMD_RD_TCON_VPARAM) |\
        (cmd == self.gv.CMD_WR_OPARAM) |\
        (cmd == self.gv.CMD_SEN_AVC) |\
        (cmd == self.gv.CMD_SEN_REF) |\
        (cmd == self.gv.CMD_SEN_SMODE_R) |\
        (cmd == self.gv.CMD_SEN_SMODE_W) |\
        (cmd == self.gv.CMD_SEN_SMODE_G) |\
        (cmd == self.gv.CMD_SEN_SMODE_B) |\
        (cmd == self.gv.CMD_SEN_SMODE_4C) |\
        (cmd == self.gv.CMD_SEN_FMODE_R) |\
        (cmd == self.gv.CMD_SEN_FMODE_W) |\
        (cmd == self.gv.CMD_SEN_FMODE_G) |\
        (cmd == self.gv.CMD_SEN_FMODE_B) |\
        (cmd == self.gv.CMD_SEN_FMODE_4C) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_R) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_W) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_G) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_B) |\
        (cmd == self.gv.CMD_SEN_OFFRF_MODE_4C) |\
        (cmd == self.gv.CMD_RD_NAND_S_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_G_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_SET_LPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_LPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_SET_VPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_VPARAM) |\
        (cmd == self.gv.CMD_RD_NAND_RS1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_RS2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_BLC1) |\
        (cmd == self.gv.CMD_RD_NAND_BLC2) |\
        (cmd == self.gv.CMD_RD_NAND_YB_INFO1) |\
        (cmd == self.gv.CMD_RD_NAND_YB_INFO2) |\
        (cmd == self.gv.CMD_RD_NAND_CRP1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_CRP2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_CME_PHI1) |\
        (cmd == self.gv.CMD_RD_NAND_CME_PHI2) |\
        (cmd == self.gv.CMD_RD_NAND_CME_ALPHA1) |\
        (cmd == self.gv.CMD_RD_NAND_CME_ALPHA2) |\
        (cmd == self.gv.CMD_RD_NAND_CB) |\
        (cmd == self.gv.CMD_RD_NAND_ATCB) |\
        (cmd == self.gv.CMD_RD_NAND_APG) |\
        (cmd == self.gv.CMD_RD_NAND_GVC) |\
        (cmd == self.gv.CMD_RD_NAND_IPA) |\
        (cmd == self.gv.CMD_RD_NAND_IPA_PHI) |\
        (cmd == self.gv.CMD_RD_NAND_IPA_ALPHA) |\
        (cmd == self.gv.CMD_RD_NAND_YB1) |\
        (cmd == self.gv.CMD_RD_NAND_YB2) |\
        (cmd == self.gv.CMD_RD_NAND_YB_YCB1) |\
        (cmd == self.gv.CMD_RD_NAND_YB_YCB2) |\
        (cmd == self.gv.CMD_RD_NAND_PHI1) |\
        (cmd == self.gv.CMD_RD_NAND_PHI2) |\
        (cmd == self.gv.CMD_RD_NAND_PHI_YCB1) |\
        (cmd == self.gv.CMD_RD_NAND_PHI_YCB2) |\
        (cmd == self.gv.CMD_RD_NAND_ALPHA1) |\
        (cmd == self.gv.CMD_RD_NAND_ALPHA2) |\
        (cmd == self.gv.CMD_RD_NAND_YCB) |\
        (cmd == self.gv.CMD_RD_NAND_RT_REF) |\
        (cmd == self.gv.CMD_RD_NAND_SET_PDCS_LUT1) |\
        (cmd == self.gv.CMD_RD_NAND_SET_PDCS_LUT2) |\
        (cmd == self.gv.CMD_RD_NAND_TIMER1) |\
        (cmd == self.gv.CMD_RD_NAND_TIMER2) |\
        (cmd == self.gv.CMD_RD_NAND_TEMP1) |\
        (cmd == self.gv.CMD_RD_NAND_TEMP2) |\
        (cmd == self.gv.CMD_RD_NAND_OC1_1LINE) |\
        (cmd == self.gv.CMD_RD_NAND_OC1) |\
        (cmd == self.gv.CMD_RD_NAND_OC2_1LINE) |\
        (cmd == self.gv.CMD_RD_NAND_OC2) |\
        (cmd == self.gv.CMD_RD_NAND_OS1_MSB) |\
        (cmd == self.gv.CMD_RD_NAND_OS1_LSB) |\
        (cmd == self.gv.CMD_RD_NAND_OS2_MSB) |\
        (cmd == self.gv.CMD_RD_NAND_OS2_LSB) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TIMER1) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TIMER2) |\
        (cmd == self.gv.CMD_RD_NAND_TSLDD_Info) |\
        (cmd == self.gv.CMD_RD_NAND_OSLB_Info) |\
        (cmd == self.gv.CMD_RD_NAND_OC1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_OC2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_OS1_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_OS2_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_SET_OSLB_LUT1) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_OSLB_LUT1) |\
        (cmd == self.gv.CMD_RD_NAND_SET_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_OSLB_Target_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_SET_KMAP_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_KMAP_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_ASC_VGAIN_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_SET_WCA_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_WCA_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_SET_GWC) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_GWC) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_TEMP_Gain_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_SET_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_TEMP_Offset_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_SET_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_LGD_Remain_TEMP_MAP) |\
        (cmd == self.gv.CMD_RD_NAND_A2T_MAP1) |\
        (cmd == self.gv.CMD_RD_NAND_A2T_MAP2) |\
        (cmd == self.gv.CMD_RD_NAND_OSLB_PRNG_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_Y_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_ASIC_SCOPE) |\
        (cmd == self.gv.CMD_RD_NAND_OSU_Info1) |\
        (cmd == self.gv.CMD_RD_NAND_OSU_Info2) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_CPS_LUT) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_EPM_LUT_IPA) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_EPM_LUT_RS1) |\
        (cmd == self.gv.CMD_RD_NAND_PYB_EPM_LUT_RS2) |\
        (cmd == self.gv.CMD_RD_NAND_YB_LUTS) |\
        (cmd == self.gv.CMD_RD_NAND_F_PARAM_0) |\
        (cmd == self.gv.CMD_RD_NAND_F_PARAM_1) |\
        (cmd == self.gv.CMD_RD_NAND_PBI) |\
        (cmd == self.gv.CMD_RD_NAND_LTVSC_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_DBPC_FLAG) |\
        (cmd == self.gv.CMD_RD_NAND_I_PARAM) |\
        (cmd == self.gv.CMD_RD_NAND_PDM) |\
        (cmd == self.gv.CMD_RD_DDR_RT1) |\
        (cmd == self.gv.CMD_RD_DDR_RT2) |\
        (cmd == self.gv.CMD_RD_DDR_ALPHA1) |\
        (cmd == self.gv.CMD_RD_DDR_ALPHA2) |\
        (cmd == self.gv.CMD_RD_DDR_PHI) |\
        (cmd == self.gv.CMD_RD_DDR_RT_REF) |\
        (cmd == self.gv.CMD_RD_DDR_YB_BUFFER) |\
        (cmd == self.gv.CMD_RD_DDR_OC) |\
        (cmd == self.gv.CMD_RD_DDR_OS_MSB) |\
        (cmd == self.gv.CMD_RD_DDR_OS_LSB) |\
        (cmd == self.gv.CMD_RD_DDR_OC_BUFFER) |\
        (cmd == self.gv.CMD_RD_DDR_OS_BUFFER_MSB) |\
        (cmd == self.gv.CMD_RD_DDR_OS_BUFFER_LSB) |\
        (cmd == self.gv.CMD_ADDLD_READ):
            if self.gv.ASIC_MODEL in ['T26']:
                if self.gv.RESOL in ['UHD+']:
                    return 0x2
                else:
                    return 0x1
            else:
                if self.gv.RESOL in ['QUHD']:
                    return 0x2
                else:
                    return 0x1
        else:
            raise Exception(f"POT 명령어를 찾을 수 없습니다.\n>> cmd : 0x{cmd.hex()}")


    def getTconVer(self) -> int:
        r"""get T-Con Version"""
        return 0x0


    def checkAck(self, received :bytearray) -> None:
        r"""check ACK packet and if it is abnormal, raise exception"""
        if received[0] != self.gv.ACK_FLAG:
            if received[0] == 0 and received[1] == 255:
                raise Exception(f"checkAck >> ACK packet is received : POT board timeout fail\n>> received : 0x{received.hex()}")
            else:
                raise Exception(f"checkAck >> ACK packet flag bit is corrupted.\n>> received : 0x{received.hex()}")
        elif received[1] == self.gv.ACK_SUCCESS:
            if(self.gv.POT_LOG_PRINT): logging.info(f"checkAck >> ACK packet is received : Success\n>> received : 0x{received.hex()}")
        elif received[1] == self.gv.ACK_TIMEOUT_TCON:
            raise Exception(f"checkAck >> ACK packet is received : T-Con timeout fail\n>> received : 0x{received.hex()}")
        elif received[1] == self.gv.ACK_CHECKSUM_ERROR1:
            raise Exception(f"checkAck >> ACK packet is received : Checksum fail (POT <<>> T-Con)\n>> received : 0x{received.hex()}")
        elif received[1] == self.gv.ACK_CHECKSUM_ERROR2:
            raise Exception(f"checkAck >> ACK packet is received : NAND error (T-Con <<>> NAND)\n>> received : 0x{received.hex()}")


    def checkFooter(self, data :bytearray, footer :bytearray):
        r"""check footer packet and if it is abnormal, raise exception"""
        if footer[0] == self.gv.FOOTER_SUCCESS:
            if(self.gv.POT_LOG_PRINT): logging.info(f"checkFooter >> Footer packet is received : Success\n>> footer : 0x{footer.hex()}")
        elif footer[0] == self.gv.FOOTER_CHECKSUM_ERROR2:
            raise Exception(f"checkFooter >> Footer packet is received : Checksum fail (T-Con <<>> NAND)\n>> footer : 0x{footer.hex()}")
        elif footer[0] == self.gv.FOOTER_SENSING_FAIL:
            raise Exception(f"checkFooter >> Footer packet is received : Sensing fail\n>> footer : 0x{footer.hex()}")
        chksum = self.calSum(data)
        if chksum == footer[1]: # checksum bit 확인
            pass
        else:
            raise Exception(f"checkFooter >> Footer packet is received : Checksum fail (PC <<>> POT)\n>> PC calculated checksum : {hex(chksum)}\n>> Received checksum : 0x{footer.hex()}")


    def calChksum(self, data :bytearray) -> int:
        r"""calculate 1byte checksum of bytearray (complement of sum)"""
        bytesum = sum(data)&0xFF
        chksum = 255-bytesum
        if(self.gv.POT_LOG_PRINT): logging.info(f"calChksum >> 1byte checksum calculation result : {chksum}")
        return chksum


    def calSum(self, data :bytearray) -> int:
        r"""calculate 1byte checksum of bytearray (only sum)"""
        bytesum = sum(data)&0xFF
        if(self.gv.POT_LOG_PRINT): logging.info(f"calSum >> 1byte bytesum calculation result : {bytesum}")
        return bytesum


    def calChksum4byte(self, data :bytearray) -> List[int]:
        r"""calculate 4byte checksum of bytearray (complement of sum)"""
        sum = 0
        if self.gv.ASIC_MODEL in ['N22']:
            LINE_LENGTH = int(self.gv.LINE_LENGTH/2)
        elif self.gv.ASIC_MODEL in ['T26']:
            LINE_LENGTH = 30720
        else:
            LINE_LENGTH = self.gv.LINE_LENGTH
        for i in range(int(LINE_LENGTH/4)-1):
            sum += (data[4*i+3]<<24) + (data[4*i+2]<<16) + (data[4*i+1]<<8) + data[4*i]
        chksum = 0xFFFFFFFF - sum&0xFFFFFFFF
        arrChksum = [chksum&0xFF, (chksum>>8)&0xFF, (chksum>>16)&0xFF, (chksum>>24)&0xFF]
        if(self.gv.POT_LOG_PRINT): logging.info(f"calChksum4byte >> 4byte checksum calculation result : {arrChksum}")
        return arrChksum


    def calLparamChksum(self, data :bytearray) -> int:
        r"""calculate 1byte checksum of bytearray (2's complement of sum)"""
        bytesum = sum(data)&0xFF
        chksum = 255-bytesum+1
        if chksum == 256:
            chksum = 0
        if(self.gv.POT_LOG_PRINT): logging.info(f"calLparamChksum >> 1byte checksum calculation result : {chksum}")
        return chksum