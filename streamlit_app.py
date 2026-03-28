import streamlit as st
import random
import time

# --- CONFIG & STYLES ---
st.set_page_config(page_title="ChemMaster: Periodic Quest", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #0e1117; color: white; border: 1px solid #4facfe; }
    .stButton>button:hover { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); color: black; }
    .stat-box { padding: 20px; border-radius: 10px; background-color: #f0f2f6; border-left: 5px solid #4facfe; }
    </style>
    """, unsafe_allow_html=True)

# --- THE DATA (First 20 Elements) ---
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
if 'current_q' not in st.session_state: st.session_state.current_q = random.choice(elements)
if 'mode' not in st.session_state: st.session_state.mode = "Learning"

def next_q():
    st.session_state.current_q = random.choice(elements)

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎮 Player Profile")
    st.metric("Total Electrons (Score)", st.session_state.score)
    st.write(f"**Rank:** {'Alchemist' if st.session_state.score < 100 else 'Professor'}")
    st.divider()
    if st.button("Reset Lab Progress"):
        st.session_state.score = 0
        st.rerun()

# --- MAIN APP ---
st.title("🧪 ChemMaster: The Periodic Quest")

tab1, tab2 = st.tabs(["📖 Learning Mode (Levels 1-3)", "⚡ Time Attack (Recall)"])

# --- TAB 1: LEVELS ---
with tab1:
    l1, l2, l3 = st.columns(3)
    q = st.session_state.current_q
    
    # LEVEL 1: KNOWLEDGE (Symbols & Numbers)
    with l1:
        st.subheader("Level 1: Knowledge")
        st.write(f"Identify the **Atomic Number** of **{q['name']}** ({q['s']})")
        ans1 = st.number_input("Enter Z:", min_value=0, key="l1")
        if st.button("Check Knowledge"):
            if ans1 == q['n']:
                st.success("Correct! +10 Electrons")
                st.session_state.score += 10
                next_q(); st.rerun()
            else:
                st.error(f"Wrong! {q['name']} has {q['n']} protons.")

    # LEVEL 2: UNDERSTANDING (Groups & Periods)
    with l2:
        st.subheader("Level 2: Understanding")
        if st.session_state.score < 50:
            st.lock("Unlock at 50 Electrons")
        else:
            st.write(f"In which **Period** is **{q['name']}** found?")
            ans2 = st.selectbox("Select Period:", [1, 2, 3, 4], key="l2")
            if st.button("Check Understanding"):
                if ans2 == q['period']:
                    st.success("Brilliant! +20 Electrons")
                    st.session_state.score += 20
                    next_q(); st.rerun()
                else:
                    st.error(f"Incorrect. Period {q['period']} matches its {len(q['config'].split(','))} electron shells.")

    # LEVEL 3: APPLICATION (Patterns)
    with l3:
        st.subheader("Level 3: Application")
        if st.session_state.score < 150:
            st.lock("Unlock at 150 Electrons")
        else:
            st.write(f"**Electron Visual:** `{q['config']}`")
            st.caption("Identify the classification based on the valence electrons.")
            ans3 = st.radio("Class:", ["Alkali Metal", "Noble Gas", "Halogen", "Non-metal"], key="l3")
            if st.button("Apply Knowledge"):
                if ans3 == q['class']:
                    st.success("Masterful! +50 Electrons")
                    st.session_state.score += 50
                    next_q(); st.rerun()
                else:
                    st.error(f"Pattern mismatch. {q['name']} is a {q['class']}.")

# --- TAB 2: TIME ATTACK ---
with tab2:
    st.subheader("⚡ Quick Recall Challenge")
    if 'timer_start' not in st.session_state:
        if st.button("🚀 START 60s CHALLENGE"):
            st.session_state.timer_start = time.time()
            st.rerun()
    else:
        elapsed = time.time() - st.session_state.timer_start
        remaining = max(0, 60 - int(elapsed))
        st.progress(remaining / 60)
        st.write(f"⏳ Time Remaining: **{remaining} seconds**")
        
        if remaining <= 0:
            st.warning(f"Time is up! Final score: {st.session_state.score}")
            if st.button("Restart"): 
                del st.session_state.timer_start
                st.rerun()
        else:
            t_q = st.session_state.current_q
            ans_t = st.text_input(f"Quick! What is the Symbol for **{t_q['name']}**?", key="ta_input")
            if st.button("Zap!"):
                if ans_t.strip().upper() == t_q['s']:
                    st.session_state.score += 5
                    next_q(); st.rerun()
                else:
                    st.error("Wrong! -2 Seconds penalty")
                    st.session_state.timer_start -= 2
