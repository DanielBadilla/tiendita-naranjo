from django.contrib import admin
from django.urls import path, include
from products.views import ProductListView
from django.conf.urls.static import static
from django.conf import settings
from products import views as products_views
from carts import views as cart_views  # Importar vistas de carts para el flujo de compra
from users import views as users_views  # Importar vistas de users para registro y login

urlpatterns = [
    path('', ProductListView.as_view(), name="index"),  # Página principal de productos
    path('usuarios/login', users_views.login_view, name="login"),  # Página de login
    path('usuarios/logout', users_views.logout_view, name="logout"),  # Logout
    path('usuarios/registro/', users_views.register_view, name="register"),  # Página de registro con ambos formularios
    path('usuarios/registro/vendedor/', users_views.registro_vendedor, name="register_vendedor"),  # Página para registro de vendedor
    path('mis-productos/', products_views.listar_productos_vendedor, name='listar_productos_vendedor'),

    path('admin/', admin.site.urls),  # Página del administrador

    # URLs de aplicaciones individuales
    path('productos/', include('products.urls')),  # Rutas de productos
    path('carrito/', include('carts.urls')),  # Rutas del carrito de compras
    path('orden/', include('orders.urls')),  # Rutas de órdenes

    # Flujo del proceso de compra
    path('checkout/', cart_views.checkout, name='checkout'),  # Paso para ingresar dirección y método de pago
    path('confirmacion/', cart_views.confirmacion_compra, name='confirmacion_compra'),  # Paso de confirmación de compra
    path('finalizar_compra/', cart_views.finalizar_compra, name='finalizar_compra'),  # Finalizar la compra
]

# Añadir URLs estáticas para el modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
