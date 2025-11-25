# Admin_Console_gui.py
'''
---------------------------------------
ธนากร กระสายกลาง 1660703172 เลขที่ 15
--------------------------------------- 
'''
import tkinter as tk
from tkinter import ttk, messagebox
from db_connector import (
    get_staff_list, 
    get_sales_report, 
    add_staff, 
    update_staff, 
    delete_staff
)
import Bus_Select_gui

def open_admin_console(prev_root, staff_id):
    """สร้างหน้าจอ Admin Console"""
    if prev_root:
        prev_root.destroy()
    
    admin_root = tk.Tk()
    admin_root.title("Admin Console")
    admin_root.geometry("1000x700")
    
    notebook = ttk.Notebook(admin_root)
    notebook.pack(pady=10, padx=10, expand=True, fill="both")

    # --- Tab 1: Sales Report ---
    sales_frame = ttk.Frame(notebook)
    notebook.add(sales_frame, text="ยอดขายตั๋ว (Sales Report) 📊")
    
    # Treeview for Sales Data
    sales_tree = ttk.Treeview(sales_frame, columns=("RouteNumber", "TotalSales", "TotalTickets"), show='headings')
    sales_tree.heading("RouteNumber", text="เลขสายรถ")
    sales_tree.heading("TotalSales", text="ยอดขายรวม (THB)")
    sales_tree.heading("TotalTickets", text="จำนวนตั๋วรวม")
    sales_tree.column("RouteNumber", width=100, anchor=tk.CENTER)
    sales_tree.column("TotalSales", width=200, anchor=tk.E)
    sales_tree.column("TotalTickets", width=200, anchor=tk.CENTER)
    
    vsb = ttk.Scrollbar(sales_frame, orient="vertical", command=sales_tree.yview)
    sales_tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    sales_tree.pack(expand=True, fill="both")
    
    def load_sales_data():
        for item in sales_tree.get_children():
            sales_tree.delete(item)
        data = get_sales_report()
        for row in data:
            route_number, total_sales, total_tickets = row
            sales_tree.insert("", tk.END, values=(route_number, f"{total_sales:,.2f}", total_tickets))

    load_sales_data()
    
    # --- Tab 2: Staff Management (พร้อม CRUD) ---
    staff_frame = ttk.Frame(notebook)
    notebook.add(staff_frame, text="จัดการพนักงาน (Staff Management) 🧑‍💼")
    
    # Input Frame for CRUD Operations
    input_frame = tk.LabelFrame(staff_frame, text="จัดการข้อมูลพนักงาน", padx=10, pady=10)
    input_frame.pack(pady=10, padx=10, fill="x")

    labels = ["StaffID", "ชื่อ", "ตำแหน่ง (Admin/Staff)", "Username", "Password"]
    entries = {}
    
    for i, text in enumerate(labels):
        tk.Label(input_frame, text=text).grid(row=0, column=i, padx=5, pady=5)
        entry = tk.Entry(input_frame, width=15)
        entry.grid(row=1, column=i, padx=5, pady=5)
        entries[text] = entry

    # Functions for Staff CRUD
    def load_staff_data():
        for item in staff_tree.get_children():
            staff_tree.delete(item)
        data = get_staff_list()
        for row in data:
            staff_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4])) 

    def clear_entries():
        for entry in entries.values():
            entry.delete(0, tk.END)
    
    def on_staff_select(event):
        clear_entries()
        selected_item = staff_tree.focus()
        if selected_item:
            values = staff_tree.item(selected_item, 'values')
            if values:
                keys = list(entries.keys())
                for key, value in zip(keys, values):
                    entries[key].insert(0, value)

    def perform_add():
        # StaffID ถูกส่งเป็น INT ใน DB, แต่ใน Tkinter รับเป็น Text
        staff_id = entries["StaffID"].get()
        name = entries["ชื่อ"].get()
        role = entries["ตำแหน่ง (Admin/Staff)"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()
        
        if not all([staff_id, name, role, username, password]):
            messagebox.showwarning("Warning", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return
            
        try:
            # แปลง StaffID เป็น INT ก่อนส่งเข้า DB
            staff_id_int = int(staff_id)
        except ValueError:
            messagebox.showerror("Error", "StaffID ต้องเป็นตัวเลขเท่านั้น")
            return

        if add_staff(staff_id_int, name, role, username, password):
            messagebox.showinfo("Success", "เพิ่มพนักงานสำเร็จ")
            clear_entries()
            load_staff_data()

    def perform_update():
        staff_id = entries["StaffID"].get()
        name = entries["ชื่อ"].get()
        role = entries["ตำแหน่ง (Admin/Staff)"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()
        
        try:
            staff_id_int = int(staff_id)
        except ValueError:
            messagebox.showerror("Error", "StaffID ต้องเป็นตัวเลขเท่านั้น")
            return

        if update_staff(staff_id_int, name, role, username, password):
            messagebox.showinfo("Success", "อัพเดทข้อมูลพนักงานสำเร็จ")
            clear_entries()
            load_staff_data()
            
    def perform_delete():
        staff_id = entries["StaffID"].get()
        if not staff_id:
            messagebox.showwarning("Warning", "กรุณาเลือกพนักงานที่ต้องการลบ")
            return
            
        try:
            staff_id_int = int(staff_id)
        except ValueError:
            messagebox.showerror("Error", "StaffID ต้องเป็นตัวเลขเท่านั้น")
            return
            
        if messagebox.askyesno("Confirm Delete", f"ยืนยันการลบ Staff ID: {staff_id}?"):
            if delete_staff(staff_id_int):
                messagebox.showinfo("Success", "ลบพนักงานสำเร็จ")
                clear_entries()
                load_staff_data()


    # Buttons for CRUD
    btn_frame = tk.Frame(input_frame)
    btn_frame.grid(row=1, column=len(labels), rowspan=2, padx=10)
    
    tk.Button(btn_frame, text="Add", command=perform_add, bg="#D4EDDA", width=10).pack(pady=2)
    tk.Button(btn_frame, text="Update", command=perform_update, bg="#FFF3CD", width=10).pack(pady=2)
    tk.Button(btn_frame, text="Delete", command=perform_delete, bg="#F8D7DA", width=10).pack(pady=2)
    tk.Button(btn_frame, text="Clear", command=clear_entries, bg="#D6D8D9", width=10).pack(pady=2)

    # Treeview for Staff Data
    staff_tree = ttk.Treeview(staff_frame, columns=("ID", "Name", "Role", "Username", "Password"), show='headings')
    staff_tree.heading("ID", text="StaffID")
    staff_tree.heading("Name", text="ชื่อพนักงาน")
    staff_tree.heading("Role", text="ตำแหน่ง")
    staff_tree.heading("Username", text="Username")
    staff_tree.heading("Password", text="Password (ซ่อน)")
    
    staff_tree.column("ID", width=80)
    staff_tree.column("Name", width=180)
    staff_tree.column("Role", width=120)
    staff_tree.column("Username", width=150)
    staff_tree.column("Password", width=0, stretch=tk.NO) 
    
    vsb_staff = ttk.Scrollbar(staff_frame, orient="vertical", command=staff_tree.yview)
    staff_tree.configure(yscrollcommand=vsb_staff.set)
    vsb_staff.pack(side="right", fill="y")
    staff_tree.pack(expand=True, fill="both")
    
    staff_tree.bind("<<TreeviewSelect>>", on_staff_select)
    load_staff_data()

    # --- Back Button ---
    def go_back():
        Bus_Select_gui.open_select_bus_screen(admin_root, staff_id)
        
    back_btn = tk.Button(admin_root, text="⬅️ กลับหน้าเลือก Bus", command=go_back, bg="#AEE0FE", relief="flat")
    back_btn.pack(pady=10)

    admin_root.mainloop()