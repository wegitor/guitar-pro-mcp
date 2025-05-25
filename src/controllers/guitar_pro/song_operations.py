from typing import Dict, Any
from .base_controller import GuitarProMixin
from guitarpro.models import Song, Track, RepeatGroup
from .track_operations import TrackOperationsController
from .measure_operations import MeasureOperationsController
from .note_operations import NoteOperationsController
import logging

logger = logging.getLogger(__name__)

class SongOperationsController(TrackOperationsController, MeasureOperationsController, NoteOperationsController):
    """Controller for Guitar Pro song operations."""
    
    def get_song_info(self) -> dict:
        """Get information about the current song."""
        self._ensure_song_loaded()
        return {
            'title': self.current_song.title,
            'artist': self.current_song.artist,
            'album': self.current_song.album,
            'copyright': self.current_song.copyright,
            'subtitle': self.current_song.subtitle,
            'notice': self.current_song.notice,
            'track_count': len(self.current_song.tracks)
        }
        
    def create_new_song(self, title: str = "New Song", artist: str = "") -> bool:
        """
        Create a new Guitar Pro song.
        
        Args:
            title (str): Title for the new song
            artist (str): Artist name
            
        Returns:
            bool: True if successful
        """
        try:
            # Print debug info
            print(f"Creating new song: {title} by {artist}")
            
            # Create a new song instance
            self.current_song = Song()
            self.current_song.title = title
            self.current_song.artist = artist
            
            # Print debug info
            print("Song instance created successfully")
            
            # Add a default track with 6 strings (standard guitar)
            print("Adding track...")
            track_index = self.add_track("Guitar")
            print(f"Track added at index {track_index}")
            
            # Add a default measure header and measure
            # This is necessary for a valid Guitar Pro song
            print("Adding measure header...")
            measure_index = self.add_measure_header()
            print(f"Measure header added at index {measure_index}")
            
            # Set default tempo (120 BPM)
            self.current_song.tempo = 120
            print("Tempo set to 120 BPM")
            
            # Verify the song structure
            print(f"Song has {len(self.current_song.tracks)} tracks and {len(self.current_song.measureHeaders)} measure headers")
            
            return True
        except Exception as e:
            import traceback
            print(f"Error creating new song: {e}")
            traceback.print_exc()
            return False
            
    def set_song_properties(self, title: str = None, artist: str = None, 
                           album: str = None, tempo: int = None) -> bool:
        """
        Set properties of the current song.
        
        Args:
            title (str, optional): Title of the song
            artist (str, optional): Artist name
            album (str, optional): Album name
            tempo (int, optional): Tempo in BPM
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            if title is not None:
                self.current_song.title = title
                
            if artist is not None:
                self.current_song.artist = artist
                
            if album is not None:
                self.current_song.album = album
                
            if tempo is not None:
                self.current_song.tempo = tempo
                
            return True
        except Exception as e:
            print(f"Error setting song properties: {e}")
            return False
            
    def get_song_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the current song.
        
        Returns:
            dict: Song statistics
        """
        if self.current_song is None:
            return {"error": "No song loaded"}
            
        stats = {
            "title": self.current_song.title,
            "track_count": len(self.current_song.tracks),
            "measure_count": len(self.current_song.measureHeaders) if self.current_song.measureHeaders else 0,
            "tracks": []
        }
        
        total_beats = 0
        total_notes = 0
        
        for track_index, track in enumerate(self.current_song.tracks):
            track_notes = 0
            track_beats = 0
            
            for measure in track.measures:
                for voice in measure.voices:
                    for beat in voice.beats:
                        track_beats += 1
                        track_notes += len(beat.notes)
            
            stats["tracks"].append({
                "name": track.name,
                "string_count": len(track.strings),
                "measure_count": len(track.measures),
                "note_count": track_notes,
                "beat_count": track_beats
            })
            
            total_beats += track_beats
            total_notes += track_notes
        
        stats["total_notes"] = total_notes
        stats["total_beats"] = total_beats
        
        return stats 

    def set_lyrics(self, lyrics: str) -> bool:
        """
        Set the lyrics for the current song.
        
        Args:
            lyrics (str): The lyrics to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            self.current_song.lyrics = lyrics
            return True
        except Exception as e:
            print(f"Error setting lyrics: {e}")
            return False

    def get_lyrics(self) -> str:
        """
        Get the lyrics of the current song.
        
        Returns:
            str: The lyrics of the song, or an empty string if no song is loaded
        """
        if self.current_song is None:
            return ""
            
        try:
            # Extract lyrics from the song's lyrics object
            if self.current_song.lyrics:
                lyrics_text = []
                for line in self.current_song.lyrics.lines:
                    if line and line.lyrics:
                        lyrics_text.append(line.lyrics)
                return "\n".join(lyrics_text)
            return ""
        except Exception as e:
            logger.error(f"Error getting lyrics: {e}")
            return ""

    def set_page_setup(self, page_setup: dict) -> bool:
        """
        Set the page setup for the current song.
        
        Args:
            page_setup (dict): A dictionary containing page setup properties
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            for key, value in page_setup.items():
                setattr(self.current_song.pageSetup, key, value)
            return True
        except Exception as e:
            print(f"Error setting page setup: {e}")
            return False

    def get_page_setup(self) -> dict:
        """
        Get the page setup of the current song.
        
        Returns:
            dict: A dictionary containing page setup properties, or an empty dict if no song is loaded
        """
        if self.current_song is None:
            return {}
        return {
            "pageSize": self.current_song.pageSetup.pageSize,
            "pageMargin": self.current_song.pageSetup.pageMargin,
            "scoreSizeProportion": self.current_song.pageSetup.scoreSizeProportion,
            "headerAndFooter": self.current_song.pageSetup.headerAndFooter,
            "title": self.current_song.pageSetup.title,
            "subtitle": self.current_song.pageSetup.subtitle,
            "artist": self.current_song.pageSetup.artist,
            "album": self.current_song.pageSetup.album,
            "words": self.current_song.pageSetup.words,
            "music": self.current_song.pageSetup.music,
            "wordsAndMusic": self.current_song.pageSetup.wordsAndMusic,
            "copyright": self.current_song.pageSetup.copyright,
            "pageNumber": self.current_song.pageSetup.pageNumber
        }

    def set_advanced_metadata(self, metadata: dict) -> bool:
        """
        Set advanced metadata for the current song.
        
        Args:
            metadata (dict): A dictionary containing metadata properties
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            for key, value in metadata.items():
                setattr(self.current_song, key, value)
            return True
        except Exception as e:
            print(f"Error setting advanced metadata: {e}")
            return False

    def get_advanced_metadata(self) -> dict:
        """
        Get advanced metadata of the current song.
        
        Returns:
            dict: A dictionary containing metadata properties, or an empty dict if no song is loaded
        """
        if self.current_song is None:
            return {}
        return {
            "subtitle": self.current_song.subtitle,
            "words": self.current_song.words,
            "music": self.current_song.music,
            "tab": self.current_song.tab,
            "instructions": self.current_song.instructions,
            "notice": self.current_song.notice
        }

    def add_repeat_group(self, start_measure: int, end_measure: int, repeat_type: str = "normal", 
                        repeat_count: int = 2, endings: list = None) -> bool:
        """
        Add a repeat group to the song.
        
        Args:
            start_measure (int): Index of the first measure in the repeat group
            end_measure (int): Index of the last measure in the repeat group
            repeat_type (str): Type of repeat ("normal", "alternate", "repeat")
            repeat_count (int): Number of times to repeat
            endings (list): List of ending numbers (e.g., [1, 2] for first and second endings)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            # Create a new repeat group
            repeat_group = RepeatGroup()
            
            # Add the repeat group to the song
            self.current_song.repeatGroups.append(repeat_group)
            
            # Update measure headers
            for i in range(start_measure, end_measure + 1):
                if i < len(self.current_song.measureHeaders):
                    header = self.current_song.measureHeaders[i]
                    header.repeatGroup = repeat_group
                    
                    # Set repeat open for first measure
                    if i == start_measure:
                        header.isRepeatOpen = True
                        header.repeatClose = repeat_count
                    
                    # Set repeat close for last measure
                    if i == end_measure:
                        header.repeatClose = repeat_count
                    
                    # Set repeat alternatives if specified
                    if endings and i == end_measure:
                        header.repeatAlternative = max(endings)
            
            return True
            
        except Exception as e:
            print(f"Error adding repeat group: {e}")
            return False

    def get_repeat_groups(self) -> list:
        """
        Get all repeat groups in the song.
        
        Returns:
            list: List of repeat groups with their properties
        """
        if self.current_song is None:
            return []
            
        try:
            repeat_groups = []
            for group in self.current_song.repeatGroups:
                # Find the measures that belong to this repeat group
                measures = []
                for i, header in enumerate(self.current_song.measureHeaders):
                    if header.repeatGroup == group:
                        measures.append(i)
                
                # Get repeat count from the first measure with repeat close
                repeat_count = 0
                for header in group.measureHeaders:
                    if header.repeatClose > 0:
                        repeat_count = header.repeatClose
                        break
                
                repeat_groups.append({
                    "type": "normal",  # PyGuitarPro doesn't have different repeat types
                    "repeat_count": repeat_count,
                    "endings": [header.repeatAlternative for header in group.measureHeaders if header.repeatAlternative > 0],
                    "measures": measures,
                    "is_closed": group.isClosed
                })
            
            return repeat_groups
            
        except Exception as e:
            print(f"Error getting repeat groups: {e}")
            return []

    def add_section(self, start_measure: int, end_measure: int, name: str, 
                   text: str = None, color: tuple = None) -> bool:
        """
        Add a section to the song.
        
        Args:
            start_measure (int): Index of the first measure in the section
            end_measure (int): Index of the last measure in the section
            name (str): Name of the section (e.g., "Verse", "Chorus")
            text (str, optional): Additional text for the section
            color (tuple, optional): RGB color tuple for the section
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            # Add section text to the first measure
            if start_measure < len(self.current_song.measureHeaders):
                header = self.current_song.measureHeaders[start_measure]
                header.text = name
                if text:
                    header.text += f"\n{text}"
                if color:
                    header.color = color
            
            return True
            
        except Exception as e:
            print(f"Error adding section: {e}")
            return False

    def get_sections(self) -> list:
        """
        Get all sections in the song.
        
        Returns:
            list: List of sections with their properties
        """
        if self.current_song is None:
            return []
            
        try:
            sections = []
            current_section = None
            
            for i, header in enumerate(self.current_song.measureHeaders):
                # Check for section markers in the measure
                section_text = None
                
                # Look for text in the measure
                for track in self.current_song.tracks:
                    if i < len(track.measures):
                        measure = track.measures[i]
                        for voice in measure.voices:
                            for beat in voice.beats:
                                if beat.text:
                                    text = beat.text.lower()
                                    if any(marker in text for marker in ['intro', 'verse', 'chorus', 'bridge', 'solo', 'outro', 'coda']):
                                        section_text = beat.text
                                        break
                            if section_text:
                                break
                        if section_text:
                            break
                
                # Check for markers in the measure header
                if not section_text and header.marker:
                    text = header.marker.title.lower()
                    if any(marker in text for marker in ['intro', 'verse', 'chorus', 'bridge', 'solo', 'outro', 'coda']):
                        section_text = header.marker.title
                
                if section_text:
                    # Start a new section
                    if current_section is None or current_section["end_measure"] < i - 1:
                        if current_section is not None:
                            sections.append(current_section)
                        current_section = {
                            "name": section_text,
                            "start_measure": i,
                            "end_measure": i
                        }
                    else:
                        # Extend current section
                        current_section["end_measure"] = i
            
            # Add the last section if exists
            if current_section is not None:
                sections.append(current_section)
            
            return sections
            
        except Exception as e:
            logger.error(f"Error getting sections: {e}")
            return []

    def add_coda(self, measure_index: int) -> bool:
        """
        Add a coda marker to a measure.
        
        Args:
            measure_index (int): Index of the measure to add the coda
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            if measure_index < len(self.current_song.measureHeaders):
                header = self.current_song.measureHeaders[measure_index]
                header.isCoda = True
                return True
            return False
            
        except Exception as e:
            print(f"Error adding coda: {e}")
            return False

    def add_double_bar(self, measure_index: int) -> bool:
        """
        Add a double bar line to a measure.
        
        Args:
            measure_index (int): Index of the measure to add the double bar
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            if measure_index < len(self.current_song.measureHeaders):
                header = self.current_song.measureHeaders[measure_index]
                header.isDoubleBar = True
                return True
            return False
            
        except Exception as e:
            print(f"Error adding double bar: {e}")
            return False

    def get_song_structure(self) -> dict:
        """
        Get the complete song structure including sections, repeats, and markers.
        
        Returns:
            dict: Dictionary containing the song structure
        """
        if self.current_song is None:
            return {}
            
        try:
            structure = {
                "sections": self.get_sections(),
                "repeat_groups": self.get_repeat_groups(),
                "markers": []
            }
            
            # Add markers from measures
            for track in self.current_song.tracks:
                for measure_index, measure in enumerate(track.measures):
                    # Check measure header marker
                    if measure.header.marker:
                        structure["markers"].append({
                            "type": "marker",
                            "text": measure.header.marker.title,
                            "measure": measure_index
                        })
                    
                    # Check for double bar
                    if measure.header.hasDoubleBar:
                        structure["markers"].append({
                            "type": "double_bar",
                            "measure": measure_index
                        })
                    
                    # Check for text in beats
                    for voice in measure.voices:
                        for beat_index, beat in enumerate(voice.beats):
                            if beat.text:
                                structure["markers"].append({
                                    "type": "text",
                                    "text": beat.text,
                                    "measure": measure_index,
                                    "beat": beat_index
                                })
                            
                            # Check for direction signs
                            if beat.voice.measure.header.direction:
                                structure["markers"].append({
                                    "type": "direction",
                                    "text": beat.voice.measure.header.direction.name,
                                    "measure": measure_index
                                })
            
            return structure
            
        except Exception as e:
            logger.error(f"Error getting song structure: {e}")
            return {} 