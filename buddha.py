import re
import sys

class NaturalScript:
    def __init__(self):
        self.variables = {}

    def execute(self, code):
        lines = [line.strip().lower() for line in code.split('.') if line.strip()]
        for line in lines:
            self._parse_line(line)

    def _parse_line(self, line):
        try:
            # Math operations (e.g., "add 5 and 2 and assign to i")
            math_match = re.match(
                r'^(add|subtract|multiply|divide)\s+([0-9]+)\s+and\s+([0-9]+)\s+and\s+assign\s+to\s+([a-z]+)', 
                line
            )
            if math_match:
                op, a, b, var = math_match.groups()
                a, b = int(a), int(b)
                if op == 'add':
                    self.variables[var] = a + b
                elif op == 'subtract':
                    self.variables[var] = a - b
                elif op == 'multiply':
                    self.variables[var] = a * b
                elif op == 'divide':
                    self.variables[var] = a / b
                return

            # Simple assignment (e.g., "assign 10 to x" or "assign 'hi' to msg")
            assign_match = re.match(
                r'^assign\s+([0-9]+|\"[^\"]+\")\s+to\s+([a-z]+)', 
                line
            )
            if assign_match:
                val, var = assign_match.groups()
                self.variables[var] = int(val) if val.isdigit() else val.strip('"')
                return

            # Print (e.g., "print x")
            print_match = re.match(r'^print\s+([a-z]+|\"[^\"]+\")', line)
            if print_match:
                val = print_match.group(1)
                output = (
                    self.variables.get(val, f"Error: '{val}' not found") 
                    if val in self.variables 
                    else val.strip('"')
                )
                print(output)
                return

            # If-then condition (e.g., "if x is 5 then print x")
            if_match = re.match(
                r'^if\s+([a-z]+)\s+is\s+([0-9]+)\s+then\s+print\s+([a-z]+)', 
                line
            )
            if if_match:
                var, val, print_var = if_match.groups()
                if self.variables.get(var) == int(val):
                    print(self.variables.get(print_var, f"Error: '{print_var}' not found"))
                return

            # Repeat loop (e.g., "repeat 3 times print 'hello'")
            repeat_match = re.match(
                r'^repeat\s+([0-9]+)\s+times\s+print\s+(.+)$', 
                line
            )
            if repeat_match:
                times, text = repeat_match.groups()
                for _ in range(int(times)):
                    print(text.strip('"') if text.startswith('"') else self.variables.get(text, text))
                return

            print(f"SyntaxError: Unknown command - '{line}'", file=sys.stderr)

        except Exception as e:
            print(f"RuntimeError: {e} in line '{line}'", file=sys.stderr)

def run_bd_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
        ns = NaturalScript()
        ns.execute(code)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python natural_script.py <filename.bd>")
    else:
        run_bd_file(sys.argv[1])