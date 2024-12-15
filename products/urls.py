from django.urls import path

from . import views

#con esto decimos que todas estas rutas son de la aplicacion products y asi nos evitamos en conflicto
#entre rutas, podemos tener dos o mas rutas con el mismo nombre
app_name = 'products'

urlpatterns = [
    path('search',views.ProductSearchListView.as_view() , name="search"),
    path('<slug:slug>',views.ProductDetailView.as_view() , name="product"),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('marcar-vendido/<int:pk>/', views.marcar_como_vendido, name='marcar_como_vendido'),
    path('mis-productos/', views.listar_productos_vendedor, name='listar_productos_vendedor'),
    
    path('casa/', views.casa_view, name='casa'),
    path('otros/', views.otros_view, name='otros'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('articulos/', views.articulos_view, name='articulos'),
]
