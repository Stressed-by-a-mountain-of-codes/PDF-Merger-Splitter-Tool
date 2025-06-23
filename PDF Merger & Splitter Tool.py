import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os

class PDFTool:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 PDF Merger & Splitter")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        tk.Label(root, text="PDF Utility Tool", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="📎 Merge PDFs", width=25, font=("Arial", 12), command=self.merge_pdfs).pack(pady=15)
        tk.Button(root, text="✂️ Split PDF by Range", width=25, font=("Arial", 12), command=self.split_pdf).pack(pady=15)
        tk.Button(root, text="❌ Exit", width=25, font=("Arial", 12), command=root.quit).pack(pady=15)

        self.status_label = tk.Label(root, text="Use File Dialog or Ctrl+V to Paste a PDF Path", font=("Arial", 9))
        self.status_label.pack(pady=10)

        # Drag & Drop Simulation (Ctrl+V)
        self.root.bind('<Control-v>', self.handle_clipboard_paste)
        self.dropped_files = []

    def handle_clipboard_paste(self, event=None):
        try:
            clipboard_path = self.root.clipboard_get()
            if os.path.isfile(clipboard_path) and clipboard_path.lower().endswith(".pdf"):
                self.dropped_files.append(clipboard_path)
                self.status_label.config(text=f"✅ Added: {os.path.basename(clipboard_path)}", fg="green")
            else:
                self.status_label.config(text="❌ Not a valid PDF file.", fg="red")
        except Exception as e:
            self.status_label.config(text="❌ Failed to read from clipboard.", fg="red")

    def get_files(self):
        if self.dropped_files:
            files = self.dropped_files
            self.dropped_files = []
        else:
            files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        return files

    def merge_pdfs(self):
        files = self.get_files()
        if not files:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not save_path:
            return

        try:
            merger = PdfMerger()
            for file in files:
                merger.append(file)
            merger.write(save_path)
            merger.close()
            self.status_label.config(text=f"✅ Merged to: {os.path.basename(save_path)}", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

    def split_pdf(self):
        file = filedialog.askopenfilename(title="Select a PDF to split", filetypes=[("PDF files", "*.pdf")])
        if not file:
            return

        reader = PdfReader(file)
        total_pages = len(reader.pages)

        def perform_split():
            try:
                start = int(start_entry.get()) - 1
                end = int(end_entry.get())
                if start < 0 or end > total_pages or start >= end:
                    raise ValueError("Invalid range.")

                writer = PdfWriter()
                for i in range(start, end):
                    writer.add_page(reader.pages[i])

                save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                         filetypes=[("PDF files", "*.pdf")],
                                                         title="Save Split PDF As")
                if not save_path:
                    return

                with open(save_path, "wb") as f:
                    writer.write(f)

                split_window.destroy()
                self.status_label.config(text=f"✅ Split saved: {os.path.basename(save_path)}", fg="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to split PDF:\n{e}")

        # Page Range Input Window
        split_window = tk.Toplevel(self.root)
        split_window.title("Page Range to Split")
        split_window.geometry("300x150")

        tk.Label(split_window, text=f"Enter page range (1 to {total_pages})").pack(pady=5)

        frame = tk.Frame(split_window)
        frame.pack(pady=5)

        tk.Label(frame, text="From:").grid(row=0, column=0, padx=5)
        start_entry = tk.Entry(frame, width=5)
        start_entry.grid(row=0, column=1)

        tk.Label(frame, text="To:").grid(row=0, column=2, padx=5)
        end_entry = tk.Entry(frame, width=5)
        end_entry.grid(row=0, column=3)

        tk.Button(split_window, text="✂️ Split Now", command=perform_split).pack(pady=10)

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    PDFTool(root)
    root.mainloop()
