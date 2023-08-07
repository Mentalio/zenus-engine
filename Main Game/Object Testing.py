import pygame
import warnings
import json
import sys
import os

sys.path.append(os.path.abspath('..'))
directory_path = 'Levels'
levels = os.listdir(directory_path)

from Logistics import tbh
from Logistics import popout_list_helper

info = pygame.display.Info()

display_width = 2000
display_height = 1200

screen = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 3072)
pygame.mixer.init()
running = True

fps = pygame.time.Clock()
tick = 160
hitboxes = []
camera_influencers = []
font = pygame.font.Font("Types/Handjet-Regular.ttf", 32)
font_lrg = pygame.font.Font("Types/Handjet-Regular.ttf", 64)

pygame.mixer.music.load("Audio/menu.mp3")
pygame.mixer.music.set_volume(0.7)

walking_sound = pygame.mixer.Sound("Audio/walk_sfx.mp3")
walking_sound.set_volume(0.0)
walking_sound_cooldown = 0

level_images = {
    1: pygame.image.load("Images/wall1.png"),
    2: pygame.image.load("Images/wall2.png"),
    3: pygame.image.load("Images/wall3.png")
}

key_mapping = {
    'a': pygame.K_a,
    'b': pygame.K_b,
    'c': pygame.K_c,
    'd': pygame.K_d,
    'e': pygame.K_e,
    'f': pygame.K_f,
    'g': pygame.K_g,
    'h': pygame.K_h,
    'i': pygame.K_i,
    'j': pygame.K_j,
    'k': pygame.K_k,
    'l': pygame.K_l,
    'm': pygame.K_m,
    'n': pygame.K_n,
    'o': pygame.K_o,
    'p': pygame.K_p,
    'q': pygame.K_q,
    'r': pygame.K_r,
    's': pygame.K_s,
    't': pygame.K_t,
    'u': pygame.K_u,
    ## sorry v is reserved for down arrow :(
    'v': pygame.K_DOWN,
    ##
    'w': pygame.K_w,
    'x': pygame.K_x,
    'y': pygame.K_y,
    'z': pygame.K_z,
    '1': pygame.K_1,
    '2': pygame.K_2,
    '3': pygame.K_3,
    '4': pygame.K_4,
    '5': pygame.K_5,
    '6': pygame.K_6,
    '7': pygame.K_7,
    '8': pygame.K_8,
    '9': pygame.K_9,
    '0': pygame.K_0,
    ' ': pygame.K_SPACE,
    '!': pygame.K_EXCLAIM,
    '@': pygame.K_AT,
    '#': pygame.K_HASH,
    '$': pygame.K_DOLLAR,
    '%': pygame.K_PERCENT,
    '&': pygame.K_AMPERSAND,
    '*': pygame.K_ASTERISK,
    '(': pygame.K_LEFTPAREN,
    ')': pygame.K_RIGHTPAREN,
    '_': pygame.K_UNDERSCORE,
    '+': pygame.K_PLUS,
    '-': pygame.K_MINUS,
    '=': pygame.K_EQUALS,
    '[': pygame.K_LEFTBRACKET,
    ']': pygame.K_RIGHTBRACKET,
    '\\': pygame.K_BACKSLASH,
    ';': pygame.K_SEMICOLON,
    ':': pygame.K_COLON,
    "'": pygame.K_QUOTE,
    '"': pygame.K_QUOTEDBL,
    ',': pygame.K_COMMA,
    '.': pygame.K_PERIOD,
    '/': pygame.K_SLASH,
    '<': pygame.K_LEFT,
    '>': pygame.K_RIGHT,
    '?': pygame.K_QUESTION,
    '^': pygame.K_UP
}


def remove_prefix_list(prefix_list: list, prefix: str):
    prefix_count = 0
    for st in prefix_list:
        if st.endswith(prefix):
            prefix_list[prefix_count] = st[:-len(prefix)]
        prefix_count += 1
    return prefix_list


def rect(position_x, position_y, width, height):
    position_x = position_x - width / 2
    position_y = position_y - height / 2
    Rectangle = pygame.rect.Rect(position_x, position_y, width, height)
    return Rectangle


