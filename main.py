from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.auth_screen import AuthScreen
from screens.register_screen import RegisterScreen
from screens.profile_screen import ProfileScreen
from screens.wishes_screen import WishesScreen
from screens.admin_screen import AdminScreen
from screens.recovery_screen import RecoveryScreen
from database import init_db

# Initialize the database
init_db()

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AuthScreen(name="auth"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(WishesScreen(name="wishes"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(RecoveryScreen(name="recovery"))
        return sm

if __name__ == "__main__":
    MainApp().run()
