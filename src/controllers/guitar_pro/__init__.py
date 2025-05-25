from .base_controller import GuitarProMixin
from .file_operations import FileOperationsController
from .song_operations import SongOperationsController
from .track_operations import TrackOperationsController
from .measure_operations import MeasureOperationsController
from .note_operations import NoteOperationsController

class GuitarProController(GuitarProMixin):
    """Main controller for Guitar Pro operations."""
    
    def __init__(self):
        """Initialize the controller with all operation handlers."""
        super().__init__()
        self.file_ops = FileOperationsController()
        self.song_ops = SongOperationsController()
        self.track_ops = TrackOperationsController()
        self.measure_ops = MeasureOperationsController()
        self.note_ops = NoteOperationsController()
        
    def __getattr__(self, name):
        """Delegate method calls to the appropriate operation handler."""
        # Try each operation handler in order
        for handler in [self.file_ops, self.song_ops, self.track_ops, 
                       self.measure_ops, self.note_ops]:
            if hasattr(handler, name):
                # Create a method that calls the handler's method
                def create_method(handler, method_name):
                    def method(*args, **kwargs):
                        # Update the handler's current_song before calling
                        handler.current_song = self.current_song
                        result = getattr(handler, method_name)(*args, **kwargs)
                        # Update our current_song after the call
                        self.current_song = handler.current_song
                        return result
                    return method
                return create_method(handler, name)
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'") 