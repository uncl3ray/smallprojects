import tkinter as tk
from tkinter import messagebox

# --- CYBERPUNK DESIGN KONSTANTEN ---
BG_COLOR = '#0D1117'          # Dunkles Cyber-Schwarz/Blau
FG_COLOR = '#00FFFF'          # Leuchtendes Cyan/Aqua (Primärfarbe)
FONT_MONO = ('Consolas', 12)   # Monospace-Font für den Terminal-Look
FONT_TITLE = ('Consolas', 20, 'bold')
PRIORITY_COLOR = {
    1: '#00FFFF',            # Niedrig: Aqua/Cyan
    2: '#FFFF00',            # Mittel: Neon-Gelb
    3: '#FF33CC'             # Hoch: Leuchtendes Magenta/Pink (Gefahr)
}

# --- DATENSPEICHER ---
# Globale Liste und ID-Zähler bleiben gleich, nur das Styling ändert sich.
tasks = []
task_id_counter = 0

class CyberpunkTaskBoard(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("[ C Y B E R T A S K - S Y S T E M ]")
        self.geometry("600x700")
        self.config(bg=BG_COLOR)
        
        global task_id_counter
        self.next_id = task_id_counter
        
        self.create_widgets()
        self.update_task_display()

    def create_widgets(self):
        # --- Titel (Größer und kantiger) ---
        tk.Label(self, text="[ /// D A T A J O B S /// ]", 
                 font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=15)

        # --- Eingabebereich ---
        input_frame = tk.Frame(self, bg=BG_COLOR)
        input_frame.pack(pady=10)

        # 1. Beschreibung
        tk.Label(input_frame, text="INPUT:", font=FONT_MONO, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        # Entry-Feld im Terminal-Stil
        self.task_entry = tk.Entry(input_frame, width=30, font=FONT_MONO, 
                                   bg='#1A202C', fg=FG_COLOR, 
                                   insertbackground=FG_COLOR, relief=tk.FLAT)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        # 2. Priorität
        tk.Label(input_frame, text="P:", font=FONT_MONO, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        self.prioritaet_var = tk.IntVar(value=1)
        # OptionMenu mit Cyber-Farben stylen
        option_menu = tk.OptionMenu(input_frame, self.prioritaet_var, 1, 2, 3)
        option_menu.config(bg=BG_COLOR, fg=FG_COLOR, font=FONT_MONO, highlightbackground=FG_COLOR, relief=tk.FLAT)
        option_menu["menu"].config(bg=BG_COLOR, fg=FG_COLOR, font=FONT_MONO)
        option_menu.pack(side=tk.LEFT, padx=5)

        # 3. Hinzufügen-Button (Block-Stil)
        tk.Button(input_frame, text=" [ + J O B ] ", command=self.add_task, 
                  font=FONT_MONO, bg=FG_COLOR, fg=BG_COLOR, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)

        # --- Sortieren-Button (Akzentfarbe) ---
        tk.Button(self, text=" * S O R T I E R U N G   D U R C H F Ü H R E N * ", command=self.sort_tasks, 
                  font=FONT_MONO, bg='#5500AA', fg=FG_COLOR, relief=tk.FLAT).pack(pady=5)
        
        # --- Anzeige-Bereich (Scrollbar im Terminal-Stil) ---
        self.task_display_frame = tk.Frame(self, bg=BG_COLOR)
        self.task_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.task_display_frame, bg=BG_COLOR, highlightthickness=1, highlightbackground=FG_COLOR)
        self.scrollbar = tk.Scrollbar(self.task_display_frame, orient="vertical", command=self.canvas.yview, bg=BG_COLOR, troughcolor=BG_COLOR)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # --- FUNKTIONEN (Logik bleibt gleich) ---

    def add_task(self):
        """Fügt einen neuen Job hinzu und aktualisiert die Anzeige."""
        global task_id_counter, tasks
        description = self.task_entry.get().strip()
        priority = self.prioritaet_var.get()

        if not description:
            messagebox.showwarning("ALERT_SYSTEM", "ERROR: DATENFELD LEER.", parent=self)
            return

        task_id_counter += 1
        new_task = {
            'id': task_id_counter,
            'beschreibung': description,
            'prioritaet': priority,
        }
        tasks.append(new_task)

        self.task_entry.delete(0, tk.END)
        self.update_task_display()

    def delete_task(self, task_id):
        """Löscht einen Job anhand seiner ID."""
        global tasks
        tasks = [task for task in tasks if task['id'] != task_id]
        self.update_task_display()

    def sort_tasks(self):
        """Sortiert Jobs nach Priorität (3, 2, 1)."""
        global tasks
        tasks.sort(key=lambda task: task['prioritaet'], reverse=True)
        self.update_task_display()

    def update_task_display(self):
        """Zeigt die Jobs im Cyberpunk-Stil an."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not tasks:
            tk.Label(self.scrollable_frame, text="// ZYKLUS BEENDET //\nKEINE OFFENEN AUFGABEN", 
                     font=FONT_MONO, bg=BG_COLOR, fg='#333333').pack(pady=20)
            return
            
        for task in tasks:
            task_id = task['id']
            prio = task['prioritaet']
            prio_color = PRIORITY_COLOR[prio]
            
            task_row = tk.Frame(self.scrollable_frame, bg=BG_COLOR, pady=5)
            # Eine dünne Linie als visueller Akzent
            tk.Frame(task_row, height=1, bg=prio_color).pack(fill=tk.X)
            task_row.pack(fill=tk.X)

            # 1. Prioritäts-Anzeige (Farbliche Hervorhebung)
            tk.Label(task_row, text=f"P:{prio}", 
                     font=FONT_MONO, bg=BG_COLOR, fg=prio_color, width=3).pack(side=tk.LEFT)

            # 2. Beschreibung
            tk.Label(task_row, text=task['beschreibung'], 
                     font=FONT_MONO, bg=BG_COLOR, fg=prio_color, anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)

            # 3. Löschen-Button (Kontrastierend Rot)
            tk.Button(task_row, text=" [E R A S E] ", 
                      command=lambda id=task_id: self.delete_task(id), 
                      font=FONT_MONO, bg='#FF33CC', fg=BG_COLOR, relief=tk.FLAT).pack(side=tk.RIGHT, padx=5)


if __name__ == "__main__":
    app = CyberpunkTaskBoard()
    app.mainloop()