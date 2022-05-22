from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from core.forms import SingUpForm


def frontpage(request):
    return render(request, 'core/frontpage.html')


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm()
        if form.is_valid():
            user = form.get_user()

            login(request, user)
            return redirect('frontpage/')
    return render(request, 'core/login.html', {'form': form})


def registration_view(request):
    context = {}
    if request.POST:
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user=form.save()
            account= authenticate(email=email, password=raw_password)
            login(request,user)
            return redirect('login')
        else:
            context['form'] = form

    else:
        form = SingUpForm()
        context['form'] = form
    return render(request, 'core/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset_form.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('frontpage')

