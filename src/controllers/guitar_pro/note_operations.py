from .base_controller import GuitarProMixin
from guitarpro.models import Note, Beat, Voice, Duration

class NoteOperationsController(GuitarProMixin):
    """Controller for Guitar Pro note operations."""
    
    def add_note(self, track_index: int, measure_index: int, string: int, fret: int, 
                 duration: int = 4, voice_index: int = 0, beat_index: int = 0) -> bool:
        """
        Add a note to a specific track, measure, and string.
        
        Args:
            track_index (int): Index of the track
            measure_index (int): Index of the measure
            string (int): String number (1-based)
            fret (int): Fret number
            duration (int): Duration value (1=whole, 2=half, 4=quarter, 8=eighth, etc.)
            voice_index (int): Index of the voice
            beat_index (int): Index of the beat
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
            
        try:
            if track_index < 0 or track_index >= len(self.current_song.tracks):
                return False
                
            track = self.current_song.tracks[track_index]
            
            if measure_index < 0 or measure_index >= len(track.measures):
                return False
                
            measure = track.measures[measure_index]
            
            # Ensure we have enough voices
            while len(measure.voices) <= voice_index:
                measure.voices.append(Voice(measure))
            
            voice = measure.voices[voice_index]
            
            # Create a new beat if needed
            if beat_index >= len(voice.beats):
                # Create a new beat with the specified duration
                duration_obj = Duration()
                duration_obj.value = duration
                
                new_beat = Beat(voice)
                new_beat.duration = duration_obj
                
                # Add the beat to the voice
                voice.beats.append(new_beat)
            
            beat = voice.beats[beat_index]
            
            # Create a new note
            note = Note(beat)
            note.value = fret
            note.string = string
            
            # Add the note to the beat
            beat.notes.append(note)
            
            return True
        
        except Exception as e:
            print(f"Error adding note: {e}")
            return False
            
    def add_note_simple(self, track_index: int, measure_index: int, beat_index: int, 
                string: int, fret: int, duration: int = 4) -> bool:
        """
        Add a note to the song (simplified version).
        
        Args:
            track_index (int): Index of the track
            measure_index (int): Index of the measure
            beat_index (int): Index of the beat
            string (int): String number (1-6, where 1 is the highest string)
            fret (int): Fret number (0 = open string)
            duration (int): Duration value (1=whole, 2=half, 4=quarter, 8=eighth, etc.)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            self.create_new_song()
            
        if track_index < 0 or track_index >= len(self.current_song.tracks):
            return False
            
        track = self.current_song.tracks[track_index]
        
        # Ensure we have enough measures
        while measure_index >= len(track.measures):
            self.add_measure_header()
            
        measure = track.measures[measure_index]
        
        # Ensure we have at least one voice
        if not measure.voices:
            voice = Voice(measure)
            measure.voices.append(voice)
        voice = measure.voices[0]
        
        # Ensure we have enough beats
        while beat_index >= len(voice.beats):
            beat = Beat(voice)
            beat.duration = Duration()
            beat.duration.value = duration
            voice.beats.append(beat)
            
        beat = voice.beats[beat_index]
        
        # Create the note
        note = Note(beat)
        note.string = string
        note.value = fret
        beat.notes.append(note)
        
        return True 

    def get_note_info(self, track_number: int, measure_number: int, voice_number: int, note_number: int) -> dict:
        """Get information about a specific note."""
        self._ensure_song_loaded()
        if not 0 <= track_number < len(self.current_song.tracks):
            raise ValueError(f"Invalid track number: {track_number}")
            
        track = self.current_song.tracks[track_number]
        if not 0 <= measure_number < len(track.measures):
            raise ValueError(f"Invalid measure number: {measure_number}")
            
        measure = track.measures[measure_number]
        if not 0 <= voice_number < len(measure.voices):
            raise ValueError(f"Invalid voice number: {voice_number}")
            
        voice = measure.voices[voice_number]
        if not 0 <= note_number < len(voice.beats):
            raise ValueError(f"Invalid note number: {note_number}")
            
        note = voice.beats[note_number].notes[0]  # Assuming first note in beat
        return {
            'value': note.value,
            'string': note.string,
            'velocity': note.velocity,
            'duration': note.durationPercent,
            'is_ghost': note.isGhostNote,
            'is_dead': note.isDeadNote,
            'is_hammer_on': note.isHammerOn,
            'is_pull_off': note.isPullOff,
            'is_slide': note.isSlide
        } 

    def add_note_with_effects(self, track_index: int, measure_index: int, string: int, fret: int, duration: int = 4, voice_index: int = 0, beat_index: int = 0, is_bend: bool = False, is_harmonic: bool = False, is_slide: bool = False, is_vibrato: bool = False, is_ghost: bool = False, is_dead: bool = False, is_hammer_on: bool = False, is_pull_off: bool = False) -> bool:
        """
        Add a note with advanced effects to a specific track, measure, and string.
        
        Args:
            track_index (int): Index of the track
            measure_index (int): Index of the measure
            string (int): String number (1-based)
            fret (int): Fret number
            duration (int): Duration value (1=whole, 2=half, 4=quarter, 8=eighth, etc.)
            voice_index (int): Index of the voice
            beat_index (int): Index of the beat
            is_bend (bool): Whether the note has a bend effect
            is_harmonic (bool): Whether the note has a harmonic effect
            is_slide (bool): Whether the note has a slide effect
            is_vibrato (bool): Whether the note has a vibrato effect
            is_ghost (bool): Whether the note is a ghost note
            is_dead (bool): Whether the note is a dead note
            is_hammer_on (bool): Whether the note has a hammer-on effect
            is_pull_off (bool): Whether the note has a pull-off effect
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_song is None:
            print("No song loaded")
            return False
        
        try:
            if track_index < 0 or track_index >= len(self.current_song.tracks):
                return False
            
            track = self.current_song.tracks[track_index]
            
            if measure_index < 0 or measure_index >= len(track.measures):
                return False
            
            measure = track.measures[measure_index]
            
            # Ensure we have enough voices
            while len(measure.voices) <= voice_index:
                measure.voices.append(Voice(measure))
            
            voice = measure.voices[voice_index]
            
            # Create a new beat if needed
            if beat_index >= len(voice.beats):
                # Create a new beat with the specified duration
                duration_obj = Duration()
                duration_obj.value = duration
                
                new_beat = Beat(voice)
                new_beat.duration = duration_obj
                
                # Add the beat to the voice
                voice.beats.append(new_beat)
            
            beat = voice.beats[beat_index]
            
            # Create a new note
            note = Note(beat)
            note.value = fret
            note.string = string
            
            # Set advanced effects
            if is_bend:
                note.effect.bend = True
            if is_harmonic:
                note.effect.isHarmonic = True
            if is_slide:
                note.effect.isSlide = True
            if is_vibrato:
                note.effect.isVibrato = True
            if is_ghost:
                note.effect.isGhostNote = True
            if is_dead:
                note.effect.isDeadNote = True
            if is_hammer_on:
                note.effect.isHammerOn = True
            if is_pull_off:
                note.effect.isPullOff = True
            
            # Add the note to the beat
            beat.notes.append(note)
            
            return True
        
        except Exception as e:
            print(f"Error adding note with effects: {e}")
            return False 