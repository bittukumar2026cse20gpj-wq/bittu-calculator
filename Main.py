
import ast
import operator
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

def safe_calculate(expression):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow
    }

    def solve(node):
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value

        if isinstance(node, ast.BinOp):
            if type(node.op) in operations:
                left = solve(node.left)
                right = solve(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 10:
                    raise ValueError("Power too large")

                return operations[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -solve(node.operand)

        raise ValueError("Invalid expression")

    if len(expression) > 100:
        raise ValueError("Expression too long")

    return solve(ast.parse(expression, mode="eval").body)


class CalculatorApp(App):

    def build(self):
        self.title = "Bittu Calculator"

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.display = TextInput(
            text="",
            font_size=36,
            readonly=True,
            multiline=False,
            halign="right",
            size_hint_y=0.25
        )

        layout.add_widget(self.display)

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "DEL", "+",
            "^", ".", "=", 
        ]

        grid = GridLayout(
            cols=4,
            spacing=5
        )

        for value in buttons:
            btn = Button(
                text=value,
                font_size=25,
                background_color=(
                    (0.85, 0.1, 0.1, 1)
                    if value in ["+", "-", "*", "/", "^", "="]
                    else (0.2, 0.2, 0.2, 1)
                )
            )

            btn.bind(
                on_press=lambda instance, v=value: self.press(v)
            )

            grid.add_widget(btn)

        layout.add_widget(grid)
        return layout

    def press(self, value):
        if value == "C":
            self.display.text = ""

        elif value == "DEL":
            self.display.text = self.display.text[:-1]

        elif value == "=":
            try:
                result = safe_calculate(self.display.text)
                self.display.text = str(result)
            except Exception:
                self.display.text = "Error"

        else:
            self.display.text += value


CalculatorApp().run()
