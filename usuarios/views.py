from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.forms import UsuarioCreationForm, UsuarioChangeForm


def register(request):
    """
    Vista de registro de usuario.
    - Permite crear usuario cliente, agente o tasador.
    - Requiere código de autorización para los dos últimos.
    - Autologin tras registro exitoso.
    """
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Tu cuenta fue creada con éxito.")
            return redirect("profile_detail")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = UsuarioCreationForm()

    return render(request, "usuarios/register.html", {"form": form})


@login_required
def profile_detail(request):
    """
    Muestra el perfil del usuario actual.
    """
    return render(request, "usuarios/profile_detail.html")


@login_required
def profile_edit(request):
    """
    Permite al usuario editar su perfil.
    - Usuarios normales: solo datos personales.
    - Staff/admins: también pueden modificar roles y estado activo.
    """
    if request.method == "POST":
        form = UsuarioChangeForm(
            request.POST,
            request.FILES,
            instance=request.user,
            user=request.user  # <-- Para mostrar los campos extra si es staff
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("profile_detail")
        else:
            messages.error(request, "Revisa los errores del formulario.")
    else:
        form = UsuarioChangeForm(instance=request.user, user=request.user)

    return render(request, "usuarios/profile_edit.html", {"form": form})


@login_required
def profile_delete(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "No se encontró la cuenta.")
        return redirect("login")
    if request.method == "POST":
        if "confirm" in request.POST:
            username = user.username
            user.delete()
            messages.success(request, f"La cuenta '{username}' fue eliminada correctamente.")
            return redirect("login")
        else:
            return redirect("profile_detail")
        
    return render(request, "usuarios/profile_delete.html")