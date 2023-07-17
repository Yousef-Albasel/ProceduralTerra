import pygame
import sys
import options
from generic import *
import Camera
import pygame_gui

pygame.init()
SCREEN_WIDTH = options.width
SCREEN_HEIGHT = options.height
pygame.display.set_caption("ProceduralTerra")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
MANAGER = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')
seed = 0
pres = 0.5
lacunarity = 2
scale = 50
octaves = 6

settings_text = pygame.font.Font("monogram.ttf", 22).render("Settings press P", False, "white")
settings_rect = settings_text.get_rect(topleft=(20, 20))
show_commit_message = False

Commit_Changes_font = pygame.font.Font("monogram.ttf", 30)

def ChangesCommited(pos, message):
    Commit_Changes = Commit_Changes_font.render(message, False, "#028A0F")
    Commit_rect = Commit_Changes.get_rect(center=pos)
    screen.blit(Commit_Changes, Commit_rect)

def show_error_message(pos, message):
    Error_Message = Commit_Changes_font.render(message, False, "Red")
    Error_rect = Error_Message.get_rect(center=pos)
    screen.blit(Error_Message, Error_rect)

# Create the UITextEntryLine elements
seed_input_rect = pygame.Rect((100, 250), (250, 50))
octaves_input_rect = pygame.Rect((100, 370), (250, 50))
lacunarity_input_rect = pygame.Rect((100, 490), (250, 50))
pres_input_rect = pygame.Rect((100, 620), (250, 50))
scale_input_rect = pygame.Rect((780, 250), (250, 50))
type_input_rect = pygame.Rect((780, 380), (250, 50))
submit_rect = pygame.Rect((780, 460), (100, 50))

seed_input = pygame_gui.elements.UITextEntryLine(relative_rect=seed_input_rect, manager=MANAGER, object_id="#seed",
                                                 placeholder_text="Enter Seed: ")
lacunarity_input = pygame_gui.elements.UITextEntryLine(relative_rect=lacunarity_input_rect, manager=MANAGER,
                                                      object_id="#lacunarity",
                                                      placeholder_text="Enter FP Number:eg(2.0)")
pres_input = pygame_gui.elements.UITextEntryLine(relative_rect=pres_input_rect, manager=MANAGER, object_id="#pres",
                                                 placeholder_text="Enter FP Number:eg(0.5) ")
scale_input = pygame_gui.elements.UITextEntryLine(relative_rect=scale_input_rect, manager=MANAGER, object_id="#scale")
octaves_input = pygame_gui.elements.UITextEntryLine(relative_rect=octaves_input_rect, manager=MANAGER,
                                                   object_id="#octaves",
                                                   placeholder_text="Enter Number of octaves eg(5): ")
Text_input = pygame_gui.elements.UITextEntryLine(relative_rect=type_input_rect, manager=MANAGER, object_id="#type",
                                                placeholder_text="Enter 'Islands' or 'Terrain': ")
submit_button = pygame_gui.elements.UIButton(submit_rect, text="Generate", manager=MANAGER, object_id="#submit")

# UI elements' positions
seed_input_pos = (300, 270-40)
octaves_input_pos = (300, 390-30)
lacunarity_input_pos = (300, 505-30)
pres_input_pos = (300, 635-30)
scale_input_pos = (780 + 200, 270-40)
type_input_pos = (780 + 200, 405-40)
submit_button_pos = (830, 485-50)

info_on = True
info_surface = pygame.image.load('info.png')
info_alpha = 0
fade_duration = 30
current_frame = 0

