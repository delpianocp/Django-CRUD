from django.contrib import admin
from django.urls import path
from inicio import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="inicio"),
    path('registro/', views.formRegister, name="registro"),
    path('indexuser/', views.indexuser, name="indexuser"),
    path('logout/', views.log_out, name="logout"),
    path('login/', views.log_in, name="login"),
    path('carga/', views.carga, name="carga"),
    path('mediciones/', views.mediciones, name="mediciones"),
    path('grafico/', views.grafico, name="grafico"),
    path('mediciones/<int:medida_id>/', views.medida, name="medida")
      
]
