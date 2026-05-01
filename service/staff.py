from model.staff import Staff
import repository.staff as staff_repo
from typing import Literal

def new_staff(name: str, rfid: str):
    staff = Staff(name, rfid)
    staff_repo.new_staff(staff)

def remove_staff(name: str):
    staff = staff_repo.get_staff_by_name(name)
    staff_repo.remove_staff(staff)

def get_staff_by_io(io: Literal["check_in", "check_out"]):
    staffs = staff_repo.get_staff_by_io(io)
    return staffs

def get_all_staff():
    staffs = staff_repo.staff_list()
    return staffs