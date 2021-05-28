# BMI Calculator
# creator: Leandro R. Frazao
# phone: 83-0555294
# email: leandrofrazao@hotmail.com

import csv
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.ttk as ttk
from datetime import datetime
from tkinter import *

import matplotlib.patches as mpatches
import matplotlib.pyplot as pyplot
import numpy as np


class Bmi_main_frame(Frame):
    '''Create frame that contains components to calculate BMI'''

    def __init__(self, master):
        '''Create and pack events'''

        Frame.__init__(self, master)

        self.master.protocol("WM_DELETE_WINDOW", self.close_app)
        self.pack(expand=YES, fill=BOTH)
        self.master.title("BMI Calculator")
        self.master.withdraw()  # hide the pre load window due to a bug to load icon
        self.master.wm_iconbitmap('icon.ico')
        self.master.after(0, self.master.deiconify) #show window again
        self.master.resizable(0, 0)  # doesnt allow to resize the frame
        self.var_result = tk.StringVar()
        self.var_result.set("Result")
        self.time_on = BooleanVar(self, True)
        self.filename = None
        self.user_index = tk.IntVar(self, 0)
        self.user_name = tk.StringVar()
        self.date_bmi = tk.StringVar(self, datetime.today().strftime('%d-%m-%Y, %H:%M:%S'))
        self.user_data = {}  # {"User": [{"Kg": "20", "cm": "20", "Date": "01/01/2000, 00:00:00"}]}

        ###### Initializing Dictionary containing units of system of measurement
        self.var_system = {"Kg": '', "cm": '', "Stones": '', "Pounds": '', "Feet": '', "Inches": ''}
        self.widget_label = {}
        self.widget_entry = {}

        for unit in self.var_system.keys():
            self.var_system[unit] = tk.StringVar()
            self.var_system[unit].set("")

        self.init_components()

    def init_components(self):  ######## ROOT FRAME
        self.time_on.set(True)
        self.time_update()
        self.frame_main = Frame(self, bd=2, relief=SUNKEN)
        self.frame_main.pack(side=TOP, fill=X, pady=15, ipady=5, padx=10, ipadx=5)

        self.main_label = Label(self.frame_main, text=" Calculate your BMI", font=("Arial", 16))
        self.main_label.pack(fill=BOTH, ipady=10)

        ######## frame: Controls
        self.frame_controls = Frame(self, bd=1, relief=SUNKEN)
        self.frame_controls.pack(fill=X)
        self.frame_controls.grid_columnconfigure(0, minsize=100)
        self.frame_controls.grid_columnconfigure(4, minsize=20)
        self.frame_controls.grid_columnconfigure(8, minsize=45)
        Button(self.frame_controls, text="User List", width=8, font=("Arial", 12), command=self.user_list_window).grid(
            row=0, column=0, ipady=0 if sys.platform == "win32" else 5)
        Button(self.frame_controls, text="<", width=5, font=("Arial", 12),
               command=lambda e="previous": self.controls(e)).grid(row=0,
                                                                   column=1, ipady=0 if sys.platform == "win32" else 5)
        Entry(self.frame_controls, justify=CENTER, relief=FLAT, state="readonly", textvariable=self.user_index,
              width=4).grid(row=0, ipady=6 if sys.platform == "win32" else 1, column=2)
        Button(self.frame_controls, text=">", width=5, font=("Arial", 12),
               command=lambda e="next": self.controls(e)).grid(row=0, column=3,
                                                               ipady=0 if sys.platform == "win32" else 5)
        Button(self.frame_controls, text="Add", width=7, font=("Arial", 12),
               command=lambda e="add": self.controls(e)).grid(row=0, column=5,
                                                              ipady=0 if sys.platform == "win32" else 5)
        Button(self.frame_controls, text="Delete", width=7, font=("Arial", 12),
               command=lambda e="del": self.controls(e)).grid(row=0,
                                                              column=7, ipady=0 if sys.platform == "win32" else 5)
        Button(self.frame_controls, text="Chart", width=5, font=("Arial", 12),
               command=lambda e="chart": self.controls(e)).grid(row=0,
                                                                column=9, ipady=0 if sys.platform == "win32" else 5)

        #### Block-  Result
        self.frame_result = Frame(self, bd=2, relief=SUNKEN)
        self.frame_result.pack(fill=BOTH)
        self.entry_result = Entry(self.frame_result, justify=CENTER, textvariable=self.var_result, state="readonly",
                                  bd=1, relief=SUNKEN, takefocus=0, fg="#1c56a0", font=("Arial", 14))
        self.entry_result.pack(fill=BOTH, pady=12, ipady=5)

        ############### block 1 - user
        self.frame_block1 = Frame(self.frame_main, bd=0, relief=SUNKEN)
        self.frame_block1.pack(side=TOP, anchor=W, padx=35)
        self.label_name = Label(self.frame_block1, text="Your Name:", font=("Arial"))
        self.label_name.grid(row=0, column=0, sticky=E, ipady=10)
        self.entry_name = Entry(self.frame_block1, textvariable=self.user_name, font=("Arial"))
        self.entry_name.grid(row=0, column=1, sticky=E)
        self.entry_date = Entry(self.frame_block1, justify=CENTER, relief=SUNKEN, state="readonly",
                                textvariable=self.date_bmi,
                                width=18, takefocus=0, font=("Arial", 10))
        self.entry_date.grid(row=0, column=2)
        self.frame_block1.columnconfigure(3, minsize=20)
        Button(self.frame_block1, text="?", font=("Arial", 7),
               command=lambda: mb.showinfo(parent=self.frame_main, title="About",
                                           message="Python Project - July 2020 \n\n Author: Leandro Frazão \n\n "
                                                   "Lecturer: Brian Rogers "
                                                   "\n\n CCT College")).grid(row=0, column=4)

        self.frame_block1.grid_columnconfigure(2, minsize=130)
        #### Limit the length of user name
        self.user_name.trace("w", lambda arg1, arg2, arg3, user_name=self.user_name: self.username_validate())

        ############### block 2 - units

        self.frame_block2 = Frame(self.frame_main, bd=1, relief=SUNKEN)
        self.frame_block2.pack(side=LEFT, fill=BOTH, pady=10, padx=10, ipady=0)

        ######## weight frame
        self.frame_weight = Frame(self.frame_block2, bd=0, relief=SUNKEN)
        self.frame_weight.pack(pady=0, ipadx=5, ipady=0)
        Label(self.frame_weight, text="Your Weight: ", font=("Arial")).grid(ipady=0, ipadx=0, pady=10)

        self.frame_weight_child = Frame(self.frame_weight)
        self.frame_weight_child.grid(pady=0, ipadx=0, ipady=10)
        self.frame_weight_child.grid_columnconfigure(2, pad=10)

        ####adding Label and Entry components of measurement system to a dictionary called widget_label and widget_entry

        self.widget_label['Kg'] = (Label(self.frame_weight_child, text="Kg: ", state="normal", font=("Arial")))
        self.widget_label['Kg'].grid(stick=E, row=1, column=0)

        self.widget_label['Stones'] = (Label(self.frame_weight_child, text="Stones: ", state="disable", font=("Arial")))
        self.widget_label['Stones'].grid(stick=E, row=2, column=0)

        self.widget_label['Pounds'] = (Label(self.frame_weight_child, text="Pounds: ", state="disable", font=("Arial")))
        self.widget_label['Pounds'].grid(stick=E, row=2, column=2)

        self.widget_entry['Kg'] = (
            Entry(self.frame_weight_child, textvariable=self.var_system['Kg'], width=8, state="normal", font=("Arial")))
        self.widget_entry['Kg'].grid(row=1, column=1)

        self.widget_entry['Stones'] = (
            Entry(self.frame_weight_child, textvariable=self.var_system['Stones'], width=8, state="disable",
                  font=("Arial")))
        self.widget_entry['Stones'].grid(stick=W, row=2, column=1)
        self.widget_entry['Pounds'] = (
            Entry(self.frame_weight_child, textvariable=self.var_system['Pounds'], width=8, state="disable",
                  font=("Arial")))
        self.widget_entry['Pounds'].grid(stick=W, row=2, column=3)

        ######## height frame
        self.frame_height = Frame(self.frame_block2, bd=0, relief=SUNKEN)
        self.frame_height.pack(anchor=W, pady=0, ipadx=5, ipady=10)
        Label(self.frame_height, text="Your Height: ", font=("Arial")).grid(ipady=0, ipadx=20, pady=10)

        self.frame_height_child = Frame(self.frame_height)
        self.frame_height_child.grid(pady=0, ipadx=0, ipady=0)
        self.frame_height_child.grid_columnconfigure(0, pad=13)  #### spacing between columns

        self.widget_label['cm'] = (Label(self.frame_height_child, text="cm: ", state="normal", font=("Arial")))
        self.widget_label['cm'].grid(stick=E, row=1, column=0)

        self.widget_label['Feet'] = (Label(self.frame_height_child, text="Feet: ", state="disable", font=("Arial")))
        self.widget_label['Feet'].grid(stick=E, row=2, column=0)
        self.frame_height_child.grid_columnconfigure(2, pad=16)  #### spacing between colunms
        self.widget_label['Inches'] = (Label(self.frame_height_child, text="Inches: ", state="disable", font=("Arial")))
        self.widget_label['Inches'].grid(stick=E, row=2, column=2)

        self.widget_entry['cm'] = (
            Entry(self.frame_height_child, textvariable=self.var_system['cm'], width=8, state="normal", font=("Arial")))
        self.widget_entry['cm'].grid(stick=W, row=1, column=1)

        self.widget_entry['Feet'] = (
            Entry(self.frame_height_child, textvariable=self.var_system['Feet'], width=8, state="disable",
                  font=("Arial")))
        self.widget_entry['Feet'].grid(stick=W, row=2, column=1)
        self.widget_entry['Inches'] = (
            Entry(self.frame_height_child, textvariable=self.var_system['Inches'], width=8, state="disable",
                  font=("Arial")))
        self.widget_entry['Inches'].grid(stick=W, row=2, column=3)

        ########### Button: Calculate
        Button(self.frame_block2, text=" Click to Calculate your BMI", width=25, font=("Arial", 12),
               command=self.result_button).pack()

        ############### block 3 -
        self.frame_block3 = Frame(self.frame_main, bd=1, relief=SUNKEN)
        self.frame_block3.pack(side=LEFT, fill=BOTH, pady=10, ipadx=0, ipady=0)

        ####### Load/save data
        self.frame_data = Frame(self.frame_block3, bd=0, relief=SUNKEN)
        self.frame_data.pack(fill=BOTH, ipady=21)

        self.frame_data.grid_columnconfigure(0, pad=70)
        Label(self.frame_data, text="User data: ", font=("Arial")).grid(ipady=10)
        Button(self.frame_data, text="Load", width=10, command=self.load_file, font=("Arial")).grid(column=0)
        Button(self.frame_data, text="Save", width=10, command=self.save_file, font=("Arial")).grid(column=0)

        ######## System of Measurement
        self.frame4 = Frame(self.frame_block3, bd=0, relief=SUNKEN)
        self.frame4.pack(fill=X, pady=0, ipady=10)
        Label(self.frame4, text="System of Measurement: ", font=("Arial")).grid(stick=W)
        self.var_radio = IntVar(self.frame_block3, 1)

        Radiobutton(self.frame4, text='Metric System', variable=self.var_radio, value=1,
                    command=self.radiobutton_click, font=("Arial")).grid(stick=W)
        Radiobutton(self.frame4, text='Imperial System', variable=self.var_radio, value=2,
                    command=self.radiobutton_click, font=("Arial")).grid(stick=W)

        ###### change background colors
        self.configure(bg="#125097")
        self.frame_main.configure(bg="#dae7f6")
        self.main_label.configure(bg="#dae7f6")
        self.label_name.configure(bg="#dae7f6")
        self.frame_block1.configure(bg="#dae7f6")
        self.frame_controls.configure(bg="#125097", bd=0)
        self.frame_result.configure(bg="#125097", bd=0, padx=10)

        ######## bind and Validation entries
        self.reg = self.register(self.callback)  ### used to validate data to an Entry widget

        for item in self.widget_entry:
            self.widget_entry[item].config(validate="key",
                                           validatecommand=(self.reg, '%i', '%P', '%s', '%S', '%d', item))
            self.widget_entry[item].bind("<KeyRelease>", lambda e, widget=item: self.conversion_units(widget))


    def username_validate(self):  # only allow alphabet letters and space, with max length of 20 characters
        if not self.user_name.get().isalpha():
            self.user_name.set(''.join(char for char in self.user_name.get() if char.isalpha() or char.isspace())[:20])
        else:
            self.user_name.set(self.user_name.get()[:20])

    def callback(self, index, input, text, char, action, widget):
        if action != '1':
            if text == '':  # necessary to validate Entries that got values through code
                return True
            if self.set_limits(widget, input, index, text):
                return True
            else:
                return False
        elif char in "1234567890":  # valid values
            if self.set_limits(widget, input, index, text):
                if str(input).find(".") == -1:  ### check if there is no dot
                    if text != "":
                        if float(text) == 0 == int(input[0]):
                            return False
                        else:
                            return True
                    else:
                        return True
                elif int(index) < str(input).find("."):  ### check if number is added before dot
                    if float(text) > 0 and input[0] == "0":
                        return False
                    else:
                        return True
                elif len(text) - str(input).find(".") <= 2:  ### limit of 2 decimals after dot
                    return True
                else:
                    return False
            else:
                return False
        elif char == '.' and widget in ["Kg", "Pounds", "Inches"]:
            if index == '0':
                return False
            elif char in text:
                return False
            elif self.set_limits(widget, input, index,
                                 text):  # check if dot is put in the end if the number is the maximum value
                return True
            else:
                return False
        else:
            return False

    def var_limit(self, widget, index):
        self.limits = {"Kg": [500, 1], "Stones": [78, 0], "Pounds": [13.99, 2.20, 10.31], "cm": [300, 40],
                       "Feet": [9, 1],
                       "Inches": [11.99, 3.75, 10.11]}
        return self.limits[widget][index]

    def set_limits(self, widget, input, index="0", text=""):

        self.var_result.set(f'Result')  # Clean the error messages, returning the standard text.
        if input == "" or input == ".":
            return True
        if widget in ("Stones") and text == "" and int(float(input)) == 0:
            return True
        if widget in ("Kg", "cm", "Feet") and text == "" and int(float(input)) == 0:
            self.var_result.set(f'Min {widget} is {self.var_limit(widget, 1): .0f}')
            return False
        if text == "" and int(float(input)) != 0:
            return True

        if widget in ["Kg", "Stones", "cm", "Feet", "Pounds", "Inches"]:
            if float(input) <= float(self.var_limit(widget, 0)):
                if widget in ["Pounds", "Inches"] and input != "":
                    if widget == "Pounds":
                        unit = "Stones"
                    else:
                        unit = "Feet"
                    if str(self.var_system[unit].get()) != "":
                        if int(self.var_system[unit].get()) == self.var_limit(unit, 0) and float(
                                input) <= self.var_limit(widget, 2):
                            return True
                        elif int(self.var_system[unit].get()) < self.var_limit(unit, 0) and float(
                                input) <= self.var_limit(widget, 0):
                            return True
                        else:
                            print(f'Max {widget} is {self.var_limit(widget, 1)}')
                            self.var_result.set(f'Max {widget} is {self.var_limit(widget, 2)}')
                            return False
                    else:
                        return True
                else:
                    return True

            else:
                # check the max values in pounds and inches when there are max values to stones and feet.
                if widget in ["Pounds"] and int(self.var_system["Stones"].get()) == self.var_limit("Stones", 0) \
                        and float(input) > self.var_limit(widget, 2):
                    self.var_result.set(f'Max {widget} is {self.var_limit(widget, 2): .2f}')
                    return False
                elif widget in ["Inches"] and int(self.var_system["Inches"].get()) == self.var_limit("Inches", 0) \
                        and float(input) > self.var_limit(widget, 2):
                    self.var_result.set(f'Max {widget} is {self.var_limit(widget, 2): .2f}')
                    return False

                else:
                    print(f'Max {widget} is {int(self.var_limit(widget, 0))}')
                    self.var_result.set(f'Max {widget} is {self.var_limit(widget, 0)}')
                    return False
        else:
            return False

    def conversion_units(self, widget):

        if widget in ["Pounds", "Inches"]:
            if widget == "Pounds":
                unit = "Stones"
            else:
                unit = "Feet"
            if str(self.var_system[unit].get()) == "":
                self.var_system[widget].set(self.var_limit(widget, 1))
                self.var_system[unit].set(self.var_limit(unit, 1))
                self.var_result.set(f'Min Weight   {unit}: {self.var_limit(unit, 1)} '
                                    f' {widget}: {self.var_limit(widget, 1): .2f}')
        if widget in ["Stones", "Feet"]:
            if widget == "Stones":
                unit = "Pounds"
            else:
                unit = "Inches"
            if str(self.var_system[widget].get()) == "0":  # or str(self.var_system[widget].get()) == "":
                self.var_system[widget].set(self.var_limit(widget, 1))
                self.var_system[unit].set(self.var_limit(unit, 1))

        if widget in ["Kg", "Stones", "Pounds", "cm", "Feet", "Inches"]:
            self.time_on.set(True)
            self.time_update()  # time update only if user enter values on entry boxes.

            if str(self.var_system[widget].get()) != "" and self.var_system[widget].get() != ".":
                if int(float(self.var_system[widget].get())) == self.var_limit(widget, 0):
                    self.var_system[widget].set(self.var_limit(widget, 0))
                    if widget not in ["Kg", "cm"]:
                        if str(self.var_system[unit].get()) != "":
                            if int(float(self.var_system[unit].get())) > float(self.var_limit(unit, 2)):
                                self.var_system[unit].set(self.var_limit(unit, 2))

                elif 0 <= float(self.var_system[widget].get()) < 1:
                    if widget in ["Pounds", "Inches"]:
                        if int(self.var_system[unit].get()) <= int(self.var_limit(unit, 1)):
                            if float(self.var_system[widget].get()) < int(self.var_limit(widget, 1)):
                                self.var_system[widget].set(self.var_limit(widget, 1))
                                self.var_result.set(f'Min {widget} is {self.var_limit(widget, 1): .2f}')
                    else:
                        self.var_system[widget].set(0)
                elif float(self.var_system[widget].get()) > 0 and str(self.var_system[widget].get()).find(".") == -1:
                    self.var_system[widget].set(int(self.var_system[widget].get()))
            else:
                if widget in ["Kg", "Stones"]:
                    self.var_system['Kg'].set('')
                    self.var_system['Stones'].set('')
                    self.var_system['Pounds'].set('')
                if widget in ["cm", "Feet"]:
                    self.var_system['cm'].set('')
                    self.var_system['Feet'].set('')
                    self.var_system['Inches'].set('')

        if self.var_radio.get() == 1 or widget == "display":
            if str(self.var_system["Kg"].get()) != "":
                var_weight = float(self.var_system['Kg'].get()) * 0.15747304441
                print(f'{int(var_weight)} Stones')
                print(f'{(var_weight - int(var_weight)) * 14:.2f} Pounds')
                var_pounds = f'{(var_weight - int(var_weight)) * 14:.2f}'
                if int(float(var_pounds)) == 14:  # convert 14 pounds to 1 stone
                    self.var_system['Stones'].set(int(var_weight) + 1)
                    self.var_system['Pounds'].set(0)
                else:
                    self.var_system['Stones'].set(int(var_weight))
                    self.var_system['Pounds'].set(f'{(var_weight - int(var_weight)) * 14:.2f}')
            if str(self.var_system["cm"].get()) != "":
                var_height = float(self.var_system['cm'].get()) * 0.032808399  # (convert cm to Feet)
                print(f'{int(var_height)} Feet')
                print(f'{(var_height - int(var_height)) * 12:.2f} Inches')
                var_inches = f'{(var_height - int(var_height)) * 12:.2f}'
                if int(float(var_inches)) == 12:  # convert 12 inches to 1 Feet
                    self.var_system['Feet'].set(int(var_height) + 1)
                    self.var_system['Inches'].set(0)
                else:
                    self.var_system['Feet'].set(int(var_height))  # Feet is integer
                    self.var_system['Inches'].set(f'{(var_height - int(var_height)) * 12:.2f}')

        if self.var_radio.get() == 2:
            if str(self.var_system["Stones"].get()) != "":
                var_weight = float(self.var_system['Stones'].get())
                if self.var_system['Pounds'].get() != "":
                    var_weight += float(self.var_system['Pounds'].get()) / 14
                var_weight = var_weight * 6.35029318
                print(f'{var_weight: .2f} Kg')
                var_weight = float(f'{var_weight:.2f}')
                if var_weight == int(self.var_limit("Kg", 0)):
                    self.var_system['Kg'].set(f'{var_weight:.0f}')
                else:
                    self.var_system['Kg'].set(f'{var_weight:.2f}')

            if str(self.var_system["Feet"].get()) != "":
                var_weight = float(self.var_system['Feet'].get())
                if self.var_system['Inches'].get() != "":
                    var_weight += float(self.var_system['Inches'].get()) / 12  # Inches to Feet
                var_weight = var_weight * 30.4840965992  # Feet to cm
                print(f'{var_weight: .2f} cm')
                self.var_system['cm'].set(f'{int(var_weight)}')

    def radiobutton_click(self):
        for item in (self.widget_label):
            if item in ["Kg", "cm"]:
                self.widget_label[item].configure(state=DISABLED if self.var_radio.get() == 2 else NORMAL)
                self.widget_entry[item].configure(state=DISABLED if self.var_radio.get() == 2 else NORMAL)
            if item in ["Stones", "Pounds", "Feet", "Inches"]:
                self.widget_label[item].configure(state=DISABLED if self.var_radio.get() == 1 else NORMAL)
                self.widget_entry[item].configure(state=DISABLED if self.var_radio.get() == 1 else NORMAL)

    def calc_bmi(self, var_weight, var_height):
        print(var_weight, 'Kg')
        print(var_height, 'cm')
        var_height = (var_height / 100) ** 2
        self.bmi = var_weight / var_height
        print(self.bmi, '<< BMI result')
        return self.bmi

    def result_button(self):
        self.entry_result.configure(font=("arial", 14))

        if self.var_system["Kg"].get() and self.var_system["cm"].get() != "":
            if float(self.var_system["Kg"].get()) >= self.var_limit("Kg", 1) and \
                    float(self.var_system["cm"].get()) >= self.var_limit("cm", 1):
                var_weight = float(self.var_system['Kg'].get())
                var_height = float(self.var_system['cm'].get())
                self.bmi_calculate(self.calc_bmi(var_weight, var_height))
                return True  # Values can only be add in User List if result return True
            else:
                if self.var_radio.get() == 1:
                    self.var_result.set(f'Min WEIGHT  Kg: {self.var_limit("Kg", 1)}  |  '
                                        f'Min HEIGHT  cm: {self.var_limit("cm", 1): .0f}')
                if self.var_radio.get() == 2:
                    self.entry_result.configure(font=("arial", 11))
                    self.var_result.set(f'Min WEIGHT  Stones: {self.var_limit("Stones", 1)}  '
                                        f'Pounds: {self.var_limit("Pounds", 1): .2f}  |  '
                                        f'Min HEIGHT  Feet: {self.var_limit("Feet", 1):}  '
                                        f'Inches: {self.var_limit("Inches", 1): .2f}')
                return False

        else:
            self.var_result.set("Enter your Weight and Height")
            return False

    def check_data(self):  # check duplicate values
        if self.user_name.get() in self.user_data.keys():
            if len(self.user_data[self.user_name.get()]) > 0:
                for index in range(0, len(self.user_data[self.user_name.get()])):
                    if self.user_data[self.user_name.get()][index]["Kg"] == self.var_system["Kg"].get():
                        if self.user_data[self.user_name.get()][index]["cm"] == self.var_system["cm"].get():
                            if self.user_data[self.user_name.get()][index]["Date"] == self.date_bmi.get():
                                self.var_result.set("Duplicate Values")
                                return False
        return True

    def add_user_data(self):
        if self.user_name.get() is not None and self.user_name.get() != '':
            if self.var_system["Kg"].get() and self.var_system["cm"].get() != "":
                user_name = self.user_name.get()
                self.date_bmi.set(datetime.today().strftime('%d-%m-%Y, %H:%M:%S'))
                if user_name in self.user_data.keys():
                    self.user_data[self.user_name.get()].append(
                        {"Kg": self.var_system["Kg"].get(), "cm": self.var_system["cm"].get(),
                         "Date": self.date_bmi.get()})
                else:
                    self.user_data[self.user_name.get()] = [
                        {"Kg": self.var_system["Kg"].get(), "cm": self.var_system["cm"].get(),
                         "Date": self.date_bmi.get()}]

                index = len(self.user_data[self.user_name.get()]) - 1
                self.user_index.set(index + 1)
            else:
                self.var_result.set("Enter your Weight and Height")
        else:
            self.var_result.set("Enter your Name!!!")

    def del_user_data(self, index):
        try:
            del self.user_data[self.user_name.get()][index]
            if len(self.user_data[self.user_name.get()]) == 0:  # if user doesnt have any values
                del self.user_data[self.user_name.get()]  # delete user from User List
                self.user_index.set(0)
                for value in self.var_system.values():
                    value.set('')
                self.var_result.set(f'{self.user_name.get()} deleted from User List.')
                self.user_name.set('')
                self.time_on.set(True)
                self.time_update()
        except:
            self.time_on.set(True)
            self.time_update()
            if all(values.get() == "" for values in self.var_system.values()):  # check if all entries are empty
                print("Nothing to delete")
                self.user_name.set('')
                self.var_result.set("Nothing to be deleted!!!")
            else:
                for value in self.var_system.values():
                    value.set('')

    def controls(self, button):

        data_error = False
        self.entry_result.configure(font=("arial", 14))
        index = self.user_index.get() - 1
        if index == -1:
            self.var_result.set("No data")
        if button == "next":
            index += 1
        if button == "previous":
            index -= 1
        if button == "add":
            if self.result_button():
                if self.check_data():  # check if there is a duplicate before add new values to the list.
                    self.add_user_data()
                    index = self.user_index.get()
                else:
                    data_error = True
            else:
                data_error = True
        if button == "del":
            self.del_user_data(index)
            index -= 1
        if button == "chart":
            if self.validate_user() or self.result_button():
                if not pyplot.fignum_exists(1):  # open a chart window only if it doesnt have any chart window opened.
                    self.chart_user()
                else:
                    pyplot.show()  # focus on chart window

        if self.validate_user() == True and data_error == False:
            self.time_on.set(False)
            self.display_data(index)

    def validate_user(self):  # check if user exist and has data.
        if self.user_name.get() in self.user_data.keys() \
                and len(self.user_data[self.user_name.get()]) > 0:
            return True
        else:
            return False

    def display_data(self, index):
        if self.user_name.get() == "":
            self.user_name.set(list(self.user_data.keys())[1])
        if index < 0:
            index = 0
        if index >= len(self.user_data[self.user_name.get()]) - 1:
            index = len(self.user_data[self.user_name.get()]) - 1

        self.user_index.set(index + 1)
        self.var_system["Kg"].set(self.user_data[self.user_name.get()][index]["Kg"])
        self.var_system["cm"].set(self.user_data[self.user_name.get()][index]["cm"])
        self.conversion_units("display")  # update the imperial units entries
        self.date_bmi.set(self.user_data[self.user_name.get()][index]["Date"])
        self.result_button()

    def bmi_calculate(self, bmi):

        if bmi < 18.5:
            self.var_result.set(f"Your BMI is {bmi:.1f} - Underweight")
        elif 18.5 <= bmi <= 24.9:
            self.var_result.set(f"Your BMI is {bmi:.1f} - Normal weight")
        elif 24.9 < bmi <= 29.9:
            self.var_result.set(f"Your BMI is {bmi:.1f} - Overweight")
        elif bmi > 29.9:
            self.var_result.set(f"Your BMI is {bmi:.1f} - Obese")

    def load_file(self):
        try:
            self.fileName = fd.askopenfilename(defaultextension=".csv",
                                               filetypes=[("csv files", ".csv"), ("all files", ".*")])
            with open(self.fileName, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter="|", skipinitialspace=True,
                                    doublequote=False) 
                mydict = {}
                for row in reader:
                    value = row[1:]
                    mydict[row[0]] = [{value[0]: value[1]}]
                    count = 0
                    max_count = 6
                    if len(value) > 6:
                        count_list = int(len(value) / 6)
                    else:
                        count_list = 1
                    for list_index in range(0, count_list):
                        for unit in range(count, max_count, 2):
                            mydict[row[0]][list_index][value[unit]] = value[unit + 1]
                            count += 2
                        max_count += 6
                        if count >= len(value):
                            break
                        else:
                            mydict[row[0]].append({})
                self.user_data = mydict
            csvfile.close()
            self.time_on.set(False)
            self.user_list_window()
            self.user_index.set(len(self.user_data[self.user_name.get()]) - 1)
            self.display_data(self.user_index.get())
        except:
            print("Error to open the file or user canceled")

    def save_file(self):
        if len(self.user_data) > 0 or self.result_button():
            try:
                if self.filename is None or self.filename == "":
                    self.filename = fd.asksaveasfilename(defaultextension=".csv",
                                                         filetypes=[("csv files", ".csv"), ("all files", ".*")])
                    self.write_file()
                else:
                    self.write_file()
            except:
                print("Error to save the file or user canceled")

        else:
            self.var_result.set("User Data is empty")

    def write_file(self):
        if len(self.user_data) > 0 or self.result_button():
            csvfile = open(file=self.filename, mode='w', newline='\n')
            writer = csv.writer(csvfile, delimiter="|", escapechar='', quoting=csv.QUOTE_NONE)

            if len(self.user_data) > 0:  # if user have added data to the user list
                for key in self.user_data.keys():
                    result = [''.join(key)]
                    for index in range(0, len(self.user_data[key])):
                        for unit, value in self.user_data[key][index].items():
                            result.append(''.join(unit))
                            result.append(''.join(value))
                    writer.writerow(result)
            elif self.result_button():  # if there is not data added to the user list, but only the values on screen
                result = [''.join(self.user_name.get())]
                for unit, value in self.var_system.items():
                    if unit in ["Kg", "cm"]:
                        result.append(''.join(unit))
                        result.append(''.join(value.get()))
                result.append(self.date_bmi.get())
                writer.writerow(result)

            csvfile.close()
            self.var_result.set("Saved")
        else:
            print("User data is empty")
            self.var_result.set("User Data is empty")

    def user_list_window(self):
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        self.window_user = tk.Toplevel(self.master)
        self.window_user.title("User List")
        self.window_user.focus_set()
        if sys.platform == "win32":  # -toolwindow only work on Windows OS
            self.window_user.attributes("-toolwindow", 1)
            self.window_user.geometry(f'+{x + 60}+{y + 125}')

        self.window_user.resizable(0, 0)
        self.frame_list = Frame(self.window_user)
        self.frame_list.pack(padx=10, pady=10)
        style_ttk = ttk.Style(self.frame_list)
        style_ttk.configure('Treeview', rowheight=20)
        Label(self.frame_list, text="Select User").pack(pady=5)

        self.treeview_list = ttk.Treeview(self.frame_list, height=5, columns=("name", "date"))
        self.scrollbar = ttk.Scrollbar(self.frame_list, orient=tk.VERTICAL, command=self.treeview_list.yview)
        self.treeview_list['yscroll'] = self.scrollbar.set
        self.treeview_list.pack(side="left")
        self.treeview_list['show'] = 'headings'  # supress the empty column
        self.treeview_list.heading('name', text="Name")
        self.treeview_list.heading('date', text="Last update")
        self.treeview_list.column('name', minwidth=200, stretch=NO, width=200)
        self.treeview_list.column('date', minwidth=120, stretch=NO, width=120)
        self.scrollbar.pack(side="left", fill="y")
        try:
            for id, user in enumerate(self.user_data.keys()):
                if len(self.user_data[user]) > 0:  # check if user has values added
                    self.treeview_list.insert('', tk.END, iid=id,
                                              values=(
                                                  user, self.user_data[user][len(self.user_data[user]) - 1]["Date"]))
            if len(self.treeview_list.get_children()) > 0:
                self.treeview_list.selection_set(0)
                self.treeview_list.bind('<Double-1>', lambda e: self.select_user_click())
        except:
            print("Error to load user data")
        self.treeview_list.bind('<ButtonRelease-1>', lambda e: self.resize_columns())
        self.window_button = Button(self.window_user, text="OK", width=15, command=self.select_user_click)
        self.window_button.pack(fill="y")

        self.window_user.grab_set()
        self.master.wait_window(self.window_user)
        self.window_user.grab_release()
        self.master.focus_force()

    def resize_columns(self):  # if user tries to change the width, it resizes automatically
        self.treeview_list.column('name', minwidth=200, width=200)
        self.treeview_list.column('date', minwidth=120, width=120)

    def select_user_click(self):
        if len(self.treeview_list.get_children()) > 0:
            item = self.treeview_list.selection()
            user = self.treeview_list.item(item, 'values')[0]
            self.user_name.set(user)
            self.display_data(len(self.user_data[user]) - 1)
        else:
            self.var_result.set("User List is empty")
        self.window_user.destroy()

    def chart_user(self):
        x = []
        y = []
        var_date = []
        pyplot.figure("BMI Chart")
        pyplot.xlabel("Date")
        pyplot.ylabel("BMI")
        if self.user_name.get() in self.user_data.keys():
            for index in range(0, len(self.user_data[self.user_name.get()])):
                var_weight = float(self.user_data[self.user_name.get()][index]["Kg"])
                var_height = float(self.user_data[self.user_name.get()][index]["cm"])
                var_date.append(self.user_data[self.user_name.get()][index]["Date"][:10])
                y.append(float(f'{self.calc_bmi(var_weight, var_height):.1f}'))
                x.append(index + 1)
            for a, b in zip(x, y):
                pyplot.text(a, b, f'BMI: {b}\n Kg: {self.user_data[self.user_name.get()][a - 1]["Kg"]}', rotation=65,
                            size=8)
        else:
            var_weight = float(self.var_system["Kg"].get())
            var_height = float(self.var_system["cm"].get())
            var_date.append(self.date_bmi.get()[:10])
            y.append(float(f'{self.calc_bmi(var_weight, var_height):.1f}'))
            x.append(1)
            for a, b in zip(x, y):
                pyplot.text(a, b, f'BMI: {b}\n Kg: {var_weight}', rotation=50,
                            size=8)

        max_y = max(y)
        min_y = min(y)
        max_x = max(x)
        pyplot.subplots_adjust(bottom=0.22)
        pyplot.ylim(min_y - 1, max_y + 1)
        pyplot.xlim(0, max_x + 1)
        pyplot.plot(x, y, "bo")
        pyplot.axhline(y=18.5, color='gray', linestyle='--', alpha=0.1)
        pyplot.axhline(y=24.9, color='gray', linestyle='--', alpha=0.1)
        pyplot.axhline(y=29.9, color='gray', linestyle='--', alpha=0.1)
        pyplot.axhspan(0, 18.5, facecolor="blue", alpha=0.1)
        pyplot.axhspan(18.5, 24.9, facecolor="green", alpha=0.1)
        pyplot.axhspan(24.9, 29.9, facecolor="yellow", alpha=0.1)
        pyplot.axhspan(29.9, max_y + 10 if max_y > 45 else 50, facecolor="red", alpha=0.1)
        pyplot.xticks(x, var_date, rotation=30, ha="right", fontsize=9)
        pyplot.yticks(np.arange(15 if max_y < 50 else 20, max_y + 10, 5 if max_y < 50 else 75), fontsize=9)
        red_patch = mpatches.Patch(color='red', label='Obese', alpha=0.1)
        yellow_patch = mpatches.Patch(color='yellow', label='Overweitgh', alpha=0.1)
        green_patch = mpatches.Patch(color='green', label='Normal weight', alpha=0.1)
        blue_patch = mpatches.Patch(color='blue', label='Underweight', alpha=0.1)
        pyplot.legend(handles=[red_patch, yellow_patch, green_patch, blue_patch], prop={'size': 8})
        pyplot.show()

    def time_update(self):
        if self.time_on.get():
            self.date_bmi.set(datetime.now().strftime('%d-%m-%Y, %H:%M:%S'))
            self.master.after(1000, self.time_update)  # Update every second


    def close_app(self):
        if pyplot.fignum_exists(1):  # check if it has a chart window opened.
            pyplot.close("all")
        sys.exit()


def main():
    root = Tk()
    Bmi_main_frame(root)

    root.mainloop()


if __name__ == "__main__":
    main()
