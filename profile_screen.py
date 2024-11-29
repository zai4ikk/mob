from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from database import SessionLocal
from models import User

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)

        # Устанавливаем размер формы как у телефона
        self.size_hint = (None, None)
        self.size = (360, 640)  # Размеры как у телефона

        # Задаем цвет фона
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Цвет фона (RGB)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Инициализация макета и элементов
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Профиль пользователя
        self.profile_label = Label(text="Профиль пользователя", font_size=24)
        self.username_label = Label(text="Логин:")
        self.email_label = Label(text="Email:")
        self.role_label = Label(text="Роль:")
        self.logout_button = Button(text="Выйти")
        self.logout_button.bind(on_press=self.logout)

        # Добавляем все виджеты на экран
        self.layout.add_widget(self.profile_label)
        self.layout.add_widget(self.username_label)
        self.layout.add_widget(self.email_label)
        self.layout.add_widget(self.role_label)
        self.layout.add_widget(self.logout_button)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        """Этот метод вызывается перед тем, как экран станет активным, обновляем данные профиля и желаний"""
        self.refresh_profile()

    def refresh_profile(self):
        """Обновляет информацию о профиле пользователя"""
        session = SessionLocal()
        user_id = self.manager.get_screen("auth").user_id  # Получаем user_id из AuthScreen
        user = session.query(User).filter_by(id=user_id).first()

        if user:
            # Обновляем метки профиля
            self.username_label.text = f"Логин: {user.username}"
            self.email_label.text = f"Email: {user.email}"
            self.role_label.text = f"Роль: {user.role}"
        else:
            # Если пользователь не найден, показываем сообщение об ошибке
            self.username_label.text = "Логин: Не найден"
            self.email_label.text = "Email: Не найден"
            self.role_label.text = "Роль: Не найден"

    def logout(self, instance):
        """Метод выхода из системы"""
        self.manager.current = "auth"  # Переводим на экран авторизации
