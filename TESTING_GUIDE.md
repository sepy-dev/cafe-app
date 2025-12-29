# 🧪 Testing Guide - Cafe Management System

This guide will help you test all features of the Cafe Management System.

## 📋 Pre-Testing Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Application runs without errors
- [ ] Database initialized successfully
- [ ] Default admin user created

## 🖥️ Desktop Application Tests

### 1. Launch & Initialization Test

**Steps:**
1. Run `python main.py`
2. Check console output for initialization messages
3. Verify default admin credentials displayed

**Expected Results:**
- ✅ Database tables created
- ✅ Default admin user created (admin/admin123)
- ✅ Sample products created
- ✅ Login dialog appears

### 2. Login Test

**Test Cases:**
- Valid credentials (admin/admin123)
- Invalid credentials
- Empty fields

**Expected Results:**
- ✅ Successful login with valid credentials
- ✅ Error message for invalid credentials
- ✅ Main window opens after successful login

### 3. POS Interface Test

**Features to Test:**
- [ ] Product categories display correctly
- [ ] Products display with name, price, category
- [ ] Click on product adds to cart
- [ ] Quantity controls (+/-) work
- [ ] Remove item from cart works
- [ ] Table selection works
- [ ] Discount field accepts numbers
- [ ] Total calculations are correct
- [ ] Submit order creates order successfully

### 4. Theme Test

**Steps:**
1. Select each theme from dropdown:
   - Blue Modern
   - Dark
   - Orange  
   - Coffee

**Expected Results:**
- ✅ UI colors change immediately
- ✅ All elements remain readable
- ✅ No visual glitches

### 5. Server Settings Test

**Steps:**
1. Click 🌐 button in header
2. Server Settings dialog opens
3. Verify current status displayed
4. Click "Start Server"
5. Wait for confirmation
6. Check URLs displayed

