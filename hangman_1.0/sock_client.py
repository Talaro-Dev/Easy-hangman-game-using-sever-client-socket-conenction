import socket
import time

def client_program():
    #get server address and port
    host = socket.gethostname() 
    port = 5000  

    #create and connect to socket
    client_socket = socket.socket()  
    client_socket.connect((host, port))  

    while True:
       
        time.sleep(0.2)
        hidden_word = client_socket.recv(1024).decode()
        print(hidden_word)

        # Check for win/loss messages and break the loop if found
        if "lost" in hidden_word.lower():
            break  # Exit the loop after displaying the message

        elif "won" in hidden_word.lower():
            client_socket.close()  # Close the socket when done
            break
        else:
            # Prompt the user to guess a letter only if the game is still ongoing
            guess = input("Guess a letter: ")
            client_socket.send(guess.encode()) 

    client_socket.close()  # Close the socket when done


if __name__ == "__main__":
    client_program()
