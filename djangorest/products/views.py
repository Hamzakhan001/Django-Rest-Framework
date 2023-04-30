from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer


@api_view(["GET","POST"])
def api_home(request,*args,**kwargs):
    model_data=Product.objects.all()
    data={}
     
    if model_data:
        # data=model_to_dict(model_data,fields=['id','title','price','sale_price','d'])
        data=ProductSerializer(model_data)
    return Response(data)
 