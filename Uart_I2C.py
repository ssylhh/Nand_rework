import sys
import serial
import serial.tools.list_ports
import threading
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QComboBox
from pyftdi.i2c import I2cController  

class USBCommApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB to UART & I2C 통신")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # UART 설정 UI
        self.uart_label = QLabel("UART COM 포트 선택:")
        layout.addWidget(self.uart_label)

        self.uart_selector = QComboBox()
        self.update_ports()
        layout.addWidget(self.uart_selector)

        self.uart_send_input = QLineEdit()
        self.uart_send_input.setPlaceholderText("UART 전송 데이터 입력...")
        layout.addWidget(self.uart_send_input)

        self.uart_send_button = QPushButton("UART 전송")
        self.uart_send_button.clicked.connect(self.send_uart_data)
        layout.addWidget(self.uart_send_button)

        self.uart_receive_label = QLabel("UART 수신 데이터:")
        layout.addWidget(self.uart_receive_label)

        self.uart_receive_text = QTextEdit()
        self.uart_receive_text.setReadOnly(True)
        layout.addWidget(self.uart_receive_text)

        # I2C 설정 UI
        self.i2c_label = QLabel("I2C 장치 주소 (16진수):")
        layout.addWidget(self.i2c_label)

        self.i2c_address_input = QLineEdit()
        self.i2c_address_input.setPlaceholderText("예: 0x50")
        layout.addWidget(self.i2c_address_input)

        self.i2c_send_input = QLineEdit()
        self.i2c_send_input.setPlaceholderText("I2C 전송 데이터 입력...")
        layout.addWidget(self.i2c_send_input)

        self.i2c_send_button = QPushButton("I2C 전송")
        self.i2c_send_button.clicked.connect(self.send_i2c_data)
        layout.addWidget(self.i2c_send_button)

        self.i2c_receive_button = QPushButton("I2C 읽기")
        self.i2c_receive_button.clicked.connect(self.read_i2c_data)
        layout.addWidget(self.i2c_receive_button)

        self.i2c_receive_label = QLabel("I2C 수신 데이터:")
        layout.addWidget(self.i2c_receive_label)

        self.i2c_receive_text = QTextEdit()
        self.i2c_receive_text.setReadOnly(True)
        layout.addWidget(self.i2c_receive_text)

        self.setLayout(layout)

        # 통신 초기화
        self.uart_port = None
        self.i2c = None
        self.running = False
        self.init_uart()
        self.init_i2c()

    def update_ports(self):
        """사용 가능한 COM 포트 목록 갱신"""
        ports = serial.tools.list_ports.comports()
        self.uart_selector.clear()
        for port in ports:
            self.uart_selector.addItem(port.device)

    def init_uart(self):
        """UART 초기화 및 스레드 시작"""
        selected_port = "COM8"  # UART 포트 (고정)
        try:
            self.uart_port = serial.Serial(selected_port, 115200, timeout=1)
            print(f"UART 연결 성공: {selected_port}")
            self.running = True
            threading.Thread(target=self.receive_uart_data, daemon=True).start()
        except serial.SerialException as e:
            print(f"UART 연결 실패: {e}")

    def init_i2c(self):
        """I2C 초기화 (FTDI 기반)"""
        try:
            self.i2c = I2cController()
            self.i2c.configure("ftdi://ftdi:2232h/1")  # FT232H I2C 포트
            print("I2C 초기화 성공")
        except Exception as e:
            print(f"I2C 초기화 실패: {e}")

    def send_uart_data(self):
        """UART 데이터 송신"""
        if self.uart_port and self.uart_port.is_open:
            data = self.uart_send_input.text()
            if data:
                self.uart_port.write(data.encode())
                print(f"UART 송신: {data}")
        else:
            print("UART 포트가 열려있지 않습니다.")

    def receive_uart_data(self):
        """UART 데이터 수신"""
        while self.running:
            if self.uart_port and self.uart_port.is_open:
                try:
                    data = self.uart_port.readline().decode(errors="ignore").strip()
                    if data:
                        print(f"UART 수신: {data}")
                        self.uart_receive_text.append(data)
                except serial.SerialException as e:
                    print(f"UART 수신 오류: {e}")
            time.sleep(0.1)

    def send_i2c_data(self):
        """I2C 데이터 송신"""
        if not self.i2c:
            print("I2C 초기화가 되지 않았습니다.")
            return
        
        address_text = self.i2c_address_input.text()
        if not address_text.startswith("0x"):
            print("올바른 I2C 주소를 입력하세요. (예: 0x50)")
            return
        
        try:
            address = int(address_text, 16)
            data = self.i2c_send_input.text().encode()
            slave = self.i2c.get_port(address)
            slave.write(data)
            print(f"I2C 송신 (주소 {hex(address)}): {data}")
        except Exception as e:
            print(f"I2C 송신 오류: {e}")

    def read_i2c_data(self):
        """I2C 데이터 읽기"""
        if not self.i2c:
            print("I2C 초기화가 되지 않았습니다.")
            return
        
        address_text = self.i2c_address_input.text()
        if not address_text.startswith("0x"):
            print("올바른 I2C 주소를 입력하세요. (예: 0x50)")
            return
        
        try:
            address = int(address_text, 16)
            slave = self.i2c.get_port(address)
            data = slave.read(16)  # 16바이트 데이터 읽기
            decoded_data = data.decode(errors="ignore")
            print(f"I2C 수신 (주소 {hex(address)}): {decoded_data}")
            self.i2c_receive_text.append(decoded_data)
        except Exception as e:
            print(f"I2C 수신 오류: {e}")

    def closeEvent(self, event):
        """창 닫을 때 UART & I2C 종료"""
        self.running = False
        if self.uart_port and self.uart_port.is_open:
            self.uart_port.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = USBCommApp()
    window.show()
    sys.exit(app.exec())
