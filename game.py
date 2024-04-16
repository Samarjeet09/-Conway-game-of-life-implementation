import pygame
from typing import List

pygame.init()
HEIGHT, WIDTH = 500, 700
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (127, 255, 0)
PURPLE = (43, 25, 61)
PINK = (197, 151, 157)
BLUE = (44, 54, 94)
CYAN = (75, 143, 140)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True



button_font = pygame.font.Font("freesansbold.ttf", 15)
button_width = 150
button_height = 70
button_margin = 20
button_hover_color = (150, 150, 150)


# Function to draw a button
def draw_button(x, y, button_color,text, action, board):
    button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(SCREEN, button_color, button_rect)
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    SCREEN.blit(text_surface, text_rect)
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(SCREEN, button_hover_color, button_rect, 3)
        if pygame.mouse.get_pressed()[0] == 1:
            action(board)


# Function to handle button actions
def start_simulation(board):
    board.setSimState(1)


def pause_simulation(board):
    board.setSimState(-1)


def reset_board(board):
    board.reset()


def simulate_next_step(board):
    board.simulate()


class Grid:
    """
    Args:
    screen_ref: reference to the screen to draw
    block_size: size of the block
    screen_width: screen parameter
    screen_height: screen parameter
    underpopulation_threshhold:default = 2 Alive cell dies if neighbours less than this threshold(exclusive)
    overpopulation_threshold:default = 3 Alive cell dies if neighbours more than this threshold(exclusive)
    reproduction_threshold:default = 3 Dead cell becomes alive if surrounded by exactly this number of cells
    """

    def __init__(
        self,
        screen_ref,
        block_size,
        screen_width,
        screen_height,
        underpopulation_threshhold: int = 2,
        overpopulation_threshhold: int = 3,
        reproduction_threshhold: int = 3,
    ):
        self.screen = screen_ref
        self.block_size = block_size
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.rows: int = screen_height // block_size
        self.cols: int = screen_width // block_size
        self.num_rects: int = self.rows * self.cols
        self.sim_state = False
        self.rect_dict = dict()
        self.alive_status: List[bool] = [
            [False for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.ALIVE_COLOR = (127, 255, 0)
        self.DEAD_COLOR = (225, 225, 225)
        i: int = 0
        for y in range(0, self.SCREEN_HEIGHT, self.block_size):
            for x in range(0, self.SCREEN_WIDTH, self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                self.rect_dict[i] = rect
                i += 1

        self.underpopulation_threshhold = underpopulation_threshhold
        self.overpopulation_threshhold = overpopulation_threshhold
        self.reproduction_threshhold = reproduction_threshhold

        print("{} Cells created".format(self.num_rects))

    def drawGrid(self):
        for y in range(self.cols):
            for x in range(self.rows):
                rect = self.rect_dict[y + x * self.cols]
                isAlive = self.alive_status[x][y]
                color = self.ALIVE_COLOR if isAlive else self.DEAD_COLOR
                # 1 for outline , 0 for fill -> opp of this var
                pygame.draw.rect(self.screen, color, rect, int(not isAlive))

    def changeCellState(self, cell_x, cell_y):
        """toggle state of the cell"""
        self.alive_status[cell_x][cell_y] = not self.alive_status[cell_x][cell_y]

    def cell_pressed(self, click_x, click_y):
        cell_x, cell_y = click_x // self.block_size, click_y // self.block_size
        self.changeCellState(cell_x, cell_y)

    def simulate(self):
        # t,tr,r,br,b,bl,l,tl
        temp: List[bool] = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        deltas = [
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
        ]
        for x in range(self.rows):
            for y in range(self.cols):
                neighbours: int = 0
                for dx, dy in deltas:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols:
                        if self.alive_status[nx][ny]:
                            neighbours += 1
                if self.alive_status[x][y]:
                    if (
                        self.underpopulation_threshhold
                        <= neighbours
                        <= self.overpopulation_threshhold
                    ):
                        temp[x][y] = True
                else:
                    if neighbours == self.reproduction_threshhold:
                        temp[x][y] = True

        self.alive_status = temp

    def reset(self):
        self.alive_status = [
            [False for _ in range(self.cols)] for _ in range(self.rows)
        ]

    def clickedInBoard(self, x, y) -> bool:
        return 0 <= x < self.SCREEN_HEIGHT and 0 <= y < self.SCREEN_WIDTH

    def getSimState(self):
        return self.sim_state

    def setSimState(self, action: int):
        if action >= 0:
            self.sim_state = True
        else:
            self.sim_state = False


board = Grid(SCREEN, 25, WIDTH - 200, HEIGHT)


while running:
    SCREEN.fill(BLACK)
    draw_button(
        WIDTH - button_width - button_margin,
        button_margin,
        PURPLE,
        "Start or press S",
        start_simulation,
        board,
    )
    draw_button(
        WIDTH - button_width - button_margin,
        button_margin * 2 + button_height,
        BLUE,
        "Pause or press P ",
        pause_simulation,
        board,
    )
    draw_button(
        WIDTH - button_width - button_margin,
        button_margin * 3 + button_height * 2,
        CYAN,
        "Reset or Press R",
        reset_board,
        board,
    )
    draw_button(
        WIDTH - button_width - button_margin,
        button_margin * 4 + button_height * 3,
        PINK,
        "Next or Press N",
        simulate_next_step,
        board,
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if board.clickedInBoard(y, x):
                board.cell_pressed(y, x)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                board.setSimState(1)
            if event.key == pygame.K_p:
                board.setSimState(-1)
            if event.key == pygame.K_r:
                board.reset()
            if event.key == pygame.K_n:
                board.simulate()
                pygame.display.set_caption("Next")

    if board.getSimState():
        board.simulate()
        pygame.display.set_caption("Simulating")
    else:
        pygame.display.set_caption("Paused")

    board.drawGrid()

    pygame.display.flip()

    clock.tick(13)

pygame.quit()
