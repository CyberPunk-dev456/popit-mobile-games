from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader

class PopBubble(ButtonBehavior, Image):
    def __init__(self, rel_x, rel_y, **kwargs):
        super(PopBubble, self).__init__(**kwargs)
        self.source = 'bubble_up.png'
        self.is_popped = False
        
        # Determine the absolute directory where your main.py is running
        app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Combine the path safely to target the .ogg file
        sound_path = os.path.join(app_dir, 'pop_sound.ogg')
        
        # Load the sound cleanly
        self.sound = SoundLoader.load(sound_path
        
        # 1. Turn off automatic layout stretching for size
        self.size_hint = (None, None)  
        
        # 2. Keep the position relative to the grid
        self.pos_hint = {'center_x': rel_x, 'center_y': rel_y}
        
        # 3. Listen for whenever the parent overlay changes size (on rotation/scaling)
        self.bind(parent=self.bind_to_parent)

    def bind_to_parent(self, instance, parent):
        if parent:
            # Whenever the red board overlay changes size, recalculate bubble size
            parent.bind(size=self.match_hole_scale)
            self.match_hole_scale(parent, parent.size)

    def match_hole_scale(self, parent, parent_size):
        # Grab the total width of the red board container
        board_width = parent_size[0]
        
        # Calculate a perfect square size based purely on the board's width.
        # Change 0.14 (14%) up or down until it perfectly plugs your holes!
        bubble_dimension = board_width * 0.16  
        
        # Apply the identical width and height
        self.size = (bubble_dimension, bubble_dimension)

    def on_press(self):
        if not self.is_popped:
            self.source = 'bubble_down.png'
            self.is_popped = True
        else:
            self.source = 'bubble_up.png'
            self.is_popped = False
            
        if self.sound:
            self.sound.play()

class PopItGame(FloatLayout):
    def __init__(self, **kwargs):
        super(PopItGame, self).__init__(**kwargs)
        
        # 1. Background Layer: Wooden Table
        self.background = Image(
            source='wooden_plate.png', 
            allow_stretch=True, 
            keep_ratio=False,
            size_hint=(1, 1)
        )
        self.add_widget(self.background)
        
        # 2. Main Toy Frame (Enforce keep_ratio so it doesn't stretch weirdly)
        self.toy_frame = Image(
            source='popit_maine.png',
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            keep_ratio=True,
            allow_stretch=True
        )
        self.add_widget(self.toy_frame)
        
        # 3. Interactive Bubble Overlay Locked to Toy Frame Scale
        self.bubble_overlay = FloatLayout(
            size_hint=(None, None),  # Turn off automatic stretching
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        # Bind the overlay size to match the exact drawn image texture size
        self.toy_frame.bind(norm_image_size=self.update_overlay_size)
        self.add_widget(self.bubble_overlay)
        
        # 4. Perfectly uniform 5x5 Grid coordinates (Adjust offsets if needed)
        # Based on your image, let's distribute 5 rows and 6 columns evenly
        columns = [0.12, 0.27, 0.42, 0.57, 0.72, 0.87]
        rows =    [0.89, 0.688, 0.486, 0.284, 0.082]
        
        for y_coord in rows:
            for x_coord in columns:
                bubble = PopBubble(rel_x=x_coord, rel_y=y_coord)
                self.bubble_overlay.add_widget(bubble)

    def update_overlay_size(self, instance, value):
        # 'norm_image_size' contains the exact width and height of the image on screen
        # after keeping its aspect ratio. We force our layout to match it exactly.
        self.bubble_overlay.size = value

class PopItApp(App):
    def build(self):
        return PopItGame()

if __name__ == '__main__':
    PopItApp().run()
