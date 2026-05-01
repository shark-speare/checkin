from model.record import Record
from model.staff import Staff
from repository.db import Database
from datetime import datetime
import logging

def check_in(staff: Staff):
    db = Database()

    now_datetime = datetime.now().isoformat()
    
    db.execute(
        "INSERT INTO records(staff_name, check_datetime, io) VALUES (?, ?, ?)",
        (staff.name, now_datetime, "check_in")
    )

    db.commit()


def check_out(staff: Staff):
    db = Database()

    now_datetime = datetime.now().isoformat()
    
    db.execute(
        "INSERT INTO records(staff_name, check_datetime, io) VALUES (?, ?, ?)",
        (staff.name, now_datetime, "check_out")
    )

    db.commit()

def get_record_by_staff(staff: Staff) -> list[Record]:
    db = Database()

    record_row = db.execute(
        "SELECT * FROM records WHERE staff_name = ?",
        (staff.name,)
    )

    records = [Record.from_row(row) for row in record_row]
    return records

def get_record_today() -> list[Record]:
    db = Database()

    record_row = db.execute(
        "SELECT * FROM records WHERE datetime('now', 'start of day') < datetime(check_datetime) "
    )

    records = [Record.from_row(row) for row in record_row]
    return records

def get_all_record():
    db = Database()

    record_row = db.execute(
        "SELECT * FROM records"
    )

    records = [Record.from_row(row) for row in record_row]
    return records

def has_checked_in(staff: Staff) -> bool:
    db = Database()

    record_row  = db.execute(
        """
        SELECT * FROM records 
        WHERE staff_name = ? 
        ORDER BY datetime(check_datetime) DESC
        LIMIT 1
        """,
        (staff.name,),
        one=True
    )

    if not record_row:
        return False

    if not dict(record_row).get("io") or dict(record_row).get("io") == "check_out":
        return False
    else:
        return True