# db_connector.py

import pyodbc
from tkinter import messagebox, Tk

# ================== SQL Server Configuration ==================
# **** โปรดแก้ไขค่าเหล่านี้ให้ตรงกับเครื่องของคุณ ****
server = 'DESKTOP-1UPQK9B\\SQLEXPRESS' 
database = 'BusTicketSystem'
driver = '{ODBC Driver 17 for SQL Server}' 
# =============================================================

def connect_db():
    conn_str = (
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        temp_root = Tk()
        temp_root.withdraw() 
        messagebox.showerror("Database Error", f"ไม่สามารถเชื่อมต่อ SQL Server ได้: {e}")
        temp_root.destroy()
        return None

def authenticate_user(username, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            # สมมติว่า StaffID เป็น INT และ Username/Password เป็น VARCHAR
            query = "SELECT StaffID, StaffName, Role FROM STAFF WHERE Username = ? AND Password = ?"
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()
            conn.close()
            return user_data
        except Exception as e:
            messagebox.showerror("Query Error", f"Error during authentication: {e}")
            conn.close()
            return None
    return None

def get_logged_in_user_info(staff_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            # StaffID ถูกส่งมาเป็น Python int
            cursor.execute("SELECT StaffName, Role FROM STAFF WHERE StaffID = ?", (staff_id,))
            user_info = cursor.fetchone()
            conn.close()
            return user_info
        except Exception as e:
            messagebox.showerror("Query Error", f"Error fetching user info: {e}")
            conn.close()
            return None
    return None

def get_fare_rates():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Price FROM FARE_RATE ORDER BY Price")
            rates = [row[0] for row in cursor.fetchall()]
            conn.close()
            return rates if rates else [15, 20, 25, 27] 
        except Exception as e:
            conn.close()
            return [15, 20, 25, 27] 
    return [15, 20, 25, 27] 

# *****************************************************************
# ฟังก์ชันใหม่: ตรวจสอบ License Plate และดึง Vehicle ID / Route Info
# *****************************************************************

def check_vehicle_and_get_route(license_plate, route_number): 
    """
    ตรวจสอบว่า License Plate ตรงกับ RouteNumber ที่เลือก และดึง VehicleID, Route Details
    :return: (True, VehicleID, RouteID, RouteDescription) หรือ (False, None, None, None)
    """
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            SELECT 
                B.VehicleID,           
                R.RouteID, 
                R.RouteDescription
            FROM BUS B
            JOIN ROUTE R ON B.RouteID = R.RouteID
            WHERE B.LicensePlate = ? AND B.RouteNumber = ?
            """
            cursor.execute(query, (license_plate, route_number)) 
            result = cursor.fetchone()
            conn.close()
            
            if result:
                # Result: (VehicleID, RouteID, RouteDescription)
                return True, result[0], result[1], result[2] 
            return False, None, None, None
            
        except Exception as e:
            messagebox.showerror("Query Error", f"Error during vehicle check: {e}")
            conn.close()
            return False, None, None, None
    return False, None, None, None

# *****************************************************************
# ฟังก์ชันสำหรับ Admin Console
# *****************************************************************

def get_staff_list():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = "SELECT StaffID, StaffName, Role, Username, Password FROM STAFF"
            cursor.execute(query)
            staff_list = cursor.fetchall()
            conn.close()
            return staff_list
        except Exception as e:
            conn.close()
            return []
    return []

def get_sales_report():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            SELECT 
                B.RouteNumber, 
                SUM(T.Price) AS TotalSales, 
                COUNT(T.TicketNo) AS TotalTickets
            FROM TICKET T
            JOIN BUS B ON T.VehicleID = B.VehicleID 
            WHERE T.TicketStatus = 'Active' 
            GROUP BY B.RouteNumber
            ORDER BY TotalSales DESC
            """
            cursor.execute(query)
            sales_data = cursor.fetchall()
            conn.close()
            return sales_data
        except Exception as e:
            conn.close()
            return []
    return []

def add_staff(staff_id, name, role, username, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO STAFF (StaffID, StaffName, Role, Username, Password) 
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, staff_id, name, role, username, password)
            conn.commit()
            conn.close()
            return True
        except pyodbc.IntegrityError:
            conn.close()
            messagebox.showerror("Error", "StaffID หรือ Username นี้ถูกใช้งานแล้ว")
            return False
        except Exception as e:
            conn.close()
            messagebox.showerror("DB Error", f"Failed to add staff: {e}")
            return False
    return False

def update_staff(staff_id, name, role, username, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            UPDATE STAFF SET StaffName = ?, Role = ?, Username = ?, Password = ? 
            WHERE StaffID = ?
            """
            cursor.execute(query, name, role, username, password, staff_id)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            messagebox.showerror("DB Error", f"Failed to update staff: {e}")
            return False
    return False

def delete_staff(staff_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = "DELETE FROM STAFF WHERE StaffID = ?"
            cursor.execute(query, staff_id)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            messagebox.showerror("DB Error", f"Failed to delete staff: {e}")
            return False
    return False