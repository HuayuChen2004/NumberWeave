from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QBrush, QPalette
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QLineEdit
from memory_pic import background_png, play_png, purple_png, to_be_known_png, win_png, choose_mode_png
import base64
from map import Map  # 假设Map类适用于PyQt5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Weave")
        self.setGeometry(100, 100, 900, 1200)
        self.width = 900
        self.height = 1200
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.is_on_win_screen = False

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
        self.layout.setSpacing(100)  # 假设您想要的间隙是10像素

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

    
    
    # 如果有更多控件，重复上述步骤

    def show_choose_mode_screen(self):
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
        custom_button.clicked.connect(lambda: self.play_screen(10))  # 示例，实际中可能需要更复杂的逻辑

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

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            # 当按下 Ctrl 键时执行的操作
            self.fill_current_cell()
        elif event.modifiers() == Qt.AltModifier:
            # 当按下 Alt 键时执行的操作
            self.cross_current_cell()
        else:
            # 对于其他按键，调用基类的处理方法
            super().keyPressEvent(event)

    def fill_current_cell(self):
        # 获取当前选中的单元格
        current_cell = self.table.currentItem()
        if current_cell is not None:
            # 填充当前单元格
            current_cell.setText("")
            current_cell.setText("■")
            current_cell.setFont(QFont("Arial", 40, QFont.Bold))
            current_cell.setTextAlignment(Qt.AlignCenter)
            current_cell.setForeground(QBrush(Qt.magenta))


    def cross_current_cell(self):
        # 获取当前选中的单元格
        current_cell = self.table.currentItem()
        if current_cell is not None:
            # 填充当前单元格
            current_cell.setText("")
            current_cell.setText("x")
            current_cell.setFont(QFont("Arial", 35, QFont.Bold))
            current_cell.setTextAlignment(Qt.AlignCenter)

    def play_screen(self, size):

        self.clear_layout()
        palette = QPalette()
        play = QPixmap()
        play.loadFromData(base64.b64decode(play_png))
        palette.setBrush(QPalette.Background, QBrush(play))
        self.setPalette(palette) 
        self.map = Map(size)  # 假设Map类适用于PyQt5
        self.current_play_size = size
        # 创建表格
        self.table = QTableWidget(self)
        self.table.setRowCount(size+1)  # 设置行数
        self.table.setColumnCount(size+1)  # 设置列数

        self.table.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.table.verticalHeader().setVisible(False)  # 隐藏垂直表头

        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # # 为第一行和第一列设置固定大小
        # fixedSize = 100  # 你希望的固定大小
        # self.table.setColumnWidth(0, fixedSize)  # 为第一列设置固定宽度
        # self.table.setRowHeight(0, fixedSize)  # 为第一行设置固定高度
        
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
            self.table.setColumnWidth(i, 50)  # 设置列宽为100像素
            self.table.setRowHeight(i, 50)  # 设置行高为50像素

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
                self.table.setItem(i, j, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        # self.table.itemChanged.connect(self.check_table)

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
        back_button.clicked.connect(self.show_choose_mode_screen)
        # 创建三个按钮
        to_be_known_button = QPushButton("游戏说明", self)
        to_be_known_button.setStyleSheet("""
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
        submit_button.setText("Submit")

        # 为按钮添加点击事件
        submit_button.clicked.connect(self.check_result)

        to_be_known_button.clicked.connect(self.show_to_be_known_screen)
        # submit_button.clicked.connect(cross_current_cell)

        # 创建一个水平布局
        hbox = QHBoxLayout()

        # 添加一个弹性空间到布局的开始，推动后面的内容到右侧
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将三个按钮添加到水平布局中
        hbox.addWidget(to_be_known_button)
        # 在按钮之间添加弹性空间
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addWidget(submit_button)
        # 再次添加弹性空间
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addWidget(back_button)

        # 添加一个弹性空间到布局的末尾，以确保按钮等间隔排列
        hbox.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将水平布局添加到主布局的底部
        self.layout.addLayout(hbox)

    def show_to_be_known_screen(self):
        self.clear_layout()
        palette = QPalette()
        to_be_known = QPixmap()
        to_be_known.loadFromData(base64.b64decode(to_be_known_png))

        palette.setBrush(QPalette.Background, QBrush(to_be_known.scaled(self.width, self.height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)))
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
        1. 请不要放大窗口，那样可能会导致无法预料的后果。\n
        2. 在游戏中，请不要双击单元格，那样可能会导致无法预料的后果。\n
        3. 游戏过程中请不要退出或进入其他页面，那样你会丢失你的进度。\n
        4. 鼠标左键单击单元格，再按下键盘上的"ctrl"键，以填充单元格。\n
        5. 鼠标左键单击单元格，再按下键盘上的"alt"键，以在单元格上画叉。\n
        6. 如在游戏中发现任何问题，请联系开发人员，你的意见对我们十分重要！\n
            开发人员微信：cauchy_stay_with_you\n
        7. 后续版本更新将会同步到github上，欢迎大家关注！
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
        back_button.clicked.connect(lambda: self.play_screen(self.current_play_size))

        self.layout.addWidget(back_button)

    def check_result(self):
        if self.is_finished():
            self.show_win_screen()

    def is_finished(self):
        for i in range(self.current_play_size):
            for j in range(self.current_play_size):
                if self.map.map[i][j] == 1 and self.table.item(i+1, j+1).text() != "■":
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


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())