from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns =[
    path('', views.tienda, name ='tienda'),
    path('carrito/', views.carrito, name ='carrito'),
    path('checkout/', views.checkout, name ='checkout'),
    path('login/', views.login, name='login'),
    path('', views.main, name='main'),
    path('registro/', views.registro, name='registro' ),
    path('update_item/', views.updateItem, name='update_item'),
    path('procesar_orden/', views.procesarOrden, name='procesar_orden'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('productos/', views.producto_list, name='producto_list'),
    path('producto_create/', views.producto_create, name='producto_create'),
    path('producto_update/<int:pk>/', views.producto_update, name='producto_update'),
    path('producto_delete/<int:pk>/', views.producto_delete, name='producto_delete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]