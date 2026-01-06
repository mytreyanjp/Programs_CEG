import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        
    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        
        if new_head in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_head)
        
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            
        return True
    
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self, position):
        return position in self.positions
    
    def draw(self, surface):
        for i, (x, y) in enumerate(self.positions):
            color = GREEN if i == 0 else BLUE
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
        return True
    
    def update(self):
        if not self.game_over and not self.paused:
            if not self.snake.move():
                self.game_over = True
                
            if self.snake.positions[0] == self.food.position:
                self.snake.grow = True
                self.score += 10
                self.food.randomize_position()
                
                while self.food.position in self.snake.positions:
                    self.food.randomize_position()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # Draw game elements
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw pause indicator
        if self.paused:
            pause_text = self.small_font.render("PAUSED - Press P to resume", True, WHITE)
            self.screen.blit(pause_text, (WINDOW_WIDTH // 2 - 100, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 10))
        
        # Draw instructions
        instructions = [
            "Arrow keys: Move snake",
            "P: Pause/Resume",
            "SPACE: Restart (when game over)",
            "ESC: Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (WINDOW_WIDTH - 200, 10 + i * 20))
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(10)  # Control game speed
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
