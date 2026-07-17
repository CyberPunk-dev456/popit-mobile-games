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
        self.sound = SoundLoader.load('pop_sound.wav')
        
        # Define the bubble's size relative to the parent board container
        self.size_hint = (0.105, 0.16)  # Adjust this value to scale your bubble size
        
        # Position the bubble relative to the parent coordinates
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
        
        # 2. Main Toy Frame Container (Anchored in the center)
        self.toy_frame = Image(
            source='popit_maine.png',
            size_hint=(0.8, 0.8),  # Takes up 80% of the screen space
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.toy_frame)
        
        # 3. Interactive Bubble Mapping Container
        # To map coordinates cleanly, we anchor this invisible canvas directly over our toy frame
        self.bubble_overlay = FloatLayout(
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.bubble_overlay)
        
        # 4. Define the coordinate grid map matching your holes
        # (0.5, 0.5) is the absolute center of the frame. 
        # Update these layout coordinate pairs to line up with your texture design!
        hole_coordinates = [
            (0.22, 0.89), (0.33, 0.89), (0.44, 0.89), (0.55, 0.89), (0.66, 0.89), (0.77, 0.89),  # Row 1 holes
            (0.22, 0.688), (0.33, 0.688), (0.44, 0.688), (0.55, 0.688), (0.66, 0.688), (0.77, 0.688),  # Row 2 holes
            (0.22, 0.486), (0.33, 0.486), (0.44, 0.486), (0.55, 0.486), (0.66, 0.486), (0.77, 0.486),  # Row 3 holes
            (0.22, 0.284), (0.33, 0.284), (0.44, 0.284), (0.55, 0.284), (0.66, 0.284), (0.77, 0.284),   # Row 4 holes
            (0.22, 0.082), (0.33, 0.082), (0.44, 0.082), (0.55, 0.082), (0.66, 0.082), (0.77, 0.082)   # Row 5 holes
        ]
        
        for x_coord, y_coord in hole_coordinates:
            bubble = PopBubble(rel_x=x_coord, rel_y=y_coord)
            self.bubble_overlay.add_widget(bubble)

class PopItApp(App):
    def build(self):
        return PopItGame()

if __name__ == '__main__':
    PopItApp().run()
