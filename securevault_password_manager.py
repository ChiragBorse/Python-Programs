import tkinter as tk
from tkinter import ttk,messagebox
import random,string

class Vault:
    def __init__(self,r):
        self.data=[]; self.r=r; r.title("SecureVault Password Manager")
        f=tk.Frame(r,padx=10,pady=10); f.pack(fill="x")
        self.vars={}
        for i,l in enumerate(("Website","Username","Password")):
            tk.Label(f,text=l).grid(row=0,column=i,sticky="w")
            v=tk.StringVar(); self.vars[l]=v
            show="*" if l=="Password" else ""
            tk.Entry(f,textvariable=v,show=show,width=22).grid(row=1,column=i,padx=5)
        tk.Button(f,text="Generate",command=self.gen).grid(row=1,column=3,padx=5)
        b=tk.Frame(r); b.pack(fill="x")
        for t,c in [("Add",self.add),("Delete",self.delete),("Copy Password",self.copy)]:
            tk.Button(b,text=t,command=c).pack(side="left",padx=5)
        tk.Label(b,text="Search").pack(side="left",padx=(20,5))
        self.s=tk.StringVar()
        e=tk.Entry(b,textvariable=self.s); e.pack(side="left")
        e.bind("<KeyRelease>",lambda x:self.refresh())
        cols=("Website","Username","Password")
        self.t=ttk.Treeview(r,columns=cols,show="headings",height=12)
        for c in cols:
            self.t.heading(c,text=c); self.t.column(c,width=180)
        self.t.pack(fill="both",expand=True,padx=10,pady=10)
        self.t.bind("<<TreeviewSelect>>",self.sel)
    def gen(self):
        p=''.join(random.choice(string.ascii_letters+string.digits+"@#$%") for _ in range(12))
        self.vars["Password"].set(p)
    def add(self):
        w,u,p=[self.vars[k].get().strip() for k in ("Website","Username","Password")]
        if not(w and u and p): messagebox.showerror("Error","Fill all fields"); return
        self.data.append([w,u,p]); self.refresh()
        [v.set("") for v in self.vars.values()]
    def refresh(self):
        [self.t.delete(i) for i in self.t.get_children()]
        q=self.s.get().lower()
        for d in self.data:
            if q and q not in d[0].lower() and q not in d[1].lower(): continue
            self.t.insert("",tk.END,values=d)
    def sel(self,e=None):
        it=self.t.focus()
        if it:self.cur=self.t.item(it)["values"]
    def delete(self):
        if not hasattr(self,"cur"): return
        self.data.remove(self.cur); self.refresh()
    def copy(self):
        if not hasattr(self,"cur"): return
        self.r.clipboard_clear(); self.r.clipboard_append(self.cur[2])
        messagebox.showinfo("Copied","Password copied.")
root=tk.Tk(); Vault(root); root.mainloop()
