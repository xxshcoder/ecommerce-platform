# Django E-Commerce Application

A full-featured e-commerce platform built with Django, offering a complete online shopping experience with user management, product catalog, shopping cart, order processing, and eSewa payment integration for Nepal market.

## 🚀 Features

- **User Management**: Complete authentication system with registration, login, and user profiles
- **Product Catalog**: Browse and search products with detailed product pages
- **Shopping Cart**: Add, update, and remove items with persistent cart session
- **Order Management**: Place orders and track order history through admin dashboard
- **Payment Integration**: eSewa payment gateway for secure online payments (NPR)
- **Admin Dashboard**: Comprehensive admin interface for managing products, orders, and users
- **Responsive Design**: Mobile-friendly interface with Bootstrap and custom CSS styling
- **Media Management**: Image uploads and storage for products
- **Production Ready**: Nginx configuration included for deployment

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+ or MariaDB 10.3+
- pip
- virtualenv (recommended)

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database

Create a MySQL database and user:
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (MySQL)
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# eSewa Payment Gateway (Test Mode)
ESEWA_MERCHANT_ID=EPAYTEST
ESEWA_SECRET_KEY=8gBm/:&EnhH.1/q
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```

### 8. Collect static files
```bash
python manage.py collectstatic
```

### 9. Run development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the application.

## 📁 Project Structure

```
.
├── dashboard/          # Admin dashboard for managing orders and analytics
├── ecommerce/         # Main project settings and configuration
├── media/             # User-uploaded files (product images)
├── nginx/             # Nginx configuration for production deployment
├── orders/            # Order processing and management
├── payments/          # eSewa payment gateway integration
├── products/          # Product catalog and management
├── shopping_cart/     # Shopping cart functionality with session storage
├── static/            # Static files (CSS, JS, images)
│   └── css/          # Custom CSS styles
├── templates/         # HTML templates
├── users/             # User authentication and profiles
├── .env              # Environment variables (create this file)
├── .gitignore        # Git ignore rules
├── manage.py         # Django management script
└── requirements.txt  # Python dependencies
```

## 🔧 Key Technologies

- **Backend**: Django 5.1
- **Database**: MySQL (required)
- **Payment Gateway**: eSewa (Nepal)
- **Forms**: django-crispy-forms with Bootstrap 4
- **Configuration**: python-decouple for environment management
- **Timezone**: Asia/Kathmandu
- **Currency**: NPR (Nepalese Rupees)

## 💳 Payment Integration

This application integrates eSewa payment gateway for Nepal market:

- **Test Mode**: Uses eSewa UAT environment by default
- **Test Credentials**: Pre-configured in settings
- **Success URL**: `/payments/esewa/success/`
- **Failure URL**: `/payments/esewa/failure/`

For production, update eSewa credentials in `.env`:
```env
ESEWA_MERCHANT_ID=your_production_merchant_id
ESEWA_SECRET_KEY=your_production_secret_key
```

## 🗄️ Database Configuration

This application **requires MySQL**. SQLite is not supported.

**Development Database**:
```env
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=ecommerce_pass123
DB_HOST=localhost
DB_PORT=3306
```

**Production Database**: Update the `.env` file with production credentials.

## 📦 Session & Cart Management

- **Cart Storage**: Session-based shopping cart
- **Session Duration**: 2 weeks (1209600 seconds)
- **Auto-save**: Sessions are saved on every request

## 🚀 Deployment

### Prerequisites for Production
- Set `DEBUG=False` in `.env`
- Configure proper `ALLOWED_HOSTS`
- Use strong `SECRET_KEY`
- Setup production MySQL database
- Configure production eSewa credentials

### Using Nginx + Gunicorn

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Configure Nginx** using the provided configuration in `nginx/` directory

3. **Run Gunicorn**:
   ```bash
   gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```

4. **Update eSewa URLs** in settings for production domain

### Production Environment Variables

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-strong-production-secret-key
DB_NAME=production_db_name
DB_USER=production_db_user
DB_PASSWORD=strong_production_password
DB_HOST=your_db_host
ESEWA_MERCHANT_ID=your_production_merchant_id
ESEWA_SECRET_KEY=your_production_secret_key
```

## 🔐 Security Considerations

- Never commit `.env` file to version control
- Use strong passwords for database and Django secret key
- Enable HTTPS in production
- Configure proper CORS settings
- Regular security updates for dependencies

## 🧪 Testing

Run tests using:
```bash
python manage.py test
```

## 📝 Admin Panel

Access the admin panel at `/admin/` with superuser credentials to:
- Manage products and categories
- View and process orders
- Manage user accounts
- Monitor payment transactions

## 🛒 User Features

- Browse products with search and filtering
- Add items to cart with quantity selection
- Secure checkout process
- Order history and tracking
- User profile management

## 🎨 Customization

- **CSS Styles**: Located in `static/css/`
- **Templates**: Located in `templates/`
- **Currency Symbol**: Configured as 'Rs.' for NPR

## 📚 Dependencies

Key packages (see `requirements.txt` for full list):
- Django
- mysqlclient
- python-decouple
- django-crispy-forms
- Pillow (for image handling)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👤 Author

**xxshcoder**

## 📄 License

[Add your license information here]

## 📧 Support

For issues and questions, please create an issue in the repository.

---

**Note**: This application is configured for the Nepal market with eSewa payment integration and NPR currency. Make sure to test payment integration thoroughly before going live.
