import os
from pathlib import Path

# ------------------------------
# BASE DIRECTORY
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# ENVIRONMENT VARIABLES
# ------------------------------
DEBUG = os.environ.get("DEBUG", "1") == "1"
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "yourdomain.com"]


# ------------------------------
# DATABASE CONFIGURATION (SQLite)
# ------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ------------------------------
# INSTALLED APPS
# ------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Core apps
    "products",
    "users",
    "shopping_cart",
    "orders",
    "payments",
    "dashboard",

    # Third-party apps
    "crispy_forms",
]

# ------------------------------
# MIDDLEWARE
# ------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

# ------------------------------
# TEMPLATES
# ------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shopping_cart.context_processors.cart_context",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce.wsgi.application"

# ------------------------------
# PASSWORD VALIDATION
# ------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------
# INTERNATIONALIZATION
# ------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------
# STATIC FILES
# ------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# ------------------------------
# MEDIA FILES
# ------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ------------------------------
# DEFAULT PRIMARY KEY FIELD
# ------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------
# CRISPY FORMS
# ------------------------------
CRISPY_TEMPLATE_PACK = "bootstrap4"

# ------------------------------
# AUTHENTICATION SETTINGS
# ------------------------------
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "products:product_list"
LOGOUT_REDIRECT_URL = "products:product_list"

# ------------------------------
# SESSION SETTINGS
# ------------------------------
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True

# ------------------------------
# eSewa Configuration (Sandbox)
# ------------------------------
ESEWA_PAYMENT_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
ESEWA_VERIFICATION_URL = "https://rc-epay.esewa.com.np/api/epay/transaction/status"
ESEWA_MERCHANT_ID = os.environ.get("ESEWA_MERCHANT_ID", "EPAYTEST")
ESEWA_SECRET_KEY = os.environ.get("ESEWA_SECRET_KEY", "8gBm/:&EnhH.1/q")
ESEWA_SUCCESS_URL = "/payments/esewa/success/"
ESEWA_FAILURE_URL = "/payments/esewa/failure/"
