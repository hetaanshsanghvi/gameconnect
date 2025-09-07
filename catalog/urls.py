from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
	path("", views.home, name="home"),
	path("favorites/", views.favorites_list, name="favorites"),
	path("game/<int:game_id>/", views.game_detail, name="game_detail"),
	path("game/<int:game_id>/toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
	path("signup/", views.signup, name="signup"),
	path("logout/", views.logout_view, name="logout"),
]


