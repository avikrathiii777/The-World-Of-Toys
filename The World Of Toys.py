import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import time
import random

PARAGRAPH1 = (
    "As the first chime of midnight rang through the air on the first day of the year, "
    "all the toys around the world came alive. They had an eerie, greenish glow in their eyes. "
    "They rose and slowly walked toward the North Pole, the origin of all toys. After about five hours, "
    "the toys were within the range of Ahumar, a dark sorcerer banished long ago for wicked deeds, to be able to be control them completely. "
    "If he succeeded, the toys would be under his control forever and the toy kingdom would be in grave danger. "
    "Danger of exposure, of being forgotten and of humans."
)

PARAGRAPH2 = (
    "A few days ago ---- "
    "'Chess grandmaster Magnus Carlsen offers a draw to the ten‑year‑old chess prodigy, Rahuma. "
    "Rahuma declines and playes the computer's top move.' informed the commentator"
    "'If Rahuma wins the tournament, he will receive the celebrated trophy, THE WHITE KING, awarded to champions since early times."
    "The first recorded winner was Sualc Atnas ,regarded by many as the best player of all time. But returning to the present Rahuma has the advantage of four points. Oh no! "
    "Magnus Carlsen has just blundered his queen by a knight fork! Oh...but what is this? Rahuma ignores the fork but plays the three-move forced mate unseen by all!'"
    " the commentator exclaimed. "
)

QUESTIONS1 = [
    {"q": "When did the toys come alive?", "choices": ["At the first chime of midnight on New Year's Day", "At noon", "At dusk", "On a rainy morning"], "answer": 0},
    {"q": "Where did the toys move toward?", "choices": ["The nearest city", "The North Pole", "The main factory", "A seaside town"], "answer": 1},
    {"q": "About how long until the toys were within Ahumar's range?", "choices": ["About one hour", "About three hours", "About five hours", "About a day"], "answer": 2},
    {"q": "Who is Ahumar?", "choices": ["A banished sorcerer", "A kind shopkeeper", "A young toymaker", "A merchant"], "answer": 0},
    {"q": "Which danger is mentioned explicitly?", "choices": ["Being exposed or forgotten", "Running out of batteries", "Rusting", "Getting lost"], "answer": 0},
]

QUESTIONS2 = [
    {"q": "Who offered a draw to Rahuma?", "choices": ["A novice", "Magnus Carlsen", "The organizer", "Rahuma's coach"], "answer": 1},
    {"q": "What did Rahuma do?", "choices": ["Accepted", "Declined and played a computer move", "Left", "Asked for time"], "answer": 1},
    {"q": "What is the trophy name?", "choices": ["The Black Queen", "The Golden Rook", "The White King", "The Silver Bishop"], "answer": 2},
    {"q": "Who was named the first recorded winner?", "choices": ["Sualc Atnas", "Magnus Carlsen", "Rahuma", "Unknown"], "answer": 0},
]

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in rgb)

