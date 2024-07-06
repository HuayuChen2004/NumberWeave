from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHeaderView, QTextEdit,
    QWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QTableWidgetItem, QTableWidget
)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap, QFont, QBrush, QPalette
from memory_pic import background_png, play_png, to_be_known_png, win_png, choose_mode_png
import base64
from map import Map  # 假设Map类适用于PyQt5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Weave")
        self.setGeometry(100, 100, 900, 1300)
        self.width = 900
        self.height = 1300
        self.actions = []
        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_timer)
        self.time_elapsed = QTime(0, 0, 0)
        # self.timer_label = QLabel("00:00:00", self)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.is_on_win_screen = False

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.show_start_screen()

    def clear_layout(self):
        item_list = list(range(self.layout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.layout.itemAt(i)
            self.layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout() is not None:
                self.clear_layout_recursive(item.layout())
                self.layout.removeItem(item)
        self.layout.update()

    def clear_layout_recursive(self, layout):
        for i in reversed(range(layout.count())): 
            layout_item = layout.itemAt(i)
            if layout_item.widget() is not None:
                layout_item.widget().deleteLater()
            elif layout_item.layout() is not None:
                self.clear_layout_recursive(layout_item.layout())
            layout.removeItem(layout_item)

    def show_start_screen(self):
        self.clear_layout()
        # 设置背景图片
        palette = QPalette()
        background = QPixmap()
        background.loadFromData(base64.b64decode(background_png))
        palette.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palette)    

        # 设置垂直布局的间隙
        self.layout.setSpacing(100)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 创建水平布局来包裹 welcome_label，并实现水平居中
        welcome_label_layout = QHBoxLayout()
        welcome_label_layout.setSpacing(100)  # 设置水平布局的间隙
        welcome_label_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        welcome_label = QLabel("Welcome to Number Weave!", self)
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: black;
            }
        """)
        welcome_label_layout.addWidget(welcome_label)
        
        welcome_label_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(welcome_label_layout)

        # 创建水平布局来包裹 play_button，并实现水平居中
        play_button_layout = QHBoxLayout()
        play_button_layout.setSpacing(100)  # 设置水平布局的间隙
        play_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        play_button = QPushButton("Play", self)
        play_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #45a049;
            }
        """)                     
        play_button_layout.addWidget(play_button)
        
        play_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(play_button_layout)

        # 创建水平布局来包裹 exit_button，并实现水平居中
        exit_button_layout = QHBoxLayout()
        exit_button_layout.setSpacing(100)  # 设置水平布局的间隙
        exit_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        exit_button = QPushButton("Exit", self)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """)                     
        exit_button_layout.addWidget(exit_button)
        
        exit_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(exit_button_layout)
        
        # 在所有控件添加完毕后，再添加一个垂直方向的弹性空间到底部，以实现垂直居中
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 为按钮添加点击事件
        play_button.clicked.connect(self.show_choose_mode_screen)
        exit_button.clicked.connect(self.close)

    def show_choose_mode_screen(self):
        self.stop_timer()
        self.clear_layout()
        palette = QPalette()
        choose_mode = QPixmap()
        choose_mode.loadFromData(base64.b64decode(choose_mode_png))
        palette.setBrush(QPalette.Background, QBrush(choose_mode))
        self.setPalette(palette) 
        easy_button = QPushButton("5x5 Easy Mode", self)
        easy_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #45a049;
            }
        """)                     
        easy_button.clicked.connect(lambda: self.play_screen(5))

        medium_button = QPushButton("10x10 Medium Mode", self)
        medium_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #45a049;
            }
        """)                     
        medium_button.clicked.connect(lambda: self.play_screen(10))

        hard_button = QPushButton("15x15 Hard Mode", self)
        hard_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #45a049;
            }
        """)                     
        hard_button.clicked.connect(lambda: self.play_screen(15))

        custom_button = QPushButton("Custom Mode", self)
        custom_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #45a049;
            }
        """)                     
        custom_button.clicked.connect(lambda: self.play_screen(10))  

        back_button = QPushButton("Back", self)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """)                     
        back_button.clicked.connect(self.show_start_screen)

        self.layout.addWidget(easy_button)
        self.layout.addWidget(medium_button)
        self.layout.addWidget(hard_button)
        self.layout.addWidget(custom_button)
        self.layout.addWidget(back_button)

    def handleKeyPress(self, event):
        key = event.key()
        if key == Qt.Key_Z:
            # 当按下 Z 键时执行的操作
            self.fill_current_cell()
        elif key == Qt.Key_X:
            # 当按下 X 键时执行的操作
            self.cross_current_cell()
        elif key == Qt.Key_C:
            # 当按下 C 键时执行的操作
            self.clear_current_cell()
        else:
            # 对于其他按键，调用基类的处理方法
            super().keyPressEvent(event)

    def fill_current_cell(self):
        # 获取当前选中的单元格
        current_cell = self.table.currentItem()
        row = self.table.currentRow()
        col = self.table.currentColumn()
        if current_cell is not None and row > 0 and col > 0:
            # 填充当前单元格
            text = current_cell.text()
            current_cell.setText("")
            current_cell.setText("■")
            current_cell.setFont(QFont("Arial", 40, QFont.Bold))
            current_cell.setTextAlignment(Qt.AlignCenter)
            current_cell.setForeground(QBrush(Qt.magenta))
            self.actions.append((row, col, text, "■"))
            if len(self.actions) > 100:
                self.actions.pop(0)

    def cross_current_cell(self):
        # 获取当前选中的单元格
        current_cell = self.table.currentItem()
        row = self.table.currentRow()
        col = self.table.currentColumn()
        if current_cell is not None and row > 0 and col > 0:
            # 填充当前单元格
            text = current_cell.text()
            current_cell.setText("")
            current_cell.setText("x")
            current_cell.setFont(QFont("Arial", 35, QFont.Bold))
            current_cell.setTextAlignment(Qt.AlignCenter)
            self.actions.append((row, col, text, "x"))
            if len(self.actions) > 100:
                self.actions.pop(0)

    def clear_current_cell(self):
        # 获取当前选中的单元格
        current_cell = self.table.currentItem()
        row = self.table.currentRow()
        col = self.table.currentColumn()
        if current_cell is not None and row > 0 and col > 0:
            # 填充当前单元格
            text = current_cell.text()
            current_cell.setText("")
            current_cell.setFont(QFont("Arial", 35, QFont.Bold))
            current_cell.setTextAlignment(Qt.AlignCenter)
            self.actions.append((row, col, text, ""))
            if len(self.actions) > 100:
                self.actions.pop(0)

    def undo_action(self):
        if self.actions:
            row, col, text, new_text = self.actions.pop()
            item = self.table.item(row, col)
            item.setText(text)

    def update_timer(self):
        if self.timer_label:
            self.time_elapsed = self.time_elapsed.addSecs(1)
            self.timer_label.setText(self.time_elapsed.toString("hh:mm:ss"))
        else:
            self.stop_timer()  # 如果 QLabel 不存在，停止计时器

    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.timer_label = None  # 清除对 QLabel 的引用

    def play_screen(self, size):

        self.clear_layout()
        palette = QPalette()
        play = QPixmap()
        play.loadFromData(base64.b64decode(play_png))
        palette.setBrush(QPalette.Background, QBrush(play))
        self.setPalette(palette) 
        self.map = Map(size)  
        self.current_play_size = size

        self.timer = QTimer(self)
        self.time_elapsed = QTime(0, 0, 0)
        self.timer.timeout.connect(self.update_timer)
        self.timer_label = QLabel("00:00:00", self)
        self.timer_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: black;
                margin-top: 10px;
                margin-left: 10px;
            }
        """)
        self.layout.addWidget(self.timer_label)
        self.timer.start(1000)  # 每1000毫秒更新一次
        # 创建表格
        self.table = MyTableWidget(self)
        self.table.setRowCount(size+1)  # 设置行数
        self.table.setColumnCount(size+1)  # 设置列数

        self.table.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.table.verticalHeader().setVisible(False)  # 隐藏垂直表头
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FFC0CB;
                border: 3px solid red;
                border-radius: 8px;
                align: center;

                margin: 10px;
            }
            
            QTableWidget::item {
                border: 3px solid red;
                border-radius: 8px;
                padding: 0px;
                font-size: 30px;
                font-weight: 800;
                color: black;
                text-align: center;
            }
            QTableWidget::item:selected {
                background-color: orange;
                color: black;
            }
        """)
            # 调整每个单元格的长度和宽度
        col_count = self.map.get_col_count()
        row_count = self.map.get_row_count()

        for i in range(size+1):
            self.table.setColumnWidth(i, 50)  
            self.table.setRowHeight(i, 50) 

        # 填充表格数据
        for i in range(size+1):
            for j in range(size+1):
                if i == 0 and j > 0:
                    item = QTableWidgetItem("\n".join(map(str, col_count[j-1])))
                    item.setFont(QFont("Arial", 16, QFont.Bold))
                elif j == 0 and i > 0:
                    item = QTableWidgetItem(" ".join(map(str, row_count[i-1])))
                    item.setFont(QFont("Arial", 16, QFont.Bold))
                else:
                    item = QTableWidgetItem("")
                flags = item.flags()
                flags &= ~Qt.ItemIsEditable  # 禁止编辑
                item.setFlags(flags)
                self.table.setItem(i, j, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.table)

        # 强制更新表格布局
        self.table.updateGeometry()

        back_button = QPushButton("Back", self)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 25px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """)                     
        back_button.clicked.connect(self.show_choose_mode_screen)
        # 创建三个按钮
        to_be_known_button = QPushButton("To be known", self)
        to_be_known_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 25px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """) 
        to_be_known_button.setText("To be known")
        submit_button = QPushButton("Submit", self)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 25px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """) 
        submit_button.setText("Submit")

        undo_button = QPushButton("Undo", self)
        undo_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 25px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """) 
        undo_button.setText("Undo")

        # 为撤销按钮添加点击事件
        undo_button.clicked.connect(self.undo_action)

        # 为按钮添加点击事件
        submit_button.clicked.connect(self.check_result)

        to_be_known_button.clicked.connect(self.show_to_be_known_screen)

        # 创建一个水平布局
        hbox = QHBoxLayout()

        # 添加一个弹性空间到布局的开始，推动后面的内容到右侧
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将三个按钮添加到水平布局中
        hbox.addWidget(to_be_known_button)
        # 在按钮之间添加弹性空间
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addWidget(submit_button)
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addWidget(undo_button)
        # 再次添加弹性空间
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addWidget(back_button)

        # 添加一个弹性空间到布局的末尾，以确保按钮等间隔排列
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将水平布局添加到主布局的底部
        self.layout.addLayout(hbox)

    def show_to_be_known_screen(self):
        self.to_be_known_window = ToBeKnownWindow()
        self.to_be_known_window.show()

    def check_result(self):
        if self.is_finished():
            self.stop_timer()
            self.show_win_screen()

    def is_finished(self):
        for i in range(self.current_play_size):
            row_answer = []
            for j in range(self.current_play_size):
                if self.table.item(i+1, j+1).text() == "■":
                    row_answer.append(1)
                else:
                    row_answer.append(0)
            str_row_answer = "".join(map(str, row_answer))
            row_answer_i = [len(x) for x in str_row_answer.split("0") if x]
            if row_answer_i != self.map.get_row_count()[i]:
                return False
        for j in range(self.current_play_size):
            col_answer = []
            for i in range(self.current_play_size):
                if self.table.item(i+1, j+1).text() == "■":
                    col_answer.append(1)
                else:
                    col_answer.append(0)
            str_col_answer = "".join(map(str, col_answer))
            col_answer_i = [len(x) for x in str_col_answer.split("0") if x]
            if col_answer_i != self.map.get_col_count()[j]:
                return False
        return True

    def show_win_screen(self):
        self.is_on_win_screen = True
        self.clear_layout()
        palette = QPalette()
        win = QPixmap()
        win.loadFromData(base64.b64decode(win_png))
        palette.setBrush(QPalette.Background, QBrush(win.scaled(self.width, self.height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)))
        self.setPalette(palette)

        self.layout.addStretch(1)  # 添加弹性空间，使后续的控件靠底部对齐

        back_button = QPushButton("Back", self)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 0px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """)
        back_button.clicked.connect(lambda: self.play_screen(self.current_play_size))

        self.layout.addWidget(back_button)


class MyTableWidget(QTableWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super(MyTableWidget, self).__init__(parent)

    def keyPressEvent(self, event):
        parent = self.parent
        if parent and hasattr(parent, 'handleKeyPress'):
            parent.handleKeyPress(event)
        else:
            super().keyPressEvent(event)


class ToBeKnownWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("To Be Known")
        self.setGeometry(100, 100, 900, 1300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        
        palette = QPalette()
        to_be_known = QPixmap()
        to_be_known.loadFromData(base64.b64decode(to_be_known_png))
        
        palette.setBrush(QPalette.Background, QBrush(to_be_known.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)))
        self.setPalette(palette)

        # 创建一个水平布局来包裹标题，并确保它在水平方向上居中
        title_hbox = QHBoxLayout()

        # 添加弹性空间到标题的左侧
        title_hbox.addStretch(1)

        title = QLabel("To be known", self)
        title.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: bold;
                color: black;
                text-align: center;
                margin-top: 50px;
                margin-bottom: 0px;
                font-family: 'Lucida Handwriting';
            }
        """)
        title_hbox.addWidget(title)

        # 添加弹性空间到标题的右侧
        title_hbox.addStretch(1)

        # 将包含标题的水平布局添加到主布局中
        self.layout.addLayout(title_hbox)

        text_box = QTextEdit(self)
        text_box.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                font-size: 24px;
                font-weight: bold;
                color: black;
                height: 1000px;
                margin: 0px 50px;
                background-color: transparent;
                border: none;
                font-family: Arial;
                
            }
        """)
        text_box.setPlainText("""
        1. 对选中的单元格，按下"Z"标记填充，按下"X"标记叉，按下"C"清空该单元格。\n
        2. 如在游戏中发现任何问题，请联系开发人员，你的意见对我们十分重要！\n
            开发人员微信：cauchy_stay_with_you\n
        3. 后续版本更新将会同步到github上，欢迎大家关注！
        """)
        text_box.setReadOnly(True)

        text_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        text_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.layout.addWidget(text_box)

        back_button = QPushButton("Back", self)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 32px;
                margin: 0px 2px;
                cursor: pointer;
                border-radius: 8px;
                font-weight: bold;
            }
        QPushButton:hover {
            background-color: #da190b;
            }
        """)                     
        back_button.clicked.connect(self.close)

        self.layout.addWidget(back_button)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())