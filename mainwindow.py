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

        # self.ui.write_1_button = QPushButton("Write NAND YB1", self)
        # self.ui.write_nand_button.setGeometry(20, 60, 180, 30)
        self.ui.write_1_button.clicked.connect(self.write_nand_yb1)

        # self.ui.erase_nand_button = QPushButton("Erase NAND YB1", self)
        # self.ui.erase_nand_button.setGeometry(20, 100, 180, 30)
        # self.ui.erase_nand_button.clicked.connect(self.erase_nand_yb1)

        # self.ui.save_csv_button = QPushButton("Save CSV", self)
        # self.ui.save_csv_button.setGeometry(20, 140, 180, 30)
        # self.ui.save_csv_button.clicked.connect(self.save_csv)

        self.ui.log_output = QTextEdit(self)
        self.ui.log_output.setGeometry(120, 350, 440, 130)
        # self.ui.log_output.setReadOnly(True)

        # self.pot = socketPot.PotConnection()
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
        """ NAND YB1 데이터 읽기 """
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
        """ NAND YB1 데이터 쓰기 """
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
        """ NAND YB1 데이터 삭제 """
        try:
            self.log_message("Erasing NAND YB1...")
            self.pot.writeTransferMono(cmd=gv.CMD_SET_PCMODE)
            self.pot.writeTransferMono(cmd=gv.CMD_ER_NAND_YB1)
            self.pot.writeTransferMono(cmd=gv.CMD_CLR_PCMODE)
            self.log_message("NAND YB1 erase completed.")
        except Exception as e:
            self.log_message(f"Error: {e}")

    def save_csv(self):
        """ 데이터 CSV로 저장 """
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