import pygame
from random import randint

# ---------------------------------------------------------
# IMPORT GAME OBJECTS
# ---------------------------------------------------------

# Asteroids that damage the hero
from enemy import Komets

# Floating department buildings
from Depart import Border

# Sound effects
from sound import click_on_depart, hit_cometa, heal_rocket

# Health keys that restore HP
from key import Key

# All department definitions (questions, images, IDs)
from departments_data import Departments

# Final planet AIity
from planet import Planet


# ---------------------------------------------------------
# CUSTOM EVENTS & TIMERS
# ---------------------------------------------------------
# pygame.USEREVENT is the first free ID for custom events.
# We add +2, +3, +4 so each event is unique.

Key_fly_in = pygame.USEREVENT + 2          # spawn health keys
Department_fly_in = pygame.USEREVENT + 3   # spawn departments
AIity_fly_in = pygame.USEREVENT + 4       # spawn final planet

# Time values are in milliseconds
Key_between_time_distance = 9_000
Departments_between_time_distance = 12_000       # 12 seconds between departments
AIity_delay = 3_000       # short pause before planet appears

# Total number of departments (so we don’t hardcode "5")
Total_departments = len(Departments)


# ---------------------------------------------------------
# INITIALIZE GAME TIMERS
# ---------------------------------------------------------
def init_events():
    # This function starts the timers used in the game.
    # It is called when:
    # - the game starts
    # - the game restarts

    # Every 10 seconds → spawn a health key
    pygame.time.set_timer(Key_fly_in, Key_between_time_distance)

    # After 10 seconds → spawn the first department
    # loops=1 means it triggers ONLY once
    pygame.time.set_timer(Department_fly_in, Departments_between_time_distance, loops=1)


# ---------------------------------------------------------
# TIMER CONTROL (IMPORTANT FOR QUIZ LOGIC)
# ---------------------------------------------------------
def pause_timers():
    # This function stops ALL timers.
    # We use it when:
    # - a quiz opens
    # - the player loses
    #
    # Why?
    # Because otherwise timer events keep piling up in the background.

    pygame.time.set_timer(Key_fly_in, 0)
    pygame.time.set_timer(Department_fly_in, 0)
    pygame.time.set_timer(AIity_fly_in, 0)

    # Remove already-queued timer events from the event queue
    pygame.event.clear([Key_fly_in, Department_fly_in, AIity_fly_in])


def resume_after_quiz(scores):
    # This function resumes timers AFTER a quiz is finished.

    # Restart health key timer
    pygame.time.set_timer(Key_fly_in, 10_000)

    # Only restart department timer if we are NOT in planet phase
    if not scores.to_planet:
        pygame.time.set_timer(Department_fly_in, Departments_between_time_distance, loops=1)


# ---------------------------------------------------------
# HEALTH KEYS
# ---------------------------------------------------------
def spawn_key_if_needed(event, group_keys):
    # This function checks:
    # "Is the current event the Key_fly_in?"

    if event.type == Key_fly_in:
        # If yes → create a new Key object
        # and add it to the sprite group
        group_keys.add(Key())


# ---------------------------------------------------------
# DEPARTMENT SPAWNING
# ---------------------------------------------------------
def fly_in_next_department(objects, scores):
    # This function spawns ONE department at a time.

    # First: check if a department is still on screen
    for dept in objects:
        if not dept.fly_out:
            # A department is still active → do nothing
            return

    # If no department is blocking the screen,
    # find the next department that was NOT completed
    for d in Departments:
        if d["id"] not in scores.completed_departments:

            # Create a Border (department)
            objects.add(
                Border(
                    stop_x=d["stop_x"],
                    image_path=d["image"],
                    dept_id=d["id"],
                    title=d["title"],
                    y=d["y"]
                )
            )

            # Spawn ONLY ONE department
            return


# ---------------------------------------------------------
# CLICK HELPERS
# ---------------------------------------------------------
def clicked_department(pos, objects):
    # Checks if the player clicked on a department

    for dept in objects:
        if dept.rect.collidepoint(pos):
            # Play click sound
            click_on_depart()
            return dept

    return None


def find_dept_data(dept_id):
    # Finds department info (questions, title) by ID

    for d in Departments:
        if d["id"] == dept_id:
            return d

    return None


