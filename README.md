# Guitar Pro MCP Server

A Message Control Protocol (MCP) server for manipulating Guitar Pro files. This server provides a set of tools for opening, modifying, and saving Guitar Pro files through a standardized interface.

> **Note**: Currently, only Guitar Pro 5 (.gp5) format has been tested. Support for other formats (.gp3, .gp4) may be limited or untested.

## Features

- Load and save Guitar Pro files
- Get song information (title, artist, tracks, etc.)
- Extract notes from tracks
- Create new songs and add tracks
- Manipulate track properties
- Export to MIDI format
- Export/Import to/from JSON format

## Requirements

- Python 3.10 or higher
- PyGuitarPro library
- MCP server framework
- MIDI support (mido library)
- uv (recommended for package management)

## Installation

### Using uv (Recommended)

1. Install uv if you haven't already:
```bash
pip install uv
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Unix/macOS:
source .venv/bin/activate
# On Windows(cmd):
call .venv\Scripts\activate.bat
```

3. Install the package:
```bash
uv pip install .
```

### Running the Server

You can run the server using uv directly:
```bash
uv --directory <project_path> run -m src.run_mcp_server
```

For example, on Windows:
```bash
uv --directory C:\path\to\guitar_pro_mcp2 run -m src.run_mcp_server
```

Or using the Python module directly after installation:
```bash
python -m src.run_mcp_server
```

### Using pip

```bash
pip install guitar-pro-mcp
```

### From source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/guitar-pro-mcp.git
cd guitar-pro-mcp
```

2. Install the package:
```bash
# Install in development mode with all dependencies
pip install -e ".[dev]"

