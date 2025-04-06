import string
from collections import Counter
import matplotlib.pyplot as plt

# Частотний розподіл літер в англійській мові (%)
english_freq = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

alphabet = string.ascii_uppercase

def caesar_encrypt(text, shift):
    text = text.upper()
    encrypted = ''
    for char in text:
        if char in alphabet:
            idx = (alphabet.index(char) + shift) % 26
            encrypted += alphabet[idx]
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def frequency_analysis(text):
    filtered = [char for char in text if char in alphabet]
    total = len(filtered)
    counter = Counter(filtered)
    frequencies = {char: round((count / total) * 100, 2) for char, count in counter.items()}
    return frequencies

def guess_caesar_shift(cipher_freq):
    if not cipher_freq:
        return 0
    most_common_cipher_letter = max(cipher_freq.items(), key=lambda x: x[1])[0]
    assumed_plain_letter = 'E'  # найчастіша в англійській
    shift = (alphabet.index(most_common_cipher_letter) - alphabet.index(assumed_plain_letter)) % 26
    return shift

def plot_frequencies(cipher_freq):
    letters = list(string.ascii_uppercase)
    cipher_vals = [cipher_freq.get(char, 0) for char in letters]
    english_vals = [english_freq.get(char, 0) for char in letters]

    x = range(len(letters))
    plt.figure(figsize=(14, 6))
    plt.bar(x, english_vals, width=0.4, label='English Frequency', align='center', alpha=0.6)
    plt.bar([i + 0.4 for i in x], cipher_vals, width=0.4, label='Cipher Frequency', align='center', alpha=0.6)
    plt.xticks([i + 0.2 for i in x], letters)
    plt.xlabel("Letters")
    plt.ylabel("Frequency (%)")
    plt.title("Letter Frequency: English vs Cipher")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

# === Основна логіка ===
original_text = "The Caesar cipher is a simple encryption technique that shifts each letter by a fixed number of positions."
real_shift = 3

# Крок 1: Шифрування
encrypted_text = caesar_encrypt(original_text, real_shift)

# Крок 2: Частотний аналіз
cipher_freq = frequency_analysis(encrypted_text)

# Візуалізація
plot_frequencies(cipher_freq)

# Крок 3: Спроба відгадати зсув
guessed_shift = guess_caesar_shift(cipher_freq)
decrypted_text = caesar_decrypt(encrypted_text, guessed_shift)

# === Результати ===
print("🔐 Original text:")
print(original_text)
print("\n🔒 Encrypted text (shift=3):")
print(encrypted_text)
print("\n📊 Guessed shift based on frequency analysis:", guessed_shift)
print("\n🔓 Decrypted text with guessed shift:")
print(decrypted_text)

# Перевірка
if decrypted_text.upper() == original_text.upper():
    print("\n✅ Успішно розшифровано!")
else:
    print("\n❌ Текст не повністю збігся.")