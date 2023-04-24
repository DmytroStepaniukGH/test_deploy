from django.urls import path

from accounts.views.password_reset import PasswordResetRequestView, PasswordResetConfirmView # noqa
from accounts.views.registration import RegistrationView, ConfirmRegistrationView # noqa
from accounts.views.login import LoginView # noqa
from accounts.views.logout import LogoutView # noqa
from accounts.views.account_info import AccountView # noqa
from accounts.views.account_edit import AccountEditView, AccountPasswordEditView # noqa

app_name = 'accounts'

urlpatterns = [
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('register-user/', RegistrationView.as_view(), name='register-user'),
    path('register-user-confirm/', ConfirmRegistrationView.as_view(), name='register-user-confirm'),
    path('login-user/', LoginView.as_view(), name='login-user'),
    path('logout-user/', LogoutView.as_view(), name='logout-user'),
    path('user-<int:user_id>/my-account/', AccountView.as_view(), name='my-account'),
    path('user-<int:user_id>/my-account/edit/', AccountEditView.as_view(), name='my-account-edit'),
    path('user-<int:user_id>/my-account/edit-password/', AccountPasswordEditView.as_view(), name='edit-password')
]
