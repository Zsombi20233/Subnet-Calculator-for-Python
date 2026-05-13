import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import winreg
import ipaddress


# change the theme to Windows theme

def get_windows_theme():
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
    return "flatly" if value == 1 else "darkly" 

# this section is for calculating the mask from CIDR to Dotted Decimal

def calc(num : int):
    if num < 8:
        ret = 0
        for x in range(num):
            ret += 2**(7-x)
        return ret
    else:
        return 255
    
# this is for calculating the mask form Dotted Decimal to CIDR

def reverse_mask_calc(mask_str: str):
    try:
        octets = mask_str.split('.')
        if len(octets) != 4:
            return None
        cidr = 0
        zero = False
        partial = False
        for octet in octets:
            num = int(octet)
            if num not in [0, 128, 192, 224, 240, 248, 252, 254, 255]:
                return None
            if zero and num != 0:
                return None
            if partial and num != 0:
                return None
            cidr += bin(num).count('1')
            if num == 0:
                zero = True
            elif num != 255:
                partial = True
        return cidr
    except:
        return None
    
# this is for GUI for the main app

current_theme = get_windows_theme()

root = ttk.Window(title="Network calculator", themename=current_theme)

notebook = ttk.Notebook(root, bootstyle=SECONDARY)
notebook.pack(padx=10, pady=10, expand=True, fill=BOTH)

# Tab 1 > CIDR to Dotted Decimal

def get_mask_copy():
    result_text = result_label_tab1.cget("text")
    if 'Decimal:' in result_text:
        clean = result_text.replace('Decimal: ', "")
        tab1.clipboard_clear()
        tab1.clipboard_append(clean)
        copy_btn.configure(text='Copied!', bootstyle=SUCCESS)
        tab1.after(2000, lambda: copy_btn.configure(text="Copy to Clipboard", bootstyle=SECONDARY))

def mask_calc(event = None):
    try:
        mask = int(CIDR_entry.get())
        if not (0 <= mask <= 32):
            result_label_tab1.configure(text='Enter a number 0 - 32', bootstyle=DANGER)
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

        result_label_tab1.configure(text=f'Decimal: {res}',bootstyle=INFO)
        copy_btn.pack(pady=5)
    except ValueError:
        result_label_tab1.configure(text='Invalid Input!', bootstyle=DANGER)
        copy_btn.pack_forget()

# tab 1 > GUI

tab1 = ttk.Frame(notebook, padding=20)

notebook.add(tab1, text='CIDR to Dotted Decimal')

label = ttk.Label(tab1, text='Enter Subnet Mask (e.g.: 24)')
label.pack(padx=20, pady=10)

CIDR_entry = ttk.Entry(tab1)
CIDR_entry.pack(padx=20, pady=5)
CIDR_entry.focus_set()

result_label_tab1 = ttk.Label(tab1, text="")
result_label_tab1.pack(pady=10)

ttk.Button(tab1, text="Calculate", command=mask_calc).pack(pady=10)

copy_btn = ttk.Button(tab1, text="Copy to Clipboard", command=get_mask_copy, bootstyle=SECONDARY)

# tab 2 > copy

def get_cidr_copy():
    result_text = result_label_tab2.cget("text")
    if 'CIDR Notation: /' in result_text:
        clean = result_text.replace('CIDR Notation: /', "")
        tab2.clipboard_clear()
        tab2.clipboard_append(clean)
        copy_cidr_btn.configure(text='Copied!', bootstyle=SUCCESS)
        tab2.after(2000, lambda: copy_btn.configure(text="Copy to Clipboard", bootstyle=SECONDARY))

# tab 2 > Dotted Decimal to CIDR

def reverse_calc(event = None):
    res = reverse_mask_calc(dotted_decimal_entry.get().strip())
    if res is not None:
        result_label_tab2.configure(text=f"CIDR Notation: /{res}", bootstyle=INFO)
        copy_cidr_btn.pack(pady=5)
    else:
        result_label_tab2.configure(text="Invalid Decimal Mask!", bootstyle=DANGER)
        copy_cidr_btn.pack_forget()

