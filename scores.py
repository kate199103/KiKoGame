import pygame
import confi
from departments_data import Departments


# Scores is a helper class that keeps track of the game's "status" and "UI".
# It does not move around like the hero or enemies.
# It mainly does two big jobs:
# 1) Remember important information (progress, score, game state)
# 2) Draw UI on the screen (health icons, visited departments, end texts, restart button)
class Scores:
    def __init__(self, window):
        # __init__ runs once when Scores(window) is created.
        # This is the "setup moment" for everything this class needs.

        # -------------------------------
        # UI IMAGES
        # -------------------------------

        # Load the health icon image (gear).
        # convert_alpha() keeps transparency and optimizes drawing.
        # smoothscale() resizes smoothly to look better (less pixelated).
        self.image_hp = pygame.transform.smoothscale(
            pygame.image.load("PICS/Stats/gear-cog-setting.png").convert_alpha(),
            (70, 70)
        )

        # Load the progress icon that is shown near the number of completed departments.
        self.image_progress = pygame.transform.smoothscale(
            pygame.image.load("PICS/Departaments/visited depa.png").convert_alpha(),
            (132, 90)
        )

        # Store the window surface so we can draw everything on it.
        self.window = window

        # -------------------------------
        # PROGRESS / SCORE (memory)
        # -------------------------------

        # completed_departments is a SET.
        # A set is like a list, but it never contains duplicates.
        # It is perfect for saving finished department IDs:
        # - you cannot accidentally store the same department twice
        # - checking if something is inside is very fast
        self.completed_departments = set()

        # total_correct_answers stores how many quiz answers were correct across ALL departments.
        # Every time a department quiz is finished, we add its correct answers to this number.
        self.total_correct_answers = 0

        # max_answers is the maximum number of correct answers possible.
        # You have 5 departments and each has 5 questions => 25.
        self.max_answers = sum(len(d["questions"]) for d in Departments)

        # -------------------------------
        # GAME STATE (switches)
        # -------------------------------

        # game = True means the game is running normally.
        # When game becomes False, the gameplay "stops" and we show end messages.
        self.game = True

        # game_over = True means the player LOST (health reached 0).
        # We use this to show the restart button.
        self.game_over = False

        # reached_planet = True means the player WON by colliding with the final planet.
        # We use this to show the mission completed text.
        self.reached_planet = False

        # -------------------------------
        # RESTART BUTTON (UI)
        # -------------------------------

        # restart_rect defines the position and size of the restart button.
        # We draw the button using this rectangle
        # and we detect clicks using collidepoint().
        self.restart_rect = pygame.Rect(
            confi.WIDTH // 2 - 220,     # center the button horizontally (move left by half width)
            confi.HEIGHT // 2 + 120,    # place it below the center of the screen
            440,                     # width of the button
            80                       # height of the button
        )

    def show_health(self, hero):
        # This function draws the health icons (gears) on the screen.
        # It does NOT change health. Health belongs to hero.health.
        # Scores only shows what hero currently has.

        # Start drawing at x = 10 (near the left edge).
        x = 10

        # For each health point the hero has:
        # If hero.health = 3 -> loop runs 3 times -> 3 gears drawn.
        for _ in range(hero.health):
            # Draw one gear icon at (x, 20)
            self.window.blit(self.image_hp, (x, 20))

            # Move x to the right so the next gear does not overlap.
            x += 70

    def visited_departments(self):
        # This function draws how many departments were completed.
        # It uses the completed_departments set.

        # Count how many departments are finished.
        count = len(self.completed_departments)

        # Create a font object to draw the number.
        # SysFont picks a system font by name.
        font = pygame.font.SysFont("Optima", 50)

        # Turn the number into a text image (surface).
        # render(text, antialias, color)
        text = font.render(str(count), True, "white")

        # Draw the progress icon image.
        self.window.blit(self.image_progress, (1000, 20))

        # Draw the number next to the icon.
        self.window.blit(text, (1110, 10))

    def finish(self, hero):
        # This function checks if the game should end
        # and draws the final messages.

        # -------------------------------
        # WIN CONDITION
        # -------------------------------
        # If reached_planet is True, the player has already won.
        # We show the win text and stop the game.
        if self.reached_planet:
            self._draw_win_text()
            self.game = False
            return

        # -------------------------------
        # LOSE CONDITION
        # -------------------------------
        # If hero health is 0 or less, the player lost.
        if hero.health <= 0:
            self._draw_lose_text()
            self.game = False
            self.game_over = True

    def _draw_lose_text(self):
        # Helper function that draws the "game over" message.
        # We keep it separate so finish() is easier to read.

        font = pygame.font.SysFont("Optima", 50)
        text = font.render("You were not cautious enough", True, "white")

        # Draw it on the screen.
        self.window.blit(text, (275, 330))

    def _draw_win_text(self):
        # Helper function that draws the "mission completed" message and the score.
        # Separate function = less clutter inside finish().

        font_big = pygame.font.SysFont("Optima", 40)
        font_small = pygame.font.SysFont("Optima", 30)

        # First line: winning message.
        line1 = font_big.render(
            "Mission completed! You successfully reached AIity",
            True,
            "white"
        )

        # Second line: show score.
        # f"..." is an f-string: it allows us to insert variables inside text.
        line2 = font_small.render(
            f"with a score of: {self.total_correct_answers} / {self.max_answers}",
            True,
            "white"
        )

        # Draw both lines.
        self.window.blit(line1, (225, 330))
        self.window.blit(line2, (225, 400))

    def draw_restart_button(self):
        # This function draws the restart button,
        # but ONLY when the player lost (game_over == True).

        # If the game is not over, do nothing.
        if not self.game_over:
            return

        # Draw button background (filled rectangle).
        pygame.draw.rect(self.window, (39, 44, 78), self.restart_rect, border_radius=12)

        # Draw button border (2 px thickness).
        pygame.draw.rect(self.window, (255, 255, 255), self.restart_rect, 2, border_radius=12)

        # Draw button text.
        font = pygame.font.SysFont("Optima", 40)
        t = font.render("Start from beginning", True, "white")

        # Center the text inside the button rectangle.
        self.window.blit(t, t.get_rect(center=self.restart_rect.center))

    def restart_clicked(self, pos):
        # This function checks if the restart button was clicked.
        # pos is the mouse position (x, y).

        # Returns True only if:
        # - game_over is True
        # - click position is inside restart_rect
        return self.game_over and self.restart_rect.collidepoint(pos)

    def add_department_score(self, correct_answers):
        # This function adds the correct answers from one department to the total score.
        # Example: department 1 correct = 4
        # total_correct_answers becomes +4

        self.total_correct_answers += correct_answers
