from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import get_object_or_404
from .models import Products

def is_seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_seller:
            raise PermissionDenied  # error 403
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_seller_product(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        product = get_object_or_404(Products, id=kwargs['product_id'])

        if request.user != product.user:
            raise PermissionDenied  # error 403
        return view_func(request, *args, **kwargs)

    return _wrapped_view
