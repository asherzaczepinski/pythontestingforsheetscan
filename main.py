# lilypond_generator.py

"""
This script generates separate LilyPond (.ly) files for specified scales,
compiles each into a centered PDF and a MIDI file using the LilyPond
command-line tool, converts the PDFs to PNG images using ImageMagick or pdf2image,
and finally combines selected scale PNGs into a single image with descriptive text.
Existing output files are deleted before generating new ones to ensure consistency.
Each scale is placed in its own file with an appropriate title.
"""

import subprocess
import sys
import os
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

# Define the scale intervals for different scale types
SCALE_INTERVALS = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2],          # Natural Minor
    "harmonic_minor": [2, 1, 2, 2, 1, 3, 1] # Harmonic Minor
}

# Define all possible notes including sharps and flats
NOTE_ORDER = ['c', 'c#', 'd', 'd#', 'e', 'f',
             'f#', 'g', 'g#', 'a', 'a#', 'b']

# List of scale types to generate
SCALE_TYPES = ["major", "harmonic_minor"]  # Modified to include only major and harmonic_minor

def get_note_index(note):
    """
    Retrieves the index of the note in the NOTE_ORDER list.
    Handles both sharps (#) and flats (b).
    """
    enharmonic = {
        'db': 'c#',
        'eb': 'd#',
        'gb': 'f#',
        'ab': 'g#',
        'bb': 'a#',
        'cb': 'b',
        'fb': 'e'
    }
    note = note.lower()
    if note in NOTE_ORDER:
        return NOTE_ORDER.index(note)
    elif note in enharmonic:
        return NOTE_ORDER.index(enharmonic[note])
    else:
        print(f"Warning: Note '{note}' is not recognized. Defaulting to 'c'.")
        return NOTE_ORDER.index('c')

def next_note(current_note, interval):
    """
    Calculates the next note in the scale based on the interval.
    """
    index = get_note_index(current_note)
    next_index = (index + interval) % len(NOTE_ORDER)
    return NOTE_ORDER[next_index]

def generate_scale_notes(key, scale_type, octaves):
    """
    Generates a scale based on the key, scale type, and number of octaves.
    
    Args:
        key (str): The key for the scale (e.g., 'c', 'g#', 'eb').
        scale_type (str): The type of scale ('major', 'minor', 'harmonic_minor').
        octaves (int): Number of octaves (1 to 4).
    
    Returns:
        str: LilyPond-formatted notes representing the scale.
    """
    if scale_type not in SCALE_INTERVALS:
        print(f"Error: Scale type '{scale_type}' is not supported.")
        sys.exit(1)
    
    intervals = SCALE_INTERVALS[scale_type]
    current_note = key.lower()
    scale = [current_note]
    
    # Generate one octave first
    for interval in intervals:
        current_note = next_note(current_note, interval)
        scale.append(current_note)
    
    # Repeat the scale for the specified number of octaves
    full_scale = scale.copy()
    for _ in range(1, octaves):
        # Start from the last note of the previous scale
        starting_note = scale[-1]
        for interval in intervals:
            starting_note = next_note(starting_note, interval)
            full_scale.append(starting_note)
    
    # For descending scale, exclude the last note to avoid repetition
    descending_scale = full_scale[::-1][1:]
    
    # Combine ascending and descending scales
    combined_scale = full_scale + descending_scale
    
    # Assign rhythmic values (quarter notes)
    notes_with_rhythm = ' '.join([f"{note}4" for note in combined_scale])
    
    return notes_with_rhythm

def delete_existing_files(filenames):
    """
    Deletes existing files if they exist.
    
    Args:
        filenames (list): List of filenames to delete.
    """
    for filename in filenames:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"Deleted existing file: {filename}")
            except Exception as e:
                print(f"Error deleting file '{filename}': {e}")
                sys.exit(1)

