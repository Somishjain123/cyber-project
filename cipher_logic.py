import string
import random
from collections import Counter

# Standard English letter frequency order (most common to least)
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# English Bigram Frequencies for fitness scoring
# Comprehensive table for accurate statistical analysis
BIGRAM_FREQ = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'AT': 1.49, 'EN': 1.45, 'ND': 1.35,
    'TI': 1.34, 'ES': 1.34, 'OR': 1.28, 'TE': 1.20, 'OF': 1.17,
    'ED': 1.17, 'IS': 1.13, 'IT': 1.12, 'AL': 1.09, 'AS': 1.07,
    'HA': 1.04, 'TO': 1.04, 'SE': 0.93, 'ME': 0.93, 'OU': 0.87,
    'SA': 0.86, 'NE': 0.84, 'WA': 0.83, 'DE': 0.82, 'LE': 0.82,
    'VE': 0.83, 'NO': 0.81, 'TA': 0.78, 'EC': 0.74, 'ST': 0.77,
    'SI': 0.73, 'IO': 0.73, 'AR': 0.73, 'LI': 0.68, 'RA': 0.69,
    'EA': 0.69, 'RI': 0.67, 'RO': 0.67, 'CO': 0.65, 'CE': 0.64,
    'NT': 0.67, 'HI': 0.62, 'EL': 0.62, 'MA': 0.60, 'LA': 0.59,
    'NS': 0.57, 'NG': 0.56, 'LO': 0.53, 'FO': 0.52, 'HO': 0.52,
    'PE': 0.51, 'IC': 0.51, 'UR': 0.51, 'SO': 0.51, 'OT': 0.51,
    'CA': 0.50, 'LY': 0.49, 'ON': 1.76, 'WH': 0.47, 'LL': 0.45,
    'BE': 0.43, 'OW': 0.44, 'WI': 0.44, 'US': 0.44, 'OO': 0.41,
    'SS': 0.41, 'EE': 0.38, 'AD': 0.38, 'CT': 0.37, 'UT': 0.37,
    'UN': 0.37, 'GH': 0.35, 'UL': 0.34, 'AG': 0.34, 'IF': 0.33
}

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        # Strictly handle ONLY A-Z to maintain consistency with Substitution cipher
        if 'A' <= char <= 'Z':
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        elif 'a' <= char <= 'z':
            result += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def calculate_score(text):
    """Simple frequency analysis score for English text."""
    if not text:
        return 0
    # Count only alphabetic characters
    chars = [c.upper() for c in text if c.isalpha()]
    if not chars:
        return 0
    
    counts = Counter(chars)
    # Sort chars by frequency in the given text
    text_freq_order = "".join([item[0] for item in counts.most_common()])
    
    # Compare with standard English frequency order
    score = 0
    # Add points if common English letters appear frequently
    for i, char in enumerate(text_freq_order[:6]): # Check top 6
        if char in ENGLISH_FREQ_ORDER[:10]:
            score += (6 - i)
            
    return score

def caesar_brute_force(text):
    """Tries all 26 shifts and returns results sorted by score."""
    results = []
    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        score = calculate_score(decrypted)
        results.append((shift, decrypted, score))
    
    # Sort results by score in descending order
    return sorted(results, key=lambda x: x[2], reverse=True)

def generate_substitution_key():
    """Generates a random substitution mapping for A-Z."""
    alphabet = list(string.ascii_uppercase)
    shuffled = list(string.ascii_uppercase)
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def substitution_encrypt(text, key_dict):
    result = ""
    # Create lowercase mapping as well
    lower_key = {k.lower(): v.lower() for k, v in key_dict.items()}
    
    for char in text:
        if char.isupper():
            result += key_dict.get(char, char)
        elif char.islower():
            result += lower_key.get(char, char)
        else:
            result += char
    return result

def substitution_decrypt(text, key_dict):
    """Inverts the key dictionary and performs standard sub-encryption (decryption)."""
    if not key_dict:
        return text
    # Invert the key dictionary for decryption
    inverted_key = {v: k for k, v in key_dict.items()}
    return substitution_encrypt(text, inverted_key)

def substitution_attack_solve(ciphertext):
    """
    Advanced Statistical Attack (Hill Climbing with Random Restarts).
    
    Uses bigram fitness + common English word detection for accurate
    decryption of substitution ciphers.
    
    The key mapping is cipher->plain (applied directly via _apply_key).
    """
    if not ciphertext or len(ciphertext) < 5:
        return ciphertext
    
    # Clean text for scoring (uppercase letters only)  
    clean_cipher = "".join([c.upper() for c in ciphertext if c.isalpha()])
    if not clean_cipher:
        return ciphertext

    # Preserve word boundaries for word-based scoring
    cipher_words = "".join([c.upper() if c.isalpha() else ' ' for c in ciphertext]).split()

    best_key = None
    best_fitness = -1
    
    # Multiple restarts to escape local optima
    num_restarts = 20
    iterations_per_restart = 5000
    
    for restart in range(num_restarts):
        # First restart uses frequency-based seed, rest use random
        if restart == 0:
            current_key = _generate_initial_key(ciphertext)
        else:
            letters = list(string.ascii_uppercase)
            shuffled = list(string.ascii_uppercase)
            random.shuffle(shuffled)
            current_key = dict(zip(letters, shuffled))
        
        # Score the current key
        current_fitness = _score_key(clean_cipher, cipher_words, current_key)
        
        # Hill Climbing: swap two values in the mapping each iteration
        no_improve_count = 0
        for _ in range(iterations_per_restart):
            k1, k2 = random.sample(string.ascii_uppercase, 2)
            
            trial_key = current_key.copy()
            trial_key[k1], trial_key[k2] = trial_key[k2], trial_key[k1]
            
            trial_fitness = _score_key(clean_cipher, cipher_words, trial_key)
            
            if trial_fitness > current_fitness:
                current_key = trial_key
                current_fitness = trial_fitness
                no_improve_count = 0
            else:
                no_improve_count += 1
                if no_improve_count > 1000:
                    break
        
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_key = current_key.copy()
    
    # Apply best key to original ciphertext (preserving spaces/punctuation)
    return _apply_key(ciphertext, best_key)