def interp_color(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

class QuizApp:
    def __init__(self, root):
        self.root = root
        root.title("The World Of Toys — Quiz")
        root.geometry("880x640")
        root.configure(bg="#f0f6ff")
 
        self.part = 1
        self.current = 0
        self.score = 0
        self.part_scores = {1:0, 2:0}
        self.current_paragraph = PARAGRAPH1
        self.questions = QUESTIONS1
        self.palette = ["#FFD1DC", "#C8E6C9", "#BBDEFB", "#FFF9C4"]
    
        self.title_font = tkfont.Font(family="Georgia", size=22, weight="bold")
        self.par_font = tkfont.Font(family="Georgia", size=16)
        self.q_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.btn_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

        top = tk.Frame(root, bg="#f0f6ff")
        top.pack(fill="x", padx=16, pady=(12,0))
        tk.Label(top, text="The World Of Toys", font=self.title_font, bg="#f0f6ff", fg="#0b3d91").pack(side="left")

        self.canvas = tk.Canvas(root, height=260, bg="#f6fbff", highlightthickness=0)
        self.canvas.pack(fill="x", padx=16, pady=(12,6))
        self._draw_gradient(self.canvas, 880, 260, "#edf6ff", "#ffffff", steps=60)
        self.par_text_id = self.canvas.create_text(28, 18, anchor="nw", text="", width=820,
                                                   font=self.par_font, fill="#1c2a44")

        mid = tk.Frame(root, bg="#f0f6ff")
        mid.pack(fill="both", expand=True, padx=16, pady=8)
        self.q_label = tk.Label(mid, text="", font=self.q_font, wraplength=820, justify="left", bg="#f0f6ff", fg="#1c2a44")
        self.q_label.pack(anchor="w", pady=(6,4))

        self.buttons_frame = tk.Frame(mid, bg="#f0f6ff")
        self.buttons_frame.pack(fill="x", pady=6)
        self.choice_buttons = []
        for i in range(4):
            b = tk.Button(self.buttons_frame, text="", anchor="w", font=self.btn_font, padx=16,
                          command=lambda i=i: self.select_choice(i), relief="raised", bd=2)
            b.grid(row=i, column=0, sticky="ew", pady=8, ipady=8)
            self.buttons_frame.grid_columnconfigure(0, weight=1)
            self.choice_buttons.append(b)
        
        bottom = tk.Frame(root, bg="#f0f6ff")
        bottom.pack(fill="x", padx=16, pady=(8,16))
        self.score_label = tk.Label(bottom, text=f"Score: {self.score}", bg="#f0f6ff", fg="#0b3d91", font=self.q_font)
        self.score_label.pack(side="left")
        self.next_btn = tk.Button(bottom, text="Next", state="disabled", font=self.btn_font, command=self.next_question, bg="#90caf9", padx=14, pady=6)
        self.next_btn.pack(side="right", padx=(6,0))

        self.restart_btn = tk.Button(bottom, text="Restart", font=self.btn_font, command=self.restart, bg="#b2dfdb", padx=12, pady=6)
        self.restart_btn.pack(side="right", padx=(0,8))

        self.start_overlay = tk.Frame(root, bg="#0b3d91", bd=0)
        self.start_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        lbl = tk.Label(self.start_overlay, text="Are you ready?", font=("Georgia", 28, "bold"), fg="white", bg="#0b3d91")
        lbl.pack(pady=(120,12))
        # create a canvas-based start button so color shows correctly on all platforms
        self.start_canvas = tk.Canvas(self.start_overlay, width=320, height=64, bg="#0b3d91", highlightthickness=0)
        self.start_canvas.pack(pady=(6,0))
        self.start_btn_rect = self.start_canvas.create_rectangle(8, 8, 312, 56, fill="#00BFA5", outline="", width=0)
        self.start_btn_text = self.start_canvas.create_text(160, 32, text="YES — Start Quiz", font=("Helvetica", 14, "bold"), fill="white")
        self.start_canvas.tag_bind(self.start_btn_rect, "<Button-1>", lambda e: self.start_quiz())
        self.start_canvas.tag_bind(self.start_btn_text, "<Button-1>", lambda e: self.start_quiz())
        self.start_canvas.config(cursor="hand2")
       
        self._pulse_val = 0
        self._pulse_dir = 1
        self._pulse()

        self._reveal_index = 0

    def _draw_gradient(self, canvas, w, h, c1, c2, steps=40):
        a = hex_to_rgb(c1)
        b = hex_to_rgb(c2)
        for i in range(steps):
            t = i / max(1, steps-1)
            color = rgb_to_hex(interp_color(a, b, t))
            y0 = int(i * h / steps)
            y1 = int((i+1) * h / steps)
            canvas.create_rectangle(0, y0, w, y1, outline=color, fill=color)

    def _pulse(self):
        
        start = hex_to_rgb("#FF8A65")
        end = hex_to_rgb("#FF7043")
        t = (self._pulse_val / 20.0)
        color = rgb_to_hex(interp_color(start, end, t))
        try:
            # animate canvas button fill if present, otherwise fall back to tk.Button
            if hasattr(self, 'start_canvas') and hasattr(self, 'start_btn_rect'):
                self.start_canvas.itemconfig(self.start_btn_rect, fill=color)
            else:
                self.start_btn.config(bg=color)
        except tk.TclError:
            pass
        self._pulse_val += self._pulse_dir
        if self._pulse_val >= 20:
            self._pulse_dir = -1
        elif self._pulse_val <= 0:
            self._pulse_dir = 1
        self.root.after(90, self._pulse)

  
    def start_quiz(self):
        self.start_overlay.place_forget()
        self.part = 1
        self.current = 0
        self.score = 0
        self.part_scores = {1:0,2:0}
        self.questions = QUESTIONS1
        self.current_paragraph = PARAGRAPH1
        self._reveal_index = 0
        self.canvas.itemconfigure(self.par_text_id, text="")
        self.reveal_paragraph_step()

    def reveal_paragraph_step(self, chunk_size=2, delay=40):
        text = self.current_paragraph
        if self._reveal_index >= len(text):
            self.load_question(animated=True)
            return
        end = min(self._reveal_index + chunk_size, len(text))
        cur = self.canvas.itemcget(self.par_text_id, "text")
        cur = cur + text[self._reveal_index:end]
        self.canvas.itemconfigure(self.par_text_id, text=cur)
        self._reveal_index = end
        self.root.after(delay, lambda: self.reveal_paragraph_step(chunk_size, delay))

    def load_question(self, animated=False):
        if self.current >= len(self.questions):
            if self.part == 1:
                messagebox.showinfo("Part Complete", "You have passed the first part.")
                # prepare part 2
                self.part = 2
                self.questions = QUESTIONS2
                self.current = 0
                self.current_paragraph = PARAGRAPH2
                self._reveal_index = 0
                self.canvas.itemconfigure(self.par_text_id, text="")
                self.reveal_paragraph_step()
                return
            else:
                self.show_result()
                return

        q = self.questions[self.current]
        self.q_label.config(text=f"Q{self.current+1}. {q['q']}")

        # shuffle choices but keep track of original index for answer checking
        pairs = list(enumerate(q["choices"]))
        random.shuffle(pairs)
        for i, (orig_idx, choice) in enumerate(pairs):
            btn = self.choice_buttons[i]
            btn.config(text=choice, state="disabled", bg="SystemButtonFace", fg="#1c2a44")
            btn._target_color = self.palette[i % len(self.palette)]
            btn._orig_index = orig_idx
        self.next_btn.config(state="disabled")
        if animated:
            
            for i in range(len(q["choices"])):
                self.root.after(120 * i, lambda i=i: self._animate_button_appear(self.choice_buttons[i]))
        else:
            for i in range(len(q["choices"])):
                btn = self.choice_buttons[i]
                btn.config(state="normal", bg=self.palette[i % len(self.palette)], activebackground=self.palette[i % len(self.palette)])

    def _animate_button_appear(self, btn, steps=10, delay=25):
     
        try:
            btn.config(state="normal")
        except tk.TclError:
            return
        start = hex_to_rgb("#ffffff")
        target = hex_to_rgb(btn._target_color if hasattr(btn, "_target_color") else "#ffffff")
        def step(n=0):
            t = n/steps
            try:
                btn.config(bg=rgb_to_hex(interp_color(start, target, t)))
            except tk.TclError:
                return
            if n < steps:
                self.root.after(delay, lambda: step(n+1))
        step(0)

    def select_choice(self, idx):
        q = self.questions[self.current]
        correct_orig = q["answer"]

        for b in self.choice_buttons:
            b.config(state="disabled")
        sel_btn = self.choice_buttons[idx]
        # find the button that holds the original correct index
        cor_btn = None
        for b in self.choice_buttons:
            if getattr(b, "_orig_index", None) == correct_orig:
                cor_btn = b
                break

        # compare using stored original indices
        if getattr(sel_btn, "_orig_index", None) == correct_orig:
            self._animate_color_transition(sel_btn, sel_btn.cget("bg"), "#2e7d32")
            self.score += 1
            self.part_scores[self.part] += 1
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self._animate_color_transition(sel_btn, sel_btn.cget("bg"), "#c62828")
            if cor_btn:
                self.root.after(300, lambda: self._animate_color_transition(cor_btn, cor_btn.cget("bg"), "#2e7d32"))

        # auto-advance to the next question after a short delay
        self.root.after(800, lambda: (self.next_btn.config(state="normal"), self.next_question()))

    def _animate_color_transition(self, widget, start_hex, end_hex, steps=12, delay=20):
        a = hex_to_rgb(start_hex)
        b = hex_to_rgb(end_hex)
        def step(n=0):
            t = n/steps
            try:
                widget.config(bg=rgb_to_hex(interp_color(a,b,t)))
            except tk.TclError:
                return
            if n < steps:
                self.root.after(delay, lambda: step(n+1))
        step(0)

    def next_question(self):
        self.current += 1
        self.load_question(animated=True)

    def restart(self):
        self.part = 1
        self.current = 0
        self.score = 0
        self.part_scores = {1:0,2:0}
        self.score_label.config(text=f"Score: {self.score}")
 
        self.start_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_result(self):
        p1 = self.part_scores.get(1, 0)
        p2 = self.part_scores.get(2, 0)
        messagebox.showinfo("Quiz Complete", f"Part 1: {p1}\nPart 2: {p2}\nTotal: {self.score}")
        self.restart()


def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()


if __name__ == "__main__":

    main()