# ui/styles.py - Modern UI Styles and Themes
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt


class ModernTheme:
    """Modern UI theme for the cafe application"""

    # Colors
    PRIMARY_COLOR = "#1976D2"      # Blue
    PRIMARY_LIGHT = "#42A5F5"      # Light Blue
    PRIMARY_DARK = "#1565C0"       # Dark Blue
    SECONDARY_COLOR = "#FF6F00"    # Orange
    ACCENT_COLOR = "#4CAF50"       # Green
    WARNING_COLOR = "#FF9800"      # Orange warning
    ERROR_COLOR = "#F44336"        # Red
    SUCCESS_COLOR = "#4CAF50"      # Green

    # Background colors
    BG_PRIMARY = "#FAFAFA"         # Light gray background
    BG_SECONDARY = "#FFFFFF"       # White
    BG_CARD = "#FFFFFF"           # Card background
    BG_HOVER = "#F5F5F5"          # Hover background

    # Text colors
    TEXT_PRIMARY = "#212121"      # Dark gray text
    TEXT_SECONDARY = "#757575"    # Medium gray text
    TEXT_HINT = "#BDBDBD"         # Light gray hint text

    # Border colors
    BORDER_LIGHT = "#E0E0E0"      # Light border
    BORDER_MEDIUM = "#BDBDBD"     # Medium border

    # Shadows
    SHADOW_LIGHT = "0 2px 4px rgba(0,0,0,0.1)"
    SHADOW_MEDIUM = "0 4px 8px rgba(0,0,0,0.15)"
    SHADOW_HEAVY = "0 8px 16px rgba(0,0,0,0.2)"


class ThemeManager:
    """Theme management system"""

    @staticmethod
    def get_available_themes():
        """Get list of available themes"""
        return {
            "modern_blue": ModernTheme.__dict__,
            "dark_mode": {
                "PRIMARY_COLOR": "#BB86FC",
                "PRIMARY_LIGHT": "#CF9FFF",
                "PRIMARY_DARK": "#9D46FF",
                "SECONDARY_COLOR": "#03DAC6",
                "ACCENT_COLOR": "#CF6679",
                "WARNING_COLOR": "#FFAB40",
                "ERROR_COLOR": "#CF6679",
                "SUCCESS_COLOR": "#03DAC6",
                "BG_PRIMARY": "#121212",
                "BG_SECONDARY": "#1E1E1E",
                "BG_CARD": "#2D2D2D",
                "BG_HOVER": "#3D3D3D",
                "TEXT_PRIMARY": "#FFFFFF",
                "TEXT_SECONDARY": "#B3B3B3",
                "TEXT_HINT": "#808080",
                "BORDER_LIGHT": "#404040",
                "BORDER_MEDIUM": "#606060"
            },
            "warm_orange": {
                "PRIMARY_COLOR": "#FF6F00",
                "PRIMARY_LIGHT": "#FF9E40",
                "PRIMARY_DARK": "#E65100",
                "SECONDARY_COLOR": "#4CAF50",
                "ACCENT_COLOR": "#2196F3",
                "WARNING_COLOR": "#FF9800",
                "ERROR_COLOR": "#F44336",
                "SUCCESS_COLOR": "#4CAF50",
                "BG_PRIMARY": "#FFF8E1",
                "BG_SECONDARY": "#FFFFFF",
                "BG_CARD": "#FFFFFF",
                "BG_HOVER": "#FFF3C4",
                "TEXT_PRIMARY": "#3E2723",
                "TEXT_SECONDARY": "#6D4C41",
                "TEXT_HINT": "#A1887F",
                "BORDER_LIGHT": "#FFCC02",
                "BORDER_MEDIUM": "#FFB300"
            }
        }

    @staticmethod
    def apply_theme(theme_name: str):
        """Apply a specific theme"""
        themes = ThemeManager.get_available_themes()
        if theme_name in themes:
            theme = themes[theme_name]
            # Update ModernTheme class attributes
            for key, value in theme.items():
                setattr(ModernTheme, key, value)


