from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from sqlalchemy import func, extract
from infrastructure.database.session import SessionLocal
from infrastructure.database.models.order_model import OrderModel
from infrastructure.database.models.order_item_model import OrderItemModel
from domain.value_objects.money import Money


class ReportService:
    def __init__(self):
        self.session = SessionLocal()

    def get_daily_sales(self, date: datetime = None) -> Dict:
        """گزارش فروش روزانه"""
        if date is None:
            date = datetime.now().date()

        start_date = datetime.combine(date, datetime.min.time())
        end_date = datetime.combine(date, datetime.max.time())

        # تعداد سفارشات
        orders_count = (
            self.session.query(func.count(OrderModel.id))
            .filter(OrderModel.created_at.between(start_date, end_date))
            .scalar()
        )

        # مجموع فروش
        total_sales = (
            self.session.query(
                func.sum(OrderItemModel.unit_price * OrderItemModel.quantity)
            )
            .join(OrderModel)
            .filter(OrderModel.created_at.between(start_date, end_date))
            .scalar()
        ) or 0

        # مجموع تخفیف‌ها
        total_discounts = (
            self.session.query(func.sum(OrderModel.discount))
            .filter(OrderModel.created_at.between(start_date, end_date))
            .scalar()
        ) or 0

        # محصولات پرفروش
        top_products = (
            self.session.query(
                OrderItemModel.product_name,
                func.sum(OrderItemModel.quantity).label('total_quantity'),
                func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label('total_revenue')
            )
            .join(OrderModel)
            .filter(OrderModel.created_at.between(start_date, end_date))
            .group_by(OrderItemModel.product_name)
            .order_by(func.sum(OrderItemModel.quantity).desc())
            .limit(10)
            .all()
        )

        return {
            'date': date.strftime('%Y-%m-%d'),
            'orders_count': orders_count,
            'total_sales': Money(total_sales),
            'total_discounts': Money(total_discounts),
            'net_sales': Money(total_sales - total_discounts),
            'top_products': [
                {
                    'name': product.product_name,
                    'quantity': product.total_quantity,
                    'revenue': Money(product.total_revenue)
                }
                for product in top_products
            ]
        }

    def get_monthly_sales(self, year: int = None, month: int = None) -> Dict:
        """گزارش فروش ماهانه"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)

        # آمار روزانه
        daily_stats = []
        current_date = start_date
        while current_date <= end_date:
            daily_report = self.get_daily_sales(current_date)
            daily_stats.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'orders': daily_report['orders_count'],
                'sales': daily_report['net_sales'].amount
            })
            current_date += timedelta(days=1)

        # مجموع ماه
        total_orders = sum(day['orders'] for day in daily_stats)
        total_sales = sum(day['sales'] for day in daily_stats)

        return {
            'year': year,
            'month': month,
            'total_orders': total_orders,
            'total_sales': Money(total_sales),
            'daily_stats': daily_stats
        }

    def get_product_sales_report(self, start_date: datetime = None,
                                end_date: datetime = None) -> List[Dict]:
        """گزارش فروش محصولات"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()

        product_stats = (
            self.session.query(
                OrderItemModel.product_name,
                func.sum(OrderItemModel.quantity).label('total_quantity'),
                func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label('total_revenue'),
                func.count(func.distinct(OrderModel.id)).label('orders_count')
            )
            .join(OrderModel)
            .filter(OrderModel.created_at.between(start_date, end_date))
            .group_by(OrderItemModel.product_name)
            .order_by(func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).desc())
            .all()
        )

        return [
            {
                'product_name': stat.product_name,
                'total_quantity': stat.total_quantity,
                'total_revenue': Money(stat.total_revenue),
                'orders_count': stat.orders_count,
                'avg_price_per_order': Money(stat.total_revenue // stat.orders_count) if stat.orders_count > 0 else Money(0)
            }
            for stat in product_stats
        ]

    def get_hourly_sales_pattern(self, date: datetime = None) -> List[Dict]:
        """الگوی فروش ساعتی"""
        if date is None:
            date = datetime.now().date()

        start_date = datetime.combine(date, datetime.min.time())
        end_date = datetime.combine(date, datetime.max.time())

        hourly_stats = (
            self.session.query(
                extract('hour', OrderModel.created_at).label('hour'),
                func.count(OrderModel.id).label('orders_count'),
                func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label('total_sales')
            )
            .join(OrderItemModel)
            .filter(OrderModel.created_at.between(start_date, end_date))
            .group_by(extract('hour', OrderModel.created_at))
            .order_by(extract('hour', OrderModel.created_at))
            .all()
        )

        # ایجاد آمار برای تمام ساعات روز (حتی ساعات بدون فروش)
        hourly_report = []
        for hour in range(24):
            stat = next((s for s in hourly_stats if s.hour == hour), None)
            hourly_report.append({
                'hour': hour,
                'orders_count': stat.orders_count if stat else 0,
                'total_sales': Money(stat.total_sales if stat else 0)
            })

        return hourly_report

    def get_table_performance(self) -> List[Dict]:
        """گزارش عملکرد میزها"""
        table_stats = (
            self.session.query(
                OrderModel.table_number,
                func.count(OrderModel.id).label('orders_count'),
                func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label('total_sales'),
                func.avg(OrderItemModel.unit_price * OrderItemModel.quantity).label('avg_order_value')
            )
            .join(OrderItemModel)
            .filter(OrderModel.table_number.isnot(None))
            .group_by(OrderModel.table_number)
            .order_by(func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).desc())
            .all()
        )

        return [
            {
                'table_number': stat.table_number,
                'orders_count': stat.orders_count,
                'total_sales': Money(stat.total_sales),
                'avg_order_value': Money(int(stat.avg_order_value))
            }
            for stat in table_stats
        ]
