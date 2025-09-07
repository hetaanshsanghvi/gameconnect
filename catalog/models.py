from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self) -> str:
		return self.name


class Game(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
	external_url = models.URLField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.title


class Favorite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorited_by')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'game')

	def __str__(self) -> str:
		return f"{self.user.username} → {self.game.title}"

# Create your models here.
