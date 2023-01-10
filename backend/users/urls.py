from django.urls import path
from knox import views as knox_view
from users.views import RegisterView, UserView, LoginView

urlpatterns = [
    path(
        'register',
        RegisterView.as_view(),
        name='register'
    ),
    path(
        'login',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'user',
        UserView.as_view(),
        name='knox_user'
    ),
    path(
        'logout',
        knox_view.LogoutView().as_view(),
        name='logout'
    ),
]
