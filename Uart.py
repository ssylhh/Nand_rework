import sys
import serial
import serial.tools.list_ports
import threading
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QComboBox

class UARTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB to UART 통신")
        self.setGeometry(100, 100, 500, 300)

        # UI 구성
        layout = QVBoxLayout()

        # 포트 선택 드롭다운
        self.port_label = QLabel("COM 포트 선택:")
        layout.addWidget(self.port_label)

        self.port_selector = QComboBox()
        self.update_ports()
        layout.addWidget(self.port_selector)

        # 송신 데이터 입력창 및 버튼
        self.send_input = QLineEdit()
        self.send_input.setPlaceholderText("전송할 데이터 입력...")
        layout.addWidget(self.send_input)

        self.send_button = QPushButton("전송")
        self.send_button.clicked.connect(self.send_data)
        layout.addWidget(self.send_button)

        # 수신 데이터 창
        self.receive_label = QLabel("수신된 데이터:")
        layout.addWidget(self.receive_label)

        self.receive_text = QTextEdit()
        self.receive_text.setReadOnly(True)
        layout.addWidget(self.receive_text)

        self.setLayout(layout)

        # UART 설정
        self.serial_port = None
        self.running = False
        self.start_uart_thread()

    def update_ports(self):
        """사용 가능한 COM 포트 목록 갱신"""
        ports = serial.tools.list_ports.comports()
        self.port_selector.clear()
        for port in ports:
            self.port_selector.addItem(port.device)

    def start_uart_thread(self):
        """UART 수신을 위한 스레드 실행"""
        self.running = True
        self.thread = threading.Thread(target=self.receive_data, daemon=True)
        self.thread.start()

    def open_uart(self):
        """선택된 COM 포트로 UART 연결"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

        selected_port = self.port_selector.currentText()
        try:
            self.serial_port = serial.Serial(selected_port, 115200, timeout=1)
            print(f"연결 성공: {selected_port}")
        except serial.SerialException as e:
            print(f"연결 실패: {e}")

    def send_data(self):
        """UART 송신"""
        if self.serial_port and self.serial_port.is_open:
            data = self.send_input.text()
            if data:
                self.serial_port.write(data.encode())
                print(f"송신: {data}")
        else:
            print("UART 포트가 열려있지 않습니다.")

    def receive_data(self):
        """UART 데이터 수신"""
        while self.running:
            if self.serial_port and self.serial_port.is_open:
                try:
                    data = self.serial_port.readline().decode(errors="ignore").strip()
                    if data:
                        print(f"수신: {data}")
                        self.receive_text.append(data)  # GUI 창에 데이터 추가
                except serial.SerialException as e:
                    print(f"수신 오류: {e}")
            time.sleep(0.1)

    def closeEvent(self, event):
        """창 닫을 때 UART 정리"""
        self.running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UARTApp()
    window.show()
    sys.exit(app.exec())