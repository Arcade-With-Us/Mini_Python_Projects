"""
Simple Snake Game using pygame
Save this file as snake_game.py and run with: python snake_game.py

Controls:
    - Arrow keys or WASD to move the snake
    - R to restart after game over
    - ESC or close window to quit

Author: ChatGPT
"""

import pygame
import sys
import random

# ---- Configuration ----
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20               # size of one block (snake segment / food)
FPS_START = 8                # starting frames per second (snake speed)
FPS_INCREMENT = 0.5          # speed increase per food eaten
FONT_NAME = None             # None -> default pygame font
BG_COLOR = (18, 18, 18)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 50, 50)
GRID_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)

# ---- Derived values (do not edit unless you know why) ----
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# ---- Helper functions ----
def draw_text(surface, text, size, x, y, center=True):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def random_food_position(snake):
    """Return a random (x, y) that is not occupied by the snake."""
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)

def grid_to_pixels(pos):
    x, y = pos
    return x * CELL_SIZE, y * CELL_SIZE

# ---- Game classes / logic ----
class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # Start snake in middle, moving right
        mid_x = GRID_WIDTH // 2
        mid_y = GRID_HEIGHT // 2
        self.snake = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = (1, 0)  # (dx, dy)
        self.next_direction = self.direction
        self.food = random_food_position(self.snake)
        self.score = 0
        self.fps = FPS_START
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_r,):
                    if self.game_over:
                        self.reset()
                # arrow keys and WASD support
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.set_direction(0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.set_direction(0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.set_direction(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.set_direction(1, 0)

    def set_direction(self, dx, dy):
        # Prevent reversing directly into yourself
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return
        self.next_direction = (dx, dy)

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wrap-around behavior (snake appears on opposite edge)
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            self.food = random_food_position(self.snake)
            self.fps += FPS_INCREMENT
        else:
            # Remove tail segment
            self.snake.pop()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def draw(self):
        self.screen.fill(BG_COLOR)

        # draw grid (optional subtle grid)
        self.draw_grid()

        # draw food
        fx, fy = grid_to_pixels(self.food)
        food_rect = pygame.Rect(fx, fy, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, FOOD_COLOR, food_rect)

        # draw snake (head slightly different shade)
        for i, (x, y) in enumerate(self.snake):
            px, py = grid_to_pixels((x, y))
            rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
            if i == 0:
                pygame.draw.rect(self.screen, (0, 200, 0), rect)  # head
            else:
                pygame.draw.rect(self.screen, SNAKE_COLOR, rect)

        # draw score
        draw_text(self.screen, f"Score: {self.score}", 20, 10, 10, center=False)

        if self.game_over:
            draw_text(self.screen, "GAME OVER", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 24)
            draw_text(self.screen, f"Final score: {self.score}", 28, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            draw_text(self.screen, "Press R to restart or ESC to quit", 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            # Use integer fps for clock tick but can be float between updates
            self.clock.tick(self.fps)

# ---- Run the game ----
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