# tab 2 > GUI

tab2 = ttk.Frame(notebook, padding=20)
notebook.add(tab2, text='Dotted Decimal to CIDR')

ttk.Label(tab2, text="Enter Mask (e.g. 255.255.255.0)").pack(padx=5, pady=5)
dotted_decimal_entry = ttk.Entry(tab2)
dotted_decimal_entry.pack(pady=5)

result_label_tab2 = ttk.Label(tab2, text="", padding=10)
result_label_tab2.pack()

copy_cidr_btn = ttk.Button(tab2, text="Copy to Clipboard", command=get_cidr_copy(), bootstyle=SECONDARY)
copy_cidr_btn.pack_forget()

ttk.Button(tab2, text="Calculate", command=reverse_calc).pack(pady=10)

# tab 3

class IPCalculatorTab:

    def __init__(self, parent):

        self.frame = ttk.Frame(parent)

        self.container = ttk.Frame(self.frame, padding=20)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        ttk.Label(
            self.container,
            text="Calculation Mode"
        ).grid(row=1, column=0, padx=10, pady=5)

        self.mode_var = tk.StringVar(value="IP + Mask")

        self.mode_box = ttk.Combobox(
            self.container,
            textvariable=self.mode_var,
            values=[
                "IP + Mask",
                "Network + Mask",
                "Broadcast + Mask",
                "IP + CIDR"
            ],
            state="readonly",
            width=25
        )

        self.mode_box.grid(row=1, column=1, pady=5)

        ttk.Label(
            self.container,
            text="IP / Network"
        ).grid(row=2, column=0, padx=10, pady=5)

        self.input1 = ttk.Entry(self.container, width=30)
        self.input1.grid(row=2, column=1, pady=5)

        ttk.Label(
            self.container,
            text="Mask / CIDR"
        ).grid(row=3, column=0, padx=10, pady=5)

        self.input2 = ttk.Entry(self.container, width=30)
        self.input2.grid(row=3, column=1, pady=5)

        self.calc_btn = ttk.Button(
            self.container,
            text="Calculate",
            bootstyle=PRIMARY,
            command=self.calculate
        )

        self.calc_btn.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=20
        )

        self.result_box = ttk.Text(
            self.container,
            height=12,
            width=60
        )

        self.results_visible = False

    def calculate(self):
        if not self.results_visible:
            self.result_box.grid(
                row=5,
                column=0,
                columnspan=2,
                pady=10
            )
            self.results_visible = True

        self.result_box.delete("1.0", tk.END)

        value = self.input1.get().strip()
        mask = self.input2.get().strip()

        try:
            if "." in mask:
                cidr = ipaddress.IPv4Network(
                    f"0.0.0.0/{mask}"
                ).prefixlen
            else:
                cidr = int(mask)

            network = ipaddress.IPv4Network(
                f"{value}/{cidr}",
                strict=False
            )

            first_host = (
                network.network_address + 1
                if network.num_addresses > 2
                else "N/A"
            )

            last_host = (
                network.broadcast_address - 1
                if network.num_addresses > 2
                else "N/A"
            )
            results = f"""
Network Address : {network.network_address}
Broadcast       : {network.broadcast_address}
Subnet Mask     : {network.netmask}
CIDR            : /{network.prefixlen}
Total Hosts     : {network.num_addresses}

First Host      : {first_host}
Last Host       : {last_host}
"""
            self.result_box.insert(tk.END, results)

        except Exception as e:
            self.result_box.insert(tk.END, f"Error:\n{e}")

net_calc = IPCalculatorTab(notebook)
notebook.add(net_calc.frame, text="Network calculator")

# Enter function

def universal_enter(event):
    current_tab = notebook.index("current")
    if current_tab == 0:
        mask_calc()
    elif current_tab == 1:
        reverse_calc()
    else:
        net_calc.calculate()


root.bind('<Return>', universal_enter)

root.mainloop()