from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        print("user not found")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.role == 'teacher':
        return render(request, 'accounts/teacher_dashboard.html')
    else:
        return render(request, 'accounts/student_dashboard.html')