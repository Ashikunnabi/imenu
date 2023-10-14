from django.shortcuts import render


def index(request):
    return render(request, "front_end/index.html")


def category(request):
    return render(request, "front_end/category.html")


def product_detail(request, uuid):
    return render(request, "front_end/product-detail.html")


def favorite(request):
    return render(request, "front_end/favorite.html")


def cart(request):
    return render(request, "front_end/cart.html")


def account(request):
    return render(request, "front_end/account.html")


def change_password(request):
    return render(request, "front_end/change-password.html")


def chat(request):
    return render(request, "front_end/chat.html")


def edit_profile(request):
    return render(request, "front_end/edit-profile.html")


def product_list(request, uuid):
    return render(request, "front_end/product-list.html")