def _apply_key(text, key):
    """Fast application of a cipher->plain uppercase key to text, preserving case and non-alpha."""
    result = []
    for char in text:
        if char.isupper():
            result.append(key.get(char, char))
        elif char.islower():
            result.append(key.get(char.upper(), char.upper()).lower())
        else:
            result.append(char)
    return "".join(result)


# --- Common English words for scoring ---
_COMMON_WORDS = set([
    "THE", "OF", "AND", "TO", "A", "IN", "IS", "THAT", "IT", "FOR",
    "WAS", "ON", "ARE", "AS", "WITH", "HIS", "THEY", "AT", "BE", "THIS",
    "FROM", "OR", "HAD", "BY", "NOT", "BUT", "SOME", "WHAT", "THERE",
    "WE", "CAN", "OUT", "OTHER", "WERE", "ALL", "YOUR", "WHEN", "UP",
    "USE", "HOW", "SAID", "AN", "EACH", "WHICH", "DO", "THEIR", "IF",
    "WILL", "WAY", "ABOUT", "MANY", "THEN", "THEM", "WOULD", "LIKE",
    "SO", "THESE", "HER", "HAS", "HIM", "HAVE", "NO", "MORE", "MAKE",
    "COULD", "BEEN", "AFTER", "WHO", "OVER", "SUCH", "OUR", "INTO",
    "VERY", "MOST", "MAY", "ITS", "ALSO", "BACK", "WORK", "JUST",
    "ATTACK", "TEST", "SECRET", "MESSAGE", "HELLO", "WORLD", "QUICK",
    "BROWN", "FOX", "JUMPS", "OVER", "LAZY", "DOG", "FREQUENCY",
    "ANALYSIS", "SHOULD", "BEST", "LONGER", "TEXTS", "CIPHER",
    "ENCRYPTION", "SECURITY", "DATA", "NETWORK", "SYSTEM", "SOLVER"
])

def _score_key(clean_cipher, cipher_words, key):
    """
    Combined fitness score using:
    1. Bigram frequency matching (statistical patterns)
    2. Common English word detection (semantic verification)
    """
    # Fast inline decryption of uppercase-only clean_cipher
    decrypted = "".join(key.get(c, c) for c in clean_cipher)
    
    # Bigram score
    bigram_score = 0
    for i in range(len(decrypted) - 1):
        bigram = decrypted[i:i+2]
        if bigram in BIGRAM_FREQ:
            bigram_score += BIGRAM_FREQ[bigram]
    
    # Word score — apply key to each word and check against common words
    word_score = 0
    for cw in cipher_words:
        plain_word = "".join(key.get(c, c) for c in cw)
        if plain_word in _COMMON_WORDS:
            word_score += len(plain_word) ** 2
    
    # Combined score (word matches are heavily weighted)
    return bigram_score + (word_score * 5)

def _generate_initial_key(ciphertext):
    """
    Generates a cipher->plain mapping based on single-letter frequency analysis.
    Maps the most frequent ciphertext letter to 'E', second to 'T', etc.
    """
    _, sorted_counts = frequency_analysis(ciphertext)
    alphabet = string.ascii_uppercase
    mapping = {}
    
    for char in alphabet:
        mapping[char] = char
    
    for i, (cipher_char, _) in enumerate(sorted_counts):
        if i < len(ENGLISH_FREQ_ORDER):
            mapping[cipher_char] = ENGLISH_FREQ_ORDER[i]
            
    return mapping


def frequency_analysis(text):
    """Performs frequency analysis on the text."""
    # Count only alphabetic characters
    chars = [c.upper() for c in text if c.isalpha()]
    total = len(chars)
    if total == 0:
        return {}, []
        
    counts = Counter(chars)
    # Calculate percentage
    freq_pct = {char: (count / total) * 100 for char, count in counts.items()}
    
    # Get standard English frequencies for comparison (approximate percentages)
    # Ref: https://en.wikipedia.org/wiki/Letter_frequency
    english_std = {
        'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95,
        'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88,
        'C': 2.71, 'M': 2.61, 'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03,
        'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11,
        'J': 0.10, 'Z': 0.07
    }
    
    return freq_pct, sorted(counts.items(), key=lambda x: x[1], reverse=True)

def multi_shift_encrypt(text, shifts):
    """Vigenere-like repeating multi-shift Caesar cipher."""
    result = ""
    shift_len = len(shifts)
    if shift_len == 0:
        return text
        
    idx = 0
    for char in text:
        if char.isalpha():
            shift = shifts[idx % shift_len]
            if char.isupper():
                result += chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                result += chr((ord(char) - 97 + shift) % 26 + 97)
            idx += 1
        else:
            result += char
    return result

def hybrid_encrypt(text, caesar_shift, sub_key):
    """Caesar then Substitution."""
    caesar_phase = caesar_encrypt(text, caesar_shift)
    return substitution_encrypt(caesar_phase, sub_key)
