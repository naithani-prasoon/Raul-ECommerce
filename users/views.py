from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm
from .forms import CreateUserForm
from .forms import UserRegisterForm
from carts.models import Cart, CartItem
from django.contrib.auth import get_user






def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = CreateUserForm()
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    User = get_user(request)
    UserOrders = CartItem.objects.filter(user=User)
    context = {"userorders":UserOrders}
    return render(request, 'users/profile.html',context)



def products(request):
    return render(request, 'product_grid/index.html.html')


# def search(request):
#     try:
#         q= request.GET.get('q')
#     except:
#         q= None
#     if q:
#         products= products.objects.filter(title__icontains=q)
#         context = {'query':q , 'products':products}
#         template = 'Raul/results.html'
#     else:
#         context = {}
#         template ='Raul/product.html'
#     return render(request, template, context)

# Create your views here.
