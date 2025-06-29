from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.formats import date_format

from .models import (
    UserProfile, Product, Cart, CartItem, Order,
    OrderItem, CardDetails
)

# Serializers for the models in the application

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['is_active', 'created_at', 'updated_at']
        
        
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Custom serializer to include user data in the token response
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']

        
class CartItemSerializer(serializers.ModelSerializer):
    # Get the product name and id
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    # Use a SerializerMethodField to get the product price
    total_price = serializers.SerializerMethodField()
    
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_name', 'product_id', 'quantity', 'total_price', 'color', 'size']
        read_only_fields = ['id', 'product_name', 'product_id', 'quantity', 'color', 'size']
        
    # Method to calculate the total price of the cart item
    def get_total_price(self, obj):
        return obj.get_total_price()
        
class CartSerializer(serializers.ModelSerializer):
    # Serialize the related CartItems
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'total_price']
        read_only_fields = ['created_at', 'updated_at']

    # Method to calculate the total price of the cart
    def get_total_price(self, obj):
        return obj.get_total_price()

        
        
class OrderItemSerializer(serializers.ModelSerializer):
    # Use a SerializerMethodField to get the product name
    product_name = serializers.CharField(source='product.name', read_only=True)
    # Use a SerializerMethodField to get the product image
    product_image = serializers.ImageField(source='product.image', read_only=True)
    # Use a SerializerMethodField to get the product price
    total_price = serializers.SerializerMethodField()
    
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_image', 'status', 'quantity', 'total_price', 'color', 'size']
        read_only_fields = ['id', 'product_name', 'product_image', 'quantity', 'color', 'size']
        
    # Method to calculate the total price of the order item
    def get_total_price(self, obj):
        return obj.get_total_price()
    
    
class CardDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetails
        fields = ['card_number', 'expiry', 'cvv']
        read_only_fields = ['card_number', 'expiry', 'cvv']
    
class OrderSerializer(serializers.ModelSerializer):
      # Serialize the related OrderItems
    items = OrderItemSerializer(many=True, read_only=True)
    card = CardDetailsSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    placed_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'shipping_address',
            'billing_address',
            'payment_method',
            'card',
            'placed_at',
            'status',
            'items',
            'total_price'
        ]
        

    # Method to calculate the total price of the order
    def get_total_price(self, obj):
        return obj.get_total_price()
    
    # Format the placed_at date to a more readable format
    def get_placed_at(self, obj):
        return date_format(obj.placed_at, 'F j, Y')
        