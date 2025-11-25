# vehicle_confirm_gui.py
'''
---------------------------------------
ธรรมสรณ์ ทองคำ 16607062593 เลขที่ 38
---------------------------------------
'''
import tkinter as tk
from tkinter import messagebox
from db_connector import check_vehicle_and_get_route 
import Bus_Select_gui 
import ticket_price_gui

def open_vehicle_confirm_screen(prev_root, staff_id, route_number):
    """สร้างหน้าจอให้พนักงานกรอก License Plate เพื่อยืนยัน"""
    if prev_root:
        prev_root.destroy()
    
    confirm_root = tk.Tk()
    confirm_root.title(f"Confirm Vehicle (Route {route_number})")
    confirm_root.geometry("350x300")
    confirm_root.config(bg="#F8E9E4")

    def confirm_action():
        license_plate = vehicle_entry.get().strip() # รับ License Plate
        
        if not license_plate:
            messagebox.showwarning("Warning", "กรุณากรอกเลขทะเบียนรถ (License Plate)")
            return
            
        # 1. ตรวจสอบ License Plate กับ Route Number
        # Result: (is_valid, VehicleID, RouteID, RouteDescription)
        is_valid, vehicle_id, route_id, route_description = check_vehicle_and_get_route(license_plate, route_number)

        if is_valid:
            messagebox.showinfo("Success", f"License Plate {license_plate} confirmed for Route {route_number}!")
            
            # 2. เมื่อยืนยันสำเร็จ ส่ง Vehicle ID ภายใน ไปหน้าเลือกราคา
            ticket_price_gui.open_select_price_screen(confirm_root, staff_id, route_number, vehicle_id, route_id, route_description)
            
        else:
            # 3. แจ้งเตือนถ้าไม่ตรงกัน
            messagebox.showerror("Invalid ID", 
                                 f"License Plate '{license_plate}' ไม่ตรงกับสาย {route_number} ในระบบ\nกรุณาลองใหม่อีกครั้ง")
            vehicle_entry.delete(0, tk.END) # ล้างช่องกรอก

    def go_back():
        """กลับไปหน้า Select Bus You Work"""
        Bus_Select_gui.open_select_bus_screen(confirm_root, staff_id)

    # --- UI Elements ---
    title = tk.Label(confirm_root, text=f"Route: {route_number}", font=("Arial", 16, "bold"), bg="#F8E9E4")
    title.pack(pady=15)
    
    instruction = tk.Label(confirm_root, text="Enter License Plate (e.g., 10-5311):", bg="#F8E9E4")
    instruction.pack(pady=5)
    
    vehicle_entry = tk.Entry(confirm_root, width=20, font=('Arial', 12))
    vehicle_entry.pack(ipady=5)
    
    confirm_btn = tk.Button(confirm_root, text="Confirm Plate", width=20,
                        command=confirm_action, 
                        bg="#28a745", fg="white",
                        relief="flat", bd=0)
    confirm_btn.pack(pady=20)

    back_btn = tk.Button(confirm_root, text="Back to Select Route", width=20,
                        command=go_back,
                        bg="#f8d7da", fg="#721c24",
                        relief="flat", bd=0)
    back_btn.pack(pady=10)


    confirm_root.mainloop()