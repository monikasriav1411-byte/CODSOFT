import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.bg_gradient_top = "#667eea"
        self.bg_gradient_bottom = "#764ba2"
        self.display_bg = "#2d3436"
        self.display_text = "#00ff88"
        self.button_bg = "#ffffff"
        self.button_text = "#2d3436"
        self.operator_bg = "#ff6b6b"
        self.operator_text = "#ffffff"
        self.equals_bg = "#00b894"
        self.clear_bg = "#fdcb6e"
        self.current = ""
        self.operator = ""
        self.first_num = ""
        self.result_shown = False
        
        self.setup_ui()
        
    def setup_ui(self):
        
        self.canvas = tk.Canvas(self.root, width=400, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.create_gradient()
        display_frame = tk.Frame(self.root, bg=self.display_bg, relief="flat", bd=0)
        display_frame.place(x=20, y=20, width=360, height=120)
        display_font = font.Font(family="Digital-7", size=36, weight="bold")
        self.display = tk.Label(display_frame, text="0", font=display_font,
                               bg=self.display_bg, fg=self.display_text,
                               anchor="e", padx=20)
        self.display.pack(fill="both", expand=True)
        self.operation_display = tk.Label(display_frame, text="", 
                                         font=("Arial", 12),
                                         bg=self.display_bg, fg="#74b9ff",
                                         anchor="e", padx=20)
        self.operation_display.place(x=0, y=10, width=360, height=30)
        
        
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        y_offset = 160
        for row in buttons:
            x_offset = 20
            for btn_text in row:
                self.create_button(btn_text, x_offset, y_offset)
                x_offset += 90
            y_offset += 80
        
    def create_gradient(self):
        """Create a gradient background"""
        width = 400
        height = 600
        r1, g1, b1 = self.hex_to_rgb(self.bg_gradient_top)
        r2, g2, b2 = self.hex_to_rgb(self.bg_gradient_bottom)
        
        for i in range(height):
            r = int(r1 + (r2 - r1) * i / height)
            g = int(g1 + (g2 - g1) * i / height)
            b = int(b1 + (b2 - b1) * i / height)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_button(self, text, x, y):
        
        if text in ['/', 'x', '-', '+']:
            bg_color = self.operator_bg
            fg_color = self.operator_text
            btn_font = ("Arial", 20, "bold")
        elif text == '=':
            bg_color = self.equals_bg
            fg_color = self.operator_text
            btn_font = ("Arial", 20, "bold")
        elif text in ['C', '⌫']:
            bg_color = self.clear_bg
            fg_color = self.button_text
            btn_font = ("Arial", 16, "bold")
        else:
            bg_color = self.button_bg
            fg_color = self.button_text
            btn_font = ("Arial", 18, "bold")
        
        shadow_frame = tk.Frame(self.root, bg="#555555")
        shadow_frame.place(x=x+2, y=y+2, width=80, height=70)
        
        button = tk.Button(self.root, text=text, font=btn_font,
                          bg=bg_color, fg=fg_color, relief="flat",
                          cursor="hand2", bd=0,
                          command=lambda t=text: self.on_button_click(t))
        button.place(x=x, y=y, width=80, height=70)
        
        
        button.bind("<Enter>", lambda e, b=button, c=bg_color: self.on_hover(b, c))
        button.bind("<Leave>", lambda e, b=button, c=bg_color: self.on_leave(b, c))
    
    def on_hover(self, button, original_color):
        """Button hover effect"""
        rgb = self.hex_to_rgb(original_color)
       
        new_rgb = tuple(min(255, c + 30) for c in rgb)
        new_color = f'#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}'
        button.config(bg=new_color)
    
    def on_leave(self, button, original_color):
        """Button leave effect"""
        button.config(bg=original_color)
    
    def on_button_click(self, char):
        if char == 'C':
            self.clear()
        elif char == '⌫':
            self.backspace()
        elif char == '=':
            self.calculate()
        elif char in ['+', '-', 'x', '/', '%']:
            self.set_operator(char)
        elif char == '±':
            self.toggle_sign()
        elif char == '.':
            self.add_decimal()
        else:
            self.add_digit(char)
    
    def clear(self):
        """Clear all"""
        self.current = ""
        self.operator = ""
        self.first_num = ""
        self.result_shown = False
        self.display.config(text="0")
        self.operation_display.config(text="")
    
    def backspace(self):
        """Remove last character"""
        if self.current:
            self.current = self.current[:-1]
            self.display.config(text=self.current if self.current else "0")
    
    def add_digit(self, digit):
        """Add a digit to current number"""
        if self.result_shown:
            self.current = ""
            self.result_shown = False
        
        self.current += digit
        self.display.config(text=self.current)
    
    def add_decimal(self):
        """Add decimal point"""
        if self.result_shown:
            self.current = "0"
            self.result_shown = False
        
        if '.' not in self.current:
            self.current += '.' if self.current else '0.'
            self.display.config(text=self.current)
    
    def toggle_sign(self):
        """Toggle positive/negative"""
        if self.current and self.current != "0":
            if self.current[0] == '-':
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.display.config(text=self.current)
    
    def set_operator(self, op):
        """Set the operator"""
        if self.current:
            if self.first_num and self.operator:
                self.calculate()
            self.first_num = self.current
            self.current = ""
            self.operator = op
            self.operation_display.config(text=f"{self.first_num} {op}")
    
    def calculate(self):
        """Perform calculation"""
        if self.first_num and self.current and self.operator:
            try:
                num1 = float(self.first_num)
                num2 = float(self.current)
                
                if self.operator == '+':
                    result = num1 + num2
                elif self.operator == '-':
                    result = num1 - num2
                elif self.operator == 'x':
                    result = num1 * num2
                elif self.operator == '/':
                    if num2 == 0:
                        self.display.config(text="Error")
                        self.operation_display.config(text="Cannot divide by zero")
                        self.current = ""
                        self.first_num = ""
                        self.operator = ""
                        return
                    result = num1 / num2
                elif self.operator == '%':
                    result = num1 % num2
                
                
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 8)
                
                self.operation_display.config(text=f"{self.first_num} {self.operator} {self.current} =")
                self.current = str(result)
                self.display.config(text=self.current)
                self.first_num = ""
                self.operator = ""
                self.result_shown = True
                
            except Exception as e:
                self.display.config(text="Error")
                self.operation_display.config(text="")
                self.current = ""
                self.first_num = ""
                self.operator = ""

def main():
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
