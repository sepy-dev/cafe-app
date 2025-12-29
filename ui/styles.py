# ui/styles.py - Professional Theme System with Full Control
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import QObject, Signal
from typing import Dict, Any


class Theme:
    """Base theme class with all color definitions"""
    
    def __init__(self, name: str, colors: Dict[str, str]):
        self.name = name
        self.colors = colors
    
    def get(self, key: str, default: str = "#000000") -> str:
        """Get color by key with fallback"""
        return self.colors.get(key, default)


class ThemePresets:
    """Predefined theme presets"""
    
    @staticmethod
    def modern_blue() -> Theme:
        """Modern blue theme - professional and clean"""
        return Theme("modern_blue", {
            # Primary colors
            "primary": "#2563EB",
            "primary_light": "#60A5FA",
            "primary_dark": "#1E40AF",
            "primary_alpha": "rgba(37, 99, 235, 0.15)",
            
            # Secondary colors
            "secondary": "#10B981",
            "secondary_light": "#34D399",
            "secondary_dark": "#059669",
            
            # Accent colors
            "accent": "#F59E0B",
            "accent_light": "#FCD34D",
            "accent_dark": "#D97706",
            
            # Backgrounds
            "bg_main": "#FFFFFF",
            "bg_secondary": "#F8FAFC",
            "bg_tertiary": "#F1F5F9",
            "bg_card": "#FFFFFF",
            "bg_hover": "#EFF6FF",
            "bg_input": "#F8FAFC",
            
            # Text colors
            "text_primary": "#1E293B",
            "text_secondary": "#64748B",
            "text_tertiary": "#94A3B8",
            "text_inverse": "#FFFFFF",
            "text_on_primary": "#FFFFFF",
            
            # Status colors
            "success": "#059669",
            "warning": "#F59E0B",
            "error": "#DC2626",
            "info": "#06B6D4",
            
            # Borders
            "border_light": "#E2E8F0",
            "border_medium": "#CBD5E1",
            "border_dark": "#94A3B8",
            
            # Shadows
            "shadow_sm": "rgba(0, 0, 0, 0.05)",
            "shadow_md": "rgba(0, 0, 0, 0.1)",
            "shadow_lg": "rgba(0, 0, 0, 0.15)",
        })
    
    @staticmethod
    def dark() -> Theme:
        """Dark theme - modern and easy on the eyes"""
        return Theme("dark", {
            # Primary colors
            "primary": "#6366F1",
            "primary_light": "#818CF8",
            "primary_dark": "#4F46E5",
            "primary_alpha": "rgba(99, 102, 241, 0.15)",
            
            # Secondary colors
            "secondary": "#8B5CF6",
            "secondary_light": "#A78BFA",
            "secondary_dark": "#7C3AED",
            
            # Accent colors
            "accent": "#F59E0B",
            "accent_light": "#FCD34D",
            "accent_dark": "#D97706",
            
            # Backgrounds
            "bg_main": "#1F2937",
            "bg_secondary": "#111827",
            "bg_tertiary": "#374151",
            "bg_card": "#1F2937",
            "bg_hover": "#374151",
            "bg_input": "#374151",
            
            # Text colors
            "text_primary": "#F9FAFB",
            "text_secondary": "#D1D5DB",
            "text_tertiary": "#9CA3AF",
            "text_inverse": "#1F2937",
            "text_on_primary": "#FFFFFF",
            
            # Status colors
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444",
            "info": "#06B6D4",
            
            # Borders
            "border_light": "#374151",
            "border_medium": "#4B5563",
            "border_dark": "#6B7280",
            
            # Shadows
            "shadow_sm": "rgba(0, 0, 0, 0.2)",
            "shadow_md": "rgba(0, 0, 0, 0.3)",
            "shadow_lg": "rgba(0, 0, 0, 0.4)",
        })
    
    @staticmethod
    def warm_orange() -> Theme:
        """Warm orange theme - cozy and inviting"""
        return Theme("warm_orange", {
            # Primary colors
            "primary": "#EA580C",
            "primary_light": "#FB923C",
            "primary_dark": "#C2410C",
            "primary_alpha": "rgba(234, 88, 12, 0.15)",
            
            # Secondary colors
            "secondary": "#059669",
            "secondary_light": "#34D399",
            "secondary_dark": "#047857",
            
            # Accent colors
            "accent": "#DC2626",
            "accent_light": "#F87171",
            "accent_dark": "#B91C1C",
            
            # Backgrounds
            "bg_main": "#FFFFFF",
            "bg_secondary": "#FFF7ED",
            "bg_tertiary": "#FFEDD5",
            "bg_card": "#FFFFFF",
            "bg_hover": "#FED7AA",
            "bg_input": "#FFF7ED",
            
            # Text colors
            "text_primary": "#1E293B",
            "text_secondary": "#64748B",
            "text_tertiary": "#94A3B8",
            "text_inverse": "#FFFFFF",
            "text_on_primary": "#FFFFFF",
            
            # Status colors
            "success": "#059669",
            "warning": "#F59E0B",
            "error": "#DC2626",
            "info": "#06B6D4",
            
            # Borders
            "border_light": "#FED7AA",
            "border_medium": "#FDBA74",
            "border_dark": "#FB923C",
            
            # Shadows
            "shadow_sm": "rgba(234, 88, 12, 0.05)",
            "shadow_md": "rgba(234, 88, 12, 0.1)",
            "shadow_lg": "rgba(234, 88, 12, 0.15)",
        })
    
    @staticmethod
    def coffee_brown() -> Theme:
        """Coffee brown theme - warm cafe aesthetic"""
        return Theme("coffee_brown", {
            # Primary colors
            "primary": "#78350F",
            "primary_light": "#A16207",
            "primary_dark": "#451A03",
            "primary_alpha": "rgba(120, 53, 15, 0.15)",
            
            # Secondary colors  
            "secondary": "#166534",
            "secondary_light": "#22C55E",
            "secondary_dark": "#14532D",
            
            # Accent colors
            "accent": "#B45309",
            "accent_light": "#D97706",
            "accent_dark": "#92400E",
            
            # Backgrounds
            "bg_main": "#FFFBEB",
            "bg_secondary": "#FEF3C7",
            "bg_tertiary": "#FDE68A",
            "bg_card": "#FFFFFF",
            "bg_hover": "#FEF9C3",
            "bg_input": "#FFFBEB",
            
            # Text colors
            "text_primary": "#422006",
            "text_secondary": "#78350F",
            "text_tertiary": "#A16207",
            "text_inverse": "#FFFFFF",
            "text_on_primary": "#FFFFFF",
            
            # Status colors
            "success": "#166534",
            "warning": "#B45309",
            "error": "#B91C1C",
            "info": "#0E7490",
            
            # Borders
            "border_light": "#FDE68A",
            "border_medium": "#FCD34D",
            "border_dark": "#FBBF24",
            
            # Shadows
            "shadow_sm": "rgba(120, 53, 15, 0.05)",
            "shadow_md": "rgba(120, 53, 15, 0.1)",
            "shadow_lg": "rgba(120, 53, 15, 0.15)",
        })


