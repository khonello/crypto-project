from PyQt5 import QtGui
from PyQt5.QtCore import (
    Qt,
    QMargins,
)
from PyQt5.QtGui import (
    QFont,
    QPixmap,
    QIcon,
    QIntValidator,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QLabel,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QMenu,
    QVBoxLayout,
    QFrame,
    QSplitter,
    QCheckBox,
    QComboBox,
    QButtonGroup,
    QDialog,
    QMessageBox,
    QFileDialog,
    QSplashScreen,
    QScrollArea,
)

from sys import (
    argv,
    exit
)

from bitcoinlib.keys import Key 
from bitcoinlib.mnemonic import Mnemonic

from concurrent.futures import Executor


app = QApplication(argv)
app.setStyle("Fusion")

clipboard = app.clipboard()

class ProjectWindow(QMainWindow):

    main_layout = QVBoxLayout()
    main_widget = QWidget()
    generated = 0

    def __init__(self, parent: QWidget= None, flags= None):
        super().__init__(parent, flags)
        self.setStyleSheet(
            '''
            QMainWindow{
                background-color: #2B2A2A;
            }
            '''
        )
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon('icon/icon.ico'))
        self.resize(720, 410)
        self.set_title()
        self.splitter()
        self.data = dict(
            public_key= [],
            recorvery_phrase= []
        )

        self.main_layout.addStretch(1)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def mouseDoubleClickEvent(self, a0):

        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

        a0.accept()

    def mousePressEvent(self, a0):

        if a0.buttons() == Qt.LeftButton:

            self.drag_position = a0.globalPos() - self.frameGeometry().topLeft()
            a0.accept()
        

    def mouseMoveEvent(self, a0):
        if a0.buttons() == Qt.LeftButton:
            if hasattr(self, 'drag_position'):
                self.move(a0.globalPos() - self.drag_position)
                a0.accept()

    def splitter(self):

        def generate_func(*args):

            def compute_key(*args):

                if not args[0]:
                    
                    key = Key().address()
                else:
                    key = Key(private_key_lineedit.text()).address()

                return key

            def compute_phrase(*args):
                
                return str

            num_of_repetitions = 1
            if length:=len(repetition.text()) >= 1:

                num_of_repetitions = int(repetition.text())
                repetition.setText("")

            if check_box1.isChecked():
                
                    if len(private_key_lineedit.text()) == 0:
                        self.data["public_key"] += [
                                compute_key(False) for _ in range(num_of_repetitions)
                        ]
                    else:
                            from bitcoin import is_privkey
                            if is_privkey(private_key_lineedit.text()):

                                self.data["public_key"] += [
                                    compute_key(True) for _ in range(num_of_repetitions)
                                ]
                            else: 
                                QMessageBox.warning(self, "Private Key", "Private key is invalid")
                                private_key_lineedit.setText("")
            
            if check_box2.isChecked():
                mnemonic = Mnemonic()

                self.data["recorvery_phrase"] += [
                    mnemonic.generate() for _ in range(num_of_repetitions)
                ]

            if self.data:

                self.key_string = ""

                if keys:=self.data.get("public_key"):

                    self.key_string = "\n".join(keys)

                    keys_content.setText(self.key_string)
                    keys_content.adjustSize()
                    scroll_area_key_widget.adjustSize()
                
                if phrases:=self.data.get("recorvery_phrase"):

                    self.phrase_string = ""
                    for phrase in phrases:

                        elements = phrase.split()

                        formatted_string = "\n".join(" ".join(elements[i:i+6]) for i in range(0, len(elements), 6))
                        formatted_string += "\n\n"

                        self.phrase_string += formatted_string

                    phrase_content.setText(self.phrase_string)
                    phrase_content.adjustSize()
                    scroll_area_phrase_widget.adjustSize()
        
        left_parent_frame = QFrame()
        left_parent_frame_layout = QVBoxLayout()

        left_frame_top = QFrame()
        left_frame_top_layout = QVBoxLayout()

        left_frame_bottom = QFrame()
        left_frame_bottom_layout = QVBoxLayout()
        
        left_frame_top.setFrameShape(QFrame.Shape.Box)
        left_frame_top.setLineWidth(1)
        left_frame_top.setFrameShadow(QFrame.Shadow.Raised)
        left_frame_top.setStyleSheet(
            '''
            QFrame{
                border-radius: 10px;
                background-color: #3D3B3B;
                margin-right: 2px;
                margin-bottom: 5px;
            }
            '''
        )

        left_frame_bottom.setFrameShape(QFrame.Shape.Box)
        left_frame_bottom.setLineWidth(1)
        left_frame_bottom.setFrameShadow(QFrame.Shadow.Raised)
        left_frame_bottom.setStyleSheet(
            '''
            QFrame{
                border-radius: 10px;
                background-color: #3D3B3B;
                margin-right: 2px;
                margin-bottom: 5px;
            }
            '''
        )
        
        left_frame_top.setLayout(left_frame_top_layout)
        left_frame_bottom.setLayout(left_frame_bottom_layout)
        
        def for_combobox(arg):

            if arg != 0:
                QMessageBox.warning(self, "Warning", "Only Bitcoin is supported")
                combo_box.setCurrentIndex(0)

        combo_box = QComboBox()
        combo_box.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        combo_box.addItems(["Bitcoin", "Etherum", "Dodgecoin"])
        combo_box.currentIndexChanged.connect(for_combobox)
        combo_box.setStyleSheet(
            '''
                QComboBox QAbstractItemView{
                margin: 0px;
            }
                QComboBox::editable{
                background: white;
            }
            '''
        )    

        button_group = QButtonGroup()
        
        check_box1 = QCheckBox()
        check_box2 = QCheckBox()
        
        button_group.addButton(check_box1, 1)
        button_group.addButton(check_box2, 2)
        
        button_group.setExclusive(False)

        check_boxes_layout = QVBoxLayout()

        check_boxes_layout.addSpacing(10)
        check_boxes_layout.addWidget(check_box1)
        check_boxes_layout.addWidget(check_box2)

        check_box1.setText("Public Key")
        check_box2.setText("Recovery Phrase")

        left_frame_top_layout.addWidget(combo_box)
        left_frame_top_layout.addLayout(check_boxes_layout)
        

        repetition = QLineEdit()
        repetition.setPlaceholderText("Number of Repetitions")
        repetition.setValidator(QIntValidator())

        private_key_lineedit = QLineEdit()
        private_key_lineedit.setPlaceholderText("Provide private key")

        generate_label = QLabel()
        generate_label.setText("Generate")
        generate_label.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_label.setFixedWidth(60)
        generate_label.setStyleSheet(
            '''
            QLabel{
                color: white;
                background-color: green;
                border-radius: 4px;
                padding-top: 2px;
                padding-bottom: 4px;
                padding-left: 4px;
            }
            '''
        )

        generate_label.mousePressEvent = generate_func

        left_frame_bottom_layout.addWidget(repetition)
        left_frame_bottom_layout.addWidget(private_key_lineedit)

        left_frame_bottom_layout.addSpacing(5)
        left_frame_bottom_layout.addWidget(generate_label)
        left_frame_bottom_layout.addStretch(1)

        left_parent_frame_layout.addWidget(left_frame_top)
        left_parent_frame_layout.addWidget(left_frame_bottom)
        left_parent_frame.setLayout(left_parent_frame_layout)
        

        right_frame_parent = QFrame()
        right_frame_parent_layout = QHBoxLayout()

        right_frame_left = QFrame()
        right_frame_right = QFrame()

        right_frame_left.setFrameShape(QFrame.Shape.Box)
        right_frame_left.setFrameShadow(QFrame.Shadow.Raised)
        right_frame_left.setStyleSheet(
            '''
            QFrame{
                border-radius: 10px;
                background-color: #585656;
                margin-left: 8px;
                margin-top: 8px;
                margin-right: 10px;
                margin-bottom: 8px;
            }
            '''
        )
        
        right_frame_right.setFrameShape(QFrame.Shape.Box)
        right_frame_right.setFrameShadow(QFrame.Shadow.Raised)
        right_frame_right.setStyleSheet(
            '''
            QFrame{
                border-radius: 10px;
                background-color: #585656;
                margin-left: 8px;
                margin-top: 8px;
                margin-right: 10px;
                margin-bottom: 8px;
            }
            '''
        )

        right_frame_left_layout = QVBoxLayout()
        right_frame_right_layout = QVBoxLayout()

        right_frame_left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        right_frame_right_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        keys_label = QLabel("Public Keys")
        phrase_label = QLabel("Recovery Phrase")

        keys_content = QLabel()
        phrase_content = QLabel()

        keys_content.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        phrase_content.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        keys_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        phrase_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        keys_content.setAlignment(Qt.AlignmentFlag.AlignTop)
        phrase_content.setAlignment(Qt.AlignmentFlag.AlignTop)

        keys_label.setFont(QFont("Arial", 12, 7, italic= False))
        keys_label.setStyleSheet(
            '''
            QLabel{
                margin-bottom: 5px;
            }
            '''
        )
        phrase_label.setFont(QFont("Arial", 12, 7, italic= False))
        phrase_label.setStyleSheet(
            '''
            QLabel{
                margin-bottom: 5px;
            }
            '''
        )

        scroll_area_key = QScrollArea()
        scroll_area_phrase = QScrollArea()

        scroll_area_key.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area_key.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area_key.setStyleSheet(
            '''
            QScrollArea{
                background-color: #585656;
            }
            QScrollBar{
                background-color: #585656;
            }
            QScrollBar:vertical{
                width: 7px;
            }
            QScrollBar::handle:vertical{
                border: 1px solid white;
                border-radius: 2px;
            }
            QScrollBar::sub-line:vertical{
                image: "";
            }
            QScrollBar::add-line:vertical{
                image: "";
            }
            '''
        )

        scroll_area_phrase.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area_phrase.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area_phrase.setStyleSheet(
            '''
            QScrollArea{
                background-color: #585656;
            }
            QScrollBar{
                background-color: #585656;
            }
            QScrollBar:vertical{
                width: 7px;
            }
            QScrollBar::handle:vertical{
                border: 1px solid white;
                border-radius: 2px;
            }
            QScrollBar::sub-line:vertical{
                image: "";
            }
            QScrollBar::add-line:vertical{
                image: "";
            }
            '''
        )

        scroll_area_key_widget = QWidget()
        scroll_area_phrase_widget = QWidget()

        scroll_area_key_widget.setStyleSheet(
            '''
            QWidget{
                margin-left: 0px;
                background-color: #585656;
            }
            '''
        )
        scroll_area_phrase_widget.setStyleSheet(
            '''
            QWidget{
                margin-left: 0px;
                background-color: #585656;
            }
            '''
        )

        scroll_area_key_widget.setMinimumSize(180, 170)
        scroll_area_phrase_widget.setMinimumSize(180, 170)

        scroll_area_key_layout = QVBoxLayout()
        scroll_area_phrase_layout = QVBoxLayout()

        right_frame_left_layout.addWidget(keys_label)
        right_frame_left_layout.addWidget(scroll_area_key)

        right_frame_right_layout.addWidget(phrase_label)
        right_frame_right_layout.addWidget(scroll_area_phrase)

        scroll_area_key_layout.addWidget(keys_content)
        scroll_area_phrase_layout.addWidget(phrase_content)

        scroll_area_key_widget.setLayout(scroll_area_key_layout)
        scroll_area_phrase_widget.setLayout(scroll_area_phrase_layout)

        scroll_area_key.setWidget(scroll_area_key_widget)
        scroll_area_phrase.setWidget(scroll_area_phrase_widget)

        right_frame_left.setLayout(right_frame_left_layout)
        right_frame_right.setLayout(right_frame_right_layout)

        right_frame_parent_layout.addWidget(right_frame_left)
        right_frame_parent_layout.addWidget(right_frame_right)
        right_frame_parent.setLayout(right_frame_parent_layout)

        right_frame_parent.setFrameShape(QFrame.Shape.Box)
        right_frame_parent.setLineWidth(1)
        right_frame_parent.setFrameShadow(QFrame.Shadow.Raised)
        right_frame_parent.setStyleSheet(
            '''
            QFrame{
                border-radius: 10px;
                background-color: #3D3B3B;
                margin-left: 8px;
                margin-top: 8px;
                margin-right: 10px;
            }
            '''
        )


        splitter_widget = QSplitter(Qt.Orientation.Horizontal)
        splitter_widget.setLineWidth(0)

        splitter_widget.addWidget(left_parent_frame)
        splitter_widget.addWidget(right_frame_parent)
        splitter_widget.setHandleWidth(2)
        # splitter_widget.splitterMoved.connect(lambda *args: print(args))

        splitter_widget.setStyleSheet(
            '''
            QSplitter::handle{
                background-color: #333;
            }
            '''
        )

        splitter_layout = QHBoxLayout()
        splitter_layout.addWidget(splitter_widget)

        footer_frame_layout = QHBoxLayout()
        footer_frame_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        def copy(*args):
            
                data = ""
                if hasattr(self, "key_string"):

                    data += f'Public Key:\n{self.key_string}\n\n'
                if hasattr(self, "phrase_string"):

                    data += f"Recovery Phrase:\n{self.phrase_string}"
                if not data:
                
                    QMessageBox.warning(self, "Clipboard", "No data is available", QMessageBox.StandardButton.Close)
                else:
                    
                    clipboard.setText(data)
                    QMessageBox.information(self, "Clipboard", "Clipboard data has been set", QMessageBox.StandardButton.Close)

        clipboard_label = QLabel("Copy")
        clipboard_label.setCursor(Qt.CursorShape.PointingHandCursor)
        clipboard_label.mousePressEvent = lambda *args: copy()
        clipboard_label.setStyleSheet(
            '''
            QLabel{
                margin-top: 1px;
                margin-right: 5px;
                padding-top: 2px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 2px;
                background-color: #585656;
                border-radius: 4px;
            }
            '''
        )

        def save(*args):

            if self.data["public_key"] or self.data["recorvery_phrase"]:

                if text_list:=self.data["public_key"]:

                    text = "\n".join(text_list)
                    data = bytes(text, encoding= "utf-8", errors= "ignore")

                    QFileDialog.saveFileContent(data, "public_key.txt")
                
                if text_list:=self.data["recorvery_phrase"]:
                    
                    data = bytes(self.phrase_string, encoding= "utf-8", errors= "ignore")
                    QFileDialog.saveFileContent(data, "recovery_phrase.txt")
                
            else:
                QMessageBox.warning(self, "Save", "No data to save", QMessageBox.StandardButton.Close)

        save_label = QLabel("Save")
        save_label.setCursor(Qt.CursorShape.PointingHandCursor)
        save_label.mousePressEvent = lambda *args: save()
        save_label.setStyleSheet(
            '''
            QLabel{
                margin-top: 1px;
                margin-right: 5px;
                padding-top: 2px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 2px;
                background-color: #54BAC0;
                border-radius: 4px;
            }
            '''
        )

        footer_frame_layout.addWidget(clipboard_label)
        footer_frame_layout.addWidget(save_label)

        self.main_layout.addLayout(footer_frame_layout)
        self.main_layout.addLayout(splitter_layout)


    def set_title(self):

        title = QLabel()
        title.setText("engine")
        title.setFont(QFont("Gadugi 13 Bold", 35, 16, False))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setContentsMargins(QMargins(0, 10, 0, 5))


        image = QPixmap("img/title_image.png")
        image_label = QLabel()
        image_label.setPixmap(image)

        label_layout = QHBoxLayout()
        label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_layout.addWidget(title)
        label_layout.addWidget(image_label)

        self.main_layout.addLayout(label_layout)

