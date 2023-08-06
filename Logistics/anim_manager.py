import pygame

animation_list = []


# noinspection PyBroadException


class animation:
    images = []
    current_image = pygame.surface.Surface([0, 0])
    current_image_pos = 0
    ticks = 0

    def __init__(self, image_phrase: str, tick_time: int):
        """
        Takes in a phrase for your images
        Starts with 1, tiles infinitely
        insert where you want your number to be with %
        example: files:(p_1,p_2,p_3) phrase:(p_%)
        example: files:(p_1_fr,p_2_fr,p_3_fr) phrase:(p_%_fr)

        Tick time:
        Tick time is the amount of times you need to activate the animate() function to play a frame
        example: tick-time:(10), activate 10 times to get to next frame
        """

        self.tick_time = tick_time
        animation_list.append(self)

        loop_time = 0
        anim_cycle = True
        while anim_cycle:
            loop_time += 1
            anim_name = image_phrase.replace("%", str(loop_time))
            anim_name += '.png'
            try:
                img = pygame.image.load(anim_name)
                self.images.append(img)
            except:
                anim_cycle = False

    def inch(self, inch_amount: int):
        """
        Moves the current image forward in the list
        """

        self.current_image_pos += inch_amount
        if self.current_image_pos > len(self.images) - 1:
            self.current_image_pos -= len(self.images)
        if self.current_image_pos < 0:
            self.current_image_pos = len(self.images)

    def draw(self, surface: pygame.surface.Surface, position: list, width: int, height: int, *centre: bool):
        if not centre:
            img = self.images[self.current_image_pos]
            img = pygame.transform.scale(img, [width, height])
            surface.blit(img, position)
        else:
            img = self.images[self.current_image_pos]
            img = pygame.transform.scale(img, [width, height])
            selected_pos = [position[0], position[1]]
            selected_pos[0] -= width / 2
            selected_pos[1] -= height / 2
            surface.blit(img, selected_pos)

    def animate(self):
        """
        'Animates' the image by moving its internal ticks forward
        When it hits the tick_time, inch
        """
        self.ticks += 1
        if not self.ticks % self.tick_time:
            self.inch(1)
        self.ticks %= self.tick_time
