from django.views import View
from django.http import *
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from common.utils import get_default_context
from .forms import SignupForm
from .models import Profile


class LogIn(View):
    def post(self, request):
        username = request.POST['uid']
        password = request.POST['pwd']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main'))
        c = get_default_context(request)
        c.update({"wrong": True})
        return render(request, 'first_page.html', c)

    def get(self, request):
        if request.user.id:
            return HttpResponseRedirect(reverse('main'))
        return render(request, 'first_page.html', get_default_context(request))


class LogOut(View):
    def get(self, request):
        if request.user.id:
            logout(request)
        return HttpResponseRedirect(reverse('login'))


class SignUp(View):
    def get(self, request):
        c = get_default_context(request)
        c.update({'form': SignupForm()})
        if request.user.id:
            return HttpResponseRedirect(reverse('main'))
        return render(request, 'signup.html', c)

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd["uid"], email=cd["email"], password=cd["pwd"])
            profile = Profile.objects.get(user=user)
            profile.nick = cd["name"]
            profile.sex = cd["sex"]
            profile.save()
            login(request, user)
            return HttpResponseRedirect(reverse('login'))

        c = get_default_context(request)
        c.update({'form': form})
        return render(request, 'signup.html', c)


class FcmRegisterView(LoginRequiredMixin, View):
    def get(self, request):
        token = request.GET["token"]
        if request.user.id:
            profile = Profile.objects.get(user=request.user)
            profile.fcm_registration_id = token
            profile.save()
        return HttpResponseRedirect(reverse('main'))

