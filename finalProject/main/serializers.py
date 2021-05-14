from rest_framework import serializers
from .models import BookCategory,BookProduct,Liked,Order,Card

class BookCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField()

    def create(self, validated_data):
        bookCategory = BookCategory.objects.create(category_name=validated_data.get('category_name'))
        return bookCategory

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.save()
        return instance

    def validate(self, data):
        if data['categoryName'] == '':
            raise serializers.ValidationError("Category should be written")
        return data

class BookProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    category = BookCategorySerializer()

    def create(self, validated_data):
        category = BookCategory.objects.get(id=validated_data.get('category'))
        bookProduct = BookProduct.objects.create(product_name=validated_data.get('product_name'),
                                                 description=validated_data.get('description'),
                                                 price=validated_data.get('price'),
                                                 category=category)
        return bookProduct

    def update(self, instance, validated_data):
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category',instance.category)
        instance.save()
        return instance

    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price can not be negative or zero")
        return data


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

        def validate_number(self, value):
            if '-' in value:
                raise serializers.ValidationError('Invalid')
            return value

class LikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'