class hitbox:
    velocity = [0, 0]
    position = []
    width = 0
    height = 0
    attribute = "undefined"

    def __init__(self, position: list, width: int, height: int):
        self.position = position
        self.width = width
        self.height = height
        hitboxes.append(self)

    def get_rect(self):
        return rect(self.position[0], self.position[1], self.width, self.height)

    def __str__(self):
        return "pos_x = %s, pos_y = %s, width = %s, height = %s, attribute = %s" % \
            (self.position[0], self.position[1], self.width, self.height, self.attribute)

    def collided_with(self, collided):
        print("Wow I a %s got collided with a %s!" % (self.attribute, collided.attribute))


class hitbox_static(hitbox):
    attribute = "static"

    def collided_with(self, collided):
        return


class hitbox_dmg(hitbox):
    attribute = "damage"

    def collided_with(self, collided):
        return

    def move_up(self, amount: int or float):
        self.position[1] -= amount

    def move_left(self, amount: int or float):
        self.position[0] -= amount

    def move_down(self, amount: int or float):
        self.position[1] += amount

    def move_right(self, amount: int or float):
        self.position[0] += amount

    def set_position(self, position: list):
        self.position = position

    def velocity_up(self, amount: int or float):
        self.velocity[1] -= amount

    def velocity_left(self, amount: int or float):
        self.velocity[0] -= amount

    def velocity_down(self, amount: int or float):
        self.velocity[1] += amount

    def velocity_right(self, amount: int or float):
        self.velocity[0] += amount

    def set_velocity(self, velocity: list):
        self.velocity = velocity


class hitbox_player(hitbox_dmg):
    walking = False
    attribute = "dynamic player"
    keys = ""
    collided = False
    previous_position = []
    speed = 500 / tick
    direction = 'none'

    def collided_with(self, collided):
        self.position = self.previous_position

    def collided_with_x(self, collided):
        self.position[0] = self.previous_position[0]

    def collided_with_y(self, collided):
        self.position[1] = self.previous_position[1]

    def __init__(self, position: list, width: int, height: int, keys: str):

        self.keys = keys
        camera_influencers.append(self)

        if len(self.keys) > 4:
            warnings.warn("Input string length for keybinding exceeds 4 characters")
        else:
            super().__init__(position, width, height)

    def set_keys_velocity(self, keys: str):
        current = 0
        if len(keys) > 4:
            warnings.warn("Input string length for keybinding exceeds 4 characters")
        else:
            self.previous_position = [self.position[0], self.position[1]]

            for char in keys:
                current += 1
                keys = pygame.key.get_pressed()
                if keys[key_mapping[char]] and current == 1:
                    self.velocity_up(self.speed)
                    self.direction = 'up'
                if keys[key_mapping[char]] and current == 2:
                    self.velocity_left(self.speed)
                    self.direction = 'left'
                if keys[key_mapping[char]] and current == 3:
                    self.velocity_down(self.speed)
                    self.direction = 'down'
                if keys[key_mapping[char]] and current == 4:
                    self.velocity_right(self.speed)
                    self.direction = 'right'

    def set_keys_position(self):
        current = 0
        if len(self.keys) > 4:
            warnings.warn("Input string length for keybinding exceeds 4 characters")
        else:
            self.previous_position = [self.position[0], self.position[1]]

            for char in self.keys:
                current += 1
                keys = pygame.key.get_pressed()
                if keys[key_mapping[char]] and current == 1:
                    self.move_up(self.speed)
                    self.direction = 'up'
                if keys[key_mapping[char]] and current == 2:
                    self.move_left(self.speed)
                    self.direction = 'left'
                if keys[key_mapping[char]] and current == 3:
                    self.move_down(self.speed)
                    self.direction = 'down'
                if keys[key_mapping[char]] and current == 4:
                    self.move_right(self.speed)
                    self.direction = 'right'


class mouse_hitbox(hitbox_static):
    attribute = "mouse"


class camera_hitbox(hitbox_static):
    attribute = "camera"


hitbox_player([display_width / 2, display_height / 2], 10, 10, "wasd")
hitbox_player([display_width / 2, display_height / 2], 10, 10, "ijkl")
hitbox_player([display_width / 2, display_height / 2], 10, 10, "^<v>")

class image_hitbox(hitbox_static):
    def __init__(self, position: list, width: int, height: int, image):
        super().__init__(position, width, height)
        self.image = image

    def draw(self):
        self.image = pygame.transform.scale(self.image, [self.get_rect()[2], self.get_rect()[3]])
        image_x = self.get_rect()[0]
        image_y = self.get_rect()[1]
        screen.blit(self.image, [image_x, image_y])

    def draw_rel(self):
        self.image = pygame.transform.scale(self.image, [self.get_rect()[2], self.get_rect()[3]])
        image_x = self.get_rect()[0] - camera_pos[0] + display_width / 2
        image_y = self.get_rect()[1] - camera_pos[1] + display_height / 2
        screen.blit(self.image, [image_x, image_y])


