import pygame
import confi

# We import MMain
# This file contains WIDTH and HEIGHT of the game window.
# Using MMain.WIDTH and MMain.HEIGHT helps us place things correctly on screen.


# =====================================================
#                  START SCREEN
# =====================================================
# This class controls the FIRST screen the player sees:
# - the Start button
# - the Rules button
# - the logo
#
# It does NOT run the game.
# It only shows buttons and reacts to clicks.
class StartScreen:

    def __init__(self):
        # __init__ runs once when StartScreen() is created.
        # Here we prepare everything we will need later.

        # ----- FONTS -----
        # Fonts are used to draw text on the screen.
        # We use two sizes:
        # - a bigger one for button titles
        # - a smaller one for helper text
        self.font_btn = pygame.font.SysFont("Optima", 44)
        self.font_btn_small = pygame.font.SysFont("Optima", 24)

        # ----- BUTTON SIZE -----
        # These numbers define how big our buttons are.
        # Bigger buttons are easier to click and read.
        self.btn_w = 560
        self.btn_h = 110

        # ----- BUTTON RECTANGLES -----
        # pygame.Rect creates a rectangle.
        # Rectangles are VERY important in pygame:
        # - we draw buttons using rectangles
        # - we detect mouse clicks using rectangles
        #
        # We center the buttons horizontally by subtracting half their width.
        self.btn_start = pygame.Rect(
            confi.WIDTH // 2 - self.btn_w // 2,   # left position (centered)
            confi.HEIGHT // 2 - 15,               # vertical position
            self.btn_w,
            self.btn_h
        )

        self.btn_rules = pygame.Rect(
            confi.WIDTH // 2 - self.btn_w // 2,
            confi.HEIGHT // 2 + 120,               # placed below Start button
            self.btn_w,
            self.btn_h
        )

        # ----- LOGO IMAGE -----
        # We load the logo ONCE here (not every frame).
        # This is faster and simpler.
        #
        # IMPORTANT:
        # convert_alpha() needs a window to exist,
        # so this class must be created AFTER set_mode() in Main.
        self.logo = pygame.image.load(
            'PICS/Player_right/LOGO.png'
        ).convert_alpha()

        # Resize the logo so it fits nicely on screen.
        self.logo = pygame.transform.smoothscale(self.logo, (950, 300))

    def draw(self, window, start_allowed=False):
        # draw() is called every frame while the menu is visible.
        #
        # window → the game window we draw on
        # start_allowed → tells us if the Start button is active or locked

        # ----- DARK OVERLAY -----
        # This makes the menu easier to read by darkening the background.
        overlay = pygame.Surface((confi.WIDTH, confi.HEIGHT))
        overlay.set_alpha(150)          # transparency (0 = invisible, 255 = solid)
        overlay.fill((0, 0, 0))         # black color
        window.blit(overlay, (0, 0))    # draw overlay

        # ----- DRAW LOGO -----
        # Draw the logo near the top of the screen.
        window.blit(
            self.logo,
            self.logo.get_rect(center=(confi.WIDTH // 2, 170))
        )

        # =================================================
        #                  START BUTTON
        # =================================================
        if start_allowed:
            # ACTIVE START BUTTON
            # This means the player has already read the rules.

            pygame.draw.rect(
                window,
                (39, 44, 78),           # dark blue color
                self.btn_start,
                border_radius=18
            )
            pygame.draw.rect(
                window,
                (255, 255, 255),        # white border
                self.btn_start,
                2,
                border_radius=18
            )

            # Draw the text "Start"
            t1 = self.font_btn.render("Start", True, "white")
            window.blit(t1, t1.get_rect(center=self.btn_start.center))

        else:
            # LOCKED START BUTTON
            # The player must read the rules first.

            pygame.draw.rect(
                window,
                (128, 128, 128),        # gray color
                self.btn_start,
                border_radius=18
            )
            pygame.draw.rect(
                window,
                (255, 255, 255),
                self.btn_start,
                2,
                border_radius=18
            )

            # Two lines of text so it fits inside the button
            line1 = self.font_btn.render("Start", True, (96, 96, 96))
            line2 = self.font_btn_small.render("(Read the rules first)", True, (96, 96, 96))

            window.blit(
                line1,
                line1.get_rect(center=(self.btn_start.centerx, self.btn_start.centery - 18))
            )
            window.blit(
                line2,
                line2.get_rect(center=(self.btn_start.centerx, self.btn_start.centery + 18))
            )

        # =================================================
        #                  RULES BUTTON
        # =================================================
        # This button is ALWAYS clickable.

        pygame.draw.rect(
            window,
            (39, 44, 78),
            self.btn_rules,
            border_radius=18
        )
        pygame.draw.rect(
            window,
            (255, 255, 255),
            self.btn_rules,
            2,
            border_radius=18
        )

        t2 = self.font_btn.render("Assessment rules", True, "white")
        window.blit(t2, t2.get_rect(center=self.btn_rules.center))

    def handle_click(self, pos, start_allowed=False):
        # This function checks WHERE the user clicked.
        # pos is a tuple: (mouse_x, mouse_y)

        # Did the user click the Start button?
        if self.btn_start.collidepoint(pos):
            if start_allowed:
                return "start"   # tell Main to start the game
            return None          # Start is locked → ignore click

        # Did the user click the Rules button?
        if self.btn_rules.collidepoint(pos):
            return "rules"

        # Click was somewhere else
        return None


# =====================================================
#                  RULES SCREEN
# =====================================================
# This class shows the rules as full-screen images.
# The player clicks a circle button to go forward.
class RulesScreen:

    def __init__(self):
        # Font for the arrow symbol ">"
        self.font_arrow = pygame.font.SysFont("Gill Sans", 40)

        # List of image paths for the rules slides
        self.rule_images = [
            "PICS/Rules/Rules/Ru1.png",
            "PICS/Rules/Rules/Ru2.png",
            "PICS/Rules/Rules/Ru3.png",
            "PICS/Rules/Rules/Ru4.png",
            "PICS/Rules/Rules/Ru5.png",
            "PICS/Rules/Rules/Ru6.png",
            "PICS/Rules/Rules/Ru7.png",
            "PICS/Rules/Rules/Ru8.png",
            "PICS/Rules/Rules/Ru9.png",
            "PICS/Rules/Rules/Ru10.png",
            "PICS/Rules/Rules/Ru11.png",
            "PICS/Rules/Rules/Ru12.png",
            "PICS/Rules/Rules/Ru13.png",
            "PICS/Rules/Rules/Ru14.png",
            "PICS/Rules/Rules/Ru15.png",
            "PICS/Rules/Rules/Ru16.png",
        ]

        # index tells us WHICH rule image is currently shown
        self.index = 0

        # _loaded will store the loaded images
        # so we don’t load them again and again
        self._loaded = []

        # Circle button settings
        self.circle_r = 30
        self.circle_center = (confi.WIDTH - 90, confi.HEIGHT - 90)

    def open(self):
        # Called when entering the rules screen.
        # Always start at the first slide.
        self.index = 0

        # Load images only once
        if not self._loaded:
            for p in self.rule_images:
                img = pygame.image.load(p).convert_alpha()
                img = pygame.transform.smoothscale(img, (confi.WIDTH, confi.HEIGHT))
                self._loaded.append(img)

    def _circle_hit(self, pos):
        # Checks if the mouse click is inside the circle.
        # This uses simple distance math.

        x, y = pos
        cx, cy = self.circle_center

        # If distance² <= radius² → inside the circle
        return (x - cx) ** 2 + (y - cy) ** 2 <= self.circle_r ** 2

    def draw(self, window):
        # Draw the current rule image
        window.blit(self._loaded[self.index], (0, 0))

        # Draw the circle button
        pygame.draw.circle(window, (39, 44, 78), self.circle_center, self.circle_r)
        pygame.draw.circle(window, (200, 200, 200), self.circle_center, self.circle_r, 2)

        # Draw the arrow inside the circle
        arrow = self.font_arrow.render(">", True, "white")
        window.blit(arrow, arrow.get_rect(center=self.circle_center))

    def handle_click(self, pos):
        # If user clicks the circle, move to next slide
        if self._circle_hit(pos):
            self.index += 1

            # If all slides were shown, tell Main we are done
            if self.index >= len(self._loaded):
                return "done"

        return None
