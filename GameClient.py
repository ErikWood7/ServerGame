import socket
import keyboard
import time

def client_program():
    print("Connecting to server...")
    host = "127.0.0.1"  # Server IP
    port = 5000

    client_socket = socket.socket()
    try:
        client_socket.connect((host, port))
        print("Connected to the server.")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    print("Press SPACE to start the game.")
    print("Use 'w', 'a', 's', 'd' to move the bucket. Press 'v' to restart or 'q' to quit.")

    try:
        while True:
            try:
                # Check for inputs
                if keyboard.is_pressed('space'):
                    client_socket.send('start'.encode())
                    print("Sent: start")
                    time.sleep(0.5)

                if keyboard.is_pressed('w'):
                    client_socket.send('w'.encode())
                    time.sleep(0.1)
                if keyboard.is_pressed('s'):
                    client_socket.send('s'.encode())
                    time.sleep(0.1)
                if keyboard.is_pressed('a'):
                    client_socket.send('a'.encode())
                    time.sleep(0.1)
                if keyboard.is_pressed('d'):
                    client_socket.send('d'.encode())
                    time.sleep(0.1)

                if keyboard.is_pressed('v'):
                    client_socket.send('restart'.encode())
                    print("Sent: restart")
                    time.sleep(0.5)

                if keyboard.is_pressed('q'):
                    client_socket.send('quit'.encode())
                    print("Sent: quit")
                    break

            except ConnectionResetError:
                print("Connection lost. The server closed the connection.")
                break
            except BrokenPipeError:
                print("The connection to the server was broken.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    client_program()
