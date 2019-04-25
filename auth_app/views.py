from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, GoodForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login
from auth_app.models import Comment
from main_app.models import Good


def home(request):
    return redirect(auth_home)


@login_required(login_url='/authapp/login/')  # перенаправит на эту страницу для входа
def auth_home(request):
    list_goods = Good.objects.all().filter()
    return render(request, 'main_app/index.html', {
        'list_goods': list_goods
    })


def authapp_sign_up(request):
    user_form = UserForm()  # передаваемые поля для заполнения

    if request.method == 'POST':
        user_form = UserForm(request.POST)  # полученные от пользователя данные

        if user_form.is_valid():
            User.objects.create_user(**user_form.cleaned_data)  # если нет пользователя, создаем нового
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            )
            login(request, user)    # функция входа

            return redirect(auth_home)

    return render(request, 'auth_app/sign_up.html', {
        'user_form': user_form,
    })



