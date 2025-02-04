#!/usr/bin/env python3
"""
ImageFlow - A simple image processing tool
"""

import click
import os
from PIL import Image

@click.group()
def cli():
    """ImageFlow - Batch image processing tool"""
    pass

@cli.command()
@click.argument('input_path')
@click.option('--width', '-w', type=int, help='Target width')
@click.option('--height', '-h', type=int, help='Target height')
@click.option('--output', '-o', help='Output file path')
def resize(input_path, width, height, output):
    """Resize an image"""
    if not os.path.exists(input_path):
        click.echo(f"Error: File {input_path} not found")
        return

    if not width and not height:
        click.echo("Error: Must specify at least width or height")
        return

    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size

            if width and height:
                new_size = (width, height)
            elif width:
                ratio = width / original_width
                new_size = (width, int(original_height * ratio))
            else:
                ratio = height / original_height
                new_size = (int(original_width * ratio), height)

            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

            if not output:
                name, ext = os.path.splitext(input_path)
                output = f"{name}_resized{ext}"

            resized_img.save(output)
            click.echo(f"Resized {input_path} to {new_size[0]}x{new_size[1]} -> {output}")

    except Exception as e:
        click.echo(f"Error processing {input_path}: {e}")

@cli.command()
def version():
    """Show version info"""
    click.echo("ImageFlow v0.1.0")

if __name__ == '__main__':
    cli()