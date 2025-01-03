"""
This script generates a single LilyPond (.ly) file containing multiple specified scales.
It automatically compiles the LilyPond file into a centered PDF and a MIDI file
using the LilyPond command-line tool. Users can specify the key and number of octaves.
Existing output files are deleted before generating new ones to ensure consistency.
"""

import subprocess
import sys
import os

# Define the scale intervals for different scale types
SCALE_INTERVALS = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2]  # Natural Minor Scale Intervals
}

# Define note orders for sharp and flat contexts
NOTE_ORDER_SHARP = ['c', 'c#', 'd', 'd#', 'e', 'f',
                   'f#', 'g', 'g#', 'a', 'a#', 'b']

NOTE_ORDER_FLAT = ['c', 'db', 'd', 'eb', 'e', 'f',
                  'gb', 'g', 'ab', 'a', 'bb', 'b']

# Define flat keys for reference
FLAT_KEYS = ['f', 'bb', 'eb', 'ab', 'db', 'gb', 'cb']

# List of scale types to generate
SCALE_TYPES = ["major", "minor"]  # Included "minor" to generate minor scales

def get_note_index(note, note_order):
    """
    Retrieves the index of the note in the provided note_order list.
    Handles both sharps (#) and flats (b).

    Args:
        note (str): The note to find (e.g., 'c', 'd#', 'eb').
        note_order (list): The list of notes to search within.

    Returns:
        int: The index of the note in the note_order list.
    """
    enharmonic = {
        'cb': 'b',
        'fb': 'e',
        'db': 'c#',
        'eb': 'd#',
        'gb': 'f#',
        'ab': 'g#',
        'bb': 'a#'
    }
    note = note.lower()
    if note in note_order:
        return note_order.index(note)
    elif note in enharmonic and enharmonic[note] in note_order:
        return note_order.index(enharmonic[note])
    else:
        print(f"Warning: Note '{note}' is not recognized. Defaulting to 'c'.")
        return note_order.index('c')

def next_note(current_note, interval, note_order):
    """
    Calculates the next note in the scale based on the interval and note_order.

    Args:
        current_note (str): The current note.
        interval (int): The interval to move to the next note.
        note_order (list): The list of notes to use (sharp or flat).

    Returns:
        str: The next note in the scale.
    """
    index = get_note_index(current_note, note_order)
    next_index = (index + interval) % len(note_order)
    return note_order[next_index]

def generate_scale_notes(key, scale_type, octaves, note_order):
    """
    Generates a scale based on the key, scale type, number of octaves, and note_order.

    Args:
        key (str): The key for the scale (e.g., 'c', 'g#', 'eb').
        scale_type (str): The type of scale ('major', 'minor').
        octaves (int): Number of octaves (1 to 4).
        note_order (list): The list of notes to use (sharp or flat).

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
        current_note = next_note(current_note, interval, note_order)
        scale.append(current_note)

    # Repeat the scale for the specified number of octaves
    full_scale = scale.copy()
    for _ in range(1, octaves):
        # Start from the last note of the previous scale
        starting_note = scale[-1]
        for interval in intervals:
            starting_note = next_note(starting_note, interval, note_order)
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

def determine_note_order(key):
    """
    Determines whether to use sharp or flat note order based on the key.

    Args:
        key (str): The key for the scale.

    Returns:
        list: The appropriate note order list (sharp or flat).
    """
    key = key.lower()
    if key in FLAT_KEYS or 'b' in key:
        return NOTE_ORDER_FLAT
    else:
        return NOTE_ORDER_SHARP

def find_relative_minor(key):
    """
    Finds the relative minor key for a given major key.

    Args:
        key (str): The major key (e.g., 'c', 'g#', 'eb').

    Returns:
        str: The relative minor key.
    """
    # Define all possible keys with their relative minors
    relative_minors = {
        'c': 'a',
        'g': 'e',
        'd': 'b',
        'a': 'f#',
        'e': 'c#',
        'b': 'g#',
        'f#': 'd#',
        'c#': 'a#',
        'f': 'd',
        'bb': 'g',
        'eb': 'c',
        'ab': 'f',
        'db': 'bb',
        'gb': 'eb',
        'cb': 'ab'
    }

    key_lower = key.lower()
    if key_lower in relative_minors:
        return relative_minors[key_lower]
    else:
        print(f"Warning: Relative minor for key '{key}' not found. Defaulting to 'a'.")
        return 'a'  # Default relative minor

def generate_lilypond_combined(filename, key, scale_types, octaves):
    """
    Generates a single LilyPond file containing multiple scales.

    Args:
        filename (str): The filename for the LilyPond (.ly) file.
        key (str): The key for the scales.
        scale_types (list): List of scale types to include.
        octaves (int): Number of octaves.
    """
    # Determine the appropriate note order
    note_order = determine_note_order(key)

    # Define the header with global metadata
    global_header = f"""
\\version "2.22.0"  % Specify the LilyPond version

\\header {{
  title = "Practice Scales"
  composer = "Traditional"
}}

\\paper {{
  top-margin = 1.5\\cm
  bottom-margin = 1.5\\cm
  left-margin = 2\\cm
  right-margin = 2\\cm
  indent = 0
  system-count = #0  % Allow multiple systems
  line-width = 16\\cm  % Adjust line width as needed
}}
"""

    # Initialize the content with the global header
    lilypond_content = global_header + "\n"

    # Iterate over each scale type and append its section
    for scale_type in scale_types:
        if scale_type == "minor":
            # Find the relative minor key
            relative_minor_key = find_relative_minor(key)
            scale_key = relative_minor_key
            key_signature = f"\\key {key.lower()} \\major"  # Major key signature for relative minor
            mode = "Minor"
        else:
            # For major scales
            scale_key = key.lower()
            key_signature = f"\\key {scale_key} \\major"
            mode = "Major"

        # Determine the appropriate note order for the scale
        scale_note_order = determine_note_order(scale_key)

        # Generate scale notes with the correct note order
        notes = generate_scale_notes(scale_key, scale_type, octaves, scale_note_order)

        # Determine relative pitch based on the scale key
        relative_pitch = f"{scale_key}'"

        # Define the score for the current scale
        scale_score = f"""
\\markup \\column {{
  \\center-column {{
    \\bold "{scale_type.replace('_', ' ').title()} Scale in {scale_key.capitalize()} ({mode})"
  }}
}}

\\score {{
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

        # Append the current scale's score to the content
        lilypond_content += scale_score + "\n"

    # Write the combined content to the specified file
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
        print(f"Compilation successful. Generated '{os.path.splitext(filename)[0]}.pdf' and '{os.path.splitext(filename)[0]}.midi'.\n")
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

    # Define the output filenames
    ly_filename = "combined_practice.ly"
    pdf_filename = "combined_practice.pdf"
    midi_filename = "combined_practice.midi"

    # Delete existing output files
    delete_existing_files([ly_filename, pdf_filename, midi_filename])

    # Generate and compile the combined LilyPond file
    print("Generating combined practice scales...")
    generate_lilypond_combined(ly_filename, key, scales_to_generate, octaves)

    print("All scales have been generated and compiled successfully.")
