from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'barcode', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegistrationSerializer(serializers.ModelSerializer):
    # Fields that are not inside AppUser
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    # Down here there are fields from AppUser
    class Meta:
        model = AppUser
        fields = ['email', 'name', 'surname', 'nickname', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}  # More security
        }

    # Override save method to make passwords match
    def save(self):
        app_user = AppUser(
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            surname=self.validated_data['surname'],
            nickname=self.validated_data['nickname']
        )
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError({'password':'Passwords does not match'})
        app_user.set_password(password)
        app_user.save()
        return app_user

class ObservedProductSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='email',
        queryset = AppUser.objects.all()
    )

    product = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=Product.objects.all()
    )

    class Meta:
        model = ObservedProduct
        fields = ['creator', 'product', 'threshold_price']
        read_only_fields = ['id']

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []



