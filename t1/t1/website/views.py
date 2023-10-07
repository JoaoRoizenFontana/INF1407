from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record
from .models import Receita
from .forms import ReceitaForm

def home(request):
    receitas = Receita.objects.all()  # Busque todas as receitas

    if request.method == "POST":
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            # Autenticação
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect("home")
            else:
                messages.success(request, "Error logging in, try again")

        campo_texto = request.POST.get('campo_texto')
        if campo_texto:
            Receita.objects.create(campo_texto=campo_texto)

    return render(request, 'home.html', {'receitas': receitas})

'''def home(request):
    receitas = Receita.objects.all()  # Busque todas as receitas
    # Verifica login
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Autentificacao
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect("home")
        else:
            messages.success(request, "error loggin in, try again")
            return redirect("home")
    
    else:
        return render(request, 'home.html', {'receitas': receitas})'''


def logout_user(request):
    logout(request)
    messages.success(request, "You havve been logged out")
    return redirect("home")

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Autenticar e logar
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso")
            return redirect('home')
    
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

'''def salvar_receita(request):
    if request.method == "POST":
        campo_texto = request.POST.get('campo_texto')
        if campo_texto:
             Receita.objects.create(campo_texto=campo_texto)
    
    return redirect('home')'''

def editar_receita(request, id_receita):
    receita = get_object_or_404(Receita, id=id_receita)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReceitaForm(instance=receita)

    return render(request, 'editar_receita.html', {'form': form, 'receita': receita})