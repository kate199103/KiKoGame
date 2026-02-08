import pygame
# Import pygame.
# We need this for images, sprites, rectangles, and drawing on the screen.
import main



# Planet is a Sprite.
# This means:
# - it can be put into a pygame.sprite.Group
# - it can use group.update() and group.draw()
class Planet(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent Sprite constructor.
        # This is REQUIRED when you inherit from pygame.sprite.Sprite.
        super().__init__()

        # ---- PLANET IMAGE ----
        # Load the planet image from file.
        # convert_alpha() keeps transparency and optimizes drawing.
        # scale() resizes the planet to 360x360 pixels.
        self.image = pygame.transform.scale(
            pygame.image.load("PICS/New Hero, Rocket/last planet.png").convert_alpha(),
            (360, 360)
        )

        # ---- RECTANGLE (POSITION & SIZE) ----
        # Create a rectangle with the same size as the image.
        self.rect = self.image.get_rect()

        # Start the planet outside the screen on the right side.
        # bg.WIDTH is the width of the game window.
        self.rect.x = main.WIDTH

        # Place the planet vertically near the center of the screen.
        # bg.HEIGHT // 2 is the vertical center.
        # -130 moves it slightly upward so it looks nicely centered.
        self.rect.y = 200

        # ---- MOVEMENT ----
        # Speed determines how fast the planet moves left.
        self.speed = 2

        # stop_x is the x-position where the planet should stop moving.
        # The planet will slowly enter the screen and stop here.
        self.stop_x = 750

        # ---- HITBOX (FOR COLLISION) ----
        # The hitbox is smaller than the image.
        # inflate(-70, -70) reduces width and height by 70 pixels.
        # This makes the final collision easier and more "friendly".
        self.hitbox = self.rect.inflate(-70, -70)

    def update(self):
        # update() is called every frame when the planet is in a sprite group.
        # It controls the planet's movement and hitbox updates.

        # If the planet has not yet reached its stop position:
        if self.rect.x > self.stop_x:
            # Move the planet left by "speed" pixels.
            self.rect.x -= 2

        # Keep the hitbox centered on the planet.
        # This ensures collision detection stays accurate.
        self.hitbox.center = self.rect.center

    def draw(self, window):
        # draw() draws the planet image onto the game window.
        # window is the main display surface from main.py.
        window.blit(self.image, self.rect)
