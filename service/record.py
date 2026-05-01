import repository.record as record_repo
import repository.staff as staff_repo
from logging import getLogger

logger = getLogger(__name__)

def check_io(rfid: str):
    staff = staff_repo.get_staff_by_rfid(rfid)

    if staff is None:
        raise ValueError("查無此卡")
    
    checked = record_repo.has_checked_in(staff)

    if not checked:
        record_repo.check_in(staff)
        logger.info(f"{staff.name} 簽到成功")

    else:
        record_repo.check_out(staff)
        logger.info(f"{staff.name} 簽退成功")


def get_record_by_name(name: str):
    staff = staff_repo.get_staff_by_name(name)
    records = record_repo.get_record_by_staff(staff)

    return records

def get_record_today():
    records = record_repo.get_record_today()
    return records

def get_all_record():
    records = record_repo.get_all_record()
    return records