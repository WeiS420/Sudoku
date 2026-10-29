import tkinter as tk
from tkinter import messagebox
import random
import copy

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Sudoku - Dev Mode")
        self.root.geometry("520x780")
        
        self.current_diff = "Easy"
        self.puzzle, self.solution = self.generate_sudoku(self.current_diff)
        self.original = copy.deepcopy(self.puzzle)
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        
        # Interactive play variables
        self.active_digit = None
        self.notes_mode = False
        self.notes = [[set() for _ in range(9)] for _ in range(9)]
        self.keypad_buttons = {}
        
        # Timer variables
        self.seconds_elapsed = 0
        self.timer_running = False
        
        self.create_widgets()
        
    def generate_sudoku(self, difficulty):
        base = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        nums = list(range(1, 10))
        random.shuffle(nums)
        board = [[nums[cell - 1] for cell in row] for row in base]
        
        for group in range(3):
            r1, r2 = group * 3, group * 3 + 2
            row_indices = list(range(r1, r2 + 1))
            random.shuffle(row_indices)
            board[r1:r2+1] = [board[i] for i in row_indices]
            
            transposed = list(zip(*board))
            transposed[r1:r2+1] = [transposed[i] for i in row_indices]
            board = [list(r) for r in zip(*transposed)]

        solution = copy.deepcopy(board)
        
        if difficulty == "Easy":
            removals = 35
        elif difficulty == "Normal":
            removals = 45
        else:
            removals = 55
            
        removed = 0
        while removed < removals:
            r = random.randint(0, 8)
            c = random.randint(0, 8)
            if board[r][c] != 0:
                board[r][c] = 0
                removed += 1
                
        return board, solution

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)
        
        tk.Label(top_frame, text="Difficulty:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        self.diff_var = tk.StringVar(value=self.current_diff)
        diff_menu = tk.OptionMenu(top_frame, self.diff_var, "Easy", "Normal", "Hard", command=self.change_difficulty)
        diff_menu.pack(side=tk.LEFT, padx=5)
        
        self.timer_label = tk.Label(top_frame, text="Time: 00:00", font=("Arial", 12, "bold"), fg="blue")
        self.timer_label.pack(side=tk.LEFT, padx=15)
        
        # Timer Buttons
        timer_btn_frame = tk.Frame(self.root)
        timer_btn_frame.pack(pady=2)
        
        tk.Button(timer_btn_frame, text="Start", bg="#d4edda", command=self.start_timer).pack(side=tk.LEFT, padx=3)
        tk.Button(timer_btn_frame, text="Pause", bg="#fff3cd", command=self.pause_timer).pack(side=tk.LEFT, padx=3)
        tk.Button(timer_btn_frame, text="Resume", bg="#cce5ff", command=self.resume_timer).pack(side=tk.LEFT, padx=3)
        
        # Sudoku Grid Frame
        self.board_frame = tk.Frame(self.root, bg="black", bd=3)
        self.board_frame.pack(pady=5)
        
        self.build_grid()
        
        # Keypad & Eraser Frame
        keypad_frame = tk.Frame(self.root)
        keypad_frame.pack(pady=5)
        
        tk.Label(keypad_frame, text="Keypad:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=3)
        for i in range(1, 10):
            btn = tk.Button(keypad_frame, text=str(i), width=2, font=("Arial", 11, "bold"),
                            command=lambda n=i: self.select_digit(n))
            btn.pack(side=tk.LEFT, padx=1)
            self.keypad_buttons[i] = btn
            
        eraser_btn = tk.Button(keypad_frame, text="Eraser", bg="#ffcccc", font=("Arial", 9, "bold"),
                               command=lambda: self.select_digit("erase"))
        eraser_btn.pack(side=tk.LEFT, padx=4)
        self.keypad_buttons["erase"] = eraser_btn

        # Notes Toggle Frame
        notes_frame = tk.Frame(self.root)
        notes_frame.pack(pady=2)
        
        self.notes_btn = tk.Button(notes_frame, text="Notes Mode: OFF", font=("Arial", 10, "bold"), bg="#e2e2e2", command=self.toggle_notes_mode)
        self.notes_btn.pack(side=tk.LEFT, padx=5)

        # Action Buttons (Including Dev Cheat Button)
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)
        
        tk.Button(action_frame, text="New Game", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white", command=self.new_game).pack(side=tk.LEFT, padx=3)
        tk.Button(action_frame, text="Check Solution", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=self.check_solution).pack(side=tk.LEFT, padx=3)
        tk.Button(action_frame, text="Dev: Auto-Solve", font=("Arial", 10, "bold"), bg="#ffc107", fg="black", command=self.dev_solve).pack(side=tk.LEFT, padx=3)

    def select_digit(self, digit):
        self.active_digit = digit
        # Reset keypad highlights
        for d, btn in self.keypad_buttons.items():
            if d == "erase":
                btn.config(bg="#ffcccc")
            else:
                btn.config(bg="#f0f0f0")
        
        # Highlight active
        if digit == "erase":
            self.keypad_buttons["erase"].config(bg="#ff6666")
        elif digit is not None:
            self.keypad_buttons[digit].config(bg="#a0c4ff")

    def toggle_notes_mode(self):
        self.notes_mode = not self.notes_mode
        if self.notes_mode:
            self.notes_btn.config(text="Notes Mode: ON", bg="#b9fbc0")
        else:
            self.notes_btn.config(text="Notes Mode: OFF", bg="#e2e2e2")

    def build_grid(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
            
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        
        for box_r in range(3):
            for box_c in range(3):
                sub_frame = tk.Frame(self.board_frame, bg="black")
                sub_frame.grid(row=box_r, column=box_c, padx=2, pady=2)
                
                for r in range(3):
                    for c in range(3):
                        row_idx = box_r * 3 + r
                        col_idx = box_c * 3 + c
                        
                        entry = tk.Entry(
                            sub_frame, 
                            width=2, 
                            font=("Arial", 16, "bold"), 
                            justify="center"
                        )
                        entry.grid(row=r, column=c, padx=1, pady=1, ipady=6)
                        
                        # Bind left click for mouse-only keypad support
                        entry.bind("<Button-1>", lambda e, r=row_idx, c=col_idx: self.handle_cell_click(r, c))
                        
                        val = self.puzzle[row_idx][col_idx]
                        if val != 0:
                            entry.insert(0, str(val))
                            entry.config(state="disabled", disabledbackground="#e0e0e0", disabledforeground="black")
                        
                        self.cells[row_idx][col_idx] = entry

    def handle_cell_click(self, r, c):
        entry = self.cells[r][c]
        if entry.cget("state") == "disabled":
            return
            
        if self.active_digit is None:
            return
            
        if self.notes_mode:
            # Do not allow notes if cell already has a solid answer
            val_str = entry.get().strip()
            if val_str.isdigit() and len(val_str) == 1 and not entry.cget("fg") == "gray":
                return
                
            if self.active_digit == "erase":
                self.notes[r][c].clear()
            else:
                digit = int(self.active_digit)
                if digit in self.notes[r][c]:
                    self.notes[r][c].remove(digit)
                else:
                    self.notes[r][c].add(digit)
            self.update_cell_notes_display(r, c)
        else:
            # Normal input mode
            entry.config(state="normal")
            if self.active_digit == "erase":
                entry.delete(0, tk.END)
                self.notes[r][c].clear()
            else:
                entry.delete(0, tk.END)
                entry.insert(0, str(self.active_digit))
                entry.config(fg="black", font=("Arial", 16, "bold"))
                self.notes[r][c].clear() # Clear notes when a definitive answer is placed

    def update_cell_notes_display(self, r, c):
        entry = self.cells[r][c]
        entry.config(state="normal")
        entry.delete(0, tk.END)
        if self.notes[r][c]:
            notes_str = " ".join(str(n) for n in sorted(self.notes[r][c]))
            entry.insert(0, notes_str)
            entry.config(fg="gray", font=("Arial", 9))
        else:
            entry.config(fg="black", font=("Arial", 16, "bold"))

    def new_game(self):
        self.puzzle, self.solution = self.generate_sudoku(self.current_diff)
        self.original = copy.deepcopy(self.puzzle)
        self.notes = [[set() for _ in range(9)] for _ in range(9)]
        self.active_digit = None
        self.select_digit(None)
        self.seconds_elapsed = 0
        self.timer_running = False
        self.timer_label.config(text="Time: 00:00")
        self.build_grid()

    def change_difficulty(self, selected_diff):
        self.current_diff = selected_diff
        self.new_game()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.run_timer()

    def pause_timer(self):
        self.timer_running = False

    def resume_timer(self):
        if not self.timer_running and self.seconds_elapsed > 0:
            self.timer_running = True
            self.run_timer()

    def run_timer(self):
        if self.timer_running:
            mins = self.seconds_elapsed // 60
            secs = self.seconds_elapsed % 60
            self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
            self.seconds_elapsed += 1
            self.root.after(1000, self.run_timer)

    def dev_solve(self):
        """Developer tool to instantly fill the board with correct answers for testing."""
        for r in range(9):
            for c in range(9):
                entry = self.cells[r][c]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, str(self.solution[r][c]))
                entry.config(fg="black", font=("Arial", 16, "bold"))
                self.notes[r][c].clear()
        print("⚡ Dev Mode: Board auto-solved.")

    def check_solution(self):
        errors = 0
        unfilled = 0
        
        for r in range(9):
            for c in range(9):
                val_str = self.cells[r][c].get().strip()
                # Treat gray note text as unfilled
                if val_str == "" or self.cells[r][c].cget("fg") == "gray":
                    unfilled += 1
                elif not (val_str.isdigit() and 1 <= int(val_str) <= 9):
                    errors += 1
                else:
                    if int(val_str) != self.solution[r][c]:
                        errors += 1
                        
        if unfilled > 0:
            messagebox.showwarning("Incomplete", f"The puzzle is not finished yet! You have {unfilled} empty or note-only cells.")
            return
            
        if errors > 0:
            messagebox.showerror("Not Quite Right", f"Your board has {errors} errors (incorrect numbers or invalid entries). Keep trying!")
            return
            
        self.timer_running = False
        messagebox.showinfo("Victory!", f"🎉 Amazing! All your answers are correct!\nTotal time: {self.timer_label.cget('text')[6:]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()
