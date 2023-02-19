import sys
import os
import pathlib
import generator_func
from time import sleep
import random

from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, QThreadPool, QDate
from PyQt6.QtWidgets import (QApplication,
                             QDateTimeEdit,
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
        self.get_directory_path = QPushButton('Выбрать каталог', self)
        self.create_IK = QPushButton('Создать конверты', self)
        self.iteration_label = QLabel()
        self.calendar_label = QLabel()
        self.directory_path = QLineEdit()
        self.converts_quantity = QLineEdit()
        self.calendar = QDateTimeEdit()
        self.progressbar = QProgressBar()
        self.status_bar = QStatusBar()
        # self.start_date = QDate.setDate(2023, 1, 1)
        self.start_date = QDate.currentDate()
        print(self.start_date)

        self.get_directory_path.clicked.connect(self.get_directory)
        # написать функцию для созданию конвертов??? См. строка ниже
        self.create_IK.clicked.connect(self.create_ik_func)
        self.converts_quantity.textChanged.connect(self.line_edit_signal)
        self.calendar.setCalendarPopup(True)
        self.calendar.setMinimumDate(self.start_date)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_directory_path, 0, 0)
        grid_layout.addWidget(self.directory_path, 0, 1)
        grid_layout.addWidget(self.iteration_label, 1, 0)
        grid_layout.addWidget(self.converts_quantity, 1, 1)
        grid_layout.addWidget(self.calendar_label, 2, 0)
        grid_layout.addWidget(self.calendar, 2, 1)
        grid_layout.addWidget(self.create_IK, 3, 0, 1, 2)
        grid_layout.addWidget(self.progressbar, 4, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
        self.iteration_label.setText('Количество конвертов')
        self.calendar_label.setText('Дата ИК')
        self.create_IK.setEnabled(False)
        # создание всплывающих подсказок для элементов интерфейса
        self.get_directory_path.setToolTip('Выберите каталог для сохранения ИК')
        self.directory_path.setToolTip('Можно вставить путь или выбрать с помощью кнопки')
        self.converts_quantity.setToolTip('Количество создаваемых конвертов')
        self.create_IK.setToolTip('Введите количество создаваемых конвертов')
        self.calendar.setToolTip('Дата должна быть не ранее текущего ОД')
        self.status_bar.showMessage('Ghbdfsdf')
        # Что-то про многопоточность
        self.threadpool = QThreadPool()
        self.iteration_label = ''
        self.iteration_count = ''
        # определение переменных для пути к каталогам и файлам
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
        """
        Вызов диалогового окна для выбора каталога сохранения создаваемых конвертов
        :return:
        """
        self.start_path = QFileDialog.getExistingDirectory(self, caption='Выбрать каталог сохранения',
                                                           directory=str(pathlib.Path.cwd()))
        self.directory_path.setText(self.start_path)

        # size_status = len(self.directory_path.())
        # self.setMinimumWidth(size_status * 8)

    def create_ik_func(self):
        """
        Создание конвертов
        :return:
        """
        generator_func.create_ik(int(self.converts_quantity.text()))

    def line_edit_signal(self, value):
        """
        Определяет заполнено поле с количеством конвертов или нет и блокирует кнопку создания ИК
        :param value:
        :return:
        """
        if self.converts_quantity.text() == '':
            self.create_IK.setEnabled(False)
            self.create_IK.setToolTip('Введите количество создаваемых конвертов')
        else:
            self.create_IK.setEnabled(True)
            self.create_IK.setToolTip('Создать конверты')
            self.iteration_count = value

    def reportProgress(self, n):  # Это старое. Надо проверить
        self.stepLabel.setText(f"Long-Running Step: {n}")

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
                /*background-color: #fff;*/
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
# TODO: ограничить допустимые значения для поля с количеством конвертов (только целые числа)
# TODO: выяснить куда сохраняются ИК при выборе другой папки и где формируются временные каталоги
# TODO: зачем мы кладем ИК в каталог converts если был указан другой путь? Это неправильно. Но в то же время
#  надо подумать что делать если выбранный каталог уже не пустой. То есть, если сейчас убрать создание
#  подкаталога converts и складывать файлы в указанный каталог, то может возникнуть ситуация
#  когда ИК будут лежать вместе с другими файлами и тогда их неудобно удалять (например)
