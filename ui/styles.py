# ui/styles.py - Clean and Simple POS UI Styles
from PySide6.QtGui import QFont


class POSTheme:
    """Clean POS-style theme for cafe application"""

    # Main colors - Clean and professional
    PRIMARY = "#2563EB"          # Modern blue
    PRIMARY_LIGHT = "#60A5FA"    # Light blue
    SECONDARY = "#10B981"        # Green
    ACCENT = "#F59E0B"          # Amber

    # Backgrounds
    BG_MAIN = "#FFFFFF"         # Pure white
    BG_SECONDARY = "#F8FAFC"    # Very light gray
    BG_CARD = "#FFFFFF"         # White cards
    BG_HOVER = "#F1F5F9"        # Light hover

    # Text colors
    TEXT_PRIMARY = "#1E293B"    # Dark slate
    TEXT_SECONDARY = "#64748B"  # Medium gray
    TEXT_LIGHT = "#94A3B8"      # Light gray

    # Status colors
    SUCCESS = "#059669"         # Green
    WARNING = "#D97706"         # Amber
    ERROR = "#DC2626"          # Red

    # Borders
    BORDER_LIGHT = "#E2E8F0"    # Light border
    BORDER_MEDIUM = "#CBD5E1"   # Medium border


class POSStyles:
    """Clean and simple POS-style QSS"""

    @staticmethod
    def get_main_style():
        """Main application stylesheet"""
        return f"""
        /* Global Styles */
        QWidget {{
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 12px;
            color: {POSTheme.TEXT_PRIMARY};
            background-color: {POSTheme.BG_MAIN};
        }}

        QMainWindow {{
            background-color: {POSTheme.BG_SECONDARY};
        }}

        /* Product Buttons - Large and Touch-Friendly */
        QPushButton[class="product-btn"] {{
            background-color: {POSTheme.BG_CARD};
            border: 2px solid {POSTheme.BORDER_LIGHT};
            border-radius: 8px;
            padding: 12px;
            font-size: 12px;
            font-weight: bold;
            color: {POSTheme.TEXT_PRIMARY};
            min-height: 70px;
        }}

        QPushButton[class="product-btn"]:hover {{
            background-color: {POSTheme.BG_HOVER};
            border-color: {POSTheme.PRIMARY};
        }}

        QPushButton[class="product-btn"]:pressed {{
            background-color: {POSTheme.PRIMARY_LIGHT};
            color: white;
        }}

        /* Category Tabs */
        QTabBar::tab {{
            background-color: {POSTheme.BG_SECONDARY};
            color: {POSTheme.TEXT_SECONDARY};
            border: none;
            padding: 10px 16px;
            margin-right: 2px;
            font-size: 12px;
            font-weight: 500;
        }}

        QTabBar::tab:selected {{
            background-color: {POSTheme.PRIMARY};
            color: white;
            font-weight: bold;
        }}

        QTabBar::tab:hover {{
            background-color: {POSTheme.PRIMARY_LIGHT};
            color: {POSTheme.BG_MAIN};
        }}

        /* Cart/Order Section */
        QWidget[class="cart-section"] {{
            background-color: {POSTheme.BG_CARD};
            border: 2px solid {POSTheme.BORDER_LIGHT};
            border-radius: 12px;
        }}

        /* Order Items */
        QWidget[class="order-item"] {{
            background-color: {POSTheme.BG_MAIN};
            border: 1px solid {POSTheme.BORDER_LIGHT};
            border-radius: 8px;
            padding: 12px;
            margin: 4px;
        }}

        /* Price Labels */
        QLabel[class="price"] {{
            color: {POSTheme.ACCENT};
            font-size: 16px;
            font-weight: bold;
        }}

        QLabel[class="total-price"] {{
            color: {POSTheme.SECONDARY};
            font-size: 18px;
            font-weight: bold;
        }}

        /* Action Buttons */
        QPushButton[class="action-btn"] {{
            background-color: {POSTheme.SECONDARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            min-height: 16px;
        }}

        QPushButton[class="action-btn"]:hover {{
            background-color: #059669;
        }}

        /* Header Section */
        QWidget[class="header"] {{
            background-color: {POSTheme.PRIMARY};
            color: white;
            padding: 16px;
            border-radius: 0px;
        }}

        QLabel[class="header-title"] {{
            color: white;
            font-size: 18px;
            font-weight: bold;
        }}

        /* Quantity Controls */
        QSpinBox {{
            border: 2px solid {POSTheme.BORDER_LIGHT};
            border-radius: 6px;
            padding: 4px 8px;
            background-color: white;
            font-size: 14px;
            font-weight: bold;
            min-width: 60px;
        }}

        /* Remove Buttons */
        QPushButton[class="remove-btn"] {{
            background-color: {POSTheme.ERROR};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 12px;
        }}

        QPushButton[class="remove-btn"]:hover {{
            background-color: #B91C1C;
        }}

        /* Combo Boxes */
        QComboBox {{
            border: 2px solid {POSTheme.BORDER_LIGHT};
            border-radius: 8px;
            padding: 8px 12px;
            background-color: white;
            min-width: 120px;
            font-size: 12px;
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        /* Grid Layouts */
        QGridLayout {{
            spacing: 12px;
        }}

        /* Focus Styles */
        QPushButton:focus, QComboBox:focus {{
            border-color: {POSTheme.PRIMARY};
        }}
        """


class FontManager:
    """Font management utilities"""

    @staticmethod
    def get_main_font():
        """Get main application font"""
        font = QFont("Segoe UI", 12)
        font.setStyleHint(QFont.System)
        return font

    @staticmethod
    def get_title_font():
        """Get title font"""
        font = QFont("Segoe UI", 18, QFont.Bold)
        font.setStyleHint(QFont.System)
        return font

    @staticmethod
    def get_subtitle_font():
        """Get subtitle font"""
        font = QFont("Segoe UI", 14)
        font.setStyleHint(QFont.System)
        return font