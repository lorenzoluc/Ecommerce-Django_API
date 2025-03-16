from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from loja.models import Products, Books, Phones

class ProductsSerializer(serializers.ModelSerializer):
    polymorphic_ctype = serializers.SerializerMethodField()

    class Meta:
        model = Products
        exclude = ['views']

    def get_polymorphic_ctype(self, obj):
        # Retorna o nome da classe real (por exemplo: "Books" ou "Phones")
        content_type = ContentType.objects.get_for_model(obj)
        return content_type.model