from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductCreateForm, ProductCreateForm2, CommentCreateForm, CategoryCreateForm
from .models import Product, Category, Comment


def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'categories/category_products.html', context)


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            "categories": categories,
        }
        return render(request, 'categories/categories.html', context=context)


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


@login_required
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        selected_category = request.GET.get('category')
        search = request.GET.get('search')
        order = request.GET.get('order')
        if selected_category:
            category = get_object_or_404(Category, title=selected_category)
            products = products.filter(category=category)
        elif search:
            products = products.filter(
                Q(title__icontains=search)
            )
        elif order == 'title':
            products = products.order_by('title')
        elif order == '-title':
            products = products.order_by('-title')
        elif order == 'created_at':
            products = products.order_by('created_at')
        elif order == '-created_at':
            products = products.order_by('-created_at')
        else:
            products = products.exclude(user=request.user)

        context = {
            "products": products,
        }
        return render(request, 'products/products.html', context=context)


def product_detail_view(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return render(request, 'errors/404.html')
        context = {
            "product": product,
            'form': CommentCreateForm()
        }
        return render(request, 'products/product_detail.html', context)
    elif request.method == 'POST':
        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            Comment.objects.create(product_id=product_id, **form.cleaned_data)
            return redirect(f'/products/{product_id}/')
        context = {
            'form': form,
        }
        return render(request, 'products/product_detail.html', context)


def product_update_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return render(request, 'errors/404.html')
    if request.method == 'GET':
        context = {
            "form": ProductCreateForm(instance=product)
        }
        return render(request, 'products/product_update.html', context)
    elif request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(f'/products/{product.id}/')
        return render(request, 'products/product_update.html', {"form": form})


def product_create(request):
    if request.method == 'GET':
        context = {
            "form": ProductCreateForm2()
        }
        return render(request, 'products/products.create.html', context)
    elif request.method == 'POST':
        form = ProductCreateForm2(request.POST, request.FILES)
        if form.is_valid():
            Product.objects.create(**form.cleaned_data)
            return redirect("/products/")
        context = {
            "form": form
        }
        return render(request, 'products/products.create.html', context)


def category_create_view(request):
    if request.method == 'GET':
        context = {
            "form": CategoryCreateForm(),
        }
        return render(request, 'categories/categories_create.html', context=context)

    elif request.method == 'POST':
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            Category.objects.create(**form.cleaned_data)
            return redirect('/categories/')
        else:
            context = {
                "form": form
            }
        return render(request, 'categories/categories_create.html', context=context)
