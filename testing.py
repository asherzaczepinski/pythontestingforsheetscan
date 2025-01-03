# testing.py

import subprocess
from music21 import stream, note, metadata, environment
import os

def create_musicxml(note_list, filename="simple_sheet"):
    """
    Creates a MusicXML file from a list of notes.

    Args:
        note_list (list): List of note names as strings (e.g., ['C4', 'D4', 'E4'])
        filename (str): The base filename for the output files
    """
    # Create a new stream
    s = stream.Stream()

    # Add metadata (title)
    meta = metadata.Metadata()
    meta.title = 'Simple Sheet Music'
    s.insert(0, meta)

    # Add each note to the stream
    for n in note_list:
        try:
            new_note = note.Note(n)
            s.append(new_note)
        except Exception as e:
            print(f"Warning: '{n}' is not a valid note. Skipping. Error: {e}")

    # Write to MusicXML
    try:
        xml_filename = f'{filename}.xml'
        s.write('musicxml', fp=xml_filename)
        print(f"MusicXML successfully saved as '{xml_filename}'")
        return xml_filename
    except Exception as e:
        print("Error generating MusicXML.")
        print(e)
        return None

def convert_musicxml_to_pdf(musescore_path, input_xml, output_pdf):
    """
    Converts a MusicXML file to PDF using MuseScore 4.

    Args:
        musescore_path (str): Path to the MuseScore 4 executable.
        input_xml (str): Path to the input MusicXML file.
        output_pdf (str): Path to the output PDF file.
    """
    if not os.path.exists(musescore_path):
        print(f"Error: MuseScore executable not found at '{musescore_path}'. Please verify the path.")
        return False

    if not os.path.exists(input_xml):
        print(f"Error: Input MusicXML file '{input_xml}' does not exist.")
        return False

    try:
        # Construct the command
        # '--export-to' specifies the output PDF path
        # '--force' overwrites the PDF if it already exists
        command = [
            musescore_path,
            '--export-to=' + output_pdf,
            '--force',
            input_xml
        ]

        # Execute the command
        subprocess.run(command, check=True)
        print(f"PDF successfully saved as '{output_pdf}'")
        return True
    except subprocess.CalledProcessError as e:
        print("Error converting MusicXML to PDF.")
        print(e)
        return False
    except Exception as e:
        print("An unexpected error occurred during conversion.")
        print(e)
        return False

def create_pdf_from_notes(note_list, filename="simple_sheet", musescore_path="/Applications/MuseScore 4.app/Contents/MacOS/mscore"):
    """
    Creates a PDF sheet music file from a list of notes.

    Args:
        note_list (list): List of note names as strings (e.g., ['C4', 'D4', 'E4'])
        filename (str): The base filename for the output files
        musescore_path (str): Path to the MuseScore 4 executable.
    """
    # Step 1: Create MusicXML
    xml_file = create_musicxml(note_list, filename)
    if not xml_file:
        print("Failed to create MusicXML. Aborting PDF generation.")
        return

    # Step 2: Define PDF filename
    pdf_file = f"{filename}.pdf"

    # Step 3: Convert MusicXML to PDF
    success = convert_musicxml_to_pdf(musescore_path, xml_file, pdf_file)
    if success:
        print(f"Sheet music PDF '{pdf_file}' generated successfully.")
    else:
        print("Failed to generate PDF.")

if __name__ == "__main__":
    # Define your list of notes here
    # Example: C4 major scale ascending and descending
    my_notes = [
        'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5',
        'B4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4'
    ]

    # Path to MuseScore 4 executable
    musescore_executable = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"

    # Create the PDF
    create_pdf_from_notes(my_notes, filename="c_major_scale", musescore_path=musescore_executable)
