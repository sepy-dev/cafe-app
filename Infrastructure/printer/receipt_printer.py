from datetime import datetime
from typing import List, Optional
from domain.entities.order import Order
from domain.entities.order_item import OrderItem

# پشتیبانی از چاپ در ویندوز
try:
    import win32print
    import win32api
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class ReceiptPrinter:
    def __init__(self, printer_name: str = None):
        self.printer_name = printer_name
        self.business_name = "کافه نمونه"
        self.business_address = "تهران، خیابان ولیعصر"
        self.business_phone = "021-12345678"

    def get_available_printers(self) -> List[str]:
        """دریافت لیست پرینترهای موجود"""
        if not WIN32_AVAILABLE:
            return ["Default Printer (Console)"]

        try:
            printers = []
            for printer_info in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS):
                printers.append(printer_info[2])  # printer name
            return printers
        except Exception:
            return ["Default Printer (Console)"]

    def set_printer(self, printer_name: str):
        """تنظیم پرینتر فعال"""
        self.printer_name = printer_name

    def print_to_printer(self, receipt_text: str, printer_name: Optional[str] = None) -> bool:
        """چاپ به پرینتر واقعی"""
        if not WIN32_AVAILABLE:
            print("پشتیبانی از چاپ واقعی موجود نیست. متن فاکتور:")
            print(receipt_text)
            return False

        printer_to_use = printer_name or self.printer_name or win32print.GetDefaultPrinter()

        try:
            # باز کردن پرینتر
            hprinter = win32print.OpenPrinter(printer_to_use)
            try:
                # شروع کار چاپ
                win32print.StartDocPrinter(hprinter, 1, ("Receipt", None, "RAW"))
                win32print.StartPagePrinter(hprinter)

                # ارسال داده‌ها به پرینتر
                win32print.WritePrinter(hprinter, receipt_text.encode('utf-8'))

                # پایان کار چاپ
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)

                return True

            finally:
                win32print.ClosePrinter(hprinter)

        except Exception as e:
            print(f"خطا در چاپ: {str(e)}")
            return False

    def print_receipt(self, order: Order, order_id: int) -> str:
        """چاپ فاکتور سفارش و برگرداندن متن فاکتور"""
        receipt_lines = []

        # هدر فاکتور
        receipt_lines.extend(self._create_header(order_id))

        # اطلاعات سفارش
        receipt_lines.extend(self._create_order_info(order))

        # آیتم‌ها
        receipt_lines.extend(self._create_items_list(order))

        # جمع‌بندی مالی
        receipt_lines.extend(self._create_totals(order))

        # فوتر
        receipt_lines.extend(self._create_footer())

        receipt_text = "\n".join(receipt_lines)

        # چاپ به پرینتر واقعی
        self.print_to_printer(receipt_text)

        return receipt_text

    def _create_header(self, order_id: int) -> List[str]:
        """ایجاد هدر فاکتور"""
        header = [
            "=" * 40,
            f"          {self.business_name}",
            f"        {self.business_address}",
            f"         {self.business_phone}",
            "=" * 40,
            f"شماره فاکتور: {order_id}",
            f"تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 40
        ]
        return header

    def _create_order_info(self, order: Order) -> List[str]:
        """ایجاد اطلاعات سفارش"""
        info = []

        if order.table_number:
            info.append(f"میز: {order.table_number}")
        else:
            info.append("نوع سفارش: بیرون بر")

        info.append(f"وضعیت: {'بسته شده' if order.status.value == 'CLOSED' else 'باز'}")
        info.append("-" * 40)

        return info

    def _create_items_list(self, order: Order) -> List[str]:
        """ایجاد لیست آیتم‌ها"""
        items = ["آیتم                    تعداد    قیمت    مجموع"]

        for item in order.get_items():
            name = item.name[:20].ljust(20)  # محدود کردن طول نام
            qty = str(item.quantity).rjust(6)
            price = f"{item.unit_price.amount:,}".rjust(8)
            total = f"{item.total_price().amount:,}".rjust(8)

            items.append(f"{name} {qty} {price} {total}")

        items.append("-" * 40)
        return items

    def _create_totals(self, order: Order) -> List[str]:
        """ایجاد بخش جمع‌بندی مالی"""
        subtotal = sum(item.total_price().amount for item in order.items)

        totals = [
            f"جمع جزء:".ljust(30) + f"{subtotal:,} تومان",
        ]

        if order.discount.amount > 0:
            totals.append(f"تخفیف:".ljust(30) + f"{order.discount.amount:,} تومان")

        totals.extend([
            f"مجموع نهایی:".ljust(30) + f"{order.total_price().amount:,} تومان",
            "=" * 40
        ])

        return totals

    def _create_footer(self) -> List[str]:
        """ایجاد فوتر فاکتور"""
        footer = [
            "با تشکر از انتخاب شما!",
            "آدرس: " + self.business_address,
            "تلفن: " + self.business_phone,
            "",
            "نرم‌افزار مدیریت کافه - نسخه ۱.۰",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "=" * 40
        ]
        return footer


    def print_test_receipt(self):
        """چاپ فاکتور تست"""
        test_receipt = [
            "=" * 40,
            "          فاکتور تست پرینتر",
            "=" * 40,
            "این یک فاکتور تست است",
            "اگر این متن را مشاهده می‌کنید،",
            "پرینتر به درستی کار می‌کند.",
            "=" * 40,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "=" * 40
        ]

        test_text = "\n".join(test_receipt)
        self.print_to_printer(test_text)
