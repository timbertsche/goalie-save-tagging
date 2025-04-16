
import streamlit as st
import pandas as pd

# Session init
if "data" not in st.session_state:
    st.session_state["data"] = []

# Button-Auswahl-Funktion
def button_select(label, options, key_prefix):
    st.markdown(f"**{label}**")
    selected = st.session_state.get(f"{key_prefix}_selected", None)
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option, key=f"{key_prefix}_{option}"):
            st.session_state[f"{key_prefix}_selected"] = option
            selected = option
    if selected:
        st.info(f"Ausgewählt: {selected}")
    return selected

# Eingabeformular
with st.form("save_form"):
    st.title("🏒 Goalie Save Tagging")

    situation = button_select("1. Situation", ["A-Save", "B-Save", "C-Save"], "situation")
    movement = button_select("2. Set / Movement", ["Set-Save", "Movement Save"], "movement")
    tactic = button_select("3. Taktische Situation", ["Off the Rush", "FC", "D-Zone", "Out of Zone"], "tactic")
    play = button_select("4. Play", [
        "Clean Shot", "Pass", "Lateral Pass", "Lateral Movement",
        "Low to High", "Net Attack", "Breakaway", "Rebounds",
        "Redirects", "Screen", "Broken Play"
    ], "play")

    outcome = button_select("5. Outcome", ["Freezed", "Rebound"], "outcome")

    # Nur bei "Rebound"
    outcome_rebound = None
    rebound_control = None
    if outcome == "Rebound":
        outcome_rebound = button_select("6. Outcome Rebound", ["Slot Rebound", "Outside Rebound"], "outcome_rebound")
        rebound_control = button_select("7. Control / Uncontrol", ["Controlled Rebound", "Uncontrolled Rebound"], "rebound_control")

    # Nur bei "Breakaway"
    breakaway_type = None
    if play == "Breakaway":
        breakaway_type = button_select("8. Type Breakaway", ["Deke", "Shot"], "breakaway_type")

    notes = st.text_area("📝 Notizen")

    submitted = st.form_submit_button("Save")

    if submitted:
        entry = {
            "Situation": situation,
            "Set/Movement": movement,
            "Tactical Situation": tactic,
            "Play": play,
            "Outcome": outcome,
            "Outcome Rebound": outcome_rebound,
            "Rebound Control": rebound_control,
            "Breakaway Type": breakaway_type,
            "Notes": notes
        }
        st.session_state["data"].append(entry)
        st.success("✅ Save gespeichert")

# Daten anzeigen & exportieren
if st.session_state["data"]:
    df = pd.DataFrame(st.session_state["data"])
    st.write("📊 Aktuelle Saves:")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export als CSV", csv, "goalie_saves.csv", "text/csv")
