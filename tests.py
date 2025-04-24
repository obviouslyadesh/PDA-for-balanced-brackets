from pda_classes import PDAMachine, PalindromePDA, ArithmeticPDA

def run_tests():
    results = []

    # --- Bracket Validator Tests ---
    bracket = PDAMachine()
    results.append(("Bracket Validator", "([]{})", True, bracket.validate("([]{})")))
    results.append(("Bracket Validator", "([)]", False, bracket.validate("([)]")))
    results.append(("Bracket Validator", "{[(])}", False, bracket.validate("{[(])}")))
    results.append(("Bracket Validator", "", True, bracket.validate("")))
    results.append(("Bracket Validator", "([{}]){}", True, bracket.validate("([{}]){}")))
    results.append(("Bracket Validator", "((({{{[[[]]]}}})))", True, bracket.validate("((({{{[[[]]]}}})))")))
    results.append(("Bracket Validator", "([{}])", True, bracket.validate("([{}])")))
    results.append(("Bracket Validator", "]", False, bracket.validate("]")))
    results.append(("Bracket Validator", "[", False, bracket.validate("[")))
    results.append(("Bracket Validator", "}{", False, bracket.validate("}{")))
    results.append(("Bracket Validator", "(()", False, bracket.validate("(()")))
    results.append(("Bracket Validator", "))", False, bracket.validate("))")))
    results.append(("Bracket Validator", "([", False, bracket.validate("([")))
    results.append(("Bracket Validator", "(}", False, bracket.validate("(}")))
    results.append(("Bracket Validator", "[)", False, bracket.validate("[)")))
    results.append(("Bracket Validator", "{]", False, bracket.validate("{]")))

    # --- Palindrome Checker Tests ---
    palindrome = PalindromePDA()
    results.append(("Palindrome Checker", "racecar", True, palindrome.validate("racecar")))
    results.append(("Palindrome Checker", "madam", True, palindrome.validate("madam")))
    results.append(("Palindrome Checker", "a", True, palindrome.validate("a")))
    results.append(("Palindrome Checker", "", True, palindrome.validate("")))
    results.append(("Palindrome Checker", "hello", False, palindrome.validate("hello")))
    results.append(("Palindrome Checker", "racer", False, palindrome.validate("racer")))
    results.append(("Palindrome Checker", "aba", True, palindrome.validate("aba")))
    results.append(("Palindrome Checker", "abba", True, palindrome.validate("abba")))
    results.append(("Palindrome Checker", "abc", False, palindrome.validate("abc")))
    results.append(("Palindrome Checker", "abca", False, palindrome.validate("abca")))
    results.append(("Palindrome Checker", "level", True, palindrome.validate("level")))
    results.append(("Palindrome Checker", "rotor", True, palindrome.validate("rotor")))
    results.append(("Palindrome Checker", "stats", True, palindrome.validate("stats")))
    results.append(("Palindrome Checker", "deified", True, palindrome.validate("deified")))
    results.append(("Palindrome Checker", "reviver", True, palindrome.validate("reviver")))

    # --- Arithmetic Expression Validator Tests ---
    arithmetic = ArithmeticPDA()
    results.append(("Arithmetic Validator", "(3+2)*4", True, arithmetic.validate("(3+2)*4")))
    results.append(("Arithmetic Validator", "((1+2)*3)", True, arithmetic.validate("((1+2)*3)")))
    results.append(("Arithmetic Validator", "a+b*(c-d)", True, arithmetic.validate("a+b*(c-d)")))
    results.append(("Arithmetic Validator", "((3+2]*4", False, arithmetic.validate("((3+2]*4")))
    results.append(("Arithmetic Validator", "3++2", False, arithmetic.validate("3++2")))
    results.append(("Arithmetic Validator", "a+@*b", False, arithmetic.validate("a+@*b")))
    results.append(("Arithmetic Validator", "3+4$", False, arithmetic.validate("3+4$")))
    results.append(("Arithmetic Validator", ")3+2(", False, arithmetic.validate(")3+2(")))
    results.append(("Arithmetic Validator", "3+*", False, arithmetic.validate("3+*")))
    results.append(("Arithmetic Validator", "*3+2", False, arithmetic.validate("*3+2")))
    results.append(("Arithmetic Validator", "3 + 2", True, arithmetic.validate("3 + 2")))
    results.append(("Arithmetic Validator", "( )", True, arithmetic.validate("( )"))) 
    results.append(("Arithmetic Validator", "[ ]", True, arithmetic.validate("[ ]"))) 
    results.append(("Arithmetic Validator", "{ }", True, arithmetic.validate("{ }"))) 
    results.append(("Arithmetic Validator", "a", True, arithmetic.validate("a"))) 
    results.append(("Arithmetic Validator", "123", True, arithmetic.validate("123"))) 
    results.append(("Arithmetic Validator", "3 % 2", True, arithmetic.validate("3 % 2"))) 
    results.append(("Arithmetic Validator", "2 ^ 3", True, arithmetic.validate("2 ^ 3"))) 
    results.append(("Arithmetic Validator", "++3", False, arithmetic.validate("++3"))) 
    results.append(("Arithmetic Validator", "3--", False, arithmetic.validate("3--"))) 
    results.append(("Arithmetic Validator", ")(", False, arithmetic.validate(")("))) 
    results.append(("Arithmetic Validator", "[(])", False, arithmetic.validate("[(])"))) 

    return results

if __name__ == "__main__":
    test_results = run_tests()
    for test_name, input_str, expected, actual in test_results:
        result_text = "✅ Passed" if expected == actual else "❌ Failed"
        print(f"**{test_name}** - Input: `{input_str}`")
        print(f"- Expected: `{expected}`")
        print(f"- Got: `{actual}`")
        print(f"- Result: **{result_text}**")
        print("-" * 20)