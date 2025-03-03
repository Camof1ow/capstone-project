from rest_framework import serializers
from .models import Menu  # Menu 모델 import

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'  # 모든 필드 직렬화
