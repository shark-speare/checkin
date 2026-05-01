from model.staff import Staff
from model.record import Record
from tabulate import tabulate
from datetime import datetime

table_style = "rounded_outline"

def make_staff_table(staffs:list[Staff]):
    data = [
        [
            staff.name,
            staff.rfid
        ]
        for staff in staffs
    ]
    table = tabulate(
        data,
        headers=["name", "RFID"],
        tablefmt=table_style
    )

    return table

def make_record_table(records:list[Record]):
    data = [
        [
            record.staff.name,
            record.check_datetime.strftime("%m/%d %H:%M:%S"),
            "check in" if record.io == "check_in" else "check out"
        ]
        for record in records
    ]

    table = tabulate(
        data,
        headers=["name", "time", "check in/out"],
        tablefmt=table_style
    )

    return table