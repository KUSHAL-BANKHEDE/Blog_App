from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserLoginSerializer, UserSignupSerializer

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        serializer.validated_data['tokens'] = data
        return Response(serializer.data)

class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            return Response(data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)
