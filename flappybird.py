import pgzrun
import random

# Screen dimensions
WIDTH = 350
HEIGHT = 600

# Initialize game actors
background = Actor('background')
background2 = Actor('background')  # additional background for scrolling
background2.x = WIDTH + background.width / 2
bird = Actor('bird')
bird.x = 50
bird.y = HEIGHT / 2

# Define obstacles (tree trunks)
bar_up = Actor('bar_up')
bar_down = Actor('bar_down')
bar_up.x = bar_down.x = WIDTH
bar_up.y = 0
bar_down.y = HEIGHT

# Game variables
score = 0
high_score = 0
lives = 3
game_over = False
gravity = 0.5  # Gravity effect
bird_velocity = 0  # Bird's vertical velocity
bar_speed = random.randint(2, 5)
gap = 200  # Space between the upper and lower bars

def reset_bars():
    """Reset bars to random positions and speed."""
    global bar_speed
    bar_speed = random.randint(3, 6) + (score // 10)  # Speed increases with score
    bar_up.x = bar_down.x = WIDTH + 50
    bar_up.y = random.randint(-150, 0)
    bar_down.y = bar_up.y + bar_up.height + gap

def reset_game():
    """Reset game variables for a new start."""
    global score, lives, game_over, bird_velocity, bar_speed
    score = 0
    lives = 3
    game_over = False
    bird.y = HEIGHT / 2
    bird_velocity = 0
    reset_bars()

def draw():
    """Draw game elements and game over screen if lives are exhausted."""
    # Draw the moving background
    background.draw()
    background2.draw()

    # Draw game elements
    bar_up.draw()
    bar_down.draw()
    bird.draw()
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Lives: {lives}", (WIDTH - 80, 10), fontsize=30, color="white")
    screen.draw.text(f"High Score: {high_score}", (WIDTH / 2 - 50, 10), fontsize=30, color="yellow")

    if game_over:
        screen.clear()
        screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=50, color="red")
        screen.draw.text(f"Score: {score}", center=(WIDTH / 2, HEIGHT / 2), fontsize=40, color="white")
        screen.draw.text("Press ENTER to Restart", center=(WIDTH / 2, HEIGHT / 2 + 50), fontsize=30, color="yellow")
        screen.draw.text("Press ESC to Exit", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=30, color="yellow")

def update():
    """Update game elements if the game is not over."""
    global score, lives, game_over, bird_velocity, high_score

    if not game_over:
        # Apply gravity
        bird_velocity += gravity
        bird.y += bird_velocity

        # Move bars and reset if they go off-screen
        bar_up.x -= bar_speed
        bar_down.x -= bar_speed

        if bar_up.x < -bar_up.width:
            reset_bars()
            score += 1
            if score > high_score:
                high_score = score

        # Move the background to simulate forward motion
        background.x -= 1
        background2.x -= 1
        if background.x < -background.width / 2:
            background.x = WIDTH + background.width / 2
        if background2.x < -background2.width / 2:
            background2.x = WIDTH + background2.width / 2

        # Check for collisions and reduce lives if collided
        if bird.colliderect(bar_up) or bird.colliderect(bar_down):
            sounds.hit.play()  # play hit sound
            lives -= 1
            if lives > 0:
                bird.y = HEIGHT / 2  # Reset bird position
                bird_velocity = 0
                reset_bars()  # reset the bars
            else:
                game_over = True
        elif bird.y > HEIGHT or bird.y < 0:  # Check if bird goes out of bounds
            lives -= 1
            if lives > 0:
                bird.y = HEIGHT / 2  # Reset bird position
                bird_velocity = 0
                reset_bars()  # reset the bars
            else:
                game_over = True

def on_mouse_down():
    """Make the bird jump if the game is not over."""
    global bird_velocity
    if not game_over:
        bird_velocity = -8  # Upward velocity for jump
        sounds.jump.play()  # play jump sound

def on_key_down(key):
    """Handle key presses for restarting or exiting the game."""
    global game_over, score, lives

    if game_over:
        if key == keys.RETURN:
            reset_game()
        elif key == keys.ESCAPE:
            exit()

# Load sound effects
sounds.jump = tone.create('A4', 0.2)  # Example jump sound
sounds.hit = tone.create('C4', 0.3)   # Example hit sound

# Initialize the game
reset_bars()
pgzrun.go()
