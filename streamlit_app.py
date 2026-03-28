import streamlit as st
import random
import time
import pandas as pd

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="MSc Periodic Master", page_icon="🧪", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #4facfe, #00f2fe); color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    .review-table { background-color: #1c212d; border-radius: 10px; padding: 10px; }
    .wheel-container { display: flex; justify-content: center; align-items: center; height: 300px; }
    .wheel {
        width: 200px; height: 200px; border-radius: 50%; border: 5px solid #FFD700;
        background: conic-gradient(#FF4136 0% 20%, #0074D9 20% 40%, #2ECC40 40% 60%, #FFDC00 60% 80%, #B10DC9 80% 100%);
        transition: transform 3s cubic-bezier(0.1, 0, 0, 1);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA (Using your 8-Level curriculum) ---
if 'levels_data' not in st.session_state:
    st.session_state.levels_data = {
        1: {"name": "Period 1 & 2 Essentials", "data": [
            {"id": 1, "q": "Which element has an Atomic Number of 6?", "opts": ["Nitrogen", "Carbon", "Oxygen", "Boron"], "ans": "Carbon", "shells": "2, 4"},
            {"id": 2, "q": "Molar Mass of Oxygen (O)?", "opts": ["8 g/mol", "12 g/mol", "16 g/mol", "32 g/mol"], "ans": "16 g/mol", "shells": "2, 6"},
            {"id": 3, "q": "Identify configuration 1s² 2s¹:", "opts": ["Helium", "Lithium", "Beryllium", "Sodium"], "ans": "Lithium", "shells": "2, 1"},
            {"id": 4, "q": "Noble Gas in Period 1?", "opts": ["Neon", "Argon", "Hydrogen", "Helium"], "ans": "Helium", "shells": "2"},
            {"id": 5, "q": "Atomic Number 7 belongs to:", "opts": ["Nitrogen", "Fluorine", "Neon", "Carbon"], "ans": "Nitrogen", "shells": "2, 5"}
        ]},
        # ... (Levels 2-8 from your previous message would go here)
        2: {"name": "Group 1 & 2 (Reactive Metals)", "data": [
            {"id": 1, "q": "Alkali Metal with Molar Mass ~23?", "opts": ["Lithium", "Potassium", "Sodium", "Magnesium"], "ans": "Sodium", "shells": "2, 8, 1"},
            {"id": 2, "q": "Atomic Number of Calcium (Ca)?", "opts": ["12", "20", "19", "30"], "ans": "20", "shells": "2, 8, 8, 2"},
            {"id": 3, "q": "Group 2 burns with white flame?", "opts": ["Beryllium", "Calcium", "Magnesium", "Barium"], "ans": "Magnesium", "shells": "2, 8, 2"},
            {"id": 4, "q": "Group 1, Period 4 element?", "opts": ["Sodium", "Potassium", "Rubidium", "Cesium"], "ans": "Potassium", "shells": "2, 8, 8, 1"},
            {"id": 5, "q": "Valency of Group 2 elements?", "opts": ["+1", "+2", "-2", "0"], "ans": "+2", "shells": "N/A"}
        ]}
    }
    # (Note: I've shortened the data here for brevity, but you should keep your full 8 levels)

# --- 3. SESSION STATE ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'history' not in st.session_state: st.session_state.history = []
if 'answered_ids' not in st.session_state: st.session_state.answered_ids = []
if 'mode' not in st.session_state: st.session_state.mode = "spin"
if 'rotation' not in st.session_state: st.session_state.rotation = 0

def draw_shells(config):
    if config == "N/A": return "Valency Question - No Diagram"
    visual = ""
    for i, e in enumerate(config.split(',')):
        visual += f"Shell {i+1}: " + ("🔵 " * int(e)) + f" ({e}e⁻)\n"
    return visual

# --- 4. GAME UI ---
st.title("🛡️ Periodic Master: The MSc Quest")

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Level", st.session_state.level)
col2.metric("Total XP", st.session_state.xp)
col3.metric("Progress", f"{len(st.session_state.answered_ids)}/5")

if st.session_state.mode == "spin":
    st.subheader(f"📍 Current Stage: {st.session_state.levels_data[st.session_state.level]['name']}")
    
    # Wheel UI
    st.markdown(f'<div class="wheel-container"><div class="wheel" style="transform: rotate({st.session_state.rotation}deg);"></div></div>', unsafe_allow_html=True)
    
    if st.button("🚀 SPIN FOR CHALLENGE"):
        available = [q for q in st.session_state.levels_data[st.session_state.level]["data"] if q["id"] not in st.session_state.answered_ids]
        target_q = random.choice(available)
        st.session_state.current_q = target_q
        
        # Spin Animation Math
        st.session_state.rotation += 1080 + (random.randint(0, 360))
        with st.spinner("Calibrating Laboratory Equipment..."):
            time.sleep(2)
        st.session_state.mode = "quiz"
        st.rerun()

elif st.session_state.mode == "quiz":
    q = st.session_state.current_q
    
    st.subheader(f"Question {q['id']}")
    
    left, right = st.columns([2, 1])
    with left:
        st.info(q["q"])
        choice = st.radio("Select your answer:", q["opts"], index=None)
        
        if st.button("CONFIRM REACTION"):
            is_correct = (choice == q["ans"])
            if is_correct:
                st.session_state.xp += 20
                st.toast("Correct!", icon="✅")
            else:
                st.toast("Error in calculation", icon="❌")
            
            # Save to Review Table
            st.session_state.history.append({
                "Level": st.session_state.level,
                "Question": q["q"],
                "Your Answer": choice,
                "Correct": q["ans"],
                "Status": "✅" if is_correct else "❌"
            })
            
            st.session_state.answered_ids.append(q["id"])
            if len(st.session_state.answered_ids) >= 5:
                st.session_state.mode = "review"
            else:
                st.session_state.mode = "spin"
            st.rerun()
            
    with right:
        st.write("**Electron Configuration Visual**")
        st.text(draw_shells(q['shells']))

elif st.session_state.mode == "review":
    st.header(f"🏁 Level {st.session_state.level} Complete")
    
    # Filter history for current level
    lvl_hist = [h for h in st.session_state.history if h["Level"] == st.session_state.level]
    df = pd.DataFrame(lvl_hist).drop(columns=["Level"])
    st.table(df) # THE REVIEW TABLE
    
    score = sum(1 for h in lvl_hist if h["Status"] == "✅")
    
    if score >= 3: # Pass mark 3/5
        st.success(f"Passed! Score: {score}/5. Ready for the next level?")
        if st.button("UNLOCK NEXT LEVEL"):
            st.session_state.level += 1
            st.session_state.answered_ids = []
            st.session_state.mode = "spin"
            st.rerun()
    else:
        st.error(f"Score: {score}/5. You need 3/5 to pass. Retrying level...")
        if st.button("RETRY LEVEL"):
            st.session_state.answered_ids = []
            st.session_state.mode = "spin"
            # Clear level history for retry
            st.session_state.history = [h for h in st.session_state.history if h["Level"] != st.session_state.level]
            st.rerun()

st.markdown(f"---")
st.caption(f"Lead Scientist: Ukazim Chidinma Favour | {time.strftime('%Y')}")
