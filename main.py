import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import cv2

# Set the tesseract path accordingly
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize modern dark UI
ctk.set_appearance_mode("Dark")  # Force Dark Mode
ctk.set_default_color_theme("dark-blue")  # Use dark theme

class TextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖤  Image to Text Extractor")

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.upload_btn = ctk.CTkButton(self.main_frame, text="📷 Upload Image", command=self.upload_image,
                                        fg_color="#4444aa", hover_color="#333388", font=("Arial", 18), corner_radius=10)
        self.upload_btn.pack(pady=50)

        self.image_label = None
        self.back_btn = None
        self.extract_btn = None
        self.textbox = None

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return

        self.clear_frame()

        image = Image.open(path)
        image.thumbnail((500, 400))
        self.tk_image = ImageTk.PhotoImage(image)

        self.image_label = ctk.CTkLabel(self.main_frame, image=self.tk_image, text="")
        self.image_label.pack(pady=20)

        self.back_btn = ctk.CTkButton(self.main_frame, text="⬅ Back", command=self.go_back,
                                      fg_color="#bb4444", hover_color="#992222", font=("Arial", 16), corner_radius=10)
        self.back_btn.pack(pady=10)

        self.extract_btn = ctk.CTkButton(self.main_frame, text="📝 Extract Text", command=lambda: self.extract_text(path),
                                         fg_color="#228855", hover_color="#116644", font=("Arial", 18), corner_radius=10)
        self.extract_btn.pack(pady=10)

    def extract_text(self, path):
        try:
            actual_image = cv2.imread(path)
            sample_img = cv2.resize(actual_image, (500, 400))
            sample_img = cv2.cvtColor(sample_img, cv2.COLOR_BGR2RGB)
            extracted_text = pytesseract.image_to_string(sample_img)

            if not extracted_text.strip():
                messagebox.showinfo("No Text", "No text found in the image.")
                return

            self.clear_frame()

            self.back_btn = ctk.CTkButton(self.main_frame, text="⬅ Back", command=self.go_back,
                                          fg_color="#bb4444", hover_color="#992222", font=("Arial", 16), corner_radius=10)
            self.back_btn.pack(pady=10)

            self.textbox = ctk.CTkTextbox(self.main_frame, width=600, height=400, font=("Consolas", 14),
                                          fg_color="#222222", text_color="#00FFAA")
            self.textbox.insert("1.0", extracted_text)
            self.textbox.configure(state="normal")  # Allow copy
            self.textbox.pack(pady=20)

        except pytesseract.pytesseract.TesseractNotFoundError:
            messagebox.showerror("Error", "Tesseract not found. Please check the installation path.")

    def go_back(self):
        self.clear_frame()  # destroys all widgets including upload_btn
        # recreate upload button freshly
        self.upload_btn = ctk.CTkButton(self.main_frame, text="📷 Upload Image", command=self.upload_image,
                                        fg_color="#4444aa", hover_color="#333388", font=("Arial", 18), corner_radius=10)
        self.upload_btn.pack(pady=50)


    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Run the dark theme app
if __name__ == "__main__":
    root = ctk.CTk()
    app = TextExtractorApp(root)
    root.geometry("800x600")
    root.mainloop()
