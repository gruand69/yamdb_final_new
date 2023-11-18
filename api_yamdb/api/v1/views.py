# -------------------------------------------------------------------------------
# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.generics import CreateAPIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
# from api_yamdb.settings import EMAIL_HOST_USER

# User = get_user_model()


# class CreateUserView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]  # Разрешает неограниченный доступ
#     # независимо от того, был ли запрос аутентифицирован или нет

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)  # Возвращает
#         # класс, который следует использовать для сериализатора
#         serializer.is_valid(raise_exception=True)  # Если данные не будут
#         # соответствовать схеме, то вызов метода
#         # is_valid(raise_exception=True)
#         #  приведёт к исключению ValidationError.
#         self.perform_create(serializer)  # Вызывается CreateModelMixin
#         # при сохранении нового экземпляра объекта.
#         headers = self.get_success_headers(serializer.data)

#         username = request.data.get('username')
#         email = request.data.get('email')
#         user = get_object_or_404(User, username=username)
#         code = default_token_generator.make_token(user)
#         # print(code)
#         user.confirmation_code = code
#         send_mail(
#             subject="Регистрация в проекте YaMBd",
#             message=f'Ваш проверочный код: {code}',
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[email],
#             fail_silently=False,
#         )
#         return Response(serializer.data, status=status.HTTP_201_CREATED,
#                         headers=headers)
#         # return Response({"code": user.confirmation_code},
#         # status=status.HTTP_201_CREATED, headers=headers)
# # @api_view(['POST'])
# # def create_user(request):
# #     serializer = RegisterSerializer(data=request.data)
# #     if serializer.is_valid():
# #         serializer.save()

# #         return Response(serializer.data, status=status.HTTP_201_CREATED)
# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_token(request):
#     # serializer = MyTokenObtainPairSerializer(data=request.data)
#     # email = request.data.get('email')
#     username = request.data.get('username')
#     user = get_object_or_404(User, username=username)
#     code = request.data.get('confirmation_code')
#     if default_token_generator.check_token(user, code):
#         user.is_active = True
#         user.save()
#         return Response({"message": "Аккаунт активирован"},
#                         status.HTTP_200_OK)

#     return Response({"message": "неверный код подтверждения."},
#                     status.HTTP_400_BAD_REQUEST)
# --------------------------------------------------------------------------------------
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title

from api_yamdb.settings import EMAIL_HOST_USER

from .filters import TitleFieldFilter
from .permissions import IsAdministrator, IsAdminOrReadOnly, OwnerOrModerator
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreViewSerializer, ReadTitleSerializer,
                          RegisterSerializer, ReviewSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # queryset = Title.objects.all().annotate(
    #     Avg('reviews__score')).order_by('name')
    # serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    http_method_names = ['get', 'patch', 'post', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFieldFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTitleSerializer
        return TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreViewSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministrator, ]
    http_method_names = ['get', 'patch', 'post', 'delete']
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated, ],
        url_path='me',
    )
    def me(self, request):
        if request.method == 'PATCH':
            if 'role' in request.data:
                return Response('Field "role" is forbidden',
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(request.user, data=request.data,
                                        partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # serializer = self.get_serializer(request.user)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
def create_user(request):
    serializer = RegisterSerializer(data=request.data)
    if User.objects.filter(username=request.data.get("username"),
                           email=request.data.get("email")).exists():
        user = User.objects.get(
            username=request.data["username"],
            email=request.data["email"]
        )
        message = 'Renew confirmation code'
        user.confirmation_code = create_send_conf_code(user, message)
        return Response('Renewing confirmation code',
                        status=status.HTTP_200_OK)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(
            username=request.data["username"],
            email=request.data["email"]
        )
        message = 'API YamDB registration'
        user.confirmation_code = create_send_conf_code(user, message)
        # print(user.confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_permissions(self):
        # if self.request.method == 'PATCH':
        if self.request.method in ('PATCH', 'DELETE'):
            return (OwnerOrModerator(), )
        return super().get_permissions()

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_permissions(self):
        # if self.request.method == 'PATCH':
        if self.request.method in ('PATCH', 'DELETE'):
            return (OwnerOrModerator(), )
        return super().get_permissions()

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())


def create_send_conf_code(user, message):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject=message,
        message=f'Your confirmation code: {confirmation_code}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return confirmation_code


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username')
        )
        code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, code):
            user.is_active = True
            # user.save()
            # print('OK')
            access = AccessToken.for_user(user)
            return Response(f'token: {access}',
                            status=status.HTTP_200_OK)
        return Response({"message": "Confirmaition code is not correct"},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
