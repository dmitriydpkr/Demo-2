"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path,reverse_lazy, include
from main_app import views
from validform_app import views as validview
from auth_app import views as authview
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.get_index, name='index'),
    path('', authview.home, name='home'),
    re_path(r'^(?P<good_id>\d+)/$', views.good_detail, name='good-detail'),
    re_path(r'formpage/', validview.from_page, name='form-page'),
    re_path(r'authapp/login/$', LoginView.as_view(template_name='auth_app/login.html',
                                                  redirect_field_name=authview.auth_home), name='authapp-login'),
    re_path(r'authapp/$', authview.auth_home, name='auth_home'),
    re_path(r'^authapp/logout/$',LogoutView.as_view(next_page=reverse_lazy('authapp-login')), name='authapp-logout'),
    re_path(r'^authapp/sign-up/', authview.authapp_sign_up, name='authapp-sign-up'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

