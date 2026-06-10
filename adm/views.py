from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
from .form import FoodItemForm

def user_login(request):
    print(1)
    if request.method == 'POST':
        print(2)
        email= request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        # Authenticate user
        user = authenticate(username=email, password=password)
        print(user)
        if user:
            print(4)
            login(request, user)

            # Get the user's role
            user_role = UserRole.objects.filter(user=user).first()
            print(user_role)
            if user_role and user_role.role.role_name == "Seller":
                return redirect('seller')  # Redirect to seller page
            elif user_role and user_role.role.role_name == "Buyer":
                return redirect('home')  # Redirect to buyer page
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def signup(request):
    print(1)
    if request.method == 'POST':
        print(2)
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')
        print("Full name from form:", full_name)
        print("Email:", email)
        print("Selected role:", selected_role)
        print(3)
        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html')
        print(4)
        # Clean the full_name (strip whitespace)
        full_name = full_name.strip() if full_name else ''
        
        # Create User with first_name directly
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password,
            first_name=full_name  # Set first_name during creation
        )
        print("Created user with first_name:", user.first_name)
        
        # Verify it was saved
        user.refresh_from_db()
        print("Verified first_name from DB after refresh:", user.first_name)
        print("user", user)

        # Assign Role
        role = Role.objects.get(role_name=selected_role)
        print("role",role)
        UserRole.objects.create(user_id=user.id, role_id=role.id)
        print(5)

        return redirect('login')  # Redirect to login page after signup

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


def remove_cart_item(request, cart_item_id):
    if request.method == "POST":
        Cart.objects.filter(id=cart_item_id, user=request.user).delete()
    return redirect("cart")


def adjust_cart_quantity(request, cart_item_id):
    if request.method != "POST":
        return redirect("cart")
    cart_item = Cart.objects.filter(id=cart_item_id, user=request.user).first()
    if not cart_item:
        return redirect("cart")
    action = request.POST.get("action")
    if action == "increment":
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrement":
        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
    return redirect("cart")


def addToCart(request, foodid):
    food_item = FoodItems.objects.get(id=foodid)
    
    # Check if the item already exists in the cart
    cart_item = Cart.objects.filter(user=request.user, food_item=food_item).first()
    
    if cart_item:
        # If item already exists, increase quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If item doesn't exist, create a new cart item
        cart_item = Cart.objects.create(
            user=request.user, 
            food_item_id=foodid,
            quantity=1,
            price=food_item.price
        )

    return redirect(f"{reverse('menu')}?cart_added=1")


def checkout(request):

    print(1)
    cart_items = Cart.objects.filter(user=request.user.id)
    total_price =sum(cart_item.quantity * cart_item.food_item.price for cart_item in cart_items)
    print(cart_items)
    print(total_price)
    if request.method == "POST":
        print(2)
        payment_type = request.POST.get('payment_type')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
         # Automatically set status based on payment type
        if payment_type == "cash":
            status = "pending"
        elif payment_type == "card":
            status = "processing"  
        else:
            status = "Delivered"
            
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status=status,
            payment_type=payment_type,
            address=address,        # Add this line
            phone_no=phone          # Add this line
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