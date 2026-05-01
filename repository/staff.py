from model.staff import Staff
from repository.db import Database
from typing import Literal

def new_staff(staff: Staff):
    db = Database()

    db.execute(
        "INSERT INTO staffs(name, rfid) VALUES (?, ?)",
        (staff.name, staff.rfid)
    )

def remove_staff(staff: Staff):
    db = Database()
    
    db.execute(
        "DELETE FROM staffs WHERE name = ?",
        (staff.name,)
    )

    db.commit()

def get_staff_by_rfid(rfid: str):
    db = Database()

    staff_row = db.execute(
        "SELECT name, rfid FROM staffs WHERE rfid = ?",
        (rfid,),
        one=True
    )

    if not staff_row:
        return None

    return Staff(*staff_row)

def get_staff_by_name(name: str):
    db = Database()

    staff_row = db.execute(
        "SELECT name, rfid FROM staffs WHERE name = ?",
        (name,),
        one=True
    )

    if not staff_row:
        return None

    return Staff(*staff_row)

def staff_list():
    db = Database()

    staff_row = db.execute(
        "SELECT * FROM staffs"
    )

    staffs = [Staff(*row) for row in staff_row]
    return staffs

def get_staff_by_io(io: Literal["check_in", "check_out"]):
    db = Database()

    staff_row = db.execute(
        """
        SELECT DISTINCT s.name, s.rfid
        FROM staffs s
        JOIN records r ON s.name = r.staff_name
        WHERE r.io = ?
        AND r.check_datetime = (
            SELECT MAX(check_datetime)
            FROM records r2
            WHERE r2.staff_name = r.staff_name
        )
        """,
        (io,)
    )

    staffs = [Staff(*row) for row in staff_row]
    return staffs