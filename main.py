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
        self.sound = SoundLoader.load('pop.mp3')  # Load the pop sound effect
        
        # Sizing the bubble relative to the main red board frame container
        self.size_hint = (0.13, 0.13)  
        self.pos_hint = {'center_x': rel_x, 'center_y': rel_y}

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
        # Based on your image, let's distribute 5 rows and 5 columns evenly
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
