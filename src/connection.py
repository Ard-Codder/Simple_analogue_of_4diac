from PyQt5.QtGui import QPainter, QPen, QCursor, QPolygon, QColor
from PyQt5.QtCore import Qt, QLine, QPoint, QRect

class ConnectionManager:
    def __init__(self, point_source, point_destination, color='black'):
        self.point_source = point_source
        self.point_destination = point_destination
        self.color = color
        self.source_x = point_source.x()
        self.source_y = point_source.y()
        self.destination_x = point_destination.x()
        self.destination_y = point_destination.y()
        self.draw_triangle()
        if self.source_x < self.destination_x:
            self.simple = True
            self.simple_case()
        else:
            self.simple = False
            self.hard_case()

    def simple_case(self, dx1=None, source=None, destination=None):
        self.dy1 = None
        self.dx2 = None
        if source:
            self.point_source = source
            self.source_x = self.point_source.x()
            self.source_y = self.point_source.y()
        if destination:
            self.point_destination = destination
            self.destination_x = self.point_destination.x()
            self.destination_y = self.point_destination.y()
        if dx1:
            self.dx1 = dx1
        else:
            self.dx1 = abs(self.source_x - self.destination_x) // 2
        self.x1 = self.source_x
        self.x2 = self.x1 + self.dx1
        self.x3 = self.destination_x
        self.y1 = self.source_y
        self.y2 = self.destination_y
        point1 = QPoint(self.x1, self.y1)
        point2 = QPoint(self.x2, self.y1)
        point3 = QPoint(self.x2, self.y2)
        point4 = QPoint(self.x3, self.y2)
        self.rect_line2 = QRect(QPoint(self.x2 - 5, self.y1 - 5), QPoint(self.x2 + 5, self.y2 + 5))
        self.rect_line3 = QRect()
        self.rect_line4 = QRect()
        line1 = QLine(point1, point2)
        line2 = QLine(point2, point3)
        line3 = QLine(point3, point4)
        self.line_array = [line1, line2, line3]
        self.simple = True
        self.draw_triangle()

    def hard_case(self, dx1=20, dx2=20, dy1=None, source=None, destination=None):
        if source:
            self.point_source = source
            self.source_x = self.point_source.x()
            self.source_y = self.point_source.y()
        if destination:
            self.point_destination = destination
            self.destination_x = self.point_destination.x()
            self.destination_y = self.point_destination.y()

        self.dx1 = dx1
        self.dx2 = dx2
        if dy1:
            self.dy1 = dy1
        else:
            self.dy1 = (self.destination_y - self.source_y) // 2
        self.x1 = self.source_x
        self.x2 = self.x1 + self.dx1
        self.x3 = self.destination_x - self.dx2
        self.x4 = self.destination_x
        self.y1 = self.source_y
        self.y2 = self.y1 + self.dy1
        self.y3 = self.destination_y
        point1 = QPoint(self.x1, self.y1)
        point2 = QPoint(self.x2, self.y1)
        point3 = QPoint(self.x2, self.y2)
        point4 = QPoint(self.x3, self.y2)
        point5 = QPoint(self.x3, self.y3)
        point6 = QPoint(self.x4, self.y3)
        self.rect_line2 = QRect(QPoint(self.x2 - 5, self.y1), QPoint(self.x2 + 5, self.y2))
        self.rect_line3 = QRect(QPoint(self.x3, self.y2 - 5), QPoint(self.x2, self.y2 + 5))
        self.rect_line4 = QRect(QPoint(self.x3 - 5, self.y3), QPoint(self.x3 + 5, self.y2))
        line1 = QLine(point1, point2)
        line2 = QLine(point2, point3)
        line3 = QLine(point3, point4)
        line4 = QLine(point4, point5)
        line5 = QLine(point5, point6)
        self.line_array = [line1, line2, line3, line4, line5]
        self.simple = False
        self.draw_triangle()

    def change_coords(self, current_point):
        self.point_destination = QPoint(current_point.x(), current_point.y())
        self.destination_x = current_point.x()
        self.destination_y = current_point.y()
        if self.source_x + 40 < self.destination_x:
            self.simple_case()
        else:
            self.hard_case()
        self.draw_triangle()

    def draw_triangle(self):
        self.triangle_points = [
            self.point_destination,
            QPoint(self.destination_x - 7, self.destination_y - 4),
            QPoint(self.destination_x - 7, self.destination_y + 4)
        ]
        self.triangle = QPolygon(self.triangle_points)
        for i in range(3):
            self.triangle.setPoint(i, self.triangle_points[i])
