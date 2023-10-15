from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
import cv2
from functools import partial
from kivy.graphics.texture import Texture


class CameraApp(App):
    def build(self):
        layout=RelativeLayout()
        self.cap=cv2.VideoCapture(0)
        self.is_camera_active=False
        # self.image=Image()
        # layout.add_widget(self.image)
        background=Image(source="background.jpg",allow_stretch=True,keep_ratio=False)
        layout.add_widget(background)
        l1=Label(text='This is the camera',font_size='25sp',color=(1,0,1),bold=True)
        l1.pos_hint={'center_x':0.5,'center_y':0.8}
        layout.add_widget(l1)
        self.b1=Button(text='open camera',size_hint=(None,None),size=(100,100))
        self.b1.pos_hint={'center_x':0.5,'center_y':0.6}
        self.b1.bind(on_press=self.opencamera)
        layout.add_widget(self.b1)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        self.new_layout=RelativeLayout()
        self.image=Image()
        self.new_layout.add_widget(self.image)
        return layout
    
    def opencamera(self,instance):
            if not self.is_camera_active:
                self.is_camera_active=True
                self.b1.text="stop camera"

            else:
                 self.is_camera_active=False
                 self.b1.text='open camera'
            return self.new_layout
    def update(self, dt):
        if self.is_camera_active:
            ret, frame = self.cap.read()
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

    def on_stop(self):
        # Release the camera when the app is closed
        if self.cap.isOpened():
            self.cap.release()

if __name__ == '__main__':
    CameraApp().run()
