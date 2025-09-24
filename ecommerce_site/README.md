# 🛒 Django E-Commerce System

A complete, feature-rich e-commerce website built with Django, demonstrating best practices for web development and e-commerce functionality.

## 🌟 Features

### Core E-commerce Features
- **Product Catalog**: Browse products by category with detailed product pages
- **Shopping Cart**: Add/remove items, adjust quantities, view totals
- **User Authentication**: Register, login, logout with secure session management
- **Order Processing**: Complete checkout flow with order tracking
- **Inventory Management**: Real-time stock tracking and validation
- **Admin Interface**: Full Django admin for managing products, orders, and users

### Technical Features
- **Responsive Design**: Mobile-friendly Bootstrap-based UI
- **Database Models**: Proper relationships and constraints
- **Security**: CSRF protection, password validation, secure authentication
- **Session Management**: Support for both authenticated and guest users
- **Template System**: Clean, maintainable template structure
- **Static Files**: Organized CSS, JavaScript, and image handling

## 📁 Project Structure

```
ecommerce_site/
├── ecommerce_site/          # Django project settings
│   ├── settings.py          # Project configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── store/                   # Main e-commerce app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL routing
│   ├── admin.py            # Admin interface configuration
│   ├── templates/          # HTML templates
│   │   ├── store/          # Main store templates
│   │   └── registration/   # Auth templates
│   ├── migrations/         # Database migrations
│   └── management/         # Custom management commands
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── media/                   # User-uploaded files
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+
- Pillow (for image handling)

### Installation

1. **Navigate to the project directory:**
```bash
cd ecommerce_site
```

2. **Install required packages:**
```bash
pip install django pillow
```

3. **Run database migrations:**
```bash
python manage.py migrate
```

4. **Create sample data:**
```bash
python manage.py create_sample_data
```

5. **Create an admin user:**
```bash
python manage.py createsuperuser
```

6. **Start the development server:**
```bash
python manage.py runserver
```

7. **Open your browser and visit:**
- **Main site:** http://localhost:8000/
- **Admin interface:** http://localhost:8000/admin/

## 📊 Database Models

### Core Models

#### Product
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Order
```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### CartItem
```python
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
```

## 🎯 Key Features Explained

### Shopping Cart System
- **Guest Users**: Cart items stored by session ID
- **Authenticated Users**: Cart items stored by user ID
- **Cart Migration**: When guests register, their cart items are automatically migrated to their user account

### Order Processing
1. User adds items to cart
2. Proceeds to checkout (login required)
3. Enters shipping information
4. Order is created with unique order ID
5. Inventory is automatically reduced
6. Cart is cleared
7. Order confirmation is displayed

### Security Features
- CSRF protection on all forms
- Password validation for user registration
- Login required for checkout and order viewing
- Session-based authentication
- SQL injection protection through Django ORM

## 🎨 UI/UX Features

### Responsive Design
- Mobile-first Bootstrap framework
- Responsive navigation with collapsible menu
- Mobile-optimized product cards and forms
- Touch-friendly interface elements

### User Experience
- Clean, modern design
- Intuitive navigation
- Real-time cart updates
- Success/error message system
- Loading states and feedback

## 🔧 Customization

### Adding New Products
1. Access Django admin at `/admin/`
2. Go to "Products" section
3. Click "Add Product"
4. Fill in product details
5. Save and view on the main site

### Modifying Templates
Templates are located in `store/templates/store/`:
- `base.html` - Main layout template
- `product/list.html` - Product listing page
- `product/detail.html` - Product detail page
- `cart/detail.html` - Shopping cart page
- `checkout.html` - Checkout form
- `order/detail.html` - Order confirmation

### Styling
CSS files are in `static/css/`:
- `style.css` - Custom styles
- Bootstrap 5 CDN for responsive framework

## 📈 Performance Considerations

### Database Optimization
- Indexes on frequently queried fields
- Efficient model relationships
- Optimized queries with select_related/prefetch_related

### Static Files
- Organized static file structure
- Placeholder images for missing product images
- Optimized CSS and JavaScript

## 🔒 Security Best Practices

- CSRF tokens on all forms
- Password strength validation
- Secure session handling
- Input validation and sanitization
- Protection against common web vulnerabilities

## 🚀 Deployment Ready

The application is structured for easy deployment:
- Environment-specific settings
- Static file configuration
- Database migrations
- WSGI configuration
- Debug mode controls

## 📚 Learning Objectives

This project demonstrates:

1. **Django Fundamentals**
   - Models, Views, Templates (MVT pattern)
   - URL routing and navigation
   - Django ORM and database relationships

2. **E-commerce Concepts**
   - Product catalog management
   - Shopping cart functionality
   - Order processing workflow
   - Inventory management

3. **Web Development Best Practices**
   - Responsive design principles
   - User authentication and authorization
   - Security considerations
   - Template inheritance and reuse

4. **Database Design**
   - Normalized database structure
   - Proper foreign key relationships
   - Data integrity constraints

## 🎓 Next Steps for Enhancement

1. **Payment Integration**: Add Stripe or PayPal integration
2. **Email System**: Send order confirmations and notifications
3. **Search & Filtering**: Advanced product search and filtering
4. **Reviews & Ratings**: Product review and rating system
5. **Wishlist**: User wishlist functionality
6. **Coupons & Discounts**: Promotional code system
7. **API Development**: REST API for mobile app integration
8. **Analytics**: Order and sales analytics dashboard

## 🤝 Contributing

This is a learning project demonstrating Django e-commerce development. Feel free to:
- Study the code structure and patterns
- Experiment with modifications
- Use as a foundation for your own projects
- Provide feedback and suggestions

## 📄 License

This project is created for educational purposes and demonstration of Django e-commerce development.