# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static # new
from django.contrib.auth import views as auth_views
from school import views as school_views # import the school views.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')), # Include school app URLs
    path('staff/', include("staff.urls")), 
    path('results/', include('result.urls')),  # Include your app's URLs
    path('login/', auth_views.LoginView.as_view(template_name='school/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='school:home'), name='logout'),
    path('logout/', school_views.custom_logout, name='lgout'), # Use custom logout view
    path('accounts/', include('django.contrib.auth.urls')), # Add this line
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # new

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)