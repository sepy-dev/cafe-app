# web/api.py - FastAPI Application and API Routes
import os
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from web.auth import (
    Token, UserLogin, UserCreate, UserResponse,
    authenticate_user, create_access_token, get_current_user, get_current_admin,
    get_password_hash
)
from infrastructure.database.session import SessionLocal
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.product_model import ProductModel
from infrastructure.database.models.order_model import OrderModel
from infrastructure.database.models.order_item_model import OrderItemModel


# Initialize FastAPI app
app = FastAPI(
    title="☕ Cafe Management API",
    description="API for Cafe Order Management System",
    version="2.0.0"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates directory
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Create directories if they don't exist
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Mount static files
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ============== Pydantic Models ==============

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    category: str
    is_active: bool


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    unit_price: int
    quantity: int
    total: int


class OrderCreate(BaseModel):
    table_number: Optional[int] = None
    items: List[OrderItemCreate]
    discount: int = 0


class OrderResponse(BaseModel):
    id: int
    table_number: Optional[int]
    status: str
    discount: int
    created_at: datetime
    items: List[OrderItemResponse]
    subtotal: int
    total: int


class OrderStatusUpdate(BaseModel):
    status: str


class DashboardStats(BaseModel):
    total_orders_today: int
    total_revenue_today: int
    pending_orders: int
    total_products: int
    total_users: int


# ============== Helper Functions ==============

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============== Web Routes (HTML) ==============

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - redirect to login or dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard page (requires authentication via JS)"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    """Orders page"""
    return templates.TemplateResponse("orders.html", {"request": request})


@app.get("/new-order", response_class=HTMLResponse)
async def new_order_page(request: Request):
    """New order page"""
    return templates.TemplateResponse("new_order.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """Admin panel page"""
    return templates.TemplateResponse("admin.html", {"request": request})


# ============== API Routes ==============

@app.post("/api/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login and get access token"""
    user = authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    session = SessionLocal()
    try:
        db_user = session.query(UserModel).filter_by(id=user.id).first()
        if db_user:
            db_user.last_login = datetime.utcnow()
            session.commit()
    finally:
        session.close()
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role
        }
    )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


# ============== Products API ==============

@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(current_user: UserModel = Depends(get_current_user)):
    """Get all active products"""
    session = SessionLocal()
    try:
        products = session.query(ProductModel).filter_by(is_active=True).all()
        return [
            ProductResponse(
                id=p.id,
                name=p.name,
                price=p.price,
                category=p.category,
                is_active=p.is_active
            )
            for p in products
        ]
    finally:
        session.close()


@app.get("/api/products/categories")
async def get_categories(current_user: UserModel = Depends(get_current_user)):
    """Get all product categories"""
    session = SessionLocal()
    try:
        products = session.query(ProductModel).filter_by(is_active=True).all()
        categories = list(set(p.category for p in products))
        return {"categories": sorted(categories)}
    finally:
        session.close()


# ============== Orders API ==============

@app.get("/api/orders", response_model=List[OrderResponse])
async def get_orders(
    status_filter: Optional[str] = None,
    limit: int = 50,
    current_user: UserModel = Depends(get_current_user)
):
    """Get orders (all for admin, today's for others)"""
    session = SessionLocal()
    try:
        query = session.query(OrderModel)
        
        # Non-admin users see only today's orders
        if current_user.role != "admin":
            today = datetime.utcnow().date()
            query = query.filter(OrderModel.created_at >= today)
        
        if status_filter:
            query = query.filter(OrderModel.status == status_filter)
        
        orders = query.order_by(OrderModel.created_at.desc()).limit(limit).all()
        
        result = []
        for order in orders:
            items = session.query(OrderItemModel).filter_by(order_id=order.id).all()
            order_items = [
                OrderItemResponse(
                    id=item.id,
                    product_name=item.product_name,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                    total=item.unit_price * item.quantity
                )
                for item in items
            ]
            subtotal = sum(item.total for item in order_items)
            
            result.append(OrderResponse(
                id=order.id,
                table_number=order.table_number,
                status=order.status,
                discount=order.discount,
                created_at=order.created_at,
                items=order_items,
                subtotal=subtotal,
                total=max(0, subtotal - order.discount)
            ))
        
        return result
    finally:
        session.close()


