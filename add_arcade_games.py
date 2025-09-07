#!/usr/bin/env python
"""
Script to add arcade games to the GameHub database
Run this from the project directory: python add_arcade_games.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()

from catalog.models import Category, Game

def add_arcade_games():
    """Add arcade games to the database"""
    
    # Get or create the Arcade category
    arcade_category, created = Category.objects.get_or_create(
        name="Arcade",
        defaults={'name': 'Arcade'}
    )
    
    if created:
        print(f"✅ Created new category: {arcade_category.name}")
    else:
        print(f"✅ Using existing category: {arcade_category.name}")
    
    # Define arcade games
    arcade_games = [
        {
            'title': 'Snake Game',
            'description': 'Classic snake game where you control a snake to eat food and grow longer. Avoid hitting walls or yourself!',
            'tags': 'snake, classic, arcade, retro',
            'external_url': 'https://playsnake.org/',
            'thumbnail': None  # You can add image files later
        },
        {
            'title': 'Tetris',
            'description': 'The iconic falling block puzzle game. Arrange falling tetrominoes to create complete lines and score points.',
            'tags': 'tetris, puzzle, blocks, classic',
            'external_url': 'https://tetris.com/play-tetris',
            'thumbnail': None
        },
        {
            'title': 'Pac-Man',
            'description': 'Navigate Pac-Man through a maze, eating dots while avoiding ghosts. Power pellets let you eat the ghosts!',
            'tags': 'pac-man, maze, ghosts, classic',
            'external_url': 'https://www.google.com/logos/2010/pacman10-i.html',
            'thumbnail': None
        },
        {
            'title': 'Space Invaders',
            'description': 'Defend Earth from invading aliens in this classic arcade shooter. Move left and right while shooting upward.',
            'tags': 'space, invaders, shooter, retro',
            'external_url': 'https://www.classicgamesarcade.com/game/215/space-invaders.html',
            'thumbnail': None
        },
        {
            'title': 'Pong',
            'description': 'The first video game ever! Simple two-player tennis game with paddles and a bouncing ball.',
            'tags': 'pong, tennis, classic, first-game',
            'external_url': 'https://www.ponggame.org/',
            'thumbnail': None
        },
        {
            'title': 'Breakout',
            'description': 'Break all the bricks with a bouncing ball and paddle. Don\'t let the ball fall below the paddle!',
            'tags': 'breakout, bricks, paddle, arcade',
            'external_url': 'https://www.classicgamesarcade.com/game/218/breakout.html',
            'thumbnail': None
        },
        {
            'title': 'Asteroids',
            'description': 'Navigate a spaceship through an asteroid field, shooting asteroids and avoiding collisions.',
            'tags': 'asteroids, space, shooter, vector',
            'external_url': 'https://www.classicgamesarcade.com/game/216/asteroids.html',
            'thumbnail': None
        },
        {
            'title': 'Donkey Kong',
            'description': 'Help Jumpman rescue Pauline from Donkey Kong by climbing ladders and avoiding barrels.',
            'tags': 'donkey-kong, platformer, classic, nintendo',
            'external_url': 'https://www.classicgamesarcade.com/game/217/donkey-kong.html',
            'thumbnail': None
        }
    ]
    
    # Add games to database
    added_count = 0
    for game_data in arcade_games:
        game, created = Game.objects.get_or_create(
            title=game_data['title'],
            defaults={
                'description': game_data['description'],
                'category': arcade_category,
                'tags': game_data['tags'],
                'external_url': game_data['external_url'],
                'thumbnail': game_data['thumbnail']
            }
        )
        
        if created:
            print(f"✅ Added: {game.title}")
            added_count += 1
        else:
            print(f"⏭️  Skipped (already exists): {game.title}")
    
    print(f"\n🎮 Added {added_count} new arcade games to the database!")
    print(f"📁 Category: {arcade_category.name}")
    print(f"🌐 Visit: http://localhost:8000/ to see your games!")

if __name__ == '__main__':
    print("🎯 Adding Arcade Games to GameHub...")
    print("=" * 50)
    
    try:
        add_arcade_games()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
