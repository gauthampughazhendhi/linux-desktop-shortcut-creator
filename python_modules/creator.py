import sys
import os
import subprocess
from PyQt5 import QtGui, QtCore, QtWidgets
from python_modules.creator_gui import Ui_MainWindow


class Creator(Ui_MainWindow):

    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.window = window
        self.setupUi(window)

        self.type.addItem('Application')
        self.type.addItem('Application in Terminal')

        self.label.setText(self.label.text() + '(Optional)')

        self.icon_button.clicked.connect(self.open_icon)
        self.exec_button.clicked.connect(self.open_exec)
        self.create.clicked.connect(self.create_shortcut)

    def open_icon(self):
        self.label_4.clear()
        icon_path = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Select Icon', '', 'images (*.png *.jpg)')
        self.icon_path.setText(icon_path[0])

    def open_exec(self):
        self.label_4.clear()
        exec_path = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Select Executable.')
        isexecutable = subprocess.getoutput("if [ -x " + exec_path[0] + " ]\nthen echo true\nfi")
        if isexecutable == "true":
            self.exec_path.setText(exec_path[0])
        else:
            self.label_4.setText('Please select an executable.')

    def create_shortcut(self):
        self.label_4.clear()
        app_type = str(self.type.currentText())
        name = str(self.app_name.text())
        icon_path = str(self.icon_path.text())
        exec_path = str(self.exec_path.text())

        if not app_type or not name or not exec_path:
            self.label_4.setText('Fill all the fields.')
        else:
            os.chdir('/usr/local/share/applications/')
            file = open(name+'.desktop', 'w')
            file.write('[Desktop Entry]\n')
            file.write('Type=Application\n')
            if app_type == 'Application':
                file.write('Terminal=false\n')
            else:
                file.write('Terminal=true\n')
            file.write('Name=' + name + '\n')
            file.write('Icon=' + icon_path + '\n')
            file.write('Exec=' + exec_path)
            file.close()

            self.label_4.setText('Shortcut created successfully.')
            self.app_name.clear()
            self.icon_path.clear()
            self.exec_path.clear()



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()

    c = Creator(w)
    w.setWindowTitle('Desktop Shortcut Creator')
    w.setFixedSize(350, 450)
    w.show()
    sys.exit(app.exec_())

