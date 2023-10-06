from django.shortcuts import render, redirect
from usuarios.forms import login_forms, cadastro_forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

def login(request):
    form = login_forms()
    
    if request.method == 'POST':
        form = login_forms(request.POST)
        
        if form.is_valid():
            nome=form['nome_login'].value()
            senha=form['senha'].value()
            
        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha
        )
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f"{nome} logado(a) com sucesso!")
            return redirect('index')
        else:
            messages.error(request, "Erro ao efetuar o login!")
            return redirect('login')
            
            
    
    return render(request, "usuarios/login.html", {"form": form})

def cadastro(request):
    form = cadastro_forms()
    
    if request.method == 'POST':
        form = cadastro_forms(request.POST)
        
        if form.is_valid():
            nome=form["nome_cadastro"].value()
            email=form["email"].value()
            senha=form["senha_1"].value()
            
            if User.objects.filter(username=nome).exists():
                messages.error(request, "Usuário já existente")
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, "Cadastro efetuado com sucesso!")
            return redirect('login')
            
    
        
    return render(request, "usuarios/cadastro.html", {"form": form})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, "Logout efetuado com sucesso!")
        return redirect('login')
    
    else:
        return redirect('login')