settings_on = False
settings_surface = pygame.image.load('settings.png')
settings_alpha = 0
fade_duration_st = 0.5
current_frame_st = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                info_on = False
                current_frame = 0
            if event.key == pygame.K_p:
                settings_on = not settings_on
                current_frame_st = 0

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#seed":
            try:
                seed = int(event.text)
                if seed > 1e4:
                    raise ValueError("Seed value should be less than or equal to 1e4.")
                commit_massege_pos = seed_input_pos
                show_commit_message = True
                commit_message_duration = 60
                commit_message = "Seed value changed to: {}".format(seed)
            except ValueError as e:
                show_error_message(seed_input_pos, str(e))

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#pres":
            try:
                pres = float(event.text)
                if pres > 1e4:
                    raise ValueError("Pres value should be less than or equal to 1e4.")
                commit_massege_pos = pres_input_pos
                show_commit_message = True
                commit_message_duration = 60
                commit_message = "Pres value changed to: {}".format(pres)
            except ValueError as e:
                show_error_message(pres_input_pos, str(e))

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#scale":
            try:
                scale = int(event.text)
                if scale > 1e4:
                    raise ValueError("Scale value should be less than or equal to 1e4.")
                commit_massege_pos = scale_input_pos
                show_commit_message = True
                commit_message_duration = 60
                commit_message = "Scale value changed to: {}".format(scale)
            except ValueError as e:
                show_error_message(scale_input_pos, str(e))

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#octaves":
            try:
                octaves = int(event.text)
                if octaves > 1e4:
                    raise ValueError("Octaves value should be less than or equal to 1e4.")
                commit_massege_pos = octaves_input_pos
                show_commit_message = True
                commit_message_duration = 60
                commit_message = "Octaves value changed to: {}".format(octaves)
            except ValueError as e:
                show_error_message(octaves_input_pos, str(e))

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#type":
            type = event.text
            commit_massege_pos = type_input_pos
            show_commit_message = True
            commit_message_duration = 60
            commit_message = "Type value changed to: {}".format(type)

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#lacunarity":
            try:
                lacunarity = float(event.text)
                if lacunarity > 1e4:
                    raise ValueError("Lacunarity value should be less than or equal to 1e4.")
                commit_massege_pos = lacunarity_input_pos
                show_commit_message = True
                commit_message_duration = 60
                commit_message = "Lacunarity value changed to: {}".format(lacunarity)
            except ValueError as e:
                show_error_message(lacunarity_input_pos, str(e))

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#submit":
            try:
                map_surface = DisplayMap(GeneratePerlinMap(seed, scale, octaves, pres, lacunarity))
                commit_massege_pos = submit_button_pos
                show_commit_message = True
                commit_message_duration = 60
                commit_message = "Map generated!"
            except Exception as e:
                show_error_message(submit_button_pos, str(e))

        MANAGER.process_events(event)

    # GUI loop: Update and draw GUI components
    MANAGER.update(clock.tick(60) / 1000)
    screen.fill("white")

    Camera.input()
    Camera.camera_move()
    if type == 'Islands':
        selected_map = island_surface
    else:
        selected_map = map_surface
    Camera.camera_surface.blit(selected_map, (0, 0), (Camera.camera_x, Camera.camera_y, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(pygame.transform.scale(Camera.camera_surface, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    if info_on:
        if current_frame < fade_duration:
            info_alpha = int((current_frame / fade_duration) * 255)
        elif current_frame >= fade_duration:
            info_alpha = 255
        current_frame += 50
        info_surface.set_alpha(info_alpha)
    else:
        if info_alpha >= 0:
            info_alpha -= 50
            info_surface.set_alpha(info_alpha)

    if info_alpha > 0:
        screen.blit(info_surface, (0, 0))

    if settings_on:
        if current_frame_st < fade_duration_st:
            settings_alpha = int((current_frame_st / fade_duration_st) * 255)
        elif current_frame_st >= fade_duration_st:
            settings_alpha = 255
        current_frame_st += 50
        settings_surface.set_alpha(settings_alpha)
    else:
        if settings_alpha >= 0:
            settings_alpha -= 50
            settings_surface.set_alpha(settings_alpha)

    if settings_alpha > 0:
        screen.blit(settings_surface, (0, 0))
        MANAGER.draw_ui(screen)

    screen.blit(settings_text, settings_rect)

    if show_commit_message:
        if commit_message_duration > 0:
            ChangesCommited(commit_massege_pos, commit_message)
            commit_message_duration -= 1
        else:
            show_commit_message = False
            commit_message_duration = 60

    pygame.display.flip()
    clock.tick(60)
