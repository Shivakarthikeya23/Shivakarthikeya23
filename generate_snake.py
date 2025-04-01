#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone
import requests
from PIL import Image, ImageDraw, ImageFont
import io

def get_contribution_data(username):
    """Get contribution data from GitHub API"""
    url = f"https://api.github.com/users/{username}/events"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Contribution-Snake"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def create_snake_image(contributions, is_dark=False):
    """Create snake image from contribution data"""
    width = 800
    height = 400
    background_color = (13, 17, 23) if is_dark else (255, 255, 255)
    grid_color = (48, 54, 61) if is_dark else (234, 238, 242)
    text_color = (255, 255, 255) if is_dark else (0, 0, 0)
    
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # Draw grid
    for x in range(0, width, 10):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 10):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
    
    # Draw snake
    snake_color = (46, 160, 67)  # GitHub green
    x, y = 50, 50
    for contribution in contributions:
        draw.rectangle([(x, y), (x+8, y+8)], fill=snake_color)
        x += 10
        if x >= width - 50:
            x = 50
            y += 10
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = f"GitHub Contribution Snake - {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    draw.text((10, height-30), text, font=font, fill=text_color)
    
    return img

def main():
    username = "Shivakarthikeya23"
    contributions = get_contribution_data(username)
    
    # Create light theme snake
    light_snake = create_snake_image(contributions, is_dark=False)
    light_snake.save("snake.svg", "SVG")
    
    # Create dark theme snake
    dark_snake = create_snake_image(contributions, is_dark=True)
    dark_snake.save("snake-dark.svg", "SVG")

if __name__ == "__main__":
    main() 