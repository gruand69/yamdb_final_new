import re

# from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                {
                    'username': 'Name me is not valid'
                })
        match = re.fullmatch(r'^[\w.@+-]+', str(value))
        if match is None:
            raise serializers.ValidationError('Invalid symbols')
        return value


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
        extra_kwargs = {'username': {'validators': []},
                        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # 'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                {
                    'username': 'Name me is not valid'
                })
        # match = re.fullmatch(r'^[\w.@+-]+\z', str(value))
        match = re.fullmatch(r'^[\w.@+-]+', str(value))
        if match is None:
            raise serializers.ValidationError('Invalid symbols')
        return value

    # def validate_last_name(self, value):
    #     if len(value) > 150:
    #         raise serializers.ValidationError('Bad lastname')
    #     return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('slug',)
        extra_kwargs = {'slug': {'validators': []},
                        }


# class TitleSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(slug_field='slug',
#                                             queryset=Category.objects.all())
#     genre = GenreSerializer(many=True)

#     class Meta:
#         model = Title
#         fields = [
#             'id',
#             'name',
#             'year',
#             'descriptions',
#             'genre',
#             'category'
#         ]

#     def validate_year(self, value):
#         if value > datetime.today().year:
#             raise serializers.ValidationError('Invalid year')
#         return value

#         # def validate(self, data):
#         #     if data['year'] > datetime.today().year:
#         #         raise serializers.ValidationError('Invalid year')
#         #     return data

#     def create(self, validated_data):
#         genres = validated_data.pop('genre')
#         for genre in genres:
#             if (Genre.objects.filter(slug=genre.get("slug")).exists()
#                 is False):
#                 raise serializers.ValidationError(
#                     f'Genre {genre["slug"]} does not exist')
#         title = Title.objects.create(**validated_data)
#         for genre in genres:
#             current_genre = Genre.objects.get(slug=genre.get("slug"))
#             GenreTitle.objects.create(title=title, genre=current_genre)
#         return title

#     def update(self, instanse, validated_data):
#         if instanse.name != validated_data.get("name"):
#             raise serializers.ValidationError(
#                 'Title name must not change!')
#         genres = validated_data.pop('genre')
#         for genre in genres:
#             if (Genre.objects.filter(slug=genre.get("slug")).exists()
#                 is False):
#                 raise serializers.ValidationError(
#                     f'Genre {genre["slug"]} does not exist')
#         # instanse.name = validated_data.get("name", instanse.name)
#         instanse.year = validated_data.get("year", instanse.year)
#         instanse.descriptions = validated_data.get("descriptions",
#                                                    instanse.descriptions)
#         instanse.category = validated_data.get("category", instanse.category)
#         GenreTitle.objects.filter(title=instanse.id).delete()
#         for genre in genres:
#             current_genre = Genre.objects.get(slug=genre.get("slug"))
#             current_title = Title.objects.get(name=instanse.name)
#             GenreTitle.objects.create(title=current_title,
#                                       genre=current_genre)
#         instanse.save()
#         return instanse


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category', 'description')

    def to_representation(self, title):
        serializer = ReadTitleSerializer(title)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    # titles = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', )
        # fields = ('name', 'slug', 'titles')

    def validate_slug(self, value):
        match = re.fullmatch(r'^[-a-zA-Z0-9_]+$', str(value))
        if match is None:
            raise serializers.ValidationError('Invalid symbols in name')
        return value


class GenreViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug', )

    def validate_slug(self, value):
        match = re.fullmatch(r'^[-a-zA-Z0-9_]+$', str(value))
        if match is None:
            raise serializers.ValidationError('Invalid symbols in name')
        return value


class ReadTitleSerializer(serializers.ModelSerializer):
    # rating = serializers.IntegerField(source='reviews__score__avg',
    #                                   read_only=True)
    rating = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(read_only=True,
    #                                          slug_field='slug')
    category = CategorySerializer(read_only=True)
    genre = GenreViewSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        ]

    def get_rating(self, obj):
        rate = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return rate.get('score__avg')
        # reviews = Review.objects.annotate(Avg('score'))
        # return reviews.filter(title=obj.id).score__avg
        # titles = Title.objects.all().annotate(
        #          Avg('reviews__score'))
        # return titles.filter(id=obj.id).reviews__score__avg


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title', )
        read_only_fields = ('author', 'title', )

    def validate(self, data):
        if self.context.get('request').method == "POST":
            author_review = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                    author=author_review,
                    title=title_id).exists():
                raise serializers.ValidationError('Review already exists.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review', )
        read_only_fields = ('author', 'review', )
