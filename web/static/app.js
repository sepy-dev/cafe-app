// Cafe Management System - Main JavaScript

// API Configuration
const API_BASE = '';
const TOKEN_KEY = 'cafe_auth_token';
const USER_KEY = 'cafe_user';

// Authentication Manager
class AuthManager {
    static getToken() {
        return localStorage.getItem(TOKEN_KEY);
    }
    
    static setToken(token) {
        localStorage.setItem(TOKEN_KEY, token);
    }
    
    static removeToken() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
    }
    
    static getUser() {
        const userJson = localStorage.getItem(USER_KEY);
        return userJson ? JSON.parse(userJson) : null;
    }
    
    static setUser(user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user));
    }
    
    static isAuthenticated() {
        return !!this.getToken();
    }
    
    static isAdmin() {
        const user = this.getUser();
        return user && user.role === 'admin';
    }
    
    static async login(username, password) {
        try {
            const response = await fetch(`${API_BASE}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }
            
            const data = await response.json();
            this.setToken(data.access_token);
            this.setUser(data.user);
            return data;
        } catch (error) {
            throw error;
        }
    }
    
    static logout() {
        this.removeToken();
        window.location.href = '/login';
    }
    
    static async getMe() {
        try {
            const response = await API.get('/api/auth/me');
            this.setUser(response);
            return response;
        } catch (error) {
            this.logout();
            throw error;
        }
    }
}

// API Client
class API {
    static async request(url, options = {}) {
        const token = AuthManager.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers,
        };
        
        try {
            const response = await fetch(`${API_BASE}${url}`, {
                ...options,
                headers,
            });
            
            if (response.status === 401) {
                AuthManager.logout();
                throw new Error('Session expired');
            }
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Request failed');
            }
            
            return await response.json();
        } catch (error) {
            throw error;
        }
    }
    
    static async get(url) {
        return this.request(url, { method: 'GET' });
    }
    
    static async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }
    
    static async patch(url, data) {
        return this.request(url, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }
    
    static async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}

// UI Utilities
class UI {
    static showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        const container = document.querySelector('.container') || document.body;
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => alertDiv.remove(), 5000);
    }
    
    static showError(message) {
        this.showAlert(message, 'danger');
    }
    
    static showSuccess(message) {
        this.showAlert(message, 'success');
    }
    
    static showLoading(element) {
        const spinner = document.createElement('div');
        spinner.className = 'spinner';
        spinner.id = 'loading-spinner';
        element.appendChild(spinner);
    }
    
    static hideLoading() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) spinner.remove();
    }
    
    static formatCurrency(amount) {
        return new Intl.NumberFormat('fa-IR', {
            maximumFractionDigits: 0,
        }).format(amount) + ' تومان';
    }
    
    static formatDate(dateString) {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('fa-IR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        }).format(date);
    }
    
    static getStatusBadgeClass(status) {
        const statusMap = {
            'open': 'badge-warning',
            'closed': 'badge-success',
            'cancelled': 'badge-danger',
        };
        return statusMap[status] || 'badge-info';
    }
    
    static getStatusText(status) {
        const statusMap = {
            'open': 'باز',
            'closed': 'بسته',
            'cancelled': 'لغو شده',
        };
        return statusMap[status] || status;
    }
}

// Modal Manager
class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
    }
    
    show() {
        if (this.modal) {
            this.modal.classList.add('show');
        }
    }
    
    hide() {
        if (this.modal) {
            this.modal.classList.remove('show');
        }
    }
}

// Products Manager
class ProductsManager {
    constructor() {
        this.products = [];
        this.categories = [];
    }
    
    async loadProducts() {
        try {
            this.products = await API.get('/api/products');
            this.extractCategories();
            return this.products;
        } catch (error) {
            UI.showError('خطا در بارگذاری محصولات: ' + error.message);
            throw error;
        }
    }
    
    extractCategories() {
        this.categories = [...new Set(this.products.map(p => p.category))];
    }
    
    getProductsByCategory(category) {
        if (!category || category === 'all') {
            return this.products;
        }
        return this.products.filter(p => p.category === category);
    }
    
    getProductById(id) {
        return this.products.find(p => p.id === id);
    }
}

// Orders Manager
class OrdersManager {
    constructor() {
        this.orders = [];
    }
    
    async loadOrders(statusFilter = null) {
        try {
            let url = '/api/orders?limit=100';
            if (statusFilter) {
                url += `&status_filter=${statusFilter}`;
            }
            this.orders = await API.get(url);
            return this.orders;
        } catch (error) {
            UI.showError('خطا در بارگذاری سفارشات: ' + error.message);
            throw error;
        }
    }
    
    async createOrder(orderData) {
        try {
            const order = await API.post('/api/orders', orderData);
            UI.showSuccess('سفارش با موفقیت ثبت شد');
            return order;
        } catch (error) {
            UI.showError('خطا در ثبت سفارش: ' + error.message);
            throw error;
        }
    }
    
    async updateOrderStatus(orderId, status) {
        try {
            await API.patch(`/api/orders/${orderId}/status`, { status });
            UI.showSuccess('وضعیت سفارش به‌روزرسانی شد');
        } catch (error) {
            UI.showError('خطا در به‌روزرسانی سفارش: ' + error.message);
            throw error;
        }
    }
}

// Users Manager (Admin)
class UsersManager {
    constructor() {
        this.users = [];
    }
    
    async loadUsers() {
        try {
            this.users = await API.get('/api/admin/users');
            return this.users;
        } catch (error) {
            UI.showError('خطا در بارگذاری کاربران: ' + error.message);
            throw error;
        }
    }
    
    async createUser(userData) {
        try {
            const user = await API.post('/api/admin/users', userData);
            UI.showSuccess('کاربر با موفقیت ایجاد شد');
            return user;
        } catch (error) {
            UI.showError('خطا در ایجاد کاربر: ' + error.message);
            throw error;
        }
    }
    
    async toggleUserActive(userId) {
        try {
            await API.patch(`/api/admin/users/${userId}/toggle-active`);
            UI.showSuccess('وضعیت کاربر تغییر یافت');
        } catch (error) {
            UI.showError('خطا در تغییر وضعیت کاربر: ' + error.message);
            throw error;
        }
    }
    
    async deleteUser(userId) {
        try {
            await API.delete(`/api/admin/users/${userId}`);
            UI.showSuccess('کاربر حذف شد');
        } catch (error) {
            UI.showError('خطا در حذف کاربر: ' + error.message);
            throw error;
        }
    }
}

// Dashboard Manager
class DashboardManager {
    async loadStats() {
        try {
            return await API.get('/api/dashboard/stats');
        } catch (error) {
            UI.showError('خطا در بارگذاری آمار: ' + error.message);
            throw error;
        }
    }
    
    renderStats(stats) {
        const statsContainer = document.getElementById('stats-container');
        if (!statsContainer) return;
        
        statsContainer.innerHTML = `
            <div class="stat-card">
                <div class="stat-icon orders">📋</div>
                <div class="stat-content">
                    <h3>${stats.total_orders_today}</h3>
                    <p>سفارشات امروز</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon revenue">💰</div>
                <div class="stat-content">
                    <h3>${UI.formatCurrency(stats.total_revenue_today)}</h3>
                    <p>فروش امروز</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon pending">⏳</div>
                <div class="stat-content">
                    <h3>${stats.pending_orders}</h3>
                    <p>سفارشات در انتظار</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon products">☕</div>
                <div class="stat-content">
                    <h3>${stats.total_products}</h3>
                    <p>محصولات</p>
                </div>
            </div>
            ${stats.total_users > 0 ? `
            <div class="stat-card">
                <div class="stat-icon users">👥</div>
                <div class="stat-content">
                    <h3>${stats.total_users}</h3>
                    <p>کاربران</p>
                </div>
            </div>
            ` : ''}
        `;
    }
}

// Initialize authentication check on protected pages
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on a protected page (not login or index)
    const currentPath = window.location.pathname;
    const publicPaths = ['/', '/login'];
    
    if (!publicPaths.includes(currentPath) && !AuthManager.isAuthenticated()) {
        window.location.href = '/login';
    }
    
    // Update user info in navbar if present
    const userInfo = document.getElementById('user-info');
    if (userInfo && AuthManager.isAuthenticated()) {
        const user = AuthManager.getUser();
        if (user) {
            userInfo.textContent = user.full_name;
        }
    }
    
    // Logout button handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('آیا می‌خواهید از سیستم خارج شوید؟')) {
                AuthManager.logout();
            }
        });
    }
});

// Export for global use
window.AuthManager = AuthManager;
window.API = API;
window.UI = UI;
window.Modal = Modal;
window.ProductsManager = ProductsManager;
window.OrdersManager = OrdersManager;
window.UsersManager = UsersManager;
window.DashboardManager = DashboardManager;

