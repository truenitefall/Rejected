import streamlit as st
import random

# --- PRODUCTION CONFIG & DATABASE ---
MAX_TOKENS = 10
MAX_ROUNDS = 8
INITIAL_HEALTH = 6

# Full 70-Card Production Selfish Deck
SELFISH_DECK_MASTER = {
    "Soul Rend": {"qty": 6, "type": "Persuasion", "effect": "Deal 2 damage to any Human player."},
    "Childish Screams": {"qty": 5, "type": "Persuasion", "effect": "Collect 2 Black Tokens from the Unwilling Child."},
    "Claws of Fury": {"qty": 5, "type": "Persuasion", "effect": "Deals 1 damage per Rejected player in play to any 1 Human."},
    "Wails of Despair": {"qty": 5, "type": "Persuasion", "effect": "Collect 1 Black token from the Unwilling Child."},
    "Hurt Them": {"qty": 4, "type": "Persuasion", "effect": "Deal 1 Damage to ANY Player."},
    "Kill Them": {"qty": 3, "type": "Persuasion", "effect": "Deal 2 Damage to ANY Player."},
    "Murder": {"qty": 2, "type": "Persuasion", "effect": "Deal 1 damage to all Humans."},
    "Murderous Rage": {"qty": 2, "type": "Persuasion", "effect": "Target Human must attack any other Human in play."},
    "Night Terrors": {"qty": 4, "type": "Persuasion", "effect": "Do 1 point of damage to a Human of your choice."},
    "Altered Mindstate": {"qty": 3, "type": "Persuasion", "effect": "All Human players lose 1 point of your choice from Spirit Pool."},
    "Depression": {"qty": 2, "type": "Persuasion", "effect": "Target Human loses all Resistance points in their Spirit Pool."},
    "Secrets": {"qty": 2, "type": "Persuasion", "effect": "Target Human loses their turn this round."},
    "Mind Over Matter": {"qty": 2, "type": "Persuasion", "effect": "Destroy one Terrain card in play."},
    "Subjugation": {"qty": 2, "type": "Persuasion", "effect": "Turn any Unwilling Human immediately to Rejected. (Gated: Target must be < 50% HP)"},
    "Darkness": {"qty": 4, "type": "Resistance", "effect": "Any damage done to Rejected player is reduced by 1."},
    "Embrace the Darkness": {"qty": 4, "type": "Resistance", "effect": "Target Rejected will heal 1 Soul Point."},
    "From Whence It Came": {"qty": 3, "type": "Resistance", "effect": "Return 1 card of any type to your hand from the discard pile."},
    "Take the Child": {"qty": 4, "type": "Resistance", "effect": "Prevent 1 point of damage from being dealt to Child."},
    "The Fire Burns": {"qty": 2, "type": "Psyche", "effect": "Every round, deal 1 damage to all Humans, and Heal 1 damage to all Rejected."},
    "Commanding Aura": {"qty": 2, "type": "Psyche", "effect": "All Rejected players gain 1 point of their choosing to their Spirit Pool."},
    "Massive Subjugation": {"qty": 2, "type": "Psyche", "effect": "Every human player loses 1 point of their choosing from their spirit pool."},
    "Master of None": {"qty": 1, "type": "Psyche", "effect": "The Child may not take damage while this card is in play."},
    "Power of Choice": {"qty": 2, "type": "Psyche", "effect": "Change any 1 die to another side every roll."},
    "Call Me Mr. Teeth": {"qty": 2, "type": "Champion", "effect": "Summon Mr. Teeth into play."}
}

