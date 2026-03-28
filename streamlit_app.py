import streamlit as st
import random
import time

# --- CONFIG ---
st.set_page_config(page_title="ChemMaster Pro", page_icon="🧪", layout="centered")

# --- STYLING ---
st.markdown("""
    <style>
    .stButton>button { border-radius: 10px; height: 3em; font-weight: bold; }
    .streak-box { background: #ff4b4b; color: white; padding: 10px; border-radius: 15px; text-align: center; }
    .feedback-correct { color: #28a745; font-weight: bold; }
    .feedback-wrong { color: #dc3545; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DATASET ---
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
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'correct_in_stage' not in st.session_state: st.session_state.correct_in_stage = 0
if 'options' not in st.session_state: st.session_state.options = []
if 'current_q' not in st.session_state: 
    st.session_state.current_q = random.choice(elements)
    st.session_state.options = [] # Trigger first shuffle

def generate_options(correct_val, key_name, all_elements):
    # Create 4 unique options
    opts = {correct_val}
    while len(opts) < 4:
        wrong_el = random.choice(all_elements)
        opts.add(wrong_el[key_name])
    opts_list = list(opts)
    random.shuffle(opts_list)
    return opts_list

# --- HEADER & STATS ---
st.title("🧪 ChemMaster: The Quest")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Level", st.session_state.level)
col_b.metric("Electrons", st.session_state.score)
col_c.write(f"🔥 Streak: **{st.session_state.streak}**")

# --- GAME LOGIC ---
q = st.session_state.current_q

# Initialize options for the current question if empty
if not st.session_state.options:
    if st.session_state.level == 1:
        st.session_state.options = generate_options(q['n'], 'n', elements)
    elif st.session_state.level == 2:
        st.session_state.options = [1, 2, 3, 4] # Periods are fixed
    else:
        st.session_state.options = ["Alkali Metal", "Noble Gas", "Halogen", "Non-metal", "Alkaline Earth", "Metalloid"]

# Display Question
st.divider()
st.subheader(f"Question {st.session_state.q_count + 1} of 35")

if st.session_state.level == 1:
    st.write(f"### What is the **Atomic Number** of **{q['name']}** ({q['s']})?")
    correct_answer = q['n']
elif st.session_state.level == 2:
    st.write(f"### Which **Period** does **{q['name']}** ({q['s']}) belong to?")
    correct_answer = q['period']
else:
    st.write(f"### Analyze: `{q['config']}`")
    st.write(f"What is the **Classification** of **{q['name']}**?")
    correct_answer = q['class']

# Multiple Choice Buttons
cols = st.columns(2)
for idx, opt in enumerate(st.session_state.options):
    with cols[idx % 2]:
        if st.button(str(opt), key=f"btn_{idx}"):
            if opt == correct_answer:
                st.toast("Correct! +10 XP", icon="✅")
                st.session_state.score += 10
                st.session_state.streak += 1
                st.session_state.correct_in_stage += 1
            else:
                st.error(f"Wrong! The correct answer was **{correct_answer}**.")
                st.info(f"Refresher: {q['name']} ({q['s']}) has Atomic Number {q['n']}, Period {q['period']}, and is a {q['class']}.")
                st.session_state.streak = 0
                time.sleep(2) # Give them time to read the feedback
            
            # Move to next question
            st.session_state.q_count += 1
            st.session_state.current_q = random.choice(elements)
            st.session_state.options = [] # Clear options for next shuffle
            st.rerun()

# --- LEVEL PROGRESSION CHECK ---
if st.session_state.q_count >= 35:
    pass_mark = 35 * 0.70 # 70% to pass
    if st.session_state.correct_in_stage >= pass_mark:
        st.balloons()
        st.success(f"🎊 Level Complete! You got {st.session_state.correct_in_stage}/35 correct. Level {st.session_state.level + 1} Unlocked!")
        st.session_state.level += 1
        st.session_state.q_count = 0
        st.session_state.correct_in_stage = 0
    else:
        st.warning(f"Level Failed. You got {st.session_state.correct_in_stage}/35. You need 25 correct to pass. Restarting Level...")
        st.session_state.q_count = 0
        st.session_state.correct_in_stage = 0
    
    if st.button("Continue"):
        st.rerun()

# --- REWARDS / BADGES ---
with st.sidebar:
    st.header("🏆 Achievements")
    if st.session_state.streak >= 5: st.write("🎖️ **Hot Streak!** (5 in a row)")
    if st.session_state.level > 1: st.write("🥈 **Science Apprentice**")
    if st.session_state.level > 2: st.write("🥇 **Master Chemist**")
    
    st.divider()
    if st.button("Reset Entire Game"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