class ModernStyles:
    """Modern QSS styles for the application"""

    @staticmethod
    def get_main_style():
        """Main application stylesheet"""
        return f"""
        /* Global Styles */
        QWidget {{
            font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
            font-size: 11px;
            color: {ModernTheme.TEXT_PRIMARY};
            background-color: {ModernTheme.BG_PRIMARY};
        }}

        /* Main Window */
        QMainWindow {{
            background-color: {ModernTheme.BG_PRIMARY};
        }}

        /* Buttons */
        QPushButton {{
            background-color: {ModernTheme.PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 16px;
            font-weight: 500;
            font-size: 11px;
            min-height: 14px;
        }}

        QPushButton:hover {{
            background-color: {ModernTheme.PRIMARY_LIGHT};
            transform: translateY(-1px);
        }}

        QPushButton:pressed {{
            background-color: {ModernTheme.PRIMARY_DARK};
            transform: translateY(0px);
        }}

        QPushButton:disabled {{
            background-color: {ModernTheme.BORDER_LIGHT};
            color: {ModernTheme.TEXT_HINT};
        }}

        /* Sidebar Buttons */
        QPushButton[class="sidebar-btn"] {{
            background-color: transparent;
            color: {ModernTheme.TEXT_SECONDARY};
            text-align: left;
            padding: 12px 16px;
            margin: 2px 8px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
        }}

        QPushButton[class="sidebar-btn"]:hover {{
            background-color: {ModernTheme.BG_HOVER};
            color: {ModernTheme.TEXT_PRIMARY};
        }}

        QPushButton[class="sidebar-btn"]:checked {{
            background-color: {ModernTheme.PRIMARY_COLOR};
            color: white;
        }}

        /* Success Button */
        QPushButton[class="success-btn"] {{
            background-color: {ModernTheme.SUCCESS_COLOR};
        }}

        QPushButton[class="success-btn"]:hover {{
            background-color: #45A049;
        }}

        /* Warning Button */
        QPushButton[class="warning-btn"] {{
            background-color: {ModernTheme.WARNING_COLOR};
        }}

        QPushButton[class="warning-btn"]:hover {{
            background-color: #FB8C00;
        }}

        /* Danger Button */
        QPushButton[class="danger-btn"] {{
            background-color: {ModernTheme.ERROR_COLOR};
        }}

        QPushButton[class="danger-btn"]:hover {{
            background-color: #D32F2F;
        }}

        /* Group Boxes */
        QGroupBox {{
            font-weight: bold;
            font-size: 13px;
            color: {ModernTheme.TEXT_PRIMARY};
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 8px;
            margin-top: 8px;
            padding-top: 8px;
            background-color: {ModernTheme.BG_CARD};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px 0 8px;
            color: {ModernTheme.PRIMARY_COLOR};
            font-weight: bold;
        }}

        /* Labels */
        QLabel {{
            color: {ModernTheme.TEXT_PRIMARY};
        }}

        QLabel[class="title"] {{
            font-size: 18px;
            font-weight: bold;
            color: {ModernTheme.PRIMARY_COLOR};
        }}

        QLabel[class="subtitle"] {{
            font-size: 14px;
            color: {ModernTheme.TEXT_SECONDARY};
        }}

        QLabel[class="price"] {{
            font-size: 16px;
            font-weight: bold;
            color: {ModernTheme.SECONDARY_COLOR};
        }}

        QLabel[class="total"] {{
            font-size: 20px;
            font-weight: bold;
            color: {ModernTheme.SUCCESS_COLOR};
        }}

        /* Line Edits */
        QLineEdit {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 6px;
            padding: 8px 12px;
            background-color: white;
            font-size: 12px;
        }}

        QLineEdit:focus {{
            border-color: {ModernTheme.PRIMARY_COLOR};
        }}

        QLineEdit:placeholder {{
            color: {ModernTheme.TEXT_HINT};
        }}

        /* Combo Boxes */
        QComboBox {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 6px;
            padding: 6px 12px;
            background-color: white;
            min-width: 100px;
        }}

        QComboBox:hover {{
            border-color: {ModernTheme.PRIMARY_LIGHT};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid {ModernTheme.TEXT_SECONDARY};
            margin-right: 8px;
        }}

        /* Tables */
        QTableWidget {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 8px;
            background-color: white;
            gridline-color: {ModernTheme.BORDER_LIGHT};
        }}

        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {ModernTheme.BORDER_LIGHT};
        }}

        QTableWidget::item:selected {{
            background-color: {ModernTheme.PRIMARY_LIGHT};
            color: white;
        }}

        QHeaderView::section {{
            background-color: {ModernTheme.BG_HOVER};
            color: {ModernTheme.TEXT_PRIMARY};
            padding: 8px;
            border: none;
            border-bottom: 2px solid {ModernTheme.BORDER_LIGHT};
            font-weight: bold;
        }}

        /* List Widgets */
        QListWidget {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 8px;
            background-color: white;
        }}

        QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {ModernTheme.BORDER_LIGHT};
        }}

        QListWidget::item:selected {{
            background-color: {ModernTheme.PRIMARY_LIGHT};
            color: white;
        }}

        QListWidget::item:hover {{
            background-color: {ModernTheme.BG_HOVER};
        }}

        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        /* Tabs */
        QTabWidget::pane {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 8px;
            background-color: white;
        }}

        QTabBar::tab {{
            background-color: {ModernTheme.BG_HOVER};
            color: {ModernTheme.TEXT_SECONDARY};
            border: none;
            padding: 10px 16px;
            margin-right: 2px;
            border-radius: 6px 6px 0 0;
        }}

        QTabBar::tab:selected {{
            background-color: white;
            color: {ModernTheme.PRIMARY_COLOR};
            font-weight: bold;
        }}

        QTabBar::tab:hover {{
            background-color: {ModernTheme.PRIMARY_LIGHT};
            color: white;
        }}

        /* Spin Boxes */
        QSpinBox {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 6px;
            padding: 4px 8px;
            background-color: white;
        }}

        QSpinBox::up-button, QSpinBox::down-button {{
            border: none;
            background-color: {ModernTheme.BORDER_LIGHT};
            width: 16px;
        }}

        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background-color: {ModernTheme.PRIMARY_LIGHT};
        }}

        /* Form Layout */
        QFormLayout {{
            spacing: 12px;
        }}

        /* Progress Bars */
        QProgressBar {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 4px;
            text-align: center;
            background-color: white;
        }}

        QProgressBar::chunk {{
            background-color: {ModernTheme.PRIMARY_COLOR};
            border-radius: 2px;
        }}

        /* Text Edits */
        QTextEdit {{
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 8px;
            background-color: white;
            padding: 8px;
        }}

        /* Menu Cards */
        QWidget[class="product-card"] {{
            background-color: {ModernTheme.BG_CARD};
            border: 2px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 12px;
            padding: 16px;
        }}

        QWidget[class="product-card"]:hover {{
            border-color: {ModernTheme.PRIMARY_LIGHT};
            background-color: {ModernTheme.BG_HOVER};
            transform: translateY(-2px);
        }}

        /* Order Items */
        QWidget[class="order-item"] {{
            background-color: {ModernTheme.BG_CARD};
            border: 1px solid {ModernTheme.BORDER_LIGHT};
            border-radius: 8px;
            padding: 12px;
            margin: 4px 0;
        }}

        /* Status Indicators */
        QLabel[class="status-open"] {{
            color: {ModernTheme.WARNING_COLOR};
            font-weight: bold;
        }}

        QLabel[class="status-closed"] {{
            color: {ModernTheme.SUCCESS_COLOR};
            font-weight: bold;
        }}

        /* Animations */
        QPushButton {{
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        QWidget[class="product-card"] {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        QListWidget::item {{
            transition: all 0.2s ease;
        }}

        /* Modern Shadows */
        QWidget[class="product-card"] {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        QWidget[class="product-card"]:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}

        /* Smooth Scrolling */
        QScrollArea {{
            background-color: transparent;
        }}

        QScrollArea QWidget {{
            background-color: transparent;
        }}

        /* Focus Styles */
        QPushButton:focus, QLineEdit:focus, QComboBox:focus {{
            outline: 2px solid {ModernTheme.PRIMARY_COLOR};
            outline-offset: 2px;
        }}
        """


class FontManager:
    """Font management utilities"""

    @staticmethod
    def get_main_font():
        """Get main application font"""
        font = QFont("Segoe UI", 11)
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
