from django.core.management.base import BaseCommand
from catalog.models import Game, Category, Favorite


class Command(BaseCommand):
	help = 'Delete all games, categories, and favorites from the database'

	def add_arguments(self, parser):
		parser.add_argument(
			'--only-favorites',
			action='store_true',
			help='Only delete favorites, keep games and categories',
		)

	def handle(self, *args, **options):
		if options['only_favorites']:
			# Only delete favorites
			count = Favorite.objects.count()
			Favorite.objects.all().delete()
			self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} favorites'))
		else:
			# Delete everything
			favorites_count = Favorite.objects.count()
			games_count = Game.objects.count()
			categories_count = Category.objects.count()
			
			# Delete in order due to foreign key constraints
			Favorite.objects.all().delete()
			self.stdout.write(self.style.SUCCESS(f'Deleted {favorites_count} favorites'))
			
			Game.objects.all().delete()
			self.stdout.write(self.style.SUCCESS(f'Deleted {games_count} games'))
			
			Category.objects.all().delete()
			self.stdout.write(self.style.SUCCESS(f'Deleted {categories_count} categories'))
			
			self.stdout.write(self.style.SUCCESS('\nAll data cleared successfully!'))

