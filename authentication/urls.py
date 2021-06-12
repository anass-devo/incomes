from django.urls import path
from .views import RegistrationView,UsernameValidationView,EmailValidationView,VerificationView,LoginView,completepasswordreset,LogoutView,RequestPasswordResetEmail
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register',RegistrationView.as_view(),name="register"),
    path('login',LoginView.as_view(),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
    path('activate/<uidb64>/<token>',csrf_exempt(VerificationView.as_view()),name="activate"),
    path('set-new-password.html/<uidb64>/<token>',csrf_exempt(completepasswordreset.as_view()),name="reset-user-password"),
    path('reset_password',csrf_exempt(RequestPasswordResetEmail.as_view()),name="reset_password"),
]