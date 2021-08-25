import pygame
from random import randint

pygame.init()
clock = pygame.time.Clock()


class Crosshair(pygame.sprite.Sprite):

    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("Sound/sfx/shot.mp3")

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        self.gunshot.play()
        pygame.sprite.spritecollide(crosshair, target_group, True)


class Target(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class Button(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__()
        self.clicked = False
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def restart(self):
        action = False
        #  Get mouse pos
        pos = pygame.mouse.get_pos()

        #  Start checking
        #  Check if cursor is above the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed(3)[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed(3)[0]:
            self.clicked = False
        return action


background_colour = (56, 56, 56)
(width, height) = (1366, 768)

# Screen properties
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MouseAim")
screen.fill(background_colour)
bg = pygame.image.load("Images/background.png")
font_normal = pygame.font.Font("Fonts/score.ttf", 40)

# Crosshair
crosshair = Crosshair("Images/crosshair.png")
# Crosshair group
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)
pygame.mouse.set_visible(False)

# Score text
text_score = font_normal.render(str("Start clicking!"), True, (255, 255, 255))
# Restart "button"
button = Button("Images/restart.png", width - 70, 75)
button_group = pygame.sprite.Group()
button_group.add(button)
# Target group
target_group = pygame.sprite.Group()


# Target
def render_targets():
    for obj in range(10):
        # Create target object at random position
        target = Target("Images/target.png", randint(0, width), randint(0, height))
        target_group.add(target)


render_targets()
clicks = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()
            clicks += 1
            text_score = font_normal.render(str(clicks), True, (255, 255, 255))

    # Timer
    time = pygame.time.get_ticks() / 1000
    pygame.display.flip()

    screen.blit(bg, (0, 0))  # Background
    screen.blit(text_score, (width / 2, 40))  # Score
    text_timer = font_normal.render(str(time), True, (255, 0, 0))
    screen.blit(text_timer, (width / 2, 80))  # Timer

    button_group.draw(screen)  # Draw button
    if button.restart():
        clicks -= clicks
        render_targets()

    target_group.draw(screen)  # Draw targets
    crosshair_group.draw(screen)  # Draw crosshair

    crosshair_group.update()
    clock.tick(60)
