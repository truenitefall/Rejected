import streamlit as st
import random

# --- PRODUCTION CARD DATA & CONFIG ---
MAX_TOKENS = 10
MAX_ROUNDS = 8
INITIAL_HEALTH = 6

# Fully mapped 70-Card Production Selfish Deck
SELFISH_ARCHETYPES = {
    "Soul Rend": 6, "Childish Screams": 5, "Claws of Fury": 5, "Wails of Despair": 5,
    "Hurt Them": 4, "Kill Them": 3, "Murder": 2, "Murderous Rage": 2, "Night Terrors": 4,
    "Altered Mindstate": 3, "Depression": 2, "Secrets": 2, "Mind Over Matter": 2,
    "Subjugation": 2, "Darkness": 4, "Embrace the Darkness": 4, "From Whence It Came": 3,
    "Take the Child": 4, "The Fire Burns": 2, "Commanding Aura": 2, "Massive Subjugation": 2,
    "Master of None": 1, "Power of Choice": 2, "Call Me Mr. Teeth": 2
}

# Fully mapped 70-Card Production Selfless Deck
SELFLESS_ARCHETYPES = {
    "Protect the Child": 3, "Awe, A Baby": 5, "A Mother's Care": 6, "Fend Them Off": 5,
    "Fight the Darkness": 5, "Hit Them Where It Hurts": 4, "Crush Them": 4, "Our Souls Are Ours": 2,
    "Mine!": 3, "Enticement": 2, "Absolution": 2, "Shrug It Off": 6, "Be Gone Demon!": 2,
    "Confession": 2, "Damned Humans": 2, "Deal Me In": 4, "Embrace the Light": 4, "Lend a Hand": 3,
    "Love of a Mother": 4, "Rebirth": 3, "Sacrifice": 2, "The World Is Ours": 2, "Stand Your Ground": 2,
    "We Are One": 2, "Make Your Choice": 2, "She Is the One (Miranda)": 2
}

SECRET_OBJECTIVES = [
    "Collect 3 white tokens from the unwilling child.", "Collect 3 black tokens from the unwilling child.",
    "Turn 2 players from unwilling to rejected.", "Turn 2 players from rejected to unwilling.",
    "Collect the last black token from unwilling child turning it rejected.", "Collect the last white token from unwilling child saving its soul.",
    "Turn to an unwilling from a rejected.", "Turn to a rejected from an unwilling.",
    "Summon Mr Teeth to the field of play.", "Summon Miranda to the field of play.",
    "Become a rejected and then turn at least one other player rejected.", "Block 4 points of damage to the unwilling child from rejected.",
    "Become unwilling and then turn at least one other player unwilling.", "Block 4 points of damage to the unwilling child from unwilling.",
    "Turn one player rejected through attacks, without using an instant turn card or ability.", "Play at least one psych card from both the selfish and selfless decks.",
    "Turn one player unwilling through attacks, without using an instant turn card or ability.", "Turn one player from unwilling to rejected then back to unwilling.",
    "Turn one player from rejected to unwilling then back to rejected.", "Survive the whole game without being turned."
]

# --- INITIALIZE PRODUCTION DECKS ---
def build_deck(deck_map):
    deck = []
    for card, qty in deck_map.items():
        deck.extend([card] * qty)
    random.shuffle(deck)
    return deck

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_round = 1
    st.session_state.white_tokens = 0
    st.session_state.black_tokens = 0
    st.session_state.game_log = ["Game initialized with 160 production cards!"]
    
    st.session_state.selfish_deck = build_deck(SELFISH_ARCHETYPES)
    st.session_state.selfless_deck = build_deck(SELFLESS_ARCHETYPES)
    st.session_state.objectives_deck = list(SECRET_OBJECTIVES)
    random.shuffle(st.session_state.objectives_deck)

    # Balanced 4-Player Starting State
    st.session_state.players = {
        "Billy (Human)": {"alignment": "Human", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives_deck.pop()},
        "Abagail (Human)": {"alignment": "Human", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives_deck.pop()},
        "Horatio (Rejected)": {"alignment": "Rejected", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives_deck.pop()},
        "Ormund (Rejected)": {"alignment": "Rejected", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives_deck.pop()}
    }
    
    # Deal 3 Starting Cards per Player based on initial alignment
    for p_name, data in st.session_state.players.items():
        for _ in range(3):
            deck = st.session_state.selfless_deck if data["alignment"] == "Human" else st.session_state.selfish_deck
            if deck: data["hand"].append(deck.pop())

def log_message(msg):
    st.session_state.game_log.insert(0, f"Rd {st.session_state.current_round}: {msg}")

# --- MOBILE VIEWPORT OPTIMIZATION ---
st.set_page_config(page_title="Faction & Soul Playtest", layout="centered")
st.title("🔮 Faction & Soul Mobile Board")

# --- MOBILE TOP HUD: GLOBAL TRACKERS ---
st.markdown("### ⏳ Global Dashboard")
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1: st.metric("Round", f"{st.session_state.current_round}/{MAX_ROUNDS}")
with metric_col2: st.metric("⬜ White", f"{st.session_state.white_tokens}/{MAX_TOKENS}")
with metric_col3: st.metric("⬛ Black", f"{st.session_state.black_tokens}/{MAX_TOKENS}")

