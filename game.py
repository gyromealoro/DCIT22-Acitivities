import pygame
# from pygame.locals import (
#     K_UP,
#     K_DOWN,
#     K_LEFT,
#     K_RIGHT,
#     K_ESCAPE,
#     KEYDOWN,
#     QUIT,
# )

# Tile class
class Tile:
    def __init__(self, i, j):
        self.position = (i,j)
        self.status = 0 # 1 for circle, 2 for cross

    def is_inside_the_tile(self, pos: tuple):
        return (self.position[0] - 0.5 < pos[0] < self.position[0] + 0.5 and
                self.position[1] - 0.5 < pos[1] < self.position[1] + 0.5)

    def reset(self):
        self.status = 0

# Tic tac toe class
class TicTacToe:
    def __init__(self, size=200):
        self.size = size
        # self.position = position or (0,0)

        self.tiles = []
        for i in range(-1,2):
            for j in range(-1,2):
                self.tiles.append(Tile(i, j))

        self.put_circle = True
        
        self.grid_color = (0,0,0)
        self.circle_color = (0,0,255)
        self.cross_color = (255,0,0)
        
        self.line_thickness = 5

    def get_tile_from_mouse(self, screen): # O(n)
        x, y = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()
        offset_center = (x / 2, y / 2)

        rel_mouse_pos = (
            (mouse_pos[0] - offset_center[0]) / (self.size * 2/3),
            (mouse_pos[1] - offset_center[1]) / (self.size * 2/3)
        )

        for tile in self.tiles:
            if tile.is_inside_the_tile(rel_mouse_pos):
                return tile

        return None

    def put_object_on_tile(self, screen): # when mouse is left-clicked.
        clicked_tile = self.get_tile_from_mouse(screen)
        if clicked_tile and clicked_tile.status == 0:
            if self.put_circle:
                clicked_tile.status = 1
            else:
                clicked_tile.status = 2

        self.put_circle = not self.put_circle

    def draw(self, screen):
        x, y = screen.get_size()
        offset_center = (x / 2, y / 2)
        
        # create grid
        for x in (-1, 1):
            pygame.draw.line(
                screen,
                self.grid_color,
                (self.size * x / 3 + offset_center[0], self.size + offset_center[1]),
                (self.size * x / 3 + offset_center[0], -self.size + offset_center[1]),
                width=self.line_thickness
            )
        
        for y in (-1, 1):
            pygame.draw.line(
                screen,
                self.grid_color,
                (self.size + offset_center[0], self.size * y / 3 + offset_center[1]),
                (-self.size + offset_center[0], self.size * y / 3 + offset_center[1]),
                width=self.line_thickness
            )
        
        # create circles or cross on the grid
        for tile in self.tiles:
            if tile.status == 1:
                pos = (tile.position[0] * self.size * (2 / 3) + offset_center[0],
                       tile.position[1] * self.size * (2 / 3) + offset_center[1])
                pygame.draw.circle(screen, self.circle_color, pos, self.size / 4, self.line_thickness)
            elif tile.status == 2:
                pos = (tile.position[0] * self.size * (2 / 3) + offset_center[0],
                       tile.position[1] * self.size * (2 / 3) + offset_center[1])
                pygame.draw.line(
                    screen,
                    self.cross_color,
                    (pos[0] + self.size / 4, pos[1] + self.size / 4),
                    (pos[0] - self.size / 4, pos[1] - self.size / 4),
                    width=self.line_thickness
                )
                pygame.draw.line(
                    screen,
                    self.cross_color,
                    (pos[0] - self.size / 4, pos[1] + self.size / 4),
                    (pos[0] + self.size / 4, pos[1] - self.size / 4),
                    width=self.line_thickness
                )

# create window class
class Window:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def update(self):
        self.screen.fill((255, 255, 255)) # set bg color

# initialize
pygame.init()

main_window = Window()
tic_tac_toe = TicTacToe()

running = True

# loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            tic_tac_toe.put_object_on_tile(main_window.screen)

    main_window.update()
    tic_tac_toe.draw(main_window.screen)

    pygame.display.flip()

# quit
pygame.quit()