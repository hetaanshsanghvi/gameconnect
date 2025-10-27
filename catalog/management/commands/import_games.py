from django.core.management.base import BaseCommand
from catalog.models import Game, Category
import re


class Command(BaseCommand):
	help = 'Import games from games.txt file'

	def handle(self, *args, **options):
		# Parse the games.txt file
		games_data = self.parse_games_file('games.txt')
		
		# Delete existing data
		Game.objects.all().delete()
		Category.objects.all().delete()
		
		# Get unique categories
		categories = list(set([game['category'] for game in games_data]))
		
		# Create categories
		category_objects = {}
		for category in categories:
			cat, created = Category.objects.get_or_create(name=category)
			category_objects[category] = cat
			self.stdout.write(self.style.SUCCESS(f'Created category: {category}'))
		
		# Create games with IDs starting from 1
		created_count = 0
		for idx, game_data in enumerate(games_data, start=1):
			category = category_objects[game_data['category']]
			
			game = Game(
				id=idx,  # Set the ID explicitly
				title=game_data['title'],
				description=game_data['description'],
				category=category,
				tags=game_data['tags'],
				external_url=game_data['external_url'],
				thumbnail=game_data['thumbnail'] if game_data['thumbnail'] else None
			)
			game.save()
			created_count += 1
		
		self.stdout.write(self.style.SUCCESS(f'\nSuccessfully imported {created_count} games!'))
	
	def parse_games_file(self, filename):
		games = []
		
		try:
			with open(filename, 'r', encoding='utf-8') as file:
				lines = file.readlines()
		
			for line in lines:
				# Skip header and empty lines
				if '| ID |' in line or '| ---' in line or '+-' in line or not line.strip():
					continue
				
				# Match the pipe-separated format
				pattern = r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
				match = re.match(pattern, line)
				
				if match:
					game_id, title, description, category, tags, external_url, thumbnail = match.groups()
					
					# Clean up the extracted values
					title = title.strip()
					description = description.strip()
					category = category.strip()
					tags = tags.strip()
					external_url = external_url.strip()
					thumbnail = thumbnail.strip()
					
					# Handle NULL values
					if thumbnail == 'NULL':
						thumbnail = ''
					if external_url == 'NULL' or 'NULL' in external_url:
						external_url = ''
					
					# Extract just the filename from thumbnail path and add thumbnails/ prefix
					if thumbnail and '/' in thumbnail:
						# Get the filename only
						filename = thumbnail.split('/')[-1]
						# Add thumbnails/ prefix to match upload_to directory
						thumbnail = f'thumbnails/{filename}'
					elif thumbnail and thumbnail != '':
						# If no path, assume it's in thumbnails folder
						thumbnail = f'thumbnails/{thumbnail}'
					
					games.append({
						'id': int(game_id),
						'title': title,
						'description': description,
						'category': category,
						'tags': tags,
						'external_url': external_url,
						'thumbnail': thumbnail
					})
		
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'Error reading file: {str(e)}'))
		
		return games

