# from django.shortcuts import render
# from .models import Product, Order, OrderItem

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'ecommerce_app/product_list.html', {'products': products})

# def cart(request):
#     # Handle user cart logic
#     pass

# def checkout(request):
#     # Handle order processing logic
#     pass
from .recommender import recommend_products

def product_list(request):
    # Assuming the user_id is available in the request (e.g., from a session)
    user_id = request.session.get('user_id', 1)  # Default to user 1 for this example

    products = Product.objects.all()
    recommended_product_ids = recommend_products(user_id)
    recommended_products = Product.objects.filter(id__in=recommended_product_ids)

    return render(request, 'ecommerce_app/product_list.html', {
        'products': products,
        'recommended_products': recommended_products
    })