from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.utils.text import slugify
from django.http import JsonResponse
import json
import os
import shutil
from .models import Club, Product, Order, OrderItem
from django.core.files.base import ContentFile
import json
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import redirect
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
import stripe
import pytz
from datetime import datetime

from django.template import loader
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import random

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def privacy(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user
    username = request.user.username
    context = {"cartItems":cartItems,"username":username}
    
    return render(request, "store/privacy.html",context)
def terms_conditions(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user
    username = request.user.username
        
    context = {"cartItems":cartItems,"username":username}
    
    return render(request, "store/terms.html",context)

def home(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user
    username = request.user.username
        

    if request.method == 'POST':
        if "contact_us" in request.POST:
            print("Contact form submitted!")
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            if name!="" and email != "" and message!="":
                send_mail(
                    'Subject: New Contact Form Submission',
                    f'Name: {name}\nEmail: {email}\nMessage: {message}',
                    'bjerseys01@gmail.com',  # Sender's email
                    ["oussama.bakadir@institutoptique.fr","bakadir.oussama@gmail.com"],  # List of recipient emails
                    fail_silently=False,
                )

                return HttpResponse('Thank you for your message! We will get back to you soon.')
        if "privacy" in request.POST:
            context = {"cartItems":cartItems,"username":username,"privacy":True}
    
            return render(request, "store/policies.html",context)
        if "terms_conditions" in request.POST:
            context = {"cartItems":cartItems,"username":username}
    
            return render(request, "store/policies.html",context)
        
    
    categories = ['Premier League','La Liga','Serie A','Bundesliga','Ligue 1',"Worldwide Jerseys"]
    clubs = [['Manchester City','Manchester United','Arsenal FC',"Chelsea FC","Tottenham Hotspur"],
             ["Real Madrid",'FC Barcelona',"Atlético Madrid"],
             ['AC Milan', 'Juventus FC','Inter Milan'],
             ["Bayern München","Borussia Dortmund"],
             ["Paris Saint Germain","Olympique Marseille"],
             ["Ajax Amsterdam","Inter Miami","Al Nassr FC"]
             ]
    data_clubs=zip(categories,clubs)
    teams = ["Brazil","Argentina","Mexico","Japan","South Korea","Spain","England","Portugal","France","Belgium","Morocco","Senegal"]

    club_names=["Argentina","Manchester United","Inter Miami","FC Barcelona","Real Madrid",
                "Al Nassr FC","Al Hilal SFC","AC Milan","Juventus FC","Bayern München","Mexico","Japan"]
    seasons = ["2022","2023-24","2023","2023-24","2023-24","2023-24","2023-24","2023-24","2023-24","2023-24","2022","2022"]
    types = ["home","home","home","home","away","home","home","home","home","third","home","home"]
    data_popular = zip(club_names,seasons,types)
    popular_products = []
    for club_name,season,type in data_popular:
        popular_products.append(Product.objects.get(club__name=club_name, season=season, type=type))

    special_products=[]
    club_names=["Argentina","Japan","FC Barcelona","AC Milan","FC Barcelona","Real Madrid","Italy","Mexico"]
    seasons = ["2022","2023","2022-23","2022-23","2023-24","2023-24","2023","2023"]
    types=["Special Edition","Special Edition","Special Edition","Special Edition","Special Edition 3","Special Edition","Special Edition","Special Edition"]
    data_special = zip(club_names,seasons,types)
    for club_name,season,type in data_special:
        special_products.append(Product.objects.get(club__name=club_name, season=season, type=type))

    context = {"cartItems":cartItems,"username":username,"categories":categories,"data_clubs":data_clubs,"teams":teams,
               "popular_products":popular_products,"special_products":special_products}


    return render(request, "store/home.html",context)
def basket(request):
   
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user
    username = request.user.username

    context = {'items':items, 'order':order, 'cartItems':cartItems,"username":username}
    return render(request, 'store/basket.html', context)

@csrf_exempt
def create_checkout_session(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    order = data['order']
    items = data['items']
    if cartItems == 0:
        username = request.user.username
        context = {'items':items, 'order':order, 'cartItems':cartItems,"username":username}
        return render(request, 'store/basket.html', context)
    
    product_images = []
    for item in items:
        product_images.append(item.product.imageURL())
    
    form_data=json.loads(request.body)['formData']
 

    firstname = form_data["firstname"]
    lastname = form_data["lastname"]
    email = form_data["email"]
    phone_number = form_data["phone_number"]
    country = form_data["country"]
    city = form_data["city"]
    zipcode = form_data["zipcode"]
    address = form_data["address"]
    promocode = form_data["promocode"]
    

  
    order.firstname=firstname
    order.lastname=lastname
    order.email=email
    order.phone_number=phone_number
    order.country=country
    order.city=city
    order.zipcode=zipcode
    order.address=address

    order.save()
    

    request_data = json.loads(request.body)
    if promocode in ["BA9A","BENA072"]:
        total_price_cents = int(float(order.get_cart_total)*0.85 * 100)
    else:
        total_price_cents = int(order.get_cart_total * 100)
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': total_price_cents,
                'product_data': {
                    'name': 'B-Jerseys',
                    
                },
            },
            'quantity': 1,
            
        }],
        
        mode='payment',

        success_url=request.build_absolute_uri(reverse('store:thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('store:basket')),
    )
    try:
        data = {
            'id': checkout_session.id,
            'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
        }
        return JsonResponse(data)
    except Exception as e:
        # Handle exceptions gracefully
        return JsonResponse({'error': str(e)})
def cancel(request):
    return render(request, 'cancel.html')
def thanks(request):
    user=request.user
    username = request.user.username
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    paris_timezone = pytz.timezone('Europe/Paris')
    paris_time = datetime.now(paris_timezone)



    email = order.email
    if email != "":
        order.date_ordered = str(datetime.now(paris_timezone))[:16]
        order.complete = True
        order.save()

        items = data['items']
    
    
    
        

        email_template = 'store/confirmation_mail.html'

        email_content = render_to_string(email_template, {
            'username': username,
            'items': items,
            'order': order,
        })

        email_subject = 'Order Confirmation'
        from_email = 'bjerseys01@gmail.com'
        to_email = email

        msg = EmailMessage(email_subject,email_content,from_email,[to_email])
        msg.content_subtype = 'html'  # Indicate that the email content is HTML
        msg_me = EmailMessage(email_subject,email_content,from_email,['bakadir.oussama@gmail.com',"oussama.bakadir@institutoptique.fr"])
        msg_me.content_subtype = 'html'  # Indicate that the email content is HTML
        try:
            msg.send()
            msg_me.send()
            # Rest of your code after sending the email
        except Exception as e:
            print("Email sending error:", e)

        OrderItem.objects.all().delete()
    else:
        print("grtugfyurgf")
    
    return render(request, 'store/thanks.html')

def authentication(request):

    if request.method == "POST":
        if "login" in request.POST:
            email_username = request.POST["email_username"]
            password = request.POST["password"]
            try:
                try:
                    user = User.objects.get(email=email_username)
                    email = user.email
                    username = user.username
                except:
                    user = User.objects.get(username=email_username)
                    email = user.email
                    username = user.username
            except User.DoesNotExist:
                username = None
            user = authenticate(request, username=username, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('store:home')
            else:
                context = {'message': 'Invalid credentials'}
                return render(request, 'store/authentication.html', context)
            
        if "signup" in request.POST:
            username_signup = request.POST["username_signup"]
            email_signup = request.POST["email_signup"]
            password_signup = request.POST["password_signup"]
            if User.objects.filter(username=username_signup).exists(): 
                context = {'message': "Username already exists. Please use a different username.","signup":True}
                return render(request, 'store/authentication.html', context)
            
            elif User.objects.filter(email=email_signup).exists(): 
                context = {'message': "Email already exists. Please use a different email.","signup":True}
                return render(request, 'store/authentication.html', context)
            else:
                user = User.objects.create_user(username=username_signup, email=email_signup, password=password_signup)
                
            #user = User.objects.create_user(username=username_signup, email=email_signup, password=password_signup)
            
            subject = 'Welcome to B-Jerseys!'
            message = 'Dear ' + str(username_signup) +', \n\nThank you for signing up with us. We are excited to have you on board!'
            send_mail(subject, message, 'bjersey01@gmail.com', [email_signup])
            send_mail("bjerseys new user ",
                        '\nusername: ' + str(username_signup) + '\nemail: '+ str(email_signup)+ '\npassword: '+ str(password_signup), 
                        'bjersey01@gmail.com', ['bakadir.oussama@gmail.com','oussama.bakadir@institutoptique.fr'])
            user = authenticate(request, username=username_signup, email=email_signup, password=password_signup)
            login(request, user)
            return redirect('store:home')
    return render(request, 'store/authentication.html')

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Construct the password reset link (change 'reset_link' to your actual reset URL)
            reset_link = f"https://bjerseys.up.railway.app/reset_password/{uid}/{token}/"

            # Send the password reset email
            subject = 'Reset your password'
            message = f'Click the link to reset your password: {reset_link}'
            send_mail(subject, message, 'bjersey01@gmail.com', [email])
            
            # Redirect or display a success message
            return render(request,'store/authentication.html',{'email_sent': True,'password_reset':True})
        else:
            # Handle case where email is not found in the database
            return render(request,'store/authentication.html', {'message': 'Email not found','password_reset':True})

    return render(request, 'store/authentication.html',{'password_reset':True})
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        # Password reset token is valid, handle password reset logic here
        # You might display a form for users to input a new password

        if request.method == 'POST':
            # Retrieve the new password from the form
            new_password = request.POST.get('new_password')

            # Set the new password for the user
            user.set_password(new_password)
            user.save()

            # Redirect to password reset success page or login page
            authenticated_user = authenticate(request, username=user.username, password=new_password)
            if authenticated_user:
                # If successfully authenticated, log the user in
                login(request, authenticated_user)
            return redirect('store:home') # Replace 'password_reset_done' with your URL name for success

        # Render a password reset form for the user to input a new password
        return render(request, 'store/authentication.html',{'reset_password':True})  # Replace 'password_reset_form.html' with your form template

    # If the token is invalid or user doesn't exist, show an error or redirect to an error page
    return render(request, 'store/authentication.html',{'reset_password':True})

def logout_request(request):
	logout(request)
	return redirect("store:home")
def cartData(request):

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cartItems = 0
        order = None
        items = None
    return {'cartItems':cartItems ,'order':order, 'items':items}
def product_detail(request, club_name, season, type):
    if request.user.is_authenticated:
        user = request.user
        username = request.user.username
        
    else:
        username = None

    products = Product.objects.all()
    for prod in products:
        if slugify(prod.club.name) == club_name:
            produit=prod
            break
    product = Product.objects.get(club__name=produit.club.name, season=season, type=type)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("store:authentication")
        if "addcommande" in request.POST:
            size = request.POST.get("selected_size")
            quantity = int(request.POST.get("quantity"))
            if size!="":
                existing_order, created = Order.objects.get_or_create(user=user,complete=False)
                try:
                    order_item = OrderItem.objects.get(order=existing_order, product=product, size=size)
                    # If the item already exists, update its quantity
                    order_item.quantity = order_item.quantity + quantity  # Increment the quantity
                    order_item.save()
                except OrderItem.DoesNotExist:
                    # If it doesn't exist, create a new order item
                    order_item = OrderItem.objects.create(
                        order=existing_order,
                        product=product,
                        size=size,
                        quantity=quantity
                    )
            #return HttpResponseRedirect("httP://localhost:8000/B-Jerseys/"+slugify(product.club.name)+"/"+product.season+"/"+product.type)
            return redirect(reverse('store:product_detail', kwargs={'club_name': club_name, 'season': season, 'type': type}))
	    
	    
	    
        if "delete" in request.POST:
            item = request.POST.get("item")
            size = request.POST.get("size")
            quantity = int(request.POST.get("quantity"))

            existing_order, created = Order.objects.get_or_create(user=user,complete=False)
            item_to_delete = existing_order.orderitem_set.get(
                        Q(product=product) & Q(size=size) & Q(quantity=quantity)
                    )
            item_to_delete.delete()
            #return HttpResponseRedirect("httP://localhost:8000/B-Jerseys/"+slugify(product.club.name)+"/"+product.season+"/"+product.type)
            return redirect("https://bjerseys.up.railway.app/"+slugify(product.club.name)+"/"+product.season+"/"+product.type)
	
        
    else:
        if request.user.is_authenticated:
            data = cartData(request)

            cartItems = data['cartItems']
            order = data['order']
            items = data['items']
            user = request.user
            username = request.user.username
            
        else:
            cartItems = 0
            order = None
            items = None
            username = None
    try:
        related_items = order.orderitem_set.filter(product__club__name=product.club.name,product__season=product.season,product__type=product.type)
    except:
        related_items = []
    return render(request, 'store/product_detail.html', {'product': product,"username":username,'club_slug':slugify(prod.club.name),'cartItems':cartItems,"related_items":related_items})
def categories(request,categorie):              
    if request.user.is_authenticated:
        data = cartData(request)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        user = request.user
        username = request.user.username
        
    else:
        cartItems = 0
        order = None
        items = None
        username = None

    clubs = Club.objects.filter(league=categorie)

    if categorie == "World Cup":
        products = Product.objects.filter(club__league=categorie,season="2022")
    elif categorie == "Lionel Messi":
        products = Product.objects.filter(
        Q(club__name="FC Barcelona", season__in=["2008-09","2011-12","2014-15", "2018-19"]) |  # Fcbarcelone from 2005 to 2021
        Q(club__name="Inter Miami", season="2023") |  # Inter Miami in 2023
        Q(club__name="Argentina", season__in=["2014","2022"]) |
        Q(club__name="Paris Saint Germain", season__in=["2021-22", "2022-23"])  # PSG in 2021-2022 and 2022-2023
        )
        seasons = list(set(product.season for product in products))
        sorted_seasons = sorted(seasons, key=lambda x: tuple(map(int, x.split('-'))), reverse=True)
        prods=[]
        i=0
        for season in sorted_seasons:
            prods.append([])
            for prod in products:
                if  prod.season == season:
                    prods[i].append(prod)
            i=i+1

        data = zip(sorted_seasons,prods)
        context = {'cartItems':cartItems ,'player': 'Lionel Messi',"data":data,"username":username}
        return render(request, 'store/player.html', context)
    elif categorie == "Cristiano Ronaldo":
        products = Product.objects.filter(
            Q(club__name="Al Nassr FC", season="2023-24") |  
        Q(club__name="Real Madrid", season__in=["2016-17","2011-12","2013-14"]) |  # Fcbarcelone from 2005 to 2021
        
        Q(club__name="Portugal", season="2022") |
        Q(club__name="Juventus FC", season="2021-22") |
        Q(club__name="Manchester United", season__in=["2021", "2022", "2022-23"])  # PSG in 2021-2022 and 2022-2023
        )
        seasons = list(set(product.season for product in products))
        sorted_seasons = sorted(seasons, key=lambda x: tuple(map(int, x.split('-'))), reverse=True)
        prods=[]
        i=0
        for season in sorted_seasons:
            prods.append([])
            for prod in products:
                if  prod.season == season:
                    prods[i].append(prod)
            i=i+1

        data = zip(sorted_seasons,prods)
        context = {'cartItems':cartItems ,'player': 'Cristiano Ronaldo',"data":data,"username":username}
        return render(request, 'store/player.html', context)
    
    else:
        products = Product.objects.filter(Q(club__league=categorie, season="2023-24") | Q(club__league=categorie, season="2023"))
    if "product_club" in request.GET:
        
        club_name = request.GET.get('product_club')  # Get the club name from the GET request
        

        # Query the database to get the products for the specified club
        club_products = Product.objects.filter(club__name=club_name)
    else:
        club_products=[]
    
    context = {'cartItems':cartItems ,'clubs': clubs,"products": products,"club_products":club_products,"username":username}
    return render(request, 'store/league.html', context)
def team(request,club_name):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user
    username = request.user.username
        
    club = Club.objects.get(name=club_name)

    club_products = Product.objects.filter(club__name=club_name)
    seasons = []
    for prod in club_products:
        if prod.season not in seasons:
            seasons.append(prod.season)
   
    seasons = list(set(product.season for product in club_products))
    sorted_seasons = sorted(seasons, key=lambda x: tuple(map(int, x.split('-'))), reverse=True)
    prods=[]
    i=0
    for season in sorted_seasons:
        prods.append([])
        for prod in club_products:
            if  prod.season == season:
                prods[i].append(prod)
        i=i+1

    data = zip(sorted_seasons,prods)
    context = {'cartItems':cartItems ,'club': club,"data":data,"username":username}
    return render(request, 'store/clubs.html', context)
def sort_year_ranges(year_range):
    start_year, end_year = map(int, year_range.split('-'))
    return start_year, end_year  
def special(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user
    username = request.user.username
        
    products = Product.objects.filter(type__in=["Special Edition","Special Edition 2","Special Edition 3","Special Edition 4"])
   
    context = {'cartItems':cartItems ,'products': products,'username':username}
    return render(request, 'store/special.html', context)
