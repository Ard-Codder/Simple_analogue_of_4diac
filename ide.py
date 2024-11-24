import sys
import xml.etree.ElementTree as ET
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("4diac IDE")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Выберите файл программы:", self)
        self.layout.addWidget(self.label)

        self.load_button = QPushButton("Загрузить файл", self)
        self.load_button.clicked.connect(self.load_program)
        self.layout.addWidget(self.load_button)

        self.send_button = QPushButton("Отправить на исполнительную среду", self)
        self.send_button.clicked.connect(self.send_program)
        self.send_button.setEnabled(False)
        self.layout.addWidget(self.send_button)

        self.status_label = QLabel("", self)
        self.layout.addWidget(self.status_label)

        self.program = None

    def load_program(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл программы", "", "XML Files (*.xml);;All Files (*)", options=options)
        if file_path:
            self.program = self.load_program_from_file(file_path)
            self.status_label.setText(f"Файл загружен: {file_path}")
            self.send_button.setEnabled(True)

    def load_program_from_file(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        return ET.tostring(root, encoding='utf-8')

    def send_program(self):
        if self.program:
            try:
                self.send_program_to_runtime(self.program)
                self.status_label.setText("Программа отправлена в исполнительную среду.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось отправить программу: {e}")

    def send_program_to_runtime(self, program, host='localhost', port=61499):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(program)
            s.close()

def main():
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
