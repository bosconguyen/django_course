from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):

    return render(request, 'quotes/index.html')

# login
def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw)
        request.session['id'] = user.id
        messages.success(request, "You have successfully registered")
    return redirect('/quotes')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        return redirect('/quotes')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
# login end

def dashboard(request):
    user = User.objects.get(id = request.session['id'])
    favorites = user.favorite_quotes.all

    context = {
        'user': user,
        'quotes': Quote.objects.exclude(favorites = user),
        'favorites': favorites
    }
    return render(request,'quotes/dashboard.html', context)


def add_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/quotes')
    else:
        Quote.objects.create_quote(request.POST, request.session['id'])
    return redirect('/quotes')

def add_favorite(request, quote_id):
    if request.method == 'POST':
        fav_quote = Quote.objects.get(id = quote_id)
        fav_by = User.objects.get(id = request.session['id'])
        fav_quote.favorites = fav_by
        fav_quote.save()
    return redirect('/quotes')

def remove_favorite(request, quote_id):
    if request.method == 'POST':
        rem_quote = Quote.objects.get(id = quote_id)
        rem_by = User.objects.get(id = request.session['id'])
        rem_quote.favorites = None
        rem_quote.save()
    return redirect('/quotes')

def user(request, user_id):
    user = User.objects.get(id=user_id)
    quotes = user.posted_quotes.all
    context = {
        'user': user,
        'quotes': quotes
    }
    return render(request, 'quotes/user.html', context)
