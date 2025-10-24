<div align="center">

# 🛍️ Django E-Commerce Platform

### A modern, full-featured e-commerce solution built with Django

![Repo Card](https://github-readme-stats.vercel.app/api/pin/?username=xxshcoder&repo=django-ecommerce&theme=default)


[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

[Features](#-features) • [Installation](#️-installation) • [Configuration](#-configuration) • [Deployment](#-deployment) • [Documentation](#-documentation)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🛒 Shopping Experience
- 🔍 **Smart Product Catalog** - Browse with search & filters
- 🛍️ **Persistent Shopping Cart** - Session-based cart management
- 💳 **Secure Checkout** - Integrated payment processing
- 📦 **Order Tracking** - Real-time order status updates

</td>
<td width="50%">

### 👥 User Management
- 🔐 **Authentication System** - Secure login/registration
- 👤 **User Profiles** - Personalized account management
- 📊 **Order History** - Track all past purchases
- 🎯 **Wishlist Support** - Save favorite items

</td>
</tr>
<tr>
<td width="50%">

### 💰 Payment & Currency
- 💳 **eSewa Integration** - Nepal's #1 payment gateway
- 🇳🇵 **NPR Currency** - Nepalese Rupees (Rs.)
- ✅ **Secure Transactions** - PCI compliant processing
- 🔄 **Auto-verification** - Real-time payment confirmation

</td>
<td width="50%">

### 🎨 Admin Dashboard
- 📈 **Analytics & Reports** - Sales insights
- 📦 **Inventory Management** - Stock control
- 👥 **Customer Management** - User administration
- ⚙️ **Full Control Panel** - Comprehensive admin tools

</td>
</tr>
</table>

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

```
✓ Python 3.8 or higher
✓ MySQL 5.7+ or MariaDB 10.3+
✓ pip (Python package manager)
✓ virtualenv (recommended)
✓ Git
```

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2️⃣ Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup MySQL Database

```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5️⃣ Configure Environment

Create a `.env` file in the project root:

```env
# 🔐 Django Core Settings
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 🗄️ Database Configuration
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# 💳 eSewa Payment Gateway (Test Mode)
ESEWA_MERCHANT_ID=EPAYTEST
ESEWA_SECRET_KEY=8gBm/:&EnhH.1/q
```

### 6️⃣ Initialize Database

```bash
# Run migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 7️⃣ Launch Development Server

```bash
python manage.py runserver
```

🎉 **Success!** Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 Project Architecture

```
ecommerce/
│
├── 📂 dashboard/          # Admin dashboard & analytics
├── 📂 ecommerce/         # Core project settings
├── 📂 media/             # User uploads (product images)
├── 📂 nginx/             # Production server config
├── 📂 orders/            # Order processing engine
├── 📂 payments/          # eSewa payment integration
├── 📂 products/          # Product catalog system
├── 📂 shopping_cart/     # Cart management
├── 📂 static/
│   └── css/             # Custom stylesheets
├── 📂 templates/         # HTML templates
├── 📂 users/             # Authentication & profiles
│
├── 📄 .env              # Environment variables (create this)
├── 📄 .gitignore        # Git ignore rules
├── 📄 manage.py         # Django CLI
└── 📄 requirements.txt  # Python dependencies
```

---

## 🔧 Configuration

### 🗄️ Database Settings

**Development Configuration:**

```env
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=ecommerce_pass123
DB_HOST=localhost
DB_PORT=3306
```

> ⚠️ **Important**: This application requires **MySQL**. SQLite is not supported.

### 💳 Payment Gateway Setup

**Test Environment (Default):**
- Merchant ID: `EPAYTEST`
- Uses eSewa UAT: `https://uat.esewa.com.np`
- Test cards available on eSewa developer portal

**Production Setup:**
```env
ESEWA_MERCHANT_ID=your_production_merchant_id
ESEWA_SECRET_KEY=your_production_secret_key
```

### 🌍 Regional Settings

- **Currency**: NPR (Nepalese Rupees)
- **Currency Symbol**: Rs.
- **Timezone**: Asia/Kathmandu
- **Language**: English (en-us)

### 🛒 Session Management

```python
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True  # Auto-save cart
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Generate strong `SECRET_KEY`
- [ ] Setup production MySQL database
- [ ] Configure production eSewa credentials
- [ ] Enable HTTPS/SSL
- [ ] Setup static file serving
- [ ] Configure media file storage
- [ ] Setup automated backups

### Using Nginx + Gunicorn

**1. Install Gunicorn:**
```bash
pip install gunicorn
```

**2. Configure Nginx:**
Use the provided configuration in the `nginx/` directory.

**3. Run with Gunicorn:**
```bash
gunicorn ecommerce.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
```

**4. Production Environment:**
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=generate-a-new-super-secure-key-for-production
DB_HOST=your_production_db_host
ESEWA_MERCHANT_ID=your_live_merchant_id
ESEWA_SECRET_KEY=your_live_secret_key
```

---

## 🎯 Key Technologies

<div align="center">

| Technology | Purpose | Version |
|:----------:|:-------:|:-------:|
| 🐍 **Django** | Backend Framework | 5.1 |
| 🗄️ **MySQL** | Database | 8.0+ |
| 💳 **eSewa** | Payment Gateway | API v1 |
| 🎨 **Bootstrap** | UI Framework | 4.x |
| 📝 **Crispy Forms** | Form Rendering | Latest |
| 🖼️ **Pillow** | Image Processing | Latest |
| ⚙️ **python-decouple** | Config Management | Latest |

</div>

---

## 📚 Documentation

### 🔐 Admin Panel

Access at `/admin/` with superuser credentials:

- **Products**: Add, edit, delete products & categories
- **Orders**: View, process, update order status
- **Users**: Manage customer accounts
- **Payments**: Monitor transactions
- **Analytics**: View sales reports & insights

### 🛍️ User Features

**Customer Interface:**
- Browse products by category
- Search & filter products
- Add items to cart with quantity
- Secure checkout process
- View order history
- Manage profile settings

### 💻 API Endpoints

```
/                          → Home page
/products/                 → Product catalog
/products/<id>/            → Product detail
/cart/                     → Shopping cart
/cart/add/<id>/           → Add to cart
/checkout/                 → Checkout page
/orders/                   → Order history
/payments/esewa/success/   → Payment success
/payments/esewa/failure/   → Payment failure
/admin/                    → Admin dashboard
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test products
python manage.py test orders

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🔒 Security Best Practices

- ✅ Never commit `.env` file to version control
- ✅ Use strong, unique passwords for database
- ✅ Generate new `SECRET_KEY` for production
- ✅ Enable HTTPS in production
- ✅ Regular security updates
- ✅ Implement rate limiting
- ✅ Setup proper CORS policies
- ✅ Use environment variables for sensitive data

---

## 🎨 Customization

### Styling
- **CSS Files**: `static/css/`
- **Templates**: `templates/`
- **Framework**: Bootstrap 4 + Custom CSS

### Configuration
- **Currency Symbol**: Edit `CURRENCY_SYMBOL` in settings
- **Timezone**: Modify `TIME_ZONE` setting
- **Session Duration**: Adjust `SESSION_COOKIE_AGE`

---

## 🤝 Contributing

Contributions make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**xxshcoder**

---

## 📧 Support & Contact

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Start a discussion
- 📖 **Documentation**: Check the wiki
- 💬 **Questions**: Create an issue with the question tag

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Made with ❤️ for the Nepal e-commerce community**

[⬆ Back to Top](#-django-e-commerce-platform)

</div>
