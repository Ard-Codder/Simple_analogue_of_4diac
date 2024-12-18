import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QLabel, QColorDialog, QStyleFactory
from PyQt5.QtGui import QPainter, QColor, QPen, QCursor, QFont, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QPoint
from file_manager import FileManager
from tcp_sender import TcpSender
from connection import ConnectionManager
import custom_blocks as cb

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the main window with menus, actions, and default settings.
        """
        super().__init__()
        self.setWindowTitle("IDE - FB Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.blocks = []
        self.start_block = None
        self.file_path = '../projects/project1.xml'
        self.label = QLabel("", self)
        self.label.setGeometry(10, 10, 300, 100)
        self.current_x = 300
        self.current_y = 300
        self.coords_coef = 5
        self.pressed = False
        self.current_block = None
        self.menu_file = self.menuBar().addMenu("File")
        self.menu_blocks = self.menuBar().addMenu("Blocks")
        self.menu_run = self.menuBar().addMenu('Run')
        self.setMouseTracking(True)
        self.source_element = None
        self.destination_element = None
        self.block_count = cb.count_blocks()
        self.block_classes = cb.all_block_classes()
        self.connections = []
        self.movable_connection = None
        self.drawing_connection = False
        self.create_actions()
        self.setStyle(QStyleFactory.create('Fusion'))

        # Set style for the menu bar
        self.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: #333333;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QMenuBar::item {
                padding: 10px 20px;
                background-color: #444444;
                border-radius: 5px;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
        """)

        self.menu_file.setStyleSheet("""
            QMenu {
                background-color: #333333;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QMenu::item {
                padding: 10px 20px;
                background-color: #444444;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
        """)
        self.menu_blocks.setStyleSheet("""
            QMenu {
                background-color: #333333;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QMenu::item {
                padding: 10px 20px;
                background-color: #444444;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
        """)
        self.menu_run.setStyleSheet("""
            QMenu {
                background-color: #333333;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QMenu::item {
                padding: 10px 20px;
                background-color: #444444;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
        """)

    def update_all(self):
        """
        Update the entire window, including block names and rectangle values.
        """
        self.update()
        self.update_block_names()
        self.update_rect_values()

    def paintEvent(self, event):
        """
        Paint all blocks and connections on the window.
        """
        painter = QPainter(self)
        font = QFont("Arial", 6)  # Increase font size
        painter.setFont(font)
        for block in self.blocks:
            path = QPainterPath()
            path.addRoundedRect(block.x, block.y, block.width, block.height, 10, 10)  # Round the corners
            painter.setBrush(QColor(block.color))
            painter.drawPath(path)
            for rect in block.rectangles:
                sub_path = QPainterPath()
                sub_path.addRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), 5, 5)  # Round the corners for inputs/outputs
                painter.setBrush(QColor('white'))
                painter.drawPath(sub_path)
                painter.drawText(rect, Qt.AlignCenter, rect.name)

        for connection in self.connections:
            pen = QPen(QColor(connection.color), 2)
            brush = QBrush(QColor(connection.color))
            painter.setPen(pen)
            painter.setBrush(brush)
            for line in connection.line_array:
                painter.drawLine(line)
            painter.drawPolygon(connection.triangle)

    def update_rect_values(self):
        """
        Update the positions of the rectangle value labels.
        """
        for block in self.blocks:
            for rect in block.rectangles:
                if rect.editable_label:
                    rect.value_x = rect.x() - rect.value_width
                    rect.value_y = rect.y() + (rect.height() - rect.value_height) // 2
                    rect.editable_label.move(rect.value_x, rect.value_y)

    def update_block_names(self):
        """
        Update the positions of the block name labels.
        """
        for block in self.blocks:
            name_x = block.x + (block.width - block.label_width) // 2
            name_y = block.y - 25
            block.editable_label.move(name_x, name_y)

    def find_block(self):
        """
        Find the block that contains the current mouse position.
        """
        for block in self.blocks:
            if block.rectangles[0].contains(self.current_x, self.current_y):
                return block

    def find_connect_element(self, is_left_flag):
        """
        Find the rectangle that contains the current mouse position and matches the is_left_flag.
        """
        for block in self.blocks:
            for rect in block.rectangles[1:]:
                if rect.contains(self.current_x, self.current_y) and (rect.is_left is is_left_flag):
                    return rect

    def mousePressEvent(self, event):
        """
        Handle mouse press events to start moving blocks or drawing connections.
        """
        self.current_x = event.x()
        self.current_y = event.y()
        self.last_mouse_pos = event.pos()
        self.label.setText(f"Mouse position (Pressed): ({self.current_x}, {self.current_y})")
        self.label.adjustSize()
        self.label.move(10, 60)

        self.movable_connection, self.coord = self.check_moving_connect(event)
        self.source_element = self.find_connect_element(is_left_flag=False)

        if self.movable_connection is None:
            self.current_block = self.find_block()
            if self.current_block:
                self.current_block.change_coords(self.current_x, self.current_y)
            elif self.source_element:
                self.current_connection = ConnectionManager(
                    QPoint(self.source_element.right() + 1, self.source_element.center().y()),
                    QPoint(self.current_x + 1, self.current_y + 2),
                    color='black'  # Set default color to black
                )
                self.connections.append(self.current_connection)
                self.drawing_connection = True
        self.pressed = True
        self.update_all()

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to finish moving blocks or drawing connections.
        """
        self.current_x = event.x()
        self.current_y = event.y()
        if self.drawing_connection:
            self.destination_element = self.find_connect_element(is_left_flag=True)
            if self.destination_element:
                if self.current_connection.simple:
                    self.current_connection.simple_case(
                        dx1=self.current_connection.dx1,
                        destination=QPoint(self.destination_element.left() - 1, self.destination_element.center().y())
                    )
                else:
                    self.current_connection.hard_case(
                        dx1=self.current_connection.dx1,
                        dx2=self.current_connection.dx2,
                        dy1=self.current_connection.dy1,
                        destination=QPoint(self.destination_element.left() - 1, self.destination_element.center().y())
                    )
                self.source_element.parent.connections[self.source_element.name].append(
                    (self.destination_element.parent.name, self.destination_element.name)
                )
                if (self.source_element.data_element or self.destination_element.data_element):
                    self.current_connection.color = 'black'
                else:
                    self.current_connection.color = 'gray'
                self.source_element.connect_lines.append(self.current_connection)
                self.destination_element.connect_lines.append(self.current_connection)
            else:
                self.connections.pop(-1)

        self.current_block = None
        self.current_connection = None
        self.drawing_connection = False
        self.pressed = False
        self.movable_connection = None
        x = event.x()
        y = event.y()
        self.label.setText(f"Mouse position: ({x}, {y})")
        self.label.adjustSize()
        self.label.move(10, 60)
        self.update()

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events to update the position of blocks or connections.
        """
        self.current_x = event.x()
        self.current_y = event.y()
        if self.pressed:
            self.label.setText(f"Mouse position (Pressed): ({self.current_x}, {self.current_y})")
            self.label.adjustSize()
            self.label.move(10, 60)
            if self.current_block:
                self.current_block.change_coords(self.current_x, self.current_y)
            elif self.drawing_connection:
                self.current_connection.change_coords(event)
            else:
                self.change_movable_connection(event)
        else:
            self.label.setText(f"Mouse position: ({self.current_x}, {self.current_y})")
            self.label.adjustSize()
            self.label.move(10, 60)
            self.check_moving_connect(event)

        self.last_mouse_pos = event.pos()
        self.update_all()

    def change_movable_connection(self, event):
        """
        Change the coordinates of the movable connection.
        """
        if self.movable_connection:
            if self.movable_connection.simple:
                if (event.x() - self.movable_connection.x1 > 10) and (self.movable_connection.x3 - event.x() > 10):
                    self.movable_connection.simple_case(dx1=event.x() - self.movable_connection.x1)
            else:
                if (self.coord == 'dx1') and (event.x() - self.movable_connection.x1 > 10):
                    self.movable_connection.hard_case(
                        dx1=event.x() - self.movable_connection.x1,
                        dx2=self.movable_connection.dx2,
                        dy1=self.movable_connection.dy1
                    )
                elif self.coord == 'dy1':
                    self.movable_connection.hard_case(
                        dx1=self.movable_connection.dx1,
                        dx2=self.movable_connection.dx2,
                        dy1=event.y() - self.movable_connection.y1
                    )
                elif (self.coord == 'dx2') and (self.movable_connection.x4 - event.x() > 10):
                    self.movable_connection.hard_case(
                        dx1=self.movable_connection.dx1,
                        dx2=self.movable_connection.x4 - event.x(),
                        dy1=self.movable_connection.dy1
                    )

    def check_moving_connect(self, event):
        """
        Check if the mouse is over a movable connection and return the connection and coordinate.
        """
        for connection in self.connections:
            if connection.rect_line2.contains(event.x(), event.y()):
                self.setCursor(QCursor(Qt.SizeHorCursor))
                return (connection, 'dx1')
            elif connection.rect_line3.contains(event.x(), event.y()):
                self.setCursor(QCursor(Qt.SizeVerCursor))
                return (connection, 'dy1')
            elif connection.rect_line4.contains(event.x(), event.y()):
                self.setCursor(QCursor(Qt.SizeHorCursor))
                return (connection, 'dx2')
            else:
                self.unsetCursor()
        return (None, None)

    def create_actions(self):
        """
        Create actions for the file and blocks menus.
        """
        open_project_action = QAction("Open", self)
        open_project_action.triggered.connect(lambda: FileManager.read_xml(self))

        create_xml_action = QAction("Save as XML", self)
        create_xml_action.triggered.connect(lambda: FileManager.create_xml(self.blocks, self.start_block, self.coords_coef))

        create_fboot_action = QAction("Create fboot file", self)
        create_fboot_action.triggered.connect(lambda: FileManager.create_fboot(self.blocks, self.start_block))

        self.menu_file.addAction(open_project_action)
        self.menu_file.addAction(create_xml_action)
        self.menu_file.addAction(create_fboot_action)

        # Add block actions to the Blocks menu
        start_action = QAction("START", self)
        start_action.triggered.connect(lambda: cb.create_block_start(self))
        self.menu_blocks.addAction(start_action)

        int2int_action = QAction("INT2INT", self)
        int2int_action.triggered.connect(lambda: cb.create_block_int2int(self))
        self.menu_blocks.addAction(int2int_action)

        out_any_console_action = QAction("OUT_ANY_CONSOLE", self)
        out_any_console_action.triggered.connect(lambda: cb.create_block_out_any_console(self))
        self.menu_blocks.addAction(out_any_console_action)

        string2string_action = QAction("STRING2STRING", self)
        string2string_action.triggered.connect(lambda: cb.create_block_string2string(self))
        self.menu_blocks.addAction(string2string_action)

        f_add_action = QAction("F_ADD", self)
        f_add_action.triggered.connect(lambda: cb.create_block_f_add(self))
        self.menu_blocks.addAction(f_add_action)

        deploy_action = QAction('Deploy', self)
        deploy_action.triggered.connect(self.deploy)
        self.menu_run.addAction(deploy_action)

    def deploy(self):
        """
        Deploy the project by creating an fboot file and sending it via TCP.
        """
        FileManager.create_fboot(self.blocks, self.start_block, with_gui=False)
        TcpSender('../projects/deploy.fboot')

    def show_connections(self):
        """
        Print the connections of all blocks to the console.
        """
        for block in self.blocks:
            print(block.name, block.connections)
            for source_element, ar_elements in block.connections.items():
                if ar_elements:
                    for dest_block_name, dest_el in ar_elements:
                        print(f"Connection Source = {block.name}.{source_element}, Destination = {dest_block_name}.{dest_el}, Comment = ")

    def contextMenuEvent(self, event):
        """
        Handle context menu events to delete connections or blocks.
        """
        cur_connection, text = self.check_moving_connect(event)
        if cur_connection:
            line_context_menu = QMenu(self)
            action_delete = QAction("Delete connection", self)
            action_delete.triggered.connect(lambda: self.delete_connection(cur_connection))
            line_context_menu.addAction(action_delete)

            action_color = QAction("Change color", self)
            action_color.triggered.connect(lambda: self.change_connection_color(cur_connection))
            line_context_menu.addAction(action_color)

            line_context_menu.exec_(event.globalPos())
        else:
            for block in self.blocks:
                if block.rectangles[0].contains(self.current_x, self.current_y):
                    context_menu = QMenu(self)
                    action1 = QAction("Delete block", self)
                    action1.triggered.connect(lambda: self.delete_block(block))
                    context_menu.addAction(action1)
                    context_menu.exec_(event.globalPos())
        self.update_all()

    def change_connection_color(self, connection):
        """
        Change the color of a connection.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            connection.color = color.name()
            self.update()

    def clear(self):
        """
        Clear all blocks and connections from the window.
        """
        while self.blocks:
            self.delete_block(self.blocks[0])
        self.connections = []
        self.pressed = False
        self.update_all()

    def delete_block(self, block):
        """
        Delete a block and its connections.
        """
        for rect in block.rectangles:
            if rect.editable_label:
                rect.editable_label.delete()
            while rect.connect_lines:
                self.delete_connection(rect.connect_lines[0])
        self.blocks.remove(block)
        block.editable_label.delete()

    def delete_connection(self, cur_connection):
        """
        Delete a connection from the window.
        """
        for block in self.blocks:
            for rect in block.rectangles[1:]:
                for connection in rect.connect_lines:
                    if connection == cur_connection:
                        if rect.is_left:
                            dest_el = rect
                        else:
                            source_el = rect
        source_el.parent.connections[source_el.name].remove((dest_el.parent.name, dest_el.name))
        source_el.connect_lines.remove(cur_connection)
        dest_el.connect_lines.remove(cur_connection)
        self.connections.remove(cur_connection)
        self.unsetCursor()
