from .models import *

#def class_processor(request):
 #   class_names = list(set([obj.__class__.__name__ for obj in Products.objects.all()]))
 #   return {
 #       'class_names' : class_names
  #  }


def class_processor(request):
    # Obter automaticamente os nomes das subclasses de Products
    subclasses = Products.__subclasses__()
    class_names = ['Products'] + [cls.__name__ for cls in subclasses]  # Adiciona 'Products' como opção

    return {
        'class_names': class_names
    }