# Or install without development dependencies
pip install -e .
```

2. Connect to the server using an MCP client.

## Usage(Direct)

1. Start the MCP server:
```bash
python src/run_mcp_server.py
```

2. Connect to the server using an MCP client.

## Available MCP Tools

### File Operations
- `load_guitar_pro`: Load a Guitar Pro file
  - Parameters: `file_path` (path to the .gp5 file)
  - Returns: Success/error message
  
- `save_guitar_pro`: Save the current song to a Guitar Pro file
  - Parameters: `file_path` (path to save the file)
  - Returns: Success/error message

### Song Information
- `get_song_info`: Get basic information about the currently loaded song
  - Returns: Dictionary containing title, artist, album, copyright, subtitle, notice, and track count
  
- `get_song_statistics`: Get detailed statistics about the current song
  - Returns: Dictionary containing track counts, measure counts, note counts, and detailed track information

### Track Operations
- `get_gp_tracks`: Get a list of tracks in the current Guitar Pro song
  - Returns: List of tracks with their name, index, strings, and instrument
  
- `get_track_notes`: Get all notes from a specific track
  - Parameters: `track_index` (index of the track)
  - Returns: List of notes with their properties (measure, beat, string, value, etc.)
  
- `add_gp_track`: Add a new track to the Guitar Pro song
  - Parameters: `name` (name of the track)
  - Returns: Success message and track index
  
- `set_track_properties`: Set properties of a track
  - Parameters:
    - `track_index`: Index of the track
    - `name`: New track name (optional)
    - `instrument`: Instrument ID (optional)
    - `volume`: Volume level (optional)
    - `pan`: Pan position (optional)
  - Returns: Success/error message

### Measure Operations
- `add_gp_measure`: Add a new measure to the Guitar Pro song
  - Returns: Success message and measure index

- `set_gp_time_signature`: Set the time signature for a measure
  - Parameters: `measure_index`, `numerator`, `denominator`
  - Returns: Success/error message

- `set_gp_key_signature`: Set the key signature for a measure
  - Parameters: `measure_index`, `key`
  - Returns: Success/error message

- `set_gp_tempo`: Set the tempo for a measure
  - Parameters: `measure_index`, `tempo`
  - Returns: Success/error message

### Note Operations
- `add_gp_note`: Add a note to a specific track and measure
  - Parameters:
    - `track_index`: Index of the track
    - `measure_index`: Index of the measure
    - `string`: String number
    - `fret`: Fret number
    - `duration`: Note duration (default: 4)
    - `voice_index`: Voice index (default: 0)
    - `beat_index`: Beat index (default: 0)
  - Returns: Success/error message

### Export/Import Operations
- `export_to_midi`: Export the current song to MIDI format
  - Parameters: `file_path`
  - Returns: Success/error message

- `export_to_json`: Export the current song to JSON format
  - Parameters: `file_path`
  - Returns: Success/error message

- `import_from_json`: Import a song from JSON format
  - Parameters: `file_path`
  - Returns: Success/error message

### Tab Operations
- `get_track_tab`: Generate ASCII tab representation of a track
  - Parameters: `track_index`
  - Returns: ASCII tab representation as string

### Song Structure Management
- `add_repeat_group`: Add a repeat group to the song
  - Parameters:
    - `start_measure`: Starting measure index
    - `end_measure`: Ending measure index
    - `repeat_type`: Type of repeat ("normal", "alternate", "repeat_1st", "repeat_2nd")
    - `repeat_count`: Number of times to repeat (default: 2)
    - `endings`: List of ending numbers (optional)
  - Returns: Success/error message

- `get_repeat_groups`: Get all repeat groups in the song
  - Returns: List of repeat group objects with their properties

- `add_section`: Add a section to the song
  - Parameters:
    - `start_measure`: Starting measure index
    - `end_measure`: Ending measure index
    - `name`: Section name
    - `text`: Optional section text
    - `color`: Optional section color as RGB tuple
  - Returns: Success/error message

- `get_sections`: Get all sections in the song
  - Returns: List of section objects with their properties

- `add_coda`: Add a coda marker to a measure
  - Parameters: `measure_index`
  - Returns: Success/error message

- `add_double_bar`: Add a double bar line to a measure
  - Parameters: `measure_index`
  - Returns: Success/error message

- `get_song_structure`: Get the complete song structure
  - Returns: Dictionary containing:
    - `sections`: List of all sections
    - `repeat_groups`: List of all repeat groups
    - `markers`: List of all markers (codas, double bars, etc.)

### Metadata and Lyrics
- `set_lyrics`: Set the lyrics for the current song
  - Parameters: `lyrics` (string containing the lyrics)
  - Returns: Success/error message
  
- `get_lyrics`: Get the lyrics of the current song
  - Returns: The lyrics as a string
  
- `set_page_setup`: Set the page setup for the current song
  - Parameters: `page_setup` (dictionary containing page setup properties)
  - Properties include: pageSize, pageMargin, scoreSizeProportion, headerAndFooter, title, subtitle, artist, album, words, music, wordsAndMusic, copyright, pageNumber
  - Returns: Success/error message
  
- `get_page_setup`: Get the page setup of the current song
  - Returns: Dictionary containing page setup properties
  
- `set_advanced_metadata`: Set advanced metadata for the current song
  - Parameters: `metadata` (dictionary containing metadata properties)
  - Properties include: subtitle, words, music, tab, instructions, notice
  - Returns: Success/error message
  
- `get_advanced_metadata`: Get advanced metadata of the current song
  - Returns: Dictionary containing metadata properties

### Chord Operations
- `add_chord`: Add a chord to a specific beat
  - Parameters:
    - `track_index`: Index of the track
    - `measure_index`: Index of the measure
    - `beat_index`: Index of the beat
    - `chord_data`: Dictionary containing chord properties
  - Chord properties include: name, root, type, extension, bass, tonality, fifth, ninth, eleventh, firstFret, strings, barres, fingerings
  - Returns: Success/error message

- `get_chord`: Get the chord from a specific beat
  - Parameters:
    - `track_index`: Index of the track
    - `measure_index`: Index of the measure
    - `beat_index`: Index of the beat
  - Returns: Dictionary containing chord properties

Claude configuration (with uv run):
```json
{
    "mcpServers": {
        "guitar-pro-mcp": {
            "type": "stdio",
            "command": "uv",
            "args": [
                "--directory",
                "<path to folder>",
                "run",
                "-m",
                "src.run_mcp_server"
            ]
        }
    }
}
```

Claude configuration (direct usage):
```json
{
    "mcpServers": {
        "guitar-pro-mcp": {
            "type": "stdio",
            "command": "python",
            "args": [
                "<path to folder>\\src\\run_mcp_server.py"
            ]
        }
    }
}
```


### Claude configuration (with uv run):
```json
{
    "mcpServers": {
        "guitar-pro-mcp": {
            "type": "stdio",
            "command": "uv",
            "args": [
                "--directory",
                "<path to folder>",
                "run",
                "-m",
                "src.run_mcp_server"
            ]
        }
    }
}
```

## Implementation Details

The implementation uses the PyGuitarPro library to parse and manipulate Guitar Pro files. The MCP server provides a simple API to access the functionality of the PyGuitarPro library.

## License

This project is licensed under the MIT License.
