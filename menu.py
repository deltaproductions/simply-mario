import sys
import pygame_gui
import sqlite3
import pygame

from config import W, H, FPS, DATABASE
from database import *

db = Database(DATABASE)


def window_records():
    screen = pygame.display.set_mode((W, H))
    manager = pygame_gui.UIManager((W, H), 'theme.json')
    title_font = pygame.font.Font("data/font/font.ttf", 42)
    text_font = pygame.font.Font("data/font/font.ttf", 30)

    level_1 = title_font.render("level 1", True, (255, 255, 0))
    min_1 = text_font.render("min", True, (225, 225, 225))
    max_1 = text_font.render("max", True, (225, 225, 225))
    avg_1 = text_font.render("avg", True, (225, 225, 225))

    db_scores = db.get_scores(1)
    level_1_scores = [0] if not(db_scores) else db_scores
    min_value_1 = text_font.render(str(min(level_1_scores)), True, (255, 255, 255))
    max_value_1 = text_font.render(str(max(level_1_scores)), True, (255, 255, 255))
    avg_value_1 = text_font.render(str(sum(level_1_scores) // len(level_1_scores)), True, (255, 255, 255))

    level_2 = title_font.render("level 2", True, (255, 255, 0))
    min_2 = text_font.render("min", True, (225, 225, 225))
    max_2 = text_font.render("max", True, (225, 225, 225))
    avg_2 = text_font.render("avg", True, (225, 225, 225))

    db_scores = db.get_scores(2)
    level_2_scores = [0] if not(db_scores) else db_scores
    min_value_2 = text_font.render(str(min(level_2_scores)), True, (255, 255, 255))
    max_value_2 = text_font.render(str(max(level_2_scores)), True, (255, 255, 255))
    avg_value_2 = text_font.render(str(sum(level_2_scores) // len(level_2_scores)), True, (255, 255, 255))

    clock = pygame.time.Clock()
    running = True
    image = pygame.image.load('data/sprites/records.png')
    button_cancel = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1040, 600), (190, 50)),
                                                 text='Back',
                                                 manager=manager)

    while running:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_cancel:
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(image, (0, 0))
        screen.blit(level_1, (604, 196))
        screen.blit(min_1, (604, 250))
        screen.blit(max_1, (804, 250))
        screen.blit(avg_1, (1004, 250))
        screen.blit(min_value_1, (704, 250))
        screen.blit(max_value_1, (904, 250))
        screen.blit(avg_value_1, (1104, 250))

        screen.blit(level_2, (604, 356))
        screen.blit(min_2, (604, 410))
        screen.blit(max_2, (804, 410))
        screen.blit(avg_2, (1004, 410))
        screen.blit(min_value_2, (704, 410))
        screen.blit(max_value_2, (904, 410))
        screen.blit(avg_value_2, (1104, 410))
        manager.draw_ui(screen)
        pygame.display.flip()


def window_help():
    """окно с инструкцией"""
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((W, H), 'theme.json')
    running = True
    button_cancel = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1040, 600), (190, 50)), text='Back',
                                                 manager=manager)
    image = pygame.image.load('data/sprites/help.png')
    screen.blit(image, (0, 0))

    while running:
        time_delta = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_cancel:
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(image, (0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()


class Menu:
    """класс главного меню"""

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load('data/sounds/soundtrack.mp3')
        pygame.mixer.music.play(-1)

        self.display = db.get_plot_value()

        self.screen = pygame.display.set_mode((W, H))
        self.background = pygame.Surface((W, H))
        self.manager = pygame_gui.UIManager((W, H), 'theme.json')
        self.button_start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 200), (170, 60)), text='Start',
                                                         manager=self.manager)
        self.button_records = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((770, 270), (230, 60)),
                                                           text='Records',
                                                           manager=self.manager)
        self.button_help = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((810, 340), (140, 60)), text='Help',
                                                        manager=self.manager)
        self.button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((810, 410), (150, 60)), text='Quit',
                                                        manager=self.manager)

    def menu(self, game_plot, game_runner):
        """главное меню"""
        # print(self.display)
        clock = pygame.time.Clock()
        image = pygame.image.load('data/sprites/background.png')

        running = True

        while running:
            time_delta = clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_start:
                        if self.display == 0:
                            db.set_plot_value()
                            game_plot()

                        if self.display == 1:
                            game_runner()

                    if event.ui_element == self.button_quit:
                        running = False

                    if event.ui_element == self.button_records:
                        window_records()

                    if event.ui_element == self.button_help:
                        window_help()

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.screen.blit(image, (0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
