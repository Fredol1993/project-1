import kivy
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import datetime

kivy.require('2.0.0')

class BMICalculator(App):
    def build(self):
        self.title = 'Advanced BMI Calculator'
        self.root = BoxLayout(orientation='vertical', spacing=10)
        
        self.title_label = Label(
            text='BMI CALCULATOR',
            font_size=32,
            color=(0.12, 0.58, 0.95, 1)  # Blue text color
        )
        self.root.add_widget(self.title_label)

        self.result_label = Label(
            text='Your BMI will appear here',
            font_size=24,
            markup=True,
            color=(0.2, 0.8, 0.2, 1)  # Green text color
        )
        self.root.add_widget(self.result_label)

        input_layout = GridLayout(cols=2, spacing=10)

        self.weight_label = Label(
            text='Enter your weight (kg):',
            font_size=18,
            halign='right',
            color=(0.12, 0.12, 0.95, 1)  # Dark blue text color
        )
        self.weight_input = TextInput(
            font_size=18,
            background_color=(0.9, 0.9, 1, 1)  # Light blue background
        )
        input_layout.add_widget(self.weight_label)
        input_layout.add_widget(self.weight_input)

        self.height_label = Label(
            text='Enter your height (cm):',
            font_size=18,
            halign='right',
            color=(0.12, 0.12, 0.95, 1)  # Dark blue text color
        )
        self.height_input = TextInput(
            font_size=18,
            background_color=(0.9, 0.9, 1, 1)  # Light blue background
        )
        input_layout.add_widget(self.height_label)
        input_layout.add_widget(self.height_input)

        self.root.add_widget(input_layout)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)

        self.calculate_button = Button(
            text='Calculate BMI',
            font_size=18,
            background_color=(0.2, 0.7, 0.2, 1),  # Green button color
            color=(1, 1, 1, 1)  # White text color
        )
        self.calculate_button.bind(on_press=self.calculate_bmi)
        button_layout.add_widget(self.calculate_button)

        self.save_button = Button(
            text='Save BMI',
            font_size=18,
            background_color=(0.2, 0.7, 0.2, 1),  # Green button color
            color=(1, 1, 1, 1)  # White text color
        )
        self.save_button.bind(on_press=self.save_bmi)
        button_layout.add_widget(self.save_button)

        self.delete_button = Button(
            text='Delete All Data',
            font_size=18,
            background_color=(0.9, 0.1, 0.1, 1),  # Red button color
            color=(1, 1, 1, 1)  # White text color
        )
        self.delete_button.bind(on_press=self.delete_data)
        button_layout.add_widget(self.delete_button)

        self.root.add_widget(button_layout)

        self.history_label = Label(
            text='BMI History:',
            font_size=24
        )
        self.root.add_widget(self.history_label)

        self.history_text = TextInput(
            readonly=True,
            font_size=18,
            multiline=True,
            background_color=(0.9, 0.9, 1, 1)  # Light blue background
        )
        self.load_bmi_history()
        self.root.add_widget(self.history_text)

        self.bmi_categories = {
            'Underweight': (0, 18.4),
            'Normal Weight': (18.5, 24.9),
            'Overweight': (25, 29.9),
            'Obesity': (30, float('inf')),
        }

        self.category_spinner = Spinner(
            text='Select BMI Category',
            values=list(self.bmi_categories.keys()),
            font_size=18
        )
        self.root.add_widget(self.category_spinner)

        return self.root

    def calculate_bmi(self, instance):
        try:
            weight = float(self.weight_input.text)
            height = float(self.height_input.text) / 100  # Convert cm to meters
            bmi = weight / (height * height)

            category = None
            for cat, (lower, upper) in self.bmi_categories.items():
                if lower <= bmi <= upper:
                    category = cat
                    break

            # Recommendations for each category
            recommendations = {
                'Underweight': 'You should consider gaining some weight. Consult a nutritionist for a proper diet plan.',
                'Normal Weight': 'Congratulations! You are in a healthy weight range.',
                'Overweight': 'You should consider losing some weight through a combination of diet and exercise. Consult a healthcare professional.',
                'Obesity': 'Immediate weight loss is recommended. Consult a healthcare professional for a personalized weight loss plan.'
            }

            result_text = f'[color=FFFFFF]Your BMI:[/color] [b]{bmi:.2f}[/b]\n[color=FFFFFF]Category:[/color] [b]{category}[/b]\n[color=FFFFFF]Recommendation:[/color] [i]{recommendations[category]}[/i]'
            self.result_label.text = result_text
        except ValueError:
            self.result_label.text = 'Invalid input. Please enter valid numbers.'

    def save_bmi(self, instance):
        try:
            weight = float(self.weight_input.text)
            height = float(self.height_input.text)
            bmi = weight / ((height / 100) ** 2)  # Convert height to meters
            category = None

            for cat, (lower, upper) in self.bmi_categories.items():
                if lower <= bmi <= upper:
                    category = cat
                    break

            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            bmi_entry = f'Date: {timestamp}\nWeight: {weight} kg\nHeight: {height} cm\nBMI: {bmi:.2f}\nCategory: {category}\n\n'

            with open('bmi_history.txt', 'a') as file:
                file.write(bmi_entry)

            self.load_bmi_history()  # Reload the history
        except ValueError:
            self.result_label.text = 'Invalid input. Please enter valid numbers.'

    def delete_data(self, instance):
        try:
            os.remove('bmi_history.txt')
            self.history_text.text = ''
        except FileNotFoundError:
            pass

    def load_bmi_history(self):
        if os.path.exists('bmi_history.txt'):
            with open('bmi_history.txt', 'r') as file:
                history = file.read()
                self.history_text.text = history

if __name__ == '__main__':
    BMICalculator().run()
