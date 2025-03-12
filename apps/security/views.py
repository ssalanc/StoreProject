from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import RegisterForm, LoginForm

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'security/auth_login.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "¡Bienvenido de nuevo!")
        
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
            
        return redirect('core:home')

    def form_invalid(self, form):
        messages.error(self.request, "Las credenciales proporcionadas son incorrectas. Por favor, inténtalo de nuevo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('security:dashboard')

def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya tienes una sesión activa.")
        return redirect('security:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido a Zay Shop.")
            return redirect('security:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'security/register.html', {
        'form': form,
        'title': 'Registro de Usuario',
    })

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        birth_date = request.POST.get("birth_date")
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")

        # Verifica si la contraseña actual es correcta antes de actualizar
        if not user.check_password(password):
            messages.error(request, "Contraseña actual incorrecta.")
            return redirect("security:profile")

        # Actualiza los datos del usuario
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.birth_date = birth_date if birth_date else None

        # Si el usuario quiere cambiar su contraseña
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Mantiene la sesión activa

        user.save()
        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect("security:profile")
    
    return render(request, "security/profile.html")






