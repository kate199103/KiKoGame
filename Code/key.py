import pygame
# Import pygame.
# We need it for:
# - sprites
# - images
# - rectangles
# - drawing on the screen

import confi

from random import randint
# Import randint so we can place the key at a random height.


# Key is a Sprite.
# This means:
# - it can be added to a sprite group
# - pygame can update it automatically
# - it can remove itself from the game
#
# In the game, the Key represents a HEALTH pickup.
class Key(pygame.sprite.Sprite):

    def __init__(self):
        # __init__ is called when a new Key is created.
        # This is the "birth moment" of the key.

        # Call the parent Sprite constructor.
        # This is REQUIRED so pygame treats this object as a real sprite.
        super().__init__()

        # ---- IMAGE ----
        # Load the key image from file.
        # scale(...) resizes the image to 106x88 pixels.
        # (Transparency is already fine here, so convert_alpha is optional.)
        self.image = pygame.transform.scale(
            pygame.image.load("PICS/Stats/key.png").convert_alpha(),(106, 88))

        # ---- RECTANGLE (POSITION & SIZE) ----
        # Create a rectangle around the image.
        #
        # center=(x, y) places the CENTER of the key at:
        # - x = bg.WIDTH  -> start just at the right edge of the screen
        # - y = random number between 118 and 620
        #
        # This makes the key:
        # - fly in from the right
        # - appear at different vertical positions
        self.rect = self.image.get_rect(center=(confi.WIDTH, randint(118, 620)))

        # ---- HITBOX ----
        # Create a smaller collision box for the key.
        # inflate(-20, -20) makes the hitbox smaller than the image.
        # This makes collecting the key feel fair and pleasant.
        self.hitbox = self.rect.inflate(-20, -20)

    def update(self):
        # update() is called every frame while the key exists.
        # It controls movement, collision position, and removal.

        # Move the key to the LEFT by 3 pixels.
        # Keys always move at the same speed.
        self.rect.x -= 3

        # Keep the hitbox centered on the image.
        # This ensures collision detection stays correct.
        self.hitbox.center = self.rect.center

        # If the key has completely left the screen on the left side:
        if self.rect.right < 0:
            # kill() removes the key from all sprite groups.
            # After this, it no longer updates or draws.
            self.kill()

    def draw(self, window):
        # draw() draws the key image on the game window.

        # window.blit(image, rect) means:
        # "Draw this image at this position"
        window.blit(self.image, self.rect)
