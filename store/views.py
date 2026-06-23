from django.shortcuts import render
from .models import Products

# Homepage view
def homepage(request):
    # Get ALL products from database
    products = Products.objects.all()
    # Send products to home.html template
    return render(request, 'store/home.html', {'products': products})