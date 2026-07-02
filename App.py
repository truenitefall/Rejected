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
    
    # Generate Decks from Production Quantities
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
    
    # Set Up Players
    st.session_state.players = {
        "Billy": {"alignment": "Human", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Billy"]},
        "Abagail": {"alignment": "Human", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Abagail"]},
        "Horatio": {"alignment": "Rejected", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Horatio"]},
        "Ormund": {"alignment": "Rejected", "health": INITIAL_HEALTH, "hand": [], "obj": st.session_state.objectives.pop(), "mat": CHARACTER_MATS["Ormund"]}
    }
    
    # Deal 3 Starting Cards Symmetrically
    for p, data in st.session_state.players.items():
        deck = st.session_state.selfless_deck if data["alignment"] == "Human" else st.session_state.selfish_deck
        data["hand"] = [deck.pop() for _ in range(3)]

def log(msg):
    st.session_state.game_log.insert(0, f"Round {st.session_state.current_round}: {msg}")

# --- APP INTERFACE ---
st.set_page_config(page_title="Faction & Soul VTT", layout="centered")
st.title("🔮 Faction & Soul: Production Suite")

# TABS FOR CLEAN MOBILE NAVIGATION
tab_board, tab_mats, tab_rules = st.tabs(["🎮 Game Board", "🪪 Character Mats", "📜 Rulebook"])

# --- TAB 1: GAME BOARD ---
with tab_board:
    st.markdown("### 📊 Status HUD")
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Round", f"{st.session_state.current_round}/{MAX_ROUNDS}")
    c2.metric("⬜ White (Human)", f"{st.session_state.white_tokens}/{MAX_TOKENS}")
    c3.metric("⬛ Black (Rejected)", f"{st.session_state.black_tokens}/{MAX_TOKENS}")
    
    st.markdown("---")
    
    # 🎲 ACTION DICE ENGINE
    with st.expander("🎲 Action Dice Roller", expanded=False):
        if st.button("Roll 3 Action Dice", use_container_width=True):
            faces = ["💥 Persuasion", "🛡️ Resistance", "🎭 Manipulation", "💥 Persuasion", "✨ Wildcard", "💀 Mat Penalty"]
            rolls = [random.choice(faces) for _ in range(3)]
            st.success(f"Results: {', '.join(rolls)}")
            
    # ACTIVE PLAYER ACTION CENTER
    st.markdown("### 🏃 Active Turn Window")
    active_player = st.selectbox("Select Current Player:", list(st.session_state.players.keys()))
    p_data = st.session_state.players[active_player]
    
    # Render Mobile Mat Card
    bg = "#1e293b" if p_data["alignment"] == "Human" else "#3f1d1d"
    st.markdown(
        f"""<div style="background-color:{bg}; padding:15px; border-radius:8px; border:1px solid #475569; color:white;">
            <h4 style="margin:0;">{active_player} — Status: {p_data['alignment']}</h4>
            <p style="margin:5px 0 0 0; color:#cbd5e1;">Soul Health: <b>{p_data['health']}/{INITIAL_HEALTH} HP</b></p>
            <p style="margin:2px 0 0 0; color:#94a3b8; font-size:13px;">Objective: <i>{p_data['obj']}</i></p>
        </div>""", unsafe_allow_html=True
    )
    
    # Quick Status Modifiers
    b_c1, b_c2, b_c3 = st.columns(3)
    if b_c1.button("💥 Apply 1 Damage", key=f"d_{active_player}", use_container_width=True):
        p_data["health"] = max(0, p_data["health"] - 1)
        log(f"{active_player} takes 1 damage.")
        if p_data["health"] == 0:
            p_data["alignment"] = "Rejected" if p_data["alignment"] == "Human" else "Human"
            p_data["health"] = INITIAL_HEALTH
            log(f"💀 {active_player}'s soul shattered! Swapped alignment to {p_data['alignment']}.")
        st.rerun()
        
    if b_c2.button("❤️ Restore 1 HP", key=f"h_{active_player}", use_container_width=True):
        p_data["health"] = min(INITIAL_HEALTH, p_data["health"] + 1)
        log(f"{active_player} restored 1 health point.")
        st.rerun()
        
    if b_c3.button("🃏 Draw Faction Card", key=f"dr_{active_player}", use_container_width=True):
        deck = st.session_state.selfless_deck if p_data["alignment"] == "Human" else st.session_state.selfish_deck
        if deck:
            card = deck.pop()
            p_data["hand"].append(card)
            log(f"{active_player} drew a card.")
        else:
            st.error("Deck is completely depleted!")
        st.rerun()

    # HAND & ABILITY RESOLUTION ENGINE
    st.markdown("#### 🃏 Hand Management")
    if p_data["hand"]:
        selected_card = st.radio("Choose card to execute:", p_data["hand"], index=0, key=f"hand_{active_player}")
        
        # Pull card metadata dynamically from master libraries
        meta = SELFLESS_DECK_MASTER.get(selected_card) or SELFISH_DECK_MASTER.get(selected_card)
        st.info(f"**[{meta['type']}]** {meta['effect']}")
        
        target_entity = st.selectbox("Select Target (if card requires one):", list(st.session_state.players.keys()))
        
        if st.button(f"🔥 Confirm and Play: {selected_card}", use_container_width=True):
            # BALANCING RULE 1: Round 1 Alignment Shield
            if st.session_state.current_round == 1 and selected_card in ["Subjugation", "Absolution", "Damned Humans"]:
                st.error("🚫 Balanced Rule: Alignment protection is active on Round 1! No instant swaps allowed.")
            else:
                # Play logic execution
                p_data["hand"].remove(selected_card)
                log(f"{active_player} played '{selected_card}' targeting {target_entity}.")
                
                # Auto-apply macro modifications based on card text keywords
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
                        log(f"💀 Damage broke {target_entity}! Alignment forced to {t_data['alignment']}.")
                
                # BALANCING RULE 2: Gated health threshold for instant alignment flips
                elif selected_card in ["Subjugation", "Absolution"]:
                    t_data = st.session_state.players[target_entity]
                    if t_data["health"] > (INITIAL_HEALTH / 2):
                        st.warning(f"🛡️ Swap Failed! {target_entity} has more than 50% HP remaining.")
                    else:
                        t_data["alignment"] = "Rejected" if selected_card == "Subjugation" else "Human"
                        log(f"🔮 {selected_card} succeeded. {target_entity} flipped to {t_data['alignment']}.")
                        
                st.rerun()
    else:
        st.warning("No cards in hand. Draw a card using the button above.")

    # TRACK MANIPULATION & ROUND CONTROL
    st.markdown("---")
    st.markdown("### ⚙️ Direct Simulation Toggles")
    m_c1, m_c2, m_c3 = st.columns(3)
    if m_c1.button("⬜ +1 White", use_container_width=True):
        st.session_state.white_tokens = min(MAX_TOKENS, st.session_state.white_tokens + 1)
        st.rerun()
    if m_c2.button("⬛ +1 Black", use_container_width=True):
        st.session_state.black_tokens = min(MAX_TOKENS, st.session_state.black_tokens + 1)
        st.rerun()
    if m_c3.button("➡️ End Round", type="primary", use_container_width=True):
        if st.session_state.current_round < MAX_ROUNDS:
            st.session_state.current_round += 1
            log("Advanced round timer.")
        st.rerun()

    # GAME OVER EVALUATIONS
    if st.session_state.white_tokens >= MAX_TOKENS:
        st.balloons()
        st.success("🎉 **HUMAN FACTION VICTORY!** The Unwilling Child's soul is secure.")
    elif st.session_state.black_tokens >= MAX_TOKENS:
        st.snow()
        st.error("🩸 **REJECTED FACTION VICTORY!** The child has fallen to the dark.")
    elif st.session_state.current_round >= MAX_ROUNDS:
        st.info("⌛ **DOOM CLOCK EXPIRED (8 Rounds Max)!**")
        if st.session_state.white_tokens > st.session_state.black_tokens:
            st.success("Humans win on token majority points!")
        elif st.session_state.black_tokens > st.session_state.white_tokens:
            st.error("Rejected wins on token majority points!")
        else:
            st.warning("Absolute Stalemate!")

    # SYSTEM LOGGER
    with st.expander("📜 System Telemetry Log", expanded=True):
        st.text_area("Live Log Output", value="\n".join(st.session_state.game_log), height=150, disabled=True)

# --- TAB 2: CHARACTER MATS REFERENCE ---
with tab_mats:
    st.markdown("### 🪪 Structural Modifiers Directory")
    for name, directions in CHARACTER_MATS.items():
        st.markdown(f"#### 👤 {name}")
        st.write(f"- ⬆️ **Top:** {directions['Top']}")
        st.write(f"- ➡️ **Right:** {directions['Right']}")
        st.write(f"- ⬇️ **Bottom:** {directions['Bottom']}")
        st.write(f"- ⬅️ **Left:** {directions['Left']}")
        st.markdown("---")

# --- TAB 3: RULEBOOK ---
with tab_rules:
    st.markdown("### 📜 Core Production Rulebook")
    st.markdown(
        """
        1. **Objective:** Humans win if the Child's track hits 10 White Tokens. The Rejected win if it hits 10 Black Tokens. 
        2. **Turn Sequence:** Roll 3 Action Dice ➡️ Gather Resources ➡️ Activate Mat Modifiers (Optional) ➡️ Play Faction Cards.
        3. **Soul Shaking (Health):** Characters start with 6 HP. If reduced to 0 HP, they do not die—their soul shatters, flipping their Alignment to the opposing side, and resets back to full 6 HP.
        4. **Balancing Fix - Shielding:** Alignments cannot be forced or flipped instantly during **Round 1**.
        5. **Balancing Fix - Threshold:** Instant alignment-flipping cards (*Subjugation*, *Absolution*) require the target player to be weakened below 50% health (3 HP or lower) to succeed.
        6. **Doom Clock:** If neither side claims the Child by the end of Round 8, the team with the most tokens wins.
        """
)
