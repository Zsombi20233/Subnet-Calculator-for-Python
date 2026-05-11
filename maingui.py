import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# this section is for calcuating the mask

def calc(num : int):
    if num < 8:
        ret = 0
        for x in range(num):
            ret += 2**(7-x)
        return ret
    else:
        return 255

# this is for GUI

def open_smaks():
    smaks = ttk.Window(root)
    smaks.title('Subnet Mask Calculator')

    label = ttk.Label(smaks, text='Enter Subnet Mask (e.g.: 24)')
    label.pack(padx=20, pady=10)

    mask_entry = ttk.Entry(smaks)
    mask_entry.pack(padx=20, pady=5)
    mask_entry.focus_set()

    result_label = ttk.Label(smaks, text="")
    result_label.pack(pady=10)

    def mask_calc():
        try:
            mask = int(mask_entry.get())
            if not (0 <= mask <= 32):
                result_label.config(text='Enter a number 0 - 32', bootstyle=DANGER)
                return
            if mask <= 8:
                res = f'Mask is in decimal > {calc(mask)}.0.0.0'
            elif mask <= 16:
                res = f'Mask is in decimal > 255.{calc(mask-8)}.0.0'
            elif mask <= 24:
                res = f'Mask is in decimal > 255.255.{calc(mask-16)}.0'
            else:
                res = f'Mask is in decimal > 255.255.255.{calc(mask-24)}'
            result_label.config(text=f'Decimal: {res}', bootstyle=SUCCESS)
        except ValueError:
            result_label.config(text='Invalid Input!', bootstyle=DANGER)

    calc_b = ttk.Button(smaks, text='Calculate', command=mask_calc, bootstyle=INFO)
    calc_b.pack(pady=10)


root = ttk.Window(title="Network calculator")

b1 = ttk.Button(root, text='Subnet Mask Calculator', bootstyle=SUCCESS, command=open_smaks)
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text='Subnet Calculator (Coming soon)', bootstyle=DANGER)
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()