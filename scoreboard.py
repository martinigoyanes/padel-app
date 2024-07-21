import tkinter as tk

class ScorePanel(tk.Frame):
    def __init__(self, parent, player_name, color, is_serving=False, *args, **kwargs):
        super().__init__(parent, bg="black", *args, **kwargs)
        self.player_name = player_name
        self.color = color
        self.is_serving = is_serving
        self.create_widgets()
        
    def create_widgets(self):
        # Create the player name label
        self.name_label = tk.Label(self, text=self.player_name, fg=self.color, bg="black", font=("Arial", 32, "bold"))
        self.name_label.grid(row=0, column=0, sticky="w")
        
        # Create the serving dot if needed
        if self.is_serving:
            self.dot_canvas = tk.Canvas(self, width=40, height=40, bg="black", highlightthickness=0)
            self.dot_canvas.create_oval(5, 5, 35, 35, fill="yellow")
            self.dot_canvas.grid(row=0, column=1, padx=(10, 0), sticky="w")

    def update_serving_status(self, is_serving):
        if is_serving:
            if not hasattr(self, 'dot_canvas'):
                self.dot_canvas = tk.Canvas(self, width=40, height=40, bg="black", highlightthickness=0)
                self.dot_canvas.create_oval(5, 5, 35, 35, fill="yellow")
                self.dot_canvas.grid(row=0, column=1, padx=(10, 0), sticky="w")
        else:
            if hasattr(self, 'dot_canvas'):
                self.dot_canvas.destroy()

class Scoreboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Padel Scoreboard")
        self.configure(bg="black")

        # Configure the grid
        self.grid_columnconfigure(index=0, weight=1, uniform="0")
        self.grid_columnconfigure(index=1, weight=1, uniform="0")
        self.grid_columnconfigure(index=2, weight=1, uniform="0")
        self.grid_columnconfigure(index=3, weight=1, uniform="0")
        self.grid_columnconfigure(index=4, weight=1, uniform="0")
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="equal")

        self.create_score_panels()
        self.create_score_labels()

    def create_score_panels(self):
        self.player_panels = [
            ScorePanel(self, "Player 1A", "red", is_serving=True),
            ScorePanel(self, "Player 2A", "red"),
            ScorePanel(self, "Player 1B", "grey"),
            ScorePanel(self, "Player 2B", "grey")
        ]
        
        for idx, panel in enumerate(self.player_panels):
            panel.grid(row=idx, column=0, sticky="nsew")

    def create_score_labels(self):
        num_score_panels = 4
        self.team_a_scores = [self.create_score_label(0, idx + 1) for idx in range(num_score_panels)]
        self.team_b_scores = [self.create_score_label(2, idx + 1) for idx in range(num_score_panels)]

    def create_score_label(self, row, column):
        score_label = tk.Label(self, text="0", fg="green", bg="black", font=("Arial", 64))
        score_label.grid(row=row, column=column, rowspan=2, padx=10, pady=10, sticky="nsew")
        return score_label

    def update_scores(self, team_a_scores, team_b_scores):
        for label, score in zip(self.team_a_scores, team_a_scores):
            label.config(text=score)
        for label, score in zip(self.team_b_scores, team_b_scores):
            label.config(text=score)

    def update_serving_status(self, serving_player_idx):
        for idx, panel in enumerate(self.player_panels):
            panel.update_serving_status(idx == serving_player_idx)

if __name__ == "__main__":
    app = Scoreboard()
    app.mainloop()

