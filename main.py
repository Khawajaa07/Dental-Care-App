from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.progressbar import MDProgressBar
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
from kivy.clock import Clock
from datetime import datetime, timedelta
import json
from pathlib import Path

# Define the app layout using Kivy language
KV = '''
ScreenManager:
    HomeScreen:
    AppointmentScreen:
    TipsScreen:
    BrushingTimerScreen:
    BrushingStreakScreen:

<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: 'Dental Care App'
            halign: 'center'
            font_style: 'H4'

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: [dp(20), 0]
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: 'Brushing Timer'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'brushing_timer'

        MDRectangleFlatButton:
            text: 'Brushing Streak'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'brushing_streak'
            
        MDRectangleFlatButton:
            text: 'Schedule Appointment'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'appointment'

        MDRectangleFlatButton:
            text: 'Dental Tips'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'tips'

        MDRectangleFlatButton:
            text: 'Exit'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: app.stop()


<AppointmentScreen>:
    name: 'appointment'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: 'Schedule an Appointment'
            halign: 'center'
            font_style: 'H4'

        MDTextField:
            id: date_input
            hint_text: 'Enter date (YYYY-MM-DD)'
            helper_text: 'Format: YYYY-MM-DD'

        ScrollView:
            MDList:
                id: appointments_list

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: [dp(20), 0]
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: 'Schedule'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.schedule_appointment()

        MDRectangleFlatButton:
            text: 'Back to Home'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'home'

<TipsScreen>:
    name: 'tips'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDLabel:
            text: 'Dental Care Tips'
            halign: 'center'
            font_style: 'H4'

        ScrollView:
            MDList:
                id: tips_list

        MDRectangleFlatButton:
            text: 'Back to Home'
            on_release: root.manager.current = 'home'

            
<BrushingTimerScreen>:
    name: 'brushing_timer'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: 'Brushing Timer'
            halign: 'center'
            font_style: 'H4'

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: [dp(20), 0]
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}

        MDProgressBar:
            id: progress_bar
            value: 100
            size_hint_y: None
            height: '10dp'

        MDRaisedButton:
            text: 'Start Timer'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.start_timer()

        MDRectangleFlatButton:
            text: 'Stop Timer'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.stop_timer()
            
        MDLabel:
            id: timer_label
            text: 'Ready to brush!'
            halign: 'center'

        MDRectangleFlatButton:
            text: 'Back to Home'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'home'
            

<BrushingStreakScreen>:
    name: 'brushing_streak'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: 'Brushing Streak'
            halign: 'center'
            font_style: 'H4'

        MDLabel:
            id: streak_label
            text: 'Your current brushing streak is 5 days.'
            halign: 'center'
        
        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            padding: [20, 0]
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: 'Brushed Teeth!'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.increment_streak()
            
        MDLabel:
            text: 'Complete your daily brushing to maintain your streak!'
            halign: 'center'

        MDRectangleFlatButton:
            text: 'Back to Home'
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}
            on_release: root.manager.current = 'home'
'''

# Define screens
class HomeScreen(Screen):
    pass

class AppointmentScreen(Screen):
    def on_enter(self):
        self.update_appointments_list()

    def update_appointments_list(self):
        app = MDApp.get_running_app()
        self.ids.appointments_list.clear_widgets()
        for appointment in sorted(app.appointments):
            self.ids.appointments_list.add_widget(
                OneLineListItem(text=f"Appointment scheduled for: {appointment}")
            )

    def schedule_appointment(self):
        date_input = self.ids.date_input.text.strip()
        if not date_input:
            self.show_dialog("Error", "Please enter a date.")
            return
            
        try:
            appointment_date = datetime.strptime(date_input, '%Y-%m-%d')
            if appointment_date < datetime.now():
                self.show_dialog("Error", "Please enter a future date.")
            else:
                self.show_dialog("Success", f"Appointment scheduled for {date_input}!")
                reminder_time = appointment_date - timedelta(days=1)
                Clock.schedule_once(
                    lambda dt: self.show_dialog("Reminder", "You have a dental appointment tomorrow!"),
                    (reminder_time - datetime.now()).total_seconds()
                )
        except ValueError:
            self.show_dialog("Error", "Invalid date format. Use YYYY-MM-DD.")

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.8, 0.3))
        dialog.open()

