from rest_framework import generics,authentication,mixins,permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .permissions import IsStaffEditorPermission
from .serializers import PrimaryProductSerializer



class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer
    authentication_classes=[authentication.SessionAuthentication]
    #default django classes
    # permission_classes=[permissions.DjangoModelPermissions]
    
    
    #custom permission classes
    permission_classes=[IsStaffEditorPermission]
    
    def perform_create(self, serializer):
        # print(serializer.validated_data)
        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content')
        # or None
        if content is None:
            content=title
        serializer.save(content=content)


class ProductMixinView(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,generics.GenericAPIView):
    
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer
    lookup_field='pk'
    
    def get(self,request,*args,**kwargs):
        pk=kwargs.get('pk') 
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,*kwargs)
    
    def perform_create(self, serializer):
        content=serializer.validated_data.get('content')
        if content is None:
            content="Single class view using mixins"
        serializer.save(content=content)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer 


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer 
    lookup_field='pk'
    
    def perform_update(self, serializer):
        instance=serializer.save()
        if not instance.content:
            instance.content=instance.title
            

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=PrimaryProductSerializer 
    lookup_field='pk'
     
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        


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
        
    