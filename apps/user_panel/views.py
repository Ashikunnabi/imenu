from django.shortcuts import render


def my_account(request):
    return render(request, 'user_panel/my_account.html')


def my_cart(request):
    return render(request, 'user_panel/my_cart.html')


def orders_cancellations(request):
    return render(request, 'user_panel/orders_cancellations.html')


def my_sales_reps(request):
    return render(request, 'user_panel/my_sales_reps.html')


def finale_invoice(request):
    return render(request, 'user_panel/finale_invoice.html')


def return_order(request):
    return render(request, 'user_panel/return.html')
