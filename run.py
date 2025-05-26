import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfMerger
import os

class PDFMergerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Merger")
        self.master.geometry("500x550")
        self.master.configure(bg="#f5f5f5")  # cor de fundo suave

        self.pdf_files = []

        self.font_title = ("Helvetica", 14, "bold")
        self.font_normal = ("Helvetica", 10)

        # Label de instrução
        self.label = tk.Label(master, text="Arraste os arquivos PDF ou clique em 'Adicionar PDF'",
                              bg="#f5f5f5", fg="#333", font=self.font_title)
        self.label.pack(pady=15)

        # Lista de arquivos
        self.listbox = tk.Listbox(master, width=60, height=10, selectmode=tk.SINGLE, font=self.font_normal)
        self.listbox.pack(pady=10)

        # Frame de botões
        button_frame = tk.Frame(master, bg="#f5f5f5")
        button_frame.pack(pady=15)

        self.add_button = tk.Button(button_frame, text="➕ Adicionar PDF", command=self.add_pdf, width=15)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.remove_button = tk.Button(button_frame, text="❌ Remover", command=self.remove_selected, width=15)
        self.remove_button.grid(row=0, column=1, padx=5, pady=5)

        self.up_button = tk.Button(button_frame, text="⬆️ Mover Cima", command=self.move_up, width=15)
        self.up_button.grid(row=1, column=0, padx=5, pady=5)

        self.down_button = tk.Button(button_frame, text="⬇️ Mover Baixo", command=self.move_down, width=15)
        self.down_button.grid(row=1, column=1, padx=5, pady=5)

        self.merge_button = tk.Button(master, text="✅ Mesclar PDFs", command=self.merge_pdfs, width=30, bg="#4CAF50", fg="white", font=self.font_title)
        self.merge_button.pack(pady=20)

        # Status bar
        self.status_label = tk.Label(master, text="Nenhum arquivo carregado.", bg="#f5f5f5", fg="#666", font=self.font_normal)
        self.status_label.pack(pady=10)

        # Área de Drop
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

    def update_status(self, message):
        self.status_label.config(text=message)

    def add_pdf(self):
        files = filedialog.askopenfilenames(title="Selecione PDFs", filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))
        self.update_status(f"{len(self.pdf_files)} arquivo(s) carregado(s).")

    def drop(self, event):
        files = self.master.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith('.pdf') and file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))
        self.update_status(f"{len(self.pdf_files)} arquivo(s) carregado(s).")

    def remove_selected(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado para remover.")
            return
        index = selected_index[0]
        removed_file = self.pdf_files.pop(index)
        self.listbox.delete(index)
        self.update_status(f"Arquivo removido: {os.path.basename(removed_file)}. {len(self.pdf_files)} restante(s).")

    def move_up(self):
        selected_index = self.listbox.curselection()
        if not selected_index or selected_index[0] == 0:
            return
        index = selected_index[0]
        self.pdf_files[index], self.pdf_files[index - 1] = self.pdf_files[index - 1], self.pdf_files[index]
        self.update_listbox()
        self.listbox.select_set(index - 1)

    def move_down(self):
        selected_index = self.listbox.curselection()
        if not selected_index or selected_index[0] == len(self.pdf_files) - 1:
            return
        index = selected_index[0]
        self.pdf_files[index], self.pdf_files[index + 1] = self.pdf_files[index + 1], self.pdf_files[index]
        self.update_listbox()
        self.listbox.select_set(index + 1)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for file in self.pdf_files:
            self.listbox.insert(tk.END, os.path.basename(file))

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("Erro", "Nenhum arquivo PDF selecionado!")
            return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_file:
            return
        merger = PdfMerger()
        try:
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_file)
            merger.close()
            messagebox.showinfo("Sucesso", f"PDF mesclado salvo em:\n{output_file}")
            self.update_status("Mesclagem concluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mesclar PDFs: {e}")
            self.update_status("Erro ao mesclar PDFs.")

# Inicialização
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
