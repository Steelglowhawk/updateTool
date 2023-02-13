import sys
import os
import generator
from time import sleep
import random

from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, QThreadPool
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QStatusBar
)


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    # get_dir = '/Users/steelhawk/PycharmProjects/UpdateTool/files'

    # def run(self):  # образец
    #     """Long-running task."""
    #     for i in range(5):
    #         sleep(1)
    #         self.progress.emit(i + 1)
    #     self.finished.emit()

    def run(self):  # мой код
        pass




class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()
        self.get_dir = '/Users/steelhawk/PycharmProjects/UpdateTool/files'

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)

        self.status = self.statusBar()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment((Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter))
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment((Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter))
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        self.button_file_dialog = QPushButton('Выберите ED421')  # кнопка для вызова окна выбора файла
        self.button_file_dialog.clicked.connect(self.get_ed)
        self.button_make_file = QPushButton()
        self.button_make_file.setText('Создать ИК')
        self.button_make_file.setToolTip('Создат заданное количество ИК')
        self.button_make_file.setDisabled(True)
        self.button_make_file.clicked.connect(self.path_to_file)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addWidget(self.button_file_dialog)
        layout.addWidget(self.button_make_file)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")


    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")

    def get_ed(self):
        get_ed421 = QFileDialog.getOpenFileName(self, caption='Выберите ED421', directory=os.getcwd())
        self.status.showMessage(f'Выбран файл: {get_ed421}')
        size_status = len(self.status.currentMessage())
        self.setMinimumWidth(size_status * 8)
        print(get_ed421)
        if get_ed421:
            print('Файл выбран')
            print(QFileDialog.fileSelected)
            print(f'Length of path is: {len(get_ed421)}')
            self.button_make_file.setDisabled(False)
        else:
            print('Файл не выбран')
            print(f'Length of path is: {len(get_ed421)}')
            self.button_make_file.setDisabled(True)
        self.get_dir = get_ed421
        print(f'self.get_dir from func is {self.get_dir}')

    def path_to_file(self):
        self.thread = QThread()
        self.worker_b = Worker()
        self.worker_b.moveToThread(self.thread)
        self.thread.started.connect(self.worker_b.run)  # вызов метода экзепляра класса Worker при старте потока
        self.worker_b.finished.connect(self.thread.quit)
        self.worker_b.finished.connect(self.worker_b.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker_b.progress.connect(self.reportProgress)
        self.thread.start()
        # if self.get_dir: # наверное надо перенести в Worker
        #     work_with_file.make_file(self.get_dir)
        #     self.label_get_dir.setText(f'File "{work_with_file.file_name}" created at the {self.get_dir}')
        # else:
        #     self.label_get_dir.setText('Directory for copying is not selected yet')

    def runLongTask(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)  # вызов метода экзепляра класса Worker при старте потока
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()
        self.thread.setPriority(QThread.Priority.LowPriority)  # приоритет процесса
        print(self.thread.priority())

        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

# TODO: поместить в строку со статусом время выполнения операции