# Full 70-Card Production Selfless Deck
SELFLESS_DECK_MASTER = {
    "Protect the Child": {"qty": 3, "type": "Persuasion", "effect": "Collect 3 White Tokens from the Unwilling Child."},
    "Awe, A Baby": {"qty": 5, "type": "Persuasion", "effect": "Collect 2 White Tokens from the Unwilling Child."},
    "A Mother's Care": {"qty": 6, "type": "Persuasion", "effect": "Collect 1 White Token from the Unwilling Child."},
    "Fend Them Off": {"qty": 5, "type": "Persuasion", "effect": "Collect 1 White Token OR Deal 1 point of damage to Rejected Player."},
    "Fight the Darkness": {"qty": 5, "type": "Persuasion", "effect": "Deal 1 point of Damage to any Rejected player."},
    "Hit Them Where It Hurts": {"qty": 4, "type": "Persuasion", "effect": "Deal 2 Damage to any Rejected Player."},
    "Crush Them": {"qty": 4, "type": "Persuasion", "effect": "Deal 2 Damage to ANY Player."},
    "Our Souls Are Ours": {"qty": 2, "type": "Persuasion", "effect": "Deal 1 Damage to All Rejected Players."},
    "Mine!": {"qty": 3, "type": "Persuasion", "effect": "Take 1 random card from ANY Player."},
    "Enticement": {"qty": 2, "type": "Persuasion", "effect": "Target Rejected must attack any other Rejected in play."},
    "Absolution": {"qty": 2, "type": "Persuasion", "effect": "Target Rejected instantly turns to Human. (Gated: Target must be < 50% HP)"},
    "Shrug It Off": {"qty": 6, "type": "Resistance", "effect": "Ignore 1 point of Damage."},
    "Be Gone Demon!": {"qty": 2, "type": "Resistance", "effect": "Heal any Human Player back to Full Health."},
    "Confession": {"qty": 2, "type": "Persuasion", "effect": "Target Rejected player loses next turn."},
    "Damned Humans": {"qty": 2, "type": "Resistance", "effect": "Turn ANY Player to Rejected or Human."},
    "Deal Me In": {"qty": 4, "type": "Resistance", "effect": "Draw 3 additional cards."},
    "Embrace the Light": {"qty": 4, "type": "Resistance", "effect": "Target Human will heal 1 soul point."},
    "Lend a Hand": {"qty": 3, "type": "Resistance", "effect": "Gain 1 soul point."},
    "Love of a Mother": {"qty": 4, "type": "Resistance", "effect": "Prevent 1 point of damage from being dealt to Child."},
    "Rebirth": {"qty": 3, "type": "Resistance", "effect": "Return 1 card from discard pile to hand."},
    "Sacrifice": {"qty": 2, "type": "Resistance", "effect": "For every soul point sacrificed, discard 2 cards from hand or play."},
    "The World Is Ours": {"qty": 2, "type": "Psyche", "effect": "Every Round, Each Human takes 1 White Token from the Unwilling Child."},
    "We Are One": {"qty": 2, "type": "Psyche", "effect": "Each Human Heals 1 Soul Point Each Round."},
    "Make Your Choice": {"qty": 2, "type": "Psyche", "effect": "Change any 1 die to another side every roll."},
    "She Is the One": {"qty": 2, "type": "Champion", "effect": "Summon Miranda into play."}
}

CHARACTER_MATS = {
    "Billy": {"Top": "🔥 Persuasion +2 / No Penalty", "Right": "🎭 Manipulation +2 / -1 Manipulation Point", "Bottom": "🛡️ Resistance +2 / -1 Resistance Point", "Left": "🎲 Reroll 1 Action Die / -2 Persuasion Points"},
    "Abagail": {"Top": "🔥 Target Persuasion +2 / No Penalty", "Right": "🎭 Target Manipulation +2 / -1 Persuasion Point", "Bottom": "🛡️ Target Resistance +2 / -2 Resistance Points", "Left": "🔥 Own Persuasion +2 / Lose 1 Action Die"},
    "Horatio": {"Top": "🎭 Manipulation +2 / No Penalty", "Right": "🎲 Reroll 1 Action Die / -1 Manipulation Point", "Bottom": "🃏 Draw 1 Free Card / -2 Manipulation Points", "Left": "🔥 Persuasion +2 / Lose 1 Action Die"},
    "Ormund": {"Top": "🎭 Own Manipulation +2 / No Penalty", "Right": "🃏 Play Card No Cost / -1 Manipulation Point", "Bottom": "🛡️ Target Resistance +2 / -1 HP", "Left": "🎭 Target Manipulation +2 / Discard 1 Card"}
}

SECRET_OBJECTIVES = [
    "Collect 3 white tokens from the unwilling child.", "Collect 3 black tokens from the unwilling child.",
    "Turn 2 players from unwilling to rejected.", "Turn 2 players from rejected to unwilling.",
    "Collect the last black token from unwilling child turning it rejected.", "Collect the last white token from unwilling child saving its soul.",
    "Turn to an unwilling from a rejected.", "Turn to a rejected from an unwilling.",
    "Summon Mr Teeth to the field of play.", "Summon Miranda to the field of play."
]

