import tkinter as tk
from tkinter import messagebox

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
    POINTS = ["0", "15", "30", "40", "Game"]
    
    def __init__(self):
        super().__init__()
        self.title("Padel Scoreboard")
        self.configure(bg="black")
        self.team_a_points = 0
        self.team_b_points = 0
        self.team_a_games = 0
        self.team_b_games = 0
        self.team_a_sets = 0
        self.team_b_sets = 0
        self.current_set = 1
        self.serving_team = 1  # 1 for team A, 2 for team B

        # Configure the grid
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="equal")
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="equal")

        self.create_score_panels()
        self.create_score_labels()
        self.create_control_buttons()
        self.update_scores()

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
        self.team_a_point_label = self.create_score_label(0, 1)
        self.team_b_point_label = self.create_score_label(2, 1)
        self.team_a_game_label = self.create_score_label(0, 2)
        self.team_b_game_label = self.create_score_label(2, 2)
        self.team_a_set_label = self.create_score_label(0, 3)
        self.team_b_set_label = self.create_score_label(2, 3)

    def create_score_label(self, row, column):
        score_label = tk.Label(self, text="0", fg="green", bg="black", font=("Arial", 64))
        score_label.grid(row=row, column=column, rowspan=2, padx=10, pady=10, sticky="nsew")
        return score_label

    def create_control_buttons(self):
        self.add_point_a_button = tk.Button(self, text="Add Point to Team A", command=lambda: self.add_point(1))
        self.add_point_a_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.add_point_b_button = tk.Button(self, text="Add Point to Team B", command=lambda: self.add_point(2))
        self.add_point_b_button.grid(row=4, column=2, columnspan=2, sticky="nsew")

        self.reset_game_button = tk.Button(self, text="Reset Game", command=self.reset_game)
        self.reset_game_button.grid(row=4, column=4, sticky="nsew")

        self.end_set_button = tk.Button(self, text="End Set", command=self.end_set)
        self.end_set_button.grid(row=4, column=5, sticky="nsew")

        self.end_match_button = tk.Button(self, text="End Match", command=self.end_match)
        self.end_match_button.grid(row=4, column=6, sticky="nsew")

    def add_point(self, team):
        if team == 1:
            self.team_a_points += 1
        else:
            self.team_b_points += 1
        self.check_game_winner()

    def check_game_winner(self):
        if self.team_a_points >= 4 and self.team_a_points - self.team_b_points >= 2:
            self.team_a_games += 1
            self.reset_points()
        elif self.team_b_points >= 4 and self.team_b_points - self.team_a_points >= 2:
            self.team_b_games += 1
            self.reset_points()
        self.update_scores()
        self.check_set_winner()

    def reset_points(self):
        self.team_a_points = 0
        self.team_b_points = 0

    def check_set_winner(self):
        if self.team_a_games >= 6 and self.team_a_games - self.team_b_games >= 2:
            self.team_a_sets += 1
            self.end_set()
        elif self.team_b_games >= 6 and self.team_b_games - self.team_a_games >= 2:
            self.team_b_sets += 1
            self.end_set()
        self.update_scores()
        self.check_match_winner()

    def reset_game(self):
        self.reset_points()
        self.team_a_games = 0
        self.team_b_games = 0
        self.update_scores()

    def end_set(self):
        self.current_set += 1
        self.reset_game()

    def end_match(self):
        winner = "Team A" if self.team_a_sets > self.team_b_sets else "Team B"
        messagebox.showinfo("Match Over", f"{winner} wins the match!")
        self.team_a_sets = 0
        self.team_b_sets = 0
        self.current_set = 1
        self.reset_game()

    def update_scores(self):
        self.team_a_point_label.config(text=self.POINTS[self.team_a_points])
        self.team_b_point_label.config(text=self.POINTS[self.team_b_points])
        self.team_a_game_label.config(text=self.team_a_games)
        self.team_b_game_label.config(text=self.team_b_games)
        self.team_a_set_label.config(text=self.team_a_sets)
        self.team_b_set_label.config(text=self.team_b_sets)

if __name__ == "__main__":
    app = Scoreboard()
    app.mainloop()
