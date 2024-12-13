import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QComboBox, QFormLayout, QDialog, QDialogButtonBox, QTextEdit

class FunctionBlockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создание функционального блока")

        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["EMB_RES", "STRING2STRING", "OUT_ANY_CONSOLE"])

        self.layout.addRow("Имя:", self.name_edit)
        self.layout.addRow("Тип:", self.type_combo)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)

    def get_values(self):
        return self.name_edit.text(), self.type_combo.currentText()

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("4diac IDE")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Выберите файл программы:", self)
        self.layout.addWidget(self.label)

        self.load_button = QPushButton("Загрузить файл", self)
        self.load_button.clicked.connect(self.load_program)
        self.layout.addWidget(self.load_button)

        self.create_button = QPushButton("Создать функциональный блок", self)
        self.create_button.clicked.connect(self.create_function_block)
        self.layout.addWidget(self.create_button)

        self.program_text = QTextEdit(self)
        self.layout.addWidget(self.program_text)

        self.send_button = QPushButton("Отправить на исполнительную среду", self)
        self.send_button.clicked.connect(self.send_program)
        self.send_button.setEnabled(False)
        self.layout.addWidget(self.send_button)

        self.status_label = QLabel("", self)
        self.layout.addWidget(self.status_label)

        self.program = ""

    def load_program(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл программы", "", "FBOOT Files (*.fboot);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                self.program = file.read()
                self.program_text.setPlainText(self.program)
                self.status_label.setText(f"Файл загружен: {file_path}")
                self.send_button.setEnabled(True)

    def create_function_block(self):
        dialog = FunctionBlockDialog(self)
        if dialog.exec_():
            name, fb_type = dialog.get_values()
            self.add_function_block(name, fb_type)

    def add_function_block(self, name, fb_type):
        # Создание строки для функционального блока
        fb_line = f';<Request ID="{self.get_next_id()}" Action="CREATE"><FB Name="{name}" Type="{fb_type}" /></Request>\n'
        self.program += fb_line
        self.program_text.setPlainText(self.program)
        self.status_label.setText(f"Функциональный блок {name} создан.")

    def get_next_id(self):
        # Генерация уникального ID для запроса
        return str(len(self.program.split(';<Request ')) + 1)

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
            for line in program.split('\n'):
                s.sendall((line + '\n').encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                if "OK" not in response:
                    raise Exception(f"Ошибка при отправке строки: {line}")
            s.close()

def main():
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
