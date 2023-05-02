import xml.etree.ElementTree as et
import tkinter as tk
from tkinter import filedialog


def get_xml(filepath):
    """Read xml file for continue manipulation"""
    tree = et.parse(filepath)
    root = tree.getroot()
    return root, tree


def create_dict(root, tree, file_path_save):
    """Collect items in list"""
    items_zap = root.findall('.//ZAP')
    logs_text.insert(tk.END, f"Число пациентов в пакете {len(items_zap)}\n")

    for item in items_zap:
        episod = item.find('./Z_SL/SL/NHISTORY').text
        logs_text.insert(tk.END, f"Эпизод № {episod}\n")
        items_sl = item.findall('./Z_SL/SL')

        for item in items_sl:
            ds1_element = item.find('./DS1')
            ds2_element = item.find('./DS2_N/DS2')
            ds3_element = item.find('./DS3')

            diagnose_1 = ds1_element.text if ds1_element is not None else "Not found"
            diagnose_2 = ds2_element.text if ds2_element is not None else "Not found 2 diagnose"
            diagnose_3 = ds3_element.text if ds3_element is not None else "Not found 3 diagnose"

            d2_list = item.findall('DS2_N')
            for index, ds2_n in enumerate(d2_list):
                if diagnose_1 == diagnose_2:
                    logs_text.insert(tk.END, f"Удален второй диагноз у эпизода {episod}\n")
                    item.remove(ds2_n)
                try:
                    ds2_element = d2_list[index + 1].find('DS2')
                except IndexError:
                    continue
                diagnose_2 = ds2_element.text if ds2_element is not None else "Not found 2 diagnose"

            d3_list = item.findall('DS3')
            for index, ds3_n in enumerate(d3_list):
                if diagnose_1 == diagnose_3:
                    logs_text.insert(tk.END, f"Удален третий диагноз у эпизода {episod}\n")
                    item.remove(ds3_n)
                try:
                    ds3_element = d3_list[index + 1].find('DS3')
                except IndexError:
                    continue
                diagnose_3 = ds3_element.text if ds3_element is not None else "Not found 3 second diagnose"

    path_label.config(text=f"Путь сохранение исправленного файла {file_path_save}")
    tree.write(file_path_save, encoding='windows-1251')


def open_file():
    filepath = filedialog.askopenfilename()
    file_name = filepath.split("/")[-1]
    return filepath, file_name


def save_file(file_name):
    file_path_save = filedialog.asksaveasfilename(defaultextension='.xml', initialfile=file_name)
    return file_path_save


def submit():
    try:
        filepath, file_name = open_file()
        file_path_save = save_file(file_name)
        root, tree = get_xml(filepath)
        create_dict(root, tree, file_path_save)
        logs_text.get('1.0', tk.END)
    except FileNotFoundError:
        print("Файл не был найден")


window = tk.Tk()
window.title("Исправь 840 ошибку")
window.geometry()

instr_label = tk.Label(window, text='Инструкция: программа находит и удаляет дублирующие '
                                    'с основным диагнозы в XML-файле')
instr_label.pack(padx=10, pady=10)

submit_button = tk.Button(window, text="Выбрать и исправить файл", command=submit)
submit_button.pack(padx=10, pady=10)

logs_text = tk.Text(window)
logs_text.pack()

path_label = tk.Label(window, text='')
path_label.pack(padx=10, pady=10)

window.mainloop()
