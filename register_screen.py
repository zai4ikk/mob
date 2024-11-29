from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from database import SessionLocal
from models import User
from hashlib import sha256


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)

        # Устанавливаем размер экрана
        self.size_hint = (None, None)
        self.size = (360, 640)  # Размеры экрана под мобильное устройство

        # Задаем цвет фона
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Цвет фона (RGB)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Создаем макет
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Добавляем заголовок экрана
        self.layout.add_widget(Label(text="Регистрация", font_size=24))
        self.username_input = TextInput(hint_text="Введите логин", multiline=False)
        self.email_input = TextInput(hint_text="Введите email", multiline=False)
        self.password_input = TextInput(hint_text="Введите пароль", multiline=False, password=True)

        # Добавляем выбор роли
        self.role_spinner = Spinner(
            text="Выберите роль",
            values=("пользователь", "администратор"),
            size_hint=(None, None),
            size=(200, 44)
        )

        # Кнопка регистрации
        self.register_button = Button(text="Зарегистрироваться")
        self.register_button.bind(on_press=self.register)

        # Добавляем все виджеты в макет
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.role_spinner)
        self.layout.add_widget(self.register_button)
        self.add_widget(self.layout)

    def register(self, instance):
        session = SessionLocal()
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        role = self.role_spinner.text

        # Проверка на заполненность полей
        if not username or not email or not password or role == "Выберите роль":
            self.layout.add_widget(Label(text="Все поля должны быть заполнены!"))
            return

        password_hash = sha256(password.encode()).hexdigest()

        # Проверяем уникальность логина и email
        if session.query(User).filter_by(username=username).first():
            self.layout.add_widget(Label(text="Логин уже существует"))
        elif session.query(User).filter_by(email=email).first():
            self.layout.add_widget(Label(text="Email уже зарегистрирован"))
        else:
            # Создаем нового пользователя
            new_user = User(username=username, email=email, password_hash=password_hash, role=role)
            session.add(new_user)
            session.commit()
            self.manager.current = "auth"  # Переход к экрану авторизации
