import string
from random import randint
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import timedelta
from django.utils import timezone
from StartPage.models import Vocabulary, Book
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def CheckRegistrPage(user, username, password1, password2):
    message = 'success'
    allowed_symbols = set(string.ascii_letters + string.digits + '.' + '@' + '-' + '_')
    name = set(username)
    if user is not None:
        message = 'This user already exists'
    if not allowed_symbols.issuperset(name):
        message = 'Enter a valid username. Only letters, numbers, and @/./+/-/_ are allowed'
    pass1 = set(password1)
    pass2 = set(password2)
    if set(string.digits).issuperset(pass1) or set(string.digits).issuperset(pass1):
        message = 'This password is entirely numeric'
    if len(password1) < 8 or len(password2) < 8:
        message = 'This password is too short. It must contain at least 8 characters'
    if password1 != password2:
        message = 'Password fields did not match'
    else:
        if not allowed_symbols.issuperset(pass1) or not allowed_symbols.issuperset(pass2):
            message = 'Enter a valid password. Only letters, numbers, and @/./+/-/_ are allowed'
    if len(username) == 0 or len(password1) == 0 or len(password2) == 0:
        message = 'please, fill all the fields'
    return message


def RegisterPage(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            messages.success(request, 'You have created a new user ' + name + '.')
            return redirect('Login')
        else:
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            user = authenticate(request, username=username, password=password1)
            password2 = request.POST.get('password2')
            username = username.lower()
            message = CheckRegistrPage(user, username, password1, password2)
            messages.info(request, message)
    context = {'form': form}
    return render(request, 'Register.html', context)


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('library')
        else:
            messages.info(request, 'username or password is incorrect')
    context = {}
    return render(request, 'Login.html', context)


def LogoutPage(request):
    logout(request)
    return redirect('Login')


def MyView(request):
    return render(request, 'MainViewStartPage.html')


def add(request, book):
    cur_book = Book.objects.filter(book=book)[0]
    vocabulary = Vocabulary.objects.filter(book=cur_book).all()
    return render(request, "AddNewWords.html", {"vocabulary": vocabulary})


def add_to_db(word, translation, book):
    cur_book = Book.objects.filter(book=book)[0]
    Vocabulary.objects.create(word=word, translation=translation, book=cur_book)


def SendForm(request, w):
    first, second, book = w.split('>>!<<')
    cur_book = Book.objects.filter(book=book)[0]
    if Vocabulary.objects.filter(word=first, book=cur_book):
        old_translation = Vocabulary.objects.filter(word=first, book=cur_book)[0].translation
        time = timezone.now()
        info = Vocabulary.objects.filter(word=first, book=cur_book)[0]
        if time - info.status > timedelta(seconds=60):
            info.status = time
            info.save()
            return HttpResponse('This word already exists.' + old_translation)
        else:
            info.translation = second
            info.save()
            return HttpResponse('Translation was changed. Done')
    else:
        add_to_db(first, second, book)
        return HttpResponse('Ok')


def TestPage(request, book):
    SendWord(request, book)
    return render(request, 'TestAll.html')


def SendWord(request, book):
    cur_book = Book.objects.filter(book=book)
    vocabulary = Vocabulary.objects.filter(book__in=cur_book)
    count = vocabulary.count()
    if count != 0:
        random_object = vocabulary.all()[randint(0, count - 1)]
        return HttpResponse(random_object.translation)
    else:
        return HttpResponse('You have no words in this vocabulary. You have nothing to test.')


def ChangeColour(row, word):
    correct = {'red': 'orange', 'orange': 'green', 'green': 'green'}
    incorrect = {'red': 'red', 'orange': 'red', 'green': 'orange'}
    if row.word == word:
        status = True
        d = correct
    else:
        status = False
        d = incorrect
    row.colour_status = d[row.colour_status]
    row.save()
    return status


def CheckTranslation(request, string):
    word, translation, book = string.split('>>!<<')
    cur_book = Book.objects.filter(book=book)[0]
    your_row = Vocabulary.objects.filter(translation=translation, book=cur_book)[0]
    status = ChangeColour(your_row, word)
    if status:
        return HttpResponse('correct')
    return HttpResponse('wrong' + '>>!<<' + your_row.word)


def DeleteFromDB(request, string):
    index, book = string.split()
    cur_book = Book.objects.filter(book=book)[0]
    vocabulary = Vocabulary.objects.filter(book=cur_book)
    vocabulary.get(id=index).delete()
    return HttpResponse('deleted')


def library(request):
    user = request.user
    books = Book.objects.filter(user=user)
    return render(request, 'Library.html', {"books": books})


def AddNewToLibrary(request, book):
    user = request.user
    Book.objects.create(book=book, user=user)
    return HttpResponse('success')


def DeleteBook(request, cur_id):
    book_id, user_id = cur_id.split('........')
    index = int(book_id)
    book = Book.objects.filter(user_id=user_id)
    book.get(id=index).delete()
    return HttpResponse('deleted')


def add_error_reminder(request):
    return HttpResponse('error')