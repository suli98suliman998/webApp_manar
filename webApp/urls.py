from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('customer/', customer_view, name='customer_view'),
    path('employee/', employee_view, name='employee_view'),
    path('order/create/', create_new_customer_order, name='create_new_customer_order'),
    path('order/update/<int:order_id>/', update_order_status, name='update_order_status'),
    path('employee/orders/', employee_assigned_orders, name='employee_assigned_orders'),
    path('logout/', logout_view, name='logout'),
]
