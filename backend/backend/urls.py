from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from accounts.views.password_reset import PasswordResetConfirmView
from accounts.views.registration import ConfirmRegistrationView

api = [
    path('', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('reviews.urls')),
    path('patients/', include('patientcard.urls')),
    path('notifications/', include('notifications.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/password-reset-confirm/<str:uid>/<str:token>', PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('api/register-user-confirm/<str:uid>/<str:token>', ConfirmRegistrationView.as_view(),
         name='register-user-confirm'),
    path('__debug__/', include('debug_toolbar.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
