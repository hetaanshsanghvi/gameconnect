from django.contrib import admin
from .models import Category, Game, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "category", "created_at")
	list_filter = ("category",)
	search_fields = ("title", "tags")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "game", "created_at")
	list_filter = ("user", "game")

# Register your models here.
