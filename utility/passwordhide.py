
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
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                hidden_input += char
                sys.stdout.write('*')
                sys.stdout.flush()

    else:
        import termios
        import tty

        print(prompt, end='', flush=True)
        try:
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
                        sys.stdout.write('\b \b')
                else:
                    hidden_input += char
                    sys.stdout.write('*')

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
