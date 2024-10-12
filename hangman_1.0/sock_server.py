import socket
import random

def server_program():
    #get the server address and port
    host = socket.gethostname()  
    port = 5000  

    #get and bind the socket
    server_socket = socket.socket()  
    server_socket.bind((host, port))  

    words = hangman_init()  # Initialize the word list

    server_socket.listen(2)  
    conn, address = server_socket.accept()  # Accept  connections
    print("Connection from: " + str(address))
    hangman_game(conn, address, words)

    conn.close()  # Close the connection

def hangman_init():
    # Read words from a file
    with open("word.txt", "r") as my_file:
        words = my_file.read().splitlines()
    return words

def hangman_game(conn, address, words):
    word = random.choice(words)
    print("Chosen word:", word)  # For debugging purposes

    hidden_word = create_word(word)  # Create the hidden word representation
    tries = 5

    conn.send(("Current word: %s" % hidden_word).encode())  

    while tries > 0:
        data = conn.recv(1024).decode()  
        if not data:
            break

        if data in word:
            # Reveal the correctly guessed letter(s) in the hidden word
            hidden_word = reveal_letters(word, hidden_word, data)
            conn.send(("Current word: %s" % hidden_word).encode())  

            if "_" not in hidden_word:  # Check if the word has been fully guessed
                conn.send("\nYou won!".encode())
                break  # Exit the loop immediately after winning
        else:
            tries -= 1
            if tries == 0:
                conn.send(("You lost! The word was %s" % word).encode())
                break  # Exit after loss
            else:
                conn.send(("Wrong answer, you have %d tries left" % tries).encode())

def create_word(word):
    # Create a string with the first and last character and underscores in between
    return word[0] + '_' * (len(word) - 2) + word[-1]

def reveal_letters(word, hidden_word, guess):
    # Reveals the guessed letters in the hidden word
    hidden_word_list = list(hidden_word)  # Convert to a list for mutability
    for i in range(len(word)):
        if word[i] == guess:
            hidden_word_list[i] = guess  # Reveal the letter in the hidden word
    return "".join(hidden_word_list)  # Return the updated hidden word as a string

if __name__ == '__main__':
    server_program()
