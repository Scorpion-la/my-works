import tkinter as tk
from tkinter import ttk
import math

class AdvancedCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Calculator")
        self.window.geometry("400x600")
        self.window.configure(bg="#f0f0f0")

        # Entry field
        self.display = ttk.Entry(self.window, font=('Arial', 20), justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Buttons layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('√', 5, 3),
            ('(', 6, 0), (')', 6, 1), ('π', 6, 2), ('^', 6, 3),
            ('C', 7, 0), ('CE', 7, 1), ('⌫', 7, 2), ('1/x', 7, 3)
        ]

        # Create and place buttons
        for (text, row, col) in buttons:
            button = ttk.Button(self.window, text=text, command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        # Configure grid weights
        for i in range(8):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 16))

    def button_click(self, value):
        current = self.display.get()
        
        if value == '=':
            try:
                # Replace special characters and calculate
                expression = current.replace('π', str(math.pi))
                expression = expression.replace('^', '**')
                expression = expression.replace('√', 'math.sqrt')
                
                # Handle trigonometric functions
                if 'sin' in expression:
                    expression = expression.replace('sin', 'math.sin(math.radians')
                    expression += ')'
                if 'cos' in expression:
                    expression = expression.replace('cos', 'math.cos(math.radians')
                    expression += ')'
                if 'tan' in expression:
                    expression = expression.replace('tan', 'math.tan(math.radians')
                    expression += ')'
                
                result = eval(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        
        elif value == 'C':
            self.display.delete(0, tk.END)
        
        elif value == 'CE':
            self.display.delete(0, tk.END)
        
        elif value == '⌫':
            self.display.delete(len(current)-1, tk.END)
        
        elif value == '1/x':
            try:
                result = 1 / float(current)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        
        else:
            self.display.insert(tk.END, value)

if __name__ == "__main__":
    calc = AdvancedCalculator()
    calc.window.mainloop()
