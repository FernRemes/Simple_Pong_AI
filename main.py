import pygame
from pong import Game  # Ensure that the Game class is correctly imported from game.py

# Constants for screen dimensions
WIDTH, HEIGHT = 1000, 555

class PongGame:
    def __init__(self, window, width, height, mode):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball
        self.mode = mode  # mode: 0 for two-player, 1 for AI left, 2 for AI right
        
    def run_game(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if self.mode == 0 or self.mode == 2:  # Player controls left paddle
                if keys[pygame.K_w]:
                    self.game.move_paddle(left=True, up=True)
                if keys[pygame.K_s]:
                    self.game.move_paddle(left=True, up=False)
            else:  # AI controls left paddle
                self.ai_move_paddle(left=True)

            if self.mode == 0 or self.mode == 1:  # Player controls right paddle
                if keys[pygame.K_UP]:
                    self.game.move_paddle(left=False, up=True)
                if keys[pygame.K_DOWN]:
                    self.game.move_paddle(left=False, up=False)
            else:  # AI controls right paddle
                self.ai_move_paddle(left=False)

            game_info = self.game.loop()
            print(game_info.left_score, game_info.right_score)

            self.game.draw()
            pygame.display.update()

        pygame.quit()

    def ai_move_paddle(self, left=True):
        paddle = self.left_paddle if left else self.right_paddle
        if self.ball.y < paddle.y:
            self.game.move_paddle(left=left, up=True)
        elif self.ball.y > paddle.y + paddle.HEIGHT:
            self.game.move_paddle(left=left, up=False)

def main_menu(window):
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 30)
    
    # Load the menu background image
    background_image = pygame.image.load('pong_bgd.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize image to fit the window

    # Define colors for buttons
    button_color = (204, 0, 0)
    hover_color = (180, 0, 0)
    text_color = (255, 255, 255)
    hover_text_color = (200, 200, 200)

    # Define button dimensions and spacing
    button_width, button_height = 269, 50
    button_x = 730
    button_spacing = 69
    
    while run:
        window.blit(background_image, (0, 0))  # Draw the background image
        clock.tick(60)

        # Render and position buttons
        button1_rect = pygame.Rect(button_x - 130, 135, button_width, button_height)
        button2_rect = pygame.Rect(button_x - 130, 135 + button_spacing, button_width, button_height)
        button3_rect = pygame.Rect(button_x - 130, 135 + 2 * button_spacing, button_width, button_height)

        # Draw buttons with hover effect
        pygame.draw.rect(window, button_color, button1_rect, 0, 20)
        pygame.draw.rect(window, button_color, button2_rect, 0, 20)
        pygame.draw.rect(window, button_color, button3_rect, 0, 20)

        # Render button text centered within each button rectangle
        play_button = font.render("Two Players", True, text_color)
        play_button_rect = play_button.get_rect(center=button1_rect.center)
        window.blit(play_button, play_button_rect)

        ai_left_button = font.render("CPU Vs You", True, text_color)
        ai_left_button_rect = ai_left_button.get_rect(center=button2_rect.center)
        window.blit(ai_left_button, ai_left_button_rect)

        ai_right_button = font.render("You Vs CPU", True, text_color)
        ai_right_button_rect = ai_right_button.get_rect(center=button3_rect.center)
        window.blit(ai_right_button, ai_right_button_rect)

        # Check for mouse hover over buttons
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button1_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, hover_color, button1_rect,0 , 20)
            play_button = font.render("Two Players", True, hover_text_color)
            window.blit(play_button, play_button_rect)

        if button2_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, hover_color, button2_rect, 0, 20)
            ai_left_button = font.render("CPU Vs You", True, hover_text_color)
            window.blit(ai_left_button, ai_left_button_rect)

        if button3_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, hover_color, button3_rect, 0, 20)
            ai_right_button = font.render("You Vs CPU", True, hover_text_color)
            window.blit(ai_right_button, ai_right_button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(mouse_x, mouse_y):
                    return 0  # Two Player
                elif button2_rect.collidepoint(mouse_x, mouse_y):
                    return 1  # AI Left Paddle
                elif button3_rect.collidepoint(mouse_x, mouse_y):
                    return 2  # AI Right Paddle

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Game")

    mode = main_menu(window)
    if mode is not None:
        pong_game = PongGame(window, WIDTH, HEIGHT, mode)
        pong_game.run_game()
