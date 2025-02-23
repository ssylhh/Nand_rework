import sys
import os
import csv
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog
from PySide6.QtCore import QMetaObject, Qt

from socketPot import socketPot, globalMemory
from ui_form import Ui_MainWindow  # UI 파일을 사용 (미리 Qt Designer에서 생성해야 함)

#  pyside6-uic ui_form.ui -o ui_form.py


gv = globalMemory.GlobalVariableT24
dc = globalMemory.GlobalDataContainer

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # UI 요소 추가 (버튼 및 로그 창)
        # self.ui.read_1_button = QPushButton("Read NAND YB1", self)
        # self.ui.read_1_button.setGeometry(20, 20, 180, 30)
        self.ui.read_1_button.clicked.connect(self.read_nand_yb1)
        self.ui.read_2_button.clicked.connect(self.readNANDLParam)

        # self.ui.write_1_button = QPushButton("Write NAND YB1", self)
        # self.ui.write_nand_button.setGeometry(20, 60, 180, 30)
        self.ui.write_1_button.clicked.connect(self.write_nand_yb1)
        self.ui.write_2_button.clicked.connect(self.writeNANDLParam)

        # self.ui.erase_nand_button = QPushButton("Erase NAND YB1", self)
        # self.ui.erase_nand_button.setGeometry(20, 100, 180, 30)
        # self.ui.erase_nand_button.clicked.connect(self.erase_nand_yb1)

        # self.ui.save_csv_button = QPushButton("Save CSV", self)
        # self.ui.save_csv_button.setGeometry(20, 140, 180, 30)
        # self.ui.save_csv_button.clicked.connect(self.save_csv)

        self.ui.log_output = QTextEdit(self)
        self.ui.log_output.setGeometry(120, 350, 440, 130)
        # self.ui.log_output.setReadOnly(True)

        self.pot = socketPot.PotConnection()
        # self.pot.connect()

    def log_message(self, message):
        """ 로그 출력 함수 """
        self.ui.log_output.append(message)

    # def log_message(self, message):
    #     """ UI 안전하게 로그 출력 """
    #     QMetaObject.invokeMethod(
    #         self.ui.log_output, "append",
    #         Qt.QueuedConnection, message
    #     )

    def read_nand_yb1(self):

        # print("*******")
        
        try:
            self.log_message("Reading NAND YB1...")
            self.pot.writeTransferMono(cmd=gv.CMD_SET_PCMODE)
            self.pot.writeTransferMono(cmd=gv.CMD_YB_DDR_BRIDGE_RESET)
            self.pot.readTransferBurst(cmd=gv.CMD_RD_NAND_YB1, dataType='comp')
            self.pot.writeTransferMono(cmd=gv.CMD_CLR_PCMODE)
            self.log_message("NAND YB1 read completed.")
        except Exception as e:
            self.log_message(f"Error: {e}")

    def write_nand_yb1(self):

        try:
            self.log_message("Writing NAND YB1...")
            self.pot.writeTransferMono(cmd=gv.CMD_SET_PCMODE)
            self.pot.writeTransferMono(cmd=gv.CMD_ER_NAND_YB1)
            self.pot.writeTransferMono(cmd=gv.CMD_YB_DDR_BRIDGE_RESET)
            self.pot.writeTransferBurst(cmd=gv.CMD_WR_NAND_YB1, dataType='comp')
            self.pot.writeTransferMono(cmd=gv.CMD_CLR_PCMODE)
            self.log_message("NAND YB1 write completed.")
        except Exception as e:
            self.log_message(f"Error: {e}")

    def erase_nand_yb1(self):

        try:
            self.log_message("Erasing NAND YB1...")
            self.pot.writeTransferMono(cmd=gv.CMD_SET_PCMODE)
            self.pot.writeTransferMono(cmd=gv.CMD_ER_NAND_YB1)
            self.pot.writeTransferMono(cmd=gv.CMD_CLR_PCMODE)
            self.log_message("NAND YB1 erase completed.")
        except Exception as e:
            self.log_message(f"Error: {e}")

    def readNANDLParam(self):

        try:
            self.log_message("Reading L Parameter...")
            # self.pot.writeTransferMono(cmd=gv.CMD_SET_PCMODE)
            # self.pot.readTransferLine(cmd = gv.CMD_RD_NAND_LPARAM, lineNumber = 0, dataType = 'setting')
            # self.pot.writeTransferMono(cmd=gv.CMD_CLR_PCMODE)
            self.log_message("L Parameter reading completed.")                        
            self.save_dc_lut_as_ini(dc, "output/[L Parmeter] Rework.ini")                         
                          
        except Exception as e:
            self.log_message(f"Error: {e}")


    def writeNANDLParam(self):

        try:
            self.log_message("Writing L Parameter...")
            self.load_dc_lut_from_ini(dc, "output/[L Parmeter] Rework.ini")
            self.pot.writeTransferMono(cmd=gv.CMD_SET_PCMODE)
            self.pot.writeTransferMono(cmd=gv.CMD_ER_NAND_LPARAM)
            self.pot.writeTransferLine(cmd = gv.CMD_WR_NAND_LPARAM, lineNumber = 0, dataType = 'setting')
            self.pot.writeTransferMono(cmd=gv.CMD_CLR_PCMODE)
            self.log_message("Writing L parameter completed.")
        except Exception as e:
            self.log_message(f"Error: {e}")


    def save_dc_lut_as_ini(self, dc, file_path):  

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("[LUT_FIRST_ROW]\n")  

            first_row = dc.lut[0]  
            for index, value in enumerate(first_row):  
                f.write(f"{index}={format(int(value), 'X')}\n")  

# for multi Lut parameter as V parameter block
    def save_dc_Luts_as_ini(self, dc, file_path):  

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            for i, row in enumerate(dc.lut):  
                f.write(f"[LUT_{i}]\n")
                for index, value in enumerate(row):  
                    f.write(f"{index}={format(value, 'X')}\n")
                f.write("\n")  

        # with open(file_path, "w", encoding="utf-8") as f:
        #     for i, row in enumerate(dc.lineBuffer):  
        #         f.write(f"[lineBuffer_{i}]\n")
        #         for index, value in enumerate(row):  
        #             f.write(f"{index}={format(value, 'X')}\n")
        #         f.write("\n")  

    def load_dc_lut_from_ini(self, dc, file_path):
        
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



    def save_csv(self):

        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "output/data.csv", "CSV Files (*.csv)", options=options)
            if file_path:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    for row in dc.lut:
                        writer.writerow(row)
                self.log_message(f"Saved CSV: {file_path}")
            else:
                self.log_message("Save cancelled.")
        except Exception as e:
            self.log_message(f"Error: {e}")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())