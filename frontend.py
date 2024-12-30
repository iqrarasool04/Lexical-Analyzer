import tkinter as tk
from tkinter import filedialog, messagebox
from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer


class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer")
        self.root.geometry("800x600")

        # File Path
        self.file_path = tk.StringVar()

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # File Selection Section
        frame = tk.Frame(self.root)
        frame.pack(fill="x", pady=10)

        tk.Label(frame, text="Select File: ").pack(side="left", padx=5)
        tk.Entry(frame, textvariable=self.file_path, width=50).pack(side="left", padx=5)
        tk.Button(frame, text="Browse", command=self.browse_file).pack(side="left", padx=5)
        tk.Button(frame, text="Analyze", command=self.analyze_file).pack(side="left", padx=5)

        # Program Content Display
        tk.Label(self.root, text="Program Content:").pack(anchor="w", padx=10, pady=5)
        
        # Create a frame for the text widget and scrollbar
        program_frame = tk.Frame(self.root)
        program_frame.pack(fill="both", padx=10, pady=5)

        self.program_text = tk.Text(program_frame, height=10, wrap="word", state=tk.DISABLED)
        self.program_text.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar for program content
        program_scrollbar = tk.Scrollbar(program_frame, command=self.program_text.yview)
        program_scrollbar.pack(side="right", fill="y")
        self.program_text.config(yscrollcommand=program_scrollbar.set)

        # Token Display
        tk.Label(self.root, text="Tokens:").pack(anchor="w", padx=10, pady=5)

        # Create a frame for the text widget and scrollbar
        token_frame = tk.Frame(self.root)
        token_frame.pack(fill="both", padx=10, pady=5)

        self.tokens_text = tk.Text(token_frame, height=15, wrap="word", state=tk.DISABLED)
        self.tokens_text.pack(side="left", fill="both", expand=True)

        # Add scrollbar for token content
        token_scrollbar = tk.Scrollbar(token_frame, command=self.tokens_text.yview)
        token_scrollbar.pack(side="right", fill="y")
        self.tokens_text.config(yscrollcommand=token_scrollbar.set)

    def browse_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("C++ Files", "*.cpp"), ("All Files", "*.*")]
        )
        if file:
            self.file_path.set(file)
            self.load_file_content(file)

    def load_file_content(self, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()
                self.program_text.config(state=tk.NORMAL)  # Allow modification for loading
                self.program_text.delete("1.0", tk.END)
                self.program_text.insert(tk.END, content)
                self.program_text.config(state=tk.DISABLED)  # Disable editing again
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def analyze_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showwarning("Warning", "Please select a file to analyze.")
            return

        try:
            buffer = Buffer()
            analyzer = LexicalAnalyzer()

            # Analyze the file and display results
            tokens_info = []
            for buf in buffer.load_buffer():
                tokens_info.extend(analyzer.tokenize(buf))

            self.tokens_text.config(state=tk.NORMAL)  # Allow modification for tokens display
            self.tokens_text.delete("1.0", tk.END)
            for token in tokens_info:
                self.tokens_text.insert(tk.END, f"Type: {token[0]}, Lexeme: {token[1]}, Line: {token[2]}, Column: {token[3]}\n")
            self.tokens_text.config(state=tk.DISABLED)  # Disable editing again
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzerApp(root)
    root.mainloop()
