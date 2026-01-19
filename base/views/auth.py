from base.models import Offer, Estate
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render


class SignUpView(View):
    def get(self, request):
        return render(request, 'auth/sign-up.html')
    
    def post(self, request):
        return render(request, 'auth/sign-up.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
    
    def post(self, request):
        return render(request, 'auth/login.html')

class LogoutView(View):
    def post(self, request):
        return render(request, 'auth/logout.html')