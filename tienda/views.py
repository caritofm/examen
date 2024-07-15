from django.shortcuts import render,redirect, get_object_or_404
from .models import *
import json
import datetime
from django.http import JsonResponse
from .forms import CustomerUserCreationForm, ProductoForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def tienda(request):
    productos = Producto.objects.all()
    if request.user.is_authenticated :
        cliente = request.user.cliente
        orden, created = Orden.objects.get_or_create(cliente=cliente, complete=False)
        items = orden.orderitem_set.all()
        carritoItems = orden.obtener_carrito_items
    else:
        items=[]
        orden = {'obtener_carrito_total':0, 'obtener_carrito_items':0, 'envio':False}
        carritoItems = orden['obtener_carrito_items']
    
    context ={'productos': productos, 'carritoItems':carritoItems}
    return render (request, 'tienda/tienda.html', context)
    
def carrito(request):
    if request.user.is_authenticated :
        cliente = request.user.cliente
        orden, created = Orden.objects.get_or_create(cliente=cliente, complete=False)
        items = orden.orderitem_set.all()
        carritoItems = orden.obtener_carrito_items
    else:
        items=[]
        orden = {'obtener_carrito_total':0, 'obtener_carrito_items':0,'envio': False}
        carritoItems = orden['obtener_carrito_items']
    
    context ={'items' :items,
               'orden':orden, 
               'carritoItems':carritoItems, 
               'user': request.user}
    return render (request, 'tienda/carrito.html', context)

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.user.is_authenticated:
        cliente = request.user.cliente
        orden, created = Orden.objects.get_or_create(cliente=cliente, complete=False)
        carritoItems = orden.obtener_carrito_items
    else:
        orden = {'obtener_carrito_total':0, 'obtener_carrito_items':0,'envio': False}
        carritoItems = orden['obtener_carrito_items']
    
    context = {
        'producto': producto,
        'carritoItems': carritoItems,
    }
    return render(request, 'tienda/producto_detalle.html', context)


def checkout(request):
    if request.user.is_authenticated :
        cliente = request.user.cliente
        orden, created = Orden.objects.get_or_create(cliente=cliente, complete=False)
        items = orden.orderitem_set.all()
        carritoItems=orden.obtener_carrito_items
    else:
        items=[]
        orden = {'obtener_carrito_total':0, 'obtener_carrito_items':0, 'envio': False}
        carritoItems=orden['obtener_carrito_items']
    context ={'items' :items, 'orden':orden}
    return render (request, 'tienda/checkout.html', context)

def login(request,user):
    context ={}
    return render(request, 'registration/login.html', context)

def main (request):
    context = {}
    return render(request, 'tienda/main.html', context)

def updateItem(request):
    try:
        data = json.loads(request.body)
        productoId = data['productoId']
        action = data['action']
        print('Action:', action)
        print('Producto:', productoId)

        cliente = request.user.cliente
        producto = Producto.objects.get(id=productoId)
        orden, created = Orden.objects.get_or_create(cliente=cliente, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(orden=orden, producto=producto)

        if action == 'add':
            orderItem.cantidad = (orderItem.cantidad + 1)
        elif action == 'remove':
            orderItem.cantidad = (orderItem.cantidad - 1)

        orderItem.save()

        removed = False
        if orderItem.cantidad <= 0:
            orderItem.delete()
            removed = True

        cartItems = orden.obtener_carrito_items
        cartTotal = orden.obtener_carrito_total

        return JsonResponse({
            'cartItems': cartItems, 
            'cartTotal': cartTotal,
            'itemCantidad': orderItem.cantidad,
            'itemTotal': orderItem.obtener_total,
            'removed': removed
        }, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

 
def procesarOrden(request):
    transaction_id= datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        cliente = request.user.cliente
        orden, created = Orden.objects.get_or_create(cliente=cliente, complete= False)
        total = float( data['form']['total'])
        orden.transaction_id= transaction_id

        if total == float(orden.obtener_carrito_total):
            orden.complete=True
        orden.save()
        if orden.envio == True:
            ShippingAdress.objects.create(
                cliente=cliente,
                orden=orden,
                direccion= data['envio']['direccion'],
                ciudad = data['envio']['ciudad'],
                estado = data['envio']['estado'],
                zipcode = data['envio']['zipcode'],

            )



    return JsonResponse('Pago completo', safe=False)

def registro(request):
    if request.method == 'POST':
        formulario = CustomerUserCreationForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1'] 
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Te has registrado correctamente")
                return redirect('tienda')  
    else:
        formulario = CustomerUserCreationForm()

    context = {'formulario': formulario}
    return render(request, 'registration/registro.html', context)

@staff_member_required
def producto_list(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'tienda/producto_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'tienda/producto_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/producto_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto_list')
    return render(request, 'tienda/producto_confirm_delete.html', {'producto': producto})