# ---------------------------------------------------------
# PLANET SPAWNING
# ---------------------------------------------------------
def schedule_planet_spawn():
    # Schedules the final planet to appear after a short delay
    pygame.time.set_timer(AIity_fly_in, AIity_delay, loops=1)


def spawn_planet_if_needed(event, planets, scores):
    # Conditions for planet spawn:
    # 1. Planet timer fired
    # 2. We are in planet phase
    # 3. No planet exists yet

    if event.type == AIity_fly_in and scores.to_planet and len(planets) == 0:
        planets.add(Planet())


def collide_with_planet(hero, planets, scores):
    # Checks if hero collides with the final planet

    if not scores.to_planet:
        return False

    for p in planets:
        if hero.hitbox.colliderect(p.hitbox):
            scores.reached_planet = True
            p.kill()
            return True

    return False


# ---------------------------------------------------------
# PAUSE SYSTEM
# ---------------------------------------------------------
def do_pause(window, clock):
    # Freezes the game until SPACE is pressed again

    pause = True
    font = pygame.font.SysFont("Optima", 50)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = False

        # Dark overlay
        overlay = pygame.Surface(window.get_size())
        overlay.set_alpha(150)
        overlay.fill((39, 44, 78))
        window.blit(overlay, (0, 0))

        pause_text = font.render(
            "Pause! Press SPACE to continue", True, "white"
        )
        window.blit(
            pause_text,
            pause_text.get_rect(
                center=(window.get_width() // 2, window.get_height() // 2)
            )
        )

        pygame.display.update()
        clock.tick(30)

    return "resume"


# ---------------------------------------------------------
# MAIN EVENT HANDLER (GAME HEART)
# ---------------------------------------------------------
def handle_events(events, window, clock,
                  objects, group_keys, scores,
                  test_screen, active_house, planets):

    # This function handles:
    # - mouse clicks
    # - keyboard input
    # - timers
    # - pause
    # - restart
    #
    # It is called ONCE PER FRAME from main.py

    for event in events:

        # Quit game
        if event.type == pygame.QUIT:
            return "quit", active_house

        # If game over → stop everything
        if scores.game_over:
            pause_timers()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if scores.restart_clicked(event.pos):
                    return "restart", active_house

            continue  # ignore all other events

        # Spawn timers only if quiz is NOT active
        if not test_screen.quiz_active:
            spawn_key_if_needed(event, group_keys)

            if event.type == Department_fly_in and not scores.to_planet:
                fly_in_next_department(objects, scores)

            spawn_planet_if_needed(event, planets, scores)

        # Pause key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if do_pause(window, clock) == "quit":
                return "quit", active_house

        # Mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Quiz active → quiz handles input
            if test_screen.quiz_active:
                result = test_screen.handle_click(event.pos)

                if result == "finished" and active_house:
                    scores.add_department_score(test_screen.get_score())
                    scores.completed_departments.add(active_house.dept_id)

                    active_house.start_fly_out()
                    active_house = None

                    # Resume timers safely
                    resume_after_quiz(scores)

                    if len(scores.completed_departments) >= Total_departments:
                        scores.to_planet = True
                        pygame.time.set_timer(Department_fly_in, 0)
                        schedule_planet_spawn()

            # Quiz not active → open department
            else:
                if not scores.to_planet:
                    dept_sprite = clicked_department(event.pos, objects)
                    if dept_sprite:
                        dept_data = find_dept_data(dept_sprite.dept_id)
                        if dept_data:
                            active_house = dept_sprite
                            pause_timers()
                            test_screen.open_quiz(dept_data)

    return "continue", active_house


# ---------------------------------------------------------
# ASTEROIDS
# ---------------------------------------------------------
def make_comet(enemies, window):
    enemies.update()
    enemies.draw(window)
    if len(enemies) < 3:
        enemies.add(Komets(randint(4, 6)))


# ---------------------------------------------------------
# COLLISIONS
# ---------------------------------------------------------
def collide(hero, enemies, group_keys):
    for comet in enemies:
        if hero.hitbox.colliderect(comet.hitbox):
            hit_cometa()
            comet.kill()
            hero.health -= 1

    if pygame.sprite.spritecollide(hero, group_keys, True):
        if hero.health < 3:
            hero.health += 1
            heal_rocket()


def move_key(window, group_keys):
    group_keys.update()
    group_keys.draw(window)
