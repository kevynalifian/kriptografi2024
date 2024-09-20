import math
import tkinter as tk
from tkinter import filedialog

def vigenere_cipher(text, key, encrypt=True):
    result = []
    text = text.upper()
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            if encrypt:
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

def playfair_cipher(text, key, encrypt=True):
    text = ''.join(filter(str.isalpha, text)).upper()
    key = ''.join(filter(str.isalpha, key)).upper()
    key += 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key = ''.join(sorted(set(key), key=key.index))

    matrix = [[None] * 5 for _ in range(5)]
    used = set()
    index = 0
    for char in key:
        if char not in used:
            if char == 'J':
                char = 'I'
            matrix[index // 5][index % 5] = char
            used.add(char)
            index += 1
            if index >= 25:
                break

    digraphs = prepare_digraphs(text)
    result = []

    for a, b in digraphs:
        posA = find_position(matrix, a)
        posB = find_position(matrix, b)

        if posA[0] == posB[0]:  # Same row
            result.append(matrix[posA[0]][(posA[1] + (1 if encrypt else 4)) % 5])
            result.append(matrix[posB[0]][(posB[1] + (1 if encrypt else 4)) % 5])
        elif posA[1] == posB[1]:  # Same column
            result.append(matrix[(posA[0] + (1 if encrypt else 4)) % 5][posA[1]])
            result.append(matrix[(posB[0] + (1 if encrypt else 4)) % 5][posB[1]])
        else:  # Rectangle
            result.append(matrix[posA[0]][posB[1]])
            result.append(matrix[posB[0]][posA[1]])

    return ''.join(result)

def prepare_digraphs(text):
    digraphs = []
    i = 0
    while i < len(text):
        if i == len(text) - 1:
            digraphs.append((text[i], 'X'))
            break
        elif text[i] == text[i + 1]:
            digraphs.append((text[i], 'X'))
            i += 1
        else:
            digraphs.append((text[i], text[i + 1]))
            i += 2
    return digraphs

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return (i, j)
    return (-1, -1)

def hill_cipher(text, key, encrypt=True):
    text = ''.join(filter(str.isalpha, text)).upper()
    key = ''.join(filter(str.isalpha, key)).upper()
    
    key_size = int(math.sqrt(len(key)))
    if key_size * key_size != len(key):
        raise ValueError("Length of key must be a perfect square.")

    key_matrix = [[ord(key[i * key_size + j]) - ord('A') for j in range(key_size)] for i in range(key_size)]
    while len(text) % key_size != 0:
        text += 'X'

    result = []
    for i in range(0, len(text), key_size):
        vector = [ord(text[i + j]) - ord('A') for j in range(key_size)]
        encrypted = [0] * key_size
        for row in range(key_size):
            for col in range(key_size):
                encrypted[row] += key_matrix[row][col] * vector[col]
            result.append(chr((encrypted[row] % 26) + ord('A')))
    
    return ''.join(result)

def perform_cipher(text, key, choice, encrypt):
    if choice == 1:
        result = vigenere_cipher(text, key, encrypt)
    elif choice == 2:
        result = playfair_cipher(text, key, encrypt)
    elif choice == 3:
        result = hill_cipher(text, key, encrypt)
    else:
        result = "Invalid choice!"
    return result

def encrypt_decrypt():
    text = text_entry.get()
    key = key_entry.get()
    choice = int(choice_var.get())
    encrypt = encrypt_var.get() == 1
    result = perform_cipher(text, key, choice, encrypt)
    result_label.config(text=result)

def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            data = file.read()
            text_entry.delete(0, tk.END)
            text_entry.insert(tk.END, data)

# Create the main window
window = tk.Tk()
window.title("Kriptografi Kevyn Alifian")

# Create labels and entry fields
text_label = tk.Label(window, text="Enter text:")
text_entry = tk.Entry(window, width=50)
key_label = tk.Label(window, text="Enter key:")
key_entry = tk.Entry(window, width=50)
choice_label = tk.Label(window, text="Choose cipher:")
choice_var = tk.IntVar()
choice_radio1 = tk.Radiobutton(window, text="Vigenere", variable=choice_var, value=1)
choice_radio2 = tk.Radiobutton(window, text="Playfair", variable=choice_var, value=2)
choice_radio3 = tk.Radiobutton(window, text="Hill", variable=choice_var, value=3)
encrypt_label = tk.Label(window, text="Operation:")
encrypt_var = tk.IntVar()
encrypt_radio1 = tk.Radiobutton(window, text="Encrypt", variable=encrypt_var, value=1)
encrypt_radio2 = tk.Radiobutton(window, text="Decrypt", variable=encrypt_var, value=0)
result_label = tk.Label(window, text="")

# Place widgets
text_label.grid(row=0, column=0)
text_entry.grid(row=0, column=1)
key_label.grid(row=1, column=0)
key_entry.grid(row=1, column=1)
choice_label.grid(row=2, column=0)
choice_radio1.grid(row=2, column=1)
choice_radio2.grid(row=3, column=1)
choice_radio3.grid(row=4, column=1)
encrypt_label.grid(row=5, column=0)
encrypt_radio1.grid(row=5, column=1)
encrypt_radio2.grid(row=6, column=1)
result_label.grid(row=7, column=0, columnspan=2)

# Create a button to load file
load_button = tk.Button(window, text="Load File", command=load_file)
load_button.grid(row=8, column=0)

# Create a button to trigger the encryption/decryption
encrypt_button = tk.Button(window, text="ACTION", command=encrypt_decrypt)
encrypt_button.grid(row=8, column=1)

# Start the GUI
window.mainloop()
