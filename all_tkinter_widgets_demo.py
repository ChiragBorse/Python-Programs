import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import time

root = tk.Tk()
root.title("Python Tkinter Components Showcase")
root.geometry("1200x700")

# ===========================
# MENU
# ===========================
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)

def open_file():
    filename = filedialog.askopenfilename()
    if filename:
        messagebox.showinfo("Selected File", filename)

def save_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        messagebox.showinfo("Saved", filename)

file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Tkinter Widgets Showcase"))

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

# ===========================
# TOOLBAR
# ===========================
toolbar = tk.Frame(root, bg="#d9d9d9")

tk.Button(toolbar, text="Open", command=open_file).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="Save", command=save_file).pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="Exit", command=root.destroy).pack(side=tk.LEFT, padx=2)

toolbar.pack(fill=tk.X)

# ===========================
# NOTEBOOK
# ===========================
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

notebook.add(tab1, text="Widgets")
notebook.add(tab2, text="Data")
notebook.add(tab3, text="Canvas")

# ===========================
# LEFT FRAME
# ===========================
left = ttk.Frame(tab1)
left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

right = ttk.Frame(tab1)
right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

# ===========================
# LABEL FRAME
# ===========================
user_frame = ttk.LabelFrame(left, text="User Details")
user_frame.pack(fill=tk.X, pady=5)

ttk.Label(user_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)

name_entry = ttk.Entry(user_frame)
name_entry.grid(row=0, column=1)

ttk.Label(user_frame, text="Password").grid(row=1, column=0)

pass_entry = ttk.Entry(user_frame, show="*")
pass_entry.grid(row=1, column=1)

# ===========================
# CHECKBUTTONS
# ===========================
check_frame = ttk.LabelFrame(left, text="Skills")
check_frame.pack(fill=tk.X, pady=5)

python_var = tk.BooleanVar()
java_var = tk.BooleanVar()

ttk.Checkbutton(check_frame, text="Python", variable=python_var).pack(anchor="w")
ttk.Checkbutton(check_frame, text="Java", variable=java_var).pack(anchor="w")

# ===========================
# RADIOBUTTONS
# ===========================
gender = tk.StringVar()

radio_frame = ttk.LabelFrame(left, text="Gender")
radio_frame.pack(fill=tk.X)

ttk.Radiobutton(radio_frame, text="Male", variable=gender, value="Male").pack(anchor="w")
ttk.Radiobutton(radio_frame, text="Female", variable=gender, value="Female").pack(anchor="w")
ttk.Radiobutton(radio_frame, text="Other", variable=gender, value="Other").pack(anchor="w")

# ===========================
# COMBOBOX
# ===========================
ttk.Label(left, text="Country").pack()

country = ttk.Combobox(left, values=["India","USA","Canada","UK","Australia"])
country.current(0)
country.pack(fill=tk.X)

# ===========================
# SPINBOX
# ===========================
ttk.Label(left, text="Age").pack()

spin = tk.Spinbox(left, from_=1, to=100)
spin.pack(fill=tk.X)

# ===========================
# SCALE
# ===========================
ttk.Label(left, text="Volume").pack()

scale = ttk.Scale(left, from_=0, to=100)
scale.pack(fill=tk.X)

# ===========================
# TEXT
# ===========================
ttk.Label(right, text="Notes")

text = tk.Text(right, height=12)
scroll = ttk.Scrollbar(right, command=text.yview)
text.config(yscrollcommand=scroll.set)

text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# ===========================
# BUTTONS
# ===========================
button_frame = ttk.Frame(left)
button_frame.pack(pady=10)

def submit():

    info = f"""
Name : {name_entry.get()}
Password : {pass_entry.get()}
Country : {country.get()}
Age : {spin.get()}
Gender : {gender.get()}
Python : {python_var.get()}
Java : {java_var.get()}
"""

    messagebox.showinfo("Information", info)

ttk.Button(button_frame, text="Submit", command=submit).grid(row=0,column=0,padx=5)

ttk.Button(button_frame,text="Choose Color",
           command=lambda: colorchooser.askcolor()).grid(row=0,column=1,padx=5)

# ===========================
# TREEVIEW
# ===========================
tree = ttk.Treeview(tab2, columns=("Name","Age","Country"), show="headings")

tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Country", text="Country")

tree.insert("",tk.END,values=("Chirag",20,"India"))
tree.insert("",tk.END,values=("Alice",22,"USA"))
tree.insert("",tk.END,values=("John",25,"Canada"))

tree.pack(fill=tk.BOTH, expand=True,padx=10,pady=10)

# ===========================
# LISTBOX
# ===========================
listbox = tk.Listbox(tab2,height=6)

languages=["Python","Java","C","C++","JavaScript","Go","Rust"]

for item in languages:
    listbox.insert(tk.END,item)

listbox.pack(pady=10)

# ===========================
# PROGRESSBAR
# ===========================
progress = ttk.Progressbar(tab2,length=400,mode="determinate")
progress.pack(pady=20)

def loading():
    progress["value"]=0

    for i in range(101):
        root.update()
        progress["value"]=i
        time.sleep(0.01)

ttk.Button(tab2,text="Start Progress",command=loading).pack()

# ===========================
# CANVAS
# ===========================
canvas=tk.Canvas(tab3,bg="white")
canvas.pack(fill=tk.BOTH,expand=True)

canvas.create_rectangle(50,50,200,150,fill="skyblue")
canvas.create_oval(250,50,400,150,fill="orange")
canvas.create_line(50,200,400,200,width=4)
canvas.create_text(220,260,text="Tkinter Canvas",font=("Arial",20))

# ===========================
# STATUS BAR
# ===========================
status=tk.StringVar()
status.set("Ready")

statusbar=ttk.Label(root,textvariable=status,relief=tk.SUNKEN,anchor="w")
statusbar.pack(fill=tk.X,side=tk.BOTTOM)

# ===========================
# DIGITAL CLOCK
# ===========================
clock=tk.Label(toolbar,font=("Arial",12,"bold"))

clock.pack(side=tk.RIGHT,padx=20)

def update_clock():
    clock.config(text=time.strftime("%H:%M:%S"))
    clock.after(1000,update_clock)

update_clock()

# ===========================
# SHORTCUTS
# ===========================
root.bind("<Control-o>",lambda e:open_file())
root.bind("<Control-s>",lambda e:save_file())
root.bind("<Escape>",lambda e:root.destroy())

root.mainloop()
