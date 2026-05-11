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
    smaks.bind('<Return>', lambda event: mask_calc())

    label = ttk.Label(smaks, text='Enter Subnet Mask (e.g.: 24)', background='white')
    label.pack(padx=20, pady=10)

    mask_entry = ttk.Entry(smaks)
    mask_entry.pack(padx=20, pady=5)
    mask_entry.focus_set()

    result_label = ttk.Label(smaks, text="", background='white')
    result_label.pack(pady=10)

    def get_mask_copy():
        result_text = result_label.cget("text")
        if 'Decimal:' in result_text:
            clean = result_text.replace('Decimal: ', "")
            smaks.clipboard_clear()
            smaks.clipboard_append(clean)
            copy_btn.configure(text='Copied!', bootstyle=SUCCESS)
            smaks.after(2000, lambda: copy_btn.configure(text="Copy to Clipboard", bootstyle=SECONDARY))


    copy_btn = ttk.Button(smaks, text="Copy to Clipboard", command=get_mask_copy, bootstyle=SECONDARY)

    def mask_calc():
        try:
            mask = int(mask_entry.get())
            if not (0 <= mask <= 32):
                result_label.configure(text='Enter a number 0 - 32', background="red", foreground='white')
                copy_btn.pack_forget()
                return
            if mask <= 8:
                res = f'{calc(mask)}.0.0.0'
            elif mask <= 16:
                res = f'255.{calc(mask-8)}.0.0'
            elif mask <= 24:
                res = f'255.255.{calc(mask-16)}.0'
            else:
                res = f'255.255.255.{calc(mask-24)}'
            result_label.configure(text=f'Decimal: {res}', background="green", foreground='white')
        except ValueError:
            result_label.configure(text='Invalid Input!', background="red", foreground='white')
            copy_btn.pack_forget()
        copy_btn.pack(pady=5)

root = ttk.Window(title="Network calculator", )

b1 = ttk.Button(root, text='Subnet Mask Calculator', bootstyle=SUCCESS, command=open_smaks)
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text='Subnet Calculator (Coming soon)', bootstyle=DANGER)
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()