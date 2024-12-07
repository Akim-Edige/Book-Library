"""
URL configuration for Web_Version project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from BookShelf import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

# Register the viewset with the router
# This will generate routes for ProductViewSet actions
# /products/
router.register(r'', views.BookViewSet, basename='books')
urlpatterns = [
    path("admin/", admin.site.urls),
    path('create/', views.create_book, name='create_book'),
    path('', views.book_list, name='show_books'),

    path('api/books/', include(router.urls), name='book-list'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),
    path('book/edit/<str:book_id>/', views.book_edit, name='book_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)