import threading
import pygame
import socket
import random
import sys

# Global variables
bucket_x = 250
bucket_y = 450
bucket_speed = 25
game_started = False
game_over = False

# Lock for thread-safe updates
lock = threading.Lock()

def resetbucket():
    global bucket_x, bucket_y, bucket_speed
    bucket_x = 250
    bucket_y = 450
    bucket_speed = 25

def GameThread():
    global bucket_x, bucket_y, bucket_speed, game_started, game_over

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Bucket Catch Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Colors and game variables
    bucket_width, bucket_height = 100, 20
    bucket_color = (225, 69, 0)
    object_color = (173, 216, 230)
    background_color = (15, 15, 15)
    falling_objects = []
    object_speed = 3
    score = 0

    while True:
        # Wait for the game to start
        while not game_started:
            screen.fill((0, 0, 0))
            waiting_text = font.render("Waiting for client to start the game...", True, (255, 255, 255))
            screen.blit(waiting_text, (50, 200))
            pygame.display.flip()
            clock.tick(60)

        # Main game loop
        while not game_over:
            screen.fill(background_color)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update bucket position
            with lock:
                bucket_rect = pygame.Rect(bucket_x, bucket_y, bucket_width, bucket_height)
                bucket_x = max(0, min(600 - bucket_width, bucket_x))
                bucket_y = max(0, min(500 - bucket_height, bucket_y))

            # Generate falling objects
            if random.randint(1, 50) == 1:
                obj_x = random.randint(0, 600 - 20)
                falling_objects.append(pygame.Rect(obj_x, 0, 20, 20))

            # Update falling objects
            for obj in falling_objects[:]:
                obj.y += object_speed
                if obj.colliderect(bucket_rect):
                    falling_objects.remove(obj)
                    score += 1
                elif obj.y > 500:
                    game_over = True
                    break

            # Draw bucket and objects
            pygame.draw.rect(screen, bucket_color, bucket_rect)
            for obj in falling_objects:
                pygame.draw.rect(screen, object_color, obj)

            # Display score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Adjust speeds
            object_speed = 3 + score // 10
            bucket_speed = 25 + score // 10

            pygame.display.flip()
            clock.tick(60)

        # Game over screen
        while game_over:
            screen.fill((0, 0, 0))
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            restart_text = font.render("Press 'r' to Restart or 'q' to Quit.", True, (255, 255, 255))
            screen.blit(game_over_text, (200, 200))
            screen.blit(final_score_text, (200, 250))
            screen.blit(restart_text, (50, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        resetbucket()
                        game_started = True
                        game_over = False
                        falling_objects.clear()
                        score = 0
                        break
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

def ServerThread():
    global bucket_x, bucket_y, bucket_speed, game_started, game_over

    host = socket.gethostbyname(socket.gethostname())
    port = 5000

    print(f"Server IP: {host}:{port}")

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server started, waiting for client connection...")
    conn, addr = server_socket.accept()
    print(f"Client connected: {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                print("No data received. Closing connection.")
                break

            if data == "start":
                game_started = True
                print("Game Started.")
            elif data == "restart":
                resetbucket()
                game_started = True
                print(game_started)
                game_over = False
                print(game_over)
                print("Game restarting...")
            elif data == "quit":
                print("Client requested to quit.")
                break
            elif data in ['w', 'a', 's', 'd']:
                with lock:
                    if data == 'w':
                        bucket_y -= bucket_speed
                    elif data == 's':
                        bucket_y += bucket_speed
                    elif data == 'a':
                        bucket_x -= bucket_speed
                    elif data == 'd':
                        bucket_x += bucket_speed
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    threading.Thread(target=ServerThread, daemon=True).start()
    GameThread()
