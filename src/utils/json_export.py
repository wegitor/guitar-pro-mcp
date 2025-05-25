"""
JSON export/import utility for Guitar Pro files.

This module provides functions to convert Guitar Pro song objects to and from JSON format,
allowing for easier interchange with other systems.
"""

import os
import json
from typing import Dict, List, Any, Optional

def song_to_json(song) -> Dict[str, Any]:
    """
    Convert a Guitar Pro song to a JSON-serializable dictionary.
    
    Args:
        song: Guitar Pro song object
        
    Returns:
        dict: JSON-serializable dictionary representing the song
    """
    if song is None:
        return {}
    
    # Basic song metadata
    song_data = {
        "metadata": {
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "author": song.author,
            "copyright": song.copyright,
            "transcriber": song.transcriber,
            "instructions": song.instructions,
            "comments": song.comments,
            "tempo": song.tempo
        },
        "tracks": []
    }
    
    # Process tracks
    for track_index, track in enumerate(song.tracks):
        track_data = {
            "name": track.name,
            "index": track_index,
            "is_percussion": track.isPercussionTrack,
            "channel": {
                "instrument": track.channel.instrument,
                "volume": track.channel.volume,
                "balance": track.channel.balance,
                "chorus": track.channel.chorus,
                "reverb": track.channel.reverb,
                "phaser": track.channel.phaser,
                "tremolo": track.channel.tremolo
            },
            "strings": [],
            "measures": []
        }
        
        # Add string tunings
        for string in track.strings:
            track_data["strings"].append({
                "number": string.number,
                "value": string.value
            })
        
        # Process measures, voices, beats, and notes
        for measure_index, measure in enumerate(track.measures):
            measure_data = {
                "index": measure_index,
                "voices": []
            }
            
            for voice_index, voice in enumerate(measure.voices):
                voice_data = {
                    "index": voice_index,
                    "beats": []
                }
                
                for beat_index, beat in enumerate(voice.beats):
                    beat_data = {
                        "index": beat_index,
                        "duration": {
                            "value": beat.duration.value,
                            "is_dotted": beat.duration.isDotted,
                            "is_rest": beat.duration.isRest
                        },
                        "notes": []
                    }
                    
                    for note in beat.notes:
                        note_data = {
                            "string": note.string,
                            "value": note.value,
                            "velocity": note.velocity,
                            "is_tied": note.isTiedNote,
                            "is_rest": note.type == gp.models.NoteType.rest,
                            "effect": {}
                        }
                        
                        # Add note effects if present
                        if note.effect:
                            if note.effect.isBend:
                                note_data["effect"]["bend"] = True
                            if note.effect.isHarmonic:
                                note_data["effect"]["harmonic"] = True
                            if note.effect.isGhostNote:
                                note_data["effect"]["ghost"] = True
                            if note.effect.isSlide:
                                note_data["effect"]["slide"] = True
                            if note.effect.isVibrato:
                                note_data["effect"]["vibrato"] = True
                            # Add more effects as needed
                        
                        beat_data["notes"].append(note_data)
                    
                    voice_data["beats"].append(beat_data)
                
                measure_data["voices"].append(voice_data)
            
            track_data["measures"].append(measure_data)
        
        song_data["tracks"].append(track_data)
    
    return song_data