def main():

    main_window = ProjectWindow(flags= Qt.WindowType.FramelessWindowHint)
    
    image = QPixmap('img/splash.png')
    splashscreen = QSplashScreen(image, Qt.WindowType.WindowStaysOnTopHint)
    splashscreen.show()

    popup_menu = QMenu()

    maximize_action = QAction('Maximize')
    minimize_action = QAction('Minimize')
    resize_action = QAction('Restore')
    close_action = QAction('Close')
    close_action.setToolTip('Exit program')

    action_separator = popup_menu.addSeparator()

    popup_menu.addActions([maximize_action, minimize_action, resize_action, action_separator, close_action])
    popup_menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    popup_menu.setStyleSheet('''
    QMenu{
        border-radius: 7px;
        background-color: rgba(51, 51, 51, 0.8);
    }
    QMenu::item{
        background-color: rgba(51, 51, 51, 0.8);
    }
    QMenu::item:selected{
        background-color: rgba(92, 92, 92, 1);
    }
    '''
    )

    maximize_action.triggered.connect(lambda *args: main_window.showMaximized())
    minimize_action.triggered.connect(lambda *args: main_window.showMinimized())
    resize_action.triggered.connect(lambda *args: main_window.showNormal())
    close_action.triggered.connect(lambda *args: main_window.close())

    main_window.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    main_window.customContextMenuRequested.connect(lambda point: popup_menu.exec_(main_window.mapToGlobal(point)))

    __import__('time').sleep(2)

    main_window.show()
    splashscreen.finish(main_window)

    exit(app.exec_())

if __name__ == "__main__":
    main()