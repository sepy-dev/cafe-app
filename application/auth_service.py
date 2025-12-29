# application/auth_service.py - Authentication Service
import hashlib
from typing import Optional, Tuple
from datetime import datetime

from infrastructure.database.session import SessionLocal
from infrastructure.database.models.user_model import UserModel


class AuthService:
    """Authentication and user management service"""
    
    _current_user = None
    
    def __init__(self):
        self.session = SessionLocal()
        self._ensure_admin_exists()
    
    def _ensure_admin_exists(self):
        """Create default admin if no users exist"""
        user_count = self.session.query(UserModel).count()
        if user_count == 0:
            # No users, will prompt for registration
            pass
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def has_users(self) -> bool:
        """Check if any users exist in the system"""
        return self.session.query(UserModel).count() > 0
    
    def register(self, username: str, password: str, full_name: str, role: str = "cashier") -> Tuple[bool, str]:
        """Register a new user"""
        # Validate
        if len(username) < 3:
            return False, "نام کاربری باید حداقل ۳ کاراکتر باشد"
        if len(password) < 4:
            return False, "رمز عبور باید حداقل ۴ کاراکتر باشد"
        if len(full_name) < 2:
            return False, "نام کامل باید حداقل ۲ کاراکتر باشد"
        
        # Check if username exists
        existing = self.session.query(UserModel).filter_by(username=username).first()
        if existing:
            return False, "این نام کاربری قبلاً استفاده شده است"
        
        # Create user
        user = UserModel(
            username=username,
            password_hash=self._hash_password(password),
            full_name=full_name,
            role=role,
            is_active=True
        )
        
        try:
            self.session.add(user)
            self.session.commit()
            return True, "ثبت‌نام با موفقیت انجام شد"
        except Exception as e:
            self.session.rollback()
            return False, f"خطا در ثبت‌نام: {str(e)}"
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Login user"""
        user = self.session.query(UserModel).filter_by(username=username).first()
        
        if not user:
            return False, "نام کاربری یافت نشد"
        
        if not user.is_active:
            return False, "این حساب غیرفعال شده است"
        
        if user.password_hash != self._hash_password(password):
            return False, "رمز عبور اشتباه است"
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.session.commit()
        
        # Set current user
        AuthService._current_user = user
        
        return True, f"خوش آمدید {user.full_name}!"
    
    def logout(self):
        """Logout current user"""
        AuthService._current_user = None
    
    @classmethod
    def get_current_user(cls) -> Optional[UserModel]:
        """Get currently logged in user"""
        return cls._current_user
    
    @classmethod
    def is_logged_in(cls) -> bool:
        """Check if user is logged in"""
        return cls._current_user is not None
    
    def get_all_users(self):
        """Get all users"""
        return self.session.query(UserModel).all()
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user"""
        user = self.session.query(UserModel).get(user_id)
        if user:
            user.is_active = False
            self.session.commit()
            return True
        return False

