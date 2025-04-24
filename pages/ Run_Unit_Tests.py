import streamlit as st
from tests import run_tests

st.title("Unit Tests")

st.write("Click the button below to run all PDA validation unit tests.")

if st.button("Run Unit Tests"):
    test_results = run_tests()

    for test_name, input_str, expected, actual in test_results:
        result_text = "✅ Passed" if expected == actual else "❌ Failed"
        st.markdown(f"**{test_name}** - Input: `{input_str}`")
        st.markdown(f"- Expected: `{expected}`")
        st.markdown(f"- Got: `{actual}`")
        st.markdown(f"- Result: **{result_text}**")
        st.divider()
