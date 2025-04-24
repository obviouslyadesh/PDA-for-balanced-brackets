from typing import List, Tuple

class PDAMachine:
    def __init__(self):
        self.stack = []
        self.transitions = []
        self.pairs = {')': '(', ']': '[', '}': '{'}

    def reset(self):
        self.stack = []
        self.transitions = []

    def validate(self, input_str: str) -> bool:
        self.reset()
        for char in input_str:
            if char in '({[':
                self.stack.append(char)
                self.transitions.append((char, list(self.stack)))
            elif char in ')}]':
                if not self.stack or self.stack[-1] != self.pairs[char]:
                    self.transitions.append((char, list(self.stack)))
                    return False
                self.stack.pop()
                self.transitions.append((char, list(self.stack)))
            else:
                return False
        return len(self.stack) == 0

    def get_trace(self) -> List[Tuple[str, List[str]]]:
        return self.transitions

class PalindromePDA:
    def __init__(self):
        self.stack = []
        self.transitions = []

    def validate(self, input_str: str) -> bool:
        self.stack.clear()
        self.transitions.clear()
        n = len(input_str)
        for i in range(n // 2):
            self.stack.append(input_str[i])
            self.transitions.append((input_str[i], list(self.stack)))
        for i in range((n + 1) // 2, n):
            if not self.stack or self.stack.pop() != input_str[i]:
                self.transitions.append((input_str[i], list(self.stack)))
                return False
            self.transitions.append((input_str[i], list(self.stack)))
        return len(self.stack) == 0

    def get_trace(self):
        return self.transitions

import re

class ArithmeticPDA:
    def __init__(self):
        self.stack = []
        self.transitions = []

    def validate(self, input_str: str) -> bool:
        self.stack.clear()
        self.transitions.clear()
        bracket_pairs = {')': '(', ']': '[', '}': '{'}

        # Trim leading/trailing spaces for initial checks
        trimmed_input = input_str.strip()
        if not trimmed_input:
            return True  # Empty string is considered valid for now

        # Check if the expression starts or ends with an operator 
        if re.match(r'^[\+\*\/\%\^]', trimmed_input) or re.search(r'[\+\*\/\%\^]$', trimmed_input):
            self.transitions.append(("Invalid Operator Placement", list(self.stack)))
            return False

        for i, char in enumerate(input_str):
            if char in '([{':
                self.stack.append(char)
            elif char in ')]}':
                if not self.stack or self.stack[-1] != bracket_pairs[char]:
                    self.transitions.append((char, list(self.stack)))
                    return False
                self.stack.pop()
            elif not char.isalnum() and char not in '+-*/%^ ':
                self.transitions.append((char, list(self.stack)))
                return False  # Invalid character
            self.transitions.append((char, list(self.stack)))

            # Basic check for consecutive operators 
            if i > 0 and char in '+-*/%^' and input_str[i-1] in '+-*/%^':
                return False

        if self.stack:
            return False

        return True

    def get_trace(self):
        return self.transitions
