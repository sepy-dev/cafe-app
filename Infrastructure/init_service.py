# infrastructure/init_service.py
"""
Initialization Service for Cafe Management System
Creates default admin user and ensures database is properly set up
"""
from datetime import datetime
from infrastructure.database.session import SessionLocal, init_db, engine
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.product_model import ProductModel
from infrastructure.database.base import Base
from web.auth import get_password_hash


class InitializationService:
    """Service to handle application initialization"""
    
    DEFAULT_ADMIN_USERNAME = "admin"
    DEFAULT_ADMIN_PASSWORD = "admin123"
    DEFAULT_ADMIN_FULLNAME = "System Administrator"
    
    @staticmethod
    def initialize_database():
        """Initialize database tables"""
        print("🔧 Initializing database...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
    
    @staticmethod
    def create_default_admin() -> bool:
        """
        Create default admin user if no admin exists
        Returns True if admin was created, False if already exists
        """
        session = SessionLocal()
        try:
            # Check if any admin user exists
            existing_admin = session.query(UserModel).filter_by(role="admin").first()
            
            if existing_admin:
                print(f"ℹ️  Admin user already exists: {existing_admin.username}")
                return False
            
            # Create default admin user
            admin_user = UserModel(
                username=InitializationService.DEFAULT_ADMIN_USERNAME,
                password_hash=get_password_hash(InitializationService.DEFAULT_ADMIN_PASSWORD),
                full_name=InitializationService.DEFAULT_ADMIN_FULLNAME,
                role="admin",
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            session.add(admin_user)
            session.commit()
            
            print("=" * 60)
            print("🎉 DEFAULT ADMIN USER CREATED SUCCESSFULLY!")
            print("=" * 60)
            print(f"   Username: {InitializationService.DEFAULT_ADMIN_USERNAME}")
            print(f"   Password: {InitializationService.DEFAULT_ADMIN_PASSWORD}")
            print("=" * 60)
            print("⚠️  IMPORTANT: Please change the default password after first login!")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating admin user: {str(e)}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def create_sample_products() -> bool:
        """Create sample products if none exist"""
        session = SessionLocal()
        try:
            # Check if products already exist
            existing_products = session.query(ProductModel).count()
            
            if existing_products > 0:
                print(f"ℹ️  Products already exist ({existing_products} products)")
                return False
            
            # Sample products for a cafe
            sample_products = [
                # Hot Drinks
                {"name": "Espresso", "price": 25000, "category": "Hot Drinks"},
                {"name": "Cappuccino", "price": 35000, "category": "Hot Drinks"},
                {"name": "Latte", "price": 40000, "category": "Hot Drinks"},
                {"name": "Americano", "price": 30000, "category": "Hot Drinks"},
                {"name": "Mocha", "price": 45000, "category": "Hot Drinks"},
                {"name": "Hot Chocolate", "price": 35000, "category": "Hot Drinks"},
                {"name": "Tea", "price": 20000, "category": "Hot Drinks"},
                
                # Cold Drinks
                {"name": "Iced Latte", "price": 45000, "category": "Cold Drinks"},
                {"name": "Iced Americano", "price": 35000, "category": "Cold Drinks"},
                {"name": "Cold Brew", "price": 40000, "category": "Cold Drinks"},
                {"name": "Smoothie", "price": 50000, "category": "Cold Drinks"},
                {"name": "Milkshake", "price": 55000, "category": "Cold Drinks"},
                {"name": "Fresh Juice", "price": 40000, "category": "Cold Drinks"},
                
                # Food
                {"name": "Croissant", "price": 30000, "category": "Food"},
                {"name": "Sandwich", "price": 60000, "category": "Food"},
                {"name": "Cake Slice", "price": 45000, "category": "Food"},
                {"name": "Cookie", "price": 20000, "category": "Food"},
                {"name": "Muffin", "price": 35000, "category": "Food"},
                
                # Desserts
                {"name": "Cheesecake", "price": 55000, "category": "Desserts"},
                {"name": "Tiramisu", "price": 60000, "category": "Desserts"},
                {"name": "Ice Cream", "price": 40000, "category": "Desserts"},
            ]
            
            for product_data in sample_products:
                product = ProductModel(
                    name=product_data["name"],
                    price=product_data["price"],
                    category=product_data["category"],
                    is_active=True
                )
                session.add(product)
            
            session.commit()
            print(f"✅ Created {len(sample_products)} sample products")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating sample products: {str(e)}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def full_initialization():
        """Perform complete initialization"""
        print("\n" + "=" * 60)
        print("🚀 CAFE MANAGEMENT SYSTEM - INITIALIZATION")
        print("=" * 60 + "\n")
        
        # Step 1: Initialize database
        InitializationService.initialize_database()
        
        # Step 2: Create default admin
        InitializationService.create_default_admin()
        
        # Step 3: Create sample products
        InitializationService.create_sample_products()
        
        print("\n" + "=" * 60)
        print("✅ INITIALIZATION COMPLETE")
        print("=" * 60 + "\n")
    
    @staticmethod
    def check_system_health() -> dict:
        """Check system health and return status"""
        session = SessionLocal()
        try:
            health = {
                "database_connected": True,
                "admin_exists": False,
                "products_count": 0,
                "users_count": 0,
                "status": "healthy"
            }
            
            # Check admin
            admin = session.query(UserModel).filter_by(role="admin").first()
            health["admin_exists"] = admin is not None
            
            # Count users and products
            health["users_count"] = session.query(UserModel).count()
            health["products_count"] = session.query(ProductModel).count()
            
            # Determine overall status
            if not health["admin_exists"]:
                health["status"] = "needs_admin"
            elif health["products_count"] == 0:
                health["status"] = "needs_products"
            
            return health
            
        except Exception as e:
            return {
                "database_connected": False,
                "admin_exists": False,
                "products_count": 0,
                "users_count": 0,
                "status": "error",
                "error": str(e)
            }
        finally:
            session.close()


def initialize_application():
    """Main initialization function to be called from main.py"""
    InitializationService.full_initialization()


if __name__ == "__main__":
    # Can be run standalone for initialization
    initialize_application()

