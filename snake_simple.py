# -*- coding: utf-8 -*-
"""
This is a Snake Game implemented using Pygame and pygame_gui libraries.

Features:
1. Customizable window size, snake size, and snake speed.
2. Randomly generated food that increases the snake's length upon consumption.
3. Detection of collisions with self and screen boundaries.
4. Simple UI for setting up the game.
5. Replayable game over screen.
"""

import pygame
import random
import pygame_gui

class SnakeGame:
    # Define the class constructor for the game
    def __init__(self):
        # Initialize pygame library
        pygame.init()
    
        # Set the screen size (width, height) of the game window
        self.screen_size = (800, 600)
        
        # Create the screen using the set size and store it in a variable
        self.screen = pygame.display.set_mode(self.screen_size)
    
        # Set the caption (title) of the game window to "贪吃蛇" (Snake in Chinese)
        pygame.display.set_caption("贪吃蛇")
    
        # Define color constants for WHITE, GREEN, and BLACK
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
    
        # Create a clock object to control game frame rate
        self.clock = pygame.time.Clock()
        
        # Create a font style with default system font and 50px size
        self.font_style = pygame.font.SysFont(None, 50)
    
        # Initialize the UI manager from pygame_gui library
        self.ui_manager = pygame_gui.UIManager(self.screen_size)
    
        # Call setup_game method to initialize game settings
        self.setup_game()
    

    # Define a helper method to change the snake's direction based on the input parameter
    def _change_direction(self, direction):
        # Check if the direction given is 'left'
        if direction == 'left':
            # Return coordinates to move the snake left by its size (negative horizontal movement)
            return -self.snake_size, 0
        # Check if the direction given is 'right'
        elif direction == 'right':
            # Return coordinates to move the snake right by its size (positive horizontal movement)
            return self.snake_size, 0
        # Check if the direction given is 'up'
        elif direction == 'up':
            # Return coordinates to move the snake up by its size (negative vertical movement)
            return 0, -self.snake_size
        # Check if the direction given is 'down'
        elif direction == 'down':
            # Return coordinates to move the snake down by its size (positive vertical movement)
            return 0, self.snake_size
        # If no valid direction is provided, don't move the snake
        else:
            return 0, 0
    

    # Define a method to start the game with user-specified settings
    def start_game(self):
        # Retrieve and convert user inputs from textboxes for width, height,
        # snake size, and snake speed; use default values if no input provided
        width_input = int(self.width_textbox.get_text() or 640)
        height_input = int(self.height_textbox.get_text() or 480)
        snake_size_input = int(self.snake_size_textbox.get_text() or 20)
        snake_speed_input = int(self.snake_speed_textbox.get_text() or 5)
    
        # Update the screen size with the user-specified width and height
        self.screen_size = (width_input, height_input)
        
        # Create a new game window using the updated screen size
        self.screen = pygame.display.set_mode(self.screen_size)
        
        # Update the snake size and speed with the user-specified values
        self.snake_size = snake_size_input
        self.snake_speed = snake_speed_input
    
        # Call the game loop method to start the game
        self.game_loop()
    

    # Define a method to set up the game menu and user interface elements
    def setup_game(self):
        # Set background color to black
        self.BLACK_BACKGROUND = (0, 0, 0)
    
        # Create UILabel and UITextEntryLine for window width input
        width_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 200), (180, 35)),
            text='Window Width:',
            manager=self.ui_manager
        )
        self.width_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((450, 200), (170, 35)),
            manager=self.ui_manager
        )
        self.width_textbox.set_text("640")
    
        # Create UILabel and UITextEntryLine for window height input
        height_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 250), (180, 35)),
            text='Window Height:',
            manager=self.ui_manager
        )
        self.height_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((450, 250), (170, 35)),
            manager=self.ui_manager
        )
        self.height_textbox.set_text("480")
    
        # Create UILabel and UITextEntryLine for snake size input
        snake_size_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 300), (180, 35)),
            text='Snake Size:',
            manager=self.ui_manager
        )
        self.snake_size_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((450, 300), (170, 35)),
            manager=self.ui_manager
        )
        self.snake_size_textbox.set_text("20")
    
        # Create UILabel and UITextEntryLine for snake speed input
        snake_speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 350), (180, 35)),
            text='Snake Speed:',
            manager=self.ui_manager
        )
        self.snake_speed_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((450, 350), (170, 35)),
            manager=self.ui_manager
        )
        self.snake_speed_textbox.set_text("5")
    
        # Create a UIButton to start the game
        start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((340, 420), (250, 60)),
            text='Start Game',
            manager=self.ui_manager
        )
    
        # Set up the event loop for the game menu
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
    
            # Process events in the game menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == start_button:
                            self.start_game()
                            running = False
    
                # Process UI manager events
                self.ui_manager.process_events(event)
    
            # Update UI elements with elapsed time
            self.ui_manager.update(time_delta)
    
            # Fill the screen with black background color
            self.screen.fill(self.BLACK_BACKGROUND)
            
            # Render UI elements on screen
            self.ui_manager.draw_ui(self.screen)
    
            # Update display
            pygame.display.update()
    
        # Quit pygame when the setup is complete
        pygame.quit()
    
    
    
    # Define a method to draw the snake on the screen using its body coordinates
    def draw_snake(self, snake_body):
        # Iterate through each segment of the snake's body
        for x in snake_body:
            # Draw a rectangle for each body segment using the segment's x and y coordinates,
            # snake size, and the black color
            pygame.draw.rect(self.screen, self.BLACK, [x[0], x[1], self.snake_size, self.snake_size])
    

    # Define a method to display a text message on the screen with a specified color and position
    def message(self, msg, color, pos):
        # Render the text using the provided font style, message, and color
        screen_text = self.font_style.render(msg, True, color)
        
        # Draw the rendered text onto the screen at the specified position
        self.screen.blit(screen_text, pos)
    
    def game_over_screen(self):
        # Initialize the UI manager for handling buttons and other UI elements
        self.ui_manager = pygame_gui.UIManager(self.screen_size)
    
        # Create a Replay button to restart the game after Game Over
        restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_size[0] / 2 - 100, self.screen_size[1] / 2 + 40), (200, 60)),
            text='Replay',
            manager=self.ui_manager
        )
    
        # Set the 'running' flag to True to start the game over screen loop
        running = True
        while running:
            # Calculate time delta, needed for updating UI manager
            time_delta = self.clock.tick(60) / 1000.0
    
            # Process all events in the Pygame event queue
            for event in pygame.event.get():
                # If the user closes the game window, set the 'running' flag to False and exit the loop
                if event.type == pygame.QUIT:
                    running = False
                # If a UI-related event occurs, check if it is a button press
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # If the Replay button was pressed, reset the game state and exit the current loop
                        if event.ui_element == restart_button:
                            self.__init__()
                            running = False
    
                # Pass the event to the UI manager to handle input
                self.ui_manager.process_events(event)
    
            # Clear the screen with the background color
            self.screen.fill(self.WHITE)
    
            # Calculate the center position for the "Game Over" message
            text_width, text_height = self.font_style.size("Game Over")
            text_x = self.screen_size[0] / 2 - text_width / 2
            text_y = self.screen_size[1] / 2 - text_height - 5
    
            # Display the "Game Over" message on the screen
            self.message("Game Over", self.BLACK, [text_x, text_y])
    
            # Update and draw the UI manager elements
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
    
            # Update the display to show changes
            pygame.display.update()
    
        # Quit the game after exiting the loop
        pygame.quit()
    
    
    def game_loop(self):
        # Initialize game_over flag as False to start the game loop
        game_over = False
    
        # Calculate the initial x and y position of the snake head by dividing screen dimensions by 2
        x1 = self.screen_size[0] / 2
        y1 = self.screen_size[1] / 2
    
        # Initialize change in x and y position for the snake head movement as 0 (no movement)
        x1_change = 0
        y1_change = 0
    
        # Create an empty list 'snake_body' to store the snake's body part positions
        snake_body = []
    
        # Initialize the length of the snake to 1 (only the head)
        length_of_snake = 1
    
        # Generate a random x-coordinate 'foodx' for the food on the screen within screen boundaries (excluding snake size) and align it with the grid
        foodx = round(random.randrange(0, self.screen_size[0] - self.snake_size) / 20.0) * 20.0
    
        # Generate a random y-coordinate 'foody' for the food on the screen within screen boundaries (excluding snake size) and align it with the grid
        foody = round(random.randrange(0, self.screen_size[1] - self.snake_size) / 20.0) * 20.0

        # Start the game loop and continue until the game is over
        while not game_over:
            # Iterate through Pygame events in the event queue
            for event in pygame.event.get():
                # Check if the event type is QUIT (e.g., closing the window)
                if event.type == pygame.QUIT:
                    game_over = True
        
                # Check if a key has been pressed
                if event.type == pygame.KEYDOWN:
                    # If no movement is happening, choose a random direction for the initial move
                    if x1_change == 0 and y1_change == 0:
                        direction = random.choice(['left', 'right', 'up', 'down'])
                        x1_change, y1_change = self._change_direction(direction)
        
                # Check if a key has been pressed again to handle snake movement
                if event.type == pygame.KEYDOWN:
                    # Update the snake's direction based on the arrow key pressed
                    if event.key == pygame.K_LEFT:
                        x1_change, y1_change = self._change_direction('left')
                    elif event.key == pygame.K_RIGHT:
                        x1_change, y1_change = self._change_direction('right')
                    elif event.key == pygame.K_UP:
                        x1_change, y1_change = self._change_direction('up')
                    elif event.key == pygame.K_DOWN:
                        x1_change, y1_change = self._change_direction('down')
        
            # Check if the snake goes out of the screen bounds; if yes, set game_over to True
            if x1 >= self.screen_size[0] or x1 < 0 or y1 >= self.screen_size[1] or y1 < 0:
                game_over = True
        
            # Update the snake's head position
            x1 += x1_change
            y1 += y1_change
        
            # Set the background color to white
            self.screen.fill(self.WHITE)
        
            # Draw the food in green on the screen
            pygame.draw.rect(self.screen, self.GREEN, [foodx, foody, self.snake_size, self.snake_size])
        
            # Update the snake's body by appending the new head position to the body list
            snake_head = [x1, y1]
            snake_body.append(snake_head)
            
            # Remove the tail segment if the body exceeds the actual length of the snake
            if len(snake_body) > length_of_snake:
                del snake_body[0]
        
            # Check for collisions between the snake's head and its body; if collided, set game_over to True
            for x in snake_body[:-1]:
                if x == snake_head:
                    game_over = True
        
            # Draw the updated snake on the screen
            self.draw_snake(snake_body)
            
            # Update the display
            pygame.display.update()
        
            # Check for collisions between the snake's head and the food; if yes, generate a new food position and increase the length of the snake
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.screen_size[0] - self.snake_size) / 20.0) * 20.0
                foody = round(random.randrange(0, self.screen_size[1] - self.snake_size) / 20.0) * 20.0
                length_of_snake += 1
        
            # Control the loop speed according to the snake's speed
            self.clock.tick(self.snake_speed)
        
        self.game_over_screen()

if __name__ == "__main__":
    SnakeGame()
