from PIL import Image
import os
import sys
from datetime import datetime

def resize_image(image_path, output_path, quality=95, target_width=None, output_format='jpg'):
    """Resize an image while maintaining aspect ratio and setting DPI to 72"""
    with Image.open(image_path) as img:
        if target_width:
            # Calculate height maintaining aspect ratio
            aspect_ratio = img.height / img.width
            target_height = int(target_width * aspect_ratio)
            
            # Resize image
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        else:
            resized_img = img
        
        # Prepare output path with correct extension
        output_base = os.path.splitext(output_path)[0]
        output_path = f"{output_base}.{output_format}"
        
        # Convert to RGB if saving as JPG (required for RGBA images)
        if output_format.lower() in ['jpg', 'jpeg'] and img.mode in ['RGBA', 'P']:
            resized_img = resized_img.convert('RGB')
        
        # Save with specified quality and 72 DPI
        resized_img.save(output_path, quality=quality, optimize=True, dpi=(72, 72))

def process_images(quality=95, width=None, format='jpg'):
    """Process all images in the images folder"""
    # Create timestamp-based output folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"resized_images_{timestamp}"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get all files from images folder
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    input_folder = "images"
    
    if not os.path.exists(input_folder):
        print(f"Error: '{input_folder}' folder not found. Please create it and add images.")
        return
    
    files = os.listdir(input_folder)
    image_files = [f for f in files if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"No images found in '{input_folder}' folder.")
        return
    
    print(f"Processing {len(image_files)} images...")
    print(f"Output format: {format.upper()}")
    
    for image_file in image_files:
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)
        
        try:
            resize_image(input_path, output_path, quality, width, format)
            print(f"Processed: {image_file}")
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
    
    print(f"\nDone! Resized images saved in '{output_folder}' folder.")

def main():
    if len(sys.argv) == 1:
        # Default: only adjust quality to 95%
        process_images()
    elif len(sys.argv) == 3:
        try:
            quality = int(sys.argv[1])
            width = int(sys.argv[2])
            
            if quality < 1 or quality > 100:
                print("Error: Quality must be between 1 and 100")
                return
            
            if width < 1:
                print("Error: Width must be greater than 0")
                return
            
            process_images(quality, width)
        except ValueError:
            print("Error: Quality and width must be valid numbers")
    elif len(sys.argv) == 4:
        try:
            quality = int(sys.argv[1])
            width = int(sys.argv[2])
            format = sys.argv[3].lower()
            
            if quality < 1 or quality > 100:
                print("Error: Quality must be between 1 and 100")
                return
            
            if width < 1:
                print("Error: Width must be greater than 0")
                return
            
            if format not in ['jpg', 'jpeg', 'png', 'webp']:
                print("Error: Format must be jpg, jpeg, png, or webp")
                return
            
            process_images(quality, width, format)
        except ValueError:
            print("Error: Quality and width must be valid numbers")
    else:
        print("Usage:")
        print("rp-resize                    # Process images with 95% quality")
        print("rp-resize 90 1200           # Process images with 90% quality and 1200px width")
        print("rp-resize 90 1200 webp      # Same as above but convert to WebP format")

if __name__ == "__main__":
    main() 