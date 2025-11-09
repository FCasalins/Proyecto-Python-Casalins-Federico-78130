from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from usuarios.forms import UsuarioCreationForm, UsuarioChangeForm

def register(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('profile_detail')
    else:
        form = UsuarioCreationForm()
    return render(request, "usuarios/register.html", {"form": form}) 


@login_required
def profile_details(request):
    return render(request, "usuarios/profile_detail.html", {"user": request.user})


def profile_edit(request):
    if request.method == "POST":
        form = UsuarioChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile_detail")
    else:
        form = UsuarioChangeForm(instance=request.user)
    return render(request, "usuarios/profile_edit.html", {"form": form})
