import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, F


# Create and run your queries within functions

def get_profiles(search_string=None):
    if search_string is None:
        return ""

    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(
        phone_number__icontains=search_string)

    profiles = Profile.objects.annotate(num_of_orders=Count('orders')).filter(query).order_by('full_name')

    if not profiles:
        return ""

    result = []

    for profile in profiles:
        result.append(
            f"Profile: {profile.full_name}, email: {profile.email}, phone number: {profile.phone_number}, orders: {profile.num_of_orders}")

    return '\n'.join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    result = []
    for profile in profiles:
        result.append(f"Profile: {profile.full_name}, orders: {profile.orders_count}")

    return '\n'.join(result) if result else ''


def get_last_sold_products():
    latest_order = Order.objects.order_by('-creation_date').first()

    if not latest_order or not latest_order.products:
        return ""

    latest_products = ', '.join([product.name for product in latest_order.products.order_by('name')])

    return f"Last sold products: {latest_products}"


def get_top_products():
    top_products = Product.objects.annotate(num_orders=Count('orders')).filter(num_orders__gt=0).order_by('-num_orders',
                                                                                                          'name')[:5]

    if top_products:
        result = []
        result.append("Top products:")

        for product in top_products:
            result.append(f"{product.name}, sold {product.num_orders} times")

        return '\n'.join(result)
    return ""


def apply_discounts():
    new_price = F('total_price') * 0.9

    searched_orders = Order.objects.annotate(num_products=Count('products')).filter(is_completed=False,
                                                                                    num_products__gt=2)

    if not searched_orders:
        num_updated_orders = 0

    else:
        num_updated_orders = searched_orders.update(total_price=new_price)

    return f"Discount applied to {num_updated_orders} orders."


def complete_order():
    searched_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if searched_order is None:
        return ""

    searched_order.is_completed = True
    searched_order.save()

    for product in searched_order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False
        product.save()

    return "Order has been completed!"