# JSON imports
# standard name: level.json :D


# noinspection PyBroadException
def load_json(json_name_input: str):
    json_level_checking = True
    json_level_checkin_pos = 0
    with open("Levels/%s.json" % json_name_input, "r") as file:
        json_level = json.load(file)
        while json_level_checking:
            try:
                json_level["Walls"][json_level_checkin_pos]["Position"]
            except:
                break
            json_level_pos = json_level["Walls"][json_level_checkin_pos]["Position"]
            json_level_type = json_level["Walls"][json_level_checkin_pos]["Type"]
            json_level_img = pygame.image.load(json_level["Image_Ref"][str(json_level_type)])
            image_hitbox(json_level_pos, 50, 50, json_level_img)
            json_level_checkin_pos += 1


# animations

# main hitboxes

# camera

# player hitboxes

pygame.mixer.music.play(999999)
levels = remove_prefix_list(levels, '.json')
level_input = True
level_popout = popout_list_helper.popout_list(rect(200, 100, 300, 100), font, pygame.image.load("Images/text_input.png"), "Click to see levels", levels)
text_box = tbh.textbox(rect(display_width / 2, display_height / 2, 300, 100), font, pygame.image.load("Images/text_input.png"), "Insert a JSON level name to load a level")
bg = pygame.image.load("Images/editor_bg.png")
bg = pygame.transform.scale(bg, [display_width, display_height])

while running:
    fps.tick(tick)
    old_display_width = display_width
    old_display_height = display_height
    display_width = screen.get_width()
    display_height = screen.get_height()
    if old_display_width != display_width or old_display_height != display_height:
        bg = pygame.transform.scale(bg, [display_width, display_height])
        text_box.rect = rect(display_width / 2, display_height / 2, 300, 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if level_input:
            text_box.check_keys_merged(event)

    # ignore this garbage
    screen.fill((200, 200, 200))
    if level_input:
        screen.blit(bg, [0, 0])
        text_box.update(screen)
        level_popout.update(screen)
        if text_box.get_entered():
            load_json(text_box.text)
            level_input = False
    # end of garbage

    if not level_input:
        ### UPDATE AREA ###

        # Camera Setup
        camera_pos_x = []
        camera_pos_y = []
        for hb in camera_influencers:
            camera_pos_x.append(hb.position[0])
            camera_pos_y.append(hb.position[1])
        camera_pos = [sum(camera_pos_x) / len(camera_pos_x), sum(camera_pos_y) / len(camera_pos_x)]

        for hb in hitboxes:

            if isinstance(hb, hitbox_player):
                hb.set_keys_position()

                if hb.position != hb.previous_position and walking_sound_cooldown == 0:
                    walking_sound_cooldown = tick / 3
                    walking_sound.play()
                if walking_sound_cooldown > 0:
                    walking_sound_cooldown -= 1

                pygame.draw.circle(screen, (255, 0, 0), [hb.position[0] - camera_pos[0] + display_width / 2,
                                                         hb.position[1] - camera_pos[1] + display_height / 2], 10)

            if isinstance(hb, hitbox_static):
                if not isinstance(hb, image_hitbox):
                    pygame.draw.rect(screen, (0, 0, 0), hb.get_rect(), 1000)

            if isinstance(hb, image_hitbox):
                hb.draw_rel()

            for hb_check in hitboxes:
                if hb.attribute == "static" and hb_check.attribute == "static":
                    continue
                if hb_check == hb:
                    continue

                if isinstance(hb, hitbox_player) and isinstance(hb_check, hitbox_static or image_hitbox):
                    if rect(hb.position[0], hb.previous_position[1], hb.width, hb.height).colliderect(
                            hb_check.get_rect()):
                        hb.collided_with_x(hb_check)

                if isinstance(hb, hitbox_player) and isinstance(hb_check, hitbox_static or image_hitbox):
                    if rect(hb.previous_position[0], hb.position[1], hb.width, hb.height).colliderect(
                            hb_check.get_rect()):
                        hb.collided_with_y(hb_check)

        ### UPDATE AREA ###

    pygame.display.flip()
pygame.quit()
