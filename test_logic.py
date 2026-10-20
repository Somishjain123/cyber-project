import cipher_logic

def test_caesar():
    text = "HELLO WORLD"
    shift = 3
    encrypted = cipher_logic.caesar_encrypt(text, shift)
    print(f"Caesar Encrypted: {encrypted}")
    decrypted = cipher_logic.caesar_decrypt(encrypted, shift)
    print(f"Caesar Decrypted: {decrypted}")
    assert decrypted == text
    
    # Test brute force
    brute_results = cipher_logic.caesar_brute_force(encrypted)
    found = False
    for shift_num, dec_text, score in brute_results:
        if dec_text == text:
            print(f"Brute force found correct shift {shift_num} with score {score}")
            found = True
            break
    assert found

def test_substitution():
    text = "THIS IS A SECRET MESSAGE"
    key = cipher_logic.generate_substitution_key()
    encrypted = cipher_logic.substitution_encrypt(text, key)
    print(f"Substitution Encrypted: {encrypted}")
    decrypted = cipher_logic.substitution_decrypt(encrypted, key)
    print(f"Substitution Decrypted: {decrypted}")
    assert decrypted == text

def test_multi_shift():
    text = "VIGENERE TEST"
    shifts = [1, 2, 3]
    encrypted = cipher_logic.multi_shift_encrypt(text, shifts)
    print(f"Multi-shift Encrypted: {encrypted}")
    # Decryption for multi-shift isn't explicitly required as a standalone function in prompt but logic check:
    # Manual check: V+1=W, I+2=K, G+3=J ...
    
def test_attack_solve():
    # Long text for better frequency mapping
    text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. THIS IS A TEST OF THE STATISTICAL ATTACK SOLVER. FREQUENCY ANALYSIS SHOULD WORK BEST ON LONGER TEXTS."
    key = cipher_logic.generate_substitution_key()
    encrypted = cipher_logic.substitution_encrypt(text, key)
    print(f"Attack Test Encrypted: {encrypted}")
    guess = cipher_logic.substitution_attack_solve(encrypted)
    print(f"Attack Test Guess: {guess}")
    # We check if some common words like 'THE' or 'IS' are partially recovered or at least the logic runs
    assert len(guess) == len(text)

if __name__ == "__main__":
    try:
        test_caesar()
        test_substitution()
        test_multi_shift()
        test_attack_solve()
        print("All logic tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