@app.post("/api/orders", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new order"""
    session = SessionLocal()
    try:
        # Get products for the order
        product_ids = [item.product_id for item in order_data.items]
        products = {
            p.id: p 
            for p in session.query(ProductModel).filter(
                ProductModel.id.in_(product_ids),
                ProductModel.is_active == True
            ).all()
        }
        
        # Validate all products exist
        for item in order_data.items:
            if item.product_id not in products:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"محصول با شناسه {item.product_id} یافت نشد"
                )
        
        # Create order
        order = OrderModel(
            table_number=order_data.table_number,
            status="open",
            discount=order_data.discount,
            created_at=datetime.utcnow()
        )
        session.add(order)
        session.flush()  # Get order ID
        
        # Create order items
        order_items = []
        for item in order_data.items:
            product = products[item.product_id]
            order_item = OrderItemModel(
                order_id=order.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity
            )
            session.add(order_item)
            order_items.append(OrderItemResponse(
                id=0,  # Will be set after commit
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
                total=product.price * item.quantity
            ))
        
        session.commit()
        
        subtotal = sum(item.total for item in order_items)
        
        return OrderResponse(
            id=order.id,
            table_number=order.table_number,
            status=order.status,
            discount=order.discount,
            created_at=order.created_at,
            items=order_items,
            subtotal=subtotal,
            total=max(0, subtotal - order.discount)
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد سفارش: {str(e)}"
        )
    finally:
        session.close()


@app.patch("/api/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_user: UserModel = Depends(get_current_user)
):
    """Update order status"""
    valid_statuses = ["open", "closed", "cancelled"]
    if status_data.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"وضعیت نامعتبر. وضعیت‌های مجاز: {', '.join(valid_statuses)}"
        )
    
    session = SessionLocal()
    try:
        order = session.query(OrderModel).filter_by(id=order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="سفارش یافت نشد"
            )
        
        order.status = status_data.status
        session.commit()
        
        return {"message": "وضعیت سفارش به‌روزرسانی شد", "status": status_data.status}
    finally:
        session.close()


@app.get("/api/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific order"""
    session = SessionLocal()
    try:
        order = session.query(OrderModel).filter_by(id=order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="سفارش یافت نشد"
            )
        
        items = session.query(OrderItemModel).filter_by(order_id=order.id).all()
        order_items = [
            OrderItemResponse(
                id=item.id,
                product_name=item.product_name,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total=item.unit_price * item.quantity
            )
            for item in items
        ]
        subtotal = sum(item.total for item in order_items)
        
        return OrderResponse(
            id=order.id,
            table_number=order.table_number,
            status=order.status,
            discount=order.discount,
            created_at=order.created_at,
            items=order_items,
            subtotal=subtotal,
            total=max(0, subtotal - order.discount)
        )
    finally:
        session.close()


# ============== Dashboard API ==============

@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: UserModel = Depends(get_current_user)):
    """Get dashboard statistics"""
    session = SessionLocal()
    try:
        today = datetime.utcnow().date()
        
        # Today's orders
        today_orders = session.query(OrderModel).filter(
            OrderModel.created_at >= today
        ).all()
        
        # Calculate revenue
        total_revenue = 0
        for order in today_orders:
            if order.status != "cancelled":
                items = session.query(OrderItemModel).filter_by(order_id=order.id).all()
                subtotal = sum(item.unit_price * item.quantity for item in items)
                total_revenue += max(0, subtotal - order.discount)
        
        # Pending orders (open orders)
        pending_orders = session.query(OrderModel).filter_by(status="open").count()
        
        # Active products
        total_products = session.query(ProductModel).filter_by(is_active=True).count()
        
        # Total users (admin only)
        total_users = 0
        if current_user.role == "admin":
            total_users = session.query(UserModel).count()
        
        return DashboardStats(
            total_orders_today=len(today_orders),
            total_revenue_today=total_revenue,
            pending_orders=pending_orders,
            total_products=total_products,
            total_users=total_users
        )
    finally:
        session.close()


# ============== Admin API ==============

@app.get("/api/admin/users", response_model=List[UserResponse])
async def get_all_users(current_user: UserModel = Depends(get_current_admin)):
    """Get all users (admin only)"""
    session = SessionLocal()
    try:
        users = session.query(UserModel).all()
        return [
            UserResponse(
                id=u.id,
                username=u.username,
                full_name=u.full_name,
                role=u.role,
                is_active=u.is_active,
                created_at=u.created_at,
                last_login=u.last_login
            )
            for u in users
        ]
    finally:
        session.close()


@app.post("/api/admin/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: UserModel = Depends(get_current_admin)
):
    """Create a new user (admin only)"""
    session = SessionLocal()
    try:
        # Check if username exists
        existing = session.query(UserModel).filter_by(username=user_data.username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این نام کاربری قبلاً استفاده شده است"
            )
        
        # Validate
        if len(user_data.username) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="نام کاربری باید حداقل ۳ کاراکتر باشد"
            )
        if len(user_data.password) < 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور باید حداقل ۴ کاراکتر باشد"
            )
        
        # Create user with bcrypt hash
        user = UserModel(
            username=user_data.username,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            role=user_data.role,
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return UserResponse(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ایجاد کاربر: {str(e)}"
        )
    finally:
        session.close()


@app.patch("/api/admin/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    current_user: UserModel = Depends(get_current_admin)
):
    """Toggle user active status (admin only)"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="نمی‌توانید حساب خودتان را غیرفعال کنید"
        )
    
    session = SessionLocal()
    try:
        user = session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کاربر یافت نشد"
            )
        
        user.is_active = not user.is_active
        session.commit()
        
        status_text = "فعال" if user.is_active else "غیرفعال"
        return {"message": f"کاربر {status_text} شد", "is_active": user.is_active}
    finally:
        session.close()


@app.delete("/api/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_admin)
):
    """Delete a user (admin only)"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="نمی‌توانید حساب خودتان را حذف کنید"
        )
    
    session = SessionLocal()
    try:
        user = session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کاربر یافت نشد"
            )
        
        session.delete(user)
        session.commit()
        
        return {"message": "کاربر حذف شد"}
    finally:
        session.close()


# ============== Server Info ==============

@app.get("/api/server/info")
async def get_server_info():
    """Get server information (public endpoint)"""
    return {
        "name": "Cafe Management System",
        "version": "2.0.0",
        "status": "running"
    }

