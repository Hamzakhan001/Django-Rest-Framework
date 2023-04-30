from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import PrimaryProductSerializer



class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer
    
    def perform_create(self, serializer):
        # print(serializer.validated_data)
        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content')
        # or None
        if content is None:
            content=title
        serializer.save(content=content)
        

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer
    

@api_view(["GET"])
def product_alt_view(request,pk=None,*args, **kwargs):
    method=request.method
    
    if method== "GET":
        if pk is not None:
            obj=get_object_or_404(Product,pk=pk)
            data=PrimaryProductSerializer(obj,many=False)
            return Response(data.data)
        else:
            qs=Product.objects.all()
            data=PrimaryProductSerializer(qs,many=True)
            return Response(data.data)
    if method=="POST":
        serializer=PrimaryProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title=serializer.validated_data.get('title')
            content=serializer.validated_data.get('content') or None
            if content is None:
                content=title
                serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid":"no data"},status=400)
        
    