from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login
from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator
import os

from .models import Game, Category, Favorite
from .forms import SignUpForm


def home(request):
	query = request.GET.get("q", "").strip()
	category_id = request.GET.get("category")
	sort = request.GET.get("sort", "id")

	# Start with all games ordered by ID (ascending by default)
	games = Game.objects.all().order_by("id")
	
	# Apply search filter
	if query:
		games = games.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query))
	
	# Apply category filter
	if category_id:
		games = games.filter(category_id=category_id)
	
	# Apply sorting
	if sort == "newest":
		games = games.order_by("-created_at")
	elif sort == "id_desc":
		games = games.order_by("-id")
	else:
		games = games.order_by("id")  # Default: ascending by ID

	# Pagination: 16 games per page
	paginator = Paginator(games, 16)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	categories = Category.objects.all().order_by("name")
	context = {
		"page_obj": page_obj,
		"categories": categories,
		"category_id": category_id,
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


def about(request):
	"""About page view"""
	return render(request, "catalog/about.html")


def contact(request):
	"""Contact us page view"""
	return render(request, "catalog/contact.html")


def play_game(request, game_id: int):
	"""Serve HTML game files directly"""
	game = get_object_or_404(Game, id=game_id)
	
	# Check if game has a game file
	if not game.game_file:
		raise Http404("Game file not found")
	
	# Get the file path
	file_path = os.path.join(settings.MEDIA_ROOT, str(game.game_file))
	
	# Check if file exists
	if not os.path.exists(file_path):
		raise Http404("Game file not found on disk")
	
	# Read and serve the file
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.read()
		
		# Set appropriate content type
		response = HttpResponse(content, content_type='text/html; charset=utf-8')
		return response
	except Exception as e:
		raise Http404(f"Error reading game file: {str(e)}")

# Create your views here.
