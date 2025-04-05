import pygame

# Initializing constants and variables
white = (255, 255, 255)
black = (0, 0, 0)

width = 600
height = 600

pygame.init()
game_font = pygame.font.SysFont("Arial", 40)


pygame.mixer.init()

# sound effects
paddle_sound = pygame.mixer.Sound("Sounds/ballhit.mp3")  
wall_sound = pygame.mixer.Sound("Sounds/wallHit.mp3")      
score_sound = pygame.mixer.Sound("Sounds/score.mp3")        

delay = 30

paddle_speed = 20
paddle_width = 10
paddle_height = 100

p1_x_pos = 10
p1_y_pos = height / 2 - paddle_height / 2

p2_x_pos = width - paddle_width - 10
p2_y_pos = height / 2 - paddle_height / 2

p1_score = 0
p2_score = 0

p1_up = False
p2_up = False
p1_down = False
p2_down = False

ball_x_pos = width / 2
ball_y_pos = height / 2
ball_width = 10
ball_x_vel = -10
ball_y_vel = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PongPY")

running = True

def draw_objects():
    pygame.draw.rect(screen, white, (int(p1_x_pos), int(p1_y_pos), paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (int(p2_x_pos), int(p2_y_pos), paddle_width, paddle_height))
    pygame.draw.circle(screen, white, (int(ball_x_pos), int(ball_y_pos)), ball_width)
    score = game_font.render(f"{p1_score} - {p2_score}", False, white)
    screen.blit(score, (width / 2 - 30, 30))

def apply_player_movement():
    global p1_y_pos, p2_y_pos

    if p1_up:
        p1_y_pos = max(p1_y_pos - paddle_speed, 0)
    if p1_down:
        p1_y_pos = min(p1_y_pos + paddle_speed, height - paddle_height)

    if p2_up:
        p2_y_pos = max(p2_y_pos - paddle_speed, 0)
    if p2_down:
        p2_y_pos = min(p2_y_pos + paddle_speed, height - paddle_height)

def apply_ball_movement():
    global ball_x_pos, ball_y_pos, ball_x_vel, ball_y_vel, p1_score, p2_score

    # Previous positions to detect collisions
    prev_ball_x = ball_x_pos
    prev_ball_y = ball_y_pos
    
    
    ball_x_pos += ball_x_vel
    ball_y_pos += ball_y_vel

    # Ball collision with top/bottom walls
    if ball_y_pos <= 0 or ball_y_pos >= height:
        ball_y_vel = -ball_y_vel
        wall_sound.play()  # Play wall bounce sound

    # Ball collision with paddles
    if (ball_x_pos <= p1_x_pos + paddle_width and p1_y_pos < ball_y_pos < p1_y_pos + paddle_height):
        # Only play sound if we're actually hitting from the right direction
        if prev_ball_x > p1_x_pos + paddle_width:
            paddle_sound.play()  
        ball_x_vel = -ball_x_vel
        ball_y_vel = (ball_y_pos - (p1_y_pos + paddle_height / 2)) / 5

    if (ball_x_pos >= p2_x_pos - ball_width and p2_y_pos < ball_y_pos < p2_y_pos + paddle_height):
        # Only play sound if we're actually hitting from the left direction
        if prev_ball_x < p2_x_pos - ball_width:
            paddle_sound.play()  
        ball_x_vel = -ball_x_vel
        ball_y_vel = (ball_y_pos - (p2_y_pos + paddle_height / 2)) / 5

    # Scoring conditions
    if ball_x_pos <= 0:
        p2_score += 1
        score_sound.play()  
        ball_x_pos, ball_y_pos = width / 2, height / 2
        ball_x_vel, ball_y_vel = 10, 0

    if ball_x_pos >= width:
        p1_score += 1
        score_sound.play()  
        ball_x_pos, ball_y_pos = width / 2, height / 2
        ball_x_vel, ball_y_vel = -10, 0

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                p1_up = True
            if event.key == pygame.K_s:
                p1_down = True
            if event.key == pygame.K_UP:
                p2_up = True
            if event.key == pygame.K_DOWN:
                p2_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1_up = False
            if event.key == pygame.K_s:
                p1_down = False
            if event.key == pygame.K_UP:
                p2_up = False
            if event.key == pygame.K_DOWN:
                p2_down = False

    screen.fill(black)
    apply_player_movement()
    apply_ball_movement()
    draw_objects()
    pygame.display.flip()
    pygame.time.delay(delay)

pygame.quit()