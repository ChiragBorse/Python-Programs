import tkinter as tk
from tkinter import ttk, messagebox

# ------------------- Account Class -------------------

class BankAccount:
    def __init__(self):
        self.username = "admin"
        self.password = "1234"
        self.balance = 5000
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"Deposited ₹{amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        self.history.append(f"Withdrawn ₹{amount}")
        return True

account = BankAccount()

# ------------------- Login -------------------

def login():
    if user_entry.get() == account.username and pass_entry.get() == account.password:
        login_frame.pack_forget()
        dashboard.pack(fill="both", expand=True)
        update_balance()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# ------------------- Functions -------------------

def update_balance():
    balance_label.config(text=f"Current Balance : ₹{account.balance}")

def deposit():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError

        account.deposit(amount)
        update_balance()
        transaction_box.insert(tk.END, f"Deposited ₹{amount}\n")
        amount_entry.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Enter Valid Amount")

def withdraw():
    try:
        amount = float(amount_entry.get())

        if amount <= 0:
            raise ValueError

        if account.withdraw(amount):
            update_balance()
            transaction_box.insert(tk.END, f"Withdrawn ₹{amount}\n")
        else:
            messagebox.showwarning("Warning", "Insufficient Balance")

        amount_entry.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Enter Valid Amount")

def show_history():
    transaction_box.delete("1.0", tk.END)

    if account.history:
        for item in account.history:
            transaction_box.insert(tk.END, item + "\n")
    else:
        transaction_box.insert(tk.END, "No Transactions Yet")

# ------------------- Window -------------------

root = tk.Tk()
root.title("Bank Management System")
root.geometry("650x500")
root.configure(bg="#EAF2F8")

style = ttk.Style()
style.theme_use("clam")

# ------------------- Login Frame -------------------

login_frame = tk.Frame(root, bg="#EAF2F8")

tk.Label(
    login_frame,
    text="BANK LOGIN",
    font=("Arial", 20, "bold"),
    bg="#EAF2F8",
    fg="navy"
).pack(pady=20)

tk.Label(login_frame, text="Username", bg="#EAF2F8").pack()

user_entry = ttk.Entry(login_frame, width=30)
user_entry.pack(pady=5)

tk.Label(login_frame, text="Password", bg="#EAF2F8").pack()

pass_entry = ttk.Entry(login_frame, show="*", width=30)
pass_entry.pack(pady=5)

ttk.Button(login_frame, text="Login", command=login).pack(pady=20)

login_frame.pack(fill="both", expand=True)

# ------------------- Dashboard -------------------

dashboard = tk.Frame(root, bg="#EAF2F8")

title = tk.Label(
    dashboard,
    text="Bank Dashboard",
    font=("Arial", 18, "bold"),
    bg="#EAF2F8",
    fg="darkgreen"
)
title.pack(pady=10)

balance_label = tk.Label(
    dashboard,
    text="Current Balance",
    font=("Arial", 14),
    bg="#EAF2F8"
)
balance_label.pack()

amount_entry = ttk.Entry(dashboard, width=30)
amount_entry.pack(pady=10)

button_frame = tk.Frame(dashboard, bg="#EAF2F8")
button_frame.pack()

ttk.Button(
    button_frame,
    text="Deposit",
    command=deposit
).grid(row=0, column=0, padx=10)

ttk.Button(
    button_frame,
    text="Withdraw",
    command=withdraw
).grid(row=0, column=1, padx=10)

ttk.Button(
    button_frame,
    text="History",
    command=show_history
).grid(row=0, column=2, padx=10)

transaction_box = tk.Text(
    dashboard,
    width=60,
    height=15,
    font=("Consolas", 10)
)
transaction_box.pack(pady=20)

root.mainloop()
