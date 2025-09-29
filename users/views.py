from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile
from shopping_cart.cart_manager import CartManager

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created successfully for {username}! You can now log in.')
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:product_list')
        return super().dispatch(request, *args, **kwargs)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Merge carts after login
        cart_manager = CartManager(self.request)
        cart_manager.merge_carts(self.request.user)
        
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('products:product_list')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('products:product_list')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile_view(request):
    """Display user profile"""
    # Ensure user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, 'Your profile has been created!')
    
    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile': profile
    })

@login_required
def profile_edit_view(request):
    """Edit user profile"""
    # Ensure user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_edit.html', context)