import streamlit as st
import random
import time
import pandas as pd

# --- CONFIG & NEON THEME ---
st.set_page_config(page_title="ChemMaster: Neon Lab", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #00f2fe; color: #0e1117; border-radius: 10px;
        border: none; font-weight: bold; transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 15px #00f2fe; transform: scale(1.02);
    }
    .stat-card {
        background: #1c212d; padding: 20px; border-radius: 15px;
        border-bottom: 4px solid #4facfe; text-align: center;
    }
    .result-pass { color: #00ff88; font-weight: bold; font-size: 20px; }
    .result-fail { color: #ff4b4b; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENHANCED DATASET ---
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

# --- SESSION STATE ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'history' not in st.session_state: st.session_state.history = []
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'show_results' not in st.session_state: st.session_state.show_results = False

def init_round():
    round_qs = []
    for _ in range(10):
        el = random.choice(elements)
        if st.session_state.level == 1: q_type = random.choice(['n', 's', 'name'])
        elif st.session_state.level == 2: q_type = random.choice(['period', 'group', 'mass'])
        else: q_type = random.choice(['config', 'class'])
        round_qs.append({'element': el, 'type': q_type})
    st.session_state.round_qs = round_qs

if 'round_qs' not in st.session_state: init_round()

# --- RANKING SYSTEM ---
def get_rank(xp):
    if xp < 100: return "Novice Alchemist 🧪"
    if xp < 300: return "Junior Chemist ⚗️"
    if xp < 600: return "Lab Specialist 🧬"
    return "Elemental Grandmaster 👑"

# --- GAME INTERFACE ---
st.title("⚡ CHEM-MASTER: NEON QUEST")

# Top HUD
hud_col1, hud_col2, hud_col3 = st.columns(3)
with hud_col1:
    st.markdown(f"<div class='stat-card'><h3>LEVEL</h3><h1>{st.session_state.level}</h1></div>", unsafe_allow_html=True)
with hud_col2:
    st.markdown(f"<div class='stat-card'><h3>XP POINTS</h3><h1>{st.session_state.xp}</h1></div>", unsafe_allow_html=True)
with hud_col3:
    st.markdown(f"<div class='stat-card'><h3>RANK</h3><p>{get_rank(st.session_state.xp)}</p></div>", unsafe_allow_html=True)

st.write("---")

if not st.session_state.show_results:
    curr_q = st.session_state.round_qs[st.session_state.q_idx]
    el = curr_q['element']
    qt = curr_q['type']
    
    # Question mapping
    data = {
        'n': (f"Identify Atomic Number: {el['name']}", el['n'], 'n'),
        's': (f"What is the Symbol for {el['name']}?", el['s'], 's'),
        'name': (f"Which element is #{el['n']}?", el['name'], 'name'),
        'period': (f"Find Period: {el['name']}", el['period'], 'period'),
        'group': (f"Find Group: {el['name']}", el['group'], 'group'),
        'mass': (f"Atomic Mass of {el['name']}?", el['mass'], 'mass'),
        'config': (f"Who has configuration {el['config']}?", el['name'], 'name'),
        'class': (f"Classification: {el['name']}?", el['class'], 'class')
    }
    prompt, correct, key = data[qt]

    # Generate Options
    if 'opts' not in st.session_state:
        opts = {correct}
        while len(opts) < 4:
            opts.add(random.choice(elements)[key])
        st.session_state.opts = list(opts)
        random.shuffle(st.session_state.opts)
        st.session_state.start_time = time.time()

    # Progress Bar
    st.write(f"Quest Progress: {st.session_state.q_idx + 1} / 10")
    st.progress((st.session_state.q_idx + 1) / 10)

    st.markdown(f"## {prompt}")
    
    # Choice Grid
    cols = st.columns(2)
    for idx, opt in enumerate(st.session_state.opts):
        with cols[idx % 2]:
            if st.button(f"⚛️ {opt}", key=f"btn_{idx}"):
                duration = time.time() - st.session_state.start_time
                is_correct = (opt == correct)
                
                # Dynamic Feedback
                if is_correct:
                    bonus = 5 if duration < 4 else 0
                    st.session_state.xp += (10 + bonus)
                    st.toast(f"EXCELLENT! +{10+bonus} XP", icon="🔥")
                else:
                    st.toast("REACTION FAILED!", icon="❌")
                
                st.session_state.history.append({
                    'Quest': prompt,
                    'You': opt,
                    'Target': correct,
                    'Result': "✅" if is_correct else "❌"
                })
                
                st.session_state.q_idx += 1
                del st.session_state.opts
                if st.session_state.q_idx >= 10: st.session_state.show_results = True
                st.rerun()

else:
    # --- END SCREEN ---
    st.header("📊 MISSION DEBRIEF")
    correct_count = sum(1 for x in st.session_state.history if x['Result'] == "✅")
    
    if correct_count >= 7:
        st.balloons()
        st.markdown(f"<p class='result-pass'>MISSION SUCCESS: {correct_count}/10 COMPLETED</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='result-fail'>MISSION FAILED: {correct_count}/10. 70% accuracy required.</p>", unsafe_allow_html=True)

    # Review Table
    df = pd.DataFrame(st.session_state.history)
    st.table(df)

    # Next Steps
    if correct_count >= 7:
        if st.button("🚀 UNLOCK NEXT LEVEL"):
            st.session_state.level += 1
            st.session_state.q_idx = 0
            st.session_state.history = []
            st.session_state.show_results = False
            init_round()
            st.rerun()
    else:
        if st.button("🔄 RE-RUN SIMULATION"):
            st.session_state.q_idx = 0
            st.session_state.history = []
            st.session_state.show_results = False
            init_round()
            st.rerun()
