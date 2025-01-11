from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Medicion
from matplotlib import pyplot as plt
import base64, urllib
import io
import re

# Create your views here.
def index(request):
    return render(request, "index.html")

def formRegister(request):
    if request.method == 'GET':
        print("es vista")
        return render(request, "form_registro.html")
    else:
        try:    
            print("envio por post")
            if request.POST['password'] == request.POST['password2']:
                user = User.objects.create_user(username=request.POST['nameuser'], password=request.POST['password'])
                user.save()
                login(request, user)
                print("Usuario registrado")
                return redirect("indexuser")
            else:
                return render(request, "form_registro.html", {
                'error': "Contraseñas no coinciden"
            })
        except:  
            return render(request, "form_registro.html", {
                'error': "Usuario ya existe"
            })
                        
def indexuser(request):
    return render(request, "indexuser.html")  

def log_out(request):
    logout(request)
    return redirect("inicio")

def log_in(request):
     if request.method == 'GET':
         return render(request, "login.html")
     else:
        try:
            user=authenticate(
                request, 
                username= request.POST['nameuser'], 
                password=request.POST['password'])   #Si no existe devuelve vacio 
            if user is None:
               return render(request, "login.html", {
                   'error':"Usuario o password incorrectos"
               })
            else:
                login(request, user)
                return redirect("indexuser")
        except:
            return render(request, "login.html")
      
     
def carga(request):
    if request.method == 'GET':
        return render(request, "carga.html")     
    else:
        s=request.POST['sector']
        m=request.POST['medicion']
        f_h=request.POST['fecha_medicion']
       
        med = Medicion(sector=s, medida=m, fecha_hora=f_h, tecnico=request.user)
        med.save()
    return render(request, "carga.html")  

def mediciones(request):
    if request.method == 'GET':
        med=Medicion.objects.all()
        return render(request, "mediciones.html", {
        'mediciones': med
        }) 
    else:
        print(request.POST)
        if request.POST['buscar'] == "buscar Sector": 
            
            busqueda=Medicion.objects.filter(sector=request.POST['sector']) 
            return render(request, "mediciones.html", {
                    'mediciones': busqueda
                    }) 
        else:
            lista_obj =[]    
            busqueda=Medicion.objects.filter(fecha_hora=request.POST['fecha_medicion']) 
            med=Medicion.objects.all()
            for l in med:
                print(str(l.fecha_hora)[:10])
                print(request.POST['fecha_medicion'][:10])
                if str(l.fecha_hora)[:10] == request.POST['fecha_medicion'][:10]:
                    lista_obj.append(l)
              
            
            return render(request, "mediciones.html", {
                    'mediciones': lista_obj
                    }) 

def grafico(request):
    lista_fecha=[]
    lista_medicion=[]
    med=Medicion.objects.all()
    
    med_ord = sorted(med, key=lambda x : x.fecha_hora)
    
    for l in med_ord:
        lista_fecha.append(str(l.fecha_hora)[5:10])
        lista_medicion.append(l.medida*220)
        
    for l in lista_fecha:
        print(l)
    
    
    año = lista_fecha
    vendido=lista_medicion
    plt.plot(año, vendido, marker='o')
    plt.title("Comsumo")
    plt.xlabel("Fecha")
    plt.ylabel("Potencia")
    plt.grid()
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string=base64.b64encode(buf.read())
    url=urllib.parse.quote(string)
    return render(request, "grafico.html", {
        'y':año, 'x':vendido, 'dt':url
        })
    
def medida(request, medida_id):
    if request.method == 'GET':
        medida=Medicion.objects.get(pk=medida_id)
        return render(request, "medida.html", {
            'medida': medida})
    else:
        if request.POST['boton'] == "Modificar":
            print(request.POST)
            medida_mod=Medicion.objects.get(pk=medida_id)
            medida_mod.sector = request.POST['sector']
            medida_mod.medida = request.POST['medicion']
            medida_mod.tecnico = request.user
            medida_mod.save()
            return render(request, "medida.html", {
                'medida': medida_mod,
                'mesage': 'Modificado con exito'})
        else:
            medida_mod=Medicion.objects.get(pk=medida_id)
            medida_mod.delete()
            return redirect('mediciones')