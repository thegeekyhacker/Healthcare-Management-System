
import sys

def get_hidden_input(prompt="Enter your secret input: "):
    hidden_input = ''
    
    if sys.platform.startswith('win'):
        import msvcrt
        
        print(prompt, end='', flush=True)
        while True:
            char = msvcrt.getch()
            char = char.decode('utf-8')

            if char == '\r':
                print('')
                return hidden_input
            elif char == '\b':
                if len(hidden_input) > 0:
                    hidden_input = hidden_input[:-1]
                    sys.stdout.write('\b \b')  # Erase character from display
                    sys.stdout.flush()
            else:
                hidden_input += char
                sys.stdout.write('*')  # Display asterisk instead of the actual character
                sys.stdout.flush()
                
    else:  # For Unix-like systems (Linux, macOS)
        import termios
        import tty
        
        print(prompt, end='', flush=True)
        try:
            # Store original terminal settings
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())

            while True:
                char = sys.stdin.read(1)

                if char == '\r' or char == '\n':
                    print('')
                    return hidden_input
                elif char == '\x7f':
                    if len(hidden_input) > 0:
                        hidden_input = hidden_input[:-1]
                        sys.stdout.write('\b \b')  # Erase character from display
                else:
                    hidden_input += char
                    sys.stdout.write('*')  # Display asterisk instead of the actual character

        finally:
            # Restore original terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

# Example usage:
# hidden_input = get_hidden_input("Enter your secret input: ")
# print("You entered:", hidden_input)
