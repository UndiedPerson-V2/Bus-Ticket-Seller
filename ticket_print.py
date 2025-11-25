# ticket_print.py

import tkinter as tk
from tkinter import messagebox
from db_connector import get_logged_in_user_info
from datetime import datetime
import Bus_Select_gui 
import ticket_price_gui # Import เพื่อให้เรียกกลับไปหน้า Price ได้
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os 

# ====================================================================
# PDF Generation (using ReportLab)
# ====================================================================
def create_ticket_pdf(data):
    """
    Creates a ticket PDF file using ReportLab.
    """
    try:
        filename = f"Ticket_{data['ticket_no']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "--- I-Love-You-BusGO Ticket ---")
        
        c.setFont("Helvetica", 12)
        y_pos = 720
        line_height = 20
        
        # Mapping English keys for PDF
        display_mapping_pdf = {
            "ticket_no": "Ticket No.",
            "route_number": "Bus Route No.",
            "vehicle_id": "Vehicle ID",
            "staff_name": "Staff Name",
            "datetime": "Time Issued",
            "route_info": "Route Info",
            "pay_method": "Payment Method",
            "price": "Price"
        }
        
        # Write details to PDF
        for key, value in data.items():
            if key in display_mapping_pdf:
                label = display_mapping_pdf[key]
                display_value = f"{value} THB" if key == 'price' else value
                c.drawString(100, y_pos, f"{label}: {display_value}")
                y_pos -= line_height

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y_pos - 10, f"*** THANK YOU ***")

        c.save()
        return os.path.abspath(filename)
        
    except Exception as e:
        messagebox.showerror("PDF Error", f"Failed to create PDF. (Make sure ReportLab is installed): {e}")
        return None


# ====================================================================
# Tkinter Screen
# ====================================================================

def open_ticket_print_screen(prev_root, staff_id, route_number, vehicle_id, price, route_description, route_id): 
    """Creates the Ticket Print screen and links it to the PDF generation function."""
    if prev_root:
        prev_root.destroy()
    
    print_root = tk.Tk()
    print_root.title("Ticket Print")
    print_root.geometry("350x550")
    print_root.config(bg="#F8E9E4")
    
    user_data = get_logged_in_user_info(staff_id)
    staff_name = user_data[0] if user_data else "Staff ID N/A"
    
    # Data for display and PDF creation
    ticket_data = {
        "title": "I-Love-You-BusGO",
        "ticket_no": f"TKT{vehicle_id}-{datetime.now().strftime('%H%M%S')}",
        "route_number": route_number, 
        "vehicle_id": vehicle_id,  
        "staff_name": staff_name,
        "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "route_info": route_description,
        "pay_method": "Cash",
        "price": price 
    }
    
    # Mapping English keys for UI
    display_mapping_ui = {
        "ticket_no": "Ticket No.",
        "route_number": "Bus Route No.",
        "vehicle_id": "Vehicle ID",
        "staff_name": "Staff Name",
        "datetime": "Time Issued",
        "route_info": "Route Info",
        "pay_method": "Payment Method",
        "price": "Price"
    }
    
    # --- New Navigation Function ---
    def go_back_to_select_price():
        """
        นำกลับไปหน้า Select Price โดยส่งค่า Vehicle ID, Route ID, และ Route Description ที่ยืนยันแล้วกลับไปด้วย
        """
        print_root.destroy()
        ticket_price_gui.open_select_price_screen(
            None, 
            staff_id, 
            route_number, 
            vehicle_id, 
            route_id, 
            route_description
        )

    def print_action():
        """Performs PDF printing and returns to the Select Price screen."""
        pdf_path = create_ticket_pdf(ticket_data)
        
        if pdf_path:
            messagebox.showinfo("Print Success", 
                                f"Ticket PDF created successfully!\nFile saved at:\n{pdf_path}")
            # กลับไปหน้า Select Price หลังพิมพ์เสร็จ
            go_back_to_select_price()
        else:
            messagebox.showwarning("Print Failed", "Could not save the ticket as PDF.")


    def go_back_to_dashboard():
        """Cancels and returns to the Select Price screen."""
        if messagebox.askyesno("Cancel Transaction", "Do you want to cancel and return to Select Price?"):
             go_back_to_select_price()


    # --- UI Elements ---
    title = tk.Label(print_root, text="Ticket Print", font=("Arial", 16, "bold"), bg="#F8E9E4")
    title.pack(pady=20)
    
    # Ticket Detail Box
    detail_frame = tk.Frame(print_root, bg="white", padx=15, pady=15, relief="solid", bd=1)
    detail_frame.pack(pady=10)
    
    # Display main header
    tk.Label(detail_frame, text=ticket_data['title'], bg="white", font=("Arial", 12, "bold")).pack(anchor="w")
    
    # Display ticket details from the dictionary
    for key, value in ticket_data.items():
        if key in display_mapping_ui:
            label_text = display_mapping_ui[key]
            
            if key == 'price':
                value = f"{value} THB" 

            tk.Label(detail_frame, text=f"{label_text}: {value}", 
                     bg="white", font=("Arial", 10)).pack(anchor="w")
    
    # Print Button
    print_btn = tk.Button(print_root, text="Print Ticket (to PDF)", width=20,
                        command=print_action, 
                        bg="#28a745", fg="white",
                        relief="flat", bd=0)
    print_btn.pack(pady=40)

    # Back Button
    back_btn = tk.Button(print_root, text="Back/Cancel (Select Price)", width=25,
                        command=go_back_to_dashboard, 
                        bg="#f8d7da", fg="#721c24",
                        relief="flat", bd=0)
    back_btn.pack(pady=10)


    print_root.mainloop()