# --- SESSION STATE INITIALIZATION ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_round = 1
    st.session_state.white_tokens = 0
    st.session_state.black_tokens = 0
    st.session_state.game_log = ["System online. Production decks mixed and shuffled."]
    
    st.session_state.selfish_deck = []
    for card, meta in SELFISH_DECK_MASTER.items():
        st.session_state.selfish_deck.extend([card] * meta["qty"])
    random.shuffle(st.session_state.selfish_deck)
    
    st.session_state.selfless_deck = []
    for card, meta in SELFLESS_DECK_MASTER.items():
        st.session_state.selfless_deck.extend([card] * meta["qty"])
    random.shuffle(st.session_state.selfless_deck)
    
    st.session_state.objectives = list(SECRET_OBJECTIVES)
    random.shuffle(st.session_state.objectives)
    
    st.session_state.players = {
        "Billy": {"alignment": "Human", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Billy"]},
        "Abagail": {"alignment": "Human", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Abagail"]},
        "Horatio": {"alignment": "Rejected", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Horatio"]},
        "Ormund": {"alignment": "Rejected", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Ormund"]}
    }
    
    for p, data in st.session_state.players.items():
        deck = st.session_state.selfless_deck if data["alignment"] == "Human" else st.session_state.selfish_deck
        data["hand"] = [deck.pop() for _ in range(3)]

def log(msg):
    st.session_state.game_log.insert(0, f"Round {st.session_state.current_round}: {msg}")

# --- THEMATIC PARCHMENT SKIN ENGINE ---
st.set_page_config(page_title="Faction & Soul VTT", layout="centered")

st.markdown(
    """
    <style>
    /* Global application canvas modifications */
    .stApp {
        background-color: #110d0a !important;
    }
    h1, h2, h3, h4 {
        color: #d4af37 !important;
        font-family: 'Georgia', serif;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    /* Custom CSS Parchment Card Simulation */
    .parchment-container {
        background-color: #f2e6ce !important;
        background-image: radial-gradient(circle, #fcf5e3 0%, #e6d3af 100%) !important;
        padding: 20px;
        border-radius: 6px;
        border: 3px double #8a6d3b;
        box-shadow: inset 0 0 20px rgba(138,109,59,0.4), 3px 3px 10px rgba(0,0,0,0.6);
        color: #2b1f11 !important;
        margin-bottom: 15px;
        font-family: 'Georgia', serif;
    }
    .parchment-container h4 {
        color: #5c0606 !important;
        border-bottom: 1px solid #8a6d3b;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a89276 !important;
        font-family: 'Georgia', serif;
    }
    .stTabs [aria-selected="true"] {
        color: #d4af37 !important;
        border-bottom-color: #d4af37 !important;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🔮 Faction & Soul: Ultimate Production Sandbox")

tab_board, tab_mats, tab_rules = st.tabs(["🎮 Interactive Board", "🪪 Parchment Mats", "📜 Canonical Rulebook"])

# --- TAB 1: INTERACTIVE BOARD ---
with tab_board:
    st.markdown("### 📊 Active Game State")
    c1, c2, c3 = st.columns(3)
    c1.metric("Doom Round Counter", f"{st.session_state.current_round}/{MAX_ROUNDS}")
    c2.metric("⬜ White Core Soul Tokens", f"{st.session_state.white_tokens}/{MAX_TOKENS}")
    c3.metric("⬛ Black Corruption Tokens", f"{st.session_state.black_tokens}/{MAX_TOKENS}")
    
    st.markdown("---")
    
    with st.expander("🎲 Physical Action Dice Simulator", expanded=False):
        if st.button("Cast 3 Physical Dice", use_container_width=True):
            faces = ["💥 Persuasion", "🛡️ Resistance", "🎭 Manipulation", "💥 Persuasion", "✨ Wildcard", "💀 Mat Penalty Trigger"]
            rolls = [random.choice(faces) for _ in range(3)]
            st.success(f"Cast Array: {', '.join(rolls)}")
            
    st.markdown("### 🏃 Strategic Play Windows")
    active_player = st.selectbox("Turn Operator Selection:", list(st.session_state.players.keys()))
    p_data = st.session_state.players[active_player]
    
    # Fully Skinned Parchment Frame for Selected Active Character Mat
    st.markdown(
        f"""<div class="parchment-container">
            <h4>🎭 MAT ARCHETYPE: {active_player.upper()}</h4>
            <p style='margin:4px 0;'>Current Alignment: <b>{p_data['alignment'].upper()}</b></p>
            <p style='margin:4px 0;'>Vitality Pool: <span style='color:#a61c1c; font-weight:bold;'>{p_data['health']} / {INITIAL_HEALTH} HP</span></p>
            <p style='margin:4px 0; font-size:13px; border-top: 1px dashed #8a6d3b; padding-top:4px;'>
                <b>Secret Vault Agenda:</b> <i>{p_data['obj']}</i>
            </p>
        </div>""", unsafe_allow_html=True
    )
    
    b_c1, b_c2, b_c3 = st.columns(3)
    if b_c1.button("💥 Inflict 1 Wound", key=f"d_{active_player}", use_container_width=True):
        p_data["health"] = max(0, p_data["health"] - 1)
        log(f"{active_player} took 1 point of structural damage.")
        if p_data["health"] == 0:
            p_data["alignment"] = "Rejected" if p_data["alignment"] == "Human" else "Human"
            p_data["health"] = INITIAL_HEALTH
            log(f"💀 CRITICAL REVERSAL: {active_player} broke entirely! Flipped to {p_data['alignment']}.")
        st.rerun()
        
    if b_c2.button("❤️ Rejuvenate 1 HP", key=f"h_{active_player}", use_container_width=True):
        p_data["health"] = min(INITIAL_HEALTH, p_data["health"] + 1)
        log(f"{active_player} mended 1 wound point.")
        st.rerun()
        
    if b_c3.button("🃏 Pull Faction Card", key=f"dr_{active_player}", use_container_width=True):
        deck = st.session_state.selfless_deck if p_data["alignment"] == "Human" else st.session_state.selfish_deck
        if deck:
            p_data["hand"].append(deck.pop())
            log(f"{active_player} drew an alignment card from their stack.")
        st.rerun()

    st.markdown("#### 🃏 Production Hand Registry")
    if p_data["hand"]:
        selected_card = st.radio("Choose Card Option:", p_data["hand"], index=0, key=f"hand_{active_player}")
        meta = SELFLESS_DECK_MASTER.get(selected_card) or SELFISH_DECK_MASTER.get(selected_card)
        
        # Display individual card layout as a parchment slip
        st.markdown(
            f"""<div class="parchment-container" style="padding:10px 15px; border:1px solid #8a6d3b;">
                <b style="color:#5c0606;">📜 CARD: {selected_card} [{meta['type'].upper()}]</b><br/>
                <span style="font-size:14px; color:#3d2b19;">{meta['effect']}</span>
            </div>""", unsafe_allow_html=True
        )
        
        target_entity = st.selectbox("Declare Target Vector:", list(st.session_state.players.keys()))
        
        if st.button(f"🔥 Strike Deck / Play Card: {selected_card}", use_container_width=True):
            # BALANCING GATEKEEPER 1: Round 1 Shield
            if st.session_state.current_round == 1 and selected_card in ["Subjugation", "Absolution", "Damned Humans"]:
                st.error("🚫 SANCTION RULE: The alignment protective fields prevent forced alignment changes on Round 1.")
            else:
                p_data["hand"].remove(selected_card)
                log(f"{active_player} casted card '{selected_card}' target: {target_entity}.")
                
                if "White Token" in meta["effect"]:
                    st.session_state.white_tokens = min(MAX_TOKENS, st.session_state.white_tokens + (3 if "3" in meta["effect"] else 2 if "2" in meta["effect"] else 1))
                elif "Black Token" in meta["effect"]:
                    st.session_state.black_tokens = min(MAX_TOKENS, st.session_state.black_tokens + (3 if "3" in meta["effect"] else 2 if "2" in meta["effect"] else 1))
                elif "2 damage" in meta["effect"] or "2 Damage" in meta["effect"]:
                    t_data = st.session_state.players[target_entity]
                    t_data["health"] = max(0, t_data["health"] - 2)
                    if t_data["health"] == 0:
                        t_data["alignment"] = "Rejected" if t_data["alignment"] == "Human" else "Human"
                        t_data["health"] = INITIAL_HEALTH
                        log(f"💀 CRISIS: {target_entity} shattered under heavy damage, shifting to {t_data['alignment']}!")
                
                # BALANCING GATEKEEPER 2: 50% HP threshold restriction
                elif selected_card in ["Subjugation", "Absolution"]:
                    t_data = st.session_state.players[target_entity]
                    if t_data["health"] > (INITIAL_HEALTH / 2):
                        st.warning(f"🛡️ PARRIED: {target_entity} possesses too much spiritual fortitude (>50% HP) to be instantly converted.")
                    else:
                        t_data["alignment"] = "Rejected" if selected_card == "Subjugation" else "Human"
                        log(f"🔮 TRANSMUTED: {selected_card} succeeded. {target_entity} turned into {t_data['alignment']}.")
                        
                st.rerun()
    else:
        st.warning("Hand is empty.")

    st.markdown("---")
    st.markdown("### ⚙️ Direct Token Toggles")
    m_c1, m_c2, m_c3 = st.columns(3)
    if m_c1.button("⬜ Add +1 White", use_container_width=True):
        st.session_state.white_tokens = min(MAX_TOKENS, st.session_state.white_tokens + 1)
        st.rerun()
    if m_c2.button("⬛ Add +1 Black", use_container_width=True):
        st.session_state.black_tokens = min(MAX_TOKENS, st.session_state.black_tokens + 1)
        st.rerun()
    if m_c3.button("➡️ Step Round Phase", type="primary", use_container_width=True):
        if st.session_state.current_round < MAX_ROUNDS:
            st.session_state.current_round += 1
            log("Advanced current turn timer.")
        st.rerun()

    if st.session_state.white_tokens >= MAX_TOKENS: st.success("🎉 HUMAN FACTION TRIUMPHS! Soul Salvaged.")
    elif st.session_state.black_tokens >= MAX_TOKENS: st.error("🩸 REJECTED FACTION TRIUMPHS! The dark claims all.")
    elif st.session_state.current_round >= MAX_ROUNDS:
        st.info("⌛ MAX ROUNDS REACHED: Resolving token scale counts...")
        if st.session_state.white_tokens > st.session_state.black_tokens: st.success("Humans win via resource concentration edge!")
        elif st.session_state.black_tokens > st.session_state.white_tokens: st.error("Corruption wins via structural saturation edge!")

    with st.expander("📜 Battle Feed Logs", expanded=True):
        st.text_area("Live Telemetry", value="\n".join(st.session_state.game_log), height=140, disabled=True)

# --- TAB 2: PARCHMENT MATS ---
with tab_mats:
    st.markdown("### 🪪 Character Mat Modifiers & Penalties")
    for name, directions in CHARACTER_MATS.items():
        st.markdown(
            f"""<div class="parchment-container">
                <h4 style="color:#5c0606; margin-top:0;">📜 CHARACTER MANIFEST: {name.upper()}</h4>
                <ul>
                    <li><b>⬆️ TOP (Neutral Zone):</b> {directions['Top']}</li>
                    <li><b>➡️ RIGHT (Action Shift):</b> {directions['Right']}</li>
                    <li><b>⬇️ BOTTOM (Deep Strategy):</b> {directions['Bottom']}</li>
                    <li><b>⬅️ LEFT (Crisis Pivot):</b> {directions['Left']}</li>
                </ul>
            </div>""", unsafe_allow_html=True
        )

# --- TAB 3: COMPLETE CANONICAL RULEBOOK ---
with tab_rules:
    st.markdown(
        """<div class="parchment-container" style="font-size:15px; line-height:1.6; text-align:justify;">
            <h3 style="text-align:center; color:#5c0606; margin-top:0;">📜 THE OFFICIAL CODEX OF FACTION & SOUL</h3>
            <p style="text-align:center; font-style:italic; font-size:13px; margin-top:-10px;">A High-Stakes Battle for the Essence of the Unwilling Child</p>
            
            <hr style="border-top:1px solid #8a6d3b; margin:10px 0;"/>
            
            <b>SECTION I: MASTER OVERVIEW</b><br/>
            Faction & Soul is a highly competitive, fast-paced tactical card game for 4 players divided into two shifting secret alliances: The <b>Humans (Selfless Faction)</b> and The <b>Rejected (Selfish Faction)</b>. The battlefield centers around the <i>Unwilling Child</i>,
