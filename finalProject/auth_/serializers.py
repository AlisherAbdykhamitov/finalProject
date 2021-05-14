from rest_framework import serializers
from auth_.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                email=validated_data['email'],
                username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return