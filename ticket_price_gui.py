# ticket_price_gui.py

import tkinter as tk
from tkinter import messagebox
from db_connector import get_fare_rates, connect_db 
import vehicle_confirm_gui 
import ticket_print 
from datetime import datetime 

# ================== Function ==================

def confirm_ticket(price, root, staff_id, route_number, vehicle_id, route_id, route_description):
    """แสดง Pop-up ยืนยันราคา และบันทึกข้อมูลตั๋วลง DB ก่อนไปหน้าพิมพ์"""
    
    answer = messagebox.askyesno("Confirm this ticket?", f"Ticket Price: {price} THB\nConfirm purchase?")
    
    if answer:
        conn = connect_db()
        if conn:
            try:
                # 1. สร้าง Ticket No (ใช้ VehicleID)
                current_time = datetime.now()
                ticket_no = f"TKT{vehicle_id}-{current_time.strftime('%Y%m%d%H%M%S')}" 
                
                cursor = conn.cursor()
                
                # 2. คำสั่ง INSERT ข้อมูลลงตาราง TICKET
                # Fields: TicketNo, VehicleID, StaffID, Price, RouteID, Datetime, TicketStatus
                query = """
                INSERT INTO TICKET (TicketNo, VehicleID, StaffID, Price, RouteID, Datetime, TicketStatus) 
                VALUES (?, ?, ?, ?, ?, ?, 'Active')
                """
                
                cursor.execute(query, 
                               ticket_no, 
                               vehicle_id, 
                               staff_id, # StaffID เป็น INT ใน DB
                               price, 
                               route_id, 
                               current_time)
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Ticket {ticket_no} confirmed and saved to DB!")
                
                # 3. ส่งข้อมูลทั้งหมดไปหน้า Ticket Print
                ticket_print.open_ticket_print_screen(root, staff_id, route_number, vehicle_id, price, route_description)
                return
                
            except Exception as e:
                if conn: conn.close()
                messagebox.showerror("DB Error", f"Failed to save ticket: {e}")
                return 
        
        else:
            messagebox.showerror("DB Connection", "Could not connect to database to save ticket.")

    else:
        messagebox.showinfo("Cancel", "Purchase Canceled")


def open_select_price_screen(prev_root, staff_id, route_number, vehicle_id, route_id, route_description):
    """ฟังก์ชันหลักสำหรับสร้างหน้าจอ Select Ticket Price"""
    if prev_root:
        prev_root.destroy()
    
    root = tk.Tk()
    root.title(f"Select Price (Route {route_number} / Car {vehicle_id})")
    root.geometry("350x550")
    root.config(bg="#F8E9E4")

    def go_back():
        """กลับไปหน้า Vehicle Confirm (License Plate)"""
        # กลับไปหน้า Vehicle Confirm พร้อมข้อมูลเดิม
        vehicle_confirm_gui.open_vehicle_confirm_screen(root, staff_id, route_number)

    # Title
    title = tk.Label(root, text=f"Route: {route_number}", font=("Arial", 16, "bold"), bg="#F8E9E4")
    title.pack(pady=15)
    
    # Subtitle for vehicle
    subtitle = tk.Label(root, text=f"Vehicle ID: {vehicle_id}", font=("Arial", 12), bg="#F8E9E4", fg="blue")
    subtitle.pack(pady=5)

    # Button Frame
    frame = tk.Frame(root, bg="#F8E9E4")
    frame.pack(pady=10)

    prices = get_fare_rates()

    # Create Price Buttons
    for i, p in enumerate(prices):
        cmd = lambda price=p: confirm_ticket(price, root, staff_id, route_number, vehicle_id, route_id, route_description)
        
        btn = tk.Button(frame, text=str(p), width=8, height=2,
                        command=cmd,
                        bg="#FFFFFF",
                        font=("Arial", 14, "bold"),
                        relief="solid", bd=1)
        btn.grid(row=i//2, column=i%2, padx=10, pady=10)

    # Note
    note = tk.Label(root, text="Please Select Correct Price", bg="#F8E9E4", font=("Arial", 10))
    note.pack(pady=10)
    
    # Back Button
    back_btn = tk.Button(root, text="Back (Change Vehicle)", width=20,
                         command=go_back,
                         bg="#AEE0FE",
                         relief="solid", bd=1)
    back_btn.pack(pady=20)

    root.mainloop()