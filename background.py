import pygame

# Background is a class that represents the moving space background.
# It is NOT a Sprite.
# It is just a helper object that:
# - moves the background
# - draws the background
class Background:

    def __init__(self):
        # __init__ is called when the background object is created.
        # This is the "birth moment" of the background.

        # ---- BACKGROUND IMAGE ----
        # Load the background image from file.
        # convert() (without alpha) is enough here because the background
        # does not need transparency.
        # scale(...) resizes the image slightly larger than the window.
        #
        # Why larger?
        # So scrolling looks smooth and no empty gaps appear.
        self.image = pygame.transform.scale(
            pygame.image.load("PICS/Background/cosmos4.png").convert(),
            (1365, 763)
        )

        # Create a rectangle around the background image.
        # This rectangle stores the image width and height.
        self.rect = self.image.get_rect()

        # Speed at which the background moves to the left.
        # Small value = slow, calm movement.
        self.moving_speed = 1

        # ---- FIRST BACKGROUND POSITION ----
        # bgX1 and bgY1 are the position of the first background image.
        self.bgX1 = 0
        self.bgY1 = 0

        # ---- SECOND BACKGROUND POSITION ----
        # bgX2 starts exactly after the first image (to the right).
        # This allows endless scrolling.
        self.bgX2 = self.rect.width
        self.bgY2 = 0

    def update(self):
        # update() is called every frame.
        # It moves the background images to create a scrolling effect.

        # Move both background images to the LEFT.
        # Subtracting moves things left.
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed

        # ---- LOOP FIRST IMAGE ----
        # If the first background has completely moved off-screen:
        if self.bgX1 <= -self.rect.width:
            # Move it to the right side again.
            # This makes the background loop forever.
            self.bgX1 = self.rect.width

        # ---- LOOP SECOND IMAGE ----
        # Same logic for the second background image.
        if self.bgX2 <= -self.rect.width:
            self.bgX2 = self.rect.width

    def render(self, window):
        # render() draws the background images on the screen.

        # Draw first background image at its current position.
        window.blit(self.image, (self.bgX1, self.bgY1))

        # Draw second background image right after it.
        # Together they fill the whole screen and scroll endlessly.
        window.blit(self.image, (self.bgX2, self.bgY2))
