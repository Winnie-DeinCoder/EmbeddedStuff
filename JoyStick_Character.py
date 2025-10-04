import pygame
import serial
import re

# Set up serial port
ser = serial.Serial('COM7', 9600, timeout=1)

# Pygame init
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Joystick-Controlled Character")

# Character setup
char_pos = [400, 300]
char_color = (255, 0, 0)
char_radius = 20
speed = 5

# Main loop
running = True
clock = pygame.time.Clock()

def parse_serial_line(line):
    match = re.match(r"X:(\d+),Y:(\d+)", line)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

while running:
    screen.fill((30, 30, 30))

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read from serial
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        x_val, y_val = parse_serial_line(line)

        if x_val is not None and y_val is not None:
            # Map analog values (0-1023) to direction
            if x_val < 400:
                char_pos[0] -= speed
            elif x_val > 600:
                char_pos[0] += speed

            if y_val < 400:
                char_pos[1] -= speed
            elif y_val > 600:
                char_pos[1] += speed

    # Keep character in bounds
    char_pos[0] = max(char_radius, min(800 - char_radius, char_pos[0]))
    char_pos[1] = max(char_radius, min(600 - char_radius, char_pos[1]))

    # Draw character
    pygame.draw.circle(screen, char_color, char_pos, char_radius)

    pygame.display.flip()
    clock.tick(60)

# Clean up
ser.close()
pygame.quit()
T