from rest_framework import serializers
from .models import Department, Position, Employee
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# ✅ Custom token serializer using email
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        # ✅ Map 'email' to 'username' so SimpleJWT can authenticate properly
        attrs['username'] = attrs.get('email')  
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email  # optional extra info in token
        return token