**Expected Results:**
- ✅ Dialog opens without errors
- ✅ Server starts successfully
- ✅ Local URL displayed (http://127.0.0.1:8080)
- ✅ Network URL displayed (http://[IP]:8080)
- ✅ Status changes to "Running"

## 🌐 Web Interface Tests

### 1. Web Server Accessibility

**Local Access Test:**
1. Start web server from desktop app
2. Open browser
3. Navigate to `http://localhost:8080`

**Expected Results:**
- ✅ Home page loads
- ✅ Styles applied correctly
- ✅ No console errors

### 2. Network Access Test

**Required:**
- Two devices on same network (e.g., computer + phone)
- Server running with host `0.0.0.0`

**Steps:**
1. On main computer:
   - Start server
   - Note the network URL
2. On second device (phone/tablet):
   - Connect to same Wi-Fi
   - Open browser
   - Navigate to network URL
   - Attempt to access the site

**Expected Results:**
- ✅ Page loads on second device
- ✅ Styles render correctly
- ✅ Can login
- ✅ Can create orders

**Troubleshooting if fails:**
- Check firewall settings
- Verify both devices on same network
- Try pinging server IP from client device
- Check server is using 0.0.0.0 not 127.0.0.1

### 3. Web Login Test

**Test Cases:**
```
Valid: admin / admin123
Invalid: admin / wrongpass
Empty: (blank fields)
```

**Expected Results:**
- ✅ Successful login redirects to dashboard
- ✅ Token stored in localStorage
- ✅ User info displayed in navbar
- ✅ Error message for invalid credentials

### 4. Dashboard Test

**Features:**
- Statistics cards display correctly
- Recent orders table shows data
- Quick action buttons work
- Auto-refresh every 30 seconds

**Expected Results:**
- ✅ All stats show correct numbers
- ✅ Charts/data load
- ✅ Navigation links work
- ✅ Admin menu visible for admin users only

### 5. New Order (Web) Test

**Steps:**
1. Navigate to "New Order"
2. Select category filter
3. Click on products
4. Adjust quantities
5. Set table number (optional)
6. Add discount (optional)
7. Submit order

**Expected Results:**
- ✅ Products display in grid
- ✅ Category filter works
- ✅ Cart updates when products added
- ✅ Quantity controls work
- ✅ Totals calculate correctly
- ✅ Order submitted successfully
- ✅ Success message shown
- ✅ Cart clears after submission

### 6. Orders Management Test

**Features:**
- View all orders
- Filter by status
- View order details
- Update order status
- Real-time updates

**Expected Results:**
- ✅ Orders list displays correctly
- ✅ Status filters work
- ✅ Order details modal opens
- ✅ Can change order status
- ✅ Status badges show correct colors
- ✅ List refreshes automatically

### 7. Admin Panel Test

**Prerequisites:** Logged in as admin

**Features:**
- View users list
- Create new user
- Toggle user active/inactive
- Delete user

**Test Cases:**

**Create User:**
```
Username: testuser
Password: test123
Full Name: Test User
Role: cashier
```

**Expected Results:**
- ✅ User list displays
- ✅ New user form validates input
- ✅ User created successfully
- ✅ New user appears in list
- ✅ Can toggle user status
- ✅ Cannot delete/deactivate self

## 📱 Mobile/Responsive Test

**Devices to Test:**
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

**Features:**
- Navigation menu responsive
- Forms usable on small screens
- Tables scroll horizontally if needed
- Buttons appropriately sized for touch
- Text readable without zooming

**Expected Results:**
- ✅ Layout adapts to screen size
- ✅ All features accessible
- ✅ No horizontal scrolling (except tables)
- ✅ Touch targets large enough

## 🔐 Security Tests

### 1. Authentication Test

**Test Cases:**
- Access protected pages without login
- Use invalid/expired token
- Logout functionality

**Expected Results:**
- ✅ Redirects to login if not authenticated
- ✅ Token validation works
- ✅ Logout clears session
- ✅ Cannot access after logout

### 2. Authorization Test

**Test Cases:**
- Non-admin tries to access admin panel
- Cashier tries to create users
- Inactive user tries to login

**Expected Results:**
- ✅ 403 Forbidden for unauthorized access
- ✅ Admin features hidden for non-admins
- ✅ Inactive users cannot login

### 3. Input Validation Test

**Test Cases:**
- SQL injection attempts
- XSS attempts
- Invalid data types
- Empty required fields

**Expected Results:**
- ✅ Input sanitized
- ✅ Validation errors shown
- ✅ No crashes or errors
- ✅ Database integrity maintained

## 🔄 Integration Tests

### 1. Cross-Interface Test

**Scenario:** Create order on web, view on desktop

**Steps:**
1. Start web server
2. Login on web interface
3. Create an order
4. Check desktop app order list
5. Update status from desktop
6. Refresh web interface

**Expected Results:**
- ✅ Order appears on both interfaces
- ✅ Changes sync across interfaces
- ✅ Data consistency maintained

### 2. Multi-User Test

**Scenario:** Multiple users on different devices

**Requirements:**
- 2+ devices
- 2+ user accounts

**Steps:**
1. Login as different users on different devices
2. Create orders simultaneously
3. View orders from different accounts

**Expected Results:**
- ✅ Each user sees appropriate orders
- ✅ Admin sees all orders
- ✅ Non-admins see today's orders only
- ✅ No data conflicts

## 📊 Performance Tests

### 1. Load Test

**Test Data:**
- 100+ products
- 50+ orders
- 10+ users

**Expected Results:**
- ✅ Interface remains responsive
- ✅ Queries execute quickly (< 1s)
- ✅ No memory leaks
- ✅ Smooth scrolling

### 2. Concurrent Users Test

**Scenario:** 5+ users using system simultaneously

**Expected Results:**
- ✅ Server handles multiple requests
- ✅ No conflicts or data corruption
- ✅ Reasonable response times

## 🐛 Edge Cases & Error Handling

### Test Cases:
1. **Empty database** - First run
2. **Large orders** - 20+ items
3. **Maximum discount** - Discount > subtotal
4. **Network interruption** - Disconnect during operation
5. **Invalid port** - Port already in use
6. **Database corruption** - Invalid data

**Expected Results:**
- ✅ Graceful error handling
- ✅ Informative error messages
- ✅ System recovers or fails safely
- ✅ No data loss

## ✅ Test Checklist Summary

### Desktop App
- [ ] Launches successfully
- [ ] Login works
- [ ] POS interface functional
- [ ] Order creation works
- [ ] Themes change correctly
- [ ] Server settings accessible
- [ ] Backup/restore works

### Web Interface
- [ ] Accessible locally
- [ ] Accessible from network
- [ ] Login/authentication works
- [ ] Dashboard displays correctly
- [ ] Can create orders
- [ ] Can view orders
- [ ] Admin panel functional (for admins)
- [ ] Responsive on mobile

### Security
- [ ] Authentication enforced
- [ ] Authorization working
- [ ] Passwords encrypted
- [ ] Tokens validated
- [ ] Input sanitized

### Integration
- [ ] Data syncs between interfaces
- [ ] Multiple users work simultaneously
- [ ] No data conflicts

## 🎯 Network Testing Steps

### Quick Network Test

1. **Find your IP:**
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. **Start server with 0.0.0.0:**
   - Open Server Settings in desktop app
   - Set host to `0.0.0.0`
   - Start server

3. **Test from another device:**
   - Connect device to same Wi-Fi
   - Open browser
   - Go to `http://[YOUR-IP]:8080`
   - Try to login and use features

4. **If it doesn't work:**
   - Check firewall (Windows Defender, etc.)
   - Verify same network
   - Try pinging the server IP
   - Check server logs for errors

## 📝 Test Report Template

```
Date: _______________
Tester: _______________
Version: 2.0.0

Desktop Tests: [ ] Pass [ ] Fail
Web Tests: [ ] Pass [ ] Fail
Network Tests: [ ] Pass [ ] Fail
Mobile Tests: [ ] Pass [ ] Fail
Security Tests: [ ] Pass [ ] Fail

Issues Found:
1. _____________________
2. _____________________
3. _____________________

Notes:
_________________________
_________________________
```

## 🚨 Critical Tests (Must Pass)

These tests MUST pass before considering the system production-ready:

1. ✅ Admin user creation on first run
2. ✅ Login with correct credentials
3. ✅ Create and submit order
4. ✅ View orders
5. ✅ Web server starts successfully
6. ✅ Network accessibility (same network)
7. ✅ JWT authentication works
8. ✅ Password encryption
9. ✅ Admin panel restricted to admins
10. ✅ Backup and restore works

---

**Happy Testing! 🎉**

If you find any issues, document them with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- System information

