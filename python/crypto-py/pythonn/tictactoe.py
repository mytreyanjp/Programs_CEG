import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
BOARD_SIZE = 3
CELL_SIZE = 150
BOARD_MARGIN = 50
LINE_WIDTH = 10
CIRCLE_RADIUS = 50
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class TicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1  # 1 for X, 2 for O
        self.game_over = False
        self.winner = 0
        self.game_mode = None  # 1 for 2-player, 2 for vs AI
        self.ai_difficulty = None  # 1 for easy, 2 for medium, 3 for hard
        
    def draw_board(self):
        # Draw background
        self.screen.fill(WHITE)
        
        # Draw title
        title = self.font.render("Tic Tac Toe", True, BLACK)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - 80, 20))
        
        # Draw game mode selection if not selected
        if self.game_mode is None:
            self.draw_mode_selection()
            return
            
        # Draw difficulty selection if vs AI and not selected
        if self.game_mode == 2 and self.ai_difficulty is None:
            self.draw_difficulty_selection()
            return
            
        # Draw game board
        self.draw_game_board()
        
        # Draw current player
        if not self.game_over:
            player_text = "X's Turn" if self.current_player == 1 else "O's Turn"
            if self.game_mode == 2 and self.current_player == 2:
                player_text = "AI's Turn"
            text = self.small_font.render(player_text, True, BLACK)
            self.screen.blit(text, (WINDOW_WIDTH // 2 - 50, 550))
            
        # Draw winner
        if self.game_over:
            if self.winner == 0:
                winner_text = "It's a Draw!"
            elif self.winner == 1:
                winner_text = "X Wins!"
            else:
                if self.game_mode == 2:
                    winner_text = "AI Wins!"
                else:
                    winner_text = "O Wins!"
                    
            text = self.font.render(winner_text, True, GREEN)
            self.screen.blit(text, (WINDOW_WIDTH // 2 - 60, 580))
            
            restart_text = self.small_font.render("Click anywhere to restart", True, GRAY)
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 80, 620))
    
    def draw_mode_selection(self):
        text = self.font.render("Select Game Mode:", True, BLACK)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - 120, 200))
        
        # Two player button
        pygame.draw.rect(self.screen, BLUE, (150, 250, 300, 60))
        text = self.font.render("Two Players", True, WHITE)
        self.screen.blit(text, (250, 270))
        
        # vs AI button
        pygame.draw.rect(self.screen, RED, (150, 350, 300, 60))
        text = self.font.render("vs AI", True, WHITE)
        self.screen.blit(text, (290, 370))
    
    def draw_difficulty_selection(self):
        text = self.font.render("Select Difficulty:", True, BLACK)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - 100, 200))
        
        difficulties = ["Easy", "Medium", "Hard"]
        colors = [GREEN, BLUE, RED]
        
        for i, (diff, color) in enumerate(zip(difficulties, colors)):
            pygame.draw.rect(self.screen, color, (150, 250 + i * 80, 300, 60))
            text = self.font.render(diff, True, WHITE)
            self.screen.blit(text, (WINDOW_WIDTH // 2 - 30, 270 + i * 80))
    
    def draw_game_board(self):
        # Draw grid lines
        for i in range(1, BOARD_SIZE):
            # Vertical lines
            pygame.draw.line(self.screen, BLACK, 
                           (BOARD_MARGIN + i * CELL_SIZE, BOARD_MARGIN),
                           (BOARD_MARGIN + i * CELL_SIZE, BOARD_MARGIN + BOARD_SIZE * CELL_SIZE),
                           LINE_WIDTH)
            # Horizontal lines
            pygame.draw.line(self.screen, BLACK,
                           (BOARD_MARGIN, BOARD_MARGIN + i * CELL_SIZE),
                           (BOARD_MARGIN + BOARD_SIZE * CELL_SIZE, BOARD_MARGIN + i * CELL_SIZE),
                           LINE_WIDTH)
        
        # Draw X's and O's
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 1:  # X
                    self.draw_x(row, col)
                elif self.board[row][col] == 2:  # O
                    self.draw_o(row, col)
    
    def draw_x(self, row, col):
        x = BOARD_MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        
        pygame.draw.line(self.screen, RED,
                        (x - CIRCLE_RADIUS, y - CIRCLE_RADIUS),
                        (x + CIRCLE_RADIUS, y + CIRCLE_RADIUS),
                        CROSS_WIDTH)
        pygame.draw.line(self.screen, RED,
                        (x + CIRCLE_RADIUS, y - CIRCLE_RADIUS),
                        (x - CIRCLE_RADIUS, y + CIRCLE_RADIUS),
                        CROSS_WIDTH)
    
    def draw_o(self, row, col):
        x = BOARD_MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        
        pygame.draw.circle(self.screen, BLUE,
                          (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)
    
    def handle_click(self, pos):
        x, y = pos
        
        if self.game_mode is None:
            # Mode selection
            if 150 <= x <= 450 and 250 <= y <= 310:
                self.game_mode = 1  # Two players
            elif 150 <= x <= 450 and 350 <= y <= 410:
                self.game_mode = 2  # vs AI
            return
            
        if self.game_mode == 2 and self.ai_difficulty is None:
            # Difficulty selection
            if 150 <= x <= 450 and 250 <= y <= 310:
                self.ai_difficulty = 1  # Easy
            elif 150 <= x <= 450 and 330 <= y <= 390:
                self.ai_difficulty = 2  # Medium
            elif 150 <= x <= 450 and 410 <= y <= 470:
                self.ai_difficulty = 3  # Hard
            return
            
        if self.game_over:
            self.reset_game()
            return
            
        if self.game_mode == 2 and self.current_player == 2:
            return  # AI's turn
            
        # Game board click
        if (BOARD_MARGIN <= x <= BOARD_MARGIN + BOARD_SIZE * CELL_SIZE and
            BOARD_MARGIN <= y <= BOARD_MARGIN + BOARD_SIZE * CELL_SIZE):
            
            col = (x - BOARD_MARGIN) // CELL_SIZE
            row = (y - BOARD_MARGIN) // CELL_SIZE
            
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.check_winner()
                
                if not self.game_over:
                    self.current_player = 3 - self.current_player  # Switch player
                    
                    if self.game_mode == 2 and self.current_player == 2:
                        self.ai_move()
    
    def check_winner(self):
        # Check rows
        for row in range(BOARD_SIZE):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                self.winner = self.board[row][0]
                self.game_over = True
                return
                
        # Check columns
        for col in range(BOARD_SIZE):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                self.winner = self.board[0][col]
                self.game_over = True
                return
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.board[0][0]
            self.game_over = True
            return
            
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winner = self.board[0][2]
            self.game_over = True
            return
            
        # Check for draw
        if all(self.board[row][col] != 0 for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
            self.winner = 0
            self.game_over = True
    
    def ai_move(self):
        if self.game_over:
            return
            
        best_move = None
        
        if self.ai_difficulty == 1:  # Easy - random move
            empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == 0]
            if empty_cells:
                best_move = random.choice(empty_cells)
                
        elif self.ai_difficulty == 2:  # Medium - mix of strategy and random
            best_move = self.find_best_move()
            if best_move is None or random.random() < 0.3:  # 30% chance of random move
                empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == 0]
                if empty_cells:
                    best_move = random.choice(empty_cells)
                    
        else:  # Hard - best move
            best_move = self.find_best_move()
            if best_move is None:
                empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == 0]
                if empty_cells:
                    best_move = random.choice(empty_cells)
        
        if best_move:
            row, col = best_move
            self.board[row][col] = 2
            self.check_winner()
            if not self.game_over:
                self.current_player = 1
    
    def find_best_move(self):
        # Check if AI can win
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 0:
                    self.board[row][col] = 2
                    if self.check_winner_simulation():
                        self.board[row][col] = 0
                        return (row, col)
                    self.board[row][col] = 0
        
        # Check if player can win and block
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 0:
                    self.board[row][col] = 1
                    if self.check_winner_simulation():
                        self.board[row][col] = 0
                        return (row, col)
                    self.board[row][col] = 0
        
        # Take center if available
        if self.board[1][1] == 0:
            return (1, 1)
        
        # Take corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty_corners = [(r, c) for r, c in corners if self.board[r][c] == 0]
        if empty_corners:
            return random.choice(empty_corners)
        
        # Take sides
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        empty_sides = [(r, c) for r, c in sides if self.board[r][c] == 0]
        if empty_sides:
            return random.choice(empty_sides)
        
        return None
    
    def check_winner_simulation(self):
        # Check rows
        for row in range(BOARD_SIZE):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                return True
                
        # Check columns
        for col in range(BOARD_SIZE):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                return True
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return True
            
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return True
            
        return False
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
