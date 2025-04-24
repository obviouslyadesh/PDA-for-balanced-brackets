import streamlit as st
from pda_classes import PDAMachine, PalindromePDA, ArithmeticPDA
from tests import run_tests
from typing import List, Tuple
from graphviz import Digraph
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd

# --- UI ---
st.set_page_config(page_title="PDA Validator APP", layout="centered")
st.title("PDA Validator Interface")

st.markdown("""
This app simulates a **Pushdown Automaton (PDA)** to validate:

1. Balanced Brackets (e.g., `([{}])`)
2. Palindromes (e.g., `aba`)
3. Arithmetic Expressions (e.g., `(4+6)*9`)
""")

mode = st.selectbox("Choose PDA Mode", ["Bracket Validator", "Palindrome Checker", "Arithmetic Expression Validator"])
input_str = st.text_input("Enter Input String")

if input_str:
    if mode == "Bracket Validator":
        pda = PDAMachine()
    elif mode == "Palindrome Checker":
        pda = PalindromePDA()
    elif mode == "Arithmetic Expression Validator":
        pda = ArithmeticPDA()

    valid = pda.validate(input_str)
    transitions = pda.get_trace()

    if valid:
        st.success("✅ Input Accepted by PDA")
    else:
        st.error("❌ Input Rejected by PDA")

    st.subheader("PDA Transition Trace")
    for symbol, stack in transitions:
        st.write(f"**Input:** {symbol} → **Stack:** {''.join(stack) if stack else 'Empty'}")

    st.subheader("PDA Trace Visualization (Graphviz)")
    dot = Digraph()
    for i, (symbol, stack) in enumerate(transitions):
        dot.node(str(i), f"{symbol}\nStack: {''.join(stack) if stack else 'Empty'}")
        if i > 0:
            dot.edge(str(i - 1), str(i))
    st.graphviz_chart(dot.source)

    if st.checkbox("Show Animated PDA using AGraph"):
        nodes = []
        edges = []
        for i, (symbol, stack) in enumerate(transitions):
            label = f"{symbol} | Stack: {''.join(stack) if stack else 'Empty'}"
            nodes.append(Node(id=str(i), label=label))
            if i > 0:
                edges.append(Edge(source=str(i - 1), target=str(i)))
        config = Config(width=750, height=400, directed=True, nodeHighlightBehavior=True,
                        highlightColor='#F7A7A6', collapsible=True)
        st.subheader("Animated PDA Transition (streamlit-agraph)")
        agraph(nodes=nodes, edges=edges, config=config)

# --- Unit Test Section ---
if st.button("🔍 Run Unit Tests"):
    st.subheader("Unit Test Results")
    test_data = run_tests()
    df = pd.DataFrame(test_data, columns=["PDA Type", "Input String", "Expected", "Actual"])
    df["Result"] = df["Expected"] == df["Actual"]
    df["Result"] = df["Result"].apply(lambda x: "✅ Pass" if x else "❌ Fail")
    st.dataframe(df.style.applymap(lambda v: 'color: green' if v == '✅ Pass' else 'color: red', subset=["Result"]))
