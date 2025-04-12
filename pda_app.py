import streamlit as st
from typing import List, Tuple
from graphviz import Digraph
from streamlit_agraph import agraph, Node, Edge, Config

# PDA Machine to validate balanced brackets
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

# Function to visualize PDA transitions as a graph (Graphviz)
def draw_pda_trace(transitions: List[Tuple[str, List[str]]]) -> Digraph:
    dot = Digraph()
    for i, (symbol, stack) in enumerate(transitions):
        dot.node(str(i), f"{symbol}\nStack: {''.join(stack) if stack else 'Empty'}")
        if i > 0:
            dot.edge(str(i - 1), str(i))
    return dot

# Function to animate PDA trace using streamlit-agraph
def animate_pda_trace(transitions: List[Tuple[str, List[str]]]):
    nodes = []
    edges = []
    for i, (symbol, stack) in enumerate(transitions):
        label = f"{symbol} | Stack: {''.join(stack) if stack else 'Empty'}"
        nodes.append(Node(id=str(i), label=label))
        if i > 0:
            edges.append(Edge(source=str(i - 1), target=str(i)))
    config = Config(width=750, height=400, directed=True, nodeHighlightBehavior=True, highlightColor='#F7A7A6', collapsible=True)
    return agraph(nodes=nodes, edges=edges, config=config)

# Test Cases
TEST_CASES = [
    ("({[]})", True),
    ("([]{})", True),
    ("([)]", False),
    ("((({{{[[[]]]}}})))", True),
    ("({[})", False),
    ("", True),
    ("([{}]){}", True),
    ("[", False),
    ("[(])", False)
]

# Streamlit Interface
st.set_page_config(page_title="PDA Bracket Validator", layout="centered")
st.title("🔢 PDA-Based Bracket Validator")

st.markdown("""
### 🧠 How This Works
A **Pushdown Automaton (PDA)** is like a finite state machine but with a stack — allowing it to remember an unlimited amount of information.

In this project, the PDA reads a string of brackets. It pushes **opening brackets** `(`, `[`, `{` onto the stack. When it encounters a **closing bracket**, it checks if it matches the **top of the stack**.

- If it matches, it pops the opening bracket.
- If it doesn't match or the stack is empty, the string is invalid.
- If the stack is empty at the end, the string is valid.
""")

with st.expander("🔍 Click to see how the PDA is implemented in code"):
    st.code('''
class PDAMachine:
    def __init__(self):
        self.stack = []
        self.transitions = []
        self.pairs = {')': '(', ']': '[', '}': '{'}

    def validate(self, input_str: str) -> bool:
        for char in input_str:
            if char in '({[':
                self.stack.append(char)
            elif char in ')}]':
                if not self.stack or self.stack[-1] != self.pairs[char]:
                    return False
                self.stack.pop()
        return len(self.stack) == 0
''', language='python')
    st.markdown("This function uses a **stack** to track opening brackets and compares them with closing brackets using a dictionary of matching pairs.")

input_str = st.text_input("Enter a string of brackets (e.g., ()[]{})")

if input_str:
    pda = PDAMachine()

    if pda.validate(input_str):
        st.success("✅ The string is balanced and accepted by the PDA.")

        st.subheader("PDA Transition Trace")
        for symbol, stack in pda.get_trace():
            st.write(f"**Input:** {symbol} → **Stack:** {''.join(stack) if stack else 'Empty'}")

        st.subheader("PDA Trace Visualization (Graphviz)")
        dot = draw_pda_trace(pda.get_trace())
        st.graphviz_chart(dot.source)

        if st.checkbox("Show Animated PDA using AGraph"):
            st.subheader("Animated PDA Transition (streamlit-agraph)")
            animate_pda_trace(pda.get_trace())

    else:
        st.error("❌ The string is not balanced and rejected by the PDA.")

        st.subheader("PDA Transition Trace")
        for symbol, stack in pda.get_trace():
            st.write(f"**Input:** {symbol} → **Stack:** {''.join(stack) if stack else 'Empty'}")

        st.subheader("PDA Trace Visualization (Graphviz)")
        dot = draw_pda_trace(pda.get_trace())
        st.graphviz_chart(dot.source)

        if st.checkbox("Show Animated PDA using AGraph"):
            st.subheader("Animated PDA Transition (streamlit-agraph)")
            animate_pda_trace(pda.get_trace())

st.markdown("---")
st.subheader("🧪 Run Built-in Tests")
if st.button("Run Test Suite"):
    passed, failed = 0, 0
    for test_input, expected in TEST_CASES:
        pda = PDAMachine()
        result = pda.validate(test_input)
        if result == expected:
            st.success(f"PASSED ✅ '{test_input}' → {expected}")
            passed += 1
        else:
            st.error(f"FAILED ❌ '{test_input}' → Expected {expected}, Got {result}")
            failed += 1
    st.info(f"✅ Total Passed: {passed} | ❌ Total Failed: {failed}")
