import pygame
import confi


# SpaceObject represents ONE department in space.
# Each department:
# - flies in from the right
# - stops at a fixed position
# - can be clicked to open a quiz
# - leaves the screen after the quiz is finished
#
# It is a Sprite, so it can:
# - be put into a sprite group
# - be updated automatically with group.update()
# - be removed using kill()
class Border(pygame.sprite.Sprite):

    def __init__(self, stop_x, image_path, dept_id, title, y):
        # __init__ runs when a new department object is created.
        # All important properties of the department are set here.

        # Call the parent Sprite class constructor.
        # This is REQUIRED whenever you inherit from pygame.sprite.Sprite.
        super().__init__()

        # ---- IMAGE ----
        # Load the department image from the given file path.
        # convert_alpha() keeps transparency (important for PNG images).
        # smoothscale() resizes the image nicely to 220x220 pixels.
        self.image = pygame.transform.smoothscale(pygame.image.load(image_path).convert_alpha(),(220, 220))

        # Create a rectangle around the image.
        # The rect stores the position and size of the department.
        self.rect = self.image.get_rect()

        # Start the department completely off-screen on the right.
        # bg.WIDTH is the screen width, so this means "just outside the view".
        self.rect.x = confi.WIDTH

        # Vertical position of the department.
        # This is passed in as "y" so different departments
        # can appear at different heights.
        self.rect.y = y

        # ---- MOVEMENT ----
        # Speed at which the department moves horizontally.
        self.speed = 2

        # stop_x is the x-position where the department should stop moving
        # and wait for the player to click it.
        self.stop_x = stop_x

        # ---- IDENTIFICATION ----
        # dept_id is a unique identifier for this department.
        # It is used to:
        # - remember which departments were completed
        # - prevent the same department from appearing twice
        self.dept_id = dept_id

        # title is the name of the department.
        # It is shown in the quiz screen.
        self.title = title

        # ---- STATE ----
        # fly_out = False means:
        # "The department is either flying in or waiting."
        #
        # fly_out = True means:
        # "The quiz is finished and the department should fly away."
        self.fly_out = False

    def start_fly_out(self):
        # This function is called when the quiz for this department is finished.
        # It switches the department into "leaving mode".
        self.fly_out = True

    def update(self):
        # update() is called every frame by the sprite group.
        # It controls how the department moves.

        # ---- NORMAL STATE (not leaving yet) ----
        if not self.fly_out:
            # If the department has not yet reached its stop position:
            if self.rect.x > self.stop_x:
                # Move the department to the left.
                self.rect.x -= self.speed
            else:
                # Once it reaches the stop position,
                # keep it fixed exactly at stop_x.
                self.rect.x = self.stop_x

        # ---- LEAVING STATE ----
        else:
            # Move the department faster to the left when leaving.
            # Multiplying speed makes the exit feel quicker and clearer.
            self.rect.x -= self.speed * 2

            # If the department has completely left the screen:
            if self.rect.right < 0:
                # Remove this sprite from all sprite groups.
                # After this, it no longer exists in the game.
                self.kill()
