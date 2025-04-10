import streamlit as st
from typing import List, Dict, Tuple
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

# Context-Free Grammar Parser to show LMD and RMD
class CFGParser:
    def __init__(self):
        self.grammar = {
            'S': ['(S)', '[S]', '{S}', 'SS', '']
        }

    def generate_lmd(self, s: str) -> List[Dict]:
        return self._derive(s, left=True)

    def generate_rmd(self, s: str) -> List[Dict]:
        return self._derive(s, left=False)

    def _derive(self, s: str, left: bool) -> List[Dict]:
        steps = [self._get_tree_structure('S')]
        current = 'S'
        while current != s:
            for rule in self.grammar['S']:
                temp = current.replace('S', rule, 1 if left else -1)
                if s.startswith(temp) if left else s.endswith(temp):
                    current = temp
                    steps.append(self._get_tree_structure(current))
                    break
            else:
                break
        return steps

    def _get_tree_structure(self, string: str) -> Dict:
        return {'symbol': string, 'children': []}

# Function to visualize PDA transitions as a graphviz graph
def draw_pda_trace(transitions: List[Tuple[str, List[str]]]) -> Digraph:
    dot = Digraph()
    for i, (symbol, stack) in enumerate(transitions):
        dot.node(str(i), f"{symbol}\nStack: {''.join(stack) if stack else 'Empty'}")
        if i > 0:
            dot.edge(str(i - 1), str(i))
    return dot

# Function to visualize PDA transitions using streamlit-agraph (animated)
def agraph_trace(transitions: List[Tuple[str, List[str]]]):
    nodes = []
    edges = []
    for i, (symbol, stack) in enumerate(transitions):
        label = f"{symbol}\nStack: {''.join(stack) if stack else 'Empty'}"
        nodes.append(Node(id=str(i), label=label))
        if i > 0:
            edges.append(Edge(source=str(i - 1), target=str(i)))

    config = Config(width=750, height=400, directed=True, nodeHighlightBehavior=True, highlightColor='#F7A7A6')
    return agraph(nodes=nodes, edges=edges, config=config)

# Function to visualize derivation trees using streamlit-agraph
def visualize_derivation_tree(steps: List[Dict]):
    nodes = []
    edges = []

    def create_nodes_edges(node, parent=None):
        node_id = node['symbol']
        nodes.append(Node(id=node_id, label=node_id))
        if parent:
            edges.append(Edge(source=parent, target=node_id))

        for child in node.get('children', []):
            create_nodes_edges(child, node_id)

    create_nodes_edges(steps[0])

    config = Config(width=750, height=400, directed=True, nodeHighlightBehavior=True, highlightColor='#F7A7A6')
    return agraph(nodes=nodes, edges=edges, config=config)

# Streamlit Interface
st.set_page_config(page_title="PDA Bracket Validator", layout="centered")
st.title("PDA-Based Bracket Validator")
st.markdown("""
This app checks whether a given string of brackets is **balanced** using a **Pushdown Automaton (PDA)**.
It also shows the **Leftmost (LMD)** and **Rightmost Derivations (RMD)** for valid strings.
""")

input_str = st.text_input("Enter a string of brackets (e.g., ()[]{}):")

if input_str:
    pda = PDAMachine()
    parser = CFGParser()

    if pda.validate(input_str):
        st.success("✅ The string is balanced and accepted by the PDA.")

        st.subheader("PDA Transition Trace")
        for symbol, stack in pda.get_trace():
            st.write(f"**Input:** {symbol} → **Stack:** {''.join(stack) if stack else 'Empty'}")

        st.subheader("PDA Trace Visualization (Graphviz)")
        dot = draw_pda_trace(pda.get_trace())
        st.graphviz_chart(dot.source)

        st.subheader("Animated PDA Trace (streamlit-agraph)")
        agraph_trace(pda.get_trace())

        st.subheader("Leftmost Derivation (LMD) Tree")
        lmd_steps = parser.generate_lmd(input_str)
        visualize_derivation_tree(lmd_steps)

        st.subheader("Rightmost Derivation (RMD) Tree")
        rmd_steps = parser.generate_rmd(input_str)
        visualize_derivation_tree(rmd_steps)

    else:
        st.error("❌ The string is not balanced and rejected by the PDA.")

        st.subheader("PDA Transition Trace")
        for symbol, stack in pda.get_trace():
            st.write(f"**Input:** {symbol} → **Stack:** {''.join(stack) if stack else 'Empty'}")

        st.subheader("PDA Trace Visualization (Graphviz)")
        dot = draw_pda_trace(pda.get_trace())
        st.graphviz_chart(dot.source)

        st.subheader("Animated PDA Trace (streamlit-agraph)")
        agraph_trace(pda.get_trace())
