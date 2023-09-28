from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
import requests
app = QApplication([])

window = QWidget()
window.setWindowTitle('Converter')
window.resize(300, 180)
window.show()

response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5')
data = response.json()



text1 = 'Исходная единица'
text2 = 'Целевая единица'
numb_text = 'Значение'

res_btn = QPushButton('Конвертировать')

number = QLineEdit('')

btn_lngth = QPushButton('Длина')
btn_mass = QPushButton('Масса')
btn_money = QPushButton('Валюта')

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
base_money = data[0]['base_ccy']
units_money = []
for i in range(len(data)):
    money = data[i-1]['ccy']
    units_money.append(money)
units_money.append(base_money)

units = units_length
for unit in units:
    units_start_box.addItem(unit)
    units_res_box.addItem(unit)

btns_line = QHBoxLayout()

btns_line.addWidget(btn_lngth)
btns_line.addWidget(btn_mass)
btns_line.addWidget(btn_money)


outer = QVBoxLayout()
outer.addLayout(btns_line)
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
    global units, units_res_box, units_start_box
    if units != units_money:
        units = units_money
        units_res_box.clear()
        units_start_box.clear()
        for unit in units:
            units_start_box.addItem(unit)
            units_res_box.addItem(unit)
def convert():
    global units, units_length, units_mass
    if units == units_length:
        convert_length()
    elif units == units_mass:
        convert_mass()
    elif units == units_money:
        convert_money()


btn_lngth.clicked.connect(change_length)
btn_mass.clicked.connect(change_mass)
btn_money.clicked.connect(change_money)
res_btn.clicked.connect(convert)


app.exec()