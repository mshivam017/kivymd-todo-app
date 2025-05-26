import os
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import TwoLineListItem, MDList
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
import json

class ToDoListApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        self.task_list = []  # List of tuples (task_title, task_detail)
        self.selected_item = None  # Track selected item

        # Set window size (adjust as needed)
        Window.size = (320, 480)

        # Main screen
        screen = MDScreen()

        # Top layout container
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Top bar
        top_label = MDLabel(
            text="All TASK",
            font_style="H4",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White text color
            size_hint_y=None,
            height=50,
        )
        layout.add_widget(top_label)

        # Main content (MDList wrapped in ScrollView)
        scroll_view = ScrollView()
        self.task_list_view = MDList()
        scroll_view.add_widget(self.task_list_view)

        # Load tasks from file
        self.load_tasks_from_json()

        for task_title, task_detail in self.task_list:
            self.add_task_item(task_title, task_detail)

        layout.add_widget(scroll_view)

        # Bottom bar (add task button and delete button)
        bottom_bar = BoxLayout(
            orientation='horizontal', size_hint_y=None, height=50, spacing=10
        )

        add_button = MDRaisedButton(
            text="ADD TASK",
            on_release=self.add_task_dialog,
            size_hint=(0.7, None),
            height=40,
        )
        delete_icon = MDIconButton(
            icon="delete",
            on_release=self.deleteTask,
            size_hint=(0.3, None),
            height=40,
        )

        bottom_bar.add_widget(add_button)
        bottom_bar.add_widget(delete_icon)

        layout.add_widget(bottom_bar)

        screen.add_widget(layout)

        return screen

    def add_task_dialog(self, *args):
        # Dialog content with two fields: title and details
        self.dialog_content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.dialog_content.bind(minimum_height=self.dialog_content.setter("height"))

        self.title_field = MDTextField(
            hint_text="Task Title", multiline=False, size_hint_y=None, height=50
        )
        self.detail_field = MDTextField(
            hint_text="Task Details", multiline=True, size_hint_y=None, height=100
        )

        self.dialog_content.add_widget(self.title_field)
        self.dialog_content.add_widget(self.detail_field)

        # Dialog with "ADD" and "CANCEL" buttons
        self.dialog = MDDialog(
            title="Add Task",
            type="custom",
            content_cls=self.dialog_content,
            buttons=[
                MDRaisedButton(
                    text="ADD",
                    on_release=self.add_task
                ),
                MDRaisedButton(
                    text="CANCEL",
                    on_release=self.dismiss_dialog
                ),
            ],
        )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def add_task(self, *args):
        new_task_title = self.title_field.text
        new_task_detail = self.detail_field.text

        if new_task_title:
            self.task_list.append((new_task_title, new_task_detail))
            self.add_task_item(new_task_title, new_task_detail)
            self.save_tasks_to_json()
            self.dismiss_dialog()

    def add_task_item(self, task_title, task_detail):
        item = TwoLineListItem(
            text=task_title,
            secondary_text=task_detail if task_detail else "No details provided",
            on_release=self.select_task,
        )
        self.task_list_view.add_widget(item)

    def select_task(self, instance):
        if self.selected_item:
            self.selected_item.bg_color = (1, 1, 1, 1)  # Deselect previously selected item
        instance.bg_color = (0.5, 0.5, 0.5, 1)  # Select the clicked item
        self.selected_item = instance

    def deleteTask(self, *args):
        if self.selected_item:
            task_title = self.selected_item.text
            # Remove from task list
            self.task_list = [
                (title, detail) for title, detail in self.task_list if title != task_title
            ]
            self.task_list_view.remove_widget(self.selected_item)
            self.selected_item = None  # Reset selected item
            self.save_tasks_to_json()

    def load_tasks_from_json(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as json_file:
                self.task_list = json.load(json_file)
        except FileNotFoundError:
            self.task_list = []
        except json.JSONDecodeError:
            self.task_list = []

    def save_tasks_to_json(self):
        with open("tasks.json", "w", encoding="utf-8") as json_file:
            json.dump(self.task_list, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    ToDoListApp().run()
