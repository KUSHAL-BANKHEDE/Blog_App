from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator

class UserSignupSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'tokens')
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except ValueError as e:
            raise serializers.ValidationError(str(e))

class UserLoginSerializer(serializers.Serializer):
    username_or_email  = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username_or_email = serializers.CharField()
        password = data.get('password')

        # Add custom validation logic for login, e.g., check credentials
        user = authenticate(request=None, username=username_or_email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        return data
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_date')

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'published_date', 'comments')
