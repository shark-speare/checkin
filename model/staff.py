from dataclasses import dataclass

@dataclass
class Staff:
    name: str
    rfid: str | None = None

    # 因為不需要多餘處理，可加可不加
    # @classmethod
    # def from_row(cls, row: dict):
    #     return cls(*row)