from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
import requests
app = QApplication([])

window = QWidget()
window.setWindowTitle('Converter')
window.resize(300, 180)
window.show()
try:
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5')
    data = response.json()
    base_money = data[0]['base_ccy']
    units_money = []
    for i in range(len(data)):
        money = data[i-1]['ccy']
        units_money.append(money)
    units_money.append(base_money)

except:
    print(123)

units_custom_1_text = list()
units_custom_1_num = list()
text1 = 'Исходная единица'
text2 = 'Целевая единица'
numb_text = 'Значение'

res_btn = QPushButton('Конвертировать')

number = QLineEdit('')

btn_lngth = QPushButton('Длина')
btn_mass = QPushButton('Масса')
btn_money = QPushButton('Валюта')

btn_empty_1 = QPushButton('Добавить\Убрать')
btn_empty_2 = QPushButton('...')



text1_txt = QLabel(text1)
text2_txt = QLabel(text2)
numb_txt = QLabel(numb_text)
unit_start = QLabel('')
unit_res = QLabel('')
res_window = QMessageBox()

units_start_box = QComboBox()
units_res_box = QComboBox()

units_mass = ["Тонны (t)", "Английские тонны (t)", "Американские тонны (t)", "фунты (lb)", "Унции (oz)", "Килограммы (kg)", "Граммы (g)"]
units_length = ["километры (km)", "метры (m)", "сантиметры (cm)", "миллиметры (mm)", "Дюймы (in)", "футы (ft)", "ярды (yd)"]
units = units_length
for unit in units:
    units_start_box.addItem(unit)
    units_res_box.addItem(unit)

btns_line_1 = QHBoxLayout()

btns_line_1.addWidget(btn_lngth)
btns_line_1.addWidget(btn_mass)
btns_line_1.addWidget(btn_money)

btns_line_2 = QHBoxLayout()

btns_line_2.addWidget(btn_empty_1)
btns_line_2.addWidget(btn_empty_2)



outer = QVBoxLayout()
outer.addLayout(btns_line_1)
outer.addLayout(btns_line_2)
outer.addWidget(text1_txt)
outer.addWidget(units_start_box, alignment= Qt.AlignTop)
outer.addWidget(text2_txt)
outer.addWidget(units_res_box)
outer.addWidget(numb_txt)
outer.addWidget(number)
outer.addWidget(res_btn)

window.setLayout(outer)

def convert_mass():
    global units_res_box, units_start_box
    num = int(number.text())
    unit1 = units_start_box.currentText()
    if unit1 == 'Тонны (t)':
        num *= 1000
    elif unit1 == 'Английские тонны (t)':
        num *= 1016.0469088
    elif unit1 == 'Американские тонны (t)':
        num *= 907.18474
    elif unit1 == 'фунты (lb)':
        num *= 0.45359237
    elif unit1 == 'Унции (oz)':
        num *= 0.0283495231
    elif unit1 == 'Граммы (g)':
        num /= 1000
    unit2 = units_res_box.currentText()
    if unit2 == 'Тонны (t)':
        num /= 1000
    elif unit2 == 'Английские тонны (t)':
        num /= 1016.0469088
    elif unit2 == 'Американские тонны (t)':
        num /= 907.18474
    elif unit2 == 'фунты (lb)':
        num /= 0.45359237
    elif unit2 == 'Унции (oz)':
        num /= 0.0283495231
    elif unit2 == 'Граммы (g)':
        num *= 1000
    res_window.setText(str(num))
    res_window.exec()