class ThemeManager(QObject):
    """Central theme manager with live updates"""
    
    theme_changed = Signal(Theme)
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._current_theme = ThemePresets.modern_blue()
        self._initialized = True
    
    @property
    def current_theme(self) -> Theme:
        """Get current theme"""
        return self._current_theme
    
    def set_theme(self, theme: Theme):
        """Set new theme and emit signal"""
        self._current_theme = theme
        self.theme_changed.emit(theme)
    
    def set_theme_by_name(self, name: str):
        """Set theme by preset name"""
        themes = {
            "modern_blue": ThemePresets.modern_blue(),
            "dark": ThemePresets.dark(),
            "warm_orange": ThemePresets.warm_orange(),
            "coffee_brown": ThemePresets.coffee_brown(),
        }
        if name in themes:
            self.set_theme(themes[name])
    
    def get_color(self, key: str, default: str = "#000000") -> str:
        """Get color from current theme"""
        return self._current_theme.get(key, default)


class StyleGenerator:
    """Generate QSS styles from theme - Modern & Smooth"""
    
    @staticmethod
    def generate_main_stylesheet(theme: Theme) -> str:
        """Generate complete application stylesheet with modern design"""
        return f"""
        /* ==========================================
           🎨 MODERN GLOBAL STYLES
           ========================================== */
        
        QWidget {{
            font-family: 'Segoe UI', 'SF Pro Display', 'Tahoma', sans-serif;
            font-size: 13px;
            color: {theme.get('text_primary')};
            background-color: {theme.get('bg_main')};
        }}
        
        QMainWindow {{
            background-color: {theme.get('bg_secondary')};
        }}
        
        /* ==========================================
           🎯 HEADER SECTION - Smooth Gradient
           ========================================== */
        
        QWidget[class="header"] {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {theme.get('primary')},
                stop:0.5 {theme.get('primary_light')},
                stop:1 {theme.get('primary')});
            color: {theme.get('text_on_primary')};
            padding: 16px;
            border: none;
            border-radius: 16px;
        }}
        
        QLabel[class="header-title"] {{
            color: {theme.get('text_on_primary')};
            font-size: 22px;
            font-weight: bold;
            background-color: transparent;
        }}
        
        /* ==========================================
           🃏 PRODUCT CARDS - Soft & Modern
           ========================================== */
        
        QWidget[class="product-card"] {{
            background-color: {theme.get('bg_card')};
            border: 1px solid {theme.get('border_light')};
            border-radius: 16px;
            padding: 14px;
        }}
        
        QWidget[class="product-card"]:hover {{
            background-color: {theme.get('bg_hover')};
            border-color: {theme.get('primary')};
        }}
        
        QPushButton[class="product-btn"] {{
            background-color: {theme.get('bg_card')};
            border: 1px solid {theme.get('border_light')};
            border-radius: 14px;
            padding: 14px;
            font-size: 13px;
            font-weight: bold;
            color: {theme.get('text_primary')};
            min-height: 70px;
        }}
        
        QPushButton[class="product-btn"]:hover {{
            background-color: {theme.get('bg_hover')};
            border-color: {theme.get('primary')};
        }}
        
        QPushButton[class="product-btn"]:pressed {{
            background-color: {theme.get('primary_alpha')};
            color: {theme.get('primary')};
        }}
        
        /* ==========================================
           📑 TABS - Pill Style
           ========================================== */
        
        QTabWidget::pane {{
            border: none;
            background-color: transparent;
            border-radius: 12px;
        }}
        
        QTabBar::tab {{
            background-color: {theme.get('bg_tertiary')};
            color: {theme.get('text_secondary')};
            border: none;
            padding: 12px 22px;
            margin-right: 6px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
            min-width: 90px;
        }}
        
        QTabBar::tab:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {theme.get('primary')},
                stop:1 {theme.get('primary_light')});
            color: white;
            font-weight: bold;
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {theme.get('bg_hover')};
            color: {theme.get('text_primary')};
        }}
        
        /* ==========================================
           🛒 CART/ORDER SECTION - Glassmorphism
           ========================================== */
        
        QWidget[class="cart-section"] {{
            background-color: {theme.get('bg_card')};
            border: 1px solid {theme.get('border_light')};
            border-radius: 20px;
        }}
        
        QWidget[class="order-item"] {{
            background-color: {theme.get('bg_main')};
            border: 1px solid {theme.get('border_light')};
            border-radius: 12px;
            padding: 12px;
            margin: 4px;
        }}
        
        QListWidget {{
            border: 1px solid {theme.get('border_light')};
            border-radius: 14px;
            background-color: {theme.get('bg_input')};
            padding: 8px;
            outline: none;
        }}
        
        QListWidget::item {{
            border: none;
            padding: 4px 0;
            border-radius: 8px;
        }}
        
        QListWidget::item:hover {{
            background-color: {theme.get('bg_hover')};
        }}
        
        QListWidget::item:selected {{
            background-color: {theme.get('primary_alpha')};
        }}
        
        /* ==========================================
           🏷️ LABELS & TEXT
           ========================================== */
        
        QLabel[class="price"] {{
            color: {theme.get('accent')};
            font-size: 16px;
            font-weight: bold;
        }}
        
        QLabel[class="total-price"] {{
            color: {theme.get('secondary')};
            font-size: 22px;
            font-weight: bold;
        }}
        
        /* ==========================================
           🔘 BUTTONS - Smooth & Modern
           ========================================== */
        
        QPushButton[class="action-btn"] {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {theme.get('secondary')},
                stop:1 {theme.get('secondary_light')});
            color: {theme.get('text_on_primary')};
            border: none;
            border-radius: 14px;
            padding: 16px 28px;
            font-size: 16px;
            font-weight: bold;
            min-height: 20px;
        }}
        
        QPushButton[class="action-btn"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {theme.get('secondary_dark')},
                stop:1 {theme.get('secondary')});
        }}
        
        QPushButton[class="action-btn"]:pressed {{
            background-color: {theme.get('secondary_dark')};
        }}
        
        QPushButton[class="remove-btn"] {{
            background-color: {theme.get('error')};
            color: {theme.get('text_on_primary')};
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 13px;
            font-weight: bold;
        }}
        
        QPushButton[class="remove-btn"]:hover {{
            background-color: #DC2626;
        }}
        
        QPushButton[class="remove-btn"]:pressed {{
            background-color: #B91C1C;
        }}
        
        /* ==========================================
           📝 INPUT CONTROLS - Soft & Rounded
           ========================================== */
        
        QLineEdit {{
            border: 2px solid {theme.get('border_light')};
            border-radius: 12px;
            padding: 12px 16px;
            background-color: {theme.get('bg_input')};
            color: {theme.get('text_primary')};
            font-size: 14px;
            selection-background-color: {theme.get('primary')};
        }}
        
        QLineEdit:focus {{
            border-color: {theme.get('primary')};
            background-color: {theme.get('bg_main')};
        }}
        
        QLineEdit:disabled {{
            background-color: {theme.get('bg_secondary')};
            color: {theme.get('text_tertiary')};
        }}
        
        QSpinBox {{
            border: 2px solid {theme.get('border_light')};
            border-radius: 10px;
            padding: 8px 12px;
            background-color: {theme.get('bg_input')};
            color: {theme.get('text_primary')};
            font-size: 14px;
            font-weight: bold;
            min-width: 70px;
        }}
        
        QSpinBox:focus {{
            border-color: {theme.get('primary')};
        }}
        
        QSpinBox::up-button {{
            border: none;
            background-color: {theme.get('bg_tertiary')};
            width: 22px;
            border-top-right-radius: 8px;
            margin: 2px;
        }}
        
        QSpinBox::down-button {{
            border: none;
            background-color: {theme.get('bg_tertiary')};
            width: 22px;
            border-bottom-right-radius: 8px;
            margin: 2px;
        }}
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background-color: {theme.get('primary_alpha')};
        }}
        
        QSpinBox::up-arrow {{
            width: 10px;
            height: 10px;
        }}
        
        QSpinBox::down-arrow {{
            width: 10px;
            height: 10px;
        }}
        
        /* ==========================================
           🎛️ COMBOBOX - Beautiful Dropdown
           ========================================== */
        
        QComboBox {{
            border: 2px solid {theme.get('border_light')};
            border-radius: 12px;
            padding: 10px 16px;
            padding-right: 35px;
            background-color: {theme.get('bg_input')};
            color: {theme.get('text_primary')};
            min-width: 120px;
            font-size: 13px;
            font-weight: 500;
        }}
        
        QComboBox:hover {{
            border-color: {theme.get('primary_light')};
            background-color: {theme.get('bg_hover')};
        }}
        
        QComboBox:focus {{
            border-color: {theme.get('primary')};
        }}
        
        QComboBox:on {{
            border-color: {theme.get('primary')};
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 35px;
            background-color: transparent;
            subcontrol-origin: padding;
            subcontrol-position: right center;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            width: 0;
            height: 0;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 8px solid {theme.get('text_secondary')};
            margin-right: 10px;
        }}
        
        QComboBox::down-arrow:hover {{
            border-top-color: {theme.get('primary')};
        }}
        
        QComboBox QAbstractItemView {{
            border: 2px solid {theme.get('primary')};
            border-top: none;
            border-radius: 0px 0px 12px 12px;
            background-color: {theme.get('bg_card')};
            color: {theme.get('text_primary')};
            selection-background-color: {theme.get('primary')};
            selection-color: white;
            padding: 6px;
            outline: none;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 10px 14px;
            border-radius: 8px;
            margin: 2px 4px;
            min-height: 28px;
        }}
        
        QComboBox QAbstractItemView::item:hover {{
            background-color: {theme.get('primary_alpha')};
            color: {theme.get('text_primary')};
        }}
        
        QComboBox QAbstractItemView::item:selected,
        QComboBox QAbstractItemView::item:selected:hover {{
            background-color: {theme.get('primary')};
            color: white;
        }}
        
        QComboBox QAbstractItemView::item:focus {{
            background-color: {theme.get('primary_alpha')};
            color: {theme.get('text_primary')};
            outline: none;
        }}
        
        /* ==========================================
           📜 SCROLL BARS - Minimal & Smooth
           ========================================== */
        
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            border: none;
            background-color: transparent;
            width: 10px;
            border-radius: 5px;
            margin: 4px 2px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {theme.get('border_medium')};
            border-radius: 5px;
            min-height: 40px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {theme.get('primary_light')};
        }}
        
        QScrollBar::handle:vertical:pressed {{
            background-color: {theme.get('primary')};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background-color: transparent;
        }}
        
        QScrollBar:horizontal {{
            border: none;
            background-color: transparent;
            height: 10px;
            border-radius: 5px;
            margin: 2px 4px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {theme.get('border_medium')};
            border-radius: 5px;
            min-width: 40px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {theme.get('primary_light')};
        }}
        
        QScrollBar::handle:horizontal:pressed {{
            background-color: {theme.get('primary')};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background-color: transparent;
        }}
        
        /* ==========================================
           💬 MESSAGE BOXES & DIALOGS - Modern
           ========================================== */
        
        QMessageBox {{
            background-color: {theme.get('bg_card')};
            border-radius: 16px;
        }}
        
        QMessageBox QLabel {{
            color: {theme.get('text_primary')};
            font-size: 14px;
            padding: 10px;
        }}
        
        QMessageBox QPushButton {{
            background-color: {theme.get('primary')};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 24px;
            font-weight: bold;
            min-width: 80px;
        }}
        
        QMessageBox QPushButton:hover {{
            background-color: {theme.get('primary_light')};
        }}
        
        QDialog {{
            background-color: {theme.get('bg_main')};
            border-radius: 20px;
        }}
        
        /* ==========================================
           📦 GROUP BOXES - Soft Cards
           ========================================== */
        
        QGroupBox {{
            border: 1px solid {theme.get('border_light')};
            border-radius: 16px;
            margin-top: 16px;
            padding: 20px;
            padding-top: 30px;
            background-color: {theme.get('bg_card')};
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 6px 16px;
            color: {theme.get('text_primary')};
            background-color: {theme.get('primary')};
            color: white;
            border-radius: 10px;
            font-size: 14px;
        }}
        
        /* ==========================================
           ✨ TOOLTIPS - Floating Style
           ========================================== */
        
        QToolTip {{
            background-color: {theme.get('bg_card')};
            color: {theme.get('text_primary')};
            border: 1px solid {theme.get('border_light')};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12px;
        }}
        
        /* ==========================================
           📋 MENU - Modern Popup
           ========================================== */
        
        QMenu {{
            background-color: {theme.get('bg_card')};
            border: 1px solid {theme.get('border_light')};
            border-radius: 12px;
            padding: 8px;
        }}
        
        QMenu::item {{
            padding: 10px 20px;
            border-radius: 8px;
            margin: 2px 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {theme.get('primary')};
            color: white;
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {theme.get('border_light')};
            margin: 6px 10px;
        }}
        
        /* ==========================================
           🔲 FRAMES - Soft Borders
           ========================================== */
        
        QFrame[frameShape="4"] {{ /* HLine */
            background-color: {theme.get('border_light')};
            max-height: 1px;
            border: none;
        }}
        
        QFrame[frameShape="5"] {{ /* VLine */
            background-color: {theme.get('border_light')};
            max-width: 1px;
            border: none;
        }}
        """


class FontManager:
    """Enhanced font management with better readability"""
    
    @staticmethod
    def get_main_font() -> QFont:
        """Get main application font with better readability"""
        font = QFont("Segoe UI", 13)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        return font
    
    @staticmethod
    def get_title_font() -> QFont:
        """Get title font"""
        font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        return font
    
    @staticmethod
    def get_subtitle_font() -> QFont:
        """Get subtitle font"""
        font = QFont("Segoe UI", 15, QFont.Weight.Medium)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        return font
    
    @staticmethod
    def get_button_font() -> QFont:
        """Get button font"""
        font = QFont("Segoe UI", 13, QFont.Weight.Bold)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        return font
