from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class RecoveryScreen(Screen):
    def __init__(self, **kwargs):
        super(RecoveryScreen, self).__init__(**kwargs)

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
        self.title_label = Label(text="Восстановление пароля", font_size=24)
        self.layout.add_widget(self.title_label)

        # Поле для ввода email
        self.email_input = TextInput(hint_text="Введите ваш email", multiline=False)
        self.submit_button = Button(text="Отправить ссылку на восстановление")
        self.submit_button.bind(on_press=self.send_recovery_link)

        # Добавляем элементы в layout
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.submit_button)

        # Добавление layout на экран
        self.add_widget(self.layout)

    def send_recovery_link(self, instance):
        email = self.email_input.text
        # Симуляция отправки ссылки на восстановление
        recovery_message = Label(text=f"Ссылка на восстановление \nотправлена на {email}", font_size=16)

        # Добавляем сообщение под кнопкой, не перекрывая заголовок
        self.layout.add_widget(recovery_message)