class TipsScreen(Screen):
    def on_enter(self):
        tips = [
            "Brush your teeth twice a day.",
            "Floss daily to remove plaque.",
            "Limit sugary foods and drinks.",
            "Visit your dentist regularly.",
            "Use fluoride toothpaste."
        ]
        self.ids.tips_list.clear_widgets()
        for tip in tips:
            self.ids.tips_list.add_widget(OneLineListItem(text=tip))

class BrushingTimerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_event = None
        self.remaining_time = 60  # 2 minutes in seconds
        self.dialog = None
        self.brushing_completed = False

    def start_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
        
        self.remaining_time = 60
        self.ids.progress_bar.value = 100
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        self.show_dialog("Timer Started", "Timer set for 1 minute!")

    def update_timer(self, dt):
        self.remaining_time -= 1
        progress = (self.remaining_time / 60) * 100
        self.ids.progress_bar.value = progress

        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.ids.timer_label.text = f"Time remaining: {minutes:02d}:{seconds:02d}"
        
        if self.remaining_time <= 0:
            self.timer_event.cancel()
            self.timer_event = None
            self.show_dialog("Time's up!", "Great job brushing your teeth!")
            self.ids.timer_label.text = "Ready to brush!"
            self.manager.get_screen('brushing_streak').increment_streak()
            return False
        

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
            self.show_dialog("Timer Stopped", "Timer cancelled!")

    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.3),
            buttons=[
                MDRectangleFlatButton(
                    text="STOP",
                    on_release=lambda x: self.stop_timer()
                )
            ]
        )
        self.dialog.open()

    def on_leave(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None


class BrushingStreakScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.streak_count = 0
        self.last_brush_date = None
        self.max_streak = 0

    def on_enter(self):
        self.update_streak_display()

    def update_streak_display(self):
        streak_label = self.ids.streak_label
        streak_label.text = f'Your current brushing streak is {self.streak_count} days!'

    def increment_streak(self):
        try:
            today = datetime.now().date()
            if not self.last_brush_date:
                self.streak_count = 1
            elif (today - self.last_brush_date).days == 1:
                self.streak_count += 1
                self.max_streak = max(self.max_streak, self.streak_count)
            elif (today - self.last_brush_date).days > 1:
                self.streak_count = 1
            elif (today - self.last_brush_date).days == 0:
                return  # Already brushed today
                
            self.last_brush_date = today
            self.update_streak_display()
            self.show_streak_achievement()
        except Exception as e:
            print(f"Error updating streak: {str(e)}")

    def show_streak_achievement(self):
        if self.streak_count in [7, 14, 30, 50, 75, 100]:
            dialog = MDDialog(
                title="Streak Achievement",
                text = f"Congratulations!, You have brushed your teeth for {self.streak_count} days in a row!",
                size_hint=(0.8, 0.3))
        dialog.open()

# Main App
class DentalCareApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = Path('dental_app_data.json')
        self.appointments = []
        self.load_data()

    def load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                screen = self.root.get_screen('brushing_streak') if self.root else None
                if screen:
                    screen.streak_count = data.get('streak_count', 0)
                    last_brush = data.get('last_brush_date')
                    if last_brush:
                        screen.last_brush_date = datetime.strptime(last_brush, '%Y-%m-%d').date()
                self.appointments = data.get('appointments', [])

    def save_data(self):
        screen = self.root.get_screen('brushing_streak')
        data = {
            'streak_count': screen.streak_count,
            'last_brush_date': screen.last_brush_date.strftime('%Y-%m-%d') if screen.last_brush_date else None,
            'appointments': self.appointments
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def on_stop(self):
        self.save_data()

# Run the app
if __name__ == '__main__':
    DentalCareApp().run()