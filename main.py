# lilypond_generator.py

"""
This script generates a combined LilyPond (.ly) file containing specified scales.
It automatically compiles the LilyPond file into a centered PDF and a MIDI file
using the LilyPond command-line tool. Users can specify the key, scale types,
and number of octaves. Existing output files are deleted before generating new
ones to ensure consistency.
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
SCALE_TYPES = ["major", "harmonic_minor"]

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

def generate_lilypond(filename, scales, key, octaves):
    """
    Generates a LilyPond file containing multiple scales.
    
    Args:
        filename (str): The filename for the LilyPond (.ly) file.
        scales (list): List of scale types to include.
        key (str): The key for the scales.
        octaves (int): Number of octaves.
    """
    # Define the header with metadata
    scale_titles = ' and '.join([scale.replace('_', ' ').title() for scale in scales])
    header = f"""
\\version "2.22.0"  % Specify the LilyPond version

\\header {{
  title = "Scales: {scale_titles} in {key.capitalize()}"
  composer = "Traditional"
}}
"""

    # Define the paper settings to center the music and fit on one page
    paper = r"""
\paper {
  top-margin = 1.5\cm
  bottom-margin = 1.5\cm
  left-margin = 2\cm
  right-margin = 2\cm
  indent = 0
  system-count = 1  % Force single system
  line-width = 16\cm  % Adjust line width as needed
}
"""

    # Initialize the music variable
    music = ""

    # Generate each scale's notes and add to the music variable
    for i, scale_type in enumerate(scales):
        notes = generate_scale_notes(key, scale_type, octaves)
        relative_pitch = "c'"  # Starting pitch

        # Define the key signature
        if scale_type in ["minor", "harmonic_minor"]:
            key_signature = f"\\key {key.lower()} \\minor"
        else:
            key_signature = f"\\key {key.lower()} \\major"

        # Define a separate Staff for each scale
        staff = f"""
\\new Staff {{
  \\relative {relative_pitch} {{
    {key_signature}
    \\time 4/4

    {notes}
  }}
}}
"""
        music += staff

    # Define the score with layout settings to center the music
    score = f"""
\\score {{
  <<
    {music}
  >>

  \\layout {{
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }}
  \\midi {{ }}
}}
"""

    # Combine header, paper, and score
    lilypond_content = header + "\n" + paper + "\n" + score

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
    ly_filename = "output_scales.ly"
    pdf_filename = "output_scales.pdf"
    midi_filename = "output_scales.midi"

    # Delete existing output files
    files_to_delete = [ly_filename, pdf_filename, midi_filename]
    delete_existing_files(files_to_delete)

    # Generate and compile the combined LilyPond file
    print(f"Generating scales: {', '.join([s.replace('_', ' ').title() for s in scales_to_generate])}...")
    generate_lilypond(ly_filename, scales_to_generate, key, octaves)

    print("All scales have been generated successfully.")
