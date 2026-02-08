import pygame
import confi
import departments_data


# We use MMain.WIDTH and MMain.HEIGHT to position quiz elements
# exactly relative to your game window size.


# ============================================================
#                       QUIZ CLASS
# ============================================================
# This class controls the quiz overlay that appears when the player
# clicks a department.
#
# Important idea:
# - The quiz is an "overlay": it draws ON TOP of the game.
# - When quiz.active == True, Main usually freezes the gameplay
#   (so asteroids do not attack while answering).
#
# Quiz does 4 main jobs:
# 1) Store the current department title + questions
# 2) Track which question we are on (q_index)
# 3) Track how many answers are correct (correct)
# 4) Draw the quiz screen and process clicks
class Quiz:

    def __init__(self, font_big, font_medium, font_small):
        # __init__ is called when you create Quiz(font_big, font_small).
        # We receive fonts from Main so the whole game has consistent style.

        self.font_big = font_big
        # Store the big font (used for question titles, results headers)

        self.font_medium = font_medium
        # Store the big font (used for question titles, results headers)

        self.font_small = font_small
        # Store the small font (used for answers, score line, continue button)

        # -------------------------
        # QUIZ STATE SWITCHES
        # -------------------------

        self.quiz_active = False
        # active == False means:
        #   quiz is NOT visible / not running
        # active == True means:
        #   quiz is currently shown on the screen

        # -------------------------
        # DEPARTMENT-SPECIFIC DATA
        # -------------------------

        self.list_of_questions = []
        # This list will store the department questions.
        # It will later become:
        #   [(question_text, [answers], correct_index), ...]
        # We start with an empty list because no department is opened yet.

        self.department_title = ""
        # This string will store the department title (like "AI Basics").
        # We start empty because no department is opened yet.

        # -------------------------
        # QUIZ PROGRESS
        # -------------------------

        self.question_index = 0
        # question_index = which question we are currently showing.
        # Example:
        #   question_index = 0 -> first question
        #   question_index = 1 -> second question

        self.correct_answered_q = 0
        # stores how many answers the player got correct so far.

        # -------------------------
        # RESULTS BUTTON RECTANGLE
        # -------------------------
        self.answer_rects = [] #A list of invisible boxes that sit on top of the answer texts so the game knows where the player clicked
        self.continue_rect = pygame.Rect(
            confi.WIDTH // 2 - 200,      # x-position: center the button horizontally
            confi.HEIGHT // 2 + 120,     # y-position: below the center area
            400,                      # width
            70                        # height
        )
        # This rectangle is used for the "Continue" button.
        # We draw it on the results screen and check clicks inside it.

    #Open and close of the quiz window
    def open_quiz (self,dept_data):
        self.quiz_active = True
        self.department_title = dept_data ["title"]
        self.list_of_questions = dept_data ["questions"]
        self.question_index = 0
        self.correct_answered_q = 0

    def close_quiz (self):
        self.quiz_active = False

    def wrap_to_three_lines(self, text, font, max_width):

        words = text.split()
        lines = ["","",""]
        line_index = 0
        i = 0

        # Build first line
        while i < len(words) and line_index < 3:
            test = (lines[line_index] + " " + words[i]).strip()
            if font.size(test)[0] <= max_width:
                lines[line_index] = test
                i += 1
            else:
                line_index += 1

        # If still words left -> add ellipsis to line2
        if i < len(words):
                while font.size(lines[2] + "...")[0] > max_width and len(lines[2]) > 0:
                    lines[2] = lines[2][:-1].rstrip()
                lines[2] = (lines[2] + "...") if lines[2] else "..."
        return lines [0], lines [1], lines [2]

    def wrap_answer_to_two_lines(self, text, font, max_width):
        words = text.split(" ")
        line1 = ""
        i = 0

        while i < len(words):
            test = (line1 + " " + words[i]).strip()
            if font.size(test)[0] <= max_width:
                line1 = test
                i += 1
            else:
                break

        line2 = ""

        while i < len(words):
            test = (line2 + " " + words[i]).strip()
            if font.size(test)[0] <= max_width:
                line2 = test
                i += 1
            else:
                break

        if i < len(words):
            while font.size(line2 + "...")[0] > max_width and len(line2) > 0:
                line2 = line2[:-1].rstrip()
            line2 += "..."
        return line1, line2

    #Clicks in the test
    def handle_click(self, pos):
        if not self.quiz_active:
            return None

        if self.question_index >= len(self.list_of_questions): #if all questions answered, stop the quiz and show results
            if self.continue_rect.collidepoint(pos):
                self.close_quiz()
                return "finished"
            return None

            # Otherwise: we are in question screen
            # Check if user clicked one of the answer boxes
        for i, rect in enumerate(self.answer_rects):
            if rect.collidepoint(pos):
                _, _, correct_idx = self.list_of_questions[self.question_index]

                if i == correct_idx:
                    self.correct_answered_q += 1

                self.question_index += 1  # go to next question
                return "answered"

        return None


    def draw(self, window):
        # draw() draws the quiz overlay onto the window.

        if not self.quiz_active:
            # If quiz is not active, do not draw anything.
            return

        # -------------------------
        # DARK OVERLAY
        # -------------------------
        overlay = pygame.Surface((confi.WIDTH, confi.HEIGHT))
        # Create a full-screen surface.

        overlay.set_alpha(220)
        # Make it semi-transparent (0 invisible, 255 fully opaque).

        overlay.fill((0, 0, 0))
        # Fill overlay with black color.

        window.blit(overlay, (0, 0))
        # Draw overlay on top of the screen.

        # -------------------------
        # RESULTS SCREEN DRAWING
        # -------------------------
        if self.question_index >= len(self.list_of_questions):
            title = self.font_big.render(f"{self.department_title} - RESULTS", True, "white")
            # Render the title text.

            window.blit(title, title.get_rect(center=(confi.WIDTH // 2, confi.HEIGHT // 2 - 60)))
            # Draw title centered slightly above the center.

            res = self.font_medium.render(
                f"Correct: {self.correct_answered_q} / {len(self.list_of_questions)}",
                True,
                "white"
            )
            # Render result line showing score.

            window.blit(res, res.get_rect(center=(confi.WIDTH // 2, confi.HEIGHT // 2 + 10)))
            # Draw results text slightly below the center.

            # Draw Continue button background
            pygame.draw.rect(window, (60, 60, 60), self.continue_rect, border_radius=12)

            # Draw Continue button border
            pygame.draw.rect(window, (200, 200, 200), self.continue_rect, 2, border_radius=12)

            # Draw Continue text
            t = self.font_medium.render("Continue", True, "white")
            window.blit(t, t.get_rect(center=self.continue_rect.center))

            return
            # Stop here so we don't draw question screen too.

        # -------------------------
        # QUESTION SCREEN DRAWING
        # -------------------------

        q, answers, _ = self.list_of_questions[self.question_index]
        # Get current question tuple:
        # q = question text
        # answers = list of 4 answers
        # _ = correct index (we do not need it for drawing)

        # -------------------------
        # QUESTION HEADER (2 LINES)
        # -------------------------

        # Line 1: Department title (big font)
        line1 = self.font_small.render(self.department_title, True, "white")
        window.blit(
            line1,
            line1.get_rect(center=(confi.WIDTH // 2, 110))
        )

        # 2) + 3) Lines: question (small), wrapped into max 2 lines
        question_text = f"Q{self.question_index + 1}/{len(self.list_of_questions)}: {q}"
        q1, q2, q3 = self.wrap_to_three_lines(question_text, self.font_big, max_width=1150)

        q_line_1 = self.font_big.render(q1, True, "white")
        q_line_2 = self.font_big.render(q2, True, "white")
        q_line_3 = self.font_big.render(q3, True, "white")

        window.blit(q_line_1, q_line_1.get_rect(center=(confi.WIDTH // 2, 145)))
        window.blit(q_line_2, q_line_2.get_rect(center=(confi.WIDTH // 2, 175)))
        window.blit(q_line_3, q_line_3.get_rect(center=(confi.WIDTH // 2, 205)))

        # Answer rectangles
        self.answer_rects.clear()

        for i, ans in enumerate (answers):
            rect = pygame.Rect(confi.WIDTH // 2 - 550, 260 + i * 95, 1100, 75)
            self.answer_rects.append(rect)

            pygame.draw.rect(window, (255, 255, 255), rect, border_radius=12)
            pygame.draw.rect(window, (200, 200, 200), rect, 1, border_radius=12)

            a1,a2 = self.wrap_answer_to_two_lines(ans, self.font_small, max_width=1000)

            if a2 == "":
                a_line = self.font_small.render(a1, True, "black")
                window.blit(a_line, a_line.get_rect(center=rect.center))
            else:
                a_line_1 = self.font_small.render(a1, True, "black")
                a_line_2 = self.font_small.render(a2, True, "black")

                line_spacing = 24
                center_y = rect.centery

                window.blit(a_line_1, a_line_1.get_rect(center=(rect.centerx, center_y - line_spacing // 2)))
                window.blit(a_line_2, a_line_2.get_rect(center=(rect.centerx, center_y + line_spacing // 2)))

    def get_score(self):
        return self.correct_answered_q
