# login.py

import tkinter as tk
from tkinter import messagebox
from db_connector import authenticate_user
import Bus_Select_gui 

def open_login_screen():
    """สร้างหน้าจอ Login"""
    login_root = tk.Tk()
    login_root.title("Login UI")
    login_root.geometry("350x550") 
    login_root.resizable(False, False) 
    login_root.configure(bg="#f0f0f0") 

    def login_attempt():
        username = user_entry.get()
        password = pass_entry.get()
        
        if not username or not password:
             messagebox.showwarning("Warning", "กรุณากรอก Username และ Password ให้ครบถ้วน")
             return

        user_info = authenticate_user(username, password)

        if user_info:
            staff_id, staff_name, staff_role = user_info
            messagebox.showinfo("Success", f"Login สำเร็จ! ยินดีต้อนรับคุณ {staff_name}")
            
            Bus_Select_gui.open_select_bus_screen(login_root, staff_id)
            
        else:
            messagebox.showerror("Error", "Username หรือ Password ไม่ถูกต้อง!")

    # --- UI Elements ---
    mobile_frame = tk.Frame(login_root, bg="white", width=300, height=550)
    mobile_frame.pack_propagate(False) 
    mobile_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    title_label = tk.Label(mobile_frame, text="Login", font=("Arial", 24, "bold"), bg="white")
    title_label.pack(pady=(70, 40))

    widget_frame = tk.Frame(mobile_frame, bg="white")
    widget_frame.pack(padx=20, fill="x")

    user_entry = tk.Entry(widget_frame, width=30, font=('Arial', 12))
    pass_entry = tk.Entry(widget_frame, show="*", width=30, font=('Arial', 12))

    username_label = tk.Label(widget_frame, text="Username", bg="white")
    username_label.pack(fill="x", pady=(10, 2))
    user_entry.pack(fill="x", ipady=3) 

    password_label = tk.Label(widget_frame, text="Password", bg="white")
    password_label.pack(fill="x", pady=(15, 2))
    pass_entry.pack(fill="x", ipady=3)

    BLUE_COLOR = "#3498db" 
    HOVER_COLOR = "#5dade2" 

    login_btn = tk.Button(
        widget_frame, 
        text="Login", 
        command=login_attempt, 
        font=('Arial', 12, 'bold'),
        fg="white", 
        bg=BLUE_COLOR, 
        activebackground=HOVER_COLOR, 
        activeforeground="white", 
        borderwidth=0, 
        relief="flat" 
    )
    login_btn.pack(fill="x", pady=(30, 20), ipady=5) 

    login_root.mainloop()

# Start Application
if __name__ == "__main__":
    open_login_screen()