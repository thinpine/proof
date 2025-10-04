import time
import sys

# --- 1. Data Structure Definitions ---

# International Morse Code Mapping (Used for both building the Trie and for Encoding)
MORSE_MAP = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..-..', '/': '-..-.'
}


class MorseNode:
    """A node in the Morse Code Trie (Binary Tree)."""
    def __init__(self, char=None):
        # The character stored at this node (None for intermediate nodes)
        self.char = char
        # Reference for a Dot (Dit) traversal
        self.dot_child = None
        # Reference for a Dash (Dah) traversal
        self.dash_child = None


class MorseTrie:
    """Manages the Morse Code Binary Tree structure."""
    def __init__(self):
        # The root is the starting point for all code sequences
        self.root = MorseNode()
        # Build the tree upon initialization
        self.build_trie()

    def build_trie(self):
        """
        Builds the entire Morse code tree by traversing from the root
        based on the dits and dahs in the MORSE_MAP.
        """
        for char, code in MORSE_MAP.items():
            current_node = self.root
            for symbol in code:
                if symbol == '.':
                    # If dot child doesn't exist, create it
                    if current_node.dot_child is None:
                        current_node.dot_child = MorseNode()
                    current_node = current_node.dot_child
                elif symbol == '-':
                    # If dash child doesn't exist, create it
                    if current_node.dash_child is None:
                        current_node.dash_child = MorseNode()
                    current_node = current_node.dash_child

            # After traversing the full code, assign the character to the final node
            current_node.char = char

    def decode(self, morse_message):
        """
        Decodes a Morse code string back into English text using the Trie structure.

        Args:
            morse_message (str): The Morse code string, with characters separated by
                                 single spaces (' ') and words by triple spaces ('   ').

        Returns:
            str: The decoded message.
        """
        decoded_text = []

        # 1. Standardize word separation (replace triple space with a unique marker)
        # We use a single space for character separation, and two extra spaces for word separation.
        # Morse standard dictates 7 unit spaces between words, which is often represented
        # as a large gap. Here we use ' / ' as a cleaner word separator for user input.
        # The split handles any sequence of spaces greater than 1 as a word break.
        words = morse_message.strip().split('   ') # Use triple space to split words

        for word_morse in words:
            # 2. Split words into individual character codes (separated by single space)
            char_codes = word_morse.split(' ')
            decoded_word = []

            for code in char_codes:
                if not code:
                    continue  # Skip empty strings resulting from multiple spaces

                current_node = self.root

                # 3. Traverse the Trie based on the code sequence
                for symbol in code:
                    if symbol == '.':
                        current_node = current_node.dot_child
                    elif symbol == '-':
                        current_node = current_node.dash_child
                    else:
                        # Should not happen with clean input
                        print(f"Error: Invalid Morse symbol '{symbol}' in code '{code}'", file=sys.stderr)
                        current_node = None
                        break

                # 4. Extract the character from the final node
                if current_node and current_node.char:
                    decoded_word.append(current_node.char)
                else:
                    decoded_word.append('?') # Use '?' for unknown/invalid sequence

            decoded_text.append("".join(decoded_word))

        return " ".join(decoded_text)

# --- 2. Encoding Logic (Simpler, uses the map directly) ---

def encode(text):
    """
    Encodes English text to Morse code.

    Args:
        text (str): The English input string.

    Returns:
        str: The encoded Morse code string.
    """
    encoded_parts = []

    # Pre-process the text: convert to uppercase, handle unrecognized characters
    text = text.upper()

    for word in text.split():
        morse_word = []
        for char in word:
            if char in MORSE_MAP:
                # Characters are separated by a single space
                morse_word.append(MORSE_MAP[char])
            else:
                # Handle characters not in the map (e.g., special symbols)
                morse_word.append('###')

        # Join characters with a single space, then append to the list
        encoded_parts.append(" ".join(morse_word))

    # Words are separated by a triple space ('   ') to conform to the decoding logic
    return "   ".join(encoded_parts)


