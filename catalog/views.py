from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login

from .models import Game, Category, Favorite
from .forms import SignUpForm


def home(request):
	query = request.GET.get("q", "").strip()
	category_id = request.GET.get("category")
	sort = request.GET.get("sort", "newest")

	games = Game.objects.all()
	if query:
		games = games.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query))
	if category_id:
		games = games.filter(category_id=category_id)
	if sort == "newest":
		games = games.order_by("-created_at")

	categories = Category.objects.all().order_by("name")
	context = {
		"games": games,
		"categories": categories,
		"selected_category": int(category_id) if category_id else None,
		"query": query,
		"sort": sort,
	}
	return render(request, "catalog/home.html", context)


def game_detail(request, game_id: int):
	game = get_object_or_404(Game, id=game_id)
	is_favorite = False
	if request.user.is_authenticated:
		is_favorite = Favorite.objects.filter(user=request.user, game=game).exists()
	return render(request, "catalog/game_detail.html", {"game": game, "is_favorite": is_favorite})


@login_required
def toggle_favorite(request, game_id: int):
	game = get_object_or_404(Game, id=game_id)
	fav, created = Favorite.objects.get_or_create(user=request.user, game=game)
	if created:
		messages.success(request, "Added to favorites")
	else:
		fav.delete()
		messages.info(request, "Removed from favorites")
	return redirect("catalog:game_detail", game_id=game.id)


@login_required
def favorites_list(request):
	favorites = Favorite.objects.filter(user=request.user).select_related("game")
	return render(request, "catalog/favorites.html", {"favorites": favorites})


def signup(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("home")
	else:
		form = SignUpForm()
	return render(request, "registration/signup.html", {"form": form})


def logout_view(request):
	from django.contrib.auth import logout
	logout(request)
	return redirect("home")

# Create your views here.
