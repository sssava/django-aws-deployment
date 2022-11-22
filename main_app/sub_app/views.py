import json
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.views.generic import ListView
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    movies = Movie.objects.all()
    category = Category.objects.all()
    paginator = Paginator(movies, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': page_obj,
        'category': category,
    }
    return render(request, 'home.html', context)


def about(request, slug):
    movie = Movie.objects.get(slug=slug)
    category = Category.objects.all()
    context = {
        'movie': movie,
        'category': category,
    }

    return render(request, 'about.html', context)


def category(request, slug):
    movies = Movie.objects.filter(category__slug=slug)
    category = Category.objects.all()
    paginator = Paginator(movies, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': page_obj,
        'category': category,
    }
    return render(request, 'category.html', context)


class Search(ListView):
    template_name = 'home.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account created successful for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_page(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        profile = Profile.objects.get(user=request.user)
        fav = FavMovie.objects.filter(user=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('user')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        profile = Profile.objects.get(user=request.user)
        fav = FavMovie.objects.filter(user=request.user)

    context = {'user_form': user_form, 'profile_form': profile_form, 'profile': profile, 'fav': fav}
    return render(request, 'user.html', context)


@login_required(login_url='login')
def likeMovie(request):
    data = json.loads(request.body)
    btnId = data['btnId']
    username = data['username']

    print('btnId', btnId)
    print('username', username)

    movie = Movie.objects.get(pk=btnId)
    user = User.objects.get(username=username)

    try:
        FavMovie.objects.get(movie=movie, user=user).delete()
    except:
        FavMovie.objects.create(movie=movie, user=user)

    return JsonResponse('Movie was added', safe=False)