def display_morse_timing_simulation(morse_code, wpm=15):
    """
    Simulates the time-based transmission of the Morse code.

    This is based on the mathematical principle:
    One unit (dot duration) = 60 / (50 * WPM) seconds.
    A simple terminal beep is used to simulate the sound.
    """
    if not morse_code.strip():
        print("No code to transmit.", file=sys.stderr)
        return

    # Mathematical calculation for timing (WPM based on 'PARIS' = 50 units)
    try:
        unit_time = 60 / (50 * wpm)
    except ZeroDivisionError:
        unit_time = 0.1 # Default if WPM is 0

    dot_duration = unit_time
    dash_duration = unit_time * 3

    print(f"\n--- Simulating Transmission at {wpm} WPM (Unit Time: {dot_duration:.3f}s) ---")

    # Replace triple spaces with a word separator and single spaces with a character separator
    display_code = morse_code.replace('   ', ' | ')

    for symbol in display_code:
        if symbol == '.':
            # Beep for the duration of a dot
            sys.stdout.write('\a') # Terminal beep (may not work on all systems)
            print('.', end='', flush=True)
            time.sleep(dot_duration)
            # Intra-character space (1 unit)
            time.sleep(unit_time)
        elif symbol == '-':
            # Beep for the duration of a dash
            sys.stdout.write('\a')
            print('-', end='', flush=True)
            time.sleep(dash_duration)
            # Intra-character space (1 unit)
            time.sleep(unit_time)
        elif symbol == ' ':
            # Inter-character space (3 units total, 1 unit already covered by previous symbol's space)
            print(' ', end='', flush=True)
            time.sleep(unit_time * 2)
        elif symbol == '|':
            # Inter-word space (7 units total, 1 unit covered, 2 units covered by ' ')
            print(' | ', end='', flush=True)
            time.sleep(unit_time * 4)
        else:
            print(symbol, end='', flush=True)

    print("\n--- Transmission Complete ---")


# --- 3. User Interface ---

def main():
    """Main function to run the interactive Morse Code Translator."""
    print("--- Morse Code Translator using Trie Structure ---")

    try:
        # Initialize the Trie structure (builds the tree)
        trie = MorseTrie()
    except Exception as e:
        print(f"Failed to initialize MorseTrie: {e}", file=sys.stderr)
        return

    while True:
        print("\nWhat would you like to do?")
        print("  [1] Encrypt Text to Morse Code")
        print("  [2] Decrypt Morse Code to Text (Uses Trie/Binary Tree)")
        print("  [3] Exit")

        choice = input("Enter choice (1, 2, or 3): ").strip()

        if choice == '1':
            text = input("Enter English text to encrypt: ").strip()
            if text:
                morse_result = encode(text)
                print(f"\n[ENCODED MORSE]: {morse_result}")

                try:
                    wpm_speed = int(input("Enter WPM speed for simulation (e.g., 15): "))
                    display_morse_timing_simulation(morse_result, wpm_speed)
                except ValueError:
                    print("Invalid speed entered. Skipping simulation.")
            else:
                print("No text provided.")

        elif choice == '2':
            print("\n[INPUT FORMAT]: Separate characters with a single space (e.g., .-- .),")
            print("                 and words with triple spaces (e.g., .-- .   -.--)")
            morse_input = input("Enter Morse code to decrypt: ").strip()
            if morse_input:
                try:
                    text_result = trie.decode(morse_input)
                    print(f"\n[DECODED TEXT]: {text_result}")
                except Exception as e:
                    print(f"An error occurred during decoding: {e}", file=sys.stderr)
            else:
                print("No Morse code provided.")

        elif choice == '3':
            print("Exiting translator. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Execute the main function
if __name__ == '__main__':
    # Increase recursion limit slightly for safety, although the trie depth is low
    sys.setrecursionlimit(2000)
    main()