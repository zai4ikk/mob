from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle  # Добавляем импорты для работы с цветами и прямоугольниками
from database import SessionLocal
from models import Wish, Category

class WishesScreen(Screen):
    def __init__(self, **kwargs):
        super(WishesScreen, self).__init__(**kwargs)

        # Устанавливаем размер экрана
        self.size_hint = (None, None)
        self.size = (360, 640)  # Размеры экрана под мобильное устройство

        # Задаем цвет фона
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Цвет фона (RGB)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.user_id = None  # Инициализируем user_id, который будет устанавливаться из AuthScreen

        # Добавим кнопку для создания желания
        self.add_wish_button = Button(text="Добавить желание")
        self.add_wish_button.bind(on_press=self.add_wish)
        self.layout.add_widget(self.add_wish_button)

        # Кнопка для перехода в профиль
        self.profile_button = Button(text="Перейти в профиль")
        self.profile_button.bind(on_press=self.go_to_profile)

        # Используем BoxLayout для списка желаний
        self.wish_list = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint_y=None)
        self.wish_list.bind(minimum_height=self.wish_list.setter('height'))  # Делаем размер динамичным

        # Оборачиваем список желаний в ScrollView для прокрутки
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.wish_list)
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.profile_button)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        """Метод вызывается перед тем, как экран станет активным, обновляем список желаний"""
        self.refresh_wishes()

    def refresh_wishes(self):
        """Обновляет список желаний для текущего пользователя"""
        if not self.user_id:
            return

        session = SessionLocal()
        wishes = session.query(Wish).filter_by(user_id=self.user_id).all()

        # Очистим текущий список желаний перед добавлением новых
        self.wish_list.clear_widgets()

        # Добавляем желания пользователя в список
        for wish in wishes:
            wish_text = f"Заголовок: {wish.title}\nОписание: {wish.description}\nКатегория: {wish.category.name}"

            # Используем Label с размером шрифта и отступами
            label = Label(
                text=wish_text,
                size_hint_y=None,
                height=100,
                padding=(10, 10),
                text_size=(self.width - 20, None),  # Ограничиваем размер текста по ширине
                halign='left',  # Выравнивание текста по левому краю
                valign='top'  # Выравнивание текста по верхнему краю
            )
            label.bind(texture_size=label.setter('size'))  # Автоматическое изменение размера метки по тексту
            self.wish_list.add_widget(label)

    def add_wish(self, instance):
        """Открывает диалоговое окно для добавления нового желания"""
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Поля для ввода заголовка и описания желания
        self.title_input = TextInput(hint_text="Введите заголовок желания", multiline=False)
        self.description_input = TextInput(hint_text="Введите описание желания", multiline=True)

        # Получаем список категорий из базы данных
        session = SessionLocal()
        categories = session.query(Category).all()

        # Добавляем Spinner для выбора категории
        self.category_spinner = Spinner(
            text='Выберите категорию',
            values=[category.name for category in categories]
        )

        # Кнопка для сохранения нового желания
        save_button = Button(text="Сохранить желание")
        save_button.bind(on_press=self.save_wish)

        # Кнопка для отмены добавления желания
        cancel_button = Button(text="Отмена")
        cancel_button.bind(on_press=self.close_popup)

        content.add_widget(self.title_input)
        content.add_widget(self.description_input)
        content.add_widget(self.category_spinner)
        content.add_widget(save_button)
        content.add_widget(cancel_button)

        # Создаем попап с полями ввода и кнопками
        self.popup = Popup(
            title="Добавить новое желание",
            content=content,
            size_hint=(None, None),  # Убираем пропорциональность для фиксированных размеров
            size=(360, 640),  # Устанавливаем размеры попапа как у экрана
            background_color=(0.2, 0.6, 0.8, 1),  # Цвет фона аналогичный остальным экранам
            separator_height=10  # Добавим разделитель между контентом и кнопками
        )
        self.popup.open()

    def save_wish(self, instance):
        """Сохраняет новое желание в базе данных"""
        title = self.title_input.text
        description = self.description_input.text
        category_name = self.category_spinner.text

        # Проверка, чтобы поля не были пустыми
        if title and description and category_name != "Выберите категорию":
            session = SessionLocal()

            # Находим категорию по названию
            category = session.query(Category).filter_by(name=category_name).first()

            if category:
                # Создаем новый объект желания, передавая category_id
                new_wish = Wish(
                    title=title,
                    description=description,
                    user_id=self.user_id,  # Используем user_id
                    category_id=category.id  # передаем только ID категории
                )

                # Добавляем желание в базу данных
                session.add(new_wish)
                session.commit()

                # Закрываем попап и обновляем список желаний
                self.popup.dismiss()
                self.refresh_wishes()
            else:
                # Если категория не найдена
                self.show_error_popup("Выберите корректную категорию!")
        else:
            # Если поля пустые
            self.show_error_popup("Заполните все поля и выберите категорию!")

    def show_error_popup(self, message):
        """Показывает всплывающее окно с ошибкой"""
        error_popup = Popup(title="Ошибка", content=Label(text=message), size_hint=(0.6, 0.4))
        error_popup.open()

    def close_popup(self, instance):
        """Закрывает попап, если пользователь нажал 'Отмена'"""
        self.popup.dismiss()

    def on_enter(self):
        """Метод, вызываемый при входе в экран"""
        # Получаем user_id из AuthScreen
        auth_screen = self.manager.get_screen('auth')
        self.user_id = auth_screen.user_id  # Устанавливаем user_id из AuthScreen
        self.refresh_wishes()  # Обновляем список желаний

    def go_to_profile(self, instance):
        # Переход на экран профиля
        self.manager.current = "profile"
