import tkinter as tk
import hashlib
from tkinter import messagebox
from core.login_core import LoginCore
from gui.ToDoList import ToDoListUI

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.top_bar_color = "#3B82F6"
        self.button_color = "#2563EB"
        self.button_fg = "#ffffff"
        self.core=LoginCore()

        self.configure(bg=self.top_bar_color)
        
        loginlbl=tk.Label(self,text='LOGIN', width=10, bg=self.top_bar_color, fg="white")
        loginlbl.grid(row=0, column=1, columnspan=2,pady=(0,50),padx=(0,30))

        user_lbl = tk.Label(self, text="Username:", width=10, bg=self.top_bar_color, fg="white")
        user_lbl.grid(row=0, column=0, pady=30, padx=10)
        
        self.user_entry = tk.Entry(self, width=25)
        self.user_entry.grid(row=0, column=1, pady=30)
    
        pass_lbl = tk.Label(self, text="Password:", width=10, bg=self.top_bar_color, fg="white")
        pass_lbl.grid(row=1, column=0, padx=10)
        
        self.pass_entry = tk.Entry(self, width=25, show="*")
        self.pass_entry.grid(row=1, column=1)
        
        login_btn = tk.Button(self, text='Login', width=15, bg=self.button_color, fg=self.button_fg,command=self.login)
        login_btn.grid(row=2, column=1, columnspan=2, pady=20,padx=(0,30))

        sign_up = tk.Button(self, text='Sign up', width=15, bg=self.button_color, fg=self.button_fg,command=self.sign_up)
        sign_up.grid(row=3, column=1, columnspan=2,padx=(0,30))

    def sign_up(self):
        sup=tk.Toplevel(self)
        sup.geometry('300x250')
        sup.title('Sign up Page')
        sup.resizable(False,False)

        su_lbl=tk.Label(sup,text='SIGN UP', width=10)
        su_lbl.grid(row=0, column=1, columnspan=2,pady=(0,50),padx=(0,30))

        user_lbl=tk.Label(sup,text='Username:',width=10)
        user_lbl.grid(row=0, column=0, pady=30, padx=10)

        self.suser_ent=tk.Entry(sup,width=25)
        self.suser_ent.grid(row=0, column=1, pady=30)
        
        spass_lbl=tk.Label(sup,text='Password:')
        spass_lbl.grid(row=1, column=0, pady=10)

        self.spass_ent=tk.Entry(sup,width=25,show='*')
        self.spass_ent.grid(row=1, column=1, pady=10)
        

        su_btn=tk.Button(sup, text='sign up', width=15,command=self.sign_up_btn)
        su_btn.grid(row=2, column=1, columnspan=2, pady=20,padx=(0,30))
    
    def hash_pwd(self,password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def sign_up_btn(self):
        susername=self.suser_ent.get()
        spassword=self.spass_ent.get()
        
        
        if spassword and susername:
            hashed_pwd=self.hash_pwd(spassword)
            status =self.core.register(username=susername,password=hashed_pwd)
            
            if status=='exist':
                messagebox.showwarning(message='user already exist!')
            elif status=='successful':
                messagebox.showinfo(message="your account has been created!")
            else:
                messagebox.showerror(message=f"Database error: {status}")
        else:
            messagebox.showwarning(message="Please enter both username and password.")
    def login(self):
        luser=self.user_entry.get()
        lpass=self.pass_entry.get()

        if luser and lpass:
            hashedpass=self.hash_pwd(lpass)
            info=self.core.login(luser,hashedpass)

            if info['status'] == 'successful':
                messagebox.showinfo(message=f'login successful your uid is: {info['uid']}')

                self.master.withdraw()  # پنهان کردن لاگین
                root_main = tk.Toplevel()
                root_main.geometry('960x600')
                def on_main_close():
                    root_main.destroy()
                    self.master.destroy()

                root_main.protocol("WM_DELETE_WINDOW", on_main_close)
                ToDoListUI(root_main,info['uid']).pack(expand=True, fill="both")

            elif info['status']=='wrong':
                messagebox.showwarning(message='username or password is wrong!')

            else:
                messagebox.showerror(message='unknown error')
