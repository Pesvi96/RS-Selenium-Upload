import tkinter as tk
from tkinter import ttk
from functions import *


class InvoiceGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("RS Invoice Uploader")
        self.style = ttk.Style()
        self.style.configure('TestEnv.TCheckbutton', background='#cfe2f3', font=('Times', '16', 'bold'))

        # Layout config
        self.fields = {}

        # Button to init driver
        ttk.Button(self.window, text="Init Driver", command=self.driver_init).grid(row=0, column=0, padx=5, pady=5)

        # Input + Button rows
        self.add_input_action(row=1, label="btn_click", method=btn_click, num_fields=1)
        self.add_input_action(row=2, label="box_type", method=box_type, num_fields=2)
        self.add_input_action(row=3, label="select_vat", method=select_vat, num_fields=1)
        self.add_input_action(row=4, label="fill_invoice", method=fill_invoice, num_fields=1)

        # Buttons that need no input
        ttk.Button(self.window, text="Access Invoice Page", command=access_invoice_page).grid(row=5, column=0, padx=5,
                                                                                              pady=5)
        ttk.Button(self.window, text="Select Month", command=select_month_in_list).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self.window, text="Select Unit", command=select_unit).grid(row=5, column=2, padx=5, pady=5)

        self.update_ui()

    def add_input_action(self, row, label, method, num_fields):
        """Adds input field(s) and a button that calls a method with those field values"""
        entries = []
        for i in range(num_fields):
            entry = ttk.Entry(self.window)
            entry.grid(row=row, column=i, padx=5, pady=5)
            entries.append(entry)

        # Bind the entries to the method
        def wrapped_call():
            args = [e.get() for e in entries]
            method(*args)

        ttk.Button(self.window, text=label, command=wrapped_call).grid(row=row, column=num_fields, padx=5, pady=5)

        # Optional: store for later
        self.fields[label] = entries

    @staticmethod
    def driver_init():
        init("https://eservices.rs.ge/Login.aspx?redirect_url=https://eservices.rs.ge/Login.aspx")

    def update_ui(self):
        """Disable/Enable objects according to indicated attributes"""
        pass

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = InvoiceGUI()
    gui.run()
