import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import random
import colorsys

class WheelOfChoices:
    def __init__(self, root):
        self.root = root
        self.root.title("Wheel of Choices")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        self.choices = []
        self.colors = []
        self.current_angle = 0
        self.spinning = False
        self.spin_speed = 0
        self.friction = 0.98
        self.min_speed = 0.5
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="🎯 Wheel of Choices 🎯", 
                              font=("Arial", 24, "bold"), 
                              bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#2c3e50')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Enter your choices:", 
                font=("Arial", 14), bg='#2c3e50', fg='#ecf0f1').pack()
        
        self.choice_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.choice_entry.pack(pady=5)
        self.choice_entry.bind('<Return>', lambda e: self.add_choice())
        
        button_frame = tk.Frame(input_frame, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        add_btn = tk.Button(button_frame, text="Add Choice", 
                           command=self.add_choice,
                           font=("Arial", 11), bg='#3498db', fg='white',
                           relief='raised', bd=2)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear All", 
                             command=self.clear_choices,
                             font=("Arial", 11), bg='#e74c3c', fg='white',
                             relief='raised', bd=2)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Canvas for the wheel
        self.canvas = tk.Canvas(self.root, width=400, height=400, 
                               bg='#34495e', highlightthickness=2,
                               highlightbackground='#ecf0f1')
        self.canvas.pack(pady=20)
        
        # Spin button
        self.spin_btn = tk.Button(self.root, text="🎲 SPIN THE WHEEL! 🎲", 
                                 command=self.spin_wheel,
                                 font=("Arial", 16, "bold"), 
                                 bg='#27ae60', fg='white',
                                 relief='raised', bd=3,
                                 state=tk.DISABLED)
        self.spin_btn.pack(pady=20)
        
        # Choices display
        self.choices_label = tk.Label(self.root, text="Choices: None added yet", 
                                     font=("Arial", 11), 
                                     bg='#2c3e50', fg='#bdc3c7',
                                     wraplength=600)
        self.choices_label.pack(pady=10)
        
        self.draw_wheel()
        
    def generate_colors(self, n):
        """Generate n distinct colors using HSV color space"""
        colors = []
        for i in range(n):
            hue = i / n
            saturation = 0.7 + (i % 3) * 0.1  # Vary saturation slightly
            value = 0.8 + (i % 2) * 0.2       # Vary brightness slightly
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            colors.append(hex_color)
        return colors
        
    def add_choice(self):
        choice = self.choice_entry.get().strip()
        if choice and choice not in self.choices:
            self.choices.append(choice)
            self.choice_entry.delete(0, tk.END)
            self.update_display()
        elif choice in self.choices:
            messagebox.showwarning("Duplicate", "This choice already exists!")
        
    def clear_choices(self):
        if self.choices and messagebox.askyesno("Clear All", "Are you sure you want to clear all choices?"):
            self.choices = []
            self.colors = []
            self.update_display()
            
    def update_display(self):
        if self.choices:
            self.colors = self.generate_colors(len(self.choices))
            self.spin_btn.config(state=tk.NORMAL)
            choices_text = "Choices: " + ", ".join(self.choices)
        else:
            self.spin_btn.config(state=tk.DISABLED)
            choices_text = "Choices: None added yet"
            
        self.choices_label.config(text=choices_text)
        self.draw_wheel()
        
    def draw_wheel(self):
        self.canvas.delete("all")
        
        if not self.choices:
            # Draw empty wheel
            self.canvas.create_oval(50, 50, 350, 350, fill='#7f8c8d', outline='#2c3e50', width=3)
            self.canvas.create_text(200, 200, text="Add choices to\ncreate the wheel!", 
                                   font=("Arial", 14), fill='white')
        else:
            # Draw wheel segments
            angle_per_segment = 360 / len(self.choices)
            
            for i, (choice, color) in enumerate(zip(self.choices, self.colors)):
                start_angle = (i * angle_per_segment + self.current_angle) % 360
                
                # Create the pie slice
                self.canvas.create_arc(50, 50, 350, 350, 
                                      start=start_angle, extent=angle_per_segment,
                                      fill=color, outline='#2c3e50', width=2)
                
                # Add text
                text_angle = math.radians(start_angle + angle_per_segment/2)
                text_x = 200 + 100 * math.cos(-text_angle)
                text_y = 200 + 100 * math.sin(-text_angle)
                
                # Choose text color based on background brightness
                rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                brightness = sum(rgb) / 3
                text_color = 'white' if brightness < 128 else 'black'
                
                self.canvas.create_text(text_x, text_y, text=choice, 
                                       font=("Arial", 10, "bold"), 
                                       fill=text_color, width=80)
        
        # Draw pointer (triangle at the top)
        self.canvas.create_polygon(200, 40, 185, 60, 215, 60, 
                                  fill='#e74c3c', outline='#c0392b', width=2)
        
        # Draw center circle
        self.canvas.create_oval(185, 185, 215, 215, 
                               fill='#2c3e50', outline='#ecf0f1', width=3)
        
    def spin_wheel(self):
        if self.spinning or not self.choices:
            return
            
        self.spinning = True
        self.spin_btn.config(state=tk.DISABLED, text="🌪️ SPINNING... 🌪️")
        
        # Set initial spin speed (random between 15-25)
        self.spin_speed = random.uniform(15, 25)
        
        self.animate_spin()
        
    def animate_spin(self):
        if self.spinning:
            # Update angle
            self.current_angle = (self.current_angle + self.spin_speed) % 360
            
            # Apply friction
            self.spin_speed *= self.friction
            
            # Check if we should stop spinning
            if self.spin_speed < self.min_speed:
                self.spinning = False
                self.spin_speed = 0
                self.show_result()
                self.spin_btn.config(state=tk.NORMAL, text="🎲 SPIN THE WHEEL! 🎲")
            
            # Redraw wheel
            self.draw_wheel()
            
            # Schedule next frame
            self.root.after(16, self.animate_spin)  # ~60 FPS
            
    def show_result(self):
        if not self.choices:
            return
            
        # Calculate which segment the pointer is pointing to
        # Pointer is at the top (270 degrees in our coordinate system)
        pointer_angle = (270 - self.current_angle) % 360
        segment_angle = 360 / len(self.choices)
        winning_index = int(pointer_angle // segment_angle)
        
        winner = self.choices[winning_index]
        winner_color = self.colors[winning_index]
        
        # Show result with animated popup
        result_window = tk.Toplevel(self.root)
        result_window.title("🎉 Winner! 🎉")
        result_window.geometry("400x200")
        result_window.configure(bg=winner_color)
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Center the window
        result_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, 
                                          self.root.winfo_rooty() + 250))
        
        # Determine text color
        rgb = tuple(int(winner_color[i:i+2], 16) for i in (1, 3, 5))
        brightness = sum(rgb) / 3
        text_color = 'white' if brightness < 128 else 'black'
        
        tk.Label(result_window, text="🎊 WINNER! 🎊", 
                font=("Arial", 20, "bold"), 
                bg=winner_color, fg=text_color).pack(pady=20)
        
        tk.Label(result_window, text=winner, 
                font=("Arial", 16, "bold"), 
                bg=winner_color, fg=text_color,
                wraplength=350).pack(pady=10)
        
        tk.Button(result_window, text="Awesome!", 
                 command=result_window.destroy,
                 font=("Arial", 12), bg='white', 
                 relief='raised', bd=2).pack(pady=20)

def main():
    root = tk.Tk()
    app = WheelOfChoices(root)
    root.mainloop()

if __name__ == "__main__":
    main()
