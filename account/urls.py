from django.urls import path
from.import views

urlpatterns = [
    path("", views.Account, name="Account"),
    path("signup/", views.Signup, name="Signup"),
    path("login/", views.Login, name="Login"),
    path("profile/", views.Profile, name="Profile"),
    path("activate/<int:pk>/<str:key>/", views.Activate, name="Activate"),
    path("logout/", views.Logout, name="Logout"),
    path("forget-password/", views.ForgetPassword, name="ForgetPassword"),
    path('reset-password/<uidb64>/<token>/', views.PasswordResetConfirm, name='PasswordResetConfirm'),
] 