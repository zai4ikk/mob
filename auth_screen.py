from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from hashlib import sha256
from database import SessionLocal
from models import User
from kivy.graphics import Color, Rectangle


class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthScreen, self).__init__(**kwargs)

        # Устанавливаем размер формы как у телефона
        self.size_hint = (None, None)
        self.size = (360, 640)  # Размеры как у телефона

        # Задаем цвет фона
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Цвет фона (RGB)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Инициализация макета и элементов
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.layout.add_widget(Label(text="Авторизация", font_size=24))
        self.username_input = TextInput(hint_text="Введите логин", multiline=False)
        self.password_input = TextInput(hint_text="Введите пароль", multiline=False, password=True)
        self.login_button = Button(text="Войти")
        self.login_button.bind(on_press=self.login)

        # Кнопка для перехода на экран регистрации
        self.register_button = Button(text="Регистрация")
        self.register_button.bind(on_press=self.go_to_register)

        # Кнопка для восстановления пароля
        self.recovery_button = Button(text="Забыли пароль?")
        self.recovery_button.bind(on_press=self.go_to_recovery)

        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.register_button)
        self.layout.add_widget(self.recovery_button)
        self.add_widget(self.layout)

    def login(self, instance):
        session = SessionLocal()
        username = self.username_input.text
        password = self.password_input.text
        user = session.query(User).filter_by(username=username).first()

        if user:
            password_hash = sha256(password.encode()).hexdigest()
            if user.password_hash == password_hash:
                self.user_id = user.id
                self.manager.get_screen("wishes").user_id = user.id
                if user.role == "администратор":
                    self.manager.current = "admin"
                else:
                    self.manager.current = "wishes"
            else:
                self.layout.add_widget(Label(text="Неверный логин или пароль"))
        else:
            self.layout.add_widget(Label(text="Пользователь не найден"))

    def go_to_register(self, instance):
        self.manager.current = "register"

    def go_to_recovery(self, instance):
        self.manager.current = "recovery"
