# ☕ Cafe Management System

A comprehensive, production-ready cafe management system with dual interfaces: a modern desktop POS application and a web-based ordering system accessible from any device on your network.

## 🌟 Features

### Core Features
- **Dual Interface System**
  - Desktop POS application (PySide6/Qt)
  - Web-based interface accessible from browsers
  - Network-accessible from any device on the same network

- **Order Management**
  - Create and manage orders
  - Table assignment
  - Real-time order tracking
  - Order status management (open, closed, cancelled)
  - Kitchen display mode

- **User Management**
  - Role-based access control (Admin, Cashier, Kitchen)
  - Secure JWT authentication
  - User creation and management (admin only)
  - Default admin user on first run

- **Product Management**
  - Category-based organization
  - Product catalog with pricing
  - Easy product selection interface

- **Reporting & Analytics**
  - Dashboard with key metrics
  - Sales reports
  - Order history
  - Revenue tracking

- **Security**
  - Encrypted password storage (bcrypt)
  - JWT token authentication for web API
  - Role-based access control
  - Session management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows/Linux/macOS
- Network access (for multi-device usage)

### Installation

1. **Clone or download the repository**
   ```bash
   cd cafe-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### First Run

On the first run, the system will automatically:
- Initialize the database
- Create the default admin user
- Generate sample products

**Default Admin Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change the default password immediately after first login!

## 💻 Desktop Application

### Features
- Modern POS interface
- Fast order entry
- Multiple themes (Blue, Dark, Orange, Coffee)
- Table management
- Real-time updates
- Kitchen display mode (dual monitor support)
- Receipt printing
- Backup and restore

### Keyboard Shortcuts
- `F1-F9`: Quick table selection (Table 1-9)
- `Ctrl+N`: New order
- `Ctrl+S`: Save/Submit order
- `Esc`: Clear cart

## 🌐 Web Interface

### Starting the Web Server

1. **Open Desktop Application**
2. **Click the 🌐 button** in the header (Server Settings)
3. **Configure and Start the Server:**
   - Host: `0.0.0.0` (for network access) or `127.0.0.1` (local only)
   - Port: `8080` (or any available port)
   - Click "▶️ راه‌اندازی سرور" to start

### Accessing the Web Interface

**From the same computer:**
```
http://localhost:8080
```

**From other devices on the network:**
```
http://[YOUR-IP]:8080
```
(The exact URL is shown in the Server Settings dialog)

### Web Features
- Responsive design (works on mobile, tablet, desktop)
- Login/Authentication
- Dashboard with statistics
- Create new orders
- View and manage orders
- Admin panel for user management
- Real-time updates

## 📱 Network Access

### Setup for Network Access

1. **Configure Firewall**
   
   **Windows:**
   ```powershell
   # Allow inbound traffic on port 8080
   netsh advfirewall firewall add rule name="Cafe Server" dir=in action=allow protocol=TCP localport=8080
   ```
   
   **Linux:**
   ```bash
   # UFW
   sudo ufw allow 8080/tcp
   
   # iptables
   sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
   ```

2. **Find Your IP Address**
   
   **Windows:**
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" under your active network adapter
   
   **Linux/macOS:**
   ```bash
   ifconfig
   # or
   ip addr show
   ```

3. **Access from Mobile/Other Devices**
   - Connect to the same Wi-Fi network
   - Open browser
   - Navigate to `http://[YOUR-IP]:8080`
   - Login with your credentials

## 🗂️ Project Structure

```
cafe-app/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── application/                 # Application services layer
│   ├── order_service.py
│   ├── menu_service.py
│   └── auth_service.py
│
├── domain/                      # Domain models and business logic
│   ├── entities/
│   │   ├── order.py
│   │   ├── product.py
│   │   └── user.py
│   ├── repository/              # Repository interfaces
│   └── value_objects/
│
├── infrastructure/              # Infrastructure layer
│   ├── init_service.py         # System initialization
│   ├── backup_service.py       # Backup/restore functionality
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── models/             # SQLAlchemy models
│   │   └── repositories/
│   └── printer/
│
├── ui/                          # Desktop UI (PySide6)
│   ├── main_window.py          # Main POS window
│   ├── login_dialog.py         # Login dialog
│   ├── server_settings_dialog.py  # Server configuration
│   ├── styles.py               # Theme management
│   └── widgets/                # Custom widgets
│
└── web/                         # Web interface
    ├── server.py               # Uvicorn server management
    ├── api.py                  # FastAPI application & routes
    ├── auth.py                 # JWT authentication
    ├── config.py               # Server configuration
    ├── static/
    │   ├── style.css           # Modern responsive CSS
    │   └── app.js              # Frontend JavaScript
    └── templates/              # HTML templates
        ├── index.html
        ├── login.html
        ├── dashboard.html
        ├── new_order.html
        ├── orders.html
        └── admin.html
```

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern async web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - Database ORM
- **SQLite** - Database
- **Pydantic** - Data validation
- **python-jose** - JWT tokens
- **passlib[bcrypt]** - Password hashing

