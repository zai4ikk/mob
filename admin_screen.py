from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from database import SessionLocal
from models import Category
from kivy.graphics import Color, Rectangle

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)

        # Устанавливаем размер формы как у телефона
        self.size_hint = (None, None)
        self.size = (360, 640)  # Размеры как у телефона

        # Задаем цвет фона
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Цвет фона (RGB)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Инициализация макета и элементов
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Заголовок экрана
        self.layout.add_widget(Label(text="Управление категориями", font_size=24))

        # Поле для ввода новой категории
        self.category_input = TextInput(hint_text="Введите название категории", multiline=False)

        # Кнопка для добавления категории
        self.add_button = Button(text="Добавить категорию")
        self.add_button.bind(on_press=self.add_category)

        # Кнопка для перехода в профиль
        self.profile_button = Button(text="Перейти в профиль")
        self.profile_button.bind(on_press=self.go_to_profile)

        # Добавляем виджеты в экран
        self.layout.add_widget(self.category_input)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.profile_button)
        self.add_widget(self.layout)

    def add_category(self, instance):
        session = SessionLocal()
        category_name = self.category_input.text
        if not session.query(Category).filter_by(name=category_name).first():
            new_category = Category(name=category_name)
            session.add(new_category)
            session.commit()
            self.category_input.text = ""
        else:
            self.layout.add_widget(Label(text="Категория уже существует"))

    def go_to_profile(self, instance):
        # Переход на экран профиля
        self.manager.current = "profile"  
