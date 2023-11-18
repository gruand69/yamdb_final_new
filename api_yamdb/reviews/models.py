from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Класс для категорий."""

    name = models.CharField(verbose_name='Название категории',
                            max_length=256)
    slug = models.SlugField(verbose_name='Идентификатор категории',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    """Класс для жанров."""

    name = models.CharField(verbose_name='Название жанра',
                            max_length=256)
    slug = models.SlugField(verbose_name='Идентификатор жанра',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    """Класс для произведений."""

    name = models.CharField(verbose_name='Название произведения',
                            max_length=256, unique=True)
    year = models.PositiveSmallIntegerField(verbose_name='Дата выхода')
    rating = models.PositiveSmallIntegerField(verbose_name='Рейтинг',
                                              null=True,
                                              default=None)
    description = models.TextField(verbose_name='Описание',
                                   null=True,
                                   blank=True)
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр',
                                   through='GenreTitle',
                                   related_name='titles')
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 null=True,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')


class GenreTitle(models.Model):
    """Класс связи жанров и произведений."""

    title = models.ForeignKey(Title,
                              verbose_name='Произведение',
                              on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre,
                              verbose_name='Жанр',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        ordering = ('id',)


class Review(models.Model):
    """Класс для озывов."""

    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                1,
                message='Оценка не может быть ниже 1'
            ),
            MaxValueValidator(
                10,
                message='Оценка не может быть выше 10'
            )
        ])
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews')

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        ordering = ('-pub_date',)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments')

    review = models.ForeignKey(
        Review,
        verbose_name='Комментарий к отзыву',
        on_delete=models.CASCADE,
        related_name='comments')

    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True)

    def __str__(self):
        return (f"{self.text[:20]} to review {self.review} "
                + f"by author {self.author}")

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ('-pub_date',)
