import streamlit as st
import random
import time

# --- CONFIG ---
st.set_page_config(page_title="ChemMaster Pro", page_icon="🧪", layout="wide")

# --- DATASET (First 20 Elements) ---
elements = [
    {"n": 1, "s": "H", "name": "Hydrogen", "group": 1, "period": 1, "class": "Non-metal", "config": "1"},
    {"n": 2, "s": "He", "name": "Helium", "group": 18, "period": 1, "class": "Noble Gas", "config": "2"},
    {"n": 3, "s": "Li", "name": "Lithium", "group": 1, "period": 2, "class": "Alkali Metal", "config": "2, 1"},
    {"n": 4, "s": "Be", "name": "Beryllium", "group": 2, "period": 2, "class": "Alkaline Earth", "config": "2, 2"},
    {"n": 5, "s": "B", "name": "Boron", "group": 13, "period": 2, "class": "Metalloid", "config": "2, 3"},
    {"n": 6, "s": "C", "name": "Carbon", "group": 14, "period": 2, "class": "Non-metal", "config": "2, 4"},
    {"n": 7, "s": "N", "name": "Nitrogen", "group": 15, "period": 2, "class": "Non-metal", "config": "2, 5"},
    {"n": 8, "s": "O", "name": "Oxygen", "group": 16, "period": 2, "class": "Non-metal", "config": "2, 6"},
    {"n": 9, "s": "F", "name": "Fluorine", "group": 17, "period": 2, "class": "Halogen", "config": "2, 7"},
    {"n": 10, "s": "Ne", "name": "Neon", "group": 18, "period": 2, "class": "Noble Gas", "config": "2, 8"},
    {"n": 11, "s": "Na", "name": "Sodium", "group": 1, "period": 3, "class": "Alkali Metal", "config": "2, 8, 1"},
    {"n": 12, "s": "Mg", "name": "Magnesium", "group": 2, "period": 3, "class": "Alkaline Earth", "config": "2, 8, 2"},
    {"n": 13, "s": "Al", "name": "Aluminum", "group": 13, "period": 3, "class": "Post-transition Metal", "config": "2, 8, 3"},
    {"n": 14, "s": "Si", "name": "Silicon", "group": 14, "period": 3, "class": "Metalloid", "config": "2, 8, 4"},
    {"n": 15, "s": "P", "name": "Phosphorus", "group": 15, "period": 3, "class": "Non-metal", "config": "2, 8, 5"},
    {"n": 16, "s": "S", "name": "Sulfur", "group": 16, "period": 3, "class": "Non-metal", "config": "2, 8, 6"},
    {"n": 17, "s": "Cl", "name": "Chlorine", "group": 17, "period": 3, "class": "Halogen", "config": "2, 8, 7"},
    {"n": 18, "s": "Ar", "name": "Argon", "group": 18, "period": 3, "class": "Noble Gas", "config": "2, 8, 8"},
    {"n": 19, "s": "K", "name": "Potassium", "group": 1, "period": 4, "class": "Alkali Metal", "config": "2, 8, 8, 1"},
    {"n": 20, "s": "Ca", "name": "Calcium", "group": 2, "period": 4, "class": "Alkaline Earth", "config": "2, 8, 8, 2"},
]

# --- SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_count' not in st.session_state: st.session_state.q_count = 0
if 'current_q' not in st.session_state: st.session_state.current_q = random.choice(elements)

def next_q():
    st.session_state.current_q = random.choice(elements)
    st.session_state.q_count += 1

# --- SIDEBAR STATS ---
with st.sidebar:
    st.header("📊 Progress Tracker")
    st.metric("Questions Solved", st.session_state.q_count)
    st.metric("Electrons (Score)", st.session_state.score)
    
    # Target Progress Bars
    if st.session_state.q_count < 35:
        st.write("Next Goal: Level 2 Unlock")
        st.progress(st.session_state.q_count / 35)
    elif st.session_state.q_count < 70:
        st.write("Next Goal: Level 3 Unlock")
        st.progress((st.session_state.q_count - 35) / 35)
    
    if st.sidebar.button("Reset Game"):
        st.session_state.score = 0
        st.session_state.q_count = 0
        st.rerun()

# --- MAIN GAME LOGIC ---
st.title("🧪 ChemMaster: The Periodic Quest")

q = st.session_state.current_q

# LEVEL 1: 0 - 34 Questions (Focus on Names/Symbols)
if st.session_state.q_count < 35:
    st.header("Level 1")
    st.info(f"Question {st.session_state.q_count + 1} of 35 for this stage.")
    
    st.write(f"### Identify the **Atomic Number** of **{q['name']}** ({q['s']})")
    ans1 = st.number_input("Enter Z:", min_value=0, key="l1_input")
    
    if st.button("Check Answer"):
        if ans1 == q['n']:
            st.success(f"Correct! {q['name']} is element #{q['n']}. +10 XP")
            st.session_state.score += 10
            next_q()
            st.rerun()
        else:
            st.error(f"Incorrect. {q['name']} has {q['n']} protons. Try to remember its position!")

# LEVEL 2: 35 - 69 Questions (Focus on Group/Period)
elif 35 <= st.session_state.q_count < 70:
    st.header("Level 2")
    st.info(f"Question {st.session_state.q_count - 34} of 35 for this stage.")
    
    st.write(f"### Which **Period** does **{q['name']}** ({q['s']}) belong to?")
    ans2 = st.selectbox("Select Period:", [1, 2, 3, 4], key="l2_input")
    
    if st.button("Verify Period"):
        if ans2 == q['period']:
            st.success(f"Brilliant! It has {len(q['config'].split(','))} electron shells. +20 XP")
            st.session_state.score += 20
            next_q()
            st.rerun()
        else:
            st.error(f"Wrong. {q['name']} is in Period {q['period']}. Count the shells: {q['config']}")

# LEVEL 3: 70+ Questions (Application & Patterns)
else:
    st.header("Level 3: Master Class")
    st.info(f"Question {st.session_state.q_count - 69} of 35 for this stage.")
    
    st.write(f"### Electron Visual: `{q['config']}`")
    st.write(f"Identify the **Classification** of this element (**{q['s']}**).")
    
    ans3 = st.radio("Classification:", ["Alkali Metal", "Noble Gas", "Halogen", "Non-metal", "Alkaline Earth", "Metalloid"], key="l3_input")
    
    if st.button("Submit Mastery"):
        if ans3 == q['class']:
            st.success(f"Correct! You identified the {q['class']} pattern. +50 XP")
            st.session_state.score += 50
            next_q()
            st.rerun()
        else:
            st.error(f"Incorrect. Based on the valence electrons ({q['config'].split(',')[-1]}), it is a {q['class']}.")

# Footer pattern guide
with st.expander("🔬 Lab Reference Manual"):
    st.write("- **Period:** Number of electron shells.")
    st.write("- **Group:** Determined by outer (valence) electrons.")
    st.write("- **Atomic Number:** Number of protons in the nucleus.")
