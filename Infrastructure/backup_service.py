# infrastructure/backup_service.py
import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from sqlalchemy import text
from infrastructure.database.session import engine, SessionLocal
from infrastructure.database.models.product_model import ProductModel
from infrastructure.database.models.order_model import OrderModel
from infrastructure.database.models.order_item_model import OrderItemModel


class BackupService:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self, description: str = "") -> str:
        """ایجاد پشتیبان کامل از دیتابیس و فایل‌ها"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"cafe_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir()

        try:
            # پشتیبان از دیتابیس
            self._backup_database(backup_path)

            # پشتیبان از فایل‌های تنظیمات (اگر وجود داشته باشد)
            self._backup_config_files(backup_path)

            # ایجاد فایل اطلاعات پشتیبان
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "description": description,
                "version": "1.0",
                "type": "full_backup"
            }

            with open(backup_path / "backup_info.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            # ایجاد فایل فشرده
            archive_path = self.backup_dir / f"{backup_name}.zip"
            shutil.make_archive(str(archive_path.with_suffix("")), 'zip', backup_path)

            # پاک کردن فولدر موقت
            shutil.rmtree(backup_path)

            return str(archive_path.with_suffix(".zip"))

        except Exception as e:
            # پاک کردن فولدر پشتیبان ناقص در صورت خطا
            if backup_path.exists():
                shutil.rmtree(backup_path)
            raise Exception(f"خطا در ایجاد پشتیبان: {str(e)}")

    def restore_backup(self, backup_file: str) -> None:
        """بازیابی پشتیبان"""
        backup_path = Path(backup_file)

        if not backup_path.exists():
            raise FileNotFoundError(f"فایل پشتیبان یافت نشد: {backup_file}")

        # بررسی فایل پشتیبان
        if not self._validate_backup(backup_path):
            raise ValueError("فایل پشتیبان نامعتبر است")

        try:
            # استخراج فایل پشتیبان
            extract_path = self.backup_dir / "temp_restore"
            if extract_path.exists():
                shutil.rmtree(extract_path)

            shutil.unpack_archive(backup_path, extract_path)

            # بازیابی دیتابیس
            self._restore_database(extract_path)

            # پاک کردن فایل‌های موقت
            shutil.rmtree(extract_path)

        except Exception as e:
            # پاک کردن فایل‌های موقت در صورت خطا
            if extract_path.exists():
                shutil.rmtree(extract_path)
            raise Exception(f"خطا در بازیابی پشتیبان: {str(e)}")

    def list_backups(self) -> List[Dict]:
        """لیست تمام فایل‌های پشتیبان موجود"""
        backups = []

        for file_path in self.backup_dir.glob("cafe_backup_*.zip"):
            try:
                # استخراج اطلاعات پشتیبان از نام فایل
                filename = file_path.name
                timestamp_str = filename.replace("cafe_backup_", "").replace(".zip", "")

                # تبدیل timestamp
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

                backups.append({
                    "filename": filename,
                    "path": str(file_path),
                    "timestamp": timestamp,
                    "size_mb": round(file_path.stat().st_size / (1024 * 1024), 2)
                })

            except ValueError:
                continue

        # مرتب‌سازی بر اساس تاریخ (جدیدترین اول)
        backups.sort(key=lambda x: x["timestamp"], reverse=True)

        return backups

    def delete_backup(self, backup_filename: str) -> None:
        """حذف فایل پشتیبان"""
        backup_path = self.backup_dir / backup_filename

        if not backup_path.exists():
            raise FileNotFoundError(f"فایل پشتیبان یافت نشد: {backup_filename}")

        backup_path.unlink()

    def _backup_database(self, backup_path: Path) -> None:
        """پشتیبان‌گیری از دیتابیس"""
        session = SessionLocal()

        try:
            # پشتیبان محصولات
            products = session.query(ProductModel).all()
            products_data = [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "category": p.category,
                    "is_active": p.is_active
                }
                for p in products
            ]

            with open(backup_path / "products.json", "w", encoding="utf-8") as f:
                json.dump(products_data, f, ensure_ascii=False, indent=2)

            # پشتیبان سفارشات
            orders = session.query(OrderModel).all()
            orders_data = []

            for order in orders:
                order_items = session.query(OrderItemModel).filter_by(order_id=order.id).all()
                order_data = {
                    "id": order.id,
                    "table_number": order.table_number,
                    "status": order.status,
                    "discount": order.discount,
                    "created_at": order.created_at.isoformat() if order.created_at else None,
                    "items": [
                        {
                            "product_name": item.product_name,
                            "unit_price": item.unit_price,
                            "quantity": item.quantity
                        }
                        for item in order_items
                    ]
                }
                orders_data.append(order_data)

            with open(backup_path / "orders.json", "w", encoding="utf-8") as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)

        finally:
            session.close()

    def _backup_config_files(self, backup_path: Path) -> None:
        """پشتیبان‌گیری از فایل‌های تنظیمات"""
        # در نسخه‌های بعدی می‌توان فایل‌های تنظیمات را نیز پشتیبان گرفت
        pass

    def _restore_database(self, backup_path: Path) -> None:
        """بازیابی دیتابیس از پشتیبان"""
        session = SessionLocal()

        try:
            # پاک کردن داده‌های موجود
            session.execute(text("DELETE FROM order_items"))
            session.execute(text("DELETE FROM orders"))
            session.execute(text("DELETE FROM products"))
            session.commit()

            # بازیابی محصولات
            with open(backup_path / "products.json", "r", encoding="utf-8") as f:
                products_data = json.load(f)

            for product_data in products_data:
                product = ProductModel(
                    id=product_data["id"],
                    name=product_data["name"],
                    price=product_data["price"],
                    category=product_data["category"],
                    is_active=product_data["is_active"]
                )
                session.add(product)

            session.commit()

            # بازیابی سفارشات
            with open(backup_path / "orders.json", "r", encoding="utf-8") as f:
                orders_data = json.load(f)

            for order_data in orders_data:
                # ایجاد سفارش
                order = OrderModel(
                    id=order_data["id"],
                    table_number=order_data["table_number"],
                    status=order_data["status"],
                    discount=order_data["discount"],
                    created_at=datetime.fromisoformat(order_data["created_at"]) if order_data["created_at"] else None
                )
                session.add(order)
                session.flush()  # برای گرفتن ID

                # ایجاد آیتم‌های سفارش
                for item_data in order_data["items"]:
                    order_item = OrderItemModel(
                        order_id=order.id,
                        product_name=item_data["product_name"],
                        unit_price=item_data["unit_price"],
                        quantity=item_data["quantity"]
                    )
                    session.add(order_item)

            session.commit()

        finally:
            session.close()

    def _validate_backup(self, backup_path: Path) -> bool:
        """بررسی اعتبار فایل پشتیبان"""
        try:
            # بررسی وجود فایل اطلاعات پشتیبان
            info_file = backup_path / "backup_info.json"
            if not info_file.exists():
                return False

            # بررسی وجود فایل‌های داده
            if not (backup_path / "products.json").exists():
                return False

            if not (backup_path / "orders.json").exists():
                return False

            # بررسی محتوای فایل اطلاعات
            with open(info_file, "r", encoding="utf-8") as f:
                info = json.load(f)

            if info.get("type") != "full_backup":
                return False

            return True

        except (json.JSONDecodeError, KeyError):
            return False
