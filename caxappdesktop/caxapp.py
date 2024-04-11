import sys
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from pathlib import Path

from PyQt5 import QtCore, QtWidgets

from cax import format_csv_to_cax

root = tkinter.Tk()
root.withdraw()


class UiMain:

    def __init__(self):
        self.original_file = ''
        self.new_file = ''

    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(545, 398)
        Main.setAutoFillBackground(False)
        Main.setStyleSheet('font: 14pt "American Typewriter";\n'
                           'background-color: rgb(51, 51, 51);\n'
                           'background-repeat: no-repeat;\n')
        self.centralwidget = QtWidgets.QWidget(Main)
        self.centralwidget.setObjectName('centralwidget')
        self.csv_convert_textbox = QtWidgets.QLineEdit(self.centralwidget)
        self.csv_convert_textbox.setGeometry(QtCore.QRect(330, 150, 151, 31))
        self.csv_convert_textbox.setStyleSheet('color: rgb(182, 149, 80);\n'
                                               'background-color: rgb(255, 255, 255);\n')

        self.csv_convert_textbox.setObjectName('csv_convert_textbox')
        self.os_textbox = QtWidgets.QLineEdit(self.centralwidget)
        self.os_textbox.setGeometry(QtCore.QRect(330, 210, 151, 31))
        self.os_textbox.setStyleSheet('color: rgb(182, 149, 80);\n'
                                      'background-color: rgb(255, 255, 255);')
        self.os_textbox.setObjectName('os_textbox')
        self.convert_button = QtWidgets.QPushButton(self.centralwidget)

        # TODO button clicked
        self.convert_button.clicked.connect(self.convert)
        self.convert_button.setGeometry(QtCore.QRect(360, 299, 161, 41))
        self.convert_button.setStyleSheet('color:rgb(255, 255, 255);\n'
                                          'background-color: rgb(182, 149, 80);\n'
                                          'alternate-background-color: rgb(179, 179, 179);\n'
                                          'font: 17pt "Arial Black";')
        self.convert_button.setFlat(False)
        self.convert_button.setObjectName('convert_button')
        self.csv_label = QtWidgets.QLabel(self.centralwidget)
        self.csv_label.setGeometry(QtCore.QRect(220, 150, 101, 21))
        self.csv_label.setStyleSheet('color:rgb(255, 255, 255);\n'
                                     'font: 14pt "Arial";')
        self.csv_label.setObjectName('csv_label')
        self.os_label = QtWidgets.QLabel(self.centralwidget)
        self.os_label.setGeometry(QtCore.QRect(200, 210, 121, 21))
        self.os_label.setStyleSheet('color:rgb(255, 255, 255);\n'
                                    'font: 14pt "Arial";')
        self.os_label.setObjectName('os_label')
        self.img_label = QtWidgets.QLabel(self.centralwidget)
        self.img_label.setGeometry(QtCore.QRect(10, -10, 200, 200))
        my_button = self.img_label
        image_path = Path(__file__) / 'img' / '200x200Vssta.png'
        my_button.setStyleSheet(f'background-image: url(\'{image_path.absolute()}\');\n'
                                'background-repeat: no-repeat')
        self.os_label.setObjectName('os_label')
        self.version_label = QtWidgets.QLabel(self.centralwidget)
        self.version_label.setGeometry(QtCore.QRect(10, 355, 111, 16))
        self.version_label.setStyleSheet('color: rgb(255, 255, 255);\n'
                                         'font: 15pt \"Arial\";')
        self.version_label.setObjectName('version_label')
        self.csv_file_button = QtWidgets.QToolButton(self.centralwidget)
        self.csv_file_button.setGeometry(QtCore.QRect(490, 158, 26, 22))
        self.csv_file_button.setStyleSheet('background-color: rgb(173, 131, 51);')
        self.csv_file_button.setObjectName('csv_file_button')
        self.csv_file_button.clicked.connect(self.openfile)
        self.os_button = QtWidgets.QToolButton(self.centralwidget)
        self.os_button.setGeometry(QtCore.QRect(490, 213, 26, 22))
        self.os_button.setStyleSheet('background-color: rgb(173, 131, 51);')
        self.os_button.setObjectName('os_button')
        self.os_button.clicked.connect(self.save_as)

        Main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 22))
        self.menubar.setObjectName('menubar')
        Main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Main)
        self.statusbar.setObjectName('statusbar')
        Main.setStatusBar(self.statusbar)

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate('Main', 'Cax Builder'))
        self.convert_button.setText(_translate('Main', 'Convert'))
        self.csv_label.setText(_translate('Main', 'CSV to Convert'))
        self.img_label.setText(_translate('Main', ''))
        # self.img_label.setPixmap(QtGui.QPixmap(':/Users/bobbybeason/MEGAsync/autorun/caxbuilder/bg.png'))
        self.os_label.setText(_translate('Main', 'Operating System'))
        self.version_label.setText(_translate('Main', 'Cax Builder v2.1'))
        self.csv_file_button.setText(_translate('Main', '...'))
        self.os_button.setText(_translate('Main', '...'))

    def openfile(self):
        print('Select the file you want to convert')
        # Set file to be converted with askopen file
        # Allow user to select the file they want to convert
        self.original_file = tkinter.filedialog.askopenfilename()
        self.csv_convert_textbox.setText(self.original_file)

    def save_as(self):
        # this is the name of the file to save as
        # set file save as the new file after converting
        self.new_file = tkinter.filedialog.asksaveasfilename()
        print(self.new_file)
        self.os_textbox.setText(self.new_file)

    def convert(self):
        format_csv_to_cax(self.original_file, self.new_file)
        print('completed conversion')
        self.os_textbox.setText('')
        self.csv_convert_textbox.setText('')
        tkinter.messagebox.showinfo(title='Converter', message='File Conversion Complete')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMain()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
