import sys
import pygame
import generalOptions


class Button:
    def __init__(self, text, pos, size, font, callback):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.font = font
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = (170, 170, 170) if self.hovered else (50, 50, 50)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                self.callback()

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.buttons = []

        self.create_buttons()

    def create_buttons(self):
        # Теперь кнопки слева: x = 100
        # start_button = Button("Новая игра", (100, 200), (250, 70), self.font, self.start_new_game)
        continue_button = Button("Продолжить", (100, 300), (250, 70), self.font, self.continue_game)
        exit_button = Button("Выйти", (100, 400), (250, 70), self.font, self.exit_game)

        self.buttons.extend([continue_button, exit_button])

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self.running = True  # Для выхода из меню через кнопку

        while self.running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for button in self.buttons:
                    button.handle_event(event)

            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(generalOptions.FPS)

    def start_new_game(self):
        generalOptions.menu_flag = False
        self.running = False

    def continue_game(self):
        generalOptions.menu_flag = False
        self.running = False

    def exit_game(self):
        pygame.quit()
        sys.exit()