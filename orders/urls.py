from django.urls import path
from . import views  # Update the import statement here

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),  # Use the 'store' view from the correct import
   
]