### Desktop UI
- **PySide6 (Qt 6)** - Cross-platform GUI framework

### Frontend
- **Vanilla JavaScript** - No heavy frameworks
- **Modern CSS** - Responsive design
- **HTML5**

## 📊 Database Schema

### Users
- `id`, `username`, `password_hash`, `full_name`, `role`, `is_active`, `created_at`, `last_login`

### Products
- `id`, `name`, `price`, `category`, `is_active`

### Orders
- `id`, `table_number`, `status`, `discount`, `created_at`

### Order Items
- `id`, `order_id`, `product_name`, `unit_price`, `quantity`

## 🔐 Security Considerations

1. **Change Default Credentials**
   - Always change the default admin password after installation

2. **Network Security**
   - Use firewall rules to restrict access if needed
   - Consider using HTTPS (requires additional setup)
   - Keep the system on a trusted network

3. **User Management**
   - Create separate accounts for each employee
   - Use appropriate roles (admin, cashier, kitchen)
   - Regularly audit user accounts

4. **Backups**
   - Regularly backup your database
   - Store backups securely
   - Test restore procedures

## 📝 Configuration

### Server Configuration
Server settings are stored in `Config/server_config.json`:

```json
{
  "host": "0.0.0.0",
  "port": 8080,
  "enabled": false,
  "auto_start": false,
  "secret_key": "[auto-generated]",
  "token_expire_minutes": 480,
  "allow_registration": false
}
```

### Database
- Default location: `cafe.db` in the application directory
- Can be backed up using the built-in backup feature

## 🐛 Troubleshooting

### Web Server Won't Start
- Check if port is already in use
- Try a different port
- Check firewall settings
- Ensure all dependencies are installed

### Can't Access from Other Devices
- Verify both devices are on the same network
- Check firewall settings
- Confirm the correct IP address
- Ensure server is running (`0.0.0.0` not `127.0.0.1`)

### Login Issues
- Verify credentials
- Check if user account is active
- Clear browser cache/cookies
- Check token expiration settings

### Database Issues
- Restore from backup if available
- Delete `cafe.db` to reset (will lose all data)
- Check file permissions

## 📦 Backup & Restore

### Creating Backups
1. Open Advanced Settings in desktop app
2. Click "Backup Database"
3. Backups are stored in `backups/` directory

### Restoring Backups
1. Open Advanced Settings
2. Select backup file
3. Click "Restore"
4. Application will restart

## 🔄 Updates & Maintenance

- Keep Python and dependencies updated
- Regularly backup your data
- Monitor system logs
- Clean up old orders periodically

## 📱 Mobile Usage Tips

- Use landscape mode for better layout on phones
- Add to home screen for quick access
- Bookmark the login page
- Enable "Stay logged in" on trusted devices

## 🎨 Customization

### Themes (Desktop)
- Blue Modern (Default)
- Dark
- Orange
- Coffee
Select from the theme dropdown in the header

### Web Interface
- Customize colors in `web/static/style.css`
- Modify logo and branding in templates

## 📈 Performance Tips

- Regularly clean up old closed orders
- Keep product catalog organized
- Use categories effectively
- Monitor database size
- Restart server periodically

## 🤝 Support & Contributing

### Getting Help
- Check this README
- Review code comments
- Test in a safe environment first

### System Requirements
- **CPU:** Any modern processor (2+ cores recommended)
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 500MB free space minimum
- **Network:** Wi-Fi or Ethernet for multi-device access

## 📋 API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Products
- `GET /api/products` - List products
- `GET /api/products/categories` - List categories

### Orders
- `GET /api/orders` - List orders
- `POST /api/orders` - Create order
- `GET /api/orders/{id}` - Get order details
- `PATCH /api/orders/{id}/status` - Update order status

### Admin
- `GET /api/admin/users` - List users (admin only)
- `POST /api/admin/users` - Create user (admin only)
- `PATCH /api/admin/users/{id}/toggle-active` - Toggle user status
- `DELETE /api/admin/users/{id}` - Delete user

### Dashboard
- `GET /api/dashboard/stats` - Get statistics

## 📄 License

This is a custom-built application for cafe management. All rights reserved.

## 🎯 Version

**Version 2.0.0**

### Changelog
- ✅ Complete rewrite with modern architecture
- ✅ Added web interface with responsive design
- ✅ Network accessibility for multi-device usage
- ✅ JWT authentication
- ✅ Role-based access control
- ✅ Automatic admin initialization
- ✅ Modern UI with multiple themes
- ✅ Kitchen display mode
- ✅ Comprehensive API

---

**Built with ❤️ for Cafe Owners**

For questions or support, refer to the code documentation and comments throughout the project.

