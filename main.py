from tkinter import Tk
from gui.login import LoginPage

def main():
    root = Tk()
    root.geometry("300x250")
    root.title("Login Page")
    root.resizable(False,False)

    app = LoginPage(root)
    app.pack(expand=True, fill='both')  # مهم: اضافه کردن Frame به پنجره اصلی

    root.mainloop()

if __name__ == "__main__":
    main()