def convert_length():
    global units_res_box, units_start_box
    num = int(number.text())
    unit1 = units_start_box.currentText()
    if unit1 == 'километры (km)':
        num *= 100000
    elif unit1 == 'метры (m)':
        num *= 100
    elif unit1 == 'миллиметры (mm)':
        num /= 100
    elif unit1 == 'Дюймы (in)':
        num *= 2.54
    elif unit1 == 'футы (ft)':
        num *= 30.48
    elif unit1 == 'ярды (yd)':
        num *= 91.44
    unit2 = units_res_box.currentText()
    if unit2 == 'километры (km)':
        num /= 100000
    elif unit2 == 'метры (m)':
        num /= 100
    elif unit2 == 'миллиметры (mm)':
        num *= 100
    elif unit1 == 'Дюймы (in)':
        num /= 2.54
    elif unit2 == 'футы (ft)':
        num /= 30.48
    elif unit2 == 'ярды (yd)':
        num /= 91.44
    res_window.setText(str(num))
    res_window.exec()

def convert_money():
    global units_res_box, units_start_box
    num = float(number.text())
    unit1 = units_start_box.currentText()
    if unit1 == 'EUR':
        num *= float(data[0]['buy'])
    elif unit1 == 'USD':
        num *= float(data[1]['buy'])
    unit2 = units_res_box.currentText()
    if unit2 == 'EUR':
        num /= float(data[0]['sale'])
    elif unit2 == 'USD':
        num /= float(data[1]['sale'])
    res_window.setText(str(num))
    res_window.exec()

def convert_custom():
    global units_res_box, units_start_box
    num = float(number.text())
    unit1 = units_start_box.currentText()
    ind1 = units_custom_1_text.index(unit1)
    if ind1 != 0:
        num1 = units_custom_1_num[ind1 - 1]
        num *= num1
    unit2 = units_res_box.currentText()
    ind2 = units_custom_1_text.index(unit2)
    if ind2 != 0:
        num2 = units_custom_1_num[ind2- 1]
        num /= num2
    res_window.setText(str(num))
    res_window.exec()



def change_length():
    global units, units_res_box, units_start_box
    if units != units_length:
        units = units_length
        units_res_box.clear()
        units_start_box.clear()
        for unit in units:
            units_start_box.addItem(unit)
            units_res_box.addItem(unit)

def change_mass():
    global units, units_res_box, units_start_box
    if units != units_mass:
        units = units_mass
        units_res_box.clear()
        units_start_box.clear()
        for unit in units:
            units_start_box.addItem(unit)
            units_res_box.addItem(unit)

def change_money():
    try:
        global units, units_res_box, units_start_box
        if units != units_money:
            units = units_money
            units_res_box.clear()
            units_start_box.clear()
            for unit in units:
                units_start_box.addItem(unit)
                units_res_box.addItem(unit)
    except:
        res_window.setText('ОЙ! Возникли проблемы с соединением с сервером. \n провертье подключение к сети')
        res_window.exec()

def change_custom_1():
    try:
        global units, units_res_box, units_start_box, units_custom_1_num, units_custom_1_text, units_custom_1
        f = open('1.txt', 'r')
        units_custom_1 = (f.read()).split()
        if units != units_custom_1:
            units = units_custom_1
            units_res_box.clear()
            units_start_box.clear()
            for unit in units_custom_1:
                try:
                    unit = float(unit)
                    units_custom_1_num.append(unit)
                except:
                    units_custom_1_text.append(unit)
                    units_start_box.addItem(unit)
                    units_res_box.addItem(unit)
    except:
        ...

def add_text():
    a = units_ask_1.text()
    b = units_ask_2.text()
    c = units_ask_3.text()
    
    if a not in res:
        res.append(str(a))
    if b not in res:
        res.append(str(b))
        res.append(c)
    res_window.setText(f'Успешно добавлено значение \n {c} {a} = {b}')
    res_window.exec()


def add_close():
    print(res)
    for unit in res:
        f.write(unit + ' ')
    f.close()
    window_ask.hide()
    window_add.hide()

