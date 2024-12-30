import tkinter as tk
from tkinter import scrolledtext
from LexicalAnalyzer import LexicalAnalyzer


class LexicalAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lexical Analyzer Frontend")
        
        # Set the window size
        self.master.geometry("600x400")

        # Label for code input
        self.label = tk.Label(master, text="Enter C++ code:")
        self.label.pack(pady=5)

        # Textbox for code input
        self.code_input = tk.Text(master, height=10, width=70)
        self.code_input.pack(pady=10)

        # Button to tokenize the input code
        self.tokenize_button = tk.Button(master, text="Tokenize Code", command=self.tokenize_code)
        self.tokenize_button.pack(pady=5)

        # Scrolled text area to display tokenized output
        self.token_output = scrolledtext.ScrolledText(master, height=10, width=70)
        self.token_output.pack(pady=10)

    def tokenize_code(self):
        """Function to tokenize the code entered in the input field."""
        code = self.code_input.get("1.0", tk.END).strip()
        analyzer = LexicalAnalyzer()  # Assuming LexicalAnalyzer is your tokenizing class
        tokens = analyzer.tokenize(code)
        
        # Clear previous token output
        self.token_output.delete(1.0, tk.END)
        
        # Display the tokens
        for token_type, value in tokens:
            self.token_output.insert(tk.END, f"Type: {token_type}, Value: {value}\n")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = LexicalAnalyzerGUI(root)
    root.mainloop()
