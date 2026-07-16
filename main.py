import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader

# Create a custom Touch/Button widget using an Image base
class PopBubble(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PopBubble, self).__init__(**kwargs)
        self.source = 'bubble_up.png' # Initial state
        self.is_popped = False
        self.allow_stretch = True
        
        # Pre-load the sound effect safely
        self.sound = SoundLoader.load('pop_sound.wav')

    def on_press(self):
        # Toggle states
        if not self.is_popped:
            self.source = 'bubble_down.png'
            self.is_popped = True
            if self.sound:
                self.sound.play()
        else:
            # Optional: Allow "unpopping" or flipping the board
            self.source = 'bubble_up.png'
            self.is_popped = False
            if self.sound:
                self.sound.play()

class PopItBoard(GridLayout):
    def __init__(self, **kwargs):
        super(PopItBoard, self).__init__(**kwargs)
        # Define a 6x6 grid for the toy
        self.cols = 6
        self.rows = 6
        self.spacing = 10
        self.padding = 20

        # Populate the board with our custom bubbles
        for _ in range(self.cols * self.rows):
            self.add_widget(PopBubble())

class PopItApp(App):
    def build(self):
        return PopItBoard()

if __name__ == '__main__':
    PopItApp().run()