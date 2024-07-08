from random import seed, randint
from threading import Thread

from django import views
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .mixins import AnonymityRequiredMixin
from .forms import LoginForm, CustomUserCreationForm
from .models import Profile
from .utils import generate_token


User = get_user_model()
error_css_class = 'is-valid'


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Почта подтверждена. Теперь вы можете войти в свой аккаунт!')
        return redirect(reverse('login'))
    
    return render(request, 'users/activation_failed.html', {'user': user})


class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)
    
    def run(self) -> None:
        self.email.send()

class LoginView(AnonymityRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context=context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user and user.is_verified:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)
    

class RegistrationView(AnonymityRequiredMixin, views.View):
    @staticmethod
    def generate_code():
        seed()
        return str(randint(100000, 999999))
    
    @staticmethod
    def send_activation_email(request, user):
        current_site = get_current_site(request)
        email_subject = 'Подтвердите свою почту'
        email_body = render_to_string('users/activate_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        EmailThread(email).start()
    
    @staticmethod
    def get_context(form):
        return {'form': form}
    
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'users/registration.html', context=self.get_context(form))
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            self.send_activation_email(request, new_user)

            messages.add_message(request, messages.SUCCESS, 'Подтвердите свою почту, чтобы войти в аккаунт')

            return render(request, 'users/verificate_email.html', context=self.get_context(form))
        return render(request, 'users/registration.html', context=self.get_context(form))


class UserProfileView(views.View):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user_profile = Profile.object.get(user=user)
        context = {
            'user': user,
            'user_profile': user_profile
        }
        return render(request, 'users/user_profile.html', context=context)