# --- DICE GENERATOR FOR MOBILE ---
with st.expander("🎲 Custom Action Dice Roller"):
    if st.button("Roll 3 Action Dice", use_container_width=True):
        faces = ["💥 Persuasion", "🛡️ Resistance", "🎭 Manipulation", "💥 Persuasion", "✨ Wildcard", "💀 Penalty"]
        rolls = [random.choice(faces) for _ in range(3)]
        st.success(f"Roll Results: {', '.join(rolls)}")

# --- PLAYER SELECTOR & HAND MANAGER (MOBILE TOUCH OPTIMIZED) ---
st.markdown("---")
st.markdown("### 👥 Active Player Character Mats")
active_p = st.selectbox("Select Character to view Mat & Hand:", list(st.session_state.players.keys()))
p_data = st.session_state.players[active_p]

# Display Selected Player Stats
bg = "#1e293b" if p_data["alignment"] == "Human" else "#3f1d1d"
st.markdown(
    f"""<div style="background-color:{bg}; padding:12px; border-radius:8px; border:1px solid #475569; margin-bottom:10px;">
        <h4 style='margin:0;color:white;'>{active_p} ({p_data['alignment']})</h4>
        <p style='margin:0;color:#cbd5e1;'>Health: <b>{p_data['health']}/{INITIAL_HEALTH}</b></p>
    </div>""", unsafe_html=True
)

# Mobile Quick Action Row for Selected Player
act_col1, act_col2, act_col3 = st.columns(3)
if act_col1.button("💥 Hit (-1 HP)", key=f"h_{active_p}", use_container_width=True):
    p_data["health"] = max(0, p_data["health"] - 1)
    log_message(f"{active_p} took 1 damage.")
    if p_data["health"] == 0:
        p_data["alignment"] = "Rejected" if p_data["alignment"] == "Human" else "Human"
        p_data["health"] = INITIAL_HEALTH
        log_message(f"💀 {active_p} collapsed & flipped to {p_data['alignment']}!")
    st.rerun()

if act_col2.button("❤️ Heal (+1 HP)", key=f"hl_{active_p}", use_container_width=True):
    p_data["health"] = min(INITIAL_HEALTH, p_data["health"] + 1)
    log_message(f"{active_p} healed 1 HP.")
    st.rerun()

if act_col3.button("🃏 Draw Card", key=f"dr_{active_p}", use_container_width=True):
    deck = st.session_state.selfless_deck if p_data["alignment"] == "Human" else st.session_state.selfish_deck
    if deck:
        card = deck.pop()
        p_data["hand"].append(card)
        log_message(f"{active_p} drew 1 card.")
    st.rerun()

# Display Secret Objective & Hand
st.markdown(f"**🕵️ Hidden Secret Objective:** || `{p_data['obj']}` ||")
st.markdown("**🎴 Current Hand Cards (Tap card down below to discard/play):**")

if p_data["hand"]:
    card_to_play = st.radio("Select card from hand:", p_data["hand"], label_visibility="collapsed")
    if st.button(f"🔥 Play/Discard: {card_to_play}", use_container_width=True):
        p_data["hand"].remove(card_to_play)
        log_message(f"{active_p} played/discarded '{card_to_play}'.")
        st.rerun()
else:
    st.info("Hand is empty. Tap 'Draw Card' to draw from your production faction alignment deck.")

# --- MANUALLY ENGAGE TOKENS & NEXT ROUND ---
st.markdown("---")
st.markdown("### 🎛️ Field & Turn Manipulation")
f_col1, f_col2 = st.columns(2)
if f_col1.button("⬜ Gained +1 White Token", use_container_width=True):
    st.session_state.white_tokens = min(MAX_TOKENS, st.session_state.white_tokens + 1)
    log_message("White token manually gained.")
    st.rerun()
if f_col2.button("⬛ Gained +1 Black Token", use_container_width=True):
    st.session_state.black_tokens = min(MAX_TOKENS, st.session_state.black_tokens + 1)
    log_message("Black token manually gained.")
    st.rerun()

if st.button("➡️ End Turn / Advance Round", type="primary", use_container_width=True):
    if st.session_state.current_round < MAX_ROUNDS:
        st.session_state.current_round += 1
        log_message("Advanced to next round phase.")
    else:
        log_message("Doom Clock limit hit!")
    st.rerun()

# --- LIVE LOGGING ---
with st.expander("📜 Live Battle Telemetry Feed"):
    st.text_area("Logs", value="\n".join(st.session_state.game_log), height=150, disabled=True)

# --- WIN DETECTION ---
if st.session_state.white_tokens >= MAX_TOKENS: st.success("🎉 **HUMAN FACTION WINS!** Soul Cleansed.")
elif st.session_state.black_tokens >= MAX_TOKENS: st.error("🩸 **REJECTED FACTION WINS!** Darkness Wins.")
elif st.session_state.current_round >= MAX_ROUNDS:
    st.warning("⌛ **TIME LIMIT EXPIRED!** Checked Majority Tokens.")
