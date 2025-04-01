#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone
import requests
import svgwrite
import random

def get_contribution_data(username):
    """Get contribution data from GitHub API"""
    url = f"https://api.github.com/users/{username}/events"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Contribution-Snake"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def create_snake_svg(contributions, is_dark=False):
    """Create snake SVG from contribution data"""
    width = 800
    height = 400
    background_color = "#0d1117" if is_dark else "#ffffff"
    grid_color = "#30363d" if is_dark else "#eaeef2"
    text_color = "#ffffff" if is_dark else "#000000"
    
    # Create SVG drawing
    filename = "snake-dark.svg" if is_dark else "snake.svg"
    dwg = svgwrite.Drawing(filename, size=(width, height))
    
    # Add background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=background_color))
    
    # Draw grid
    for x in range(0, width, 10):
        dwg.add(dwg.line(start=(x, 0), end=(x, height), stroke=grid_color, stroke_width=1))
    for y in range(0, height, 10):
        dwg.add(dwg.line(start=(0, y), end=(width, y), stroke=grid_color, stroke_width=1))
    
    # Draw snake
    snake_color = "#2ea043"  # GitHub green
    x, y = 50, 50
    for contribution in contributions:
        dwg.add(dwg.rect(insert=(x, y), size=(8, 8), fill=snake_color))
        x += 10
        if x >= width - 50:
            x = 50
            y += 10
    
    # Add text
    text = f"GitHub Contribution Snake - {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    dwg.add(dwg.text(text, insert=(10, height-10), fill=text_color, font_size=20))
    
    return dwg

def main():
    username = "Shivakarthikeya23"
    contributions = get_contribution_data(username)
    
    # Create light theme snake
    light_snake = create_snake_svg(contributions, is_dark=False)
    light_snake.save()
    
    # Create dark theme snake
    dark_snake = create_snake_svg(contributions, is_dark=True)
    dark_snake.save()

if __name__ == "__main__":
    main() 