def export_to_json(song, file_path: str) -> bool:
    """
    Export a Guitar Pro song to a JSON file.
    
    Args:
        song: Guitar Pro song object
        file_path (str): Path to save the JSON file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        song_data = song_to_json(song)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(song_data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False

def json_to_song(json_data: Dict[str, Any], gp) -> Any:
    """
    Convert JSON data to a Guitar Pro song object.
    
    Args:
        json_data (dict): JSON data representing a Guitar Pro song
        gp: Guitar Pro module (guitarpro)
        
    Returns:
        Any: Guitar Pro song object
    """
    try:
        # Create a new song
        song = gp.models.Song()
        
        # Set metadata
        metadata = json_data.get("metadata", {})
        song.title = metadata.get("title", "")
        song.artist = metadata.get("artist", "")
        song.album = metadata.get("album", "")
        song.author = metadata.get("author", "")
        song.copyright = metadata.get("copyright", "")
        song.transcriber = metadata.get("transcriber", "")
        song.instructions = metadata.get("instructions", "")
        song.comments = metadata.get("comments", "")
        song.tempo = metadata.get("tempo", 120)
        
        # Process tracks
        for track_data in json_data.get("tracks", []):
            track = gp.models.Track()
            track.name = track_data.get("name", "Track")
            track.isPercussionTrack = track_data.get("is_percussion", False)
            
            # Set channel properties
            channel_data = track_data.get("channel", {})
            track.channel.instrument = channel_data.get("instrument", 0)
            track.channel.volume = channel_data.get("volume", 100)
            track.channel.balance = channel_data.get("balance", 0)
            track.channel.chorus = channel_data.get("chorus", 0)
            track.channel.reverb = channel_data.get("reverb", 0)
            track.channel.phaser = channel_data.get("phaser", 0)
            track.channel.tremolo = channel_data.get("tremolo", 0)
            
            # Add strings
            for string_data in track_data.get("strings", []):
                string = gp.models.GuitarString()
                string.number = string_data.get("number", 1)
                string.value = string_data.get("value", 64)
                track.strings.append(string)
            
            # Add measures, voices, beats, and notes
            for measure_data in track_data.get("measures", []):
                measure = gp.models.Measure(track)
                
                # Set up the measure header if it's the first track
                if len(song.tracks) == 0:
                    header = gp.models.MeasureHeader()
                    song.measureHeaders.append(header)
                    measure.header = header
                else:
                    # Use existing header for additional tracks
                    measure_index = measure_data.get("index", 0)
                    if measure_index < len(song.measureHeaders):
                        measure.header = song.measureHeaders[measure_index]
                
                for voice_data in measure_data.get("voices", []):
                    voice = gp.models.Voice(measure)
                    
                    for beat_data in voice_data.get("beats", []):
                        beat = gp.models.Beat(voice)
                        
                        # Set duration
                        duration_data = beat_data.get("duration", {})
                        duration = gp.models.Duration()
                        duration.value = duration_data.get("value", 4)
                        duration.isDotted = duration_data.get("is_dotted", False)
                        duration.isRest = duration_data.get("is_rest", False)
                        beat.duration = duration
                        
                        # Add notes
                        for note_data in beat_data.get("notes", []):
                            note = gp.models.Note(beat)
                            note.string = note_data.get("string", 1)
                            note.value = note_data.get("value", 0)
                            note.velocity = note_data.get("velocity", 100)
                            note.isTiedNote = note_data.get("is_tied", False)
                            if note_data.get("is_rest", False):
                                note.type = gp.models.NoteType.rest
                            
                            # Set note effects
                            effect_data = note_data.get("effect", {})
                            if effect_data:
                                effect = gp.models.NoteEffect()
                                if effect_data.get("bend", False):
                                    effect.isBend = True
                                if effect_data.get("harmonic", False):
                                    effect.isHarmonic = True
                                if effect_data.get("ghost", False):
                                    effect.isGhostNote = True
                                if effect_data.get("slide", False):
                                    effect.isSlide = True
                                if effect_data.get("vibrato", False):
                                    effect.isVibrato = True
                                note.effect = effect
                            
                            beat.notes.append(note)
                        
                        voice.beats.append(beat)
                    
                    measure.voices.append(voice)
                
                track.measures.append(measure)
            
            song.tracks.append(track)
        
        return song
    except Exception as e:
        print(f"Error converting JSON to song: {e}")
        return None

def import_from_json(file_path: str, gp) -> Optional[Any]:
    """
    Import a song from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        gp: Guitar Pro module (guitarpro)
        
    Returns:
        Optional[Any]: Guitar Pro song object, or None if import fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        return json_to_song(json_data, gp)
    except Exception as e:
        print(f"Error importing from JSON: {e}")
        return None
