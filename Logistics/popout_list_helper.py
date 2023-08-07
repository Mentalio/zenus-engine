import pygame

pygame.init()


def rect(position_x, position_y, width, height):
    position_x = position_x - width / 2
    position_y = position_y - height / 2
    Rectangle = pygame.rect.Rect(position_x, position_y, width, height)
    return Rectangle


class popout_list:
    clicked = False
    last_click_time = 0
    position = [0, 0]

    def __init__(self, rectangle: pygame.rect.Rect, font: pygame.font.Font, img: pygame.surface.Surface, input_text: str, items: list):
        """
        Sets all the base parameters to what you input
        So you don't have to manually input parameters
        If there's something I missed go make a branch
        """
        self.items = items
        self.text = input_text
        self.font = font
        self.rect = rectangle
        self.image = pygame.transform.scale(img, [self.get_rect()[2], self.get_rect()[3]])
        self.position[0] = self.get_rect()[0] + self.get_rect()[2] / 2
        self.position[1] = self.get_rect()[1] + self.get_rect()[3] / 2

    def get_rect(self):
        """
        Seriously what did you expect this to do?
        """
        return self.rect

    def check_clicked_alone(self):
        """
        Same as check clicked merged but the event is auto
        Only here for specific cases
        """
        mouse = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if mouse_clicked[0]:
            if self.rect.collidepoint(mouse):
                current_time = pygame.time.get_ticks()
                if current_time - self.last_click_time > 500:
                    self.clicked = not self.clicked
                    self.last_click_time = current_time

    def check_clicked_merged(self, mouse_pos: tuple, mouse_clicked):
        """
        Same as check clicked alone, but you have to input the event manually
        This can shave of the operations of getting the mouse
        """
        if mouse_clicked[0]:
            if self.rect.collidepoint(mouse_pos):
                self.clicked = True
            else:
                self.clicked = False

    def draw(self, surface: pygame.surface.Surface):
        """
        This is where the fun begins
        Draws it depending on the __init__ inputs
        """
        text_render = self.font.render(self.text, True, (255, 255, 255))
        if text_render.get_rect()[2] > self.get_rect()[2]:
            self.text = self.text[:-1]
        surface.blit(self.image, [self.get_rect()[0], self.get_rect()[1]])
        surface.blit(text_render, [self.get_rect()[0] - text_render.get_rect()[2] / 2 + self.get_rect()[2] / 2,
                                   self.get_rect()[1] - text_render.get_rect()[3] / 2 + self.get_rect()[3] / 2])
        if self.clicked:
            item_height = 0
            item_offset = self.get_rect()[3] - 30
            for item in self.items:
                item_render = self.font.render(item, True, (255, 255, 255))
                item_height += item_offset
                surface.blit(item_render, [self.position[0] - item_render.get_width() / 2, self.position[1] + item_height])
            item_height = 0

    def update(self, surface: pygame.surface.Surface):
        self.check_clicked_alone()
        self.draw(surface)

