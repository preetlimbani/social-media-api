from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, CustomTokenObtainPairSerializer, CreateUserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CreateUserRegistration(APIView):
    def post(self,request):
        serializer = CreateUserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"Message":"User Registered Successfully"})
        else:
            return Response({"Error":serializer.errors})

class AuthenticateAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'},)

        refresh = CustomTokenObtainPairSerializer.get_token(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user_to_follow = User.objects.filter(id=id).first()
        follower = request.user
        if user_to_follow is None:
            return Response({'error': 'User not found'},)

        follower.following.add(user_to_follow)
        user_to_follow.followed_by.add(request.user)

        return Response({'success': 'User followed'},)


class UnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user_to_unfollow = User.objects.filter(id=id).first()

        if user_to_unfollow is None:
            return Response({'error': 'User not found'},)

        request.user.following.remove(user_to_unfollow)
        user_to_unfollow.followed_by.remove(request.user)

        return Response({'success': 'User unfollowed'},)

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,)



class PostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,)

        return Response(serializer.errors,)

class DeletePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        post_to_delete = Post.objects.filter(id=id, user=request.user).first()

        if post_to_delete is None:
            return Response({'error': 'Post not found'},)

        post_to_delete.delete()
        return Response({'success': 'Post deleted'},)

class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        post_to_like = Post.objects.filter(id=id).first()

        if post_to_like is None:
            return Response({'error': 'Post not found'},)

        like = Like.objects.filter(post=post_to_like, user=request.user).first()

        if like is None:
            Like.objects.create(post=post_to_like, user=request.user)

        return Response({'success': 'Post liked'},)

class UnlikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        post_to_unlike = Post.objects.filter(id=id).first()

        if post_to_unlike is None:
            return Response({'error': 'Post not found'},)

        like = Like.objects.filter(post=post_to_unlike, user=request.user).first()

        if like is not None:
            like.delete()

        return Response({'success': 'Post unliked'},)

class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        post_to_comment = Post.objects.filter(id=id).first()

        if post_to_comment is None:
            return Response({'error': 'Post not found'},)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post_to_comment)
            return Response(serializer.data,)

        return Response(serializer.errors,)

class SinglePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        post = Post.objects.filter(id=id).first()

        if post is None:
            return Response({'error': 'Post not found'},)

        likes = Like.objects.filter(post=post)
        comments = Comment.objects.filter(post=post)
        data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'created_at': post.created_at,
            'likes': LikeSerializer(likes, many=True).data,
            'comments': CommentSerializer(comments, many=True).data,
        }
        return Response(data,)

class AllPostsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(user=request.user).order_by('-created_at')
        data = []

        for post in posts:
            likes = Like.objects.filter(post=post)
            comments = Comment.objects.filter(post=post)
            data.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'created_at': post.created_at,
                'likes': len(likes),
                'comments': CommentSerializer(comments, many=True).data,
            })

        return Response(data,)
