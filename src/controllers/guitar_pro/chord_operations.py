from .base_controller import GuitarProMixin
from guitarpro.models import Chord, Barre, PitchClass, ChordType, ChordExtension, ChordAlteration, Fingering

class ChordOperationsController(GuitarProMixin):
    """Controller for Guitar Pro chord operations."""

    def add_chord(self, track_index: int, measure_index: int, beat_index: int, chord_data: dict) -> bool:
        """
        Add a chord to a specific beat.
        
        Args:
            track_index (int): Index of the track
            measure_index (int): Index of the measure
            beat_index (int): Index of the beat
            chord_data (dict): A dictionary containing chord properties
            
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
            
            if beat_index < 0 or beat_index >= len(measure.voices[0].beats):
                return False
                
            beat = measure.voices[0].beats[beat_index]
            
            # Create a new chord
            chord = Chord()
            
            # Set chord properties
            if "name" in chord_data:
                chord.name = chord_data["name"]
            if "root" in chord_data:
                chord.root = PitchClass(chord_data["root"])
            if "type" in chord_data:
                chord.type = ChordType(chord_data["type"])
            if "extension" in chord_data:
                chord.extension = ChordExtension(chord_data["extension"])
            if "bass" in chord_data:
                chord.bass = PitchClass(chord_data["bass"])
            if "tonality" in chord_data:
                chord.tonality = ChordAlteration(chord_data["tonality"])
            if "fifth" in chord_data:
                chord.fifth = ChordAlteration(chord_data["fifth"])
            if "ninth" in chord_data:
                chord.ninth = ChordAlteration(chord_data["ninth"])
            if "eleventh" in chord_data:
                chord.eleventh = ChordAlteration(chord_data["eleventh"])
            if "firstFret" in chord_data:
                chord.firstFret = chord_data["firstFret"]
            if "strings" in chord_data:
                chord.strings = chord_data["strings"]
            if "barres" in chord_data:
                for barre_data in chord_data["barres"]:
                    barre = Barre()
                    barre.fret = barre_data["fret"]
                    barre.startString = barre_data["startString"]
                    barre.endString = barre_data["endString"]
                    chord.barres.append(barre)
            if "fingerings" in chord_data:
                for fingering_data in chord_data["fingerings"]:
                    fingering = Fingering()
                    fingering.finger = fingering_data["finger"]
                    fingering.string = fingering_data["string"]
                    chord.fingerings.append(fingering)
            
            # Add the chord to the beat
            beat.effect.chord = chord
            
            return True
            
        except Exception as e:
            print(f"Error adding chord: {e}")
            return False

    def get_chord(self, track_index: int, measure_index: int, beat_index: int) -> dict:
        """
        Get the chord from a specific beat.
        
        Args:
            track_index (int): Index of the track
            measure_index (int): Index of the measure
            beat_index (int): Index of the beat
            
        Returns:
            dict: A dictionary containing chord properties, or an empty dict if no chord is found
        """
        if self.current_song is None:
            return {}
            
        try:
            if track_index < 0 or track_index >= len(self.current_song.tracks):
                return {}
                
            track = self.current_song.tracks[track_index]
            
            if measure_index < 0 or measure_index >= len(track.measures):
                return {}
                
            measure = track.measures[measure_index]
            
            if beat_index < 0 or beat_index >= len(measure.voices[0].beats):
                return {}
                
            beat = measure.voices[0].beats[beat_index]
            
            if not beat.effect.isChord:
                return {}
                
            chord = beat.effect.chord
            
            return {
                "name": chord.name,
                "root": str(chord.root) if chord.root else None,
                "type": chord.type.name if chord.type else None,
                "extension": chord.extension.name if chord.extension else None,
                "bass": str(chord.bass) if chord.bass else None,
                "tonality": chord.tonality.name if chord.tonality else None,
                "fifth": chord.fifth.name if chord.fifth else None,
                "ninth": chord.ninth.name if chord.ninth else None,
                "eleventh": chord.eleventh.name if chord.eleventh else None,
                "firstFret": chord.firstFret,
                "strings": chord.strings,
                "barres": [{"fret": barre.fret, "startString": barre.startString, "endString": barre.endString} for barre in chord.barres],
                "fingerings": [{"finger": fingering.finger, "string": fingering.string} for fingering in chord.fingerings]
            }
            
        except Exception as e:
            print(f"Error getting chord: {e}")
            return {} 