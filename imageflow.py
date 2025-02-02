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

    click.echo(f"Resizing {input_path}...")
    # TODO: Implement resize logic

@cli.command()
def version():
    """Show version info"""
    click.echo("ImageFlow v0.1.0")

if __name__ == '__main__':
    cli()