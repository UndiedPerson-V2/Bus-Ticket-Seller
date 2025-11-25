# Bus_Select_gui.py
'''
---------------------------------------
ละอองทิพย์ พ่อครวงค์ 1660703016 เลขที่ 11
---------------------------------------
'''


import tkinter as tk
from tkinter import messagebox
from db_connector import get_logged_in_user_info
import login 
import vehicle_confirm_gui 
import Admin_Console_gui


def open_select_bus_screen(prev_root, staff_id):
    """สร้างหน้าจอ Select Bus You Work"""
    if prev_root:
        prev_root.destroy()
    
    bus_root = tk.Tk()
    bus_root.title("Select Bus You Work")
    bus_root.geometry("350x550")
    bus_root.config(bg="#F8E9E4")

    user_data = get_logged_in_user_info(staff_id)
    staff_name = user_data[0] if user_data else "Guest"
    staff_role = user_data[1] if user_data else "Unknown"

    def select_bus(route_number):
        # เมื่อเลือก Route Number ให้ไปหน้ากรอก License Plate
        vehicle_confirm_gui.open_vehicle_confirm_screen(bus_root, staff_id, route_number)

    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            bus_root.destroy()
            login.open_login_screen()

    # --- UI Elements ---
    title = tk.Label(bus_root, text="Select Bus You Work", font=("Arial", 16, "bold"), bg="#F8E9E4")
    title.pack(pady=15)

    frame = tk.Frame(bus_root, bg="#F8E9E4")
    frame.pack(pady=10, padx=10)

    # ใช้ RouteNumber ที่มีใน DB
    bus_routes = ['39', '520', '34', '1-31', '185'] 

    for i, p in enumerate(bus_routes):
        cmd = lambda r=p: select_bus(r)
        btn = tk.Button(frame, text=str(p), width=6, height=3,
                        command=cmd,
                        bg="#FFFFFF",
                        font=("Arial", 12, "bold"),
                        relief="solid", bd=1)
        btn.grid(row=i//3, column=i%3, padx=10, pady=10)
    
    avatar_frame = tk.Frame(bus_root, width=100, height=100, bg="#A0C3E6", borderwidth=0) 
    avatar_frame.pack(pady=20)

    welcome_text = f"Welcome Khun {staff_name}"
    note = tk.Label(bus_root, text=welcome_text, bg="#F8E9E4", font=("Arial", 12))
    note.pack(pady=5)

    logout_btn = tk.Button(bus_root, text="Logout", width=10,
                        command=logout,
                        bg="#AEE0FE",
                        relief="solid", bd=1)
    logout_btn.pack(pady=10)

    if staff_role == 'Admin':
        def open_admin():
            Admin_Console_gui.open_admin_console(bus_root, staff_id)

        admin_btn = tk.Button(bus_root, text="⚙️ Admin Console", 
                              command=open_admin,
                              fg="black", bg="#F8E9E4", relief=tk.RAISED, font=("Arial", 10, "bold"))
        admin_btn.pack(pady=10)

    bus_root.mainloop()