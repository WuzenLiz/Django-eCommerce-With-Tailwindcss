from rest_framework import serializers
from .models import *

#serlizer
class ProductSerializer(serializers.ModelSerializer):
 class Meta:
  model = Product
  fields = '__all__'

 