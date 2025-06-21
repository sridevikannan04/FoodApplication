from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from .form import FoodItemForm

def user_login(request):
    print("Login attempt started")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting login with email: {email}")
        
        # Check if user exists
        user_exists = User.objects.filter(username=email).exists()
        print(f"User exists in database: {user_exists}")
        
        # Authenticate user
        user = authenticate(username=email, password=password)
        print(f"Authentication result: {user}")
        
        if user:
            print("User authenticated successfully")
            login(request, user)

            # Get the user's role
            user_role = UserRole.objects.filter(user=user).first()
            print(f"User role: {user_role}")
            
            if user_role and user_role.role.role_name == "Seller":
                return redirect('seller')
            elif user_role and user_role.role.role_name == "Buyer":
                return redirect('home')
        else:
            print("Authentication failed")
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')

        print("Full name from form:", full_name)

        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html')

        # Create User
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name
        user.save()
        print("Saved user first_name in DB:", user.first_name)

        # Assign Role
        role = Role.objects.get(role_name=selected_role)
        UserRole.objects.create(user_id=user.id, role_id=role.id)

        return redirect('login')

    return render(request, 'signup.html')



def home(request):
    return render(request, 'home.html')

def seller(request):
    print(1)
    obj=FoodItems.objects.all()
    print(obj) #ORM - (Object Relational Mapping)
    return render(request,'seller.html',{'obj':obj})
    


def addFoodItem(request):
    print(1)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('seller')  # Redirect to seller dashboard after adding
    else:
        form = FoodItemForm()
    
    return render(request, 'add_items.html', {'form': form})


def editFoodItem(request, item):
    food_item =  FoodItems.objects.get(id=item)
    
    if request.method == "POST":
        food_item =  FoodItems.objects.filter(id=item).first()
        food_item.name=request.POST.get('name')
        food_item.description=request.POST.get('description')
        food_item.price=request.POST.get('price')
        food_item.image = request.FILES.get('image')
        food_item.save()
        return redirect('seller')
    return render(request, 'edit_items.html', {'food_item': food_item})


def deleteFoodItem(request, item):
    food_item = FoodItems.objects.get(id=item)
    food_item.delete()
    return redirect('seller')

def menu(request):
    items = FoodItems.objects.all()  # Fetch food items
    return render(request, 'menu.html', {'items': items})


def about(request):
    return render(request,'about.html')

def cart(request):
    cart_items = Cart.objects.filter(user_id=request.user.id)

    total_price =sum(cart_item.quantity *  cart_item.food_item.price for cart_item in cart_items)

    if request.method == "POST":
        print("cart")
        # Simulating order success
        # cart_items.delete()  # Clear the cart after orderxz                             
        return redirect('/checkout')

    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})


def addToCart(request, foodid):
    food_item = FoodItems.objects.get(id=foodid)
    print(request.user.id)
    cart_item = Cart.objects.filter(user=request.user.id, food_item=food_item)
    print(cart_item)
    if len(cart_item)==0:
        cart_item= Cart.objects.create(user=request.user, food_item_id =foodid,quantity=1,price=food_item.price)
    else:
        cart_item = Cart.objects.filter(user=request.user.id, food_item=food_item).first()
        print("cart",cart_item)
        cart_item.quantity+=1 # If item already exists, increase quantity
        cart_item.save()

    return redirect('menu')  # Redirect to the cart page


def checkout(request):
    print(1)
    cart_items = Cart.objects.filter(user=request.user.id)
    total_price =sum(cart_item.quantity * cart_item.food_item.price for cart_item in cart_items)
    print(cart_items)
    print(total_price)
    if request.method == "POST":
        payment_type = request.POST.get('payment_type')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        print(2)
        # Automatically set status based on payment type
        if payment_type == "cash":
            status = "pending"  # Pending for Cash on Delivery
        elif payment_type == "card":
            status = "processing"  
        else:
            status = "Delivered" 
        print(payment_type)
        order = Order.objects.create(
            user=request.user,  # Ensure the user is authenticated
            total_price=total_price,
            status=status,
            payment_type=payment_type,
            address=address,
            phone_no=phone
        )
        print(3)
        # Add ordered items to the order
        for item in cart_items:
            print(4)
            OrderItem.objects.create(order=order, food_item=item.food_item, quantity=item.quantity)

        # Clear the cart
        cart_items.delete()
        print(5)
        return redirect('orderSuccess')  # Redirect to success page

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


def orderSuccess(request):
    return render(request, 'order.html')

def user_logout(request):
    logout(request)
    return redirect('home')