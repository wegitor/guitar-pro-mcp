from .base_controller import GuitarProMixin
import guitarpro as gp
from guitarpro.models import MeasureHeader, TimeSignature, KeySignature, Measure, Voice

class MeasureOperationsController(GuitarProMixin):
    """Controller for Guitar Pro measure operations."""
    
    def add_measure_header(self) -> int:
        """
        Add a new measure header to the song.
        
        Returns:
            int: Index of the new measure header
        """
        if self.current_song is None:
            self.create_new_song()
            
        header = MeasureHeader()
        
        # Set up default time signature (4/4)
        time_sig = TimeSignature()
        time_sig.numerator = 4
        time_sig.denominator.value = 4
        header.timeSignature = time_sig
        
        # Set up default key signature (C major)
        header.keySignature = KeySignature.CMajor
        
        # Add the header to the song
        self.current_song.measureHeaders.append(header)
        
        # For each track, add a new measure with this header
        for track in self.current_song.tracks:
            measure = Measure(track, header)
            # Add a default voice
            voice = Voice(measure)
            measure.voices.append(voice)
            track.measures.append(measure)
            
        return len(self.current_song.measureHeaders) - 1
        
    def set_time_signature(self, measure_index: int, numerator: int, denominator: int) -> bool:
        """
        Set the time signature for a measure.
        
        Args:
            measure_index (int): Index of the measure
            numerator (int): Numerator of time signature (e.g., 4 for 4/4)
            denominator (int): Denominator of time signature (e.g., 4 for 4/4)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            return False
            
        # Ensure we have enough measure headers
        while measure_index >= len(self.current_song.measureHeaders):
            self.add_measure_header()
            
        header = self.current_song.measureHeaders[measure_index]
        
        # Set the time signature
        header.timeSignature.numerator = numerator
        header.timeSignature.denominator.value = denominator
        
        return True
        
    def set_key_signature(self, measure_index: int, key: int) -> bool:
        """
        Set the key signature for a measure.
        
        Args:
            measure_index (int): Index of the measure
            key (int): Key value (-7 to 7, where 0 is C, 1 is G, -1 is F, etc.)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            return False
            
        # Ensure we have enough measure headers
        while measure_index >= len(self.current_song.measureHeaders):
            self.add_measure_header()
            
        header = self.current_song.measureHeaders[measure_index]
        
        # Set the key signature
        header.keySignature = gp.models.KeySignature(key)
        
        return True
        
    def set_tempo(self, measure_index: int, tempo: int) -> bool:
        """
        Set the tempo for a measure.
        
        Args:
            measure_index (int): Index of the measure
            tempo (int): Tempo in BPM
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            return False
            
        # Ensure we have enough measure headers
        while measure_index >= len(self.current_song.measureHeaders):
            self.add_measure_header()
            
        header = self.current_song.measureHeaders[measure_index]
        
        # Set the tempo
        self.current_song.tempo = tempo
        
        return True

    def get_measure_info(self, track_number: int, measure_number: int) -> dict:
        """Get information about a specific measure."""
        self._ensure_song_loaded()
        if not 0 <= track_number < len(self.current_song.tracks):
            raise ValueError(f"Invalid track number: {track_number}")
            
        track = self.current_song.tracks[track_number]
        if not 0 <= measure_number < len(track.measures):
            raise ValueError(f"Invalid measure number: {measure_number}")
            
        measure = track.measures[measure_number]
        return {
            'time_signature': f"{measure.timeSignature.numerator}/{measure.timeSignature.denominator}",
            'key_signature': measure.keySignature.name,
            'repeat_start': measure.header.repeatStart,
            'repeat_end': measure.header.repeatEnd,
            'repeat_count': measure.header.repeatCount,
            'voice_count': len(measure.voices)
        } 