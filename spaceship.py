import pygame

class Spaceship:
    def __init__(self, window):

        self.fly_right = [
            pygame.transform.scale(
                pygame.image.load('PICS/Player_right/R11.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_right/R22.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_right/R33.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_right/R44.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_right/R55.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_right/R66.png').convert_alpha(), (230, 150)),
        ]

        self.move_left = [
            pygame.transform.scale(
                pygame.image.load('PICS/Player_left/L11.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_left/L22.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_left/L33.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_left/L44.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_left/L55.png').convert_alpha(), (230, 150)),
            pygame.transform.scale(
                pygame.image.load('PICS/Player_left/L66.png').convert_alpha(), (230, 150)),
        ]

        # Store the game window so the hero can draw itself later.
        self.window = window

        # Set the starting image (first right-facing frame).
        self.index = 0
        self.image = self.fly_right[self.index]

        # Create a rectangle around the image.
        # The rectangle is used for position and movement.
        # The hero starts in the middle of the screen at (600, 400).
        self.rect = self.image.get_rect(center=(600,400))

        # Create a hitbox for collisions.
        # inflate(0, -100) means:
        # - width stays the same
        # - height becomes smaller by 100 pixels
        # This makes collisions fairer (not the full image size).
        self.hitbox = self.rect.inflate(0, -100)

        # Speed of the hero (pixels per frame).
        self.speed = 3

        # Health points (lives).
        self.health = 3

    def update(self):
        # update() is called every frame while the game runs.
        # It handles:
        # - movement
        # - animation
        # - drawing
        # - hitbox updates

        # ---- ANIMATION DEFAULT ----
        # NOTE (Tiny note #2):
        # This sets a default animation frame every frame.
        # If no key is pressed, the rocket still animates gently.
        #
        # self.index // 6 explanation (Tiny note #1):
        # index goes from 0 to 30.
        # Dividing by 6 gives values from 0 to 5.
        # That matches the 6 images in move_right / move_left.
        # This slows down animation so it doesn't change every frame.
        self.image = self.fly_right[self.index // 6] #default direction

        # Get the current state of all keyboard keys.
        # keys[pygame.K_RIGHT] is True if the RIGHT arrow is held down.
        arrow = pygame.key.get_pressed()

        # ---- MOVE RIGHT ----
        # If RIGHT arrow is pressed and the hero is not too far right:
        if arrow[pygame.K_RIGHT] and self.rect.x < 700:
            # Use right-facing animation
            self.image = self.fly_right[self.index // 6]
            # Move hero to the right
            self.rect.x += self.speed

        # ---- MOVE LEFT ----
        # If LEFT arrow is pressed and hero is not too far left:
        if arrow[pygame.K_LEFT] and self.rect.x > 0:
            # Use left-facing animation
            self.image = self.move_left[self.index // 6]
            # Move hero to the left
            self.rect.x -= self.speed

        # ---- MOVE UP ----
        # If UP arrow is pressed and hero is above the top limit:
        # (118 prevents moving into the UI / top area)
        if arrow[pygame.K_UP] and self.rect.y > 45:
            self.rect.y -= self.speed

        # ---- MOVE DOWN ----
        # If DOWN arrow is pressed and hero is below the bottom limit:
        if arrow[pygame.K_DOWN] and self.rect.y < 560:
            self.rect.y += self.speed

        # ---- ANIMATION COUNTER ----
        # Increase animation index to move to the next frame.
        # 0 → 30 gives a smooth loop.
        if self.index < 30:
            self.index += 1
        else:
            # Reset index to loop animation again.
            self.index = 0

        # ---- DRAW HERO ----
        # Draw the current image at the hero's position.
        self.window.blit(self.image, self.rect)

        # ---- UPDATE HITBOX ----
        # Keep hitbox centered on the hero.
        self.hitbox.center = self.rect.center
