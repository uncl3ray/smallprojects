import tkinter as tk
from tkinter import messagebox
from random import randint # Für zufällige IDs

# --- PIP-BOY DESIGN KONSTANTEN ---
BG_COLOR = 'black'          # Hintergrund
FG_COLOR = '#00CD00'        # Leuchtendes Grün (Pip-Boy)
FONT_MONO = ('Consolas', 12)  # Monospace-Font
FONT_TITLE = ('Consolas', 18, 'bold') #Titel-Font
PRIORITY_COLOR = {
    1: '#00CD00',            # Niedrig: Grün
    2: '#FFFF00',           # Mittel: Gelb
    3: '#FF6666'            # Hoch: Hellrot/Orange für Hervorhebung
}

# --- DATENSPEICHER ---
# Eine Liste von Dictionaries, die als unsere In-Memory-Datenbank dient.
tasks = []
task_id_counter = 0

class PipBoyTaskBoard(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Task-Boy: Wasteland Tracker")
        self.geometry("600x700")
        self.config(bg=BG_COLOR)
        
        # Sicherstellen, dass die ID-Zähler initialisiert sind
        global task_id_counter
        self.next_id = task_id_counter
        
        # --- GUI-Elemente initialisieren ---
        self.create_widgets()
        
        # Initial die leere Liste anzeigen
        self.update_task_display()

    def create_widgets(self):
        # --- Titel ---
        tk.Label(self, text="[ A U F G A B E N L I S T E ]", 
                 font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

        # --- Eingabebereich (Neuer Eintrag) ---
        input_frame = tk.Frame(self, bg=BG_COLOR)
        input_frame.pack(pady=10)

        # 1. Beschreibung
        tk.Label(input_frame, text="Neue Aufgabe:", font=FONT_MONO, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        self.task_entry = tk.Entry(input_frame, width=30, font=FONT_MONO, bg='#222222', fg=FG_COLOR, insertbackground=FG_COLOR)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        # 2. Priorität
        tk.Label(input_frame, text="Prio:", font=FONT_MONO, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        self.prioritaet_var = tk.IntVar(value=1)
        tk.OptionMenu(input_frame, self.prioritaet_var, 1, 2, 3).pack(side=tk.LEFT, padx=5)

        # 3. Erstellen-Button
        tk.Button(input_frame, text=" HINZUFÜGEN ", command=self.add_task, font=FONT_MONO, bg=FG_COLOR, fg=BG_COLOR).pack(side=tk.LEFT, padx=10)

        # --- Sortieren-Button ---
        tk.Button(self, text=" NACH WICHTIGKEIT SORTIEREN ", command=self.sort_tasks, font=FONT_MONO, bg='#006600', fg=FG_COLOR).pack(pady=5)
        
        # --- Anzeige-Bereich (Scrollbar) ---
        self.task_display_frame = tk.Frame(self, bg=BG_COLOR)
        self.task_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.task_display_frame, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.task_display_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frad, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # --- FUNKTIONEN ---

    def add_task(self):
        """Erstellt einen neuen Eintrag und fügt ihn zur Liste hinzu."""
        global task_id_counter
        description = self.task_entry.get().strip()
        priority = self.prioritaet_var.get()

        if not description:
            messagebox.showwarning("Fehler", "Bitte geben Sie eine Aufgabe ein.", parent=self)
            return

        # 1. Daten zur Python-Liste hinzufügen
        task_id_counter += 1
        new_task = {
            'id': task_id_counter,
            'beschreibung': description,
            'prioritaet': priority,
        }
        tasks.append(new_task)

        # 2. GUI aktualisieren
        self.task_entry.delete(0, tk.END) # Eingabefeld leeren
        self.update_task_display()

    def delete_task(self, task_id):
        """Löscht einen Eintrag anhand seiner ID aus der Liste."""
        global tasks
        # Erstellt eine neue Liste, die alle Aufgaben außer der zu löschenden enthält.
        tasks = [task for task in tasks if task['id'] != task_id]
        self.update_task_display()

    def sort_tasks(self):
        """Sortiert die Einträge nach Wichtigkeit (Priorität 3, 2, 1)."""
        global tasks
        # Sortiert die Liste: 'prioritaet' ist der Schlüssel, und wir sortieren absteigend (reverse=True)
        tasks.sort(key=lambda task: task['prioritaet'], reverse=True)
        self.update_task_display()

    def update_task_display(self):
        """Aktualisiert die Liste der Aufgaben im Scroll-Bereich."""
        # Löscht alle alten Widgets im Scroll-Frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not tasks:
            tk.Label(self.scrollable_frame, text="Keine Aufgaben. Zeit zum Entspannen?", 
                     font=FONT_MONO, bg=BG_COLOR, fg='#666666').pack(pady=10)
            return
            
        # Durchläuft die Aufgaben und erstellt für jede ein eigenes Frame
        for task in tasks:
            task_id = task['id']
            prio = task['prioritaet']
            prio_color = PRIORITY_COLOR[prio]
            
            # Frame für die Aufgabe (eine Zeile)
            task_row = tk.Frame(self.scrollable_frame, bg=BG_COLOR, pady=5)
            task_row.pack(fill=tk.X)

            # 1. Prioritäts-Anzeige (Farblich hervorheben!)
            tk.Label(task_row, text=f"[{prio}]", 
                     font=FONT_MONO, bg=BG_COLOR, fg=prio_color, width=4).pack(side=tk.LEFT)

            # 2. Beschreibung
            tk.Label(task_row, text=task['beschreibung'], 
                     font=FONT_MONO, bg=BG_COLOR, fg=prio_color, anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)

            # 3. Löschen-Button
            tk.Button(task_row, text=" [X] ", 
                      command=lambda id=task_id: self.delete_task(id), 
                      font=FONT_MONO, bg='#AA0000', fg=BG_COLOR).pack(side=tk.RIGHT, padx=5)


if __name__ == "__main__":
    app = PipBoyTaskBoard()
    app.mainloop()