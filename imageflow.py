#!/usr/bin/env python3
"""
ImageFlow - A simple image processing tool
"""

import click
import os
import glob
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
@click.argument('input_path')
@click.option('--format', '-f', required=True, help='Target format (jpg, png, webp, etc.)')
@click.option('--output', '-o', help='Output file path')
def convert(input_path, format, output):
    """Convert image format"""
    if not os.path.exists(input_path):
        click.echo(f"Error: File {input_path} not found")
        return

    try:
        with Image.open(input_path) as img:
            if not output:
                name = os.path.splitext(input_path)[0]
                output = f"{name}.{format.lower()}"

            if format.lower() == 'jpg' or format.lower() == 'jpeg':
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

            img.save(output, format=format.upper())
            click.echo(f"Converted {input_path} to {format.upper()} -> {output}")

    except Exception as e:
        click.echo(f"Error converting {input_path}: {e}")

@cli.command()
@click.argument('directory')
@click.option('--pattern', '-p', default='*', help='File pattern (e.g., *.jpg)')
@click.option('--width', '-w', type=int, help='Target width for resize')
@click.option('--height', '-h', type=int, help='Target height for resize')
@click.option('--format', '-f', help='Convert to format')
@click.option('--output-dir', '-d', help='Output directory')
def batch(directory, pattern, width, height, format, output_dir):
    """Batch process images in directory"""
    if not os.path.exists(directory):
        click.echo(f"Error: Directory {directory} not found")
        return

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    search_pattern = os.path.join(directory, pattern)
    files = glob.glob(search_pattern)

    if not files:
        click.echo(f"No files found matching {search_pattern}")
        return

    processed = 0
    for file_path in files:
        try:
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                continue

            with Image.open(file_path) as img:
                result_img = img.copy()

                if width or height:
                    original_width, original_height = img.size
                    if width and height:
                        new_size = (width, height)
                    elif width:
                        ratio = width / original_width
                        new_size = (width, int(original_height * ratio))
                    else:
                        ratio = height / original_height
                        new_size = (int(original_width * ratio), height)

                    result_img = result_img.resize(new_size, Image.Resampling.LANCZOS)

                filename = os.path.basename(file_path)
                name, ext = os.path.splitext(filename)

                if format:
                    ext = f".{format.lower()}"
                    if format.lower() in ('jpg', 'jpeg') and result_img.mode in ('RGBA', 'LA', 'P'):
                        result_img = result_img.convert('RGB')

                if output_dir:
                    output_path = os.path.join(output_dir, f"{name}_processed{ext}")
                else:
                    output_path = os.path.join(directory, f"{name}_processed{ext}")

                result_img.save(output_path)
                processed += 1
                click.echo(f"Processed: {filename} -> {os.path.basename(output_path)}")

        except Exception as e:
            click.echo(f"Error processing {file_path}: {e}")

    click.echo(f"Batch processing complete. Processed {processed} files.")

@cli.command()
@click.argument('input_path')
def info(input_path):
    """Show image information"""
    if not os.path.exists(input_path):
        click.echo(f"Error: File {input_path} not found")
        return

    try:
        with Image.open(input_path) as img:
            click.echo(f"File: {input_path}")
            click.echo(f"Format: {img.format}")
            click.echo(f"Mode: {img.mode}")
            click.echo(f"Size: {img.size[0]}x{img.size[1]}")

            if hasattr(img, '_getexif') and img._getexif():
                click.echo("EXIF data: Present")
            else:
                click.echo("EXIF data: None")

    except Exception as e:
        click.echo(f"Error reading {input_path}: {e}")

@cli.command()
def version():
    """Show version info"""
    click.echo("ImageFlow v0.1.0")

if __name__ == '__main__':
    cli()