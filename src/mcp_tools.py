from mcp import types
from mcp.server.fastmcp import FastMCP, Context
from typing import Optional, Dict, Any, List

def setup_mcp_tools(mcp: FastMCP, controller) -> None:
    """Setup MCP tools for Guitar Pro control."""
    
    @mcp.tool("load_guitar_pro")
    def load_guitar_pro(ctx: Context, file_path: str) -> Dict[str, Any]:
        """Load a Guitar Pro file."""
        try:
            controller.load_file(file_path)
            return {"status": "success", "message": f"Loaded Guitar Pro file: {file_path}"}
        except Exception as e:
            return {"status": "error", "message": f"Error loading Guitar Pro file: {str(e)}"}

    @mcp.tool("save_guitar_pro")
    def save_guitar_pro(ctx: Context, file_path: str) -> Dict[str, Any]:
        """Save the current song to a Guitar Pro file."""
        try:
            controller.save_file(file_path)
            return {"status": "success", "message": f"Saved Guitar Pro file: {file_path}"}
        except Exception as e:
            return {"status": "error", "message": f"Error saving Guitar Pro file: {str(e)}"}

    @mcp.tool("get_song_info")
    def get_song_info(ctx: Context) -> Dict[str, Any]:
        """Get information about the currently loaded song."""
        try:
            song_info = controller.get_song_info()
            return {"status": "success", "data": song_info}
        except Exception as e:
            return {"status": "error", "message": f"Error getting song info: {str(e)}"}

    @mcp.tool("get_gp_tracks")
    def get_gp_tracks(ctx: Context) -> Dict[str, Any]:
        """Get a list of tracks in the current Guitar Pro song."""
        try:
            tracks = controller.get_tracks()
            return {"status": "success", "data": tracks}
        except Exception as e:
            return {"status": "error", "message": f"Error getting tracks: {str(e)}"}

    @mcp.tool("get_track_notes")
    def get_track_notes(ctx: Context, track_index: int) -> Dict[str, Any]:
        """Get all notes from a specific track."""
        try:
            notes = controller.get_track_notes(track_index)
            return {"status": "success", "data": notes}
        except Exception as e:
            return {"status": "error", "message": f"Error getting track notes: {str(e)}"}

    @mcp.tool("create_new_gp_song")
    def create_new_gp_song(ctx: Context, title: str = "New Song", artist: str = "") -> Dict[str, Any]:
        """Create a new Guitar Pro song."""
        try:
            if controller.create_new_song(title, artist):
                return {"status": "success", "message": f"Created new song: {title}"}
            return {"status": "error", "message": "Failed to create new song"}
        except Exception as e:
            return {"status": "error", "message": f"Error creating new song: {str(e)}"}

    @mcp.tool("add_gp_track")
    def add_gp_track(ctx: Context, name: str) -> Dict[str, Any]:
        """Add a new track to the Guitar Pro song."""
        try:
            track_index = controller.add_track(name)
            return {"status": "success", "message": f"Added track: {name}", "track_index": track_index}
        except Exception as e:
            return {"status": "error", "message": f"Error adding track: {str(e)}"}

    @mcp.tool("add_gp_measure")
    def add_gp_measure(ctx: Context) -> Dict[str, Any]:
        """Add a new measure to the Guitar Pro song."""
        try:
            measure_index = controller.add_measure_header()
            return {"status": "success", "message": f"Added measure", "measure_index": measure_index}
        except Exception as e:
            return {"status": "error", "message": f"Error adding measure: {str(e)}"}

    @mcp.tool("add_gp_note")
    def add_gp_note(ctx: Context, track_index: int, measure_index: int, string: int, fret: int, 
                 duration: int = 4, voice_index: int = 0, beat_index: int = 0) -> Dict[str, Any]:
        """Add a note to a specific track, measure, and string."""
        try:
            if controller.add_note(track_index, measure_index, string, fret, duration, voice_index, beat_index):
                return {"status": "success", 
                        "message": f"Added note: string {string}, fret {fret} to measure {measure_index}"}
            return {"status": "error", "message": "Failed to add note"}
        except Exception as e:
            return {"status": "error", "message": f"Error adding note: {str(e)}"}

    @mcp.tool("export_to_midi")
    def export_to_midi(ctx: Context, file_path: str) -> Dict[str, Any]:
        """Export the current song to MIDI format."""
        try:
            if controller.export_to_midi(file_path):
                return {"status": "success", "message": f"Exported to MIDI file: {file_path}"}
            return {"status": "error", "message": f"Failed to export to MIDI file: {file_path}"}
        except Exception as e:
            return {"status": "error", "message": f"Error exporting to MIDI: {str(e)}"}

    @mcp.tool("set_song_properties")
    def set_song_properties(ctx: Context, title: str = None, artist: str = None, 
                           album: str = None, tempo: int = None) -> Dict[str, Any]:
        """Set properties of the current song."""
        try:
            if controller.set_song_properties(title, artist, album, tempo):
                return {"status": "success", "message": "Song properties updated"}
            return {"status": "error", "message": "Failed to update song properties"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting song properties: {str(e)}"}

    @mcp.tool("set_track_properties")
    def set_track_properties(ctx: Context, track_index: int, name: str = None,
                           instrument: int = None, volume: int = None,
                           pan: int = None) -> Dict[str, Any]:
        """Set properties of a track."""
        try:
            if controller.set_track_properties(track_index, name, instrument, volume, pan):
                return {"status": "success", "message": f"Track {track_index} properties updated"}
            return {"status": "error", "message": f"Failed to update track {track_index} properties"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting track properties: {str(e)}"}

    @mcp.tool("transpose_track")
    def transpose_track(ctx: Context, track_index: int, semitones: int) -> Dict[str, Any]:
        """Transpose all notes in a track by a specified number of semitones."""
        try:
            if controller.transpose_track(track_index, semitones):
                direction = "up" if semitones > 0 else "down"
                semitone_str = f"{abs(semitones)} semitone{'s' if abs(semitones) != 1 else ''}"
                return {"status": "success", 
                        "message": f"Transposed track {track_index} {direction} by {semitone_str}"}
            return {"status": "error", "message": f"Failed to transpose track {track_index}"}
        except Exception as e:
            return {"status": "error", "message": f"Error transposing track: {str(e)}"}

    @mcp.tool("set_gp_time_signature")
    def set_gp_time_signature(ctx: Context, measure_index: int, numerator: int, denominator: int) -> Dict[str, Any]:
        """Set the time signature for a measure."""
        try:
            if controller.set_time_signature(measure_index, numerator, denominator):
                return {"status": "success", "message": f"Set time signature to {numerator}/{denominator}"}
            return {"status": "error", "message": "Failed to set time signature"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting time signature: {str(e)}"}

    @mcp.tool("set_gp_key_signature")
    def set_gp_key_signature(ctx: Context, measure_index: int, key: int) -> Dict[str, Any]:
        """Set the key signature for a measure."""
        try:
            if controller.set_key_signature(measure_index, key):
                return {"status": "success", "message": f"Set key signature to {key}"}
            return {"status": "error", "message": "Failed to set key signature"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting key signature: {str(e)}"}

    @mcp.tool("set_gp_tempo")
    def set_gp_tempo(ctx: Context, measure_index: int, tempo: int) -> Dict[str, Any]:
        """Set the tempo for a measure."""
        try:
            if controller.set_tempo(measure_index, tempo):
                return {"status": "success", "message": f"Set tempo to {tempo} BPM"}
            return {"status": "error", "message": "Failed to set tempo"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting tempo: {str(e)}"}

    @mcp.tool("export_to_json")
    def export_to_json(ctx: Context, file_path: str) -> Dict[str, Any]:
        """Export the current song to a JSON file."""
        try:
            if controller.export_to_json(file_path):
                return {"status": "success", "message": f"Exported to JSON file: {file_path}"}
            return {"status": "error", "message": f"Failed to export to JSON file: {file_path}"}
        except Exception as e:
            return {"status": "error", "message": f"Error exporting to JSON: {str(e)}"}

    @mcp.tool("import_from_json")
    def import_from_json(ctx: Context, file_path: str) -> Dict[str, Any]:
        """Import a song from a JSON file."""
        try:
            if controller.import_from_json(file_path):
                return {"status": "success", "message": f"Imported from JSON file: {file_path}"}
            return {"status": "error", "message": f"Failed to import from JSON file: {file_path}"}
        except Exception as e:
            return {"status": "error", "message": f"Error importing from JSON: {str(e)}"}

    @mcp.tool("get_track_tab")
    def get_track_tab(ctx: Context, track_index: int) -> Dict[str, Any]:
        """Get an ASCII tab representation of a track."""
        try:
            tab = controller.get_track_tab(track_index)
            return {"status": "success", "data": tab}
        except Exception as e:
            return {"status": "error", "message": f"Error getting track tab: {str(e)}"}

    @mcp.tool("get_song_statistics")
    def get_song_statistics(ctx: Context) -> Dict[str, Any]:
        """Get statistics about the current song."""
        try:
            stats = controller.get_song_statistics()
            return {"status": "success", "data": stats}
        except Exception as e:
            return {"status": "error", "message": f"Error getting song statistics: {str(e)}"}

    @mcp.tool("set_lyrics")
    def set_lyrics(ctx: Context, lyrics: str) -> Dict[str, Any]:
        """Set the lyrics for the current song."""
        try:
            if controller.set_lyrics(lyrics):
                return {"status": "success", "message": "Lyrics updated successfully"}
            return {"status": "error", "message": "Failed to update lyrics"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting lyrics: {str(e)}"}

    @mcp.tool("get_lyrics")
    def get_lyrics(ctx: Context) -> Dict[str, Any]:
        """Get the lyrics of the current song."""
        try:
            lyrics = controller.get_lyrics()
            return {"status": "success", "data": lyrics}
        except Exception as e:
            return {"status": "error", "message": f"Error getting lyrics: {str(e)}"}

    @mcp.tool("set_page_setup")
    def set_page_setup(ctx: Context, page_setup: dict) -> Dict[str, Any]:
        """Set the page setup for the current song."""
        try:
            if controller.set_page_setup(page_setup):
                return {"status": "success", "message": "Page setup updated successfully"}
            return {"status": "error", "message": "Failed to update page setup"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting page setup: {str(e)}"}

    @mcp.tool("get_page_setup")
    def get_page_setup(ctx: Context) -> Dict[str, Any]:
        """Get the page setup of the current song."""
        try:
            page_setup = controller.get_page_setup()
            return {"status": "success", "data": page_setup}
        except Exception as e:
            return {"status": "error", "message": f"Error getting page setup: {str(e)}"}

    @mcp.tool("set_advanced_metadata")
    def set_advanced_metadata(ctx: Context, metadata: dict) -> Dict[str, Any]:
        """Set advanced metadata for the current song."""
        try:
            if controller.set_advanced_metadata(metadata):
                return {"status": "success", "message": "Advanced metadata updated successfully"}
            return {"status": "error", "message": "Failed to update advanced metadata"}
        except Exception as e:
            return {"status": "error", "message": f"Error setting advanced metadata: {str(e)}"}

    @mcp.tool("get_advanced_metadata")
    def get_advanced_metadata(ctx: Context) -> Dict[str, Any]:
        """Get advanced metadata of the current song."""
        try:
            metadata = controller.get_advanced_metadata()
            return {"status": "success", "data": metadata}
        except Exception as e:
            return {"status": "error", "message": f"Error getting advanced metadata: {str(e)}"}

    @mcp.tool("add_chord")
    def add_chord(ctx: Context, track_index: int, measure_index: int, beat_index: int, chord_data: dict) -> Dict[str, Any]:
        """Add a chord to a specific beat."""
        try:
            if controller.add_chord(track_index, measure_index, beat_index, chord_data):
                return {"status": "success", "message": "Chord added successfully"}
            return {"status": "error", "message": "Failed to add chord"}
        except Exception as e:
            return {"status": "error", "message": f"Error adding chord: {str(e)}"}

    @mcp.tool("get_chord")
    def get_chord(ctx: Context, track_index: int, measure_index: int, beat_index: int) -> Dict[str, Any]:
        """Get the chord from a specific beat."""
        try:
            chord = controller.get_chord(track_index, measure_index, beat_index)
            return {"status": "success", "data": chord}
        except Exception as e:
            return {"status": "error", "message": f"Error getting chord: {str(e)}"}

    @mcp.tool("add_repeat_group")
    def add_repeat_group(ctx: Context, start_measure: int, end_measure: int, 
                        repeat_type: str = "normal", repeat_count: int = 2, 
                        endings: list = None) -> Dict[str, Any]:
        """Add a repeat group to the song."""
        try:
            if controller.add_repeat_group(start_measure, end_measure, repeat_type, repeat_count, endings):
                return {"status": "success", "message": f"Added repeat group from measure {start_measure} to {end_measure}"}
            return {"status": "error", "message": "Failed to add repeat group"}
        except Exception as e:
            return {"status": "error", "message": f"Error adding repeat group: {str(e)}"}

    @mcp.tool("get_repeat_groups")
    def get_repeat_groups(ctx: Context) -> Dict[str, Any]:
        """Get all repeat groups in the song."""
        try:
            repeat_groups = controller.get_repeat_groups()
            return {"status": "success", "data": repeat_groups}
        except Exception as e:
            return {"status": "error", "message": f"Error getting repeat groups: {str(e)}"}

    @mcp.tool("add_section")
    def add_section(ctx: Context, start_measure: int, end_measure: int, name: str,
                   text: str = None, color: tuple = None) -> Dict[str, Any]:
        """Add a section to the song."""
        try:
            if controller.add_section(start_measure, end_measure, name, text, color):
                return {"status": "success", "message": f"Added section '{name}' from measure {start_measure} to {end_measure}"}
            return {"status": "error", "message": "Failed to add section"}
        except Exception as e:
            return {"status": "error", "message": f"Error adding section: {str(e)}"}

    @mcp.tool("get_sections")
    def get_sections(ctx: Context) -> Dict[str, Any]:
        """Get all sections in the song."""
        try:
            sections = controller.get_sections()
            return {"status": "success", "data": sections}
        except Exception as e:
            return {"status": "error", "message": f"Error getting sections: {str(e)}"}

    @mcp.tool("add_coda")
    def add_coda(ctx: Context, measure_index: int) -> Dict[str, Any]:
        """Add a coda marker to a measure."""
        try:
            if controller.add_coda(measure_index):
                return {"status": "success", "message": f"Added coda at measure {measure_index}"}
            return {"status": "error", "message": "Failed to add coda"}
        except Exception as e:
            return {"status": "error", "message": f"Error adding coda: {str(e)}"}

    @mcp.tool("add_double_bar")
    def add_double_bar(ctx: Context, measure_index: int) -> Dict[str, Any]:
        """Add a double bar line to a measure."""
        try:
            if controller.add_double_bar(measure_index):
                return {"status": "success", "message": f"Added double bar at measure {measure_index}"}
            return {"status": "error", "message": "Failed to add double bar"}
        except Exception as e:
            return {"status": "error", "message": f"Error adding double bar: {str(e)}"}

    @mcp.tool("get_song_structure")
    def get_song_structure(ctx: Context) -> Dict[str, Any]:
        """Get the complete song structure including sections, repeats, and markers."""
        try:
            structure = controller.get_song_structure()
            return {"status": "success", "data": structure}
        except Exception as e:
            return {"status": "error", "message": f"Error getting song structure: {str(e)}"}