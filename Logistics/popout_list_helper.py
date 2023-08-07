import pygame

pygame.init()


def rect(position_x, position_y, width, height):
    position_x = position_x - width / 2
    position_y = position_y - height / 2
    Rectangle = pygame.rect.Rect(position_x, position_y, width, height)
    return Rectangle


class textbox:
    writeable = True
    text = ""
    clicked = False
    entered = False

    def __init__(self, rectangle: pygame.rect.Rect, font: pygame.font.Font, img: pygame.surface.Surface, caption: str):
        """
        Sets all the base parameters to what you input
        So you don't have to manually input parameters
        If there's something I missed go make a branch
        """
        self.caption = caption
        self.font = font
        self.rect = rectangle
        self.image = pygame.transform.scale(img, [self.get_rect()[2], self.get_rect()[3]])

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
                self.clicked = True
            else:
                self.clicked = False

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
        caption_render = self.font.render(self.caption, True, (255, 255, 255))
        if text_render.get_rect()[2] > self.get_rect()[2]:
            self.text = self.text[:-1]
        surface.blit(self.image, [self.get_rect()[0], self.get_rect()[1]])
        surface.blit(text_render, [self.get_rect()[0] - text_render.get_rect()[2] / 2 + self.get_rect()[2] / 2,
                                   self.get_rect()[1] - text_render.get_rect()[3] / 2 + self.get_rect()[3] / 2])
        surface.blit(caption_render, [self.get_rect()[0] - caption_render.get_rect()[2] / 2 + self.get_rect()[2] / 2,
                                      self.get_rect()[1] - caption_render.get_rect()[3] / 2 + self.get_rect()[3] / 2 - 100])

    def get_entered(self):
        return self.entered

    def update(self, surface: pygame.surface.Surface):
        self.check_clicked_alone()
        self.draw(surface)
