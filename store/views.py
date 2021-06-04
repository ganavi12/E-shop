from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product, Category,Customer,Order
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ProductSerializer,CustomerSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.views import View

# Create your views here.

# print(make_password('1234'))
# print(check_password('1234', 'pbkdf2_sha256$260000$6AGMrwcfqATeV1UEJs3ILl$2jLggwGQaWcaum8+WJ3YkBZgCElvP9I+CiKJGo3BpXU='))

class Index(View):
    def get(self, request):
        # request.session.clear()
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        products = Product.objects.all()
        category_list = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(category=category_id)
            # print("you are" , request.session.get('email')) 
        return render(request, 'store/index.html', {"products": products, "category_list": category_list})
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity -  1
                else:
                    cart[product] = quantity+  1
            else:
                cart[product] =   1     
        else:
            cart = {} 
            cart[product] = 1

        request.session['cart'] = cart

       
        return redirect("index")
            

class Signup(View): 
    def get(self, request):
        return render(request, 'store/signup.html')

    def post(self, request):
        postData = request.POST 
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'store/signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.email_exist():
            error_message = 'Email Address Already Registered..'
      
        return error_message


# def signup(request):
   
#     if request.method == "GET":
#         return render(request, 'store/signup.html')
#     else:
#         request_data = request.POST
#         value = {
#             'first_name': request_data.get('firstname'),
#             'last_name': request_data.get('lasttname'),
#             'phone': request_data.get('phone'),
#             'email': request_data.get('email')
#         }

#         error_message = None

#         customer = Customer(first_name=request_data.get('firstname'),
#                             last_name=request_data.get('lasttname'),
#                             phone=request_data.get('phone'),
#                             email=request_data.get('email'),
#                             password=request_data.get('password'))

#         error_msg = validateCustomer(customer)
#         print(error_msg)
#         if not error_msg:
#             customer.password = make_password(customer.password)
#             customer.save()
#             return redirect("index") 
#         else:
#             data = {
#                 'error': error_message,
#                 'values': value
#             }
#             return render(request, 'store/signup.html', data)
        


# def validateCustomer(customer):
#     error_message = None;
#     if (not customer.first_name):
#         error_message = "First Name Required !!"
#     elif len(customer.first_name) < 4:
#         error_message = 'First Name must be 4 char long or more'
#     elif not customer.last_name:
#         error_message = 'Last Name Required'
#     elif len(customer.last_name) < 4:
#         error_message = 'Last Name must be 4 char long or more'
#     elif not customer.phone:
#         error_message = 'Phone Number required'
#     elif len(customer.phone) < 10:
#         error_message = 'Phone Number must be 10 char Long'
#     elif len(customer.password) < 6:
#         error_message = 'Password must be 6 char long'
#     elif len(customer.email) < 5:
#         error_message = 'Email must be 5 char long'
#     elif customer.email_exist():
#         error_message = 'Email Address Already Registered..'
#     return error_message



class Login(View):
    def get(self,request):
        return render(request, 'store/login.html')
    def post(self,request):
        email = request.POST.get('email') 
        password = request.POST.get('password')
        # customer = Customer.objects.get(email=email)
        customer = Customer.get_customer_by_email(email)
        if customer:
            if check_password(password, customer.password):
                request.session['customer'] = customer.id
                return redirect("index") 
            else:
                error_message = "Email or Password is invalid"
        else:
            error_message = "Email or Password is invalid" 
        return render(request, 'store/login.html', {"error": error_message})
        

class Logout(View):
    def get(self, request):
        request.session.clear()
        return redirect("login")

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in=ids)
        print(products)
        return render(request, 'store/cart.html',{"products":products})

class CheckOut(View):
    def post(self, request):
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        ids = list(cart.keys())
        products = Product.objects.filter(id__in=ids)
        print(address, phone, customer, cart, products)
        for product in products:
            order = Order(product=product,customer=Customer(id=customer),quantity=cart.get(str(product.id)),price=product.price,
                            address=address,phone=phone)

            order.save()
        request.session['cart']  = {} 
        # print(order)

        return redirect("cart")

# class signup(APIView):
#     def get(self, request):
#         return render(request, 'store/signup.html')
#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data) 
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)