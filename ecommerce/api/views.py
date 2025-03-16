from rest_framework.decorators import api_view
from rest_framework.response import Response
from loja.models import Products
from .serializers import ProductsSerializer

@api_view(['GET'])
def getData(request):
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)