def add():
    global window_add, units_ask_1, f, units_ask_2, units_ask_3, res
    window_ask_add.hide()
    with open('1.txt', 'w+') as f:
        f.write('')

    f = open('1.txt', 'w+')

    res = list()
    window_add = QWidget()
    window_add.setWindowTitle('Добавить единицу измерения')
    window_add.resize(300, 180)
    window_add.show()

    text1 = 'Исходное значение, то к чему все будет приводиться'
    text2 = 'Начальное значение, то от чего все будет приводиться'
    text3 = 'Значение'

    text1_txt = QLabel(text1)
    text2_txt = QLabel(text2)
    text3_txt = QLabel(text3)

    units_ask_1 = QLineEdit()
    units_ask_1.setPlaceholderText('Килограммы (kg)')

    units_ask_2 = QLineEdit()
    units_ask_2.setPlaceholderText('Тонны (t)')

    units_ask_3 = QLineEdit()
    units_ask_3.setPlaceholderText('1000')

    btn_add_1 = QPushButton("Добавить")
    btn_add_2 = QPushButton('Завершить')

    btns_line_3 = QHBoxLayout()

    btns_line_3.addWidget(btn_add_1)
    btns_line_3.addWidget(btn_add_2)

    Line = QVBoxLayout()

    Line.addWidget(text1_txt)
    Line.addWidget(units_ask_1)
    Line.addWidget(text2_txt)
    Line.addWidget(units_ask_2)
    Line.addWidget(text3_txt)
    Line.addWidget(units_ask_3)
    Line.addLayout(btns_line_3)
    
    btn_add_1.clicked.connect(add_text)
    btn_add_2.clicked.connect(check_close)
    window_add.setLayout(Line)

def check_close():
    global window_ask
    window_ask = QWidget()
    window_ask.setWindowTitle('Добавить единицу измерения')
    window_ask.resize(300, 80)
    window_ask.show()
    btn_ask_1 = QPushButton("да")
    btn_ask_2 = QPushButton('нет')
    asking = 'Уверены что хотите завершить?'
    asking_txt = QLabel(asking)
    btns_line_4 = QHBoxLayout()

    btns_line_4.addWidget(btn_ask_1)
    btns_line_4.addWidget(btn_ask_2)

    Line = QVBoxLayout()
    Line.addWidget(asking_txt)
    Line.addLayout(btns_line_4)
    window_ask.setLayout(Line)
    btn_ask_1.clicked.connect(add_close)
    btn_ask_2.clicked.connect(window_ask.hide)

def check_add():
    global window_ask_add
    window_ask_add = QWidget()
    window_ask_add.setWindowTitle('...')
    window_ask_add.resize(300, 80)
    window_ask_add.show()
    btn_ask_1 = QPushButton("да")
    btn_ask_2 = QPushButton('нет')
    asking = 'Уверены что хотите что хотите добавить? \n Если у вас есть сохранение, то они не удалятся'
    asking_txt = QLabel(asking)
    btns_line_4 = QHBoxLayout()

    btns_line_4.addWidget(btn_ask_1)
    btns_line_4.addWidget(btn_ask_2)

    Line = QVBoxLayout()
    Line.addWidget(asking_txt)
    Line.addLayout(btns_line_4)
    window_ask_add.setLayout(Line)
    btn_ask_1.clicked.connect(add)
    btn_ask_2.clicked.connect(window_ask_add.hide)


def convert():
    global units, units_length, units_mass, units_custom_1, units_money
    try:
        if units == units_length:
            convert_length()
        elif units == units_mass:
            convert_mass()
        elif units == units_money:
            convert_money()
        elif units == units_custom_1:
            convert_custom()
    except:
        res_window.setText('Неправильный ввод')
        res_window.exec()


btn_lngth.clicked.connect(change_length)
btn_mass.clicked.connect(change_mass)
btn_money.clicked.connect(change_money)
res_btn.clicked.connect(convert)
btn_empty_1.clicked.connect(check_add)
btn_empty_2.clicked.connect(change_custom_1)

app.exec()