import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

class SinhalaConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sinhala Unicode Converter")
        self.root.geometry("600x500")
        
        # Load mapping data
        try:
            if getattr(sys, 'frozen', False):  # Running as executable
                base_path = sys._MEIPASS
            else:  # Running as script
                base_path = os.path.dirname(__file__)
            
            with open(os.path.join(base_path, 'data_list.json'), 'r', encoding='utf-8') as f:
                self.mapping_data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.root.destroy()
            return
        
        # Create conversion dictionaries
        self.unicode_to_fm = {item['uni']: item['fm'] for item in self.mapping_data if item['uni'] and item['fm']}
        self.unicode_to_isi = {item['uni']: item['isi'] for item in self.mapping_data if item['uni'] and item['isi']}
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input
        ttk.Label(main_frame, text="Input Unicode Text:").pack()
        self.input_text = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD)
        self.input_text.pack(fill=tk.X, pady=5)
        
        # Options
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        self.style_var = tk.StringVar(value="fm")
        ttk.Radiobutton(options_frame, text="FM", variable=self.style_var, value="fm").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(options_frame, text="ISI", variable=self.style_var, value="isi").pack(side=tk.LEFT, padx=5)
        
        # Convert button
        ttk.Button(main_frame, text="Convert", command=self.convert).pack(pady=5)
        
        # Output
        ttk.Label(main_frame, text="Converted Text:").pack()
        self.output_text = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD, state='disabled')
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Copy button
        ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)
    
    def convert(self):
        text = self.input_text.get("1.0", tk.END).strip()
        style = self.style_var.get()
        
        if not text:
            return
            
        converted = []
        i = 0
        n = len(text)
        
        mapping = self.unicode_to_fm if style == "fm" else self.unicode_to_isi
        
        while i < n:
            matched = False
            for l in range(4, 0, -1):
                if i + l <= n:
                    substr = text[i:i+l]
                    if substr in mapping:
                        converted.append(mapping[substr])
                        i += l
                        matched = True
                        break
            if not matched:
                converted.append(text[i])
                i += 1
        
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, ''.join(converted))
        self.output_text.config(state='disabled')
    
    def copy_to_clipboard(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Success", "Text copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SinhalaConverterApp(root)
    root.mainloop()