import pygame
import generalOptions


class Walls(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()  # Получаем прямоугольник для объектов
        self.rect.center = (x, y)  # Размещаем объект

    def update(self, x_to_right, x_to_left, y_to_up, y_to_down):
        self.rect.x -= x_to_right
        self.rect.x += x_to_left

        self.rect.y += y_to_up
        self.rect.y -= y_to_down

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def give_coordinations_wall(self):
        return [(self.rect.x - 25, self.rect.y - 25), (self.rect.x + 25, self.rect.y + 25), (self.rect.x + 25, self.rect.y - 25), (self.rect.x - 25, self.rect.y + 25)]

    def give_centre(self):
        return [self.rect.x, self.rect.y]

    def give_rect(self):
        return self.rect

    def collision(self, creature_x, creature_y, creature_rect, screen, radius_creature=8):
        if self.rect.colliderect(creature_rect):
            self.image_r = pygame.Surface((5, 40))
            self.rect_r = self.image_r.get_rect()  # Получаем прямоугольник для объектов
            self.rect_r.center = (self.rect.x + 47, self.rect.y + 27)  # Размещаем объект
            if self.rect_r.colliderect(creature_rect):
                self.image_r.fill((255, 0, 0))
                # screen.blit(self.image_r, self.rect_r)

                generalOptions.x_to_left = 0

            self.image_l = pygame.Surface((5, 40))
            self.rect_l = self.image_l.get_rect()  # Получаем прямоугольник для объектов
            self.rect_l.center = (self.rect.x, self.rect.y + 27)  # Размещаем объект
            if self.rect_l.colliderect(creature_rect):
                self.image_l.fill((255, 0, 0))
                # screen.blit(self.image_l, self.rect_l)

                generalOptions.x_to_right = 0

            self.image_u = pygame.Surface((40, 5))
            self.rect_u = self.image_u.get_rect()  # Получаем прямоугольник для объектов
            self.rect_u.center = (self.rect.x + 27, self.rect.y)  # Размещаем объект
            if self.rect_u.colliderect(creature_rect):
                self.image_u.fill((255, 0, 0))
                # screen.blit(self.image_u, self.rect_u)

                generalOptions.y_to_down = 0

            self.image_d = pygame.Surface((40, 5))
            self.rect_d = self.image_d.get_rect()  # Получаем прямоугольник для объектов
            self.rect_d.center = (self.rect.x + 27, self.rect.y + 50)  # Размещаем объект
            if self.rect_d.colliderect(creature_rect):
                self.image_d.fill((255, 0, 0))
                # screen.blit(self.image_d, self.rect_d)

                generalOptions.y_to_up = 0








    # def collision(self, creature_x, creature_y, creature_rect, screen, radius_creature=8):
    #     if self.rect.colliderect(creature_rect):
    #         self.image_r = pygame.Surface((2, 50))
    #         self.rect_r = self.image_r.get_rect()  # Получаем прямоугольник для объектов
    #         self.rect_r.center = (self.rect.x + 47, self.rect.y + 27)  # Размещаем объект
    #         if self.rect_r.colliderect(creature_rect):
    #             self.image_r.fill((0, 255, 0))
    #             screen.blit(self.image_r, self.rect_r)
    #
    #             generalOptions.x_to_left = 0
    #
    #         self.image_l = pygame.Surface((2, 50))
    #         self.rect_l = self.image_l.get_rect()  # Получаем прямоугольник для объектов
    #         self.rect_l.center = (self.rect.x, self.rect.y + 27)  # Размещаем объект
    #         if self.rect_l.colliderect(creature_rect):
    #             self.image_l.fill((0, 255, 0))
    #             screen.blit(self.image_l, self.rect_l)
    #
    #             generalOptions.x_to_right = 0
    #
    #         self.image_u = pygame.Surface((50, 2))
    #         self.rect_u = self.image_u.get_rect()  # Получаем прямоугольник для объектов
    #         self.rect_u.center = (self.rect.x + 27, self.rect.y)  # Размещаем объект
    #         if self.rect_u.colliderect(creature_rect):
    #             self.image_u.fill((0, 255, 0))
    #             screen.blit(self.image_u, self.rect_u)
    #
    #             generalOptions.y_to_down = 0
    #
    #         self.image_d = pygame.Surface((50, 2))
    #         self.rect_d = self.image_d.get_rect()  # Получаем прямоугольник для объектов
    #         self.rect_d.center = (self.rect.x + 27, self.rect.y + 50)  # Размещаем объект
    #         if self.rect_d.colliderect(creature_rect):
    #             self.image_d.fill((0, 255, 0))
    #             screen.blit(self.image_d, self.rect_d)
    #
    #             generalOptions.y_to_up = 0
