from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/<str:order_number>/', views.payments, name='payments'),
    
    
    path('order-complete/<str:order_number>/',views.order_complete,name='order_complete'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-detail/<str:order_number>/', views.order_detail, name='order_detail'),
    
    path('invoice/<str:order_number>/', views.invoice, name='invoice')
    
]