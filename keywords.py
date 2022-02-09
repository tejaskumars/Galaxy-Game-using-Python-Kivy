from kivy.uix.relativelayout import RelativeLayout

def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None


def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_SPEED_X = self.SPEED_x
        elif keycode[1] == 'right':
             self.current_SPEED_X = -self.SPEED_x
        elif keycode[1] == "enter":
            self.on_menu_button_pressed()


def _on_keyboard_up(self, keyboard, keycode):
        self.current_SPEED_X = 0

def on_touch_down(self, touch):
    game_over = False
    game_is_on = False
    if not self.game_over and self.game_is_on:
        if touch.x < self.width/2:
            self.current_SPEED_X = self.SPEED_x
        else:
            self.current_SPEED_X = -self.SPEED_x

    return super(RelativeLayout, self).on_touch_down(touch)
        

def on_touch_up(self, touch):
        self.current_SPEED_X = 0
