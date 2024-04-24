import tkinter as tk
from tkinter import ttk, filedialog

class ImageSelectFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.image_path = None
        self.image_name_label = ttk.Label(self, text="No image selected")
        self.image_name_label.pack(pady=10)

        self.select_button = ttk.Button(self, text="Select Image", command=self.select_image)
        self.select_button.pack()

        self.submit_button = ttk.Button(self, text="Submit", state="disabled", command=self.submit)
        self.submit_button.pack(pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(defaultextension=".pptx", filetypes=[("PowerPoint Presentations", "*.pptx")])
        file_name = self.image_path.split("/")[-1]
        if self.image_path:
            self.image_name_label.config(text=f'Selected file: {file_name}')
            self.submit_button.config(state="normal")
    
    def submit(self):
        print('clicked')


class PromptFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.prompt_entry = ttk.Entry(self)
        self.prompt_entry.pack(pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        prompt_text = self.prompt_entry.get()
        if prompt_text:
            # Simulate text processing for 1 second
            self.after(1000, lambda: print(f"Prompt processing complete: {prompt_text}"))
            # self.prompt_entry.delete(0, tk.END)  # Clear entry after processing


class ModernUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Tkinter UI")
        self.geometry('300x300')
        self.resizable(False,False)
        menubar = tk.Menu(self)
        menubar.add_command(label="Select Image", command=self.show_image_select_frame)
        menubar.add_command(label="Prompt", command=self.show_prompt_frame)
        self.config(menu=menubar)

        self.current_frame = None
        self.image_select_frame = ImageSelectFrame(self)
        self.prompt_frame = PromptFrame(self)

        # Show image selection frame by default
        self.show_image_select_frame()

    def show_image_select_frame(self):
        if self.current_frame is not self.image_select_frame:
            if self.current_frame:
                self.current_frame.pack_forget()
            self.current_frame = self.image_select_frame
            self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_prompt_frame(self):
        if self.current_frame is not self.prompt_frame:
            if self.current_frame:
                self.current_frame.pack_forget()
            self.current_frame = self.prompt_frame
            self.current_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    ui = ModernUI()
    ui.mainloop()
