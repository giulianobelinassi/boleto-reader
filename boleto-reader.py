#!/usr/bin/python3

import os
import sys
import subprocess
import random
import threading
import tkinter as tk
from tkinter import messagebox


token = random.randint(1, 65535)
temp_img = 'boleto-reader-' + str(token) + ".png"

if sys.platform == 'win32':
    from PIL import ImageGrab
    temp_img_path = os.getenv('TEMP') + temp_img
else:
    temp_img_path = '/tmp/' + temp_img

def take_screenshot():
    if sys.platform == 'win32':
        try:
            proc=subprocess.Popen([os.getenv('WINDIR') + '\\System32\\SnippingTool.exe',
                                   '/clip'])
            proc.communicate()
        except:
            messagebox.showerror("Erro Fatal", "Erro ao lançar o 'SnippingTool.exe'.")
            os._exit(1)

        try:
            im = ImageGrab.grabclipboard()
            im.save(temp_img_path,'PNG')
        except Exception as err:
            messagebox.showerror("Erro Fatal", "Erro ao salvar screenshot: " + str(err))
            os._exit(1)

    else:
        try:
            proc=subprocess.Popen(['gnome-screenshot',
                                   '-a',
                                   '--file='+temp_img_path])
            proc.communicate()

        except:
            messagebox.showerror("Erro Fatal", "Erro ao lançar o 'gnome-screenshot'. Veja o manual para ver as dependências do programa.")
            os._exit(1)



def launch_tesseract():
    path_to_tesseract = 'tesseract'


    if sys.platform == 'win32':
        path_to_tesseract = 'win32\\Tesseract-OCR\\tesseract.exe'
        if getattr(sys, 'frozen', True):
            path_to_tesseract = os.path.dirname(os.path.abspath(__file__)) + '\\' + path_to_tesseract
    try:
        if sys.platform == 'win32':
            proc=subprocess.Popen([path_to_tesseract,
                                   '-l', 'por',
                                   '--dpi', '300',
                                   temp_img_path,
                                   'stdout'],
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            proc=subprocess.Popen([path_to_tesseract,
                                   '-l', 'por',
                                   '--dpi', '300',
                                   temp_img_path,
                                   'stdout'],
                                   stdout=subprocess.PIPE)

        code = proc.stdout.read()
        code = code.decode()
        return str(code)

    except Exception as err:
        messagebox.showerror("Erro Fatal", "Erro ao lançar o 'tesseract': " + str(err))
        os._exit(1)

    return None

def assemble_damsp(numbers):
    numbers = str(numbers)

    first  = numbers[0:11]
    second = numbers[11:12]

    third  = numbers[12:23]
    fourth = numbers[23:24]

    fifth  = numbers[24:35]
    sixth  = numbers[35:36]

    seventh= numbers[36:47]
    eigth  = numbers[47:48]

    damsp = '%s-%s %s-%s %s-%s %s-%s' % (first, second, third, fourth,
                                         fifth, sixth, seventh, eigth)
    return damsp

def assemble_boleto(numbers):
    numbers = str(numbers)

    first  = numbers[0:5]
    second = numbers[5:10]

    third  = numbers[10:15]
    fourth = numbers[15:21]

    fifth  = numbers[21:26]
    sixth  = numbers[26:32]

    seventh= numbers[32:33]
    eigth  = numbers[33:47]

    boleto = '%s.%s %s.%s %s.%s %s %s' % (first, second, third, fourth,
                fifth, sixth, seventh, eigth)
    return boleto

def process_code(code):

    interesting = code.split('\n')[0]

    interesting = interesting.replace('.', '')
    interesting = interesting.replace('-', '')
    interesting = interesting.replace(' ', '')

    no_spaces = interesting

    damsp = assemble_damsp(no_spaces)
    boleto = assemble_boleto(no_spaces)

    return no_spaces, damsp, boleto

def main():
    take_screenshot()
    code = launch_tesseract()
    no_spaces, damsp, boleto = process_code(code)
    try:
        os.remove(temp_img_path)
    except:
        pass
    return no_spaces, damsp, boleto, code

class Window:
    def messagebox_error_handler(self, widget, response_id):
        sys.exit()

    def on_button_doit(self):
        t = threading.Thread(target=self.run_button_doit)
        t.start()

    def run_button_doit(self):
        top = tk.Toplevel()
        msg = tk.Message(top, text="Selecione a área com o número do documento", width=400).pack()

        no_spaces, damsp, boleto, code = main()
        top.destroy()

        if len(no_spaces) != 48:
            damsp = "ERRO / INVÁLIDO"

        if len(no_spaces) != 47:
            boleto = "ERRO / INVÁLIDO"

        self.entry_damsp.configure(state = tk.NORMAL)
        self.entry_damsp.delete(0, tk.END)
        self.entry_damsp.insert(0, damsp)
        self.entry_boleto.configure(state = tk.NORMAL)
        self.entry_boleto.delete(0, tk.END)
        self.entry_boleto.insert(0, boleto)

        if self.sensor_out:
            self.sensor_out.configure(state = tk.NORMAL)
            self.sensor_out.delete(1., tk.END)
            self.sensor_out.insert(1., code)
            self.sensor_out.configure(state = tk.DISABLED)

    def show_debug_box(self):
        self.top.geometry("700x400")
        self.row4 = tk.Frame(self.top)
        self.row4.pack(side=tk.TOP)

        self.sensor_label = tk.Label(self.row4, text="Lido pelo Sensor (debug):", anchor='w')
        self.sensor_label.pack(side=tk.BOTTOM)

        self.row5 = tk.Frame(self.top)
        self.row5.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.sensor_out = tk.Text(self.row5)
        self.sensor_out.config(state=tk.DISABLED)
        self.sensor_out.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        self.button_sensor.config(command=lambda: self.hide_debug_box())

    def hide_debug_box(self):
        self.top.geometry("700x130")

        self.sensor_label.destroy()
        self.sensor_out.destroy()

        self.row4.destroy()
        self.row5.destroy()

        self.button_sensor.config(command=lambda: self.show_debug_box())

    def __init__(self):
        self.top = tk.Tk(className="Boleto Reader")
        self.top.title("Boleto Reader")
        self.top.geometry("700x130")

        self.row1 = tk.Frame(self.top)
        self.row1.pack(side=tk.TOP, fill=tk.X)

        self.label_damsp = tk.Label(self.row1, width=22, text="Concessionária/Tributos", anchor='w', padx=5)
        self.label_damsp.pack(side=tk.LEFT)

        self.entry_damsp = tk.Entry(self.row1, text="", state='readonly')
        self.entry_damsp.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES)

        self.row2 = tk.Frame(self.top)
        self.row2.pack(side=tk.TOP, fill=tk.X)

        self.label_boleto = tk.Label(self.row2, width=22, text="Título Bancário", anchor='w', padx=5)
        self.label_boleto.pack(side=tk.LEFT)

        self.entry_boleto = tk.Entry(self.row2, text="", state='readonly')
        self.entry_boleto.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES)

        self.row3 = tk.Frame(self.top, pady=5)
        self.row3.pack(side=tk.TOP)

        self.button_doit = tk.Button(self.row3, text="Ler Código", command=lambda: self.on_button_doit(), pady=10, padx=50)
        self.button_doit.pack(side=tk.RIGHT)

        self.button_sensor = tk.Button(self.row3, text="Info. Sensor", command=lambda: self.show_debug_box(), pady=10)
        self.button_sensor.pack(side=tk.LEFT)

        self.sensor_out = None

        self.top.mainloop()

win = Window()
