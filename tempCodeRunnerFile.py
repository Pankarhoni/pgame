import pygame

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (135, 206, 250)  # Light blue background
GRAVITY = 0.3
JUMP_STRENGTH = -10
DOUBLE_JUMP_STRENGTH = -8
SPEED = 5
ANIMATION_SPEED = 5  # Adjust to control animation speed
IDLE_ANIMATION_SPEED = 10  # Slower idle animation speed

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Platformer Game")

# Load Sprite Sheets
run_sprite_sheet = pygame.image.load("assets/Main Characters/Pink Man/Run (32x32).png")
idle_sprite_sheet = pygame.image.load("assets/Main Characters/Pink Man/Idle (32x32).png")
jump_sprite = pygame.image.load("assets/Main Characters/Pink Man/Jump (32x32).png")
fall_sprite = pygame.image.load("assets/Main Characters/Pink Man/Fall.png")
box_image = pygame.image.load("assets/Items/Boxes/Box1/Idle.png")

print("Loaded: Run (32x32).png")
print("Loaded: Idle (32x32).png")
print("Loaded: Jump (32x32).png")
print("Loaded: Fall.png")
print("Loaded: Box1/Idle.png")

FRAME_WIDTH = 32
FRAME_HEIGHT = 32

# Extract Frames from Sprite Sheets
def extract_frames(sprite_sheet):
    frames = []
    sheet_width = sprite_sheet.get_width()
    num_frames = sheet_width // FRAME_WIDTH  # Dynamically calculate frame count
    for i in range(num_frames):
        frame = sprite_sheet.subsurface((i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
        frames.append(frame)
    if not frames:
        print(f"Warning: No frames extracted from {sprite_sheet}")
    return frames

run_frames = extract_frames(run_sprite_sheet)
idle_frames = extract_frames(idle_sprite_sheet)
if not idle_frames:
    print("⚠️ Warning: No idle frames found! Using jump sprite instead.")
    idle_frames = [jump_sprite]

jump_frame = jump_sprite
fall_frame = fall_sprite

# Character Setup
character_rect = run_frames[0].get_rect(midbottom=(100, HEIGHT - 50))

# Boxes Setup
boxes = [
    box_image.get_rect(midbottom=(400, HEIGHT - 150)),
    box_image.get_rect(midbottom=(200, HEIGHT - 250)),
    box_image.get_rect(midbottom=(600, HEIGHT - 200))
]

# Movement Variables
velocity_y = 0
on_ground = True
on_box = False
box_touch = None  # Track which box character is on
double_jump_used = False
frame_index = 0
frame_counter = 0  # Controls animation speed
facing_right = True  # Track direction
jump_pressed = False

def check_collision():
    global on_ground, velocity_y, double_jump_used, on_box, box_touch
    on_ground = False
    on_box = False
    box_touch = None
    for box_rect in boxes:
        if character_rect.colliderect(box_rect) and velocity_y > 0:
            character_rect.bottom = box_rect.top
            velocity_y = 0
            on_ground = True
            on_box = True
            box_touch = box_rect
            double_jump_used = False
            return
        elif character_rect.colliderect(box_rect) and velocity_y < 0:
            character_rect.top = box_rect.bottom
            velocity_y = 0  # Stop upward movement if hitting the bottom of the box
    if character_rect.bottom >= HEIGHT - 50:
        character_rect.bottom = HEIGHT - 50
        velocity_y = 0
        on_ground = True
        double_jump_used = False

# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BG_COLOR)
    for box_rect in boxes:
        screen.blit(box_image, box_rect)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if on_ground:
                    velocity_y = JUMP_STRENGTH
                    on_ground = False
                    jump_pressed = True
                elif not double_jump_used:
                    velocity_y = JUMP_STRENGTH  # Use normal jump strength for double jump
                    double_jump_used = True
                    jump_pressed = True

    # Key Presses
    keys = pygame.key.get_pressed()
    moving = False  # Track if player is moving
    if keys[pygame.K_LEFT]:
        character_rect.x -= SPEED
        moving = True
        facing_right = False
    if keys[pygame.K_RIGHT]:
        character_rect.x += SPEED
        moving = True
        facing_right = True

    # Apply Gravity
    velocity_y += GRAVITY
    character_rect.y += velocity_y
    check_collision()

    # Select Animation
    if not on_ground:
        if velocity_y > 0:
            current_frame = fall_frame
        else:
            current_frame = jump_frame  # Use normal jump animation for both jumps
    elif moving:
        frame_counter += 1
        if frame_counter >= ANIMATION_SPEED:
            frame_index = (frame_index + 1) % max(1, len(run_frames))
            frame_counter = 0
        frame_index = min(frame_index, len(run_frames) - 1)  # Prevent out-of-bounds error
        current_frame = run_frames[frame_index]
    else:
        frame_counter += 1
        if frame_counter >= (IDLE_ANIMATION_SPEED if on_box else ANIMATION_SPEED):
            frame_index = (frame_index + 1) % max(1, len(idle_frames))  # Reset frame index safely
            frame_counter = 0
        frame_index = min(frame_index, len(idle_frames) - 1)  # Prevent out-of-bounds error
        current_frame = idle_frames[frame_index]

    # Flip Sprite if Moving Left
    if not facing_right:
        current_frame = pygame.transform.flip(current_frame, True, False)

