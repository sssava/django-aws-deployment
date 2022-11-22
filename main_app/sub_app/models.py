from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    @property
    def get_movie(self):
        return self.movie_set.all()


class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=50)
    image = models.ImageField(default="default.png", null=True, blank=True)
    date = models.DateField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    time = models.IntegerField()
    rating = models.FloatField()
    slug = models.SlugField(max_length=100, unique=True)
    video = models.CharField(max_length=100, blank=True, null=True)
    like = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class FavMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} | {self.movie.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_count_likes(self):
        likes = self.user.favmovie_set.all()
        total = 0
        for i in likes:
            total += 1
        return total
