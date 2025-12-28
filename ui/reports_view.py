from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTextEdit, QComboBox, QDateEdit, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import QDate
from datetime import datetime
from application.report_service import ReportService

# Import matplotlib for charts
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class ReportsView(QWidget):
    def __init__(self):
        super().__init__()

        self.report_service = ReportService()

        layout = QVBoxLayout(self)

        title = QLabel("گزارشات فروش")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        # کنترل‌های انتخاب تاریخ
        controls_layout = QHBoxLayout()

        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)

        self.report_type = QComboBox()
        self.report_type.addItems([
            "گزارش روزانه",
            "گزارش ماهانه",
            "گزارش محصولات",
            "الگوی فروش ساعتی",
            "عملکرد میزها"
        ])

        self.generate_btn = QPushButton("تولید گزارش")
        self.generate_btn.clicked.connect(self.generate_report)

        controls_layout.addWidget(QLabel("تاریخ:"))
        controls_layout.addWidget(self.date_picker)
        controls_layout.addWidget(self.report_type)
        controls_layout.addWidget(self.generate_btn)
        controls_layout.addStretch()

        layout.addLayout(controls_layout)

        # تب‌ها برای نمایش گزارشات مختلف
        self.tabs = QTabWidget()

        # تب خلاصه
        self.summary_tab = QWidget()
        summary_layout = QVBoxLayout(self.summary_tab)
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        summary_layout.addWidget(self.summary_text)
        self.tabs.addTab(self.summary_tab, "خلاصه")

        # تب جدول جزئیات
        self.details_tab = QWidget()
        details_layout = QVBoxLayout(self.details_tab)
        self.details_table = QTableWidget()
        details_layout.addWidget(self.details_table)
        self.tabs.addTab(self.details_tab, "جزئیات")

        # تب نمودارها (اگر matplotlib موجود باشد)
        if MATPLOTLIB_AVAILABLE:
            self.chart_tab = QWidget()
            chart_layout = QVBoxLayout(self.chart_tab)
            self.chart_canvas = FigureCanvas(Figure(figsize=(8, 6)))
            chart_layout.addWidget(self.chart_canvas)
            self.tabs.addTab(self.chart_tab, "نمودارها")

        layout.addWidget(self.tabs)

        # تولید گزارش اولیه
        self.generate_report()

    def generate_report(self):
        report_type = self.report_type.currentText()
        selected_date = self.date_picker.date().toPython()

        try:
            if report_type == "گزارش روزانه":
                self.show_daily_report(selected_date)
            elif report_type == "گزارش ماهانه":
                self.show_monthly_report(selected_date.year, selected_date.month)
            elif report_type == "گزارش محصولات":
                self.show_product_report(selected_date)
            elif report_type == "الگوی فروش ساعتی":
                self.show_hourly_pattern(selected_date)
            elif report_type == "عملکرد میزها":
                self.show_table_performance()

        except Exception as e:
            self.summary_text.setText(f"خطا در تولید گزارش: {str(e)}")

    def show_daily_report(self, date):
        report = self.report_service.get_daily_sales(date)

        summary = f"""
گزارش فروش روزانه - {report['date']}

تعداد سفارشات: {report['orders_count']}
مجموع فروش: {report['total_sales']}
مجموع تخفیف‌ها: {report['total_discounts']}
فروش خالص: {report['net_sales']}
"""
        self.summary_text.setText(summary.strip())

        # نمایش محصولات پرفروش در جدول
        self.details_table.setColumnCount(3)
        self.details_table.setHorizontalHeaderLabels(["محصول", "تعداد", "فروش"])
        self.details_table.horizontalHeader().setStretchLastSection(True)

        self.details_table.setRowCount(len(report['top_products']))
        for row, product in enumerate(report['top_products']):
            self.details_table.setItem(row, 0, QTableWidgetItem(product['name']))
            self.details_table.setItem(row, 1, QTableWidgetItem(str(product['quantity'])))
            self.details_table.setItem(row, 2, QTableWidgetItem(str(product['revenue'])))

    def show_monthly_report(self, year, month):
        report = self.report_service.get_monthly_sales(year, month)

        summary = f"""
گزارش فروش ماهانه - {year}/{month}

تعداد کل سفارشات: {report['total_orders']}
مجموع فروش: {report['total_sales']}
"""
        self.summary_text.setText(summary.strip())

        # نمایش آمار روزانه در جدول
        self.details_table.setColumnCount(3)
        self.details_table.setHorizontalHeaderLabels(["تاریخ", "سفارشات", "فروش"])
        self.details_table.horizontalHeader().setStretchLastSection(True)

        self.details_table.setRowCount(len(report['daily_stats']))
        for row, day in enumerate(report['daily_stats']):
            self.details_table.setItem(row, 0, QTableWidgetItem(day['date']))
            self.details_table.setItem(row, 1, QTableWidgetItem(str(day['orders'])))
            self.details_table.setItem(row, 2, QTableWidgetItem(f"{day['sales']:,} تومان"))

    def show_product_report(self, date):
        from datetime import timedelta
        start_date = datetime.combine(date, datetime.min.time()) - timedelta(days=30)
        end_date = datetime.combine(date, datetime.max.time())

        products = self.report_service.get_product_sales_report(start_date, end_date)

        summary = f"گزارش فروش محصولات (۳۰ روز گذشته تا {date.strftime('%Y-%m-%d')})"
        self.summary_text.setText(summary)

        # نمایش محصولات در جدول
        self.details_table.setColumnCount(5)
        self.details_table.setHorizontalHeaderLabels(["محصول", "تعداد", "فروش کل", "سفارشات", "میانگین فروش"])
        self.details_table.horizontalHeader().setStretchLastSection(True)

        self.details_table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.details_table.setItem(row, 0, QTableWidgetItem(product['product_name']))
            self.details_table.setItem(row, 1, QTableWidgetItem(str(product['total_quantity'])))
            self.details_table.setItem(row, 2, QTableWidgetItem(str(product['total_revenue'])))
            self.details_table.setItem(row, 3, QTableWidgetItem(str(product['orders_count'])))
            self.details_table.setItem(row, 4, QTableWidgetItem(str(product['avg_price_per_order'])))

    def show_hourly_pattern(self, date):
        hourly_data = self.report_service.get_hourly_sales_pattern(date)

        summary = f"الگوی فروش ساعتی - {date.strftime('%Y-%m-%d')}"
        self.summary_text.setText(summary)

        # نمایش آمار ساعتی در جدول
        self.details_table.setColumnCount(3)
        self.details_table.setHorizontalHeaderLabels(["ساعت", "سفارشات", "فروش"])
        self.details_table.horizontalHeader().setStretchLastSection(True)

        self.details_table.setRowCount(24)
        for row, hour_data in enumerate(hourly_data):
            self.details_table.setItem(row, 0, QTableWidgetItem(f"{hour_data['hour']:02d}:00"))
            self.details_table.setItem(row, 1, QTableWidgetItem(str(hour_data['orders_count'])))
            self.details_table.setItem(row, 2, QTableWidgetItem(str(hour_data['total_sales'])))

        # ایجاد نمودار فروش ساعتی
        if MATPLOTLIB_AVAILABLE:
            self.create_hourly_sales_chart(hourly_data)

    def show_table_performance(self):
        tables = self.report_service.get_table_performance()

        summary = "گزارش عملکرد میزها"
        self.summary_text.setText(summary)

        # نمایش عملکرد میزها در جدول
        self.details_table.setColumnCount(4)
        self.details_table.setHorizontalHeaderLabels(["میز", "سفارشات", "فروش کل", "میانگین سفارش"])
        self.details_table.horizontalHeader().setStretchLastSection(True)

        self.details_table.setRowCount(len(tables))
        for row, table in enumerate(tables):
            self.details_table.setItem(row, 0, QTableWidgetItem(str(table['table_number'])))
            self.details_table.setItem(row, 1, QTableWidgetItem(str(table['orders_count'])))
            self.details_table.setItem(row, 2, QTableWidgetItem(str(table['total_sales'])))
            self.details_table.setItem(row, 3, QTableWidgetItem(str(table['avg_order_value'])))

        # ایجاد نمودار اگر matplotlib موجود باشد
        if MATPLOTLIB_AVAILABLE:
            self.create_table_performance_chart(tables)

    def create_hourly_sales_chart(self, hourly_data):
        """ایجاد نمودار فروش ساعتی"""
        if not MATPLOTLIB_AVAILABLE:
            return

        self.chart_canvas.figure.clear()
        ax = self.chart_canvas.figure.add_subplot(111)

        hours = [data['hour'] for data in hourly_data]
        sales = [data['total_sales'].amount for data in hourly_data]
        orders = [data['orders_count'] for data in hourly_data]

        ax.bar(hours, sales, alpha=0.7, label='فروش (تومان)', color='blue')
        ax.set_xlabel('ساعت')
        ax.set_ylabel('فروش (تومان)', color='blue')
        ax.tick_params(axis='y', labelcolor='blue')

        ax2 = ax.twinx()
        ax2.plot(hours, orders, color='red', marker='o', label='تعداد سفارشات')
        ax2.set_ylabel('تعداد سفارشات', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        ax.set_title('الگوی فروش ساعتی')
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, alpha=0.3)

        # اضافه کردن برچسب مقادیر روی نقاط
        for i, (hour, sale, order) in enumerate(zip(hours, sales, orders)):
            if order > 0:  # فقط برای ساعات با سفارش
                ax2.annotate(f'{order}', (hour, order), textcoords="offset points", xytext=(0,10), ha='center')

        self.chart_canvas.figure.tight_layout()
        self.chart_canvas.draw()

    def create_table_performance_chart(self, tables_data):
        """ایجاد نمودار عملکرد میزها"""
        if not MATPLOTLIB_AVAILABLE:
            return

        self.chart_canvas.figure.clear()

        if not tables_data:
            ax = self.chart_canvas.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'داده‌ای برای نمایش وجود ندارد', ha='center', va='center', transform=ax.transAxes)
            self.chart_canvas.draw()
            return

        # نمودار فروش کل میزها
        ax1 = self.chart_canvas.figure.add_subplot(221)
        table_numbers = [str(t['table_number']) for t in tables_data]
        total_sales = [t['total_sales'].amount for t in tables_data]

        bars = ax1.bar(table_numbers, total_sales, color='skyblue')
        ax1.set_title('فروش کل میزها')
        ax1.set_xlabel('شماره میز')
        ax1.set_ylabel('فروش (تومان)')
        ax1.tick_params(axis='x', rotation=45)

        # اضافه کردن برچسب مقادیر روی میله‌ها
        for bar, sales in zip(bars, total_sales):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{sales:,}', ha='center', va='bottom')

        # نمودار تعداد سفارشات میزها
        ax2 = self.chart_canvas.figure.add_subplot(222)
        order_counts = [t['orders_count'] for t in tables_data]

        bars2 = ax2.bar(table_numbers, order_counts, color='lightgreen')
        ax2.set_title('تعداد سفارشات میزها')
        ax2.set_xlabel('شماره میز')
        ax2.set_ylabel('تعداد سفارشات')
        ax2.tick_params(axis='x', rotation=45)

        for bar, count in zip(bars2, order_counts):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count}', ha='center', va='bottom')

        # نمودار میانگین سفارشات
        ax3 = self.chart_canvas.figure.add_subplot(223)
        avg_orders = [int(t['avg_order_value'].amount) for t in tables_data]

        bars3 = ax3.bar(table_numbers, avg_orders, color='orange')
        ax3.set_title('میانگین ارزش سفارشات')
        ax3.set_xlabel('شماره میز')
        ax3.set_ylabel('میانگین (تومان)')
        ax3.tick_params(axis='x', rotation=45)

        for bar, avg in zip(bars3, avg_orders):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{avg:,}', ha='center', va='bottom')

        self.chart_canvas.figure.tight_layout()
        self.chart_canvas.draw()
