import sys
import pathlib
import generator_func
import generator_logging
from datetime import datetime

from PyQt6.QtCore import QRunnable, QThreadPool, QDateTime, QSettings
from PyQt6.QtWidgets import (QApplication,
                             QDateTimeEdit,
                             QLabel,
                             QMainWindow,
                             QPushButton,
                             QWidget,
                             QFileDialog,
                             QGridLayout,
                             QLineEdit,
                             QComboBox,
                             QProgressBar,
                             QStatusBar,
                             QSpinBox,
                             QTableWidget,
                             QTableWidgetItem,
                             QMessageBox)
from PyQt6.QtGui import QIcon

MAXIMUM_IK_QUANTITY = 9999


class Worker(QRunnable):  # класс для мультипоточности???
    def run(self):  # мой код
        date_1 = win.date_1
        ed_date = date_1.toString('yyyy-MM-dd')
        req_date_time = date_1.toString('yyyy-MM-ddThh:mm:ssZ')
        path_for_ik = win.directory_path.currentText()  # в качестве пути для ИК берётся значение, указанное в ComboBox
        win.progressbar.setMaximum(win.ik_quantity.value())
        win.btn_create_IK.setEnabled(False)
        start = datetime.now()
        # aaa = generator_func.check_dir_emptiness(path_for_ik) # проверка каталога сохранения ИК на наличие файлов
        for i in range(win.ik_quantity.value()):
            generator_func.create_ik(path_for_ik, ed_date, req_date_time)
            win.progressbar.setValue(i + 1)
            win.status_bar.showMessage(f'Создано конвертов: {i + 1}')
        end = datetime.now()
        win.status_bar.showMessage(f'Создано конвертов: {win.ik_quantity.value()}. Затраченное время: {end - start}')
        generator_logging.log_event(f'Создано конвертов: {win.ik_quantity.value()}. Каталог: {path_for_ik}. '
                                    f'Затраченное время: {end - start}')
        win.btn_create_IK.setEnabled(True)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # Добавляем файл с настройками
        self.settings = QSettings('settings.ini', QSettings.Format.IniFormat)
        self.path_history = set()
        self.date_1 = ''
        self.setWindowTitle("Генератор ИК")  # заголовок главного окна
        self.setMinimumSize(500, 150)  # минимальные размеры главного окна
        self.get_directory_path = QPushButton('Выбрать каталог', self)
        self.get_directory_path.setFixedWidth(150)  # установка ширины кнопки
        # Определяем элементы интерфейса
        self.btn_create_IK = QPushButton('Создать конверты', self)
        self.ik_quantity_label = QLabel()
        self.calendar_label = QLabel()
        self.line_edit_for_combo = QLineEdit()
        self.directory_path = QComboBox()
        self.directory_path.setLineEdit(self.line_edit_for_combo)
        self.ik_quantity = QSpinBox()
        self.calendar = QDateTimeEdit()
        self.progressbar = QProgressBar()
        self.status_bar = QStatusBar()
        self.start_date = QDateTime.currentDateTime()
        self.calendar.setDisplayFormat('dd.MM.yyyy')
        self.ik_quantity.setMaximum(MAXIMUM_IK_QUANTITY)
        self.setMaximumWidth(1800)
        self.get_directory_path.clicked.connect(self.get_directory)
        self.btn_create_IK.clicked.connect(self.create_ik_func)
        self.ik_quantity.textChanged.connect(self.ik_quantity_signal)
        self.calendar.dateTimeChanged.connect(self.calendar_changed)
        self.calendar.setCalendarPopup(True)
        self.calendar.setDateTime(self.start_date)
        self.date_1 = self.calendar.dateTime()
        self.table = QTableWidget()
        self.table_widget_item = QTableWidgetItem()
        # размещение элементов
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_directory_path, 0, 0)
        grid_layout.addWidget(self.directory_path, 0, 1)
        grid_layout.addWidget(self.ik_quantity_label, 1, 0)
        grid_layout.addWidget(self.ik_quantity, 1, 1)
        grid_layout.addWidget(self.calendar_label, 2, 0)
        grid_layout.addWidget(self.calendar, 2, 1)
        grid_layout.addWidget(self.btn_create_IK, 3, 0, 1, 2)
        # grid_layout.addWidget(self.progressbar, 5, 0, 1, 2)
        grid_layout.addWidget(self.status_bar, 4, 0, 1, 2)
        widget = QWidget()
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
        self.ik_quantity_label.setText('Количество конвертов')
        self.calendar_label.setText('Дата ИК')
        self.btn_create_IK.setEnabled(False)
        # создание всплывающих подсказок для элементов интерфейса
        self.get_directory_path.setToolTip('Выберите каталог для сохранения ИК')
        self.directory_path.setToolTip('Можно вставить путь или выбрать с помощью кнопки')
        self.ik_quantity.setToolTip('Количество создаваемых конвертов')
        self.btn_create_IK.setToolTip('Введите количество создаваемых конвертов')
        self.calendar.setToolTip('Дата интеграционного конверта, дата заявки, дата выдачи кредита')
        self.status_bar.showMessage('')
        # self.table.cellClicked(0,0)
        # Что-то про многопоточность
        self.threadpool = QThreadPool()
        self.ik_quantity_label = ''
        self.iteration_count = ''
        # определение переменных для пути к каталогам и файлам
        self.start_path = pathlib.Path.cwd()
        self.envelope_path = self.start_path.joinpath('sample/envelope.xml')
        self.routeinfo_path = self.start_path.joinpath('sample/RouteInfo.xml')
        self.ed421_path = self.start_path.joinpath('sample/ED421.xml')
        self.line_edit_for_combo.setText(str(self.start_path))
        self.path_for_ik = self.start_path
        self.path_for_ik_str = str(self.path_for_ik)
        # подгонка ширины под длину пути к каталогу
        self.setMinimumWidth(int(len(str(self.start_path)) * 8.5))
        # импорт сохраненных настроек
        if self.settings.value('OD'):
            self.calendar.setDateTime(self.settings.value('OD'))
        else:
            self.date_1 = self.calendar.date()
        if self.settings.value('Path'):
            self.directory_path.addItems(self.settings.value('Path'))
            self.path_history = self.settings.value('Path')
        else:
            self.path_history = set()

    def get_directory(self):
        """
        Вызов диалогового окна для выбора каталога сохранения создаваемых конвертов
        :return:
        """
        self.path_for_ik = QFileDialog.getExistingDirectory(self, caption='Выбрать каталог сохранения',
                                                            directory=str(pathlib.Path.cwd()))
        self.path_for_ik_str = str(self.path_for_ik)
        self.line_edit_for_combo.setText(self.path_for_ik_str)
        self.setMinimumWidth(len(self.path_for_ik_str * 10))

    def create_ik_func(self):
        """
        Создание конвертов
        :return:
        """
        worker = Worker()  # делаем переменную на созданный класс FirstThread
        self.threadpool.start(worker)  # обращаемся к созданному классу FirstThread
        # добавление пути для ИК в выпадающий список
        if self.path_for_ik_str in self.path_history:
            pass
        elif self.path_for_ik_str not in self.path_history:
            self.path_history.add(self.path_for_ik_str)
            self.directory_path.addItem(self.path_for_ik_str)

    def ik_quantity_signal(self, value):
        """
        Определяет заполнено поле с количеством конвертов или нет и блокирует кнопку создания ИК
        :param value:
        :return:
        """
        if self.ik_quantity.value() == 0:
            self.btn_create_IK.setEnabled(False)
            self.btn_create_IK.setToolTip('Введите количество создаваемых конвертов')
        else:
            self.btn_create_IK.setEnabled(True)
            self.btn_create_IK.setToolTip('Создать конверты')

    def calendar_changed(self):
        self.date_1 = self.calendar.dateTime()

    def closeEvent(self, event):  # переопределение события закрытия окна
        self.settings.setValue('Path', self.path_history)  # Сохранить переменную с историей в файле с настройками
        self.settings.setValue('OD', self.date_1)  # Сохранить переменную с датой в файле с настройками


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
                width: 10px;
                /*margin: 0.5px;*/
            }
            """
    app.setStyleSheet(style)
    win = Window()
    app.setWindowIcon(QIcon(str(win.start_path.joinpath('other/hedgehog_deep_red.png'))))
    win.show()
    sys.exit(app.exec())
