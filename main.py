# lilypond_generator.py

"""
This script generates separate LilyPond (.ly) files for specified scales,
compiles each into a centered PDF and a MIDI file using the LilyPond
command-line tool, and then converts the PDFs to PNG images using ImageMagick.
Existing output files are deleted before generating new ones to ensure consistency.
Each scale is placed in its own file with an appropriate title.
"""

import subprocess
import sys
import os

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
SCALE_TYPES = ["major", "minor"]  # Modified to include only major and minor

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
        print(f"Converting '{pdf_file}' to '{png_file}'...")
        subprocess.run(['convert', '-density', '300', pdf_file, '-quality', '90', png_file], check=True)
        print(f"Conversion successful. Generated '{png_file}'.\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting '{pdf_file}' to PNG: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: ImageMagick's 'convert' command is not installed or not found in PATH.")
        sys.exit(1)

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

    # Define output filenames
    # Since we're generating separate files, we'll handle filenames within the loop

    # Delete existing output files
    # Collect all possible output filenames based on SCALE_TYPES
    existing_files = []
    for scale_type in scales_to_generate:
        base = f"{scale_type}_scale"
        existing_files.extend([
            f"{base}.ly",
            f"{base}.pdf",
            f"{base}.midi",
            f"{base}.png"
        ])
    delete_existing_files(existing_files)

    # Generate, compile, and convert each scale
    for scale_type in scales_to_generate:
        base_filename = f"{scale_type}_scale"
        ly_filename = f"{base_filename}.ly"
        # Generate the LilyPond file
        print(f"Generating {scale_type.replace('_', ' ').title()} Scale...")
        generate_lilypond(ly_filename, scale_type, key, octaves)
        
        # Convert the generated PDF to PNG
        pdf_filename = f"{base_filename}.pdf"
        png_filename = f"{base_filename}.png"
        convert_pdf_to_png(pdf_filename, png_filename)

    print("All scales have been generated, compiled, and converted successfully.")
