from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, WatchProgress, MyList
from .serializers import RegisterSerializer, UserSerializer, WatchProgressSerializer
from movies.models import Movie
from movies.serializers import MovieListSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if not user:
        return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    return Response({
        'token': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    })


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user).data)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_list_view(request):
    ids = MyList.objects.filter(user=request.user).values_list('movie_id', flat=True)
    movies = Movie.objects.filter(id__in=ids)
    return Response(MovieListSerializer(movies, many=True).data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def my_list_toggle(request, movie_id):
    if request.method == 'POST':
        MyList.objects.get_or_create(user=request.user, movie_id=movie_id)
        return Response({'inList': True})
    MyList.objects.filter(user=request.user, movie_id=movie_id).delete()
    return Response({'inList': False})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_list_status(request, movie_id):
    in_list = MyList.objects.filter(user=request.user, movie_id=movie_id).exists()
    return Response({'inList': in_list})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def continue_watching(request):
    progress = (
        WatchProgress.objects
        .filter(user=request.user, position__gt=10)
        .exclude(percent__gte=95)
        .order_by('-updated_at')[:10]
    )
    ids = [p.movie_id for p in progress]
    movies = Movie.objects.filter(id__in=ids)
    movie_map = {str(m.id): m for m in movies}
    result = []
    for p in progress:
        m = movie_map.get(str(p.movie_id))
        if m:
            data = MovieListSerializer(m).data
            data['progress'] = WatchProgressSerializer(p).data
            result.append(data)
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_progress(request, movie_id):
    position = request.data.get('position', 0)
    duration = request.data.get('duration', 0)
    WatchProgress.objects.update_or_create(
        user=request.user, movie_id=movie_id,
        defaults={'position': position, 'duration': duration}
    )
    return Response({'success': True})
