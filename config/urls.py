#type:ignore
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from rental import views
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from rental.views import register_view


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher URLs
]

# Wrap your main URLs with i18n_patterns
urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('place-order/', views.place_order, name='place_order'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('contact/', views.contact_view, name='contact'),
    path('products/', views.gallery_view, name='products'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Product
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Auth
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', register_view, name='register'),

    # Account
    path('account/', views.account_view, name='account'),
    
    prefix_default_language=False,  # Don't prefix default language (English)
)

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)