from enum import Enum


class TableStatus(Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"


class Table:
    def __init__(self, number: int, capacity: int = 4, status: TableStatus = TableStatus.AVAILABLE):
        if number <= 0:
            raise ValueError("شماره میز باید مثبت باشد")

        if capacity <= 0:
            raise ValueError("ظرفیت میز باید مثبت باشد")

        self.number = number
        self.capacity = capacity
        self.status = status

    def occupy(self):
        """اشغال میز"""
        if self.status != TableStatus.AVAILABLE:
            raise ValueError(f"میز {self.number} در حال حاضر قابل اشغال نیست")
        self.status = TableStatus.OCCUPIED

    def free(self):
        """آزاد کردن میز"""
        if self.status == TableStatus.RESERVED:
            raise ValueError(f"میز {self.number} رزرو شده و نمی‌تواند آزاد شود")
        self.status = TableStatus.AVAILABLE

    def reserve(self):
        """رزرو میز"""
        if self.status != TableStatus.AVAILABLE:
            raise ValueError(f"میز {self.number} قابل رزرو نیست")
        self.status = TableStatus.RESERVED

    def cancel_reservation(self):
        """لغو رزرو"""
        if self.status != TableStatus.RESERVED:
            raise ValueError(f"میز {self.number} رزرو نشده است")
        self.status = TableStatus.AVAILABLE

    def __str__(self) -> str:
        return f"میز {self.number} ({self.capacity} نفره - {self.status.value})"