def generate_lilypond(filename, scale_type, key, octaves):
    """
    Generates a LilyPond file for a specific scale type.

    Args:
        filename (str): The filename for the LilyPond (.ly) file.
        scale_type (str): The type of scale ('major', 'minor', 'harmonic_minor').
        key (str): The key for the scale.
        octaves (int): Number of octaves.
    """
    # Define the LilyPond version
    version = '\\version "2.22.0"  % Specify the LilyPond version\n\n'

    # Define the paper settings to center the music and fit on one page per score
    paper = r"""
\paper {
  top-margin = 1.5\cm
  bottom-margin = 1.5\cm
  left-margin = 2\cm
  right-margin = 2\cm
  indent = 0
  line-width = 16\cm  % Adjust line width as needed
}
"""

    # Start building the LilyPond content
    lilypond_content = version + paper + "\n\\score {\n"

    # Generate the scale
    scale_title = f"{scale_type.replace('_', ' ').title()} Scale in {key.capitalize()}"
    notes = generate_scale_notes(key, scale_type, octaves)
    relative_pitch = "c'"  # Starting pitch

    # Define the key signature
    if scale_type in ["minor", "harmonic_minor"]:
        key_signature = f"\\key {key.lower()} \\minor"
    else:
        key_signature = f"\\key {key.lower()} \\major"

    # Create the \score block for the current scale
    score = f"""
  \\header {{
    title = "{scale_title}"
    composer = "Traditional"
  }}
  
  \\new Staff {{
    \\relative {relative_pitch} {{
      {key_signature}
      \\time 4/4

      {notes}
    }}
  }}

  \\layout {{
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }}
  \\midi {{ }}
}}
"""

    lilypond_content += score

    # Close the score
    lilypond_content += "\n"

    # Write the content to the specified file
    try:
        with open(filename, 'w') as file:
            file.write(lilypond_content)
        print(f"LilyPond file '{filename}' has been generated successfully.")
    except IOError as e:
        print(f"Error writing to file '{filename}': {e}")
        sys.exit(1)

    # Compile the LilyPond file
    try:
        print(f"Compiling the LilyPond file '{filename}'...")
        subprocess.run(['lilypond', filename], check=True)
        base_filename = os.path.splitext(filename)[0]
        pdf_filename = f"{base_filename}.pdf"
        midi_filename = f"{base_filename}.midi"
        print(f"Compilation successful. Generated '{pdf_filename}' and '{midi_filename}'.\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while compiling '{filename}': {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: LilyPond is not installed or not found in PATH.")
        sys.exit(1)

    return base_filename  # Return base name for further processing

def convert_pdf_to_png(pdf_file, png_file):
    """
    Converts a PDF file to a PNG image using ImageMagick.

    Args:
        pdf_file (str): The source PDF filename.
        png_file (str): The target PNG filename.
    """
    try:
        print(f"Converting '{pdf_file}' to '{png_file}' using ImageMagick...")
        subprocess.run(['convert', '-density', '300', pdf_file, '-quality', '90', png_file], check=True)
        print(f"Conversion successful. Generated '{png_file}'.\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting '{pdf_file}' to PNG: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: ImageMagick's 'convert' command is not installed or not found in PATH.")
        sys.exit(1)

def convert_pdf_to_png_using_pdf2image(pdf_file, png_file):
    """
    Converts a PDF file to a PNG image using pdf2image.

    Args:
        pdf_file (str): The source PDF filename.
        png_file (str): The target PNG filename.
    """
    try:
        print(f"Converting '{pdf_file}' to '{png_file}' using pdf2image...")
        images = convert_from_path(pdf_file, dpi=300)
        # Save the first page as PNG
        if images:
            images[0].save(png_file, 'PNG')
            print(f"Conversion successful. Generated '{png_file}'.\n")
        else:
            print(f"No pages found in '{pdf_file}'.")
    except Exception as e:
        print(f"An error occurred while converting '{pdf_file}' to PNG: {e}")
        sys.exit(1)

