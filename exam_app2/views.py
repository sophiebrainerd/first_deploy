from django.shortcuts import render, redirect
from .models import User, Quote
import re, bcrypt
from django.contrib import messages
from django.db.models import Q

def main(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User()
        user.name = request.POST['name']
        user.email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
        user.password = pw_hash
        user.save()
        thisUser = User.objects.get(email=request.POST['email'])
        request.session['userid'] = thisUser.id
        return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        thisUser = User.objects.get(email=request.POST['email'])
        request.session['userid'] = thisUser.id
        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect("/")

def success(request):
    return redirect('/quotes')

def all_quotes(request):
    thisUser = User.objects.get(id = request.session['userid'])
    userFaves = Quote.objects.filter(likes = thisUser)
    otherQuotes = Quote.objects.exclude(likes = thisUser)
    context = {
        'user' : thisUser, 'userFaves' : userFaves, 'otherQuotes' : otherQuotes
    }
    return render(request, 'quotes.html', context)

def quote_page(request, quoteid):
    thisQuote = Quote.objects.get(id = quoteid)
    context = {
        'thisQuote' : thisQuote
    }
    return render(request, 'edit.html', context)

def edit(request, quoteid):
    errors = Quote.objects.quote_validator(request.POST)
    thisQuote = Quote.objects.get(id = quoteid)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/quotes/{{quoteid}}')
    else:
        thisQuote.author = request.POST['author']
        thisQuote.content = request.POST['content']
        thisQuote.save()
        return redirect('/quotes')


def user_page(request, userid):
    thisUser = User.objects.get(id = userid)
    userQuotes = Quote.objects.filter(Q(contributor = thisUser) | Q(likes = thisUser))
    context = {
        'user' : thisUser, 'posts' : userQuotes
    }
    return render(request, 'user.html', context)

def favorite(request):
    thisUser = User.objects.get(id = request.session['userid'])
    newFave = request.POST['quoteid']
    thisUser.favorites.add(newFave)
    return redirect('/quotes')

def remove(request):
    thisUser = User.objects.get(id = request.session['userid'])
    thisQuote = request.POST['quoteid']
    thisUser.favorites.remove(thisQuote)
    return redirect('/quotes')

def delete(request, quoteid):
    thisQuote = Quote.objects.get(id = quoteid)
    person = thisQuote.contributor
    person.contributions.remove(thisQuote)
    thisQuote.delete()
    return redirect('/quotes')

def add_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    thisUser = User.objects.get(id = request.session['userid'])
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else: 
        thisQuote = Quote.objects.create(contributor = thisUser, author = request.POST['author'], content = request.POST['content'])
        thisQuote.save()
        return redirect('/quotes')