"""
MIDI export utility for Guitar Pro files.

This module provides a function to export Guitar Pro song objects to MIDI files.
It acts as a wrapper around the PyGuitarPro library and adds MIDI export functionality.
"""

import os
import mido
from typing import List, Dict, Any

def convert_to_midi(song, output_path: str) -> bool:
    """
    Convert a Guitar Pro song to a MIDI file.
    
    Args:
        song: Guitar Pro song object
        output_path (str): Path to save the MIDI file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create a new MIDI file
        midi_file = mido.MidiFile()
        
        # Add a track for each Guitar Pro track
        for track in song.tracks:
            # Skip drum tracks for simplicity
            if track.isPercussionTrack:
                continue
                
            # Create a MIDI track
            midi_track = mido.MidiTrack()
            midi_file.tracks.append(midi_track)
            
            # Add track name
            midi_track.append(mido.MetaMessage('track_name', name=track.name))
            
            # Set instrument
            program = track.channel.instrument
            midi_track.append(mido.Message('program_change', program=program))
            
            # Current tick position
            current_tick = 0
            ticks_per_beat = 480  # Standard MIDI resolution
            
            # Process measures, voices, beats, and notes
            for measure in track.measures:
                for voice in measure.voices:
                    for beat in voice.beats:
                        # Skip empty beats
                        if not beat.notes:
                            continue
                            
                        # Calculate duration in ticks
                        duration_value = beat.duration.value
                        tick_duration = int(4 * ticks_per_beat / duration_value)
                        
                        # Adjust for dotted notes
                        if beat.duration.isDotted:
                            tick_duration = int(tick_duration * 1.5)
                        
                        # Add note_on events for all notes in the beat
                        for note in beat.notes:
                            # Get the actual pitch by adding fret value to the string tuning
                            string_tuning = 0
                            for string in track.strings:
                                if string.number == note.string:
                                    string_tuning = string.value
                                    break
                            
                            # Calculate the MIDI note value
                            pitch = string_tuning + note.value
                            
                            # Add note_on message
                            velocity = 64 + note.velocity
                            if velocity > 127:
                                velocity = 127
                                
                            midi_track.append(mido.Message('note_on', 
                                                          note=pitch, 
                                                          velocity=velocity, 
                                                          time=0 if len(midi_track) > 0 else 0))
                            
                            # Add note_off message after the duration
                            midi_track.append(mido.Message('note_off', 
                                                          note=pitch, 
                                                          velocity=0, 
                                                          time=tick_duration))
        
        # Save the MIDI file
        midi_file.save(output_path)
        return True
        
    except Exception as e:
        print(f"Error converting to MIDI: {e}")
        return False
