from django.contrib import admin
from .models import Category, Game, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "category", "has_game_file", "has_external_url", "created_at")
	list_filter = ("category",)
	search_fields = ("title", "tags")
	fields = ("title", "description", "thumbnail", "category", "tags", "external_url", "game_file")
	
	def has_game_file(self, obj):
		return bool(obj.game_file)
	has_game_file.boolean = True
	has_game_file.short_description = "Has Game File"
	
	def has_external_url(self, obj):
		return bool(obj.external_url)
	has_external_url.boolean = True
	has_external_url.short_description = "Has External URL"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "game", "created_at")
	list_filter = ("user", "game")

# Register your models here.
