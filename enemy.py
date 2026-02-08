import pygame
import confi

from random import randint
# Import randint from the random module.
# randint(a, b) gives a RANDOM whole number between a and b (including both).


# Komets is an enemy object (asteroid).
# It is a Sprite, which means:
# - it can live inside a pygame.sprite.Group
# - it can update itself automatically
# - it can remove itself from the game
class Komets(pygame.sprite.Sprite):

    def __init__(self, speed):
        # __init__ is called when a new comet is created.
        # speed is given from outside and controls how fast the comet moves.

        # Call the parent Sprite constructor.
        # This is REQUIRED so pygame knows this object is a real sprite.
        super().__init__()

        # A list of possible asteroid images.
        # Each comet will randomly choose one of these.
        self.asteroids = [
            'PICS/Enemy/Stone1.png',
            'PICS/Enemy/Stone2.png'
        ]

        # ---- IMAGE SETUP ----
        # randint(0, 1) randomly chooses 0 or 1.
        # self.stones[...] then selects one of the two image paths.
        # pygame.image.load(...) loads the image file.
        # convert_alpha() keeps transparency and makes drawing faster.
        # scale(...) resizes the image to a fixed size.
        self.image = pygame.transform.scale(
            pygame.image.load(self.asteroids[randint(0, 1)]).convert_alpha(),(106, 88))

        # ---- RECTANGLE (POSITION & SIZE) ----
        # Create a rectangle around the image.
        # This rectangle controls position and movement.
        self.rect = self.image.get_rect()
        self.rect.x = confi.WIDTH
        self.rect.y = randint(0,620)

        # ---- MOVEMENT SPEED ----
        # Store how fast the comet moves to the left.
        self.speed = speed

        # ---- HITBOX (COLLISION AREA) ----
        # The hitbox is smaller than the image.
        # inflate(-15, -65) reduces the size of the rectangle:
        # - width becomes smaller by 15 pixels
        # - height becomes smaller by 65 pixels
        # This makes collisions feel fairer for the player.
        self.hitbox = self.rect.inflate(-15, -65)

    def update(self):
        # update() is called EVERY FRAME while the comet exists.
        # This controls movement, collision position, and removal.

        # Move the comet to the LEFT by "speed" pixels.
        # Subtracting from x moves the object left.
        self.rect.x -= self.speed

        # Keep the hitbox centered on the image.
        # This ensures collision detection stays correct while moving.
        self.hitbox.center = self.rect.center

        # Check if the comet has completely left the screen on the left side.
        # rect.right < 0 means the whole comet is off-screen.
        if self.rect.right < 0:
            # kill() removes the comet from all sprite groups.
            # After this, it no longer updates or draws.
            self.kill()

    def draw(self, window):
        # draw() draws the comet on the screen.

        # window.blit(image, rect) means:
        # "Draw this image at this rectangle position"
        window.blit(self.image, self.rect)
