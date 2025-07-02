import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from core.ToDo_logic import ToDoListCore
import os
import sys
import tkinter.font as tkfont
from pathlib import Path

# font_path = os.path.join(Path(__file__).resolve().parent, "..", "fonts", "Vazirmatn.ttf")
# tkfont.Font(family="Vazirmatn", size=12)

def load_custom_font(font_file_name, font_family_name, size=12):
    from ctypes import windll
    # مسیر فایل فونت
    if hasattr(sys, "_MEIPASS"):
        font_path = os.path.join(sys._MEIPASS, "fonts", font_file_name)
    else:
        font_path = os.path.join("fonts", font_file_name)

    if os.name == "nt":  # فقط برای ویندوز
        FR_PRIVATE  = 0x10
        FR_NOT_ENUM = 0x20
        windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)

    return tkfont.Font(family=font_family_name, size=size)

class ToDoListUI(tk.Frame):
    def __init__(self, master,uid):
        super().__init__(master)
        
        self.master = master
        self.todo_list=ToDoListCore(user_id=uid)
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(bg="#F3F4F6")  # Main background

        self.my_font = load_custom_font("Vazirmatn.ttf", "Vazirmatn", size=12)

        self.selected_task_index = None

        # Colors
        top_bar_color = "#3B82F6"
        right_bg = "#E0F2FE"
        button_color = "#2563EB"
        button_fg = "#ffffff"

        
        # Main grid layout
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        # Top bar
        top_bar = tk.Frame(self, bg=top_bar_color, height=60)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        top_bar.columnconfigure(0, weight=1)
        top_bar.columnconfigure(1, weight=1)
        top_bar.columnconfigure(2, weight=1)

        menu_lbl = tk.Label(top_bar, text="≡ Menu", bg=top_bar_color, fg="white", font=self.my_font, anchor="w")
        menu_lbl.grid(row=0, column=0, sticky="w", padx=20)

        title_lbl = tk.Label(top_bar, text="📝 To-Do List", bg=top_bar_color, fg="white", font=("Vazirmatn", 14, "bold"))
        title_lbl.grid(row=0, column=1, sticky="n")

        profile_lbl = tk.Label(top_bar, text="👤 Profile", bg=top_bar_color, fg="white", font=self.my_font, anchor="e")
        profile_lbl.grid(row=0, column=2, sticky="e", padx=20)

        # Left frame (task list)
        left_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        left_frame.grid(row=1, column=0, sticky="nsew")

        columns = ("subject", "description")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        self.tree.heading("subject", text="Subject")
        self.tree.heading("description", text="Description")
        self.tree.column("subject", width=120)
        self.tree.column("description", width=240)
        self.tree.pack(fill="both", expand=True)

        # Edit/Delete buttons under the table
        btn_frame = tk.Frame(left_frame, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(10, 0))

        edit_btn = tk.Button(btn_frame, text="✏️ Edit", font=self.my_font, width=10,
                             bg=button_color, fg=button_fg, activebackground="#1D4ED8",command=self.edit_btn)
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(btn_frame, text="🗑️ Delete", font=self.my_font, width=10,
                               bg="#EF4444", fg="white", activebackground="#DC2626",command=self.remove_btn)
        delete_btn.pack(side="right", padx=5)

        # Right frame (add task form)
        right_frame = tk.Frame(self, bg=right_bg, padx=20, pady=20)
        right_frame.grid(row=1, column=1, sticky="nsew")

        tk.Label(right_frame, text="Subject:", font=self.my_font, bg=right_bg).grid(row=0, column=0, sticky="w")
        self.subject_entry = tk.Entry(right_frame, font=self.my_font, width=30)
        self.subject_entry.grid(row=1, column=0, pady=(0, 20), sticky="w")

        tk.Label(right_frame, text="Description:", font=self.my_font, bg=right_bg).grid(row=2, column=0, sticky="w")
        self.description_text = tk.Text(right_frame, font=self.my_font, width=30, height=10)
        self.description_text.grid(row=3, column=0, pady=(0, 20), sticky="w")

        self.add_btn = tk.Button(right_frame, text="➕ Add Task", font=self.my_font, width=20,
                            bg=button_color, fg=button_fg, activebackground="#1D4ED8",command=self.on_btn)
        self.add_btn.grid(row=4, column=0, sticky="w")

        #save button will be placed after you select atsk and click on edit button
        self.save_btn=tk.Button(right_frame, text="💾 Save", font=self.my_font, width=20,
                            bg=button_color, fg=button_fg, activebackground="#1D4ED8",command=self.on_save_btn)
        self.refresh_task_list()

    def refresh_task_list(self):
        #remove old task
        for row in self.tree.get_children():
            self.tree.delete(row)
        #add new task
        for idx,task in enumerate(self.todo_list.get_tasks()):
            self.tree.insert("","end",iid=idx,values=(task['subject'],task['description']))
        
    def on_btn(self):
        subject = self.subject_entry.get()
        desc = self.description_text.get("1.0", "end")
        self.todo_list.add_task(subject, desc)
        self.refresh_task_list()
        self.subject_entry.delete(0, "end")
        self.description_text.delete("1.0", "end")

    def remove_btn(self):
        index=self.tree.selection()
        if index:
            index_id=int(index[0])
            self.todo_list.remove_task(index=index_id)
            self.refresh_task_list()

    def edit_btn(self):
        selected = self.tree.selection()
        if selected:
            idx = int(selected[0])
            task = self.todo_list.get_tasks()[idx]

            # مقداردهی به فرم سمت راست
            self.subject_entry.delete(0, "end")
            self.subject_entry.insert(0, task["subject"])

            self.description_text.delete("1.0", "end")
            self.description_text.insert("1.0", task["description"])

            # ذخیره index برای استفاده در update
            self.selected_task_index = idx

            #add edit button
            self.add_btn.grid_forget()
            self.save_btn.grid(row=4, column=0, sticky="w")
    
    def on_save_btn(self):
        subject = self.subject_entry.get().strip()
        description = self.description_text.get("1.0", "end").strip()

        if self.selected_task_index is None:
            # اضافه کردن تسک جدید
            self.todo_list.add_task(subject, description)
        else:
            # ویرایش تسک موجود
            self.todo_list.edit_task(self.selected_task_index, subject, description)
            self.selected_task_index = None  # ریست برای عملیات بعدی

        self.refresh_task_list()
        self.subject_entry.delete(0, "end")
        self.description_text.delete("1.0", "end")
        self.save_btn.grid_forget()
        self.add_btn.grid(row=4, column=0, sticky="w")
