from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QPainterPath, QColor, QFont
from editable_label import EditableLabel

class MyRect(QRect):
    def __init__(self, *args, parent=None, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.name = name
        self.connect_lines = []
        self.value = "''"
        self.is_left = False
        self.editable_label = None
        self.value_width = 0
        self.value_height = 0
        self.value_x = None
        self.value_y = None
        self.data_element = False

class FuncBlock:
    def __init__(self, main_window, name=None, x=300, y=300, width=100, height=100, color='white', n_rects_left=4, n_rects_right=4, labels=None):
        self.main_window = main_window
        self.name = name
        self.block_size_coef = 1
        self.x = x
        self.y = y
        self.width = int(width * self.block_size_coef)
        self.height = int(height * self.block_size_coef)
        self.rectangles = []
        self.labels = labels
        self.type = labels[0]
        self.connections = {self.labels[i]: [] for i in range(1, len(self.labels))}
        self.n_rects_left = n_rects_left
        self.n_rects_right = n_rects_right
        self.color = color
        self.cell_height_left = int(self.height / self.n_rects_left)
        self.cell_height_right = int(self.height / self.n_rects_right)
        self.cell_width = int(self.width / 2)
        self.create_label()
        self.create_rect()
        self.create_rect_values()

    def create_label(self):
        self.label_width = self.width + self.width // 2
        self.label_height = 20
        self.label_x = self.x + (self.width - self.label_width) // 2
        self.label_y = self.y - 25
        self.editable_label = EditableLabel(main_window=self.main_window, block=self, field='name', text=self.name, x=self.label_x, y=self.label_y, width=self.label_width, height=self.label_height)

    def create_rect_values(self):
        rect_with_values = ['IN', 'IN1', 'IN2', 'IN3', 'IN4', 'QI', 'LABEL']
        for rect in self.rectangles:
            if rect.name in rect_with_values:
                rect.value_width = 50
                rect.value_height = 20
                rect.data_element = True
                rect.value_x = rect.x() - rect.value_width
                rect.value_y = rect.y() + (rect.height() - rect.value_height) // 2
                rect.editable_label = EditableLabel(main_window=self.main_window, block=self, rect=rect, field='value', text=rect.value, x=rect.value_x, y=rect.value_y, width=rect.value_width, height=rect.value_height)

    def create_rect(self):
        self.rectangles.append(MyRect(self.x, self.y, self.width, self.height, name=self.type, parent=self))
        cell_x_left = self.x - self.cell_width
        for cur_rect in range(self.n_rects_left):
            new_y = int(self.y + (self.height / self.n_rects_left) * cur_rect)
            new_rect = MyRect(cell_x_left, new_y, self.cell_width, self.cell_height_left, name=self.labels[1 + cur_rect], parent=self)
            new_rect.is_left = True
            self.rectangles.append(new_rect)

        cell_x_right = self.x + self.width
        for cur_rect in range(self.n_rects_right):
            new_y = int(self.y + (self.height / self.n_rects_right) * cur_rect)
            self.rectangles.append(MyRect(cell_x_right, new_y, self.cell_width, self.cell_height_right, name=self.labels[self.n_rects_left + 1 + cur_rect], parent=self))

    def change_coords(self, current_x, current_y):
        for rect in self.rectangles:
            dx = self.main_window.last_mouse_pos.x() - rect.x()
            dy = self.main_window.last_mouse_pos.y() - rect.y()
            rect.moveTo(current_x - dx, current_y - dy)
            if rect != self.rectangles[0]:
                for polyline in rect.connect_lines:
                    if rect.is_left:
                        if polyline.simple:
                            if polyline.source_x + 40 < polyline.destination_x:
                                if polyline.dx1 > rect.left() - polyline.source_x - 20:
                                    polyline.simple_case(dx1=rect.left() - polyline.source_x - 20, destination=QPoint(rect.left() - 1, rect.center().y()))
                                else:
                                    polyline.simple_case(dx1=polyline.dx1, destination=QPoint(rect.left() - 1, rect.center().y()))
                            else:
                                polyline.hard_case()
                        else:
                            if polyline.source_x + 40 < polyline.destination_x:
                                polyline.simple_case()
                            else:
                                polyline.hard_case(dx1=polyline.dx1, dx2=polyline.dx2, dy1=polyline.dy1, destination=QPoint(rect.left() - 1, rect.center().y()))
                    else:
                        if polyline.simple:
                            if polyline.source_x + 40 < polyline.destination_x:
                                if polyline.dx1 > polyline.destination_x - rect.right() - 20:
                                    polyline.simple_case(dx1=polyline.destination_x - rect.right() - 20, source=QPoint(rect.right() + 1, rect.center().y()))
                                else:
                                    polyline.simple_case(dx1=polyline.dx1, source=QPoint(rect.right() + 1, rect.center().y()))
                            else:
                                polyline.hard_case()
                        else:
                            if polyline.source_x + 40 < polyline.destination_x:
                                polyline.simple_case()
                            else:
                                polyline.hard_case(dx1=polyline.dx1, dx2=polyline.dx2, dy1=polyline.dy1, source=QPoint(rect.right() + 1, rect.center().y()))
            self.x = self.rectangles[0].x()
            self.y = self.rectangles[0].y()

    def draw(self, painter):
        path = QPainterPath()
        path.addRoundedRect(self.x, self.y, self.width, self.height, 10, 10)  # Закругляем углы
        painter.setBrush(QColor(self.color))
        painter.drawPath(path)
        for rect in self.rectangles:
            painter.drawText(rect, Qt.AlignCenter, rect.name)
