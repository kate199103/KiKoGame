import asyncio
import pygame
import background
import Events
from spaceship import Spaceship               #  rocket
from Test import Quiz                 # Quiz overlay
from sound import music
from scores import Scores             # Health / progress / win-lose logic + restart button
from start_screen import StartScreen, RulesScreen  # Menu screens
from departments_data import Departments           # To know how many departments exist
from confi import WIDTH, HEIGHT

async def run():

    pygame.init()

    pygame.display.set_caption("KikoGame")

    window = pygame.display.set_mode((WIDTH, HEIGHT))

    #pygame.display.set_icon(pygame.image.load("PICS/New Hero, Rocket/last planet.png").convert_alpha())
    # PORTED 
    icon = pygame.image.load("PICS/New Hero, Rocket/last planet.png")
    pygame.display.set_icon(icon)

    #CLOCK (FPS CONTROL)
    clock = pygame.time.Clock()
    # Clock helps  limit the game to a constant FPS (frames per second)
    # If  don't use it,  game might run too fast

    #CREATE MAIN GAME OBJECTS

    cosmos_picture_background = background.Background()
    # Background object that scrolls the space image

    rocket = Spaceship(window)
    # The rocket/player object.
    #  pass "window" because Spaceship draws itself onto this window in rocket.update().

    scores = Scores(window)
    # Handles health display, visited department counter,
    # win text, lose text, and restart button

    #CREATE SPRITE GROUPS

    asteroids = pygame.sprite.Group()       # Asteroids
    departments = pygame.sprite.Group()       # Departments
    keys = pygame.sprite.Group()    # Healing keys
    AIity = pygame.sprite.Group()       # Final planet

    # MENU SCREENS

    start_screen = StartScreen()
    # The first screen with Start button and Rules button

    rules_screen = RulesScreen()
    # The screen that shows rule images (slides)


    #STATE MACHINE, logic of the change between inputs
    state = "menu"
    # "state" to control what we draw and what input we accept.
    # "menu"  -> show start buttons
    # "rules" -> show rules slides
    # "game"  -> actual gameplay

    rules_completed = False
    # Start button should be disabled until user finished rules slides.
    # When rules are done,  set rules_completed = True.

    # QUIZ SETUP (FONTS + QUIZ OBJECT)

    #font_big = pygame.font.SysFont("Optima", 28)
    # Used for question titles and results header.

    #font_medium = pygame.font.SysFont("Optima", 26)
    # Used for question titles and results header.

    #font_small = pygame.font.SysFont("Optima", 22)
    # Used for answers and smaller text.
    # PORTED FONTS
    font_big = pygame.font.Font(None, 28)
    font_medium = pygame.font.Font(None, 26)
    font_small = pygame.font.Font(None, 22)



    test_screen = Quiz(font_big, font_medium, font_small)
    # Quiz overlay object.

    active_house = None
    # Stores the department sprite the player clicked.
    # after quiz finishes we must remove THIS department.
    #! Test
    music()
    # keep track of whether music is currently paused or not.
    # This prevents calling pause/unpause repeatedly each frame.
    music_paused_for_quiz = False

    # RESET GAME WORLD OBJECTS
    def reset_world():
        # This clears all moving objects and resets hero to start position.

        asteroids.empty()
        # Remove all asteroids from the game.

        departments.empty()
        # Remove all departments from the game.

        keys.empty()
        # Remove all keys from the game.

        AIity.empty()
        # Remove planet from the game.

        rocket.health = 3
        # Reset hero health to full.

        rocket.rect.center = (600, 400)
        # Move hero to the starting position

        rocket.hitbox.center = rocket.rect.center
        # Keep the hitbox aligned with the hero rectangle

        test_screen.close_quiz()
        # If quiz was open, close it

    #START = NEW SESSION (RESET EVERYTHING)
    def start_game_new_session():
        nonlocal active_house
        # nonlocal means: we want to modify the variable active_house from the outer run() function.

        reset_world()
        # Clear all objects and reset hero.

        scores.game = True
        # Game is running again.

        scores.game_over = False
        # Not in "game over" state.

        scores.to_planet = False
        # Not in planet phase yet.

        scores.reached_planet = False
        # Not reached planet yet.

        # NEW session means: reset progress completely.
        scores.completed_departments = set()
        # Remove all remembered completed departments.

        scores.total_correct_answers = 0
        # Reset total score across departments.

        active_house = None
        # No department currently active.

        Events.init_events()
        # Starts timers:
        # - first department appears after 10 seconds
        # - keys appear every 10 seconds


    # RESTART = CONTINUE PROGRESS (KEEP COMPLETED DEPARTMENTS)

    def restart_run_keep_departments():
        nonlocal active_house

        reset_world()
        # Clear asteroids, keys, planet, etc. and reset hero.

        scores.game = True
        # Game runs again.

        scores.game_over = False
        # Not game over anymore.

        scores.reached_planet = False
        # Planet not reached yet.

        # Restart keeps progress, so departments already completed are NOT repeated.
        scores.to_planet = (len(scores.completed_departments) >= len(Departments))
        # If all departments are already completed,  go directly into planet phase.

        active_house = None
        # Reset current department pointer.

        Events.init_events()
        # Restart timers again.

        # If we are already in planet phase:
        # - stop the department timer
        # - schedule the planet spawn
        if scores.to_planet:
            pygame.time.set_timer(Events.Department_fly_in, 0)  # stop department spawning
            pygame.time.set_timer(Events.AIity_fly_in, 0)      # clear possible old planet timer
            Events.schedule_planet_spawn()                     # spawn planet after delay

    # MAIN GAME LOOP (RUNS FOREVER)
    running = True
    while running:
        events = pygame.event.get()
        # Get all events

        # A) MENU / RULES INPUT
        for event in events:
            # Check global quit in every state.
            if event.type == pygame.QUIT:
                running = False



            # MENU STATE INPUT
            if state == "menu":
                # Handle mouse clicks on menu buttons.
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Ask start screen which button was clicked.
                    action = start_screen.handle_click(event.pos, start_allowed=rules_completed)

                    if action == "rules":
                        # Open rules slides and switch to rules state.
                        rules_screen.open()
                        state = "rules"

                    elif action == "start":
                        # Start is only possible after rules_completed == True.
                        start_game_new_session()
                        state = "game"


            # RULES STATE INPUT
            elif state == "rules":
                # Only mouse click is relevant here
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    r = rules_screen.handle_click(event.pos)
                    # handle_click returns "done" when slides finished.

                    if r == "done":
                        # Unlock start button
                        rules_completed = True
                        # Return to menu
                        state = "menu"

        # B) GAME EVENTS (ONLY IF STATE == "game")
        if state == "game":
            #  Events.py process gameplay events:
            # - spawn departments/keys
            # - pause
            # - quiz clicks
            # - restart click
            status, active_house = Events.handle_events(
                events, window, clock, departments, keys, scores, test_screen, active_house, AIity
            )

            # If Events tells us to quit, exit run()
            if status == "quit":
                running = False

            # If Events tells us restart clicked, restart but keep departments
            if status == "restart":
                restart_run_keep_departments()

        # C) MUSIC CONTROL DURING QUIZ

        # music to stop while answering questions
        # So pause music when quiz becomes active,
        # and unpause it when quiz closes again.

        if state == "game" and test_screen.quiz_active and not music_paused_for_quiz:
            pygame.mixer.music.pause()
            # Pause the currently playing background music.
            music_paused_for_quiz = True
            # Remember that we paused it, so we don't pause again every frame.

        if (state != "game" or not test_screen.quiz_active) and music_paused_for_quiz:
            pygame.mixer.music.unpause()
            # Resume music when quiz is not active.
            music_paused_for_quiz = False

        # D) DRAW EVERYTHING
        if state == "menu":
            # Draw moving background behind the menu for a nice effect
            cosmos_picture_background.update()
            cosmos_picture_background.render(window)

            # Draw menu buttons
            start_screen.draw(window, start_allowed=rules_completed)

        elif state == "rules":
            # Show rules slides
            rules_screen.draw(window)

        elif state == "game":
            # Always draw background first
            cosmos_picture_background.update()
            cosmos_picture_background.render(window)

            # Only move departments while the game is running
            if scores.game:
                departments.update()

            # Drawing is OK even when game is over (it just shows where they are)
            departments.draw(window)



            # GAME is STILL RUNNING
            if scores.game:
                # If quiz is open, freeze gameplay (no asteroid damage)
                if test_screen.quiz_active:
                    # Only show UI and quiz
                    scores.show_health(rocket)
                    scores.visited_departments()
                    test_screen.draw(window)

                else:
                    # Normal gameplay logic
                    rocket.update()
                    Events.make_comet(asteroids, window)
                    Events.move_key(window, keys)
                    Events.collide(rocket, asteroids, keys)

                    # Planet phase objects
                    AIity.update()
                    AIity.draw(window)

                    # Check if hero reached planet
                    Events.collide_with_planet(rocket, AIity, scores)

                    # UI and quiz (quiz not active now, but still safe)
                    scores.show_health(rocket)
                    scores.visited_departments()
                    scores.finish(rocket)
                    test_screen.draw(window)


            # GAME OVER OR WIN SCREEN
            else:
                # Even when game ended, planet might still be visible
                AIity.update()
                AIity.draw(window)

                # Draw score texts and restart button
                scores.show_health(rocket)
                scores.visited_departments()
                scores.finish(rocket)
                scores.draw_restart_button()

        # E) FINAL DISPLAY UPDATE + FPS LIMIT
        pygame.display.flip()
        # Show everything we drew this frame.

        clock.tick(60)
        # Limit the loop to ~60 frames per second.
        await asyncio.sleep(0)
    pygame.quit()


# start the game
if __name__ == '__main__':
    asyncio.run(run())
