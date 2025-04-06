import string
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# --- Частотний розподіл англійських літер (%)
english_freq = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# --- Шифрування / дешифрування Віженера ---
def vigenere_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = ''
    key_idx = 0
    for char in text:
        if char in string.ascii_uppercase:
            shift = ord(key[key_idx % len(key)]) - ord('A')
            result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            key_idx += 1
        else:
            result += char
    return result

def vigenere_decrypt(cipher, key):
    key = key.upper()
    result = ''
    key_idx = 0
    for char in cipher:
        if char in string.ascii_uppercase:
            shift = ord(key[key_idx % len(key)]) - ord('A')
            result += chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            key_idx += 1
        else:
            result += char
    return result

# --- Частотний аналіз ---
def frequency_analysis(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    counter = Counter(text)
    total = sum(counter.values())
    return {char: round((count / total) * 100, 2) for char, count in counter.items()}

def plot_frequencies(freq_dict, title="Frequency"):
    letters = string.ascii_uppercase
    values = [freq_dict.get(ch, 0) for ch in letters]
    plt.figure(figsize=(12, 5))
    plt.bar(letters, values)
    plt.xlabel("Letters")
    plt.ylabel("Frequency (%)")
    plt.title(title)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")

# --- Метод Касіскі ---
def kasiski_examination(cipher, min_len=3):
    repeated = {}
    for i in range(len(cipher) - min_len):
        seq = cipher[i:i+min_len]
        for j in range(i + min_len, len(cipher) - min_len):
            if cipher[j:j+min_len] == seq:
                distance = j - i
                repeated.setdefault(seq, []).append(distance)
    return repeated

def find_factors(distances):
    factors = Counter()
    for d in distances:
        for f in range(2, 21):
            if d % f == 0:
                factors[f] += 1
    return factors

# --- Тест Фрідмана ---
def friedman_test(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    N = len(text)
    freqs = Counter(text)
    IC = sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1)) if N > 1 else 0
    K = 0.0265
    r = 1 / 26
    if IC == 0:
        return 0
    return round((K * N) / ((IC * (N - 1)) - r * N + K), 2)

# --- Розбиття тексту по стовпцях ---
def split_segments(text, key_len):
    segments = ['' for _ in range(key_len)]
    for i, char in enumerate(text):
        segments[i % key_len] += char
    return segments

def analyze_segments(cipher_text, estimated_key_len):
    print(f"\n🔍 Частотний аналіз для кожного з {estimated_key_len} сегментів:")
    segments = split_segments(cipher_text, estimated_key_len)
    for idx, segment in enumerate(segments):
        freqs = frequency_analysis(segment)
        print(f"\n📎 Сегмент {idx + 1}:")
        df = pd.DataFrame.from_dict(freqs, orient='index', columns=['Frequency (%)'])
        print(df.sort_values('Frequency (%)', ascending=False))

# --- Визначення ключа через частотний збіг ---
def caesar_decrypt(segment, shift):
    result = ''
    for char in segment:
        if char in string.ascii_uppercase:
            result += chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
    return result

def chi_squared_score(segment_freq):
    score = 0
    for letter in string.ascii_uppercase:
        observed = segment_freq.get(letter, 0)
        expected = english_freq.get(letter, 0)
        score += ((observed - expected) ** 2) / expected if expected > 0 else 0
    return score

def guess_shift_for_segment(segment):
    scores = []
    for shift in range(26):
        decrypted = caesar_decrypt(segment, shift)
        freq = frequency_analysis(decrypted)
        score = chi_squared_score(freq)
        scores.append((shift, score))
    return min(scores, key=lambda x: x[1])  # найкращий зсув

def auto_recover_key(cipher_text, max_key_len=6):
    print(f"\n🧠 Guessed key length (Friedman): {friedman_test(cipher_text)}\n")
    best_score = float('inf')
    best_key = ''

    for key_len in range(2, max_key_len + 1):
        print(f"[+] Trying key length: {key_len}")
        segments = split_segments(cipher_text, key_len)
        key = ''
        total_score = 0

        for idx, segment in enumerate(segments):
            shift, score = guess_shift_for_segment(segment)
            key_char = string.ascii_uppercase[shift]
            key += key_char
            total_score += score
            print(f"[-] Column {idx}: Guessed shift = {shift} ({key_char})")

        print(f"[-] Candidate key: {key}, English Score: {round(total_score, 2)}\n")

        if total_score < best_score:
            best_score = total_score
            best_key = key

    print(f"[✓] Best guessed key: {best_key} with score: {round(best_score, 2)}")
    return best_key

# === Основна програма ===
original_text = "Vigenere cipher is a method of encrypting alphabetic text using a series of interwoven Caesar ciphers."
key = "KEY"
clean_text = ''.join(filter(str.isalpha, original_text.upper()))

# Шифрування
cipher_text = vigenere_encrypt(original_text, key)
filtered_cipher = ''.join(filter(str.isalpha, cipher_text.upper()))

# Частотний аналіз
freqs = frequency_analysis(filtered_cipher)
plot_frequencies(freqs, title="Vigenère Cipher Frequency Analysis")

# Касіскі
repeats = kasiski_examination(filtered_cipher, min_len=3)
distances = [dist for group in repeats.values() for dist in group]
factors = find_factors(distances)

# Вивід Касіскі та Фрідмана
print("\n🔐 Original:", original_text)
print("\n🔒 Cipher:", cipher_text)
print("\n🧠 Kasiski factors (likely key lengths):", factors.most_common(5))
friedman_len = friedman_test(filtered_cipher)
print("📏 Friedman estimated key length:", friedman_len)

# Частотний аналіз по сегментах
likely_key_len = factors.most_common(1)[0][0] if factors else round(friedman_len)
analyze_segments(filtered_cipher, likely_key_len)

# Автоматичне відновлення ключа
recovered_key = auto_recover_key(filtered_cipher, max_key_len=6)

# Перевірка розшифрування
decrypted = vigenere_decrypt(cipher_text, recovered_key)
match = ''.join(filter(str.isalpha, decrypted.upper())) == clean_text
print("\n🔓 Decrypted with key:", decrypted)
print("✅ Match:", match)