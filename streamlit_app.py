import streamlit as st
import random
import time
import pandas as pd

# --- 1. APP SETUP ---
st.set_page_config(page_title="First 20 Elements Master", page_icon="🧪")

# Custom Styling to make it look like a Game Interface
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #4facfe; }
    .metric-container { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #4facfe; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE DATA (FIRST 20 ELEMENTS) ---
elements = [
    {"n": 1, "s": "H", "name": "Hydrogen", "mass": 1, "group": 1, "period": 1, "class": "Non-metal", "config": "1"},
    {"n": 2, "s": "He", "name": "Helium", "mass": 4, "group": 18, "period": 1, "class": "Noble Gas", "config": "2"},
    {"n": 3, "s": "Li", "name": "Lithium", "mass": 7, "group": 1, "period": 2, "class": "Alkali Metal", "config": "2, 1"},
    {"n": 4, "s": "Be", "name": "Beryllium", "mass": 9, "group": 2, "period": 2, "class": "Alkaline Earth", "config": "2, 2"},
    {"n": 5, "s": "B", "name": "Boron", "mass": 11, "group": 13, "period": 2, "class": "Metalloid", "config": "2, 3"},
    {"n": 6, "s": "C", "name": "Carbon", "mass": 12, "group": 14, "period": 2, "class": "Non-metal", "config": "2, 4"},
    {"n": 7, "s": "N", "name": "Nitrogen", "mass": 14, "group": 15, "period": 2, "class": "Non-metal", "config": "2, 5"},
    {"n": 8, "s": "O", "name": "Oxygen", "mass": 16, "group": 16, "period": 2, "class": "Non-metal", "config": "2, 6"},
    {"n": 9, "s": "F", "name": "Fluorine", "mass": 19, "group": 17, "period": 2, "class": "Halogen", "config": "2, 7"},
    {"n": 10, "s": "Ne", "name": "Neon", "mass": 20, "group": 18, "period": 2, "class": "Noble Gas", "config": "2, 8"},
    {"n": 11, "s": "Na", "name": "Sodium", "mass": 23, "group": 1, "period": 3, "class": "Alkali Metal", "config": "2, 8, 1"},
    {"n": 12, "s": "Mg", "name": "Magnesium", "mass": 24, "group": 2, "period": 3, "class": "Alkaline Earth", "config": "2, 8, 2"},
    {"n": 13, "s": "Al", "name": "Aluminum", "mass": 27, "group": 13, "period": 3, "class": "Post-transition Metal", "config": "2, 8, 3"},
    {"n": 14, "s": "Si", "name": "Silicon", "mass": 28, "group": 14, "period": 3, "class": "Metalloid", "config": "2, 8, 4"},
    {"n": 15, "s": "P", "name": "Phosphorus", "mass": 31, "group": 15, "period": 3, "class": "Non-metal", "config": "2, 8, 5"},
    {"n": 16, "s": "S", "name": "Sulfur", "mass": 32, "group": 16, "period": 3, "class": "Non-metal", "config": "2, 8, 6"},
    {"n": 17, "s": "Cl", "name": "Chlorine", "mass": 35.5, "group": 17, "period": 3, "class": "Halogen", "config": "2, 8, 7"},
    {"n": 18, "s": "Ar", "name": "Argon", "mass": 40, "group": 18, "period": 3, "class": "Noble Gas", "config": "2, 8, 8"},
    {"n": 19, "s": "K", "name": "Potassium", "mass": 39, "group": 1, "period": 4, "class": "Alkali Metal", "config": "2, 8, 8, 1"},
    {"n": 20, "s": "Ca", "name": "Calcium", "mass": 40, "group": 2, "period": 4, "class": "Alkaline Earth", "config": "2, 8, 8, 2"},
]

# --- 3. GAME STATE MANAGEMENT ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'history' not in st.session_state: st.session_state.history = []
if 'show_results' not in st.session_state: st.session_state.show_results = False

def start_new_round():
    round_qs = []
    for _ in range(10):
        el = random.choice(elements)
        # Level-specific question types
        if st.session_state.level == 1:
            q_type = random.choice(['symbol', 'n', 'name'])
        elif st.session_state.level == 2:
            q_type = random.choice(['period', 'group', 'mass'])
        else:
            q_type = random.choice(['config', 'class'])
        round_qs.append({'el': el, 'type': q_type})
    st.session_state.round_qs = round_qs

if 'round_qs' not in st.session_state:
    start_new_round()

# --- 4. GAME UI ---
st.title("🧪 Chemistry Lab Challenge")
st.write("Master the first 20 elements to earn your Chemist Certification!")

# Dashboard
c1, c2, c3 = st.columns(3)
c1.metric("Current Level", st.session_state.level)
c2.metric("Total XP", st.session_state.xp)
c3.write(f"**Status:** {'Beginner' if st.session_state.xp < 100 else 'Expert'}")

if not st.session_state.show_results:
    curr = st.session_state.round_qs[st.session_state.q_idx]
    el = curr['el']
    t = curr['type']
    
    # Question Setup
    if t == 'symbol': prompt, correct, key = f"What is the Symbol for {el['name']}?", el['s'], 's'
    elif t == 'n': prompt, correct, key = f"What is the Atomic Number of {el['name']}?", el['n'], 'n'
    elif t == 'name': prompt, correct, key = f"Which element has Atomic Number {el['n']}?", el['name'], 'name'
    elif t == 'period': prompt, correct, key = f"What Period is {el['name']} in?", el['period'], 'period'
    elif t == 'group': prompt, correct, key = f"What Group is {el['name']} in?", el['group'], 'group'
    elif t == 'mass': prompt, correct, key = f"What is the Atomic Mass of {el['name']}?", el['mass'], 'mass'
    elif t == 'config': prompt, correct, key = f"Identify the element with configuration {el['config']}:", el['name'], 'name'
    elif t == 'class': prompt, correct, key = f"What is the classification of {el['name']}?", el['class'], 'class'

    # Generate Multiple Choice Options
    if 'current_options' not in st.session_state:
        opts = {correct}
        while len(opts) < 4:
            opts.add(random.choice(elements)[key])
        st.session_state.current_options = list(opts)
        random.shuffle(st.session_state.current_options)

    # Progress Bar for the 10 questions
    st.write(f"Question {st.session_state.q_idx + 1} of 10")
    st.progress((st.session_state.q_idx + 1) / 10)

    st.subheader(prompt)
    
    # Choice Buttons
    for opt in st.session_state.current_options:
        if st.button(str(opt), use_container_width=True):
            is_right = (opt == correct)
            if is_right:
                st.session_state.xp += 10
                st.toast("Correct!", icon="✅")
            else:
                st.toast("Incorrect", icon="❌")
            
            # Save to review history
            st.session_state.history.append({
                "Question": prompt,
                "Your Answer": opt,
                "Correct Answer": correct,
                "Result": "✅" if is_right else "❌"
            })
            
            # Move forward
            st.session_state.q_idx += 1
            del st.session_state.current_options
            
            if st.session_state.q_idx >= 10:
                st.session_state.show_results = True
            st.rerun()

else:
    # --- 5. RESULTS & REVIEW PAGE ---
    st.header("🔬 Lab Results Table")
    df = pd.DataFrame(st.session_state.history)
    st.table(df) # This shows exactly what they got right and wrong
    
    score = sum(1 for x in st.session_state.history if x['Result'] == "✅")
    st.write(f"### Final Score: {score} / 10")

    if score >= 7:
        st.success("Great job! You passed the requirements for this level.")
        if st.button("Proceed to Next Level"):
            st.session_state.level += 1
            st.session_state.q_idx = 0
            st.session_state.history = []
            st.session_state.show_results = False
            start_new_round()
            st.rerun()
    else:
        st.error("You need at least 7 correct answers to pass. Study the table above and try again!")
        if st.button("Retry Level"):
            st.session_state.q_idx = 0
            st.session_state.history = []
            st.session_state.show_results = False
            start_new_round()
            st.rerun()
