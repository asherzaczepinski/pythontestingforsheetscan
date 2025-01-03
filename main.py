"""
This script generates a single LilyPond (.ly) file containing multiple specified scales.
It automatically compiles the LilyPond file into a centered PDF and a MIDI file
using the LilyPond command-line tool. Users can specify the key and number of octaves.
Existing output files are deleted before generating new ones to ensure consistency.
"""

import subprocess
import sys
import os
import re

def generate_and_compile_scales(key, octaves):
    """
    Generates multiple scales in LilyPond format based on the specified key and number of octaves.
    Compiles the LilyPond file into PDF and MIDI formats.

    Args:
        key (str): The root note of the scale (e.g., 'c', 'g#', 'eb').
        octaves (int): The number of octaves to generate (1 to 4).

    Raises:
        SystemExit: If any errors occur during file operations or compilation.
    """

    # Define the scale intervals for different scale types
    SCALE_INTERVALS = {
        "major": [2, 2, 1, 2, 2, 2, 1],
        "minor": [2, 1, 2, 2, 1, 2, 2]  # Natural Minor Scale
    }

    # Define note orders for sharp and flat contexts
    NOTE_ORDER_SHARP = ['c', 'c#', 'd', 'd#', 'e', 'f',
                        'f#', 'g', 'g#', 'a', 'a#', 'b']
    NOTE_ORDER_FLAT = ['c', 'db', 'd', 'eb', 'e', 'f',
                       'gb', 'g', 'ab', 'a', 'bb', 'b']

    # Define flat keys for reference
    FLAT_KEYS = ['f', 'bb', 'eb', 'ab', 'db', 'gb', 'cb']

    # Scale types to generate
    SCALE_TYPES = ["major", "minor"]

    ############################################################################
    # 1. Utility: Convert accidentals to LilyPond format (for notes AND keys)  #
    ############################################################################
    def convert_to_lilypond_note(note):
        """
        Converts a standard note with accidentals to LilyPond-compatible notation.

        Args:
            note (str): The note to convert (e.g., 'f#', 'eb').

        Returns:
            str: The LilyPond-compatible note name (e.g., 'fis', 'ees').
        """
        mapping = {
            'c#': 'cis',  'd#': 'dis',  'f#': 'fis',  'g#': 'gis',
            'a#': 'ais',  'cb': 'ces',  'db': 'des',  'eb': 'ees',
            'fb': 'fes',  'gb': 'ges',  'ab': 'aes',  'bb': 'bes'
            # You can add double sharps/flats if needed
        }
        note_lower = note.lower()
        return mapping.get(note_lower, note_lower)

    def convert_to_lilypond_key_signature(note, scale_type):
        """
        Converts the base note to LilyPond format and appends \major or \minor.

        Args:
            note (str): The key, e.g. 'f#' or 'eb'
            scale_type (str): 'major' or 'minor'

        Returns:
            str: A LilyPond key signature directive, e.g. "\\key fis \\minor"
        """
        lilypond_note = convert_to_lilypond_note(note)  # e.g. 'f#' -> 'fis'
        return f"\\key {lilypond_note} \\{scale_type}"

    def convert_to_lilypond_relative(note):
        """
        Converts the first note of a key (e.g., 'f#') into LilyPond-compatible
        relative pitch (e.g., 'fis' + "'").

        Args:
            note (str): The key, e.g. 'f#'

        Returns:
            str: Something like "fis'" or "ees'"
        """
        # Extract the letter + accidental portion (e.g., 'f#')
        match = re.match(r'^([a-gA-G][b#]?)', note)
        if match:
            base_note = match.group(1).lower()  # e.g., 'f#'
            base_note_lily = convert_to_lilypond_note(base_note)  # e.g., 'fis'
            return base_note_lily + "'"          # e.g., 'fis' + "'"
        else:
            # Default to middle c if we can't parse
            return "c'"

    ############################################################################
    # 2. Creating the scale notes (ascending + descending)                     #
    ############################################################################
    def get_note_index(note, note_order):
        """
        Retrieves the index of the note in the provided note_order list.
        Handles enharmonic equivalents as well (db -> c#, etc.).

        Args:
            note (str): The note to find (e.g., 'c', 'd#', 'eb').
            note_order (list): The list of notes to search within.
        """
        # Map some common enharmonics to their sharps
        enharmonic = {
            'cb': 'b',
            'fb': 'e',
            'db': 'c#',
            'eb': 'd#',
            'gb': 'f#',
            'ab': 'g#',
            'bb': 'a#'
        }
        n_lower = note.lower()
        if n_lower in note_order:
            return note_order.index(n_lower)
        elif n_lower in enharmonic and enharmonic[n_lower] in note_order:
            return note_order.index(enharmonic[n_lower])
        else:
            print(f"Warning: Note '{note}' not recognized. Defaulting to 'c'.")
            return note_order.index('c')

    def next_note(current_note, interval, note_order):
        """
        Calculates the next note in the scale based on the interval.

        Args:
            current_note (str): The current note.
            interval (int): Steps to move in the note_order (e.g., 2 or 1).
            note_order (list): The list of notes to use (sharps or flats).
        """
        index = get_note_index(current_note, note_order)
        next_index = (index + interval) % len(note_order)
        return note_order[next_index]

    def generate_scale_notes(key, scale_type, octaves, note_order):
        """
        Generates ascending + descending scale notes in LilyPond format.

        Args:
            key (str): The key (e.g., 'c', 'g#', 'eb').
            scale_type (str): 'major' or 'minor'.
            octaves (int): 1-4.
            note_order (list): Sharps or flats version of the chromatic scale.

        Returns:
            str: LilyPond-formatted scale notes with quarter durations.
        """
        if scale_type not in SCALE_INTERVALS:
            print(f"Error: Scale type '{scale_type}' not supported.")
            sys.exit(1)

        intervals = SCALE_INTERVALS[scale_type]
        current_note = key.lower()
        scale = [current_note]

        # Build one octave ascending
        for interval in intervals:
            current_note = next_note(current_note, interval, note_order)
            scale.append(current_note)

        # Repeat for the specified number of octaves
        full_scale = scale.copy()
        for _ in range(1, octaves):
            starting_note = scale[-1]
            for interval in intervals:
                starting_note = next_note(starting_note, interval, note_order)
                full_scale.append(starting_note)

        # Descending scale (exclude last note to avoid duplication)
        descending_scale = full_scale[::-1][1:]

        # Combine ascending + descending
        combined_scale = full_scale + descending_scale

        # Convert everything to LilyPond note names
        lilypond_notes = [convert_to_lilypond_note(n) for n in combined_scale]

        # Give each note a quarter duration
        notes_with_rhythm = ' '.join(f"{n}4" for n in lilypond_notes)
        return notes_with_rhythm

    ############################################################################
    # 3. Determine note order (sharp/flat), relative minors, etc.             #
    ############################################################################
    def determine_note_order(k):
        """
        Chooses sharps vs flats based on the key name.
        """
        k_lower = k.lower()
        if k_lower in FLAT_KEYS or 'b' in k_lower:
            return NOTE_ORDER_FLAT
        else:
            return NOTE_ORDER_SHARP

    def find_relative_minor(major_key):
        """
        Returns the relative minor for a given major key.
        """
        relative_minors = {
            'c': 'a',   'g': 'e',   'd': 'b',   'a': 'f#',
            'e': 'c#',  'b': 'g#',  'f#': 'd#', 'c#': 'a#',
            'f': 'd',   'bb': 'g',  'eb': 'c',  'ab': 'f',
            'db': 'bb', 'gb': 'eb', 'cb': 'ab'
        }
        mk_lower = major_key.lower()
        if mk_lower in relative_minors:
            return relative_minors[mk_lower]
        else:
            print(f"Warning: No relative minor for '{major_key}'. Defaulting to 'a'.")
            return 'a'

    ############################################################################
    # 4. File cleanup, LilyPond version retrieval, compile steps              #
    ############################################################################
    def delete_existing_files(filenames):
        """
        Deletes existing files if they exist.
        """
        for filename in filenames:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    print(f"Deleted existing file: {filename}")
                except Exception as e:
                    print(f"Error deleting file '{filename}': {e}")
                    sys.exit(1)

    def get_lilypond_version():
        """
        Checks the installed LilyPond version, or exits if not found.
        """
        try:
            result = subprocess.run(['lilypond', '--version'],
                                    capture_output=True, text=True, check=True)
            # Example output: "GNU LilyPond 2.24.0"
            match = re.search(r'LilyPond\s+(\d+\.\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
            else:
                print("Error: Could not parse LilyPond version.")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving LilyPond version: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: LilyPond not found in PATH.")
            sys.exit(1)

    ############################################################################
    # 5. Build the actual .ly content and run the compilation                 #
    ############################################################################
    def generate_lilypond_combined(filename, main_key, scale_types, octaves, lilypond_version):
        """
        Generates a LilyPond .ly file with the desired scales, then compiles it.
        """
        # Global header for the LilyPond file
        global_header = f"""
\\version "{lilypond_version}"  % Force LilyPond to treat code with this version

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
    system-count = #0
    line-width = 16\\cm  % Adjust as needed
}}
"""

        lilypond_content = global_header + "\n"

        # For each scale type (major / minor) ...
        for st in scale_types:
            if st == "minor":
                rel_minor_key = find_relative_minor(main_key)
                scale_key = rel_minor_key
                mode = "Minor"
            else:
                scale_key = main_key.lower()
                mode = "Major"

            # Build the \key ... \minor or \major line
            key_signature = convert_to_lilypond_key_signature(scale_key, st)

            # Decide the note-order (sharp vs flat)
            this_note_order = determine_note_order(scale_key)

            # Generate the actual scale notes
            scale_notes = generate_scale_notes(scale_key, st, octaves, this_note_order)

            # Figure out the correct \relative pitch
            relative_pitch = convert_to_lilypond_relative(scale_key)

            # Build the snippet for this scale
            scale_score = f"""
\\markup \\column {{
  \\center-column {{
    \\bold "{st.capitalize()} Scale in {scale_key.capitalize()} ({mode})"
  }}
}}

\\score {{
  \\new Staff {{
    \\relative {relative_pitch} {{
      {key_signature}
      \\time 4/4

      {scale_notes}
    }}
  }}
  \\layout {{
    indent = 0
    ragged-right = ##t
  }}
  \\midi {{ }}
}}
"""
            lilypond_content += scale_score + "\n"

        # Write the .ly file
        try:
            with open(filename, 'w') as f:
                f.write(lilypond_content)
            print(f"LilyPond file '{filename}' generated successfully.")
        except IOError as e:
            print(f"Error writing to '{filename}': {e}")
            sys.exit(1)

        # Invoke LilyPond to compile
        try:
            print(f"Compiling the LilyPond file '{filename}'...")
            subprocess.run(['lilypond', filename], check=True)
            base = os.path.splitext(filename)[0]
            print(f"Compilation successful! Created '{base}.pdf' and '{base}.midi'.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error while compiling '{filename}': {e}")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: LilyPond is not installed or not in PATH.")
            sys.exit(1)

    # ------------------------------- MAIN LOGIC -------------------------------

    # 1. Validate octaves
    if not isinstance(octaves, int) or not (1 <= octaves <= 4):
        print("Error: Number of octaves must be an integer between 1 and 4.")
        sys.exit(1)

    # 2. Define output filenames
    ly_filename = "combined_practice.ly"
    pdf_filename = "combined_practice.pdf"
    midi_filename = "combined_practice.midi"

    # 3. Delete any existing versions of these files
    delete_existing_files([ly_filename, pdf_filename, midi_filename])

    # 4. Get LilyPond version
    lilypond_version = get_lilypond_version()

    # 5. Generate and compile
    print("Generating scales in LilyPond...")
    generate_lilypond_combined(ly_filename, key, SCALE_TYPES, octaves, lilypond_version)
    print("All scales generated and compiled successfully.")

# Example usage (uncomment to run directly):
if __name__ == "__main__":
    key_input = "c"   # Try 'a', 'c', 'f#', 'eb', etc.
    octaves_input = 2  # 1 to 4
    generate_and_compile_scales(key_input, octaves_input)
