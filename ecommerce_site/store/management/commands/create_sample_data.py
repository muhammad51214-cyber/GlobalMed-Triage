from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample data for the e-commerce store'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest electronic gadgets and devices',
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for all ages',
            },
            {
                'name': 'Books',
                'description': 'Educational and entertainment books',
            },
            {
                'name': 'Home & Garden',
                'description': 'Items for your home and garden',
            },
            {
                'name': 'Sports',
                'description': 'Sports equipment and accessories',
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # Electronics
            {
                'name': 'Smartphone Pro X',
                'description': 'Latest smartphone with advanced camera and long battery life. Features include 128GB storage, 12MP camera, and water resistance.',
                'price': Decimal('799.99'),
                'stock': 25,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
            },
            {
                'name': 'Wireless Headphones',
                'description': 'Premium noise-canceling wireless headphones with 30-hour battery life. Perfect for music lovers and professionals.',
                'price': Decimal('199.99'),
                'stock': 50,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            },
            {
                'name': 'Laptop Ultra',
                'description': '13-inch lightweight laptop with SSD storage and long battery life. Ideal for students and professionals.',
                'price': Decimal('1299.99'),
                'stock': 15,
                'category': 'Electronics',
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400',
            },

            # Clothing
            {
                'name': 'Cotton T-Shirt',
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors. Machine washable and pre-shrunk.',
                'price': Decimal('24.99'),
                'stock': 100,
                'category': 'Clothing',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic blue denim jeans with perfect fit. Made from premium denim fabric with stretch for comfort.',
                'price': Decimal('79.99'),
                'stock': 75,
                'category': 'Clothing',
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
            },
            {
                'name': 'Winter Jacket',
                'description': 'Warm and stylish winter jacket with water-resistant exterior. Perfect for cold weather.',
                'price': Decimal('149.99'),
                'stock': 30,
                'category': 'Clothing',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            },

            # Books
            {
                'name': 'Python Programming Guide',
                'description': 'Comprehensive guide to Python programming for beginners and advanced users. Includes practical examples.',
                'price': Decimal('39.99'),
                'stock': 60,
                'category': 'Books',
                'image_url': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400',
            },
            {
                'name': 'Web Development Handbook',
                'description': 'Complete handbook for modern web development covering HTML, CSS, JavaScript, and frameworks.',
                'price': Decimal('49.99'),
                'stock': 45,
                'category': 'Books',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
            },

            # Home & Garden
            {
                'name': 'Coffee Maker Deluxe',
                'description': 'Premium coffee maker with programmable features and thermal carafe. Makes perfect coffee every time.',
                'price': Decimal('129.99'),
                'stock': 35,
                'category': 'Home & Garden',
                'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400',
            },
            {
                'name': 'Plant Pot Set',
                'description': 'Beautiful ceramic plant pot set with drainage holes. Perfect for indoor plants and herbs.',
                'price': Decimal('34.99'),
                'stock': 80,
                'category': 'Home & Garden',
                'image_url': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400',
            },

            # Sports
            {
                'name': 'Yoga Mat Premium',
                'description': 'Non-slip premium yoga mat with extra cushioning. Perfect for yoga, pilates, and fitness exercises.',
                'price': Decimal('59.99'),
                'stock': 70,
                'category': 'Sports',
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400',
            },
            {
                'name': 'Running Shoes',
                'description': 'Lightweight running shoes with excellent cushioning and breathable material. Suitable for all terrains.',
                'price': Decimal('119.99'),
                'stock': 40,
                'category': 'Sports',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
            },
        ]

        for product_data in products_data:
            category = categories[product_data['category']]
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': slugify(product_data['name']),
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'category': category,
                    'image_url': product_data['image_url'],
                    'available': True,
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data: '
                f'{Category.objects.count()} categories, '
                f'{Product.objects.count()} products'
            )
        )