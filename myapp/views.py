from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from myapp.models import MyUser, NewCustomerOrder, Employee

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Employee, MyUser, NewCustomerOrder


def create_new_customer_order(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        marital_status = request.POST.get('marital_status')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Auto-assign an employee based on minimum active_orders_count
        employee = Employee.objects.order_by('active_orders_count').first()
        employee.active_orders_count += 1
        employee.save()

        # Create a MyUser object associated with the User
        my_user = MyUser(username=username, password=password, user_type='customer')

        # Save the MyUser object
        my_user.save()

        # Create a NewCustomerOrder object
        new_order = NewCustomerOrder(
            employee=employee,
            username=my_user,
            customer_name=full_name,
            age=age,
            marital_status=marital_status,
            phone_number=phone_number,
            email=email
        )

        # Save the NewCustomerOrder object
        new_order.save()

        return redirect('employee_view')
    return render(request, 'create_new_customer_order.html')


def update_order_status_in_database(order, new_status):
    order.status = new_status
    order.save()


def get_order_by_id(order_id):
    try:
        order = NewCustomerOrder.objects.get(pk=order_id)
        return order
    except NewCustomerOrder.DoesNotExist:
        return None


def decrease_active_orders_count(username):
    try:
        employee = Employee.objects.get(username__username=username)
        employee.active_orders_count -= 1
        employee.save()
    except Employee.DoesNotExist:
        # Handle the case where the employee does not exist
        pass


def update_order_status(request, order_id):
    order = get_order_by_id(order_id)

    status = request.POST.get('status')
    employee_name = request.session.get('username')
    if status:
        update_order_status_in_database(order, status)
        decrease_active_orders_count(employee_name)
        return redirect('employee_view')

    return render(request, 'update_order_status.html', {'order': order})


def update_status():
    return None


def login_view(request):
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = my_authentication(request, username=username, password=password)
        if user is not None:
            # Set the user in the session
            request.session['user_type'] = user.user_type
            request.session['username'] = username
            login(request, user)

            if user.user_type == 'employee':
                return redirect('employee_view')
            else:
                return redirect('customer_view')

        return HttpResponse('Invalid username or password')
    else:
        # Display login form
        return render(request, 'login.html')


def my_authentication(request, username=None, password=None):
    try:
        user = MyUser.objects.get(username=username, password=password)
        return user
    except MyUser.DoesNotExist:
        return None


def get_user_type(user_id):
    user = MyUser.objects.get(id=user_id)
    if user.user_type == 'employee':
        return 'employee'
    elif user.user_type == 'customer':
        return 'customer'
    else:
        return None


def customer_view(request):
    username = request.session.get('username')
    customer = MyUser.objects.get(username=username)
    order = get_order_for_customer(customer.id)
    employee_name = Employee.objects.get(id=order.employee_id).emp_name

    context = {
        'customer': customer,
        'order': order,
        'employee_name': employee_name
    }

    return render(request, 'customer_view.html', context)


# def get_employee_from_request(request):
#     employee_id = request.session.get('employee_id')
#     print(employee_id)
#     if employee_id:
#         try:
#             employee = Employee.objects.get(id=employee_id)
#             return employee
#         except Employee.DoesNotExist:
#             pass
#     return None


def get_assigned_order_for_employee(employee_id):
    # Retrieve all orders with status 'waiting' assigned to the logged-in employee
    assigned_orders = NewCustomerOrder.objects.filter(employee_id=employee_id, status='waiting')
    if assigned_orders:
        return assigned_orders
    else:
        return None


def employee_assigned_orders(request):
    employee_name = request.session.get('username')  # Assuming the logged-in user is an employee
    employee_id = (MyUser.objects.get(username=employee_name)).id
    assigned_orders = get_assigned_order_for_employee(employee_id)
    if assigned_orders is None:
        message = "No assigned orders found."
        return render(request, 'employee_assigned_orders.html', {'message': message})
    else:
        return render(request, 'employee_assigned_orders.html', {'assigned_orders': assigned_orders})


def employee_view(request):
    username = request.session.get('username')
    user = MyUser.objects.get(username=username)
    print(1111111111111, user.id)
    employee = Employee.objects.get(username_id=user.id)

    return render(request, 'employee_view.html', {'employee': employee.emp_name})


def get_order_for_customer(customer):
    # Placeholder function to retrieve order for the customer
    # Replace with your own logic to fetch order from the database
    try:
        order = NewCustomerOrder.objects.get(username=customer)
        return order
    except NewCustomerOrder.DoesNotExist:
        return None


def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'home' with the appropriate URL name for your home page
