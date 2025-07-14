from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginForm, RegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.views import View


# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(username=data['username'], password=data['password'])
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Login Successful")
                else:
                    return HttpResponse("Login Failed")
            else:
                return HttpResponse("Login Failed")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {"form": form})


def dashboard_view(request):
    user = request.user
    profile = request.user.profile
    context = {'user': user, 'profile': profile}
    return render(request, 'pages/user_profile.html', context)


def user_register(request):
    if request.method == "POST":
        user_form = RegistrationForm (request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})

    else:
        user_form = RegistrationForm ()
    return render(request, 'account/register.html', {'user_form': user_form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})



class EditUserView(LoginRequiredMixin,View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

