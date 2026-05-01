from dataclasses import dataclass
from model.staff import Staff
from datetime import datetime
from typing import Literal

@dataclass
class Record:
    staff: Staff
    check_datetime: datetime
    io: Literal["check_in", "check_out"]

    @classmethod
    def from_row(cls, row: dict):
        return cls(
            staff=Staff(name=row["staff_name"]),
            check_datetime=datetime.fromisoformat(row["check_datetime"]),
            io=row["io"]
        )