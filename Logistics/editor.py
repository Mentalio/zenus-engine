import pygame
import ctypes
import tbh

editor = 'mentalio_ind.mentalio_games.editor.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(editor)

json_name = ""

display_width = 2000
display_height = 1200
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Editor")
pygame.display.set_icon(pygame.image.load("../Main Game/Images/editor_icon.png"))
pygame.init()
running = True
hitboxes = []
pygame.mouse.set_visible(False)
font_sml = pygame.font.Font("../Main Game/Types/Handjet-Regular.ttf", 16)
font = pygame.font.Font("../Main Game/Types/Handjet-Regular.ttf", 32)
font_lrg = pygame.font.Font("../Main Game/Types/Handjet-Regular.ttf", 64)

font_sml_bold = pygame.font.Font("../Main Game/Types/Handjet-ExtraBold.ttf", 16)
font_bold = pygame.font.Font("../Main Game/Types/Handjet-ExtraBold.ttf", 32)
font_lrg_bold = pygame.font.Font("../Main Game/Types/Handjet-ExtraBold.ttf", 64)


pygame.mixer.music.load("../Main Game/Audio/menu.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(9999)

cursor = pygame.image.load("../Main Game/Images/cursor.png")
cursor = pygame.transform.scale(cursor, [20, 20])

keys_mapping = {
    1: pygame.K_1,
    2: pygame.K_2,
    3: pygame.K_3,
    4: pygame.K_4,
    5: pygame.K_5,
    6: pygame.K_6,
    7: pygame.K_7,
    8: pygame.K_8,
    9: pygame.K_9,
    0: pygame.K_0,
}


def rect(position_x, position_y, width, height):
    position_x = position_x - width / 2
    position_y = position_y - height / 2
    Rectangle = pygame.rect.Rect(position_x, position_y, width, height)
    return Rectangle


class item:
    def __init__(self, image_name: str, t: str):
        """
        No need to add the file config. They will automatically be set as a png
        As well as in the sub folder of Main Game
        Creates 2 images,
        One small (used for cursor highlights)
        One big (used for displaying the object)
        Type is going to be used on the scroll wheel for floors and enemies
        """
        self.image_name = image_name + ".png"
        image_name = "../Main Game/Images/" + image_name + ".png"
        self.image = pygame.transform.scale(pygame.image.load(image_name), [50, 50])
        self.image_sml = pygame.transform.scale(pygame.image.load(image_name), [30, 30])
        self.type = t


class editor_helper:
    items = [item("bin", "wall")]
    current = 0

    def add_item(self, item_input: item):
        self.items.append(item_input)

    def update_current(self):
        keys = pygame.key.get_pressed()
        checking_keys = True
        key_checked = 0
        while checking_keys:
            if len(self.items) > key_checked:
                if keys[keys_mapping[key_checked]]:
                    self.current = key_checked
            else:
                checking_keys = False
            key_checked += 1


class clickable_hitbox:
    gray = 10
    position = [0, 0]
    width = 50
    height = 50
    type = 0
    image1 = pygame.image.load("../Main Game/Images/wall1.png")
    image1 = pygame.transform.scale(image1, [width, height])
    image2 = pygame.image.load("../Main Game/Images/wall2.png")
    image2 = pygame.transform.scale(image2, [width, height])
    image3 = pygame.image.load("../Main Game/Images/wall3.png")
    image3 = pygame.transform.scale(image3, [width, height])
    hitbox_info = [position[0], position[1], type]

    def __init__(self, position: list, editor_in: editor_helper):
        """
        Use the items from the ed instance
        :)
        """
        self.editor = editor_in
        self.position = position
        hitboxes.append(self)

    def get_rect(self):
        return rect(self.position[0], self.position[1], self.width, self.height)

    def draw(self):
        if self.type != 0:
            screen.blit(self.editor.items[self.type].image,
                        (self.position[0] - self.editor.items[self.editor.current].image.get_rect()[2] / 2,
                         self.position[1] - self.editor.items[self.editor.current].image.get_rect()[3] / 2))
        else:
            pygame.draw.rect(screen, (10, 10, 10), rect(self.position[0], self.position[1], 50, 50), 1)


ed = editor_helper()
ed.add_item(item("wall1", "wall"))
ed.add_item(item("wall2", "wall"))
ed.add_item(item("wall3", "wall"))

## Make the grid ##
grid_make = True
clickable_hitbox([25, 25], ed)
grid_pos = [25, 25]
while grid_make:
    grid_pos[0] += 50
    clickable_hitbox([grid_pos[0], grid_pos[1]], ed)
    if grid_pos[1] > display_height:
        break
    if grid_pos[0] > display_width - 50:
        grid_pos[1] += 50
        grid_pos[0] = -25

idk = tbh.textbox(rect(display_width / 2, display_height / 2, 300, 100), font, pygame.image.load(
    "../Main Game/Images/text_input.png"), "Input name for levels JSON file")
bg = pygame.image.load("../Main Game/Images/editor_bg.png")
bg = pygame.transform.scale(bg, [display_width, display_height])
text_input = True

while running:
    mouse = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if text_input:
            idk.check_keys_merged(event)

    if text_input:
        screen.blit(bg, [0, 0])
        idk.draw(screen)
        idk.check_clicked_alone()
        if idk.entered:
            pygame.mixer.music.load("../Main Game/Audio/main_song.mp3")
            pygame.mixer.music.play()
            json_name = idk.text
            text_input = False
    else:
        ed.update_current()

        for hb in hitboxes:
            if isinstance(hb, clickable_hitbox):
                mouse_button = pygame.mouse.get_pressed()
                if hb.get_rect().collidepoint(mouse):
                    if mouse_button[0]:
                        hb.type = hb.editor.current
                hb.draw()

        pygame.draw.circle(screen, (255, 255, 255), [display_width / 2, display_height / 2], 5)
        screen.blit(font_sml.render("0, 0", True, (255, 255, 255)), [display_width / 2 + 10, display_height / 2])
        screen.blit(ed.items[ed.current].image_sml, [list(mouse)[0] + 20, list(mouse)[1] + 20])

    screen.blit(cursor, mouse)

    pygame.display.flip()

### END OF LOOP ###
current_line = 0
json_out_str = '{\n  "Walls" : [\n'
for hb in hitboxes:
    """
    This is really a mess
    I wasn't bothered to write a JSON formatter
    So have this >:D
    """
    if isinstance(hb, clickable_hitbox):
        if hb.type != 0:
            json_out_str += "    {\n"
            json_out_str += '      "Position" : %s, \n' % hb.position
            json_out_str += '      "Type" : %s \n' % hb.type
            json_out_str += "    },\n"
json_out_str = json_out_str[:-2]
json_out_str += "\n  ],\n"
json_out_str += '"Image_Ref" : {\n'

items_pos = 0
for it in ed.items:
    json_out_str += '  "%s" : "Images/%s",\n' % (items_pos, it.image_name)
    items_pos += 1

json_out_str = json_out_str[:-2]
json_out_str += "\n"
json_out_str += "  }"
json_out_str += "\n}"

if json_name:
    with open("../Main Game/Levels/%s.json" % json_name, "w") as file:
        file.write(json_out_str)
