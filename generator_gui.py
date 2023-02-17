import sys
import os
import pathlib
import generator_func
from time import sleep
import random

from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, QThreadPool
from PyQt6.QtWidgets import (QApplication,
                             QLabel,
                             QMainWindow,
                             QPushButton,
                             QVBoxLayout,
                             QWidget,
                             QFileDialog,
                             QGridLayout,
                             QLineEdit,
                             QProgressBar,
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
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Генератор ИК")  # заголовок главного окна
        self.setMinimumSize(400, 150)  # минимальные размеры главного окна
        self.get_directory_path = QPushButton('Выбор каталога', self)
        self.create_IK = QPushButton('Создать конверты', self)
        self.iteration_label = QLabel()
        self.date_label = QLabel()
        self.directory_path = QLineEdit()
        self.converts = QLineEdit()
        self.input_date = QLineEdit()
        self.progressbar = QProgressBar()
        self.get_directory_path.clicked.connect(self.get_directory)
        # написать функцию для созданию конвертов??? См. строка ниже
        # self.create_IK.clicked.connect(self.create_converts)
        self.converts.textChanged.connect(self.line_edit_signal)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_directory_path, 0, 0)
        grid_layout.addWidget(self.directory_path, 0, 1)
        grid_layout.addWidget(self.iteration_label, 1, 0)
        grid_layout.addWidget(self.converts, 1, 1)
        grid_layout.addWidget(self.date_label, 2, 0)
        grid_layout.addWidget(self.input_date, 2, 1)
        grid_layout.addWidget(self.create_IK, 3, 0, 1, 2)
        grid_layout.addWidget(self.progressbar, 4, 0, 1, 2)
        widget = QWidget()
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
        self.iteration_label.setText('Количество конвертов')
        self.date_label.setText('Введите дату')
        self.create_IK.setEnabled(False)
        self.get_directory_path.setToolTip('Выберите каталог для сохранения ИК')
        self.directory_path.setToolTip('Можно вставить путь или выбрать с помощью кнопки')
        self.converts.setToolTip('Количество необходимых конвертов')
        self.create_IK.setToolTip('Введите количество необходимых конвертов')
        self.input_date.setToolTip('Дата должна быть не ранее текущего ОД')
        self.threadpool = QThreadPool()
        self.iteration_label = ''
        self.iteration_count = ''
        # self.start_path = 'C:/install'
        self.start_path = pathlib.Path.cwd()
        self.envelope_path = self.start_path.joinpath('sample/envelope.xml')
        self.routeinfo_path = self.start_path.joinpath('sample/RouteInfo.xml')
        self.ed421_path = self.start_path.joinpath('sample/ED421.xml')
        self.directory_path.setText(str(self.start_path))

    '''Это от моего старого интерфейса
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
    '''

    def get_directory(self):
        self.start_path = QFileDialog.getExistingDirectory(self, caption='Выбрать файл', directory='C:/')
        self.directory_path.setText(self.start_path)


# зачем эта функция? Из шаблона Димы
    def line_edit_signal(self, value):
        if self.converts.text() == '':
            self.create_IK.setEnabled(False)
        else:
            self.create_IK.setEnabled(True)
            self.iteration_count = value

    def reportProgress(self, n):  # Это старое. Надо проверить
        self.stepLabel.setText(f"Long-Running Step: {n}")

    def get_ed(self):  # Это старое. Надо проверить
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

    def path_to_file(self):  # Это старое. Надо проверить
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

    def runLongTask(self):  # Это старое. Но это что-то от многопоточности
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
    style = """
            QMainWindow {
                /*background-color: Red;*/
            }
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
            """
    app.setStyleSheet(style)
    win = Window()
    win.show()
    sys.exit(app.exec())

# TODO: поместить в строку со статусом время выполнения операции
# TODO: что делает кнопка выбор каталога? Это каталог для сохранения ИК?
# TODO: адаптировать размер окна под длину текста в поле для ввода каталога
