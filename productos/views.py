from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import SubirProducto

@login_required(login_url="/users/login/")
def lista_productos_view(request):
    # Obtener los primeros 20 productos
    lista_productos = Producto.objects.all().order_by('-fecha_publicacion')[:20]
    
    if request.method == 'POST':
        form = SubirProducto(request.POST)
        if form.is_valid():
            # Guardar el producto asociado al usuario actual
            nuevo_producto = form.save(commit=False)
            nuevo_producto.usuario = request.user
            nuevo_producto.save()
            return redirect('productos:lista')
    else:
        form = SubirProducto()
    
    return render(request, "productos/lista.html", { 
        "lista_productos": lista_productos,
        "form": form 
    })