def find_lowest_black_pixel(image_path):
    """
    Finds the y-coordinate of the lowest black pixel in the image.

    Args:
        image_path (str): Path to the PNG image.

    Returns:
        int: Y-coordinate of the lowest black pixel. Returns image height if no black pixels are found.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert('L')  # Convert to grayscale
            width, height = img.size
            pixels = img.load()

            for y in range(height-1, -1, -1):
                for x in range(width):
                    if pixels[x, y] < 10:  # Threshold for black pixel
                        return y
            return height  # If no black pixels found
    except Exception as e:
        print(f"Error processing image '{image_path}': {e}")
        sys.exit(1)

def combine_images_with_text(image1_path, image2_path, output_path, text):
    """
    Combines two images side by side, aligned based on their lowest black pixels,
    and adds descriptive text below.

    Args:
        image1_path (str): Path to the first PNG image.
        image2_path (str): Path to the second PNG image.
        output_path (str): Path to save the combined PNG image.
        text (str): Descriptive text to add below the images.
    """
    try:
        # Open images
        img1 = Image.open(image1_path).convert("RGBA")
        img2 = Image.open(image2_path).convert("RGBA")

        # Find lowest black pixels
        img1_lowest = find_lowest_black_pixel(image1_path)
        img2_lowest = find_lowest_black_pixel(image2_path)

        # Calculate the y-offsets to align the images based on lowest black pixel
        img1_offset_y = img1.size[1] - img1_lowest
        img2_offset_y = img2.size[1] - img2_lowest
        max_offset = max(img1_offset_y, img2_offset_y)

        # Calculate new image height
        combined_height = max(img1.size[1] + (max_offset - img1_offset_y),
                             img2.size[1] + (max_offset - img2_offset_y)) + 100  # Extra space for text

        # Calculate new image width
        combined_width = img1.size[0] + img2.size[0] + 50  # Space between images

        # Create a new blank image
        combined_img = Image.new('RGBA', (combined_width, combined_height), 'white')

        # Paste img1
        paste_x1 = 0
        paste_y1 = combined_height - (img1.size[1] + (max_offset - img1_offset_y)) - 100  # Leave space for text
        combined_img.paste(img1, (paste_x1, paste_y1), img1)

        # Paste img2
        paste_x2 = img1.size[0] + 50  # 50 pixels space between images
        paste_y2 = combined_height - (img2.size[1] + (max_offset - img2_offset_y)) - 100
        combined_img.paste(img2, (paste_x2, paste_y2), img2)

        # Add text
        draw = ImageDraw.Draw(combined_img)
        try:
            # Try to use a TrueType font
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            # If the font is not found, use the default font
            font = ImageFont.load_default()

        text_width, text_height = draw.textsize(text, font=font)
        text_position = ((combined_width - text_width) // 2, combined_height - 80)  # 80 pixels from bottom
        draw.text(text_position, text, fill="black", font=font)

        # Save the combined image
        combined_img = combined_img.convert("RGB")  # Remove alpha for saving as JPEG or PNG
        combined_img.save(output_path)
        print(f"Combined image saved as '{output_path}'.\n")
    except Exception as e:
        print(f"Error combining images: {e}")
        sys.exit(1)

def delete_existing_output_files(scale_types):
    """
    Deletes existing output files based on the scale types.

    Args:
        scale_types (list): List of scale types.
    """
    existing_files = []
    for scale_type in scale_types:
        base = f"{scale_type}_scale"
        existing_files.extend([
            f"{base}.ly",
            f"{base}.pdf",
            f"{base}.midi",
            f"{base}.png"
        ])
    # Add combined image files
    existing_files.append("combined_scales.png")
    delete_existing_files(existing_files)

if __name__ == "__main__":
    # User-defined variables
    key = "c"                 # Change this to your desired key (e.g., 'c', 'g#', 'eb')
    octaves = 2               # Number of octaves (1, 2, 3, or 4)

    # Validate octaves input
    if not isinstance(octaves, int) or not (1 <= octaves <= 4):
        print("Error: Number of octaves must be an integer between 1 and 4.")
        sys.exit(1)

    # Prepare list of scale types to generate
    scales_to_generate = SCALE_TYPES

    # Delete existing output files
    delete_existing_output_files(scales_to_generate)

    # Generate, compile, and convert each scale
    for scale_type in scales_to_generate:
        base_filename = f"{scale_type}_scale"
        ly_filename = f"{base_filename}.ly"
        # Generate the LilyPond file
        print(f"Generating {scale_type.replace('_', ' ').title()} Scale...")
        base = generate_lilypond(ly_filename, scale_type, key, octaves)
        
        # Convert the generated PDF to PNG
        pdf_filename = f"{base}.pdf"
        png_filename = f"{base}.png"

        # Choose conversion method: ImageMagick or pdf2image
        # Uncomment one of the following lines based on your preference

        # Using ImageMagick's convert
        convert_pdf_to_png(pdf_filename, png_filename)

        # Using pdf2image (comment out if using ImageMagick)
        # convert_pdf_to_png_using_pdf2image(pdf_filename, png_filename)

    # Combine Major and Harmonic Minor scales into a single image with description
    combined_image_path = "combined_scales.png"
    major_png = "major_scale.png"
    harmonic_minor_png = "harmonic_minor_scale.png"

    # Check if both PNG files exist
    if not (os.path.exists(major_png) and os.path.exists(harmonic_minor_png)):
        print(f"Error: Required PNG files '{major_png}' and/or '{harmonic_minor_png}' not found.")
        sys.exit(1)

    # Define descriptive text
    description_text = (
        "Comparison of Major Scale and Harmonic Minor Scale\n"
        "The Major scale has a bright and happy sound, while the Harmonic Minor scale introduces a distinctive, exotic flavor due to its augmented second."
    )

    # Combine the images with text
    combine_images_with_text(major_png, harmonic_minor_png, combined_image_path, description_text)

    print("All scales have been generated, compiled, converted, and combined successfully.")
