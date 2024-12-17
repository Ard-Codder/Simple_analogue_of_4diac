from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QFont

class EditableLabel:
    def __init__(self, main_window, block=None, rect=None, field="", text="", x=0, y=0, width=100, height=30):
        self.main_window = main_window
        self.block = block
        self.rect = rect
        self.field = field

        self.label = QLabel(text, main_window)
        font = QFont("Arial", 9, QFont.Bold)  # Изменяем шрифт
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(x, y, width, height)
        self.label.mousePressEvent = self.edit_label
        self.label.show()

        self.line_edit = QLineEdit(main_window)
        self.line_edit.setFont(font)
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setGeometry(x, y, width, height)
        self.line_edit.setVisible(False)
        self.line_edit.returnPressed.connect(self.save_label)
        self.line_edit.editingFinished.connect(self.save_label)

    def edit_label(self, event):
        self.label.setVisible(False)
        self.line_edit.setText(self.label.text())
        self.line_edit.setVisible(True)
        self.line_edit.setFocus()

    def save_label(self):
        self.label.setText(self.line_edit.text())
        self.line_edit.setVisible(False)
        self.label.setVisible(True)
        self.change_field()

    def move(self, x, y):
        self.label.move(x, y)
        self.line_edit.move(x, y)

    def get_text(self):
        return self.line_edit.text()

    def change_field(self):
        if self.field == 'name':
            self.block.name = self.line_edit.text()
        else:
            self.rect.value = self.line_edit.text()

    def delete(self):
        self.label.hide()
        self.line_edit.hide()
        self.label.deleteLater()
        self.line_edit.deleteLater()
