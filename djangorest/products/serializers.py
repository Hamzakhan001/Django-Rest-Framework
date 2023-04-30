from rest_framework import serializers
from .models import Product



class PrimaryProductSerializer(serializers.ModelSerializer):
    my_discount=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Product
        fields=['title','content','price','sale_price','my_discount']
        
    def get_my_discount(self,obj):
        # obj is the current instance it has all the properties of current run
        return obj.get_discount(); 
    
class SecondaryProductSerializer(serializers.ModelSerializer):
    my_discount=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Product
        fields=['title','content','price','sale_price','my_discount']
        
    def get_my_discount(self,obj):
        # obj is the current instance it has all the properties of current run
        # try:
        #     return obj.get_discount(); 
        # except:
        #     return None
        
        #when modal is not making instance and direct serializer is used
        
        if not hasattr(obj,'id'):
            return None;
        if not isinstance(obj,Product):
            return None
        return obj.get_discount();
            
        
        