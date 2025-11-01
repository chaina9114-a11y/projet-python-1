# app.py — Trading Journal
# -----------------------------------------------------------
# Points clés:
# - 2 CSV dans /data : trades.csv et daily.csv
# - Page "Journal": saisie rapide + notes du jour + édition/suppression
# - Page "Progress": KPIs, equity curve animée (~2s), totaux Weekly/Monthly
# - On utilise SEULEMENT "result_usd" pour la perf (pas de PnL technique)
# - Colonne "id" et "strategy" masquées dans l'UI (compatibilité CSV)
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import time
from datetime import datetime, date, time as dtime
from pathlib import Path
import altair as alt

st.set_page_config(page_title="🗒️ Trading Journal", layout="wide")

# ---------- Constantes / Schémas ----------
DATA_DIR = Path("data")
TRADES_CSV = DATA_DIR / "trades.csv"
DAILY_CSV  = DATA_DIR / "daily.csv"

TRADE_COLUMNS = [
    "id","date","time","session","ticker","side",
    "quantity","entry","exit","strategy","notes",
    "result_usd"
]
DAILY_COLUMNS = [
    "date","mood","confidence","day_type","day_result","day_pl","sessions",
    "day_notes","lesson","checklist_ok","screenshot_path"
]

MOODS = ["😄","🙂","😐","😕","😫"]
DAY_TYPES = ["Green","Red","Flat"]
DAY_RESULT = ["No trade","Positive (+)","Negative (-)"]
SESSIONS = ["Asia","London","NY"]


# ---------- Petites fonctions utilitaires ----------
def ensure_datafiles():
    """Crée le dossier /data et les deux CSV vides si besoin."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TRADES_CSV.exists():
        pd.DataFrame(columns=TRADE_COLUMNS).to_csv(TRADES_CSV, index=False)
    if not DAILY_CSV.exists():
        pd.DataFrame(columns=DAILY_COLUMNS).to_csv(DAILY_CSV, index=False)

def coerce_trades_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Garantit que trades.csv a les bonnes colonnes + bons types."""
    for col in TRADE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0 if col in ["quantity","entry","exit","result_usd"] else ""
    if "date" in df: df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    for c in ["quantity","entry","exit","result_usd"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["session","ticker","side","strategy","notes","time"]:
        df[c] = df[c].astype(str)
    return df[TRADE_COLUMNS]

def load_trades() -> pd.DataFrame:
    ensure_datafiles()
    df = pd.read_csv(TRADES_CSV)
    return coerce_trades_schema(df) if not df.empty else pd.DataFrame(columns=TRADE_COLUMNS)

def save_trades(df: pd.DataFrame):
    coerce_trades_schema(df).to_csv(TRADES_CSV, index=False)

def load_daily() -> pd.DataFrame:
    ensure_datafiles()
    df = pd.read_csv(DAILY_CSV)
    if df.empty:
        return pd.DataFrame(columns=DAILY_COLUMNS)
    if "date" in df: df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    for c in ["confidence","day_pl"]:
        if c in df: df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["mood","day_type","day_result","sessions","day_notes","lesson","screenshot_path"]:
        if c in df: df[c] = df[c].astype(str)
    if "checklist_ok" in df: df["checklist_ok"] = df["checklist_ok"].fillna(False).astype(bool)
    for col in DAILY_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col in ["mood","day_type","day_result","sessions","day_notes","lesson","screenshot_path"] else 0
    return df[DAILY_COLUMNS]

def save_daily(df: pd.DataFrame):
    df = df.copy()
    for col in DAILY_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col in ["mood","day_type","day_result","sessions","day_notes","lesson","screenshot_path"] else 0
    df[DAILY_COLUMNS].to_csv(DAILY_CSV, index=False)

def animate_line_chart(df: pd.DataFrame, x_col: str, y_col: str, total_seconds: float = 2.0):
    """Affiche une ligne Altair avec une petite animation (dessin en ~2s)."""
    placeholder = st.empty()
    frames = min(30, max(2, len(df)))
    def render(dfi):
        chart = (alt.Chart(dfi)
                 .mark_line()
                 .encode(
                    x=alt.X(f"{x_col}:T", title="Date"),
                    y=alt.Y(f"{y_col}:Q", title="Equity ($)"),
                    tooltip=[alt.Tooltip(f"{x_col}:T", title="Date"),
                             alt.Tooltip(f"{y_col}:Q", title="Equity ($)", format=".2f")]
                 ).properties(height=260))
        placeholder.altair_chart(chart, use_container_width=True)
    for i in range(1, frames+1):
        idx = max(1, round(len(df) * i / frames))
        render(df.iloc[:idx])
        time.sleep(total_seconds/frames)


# ---------- UI ----------
st.title("🗒️ Trading Journal")

with st.sidebar:
    page = st.radio("Navigation", ["📝 Journal","📈 Progress"], index=0)
    st.markdown("---")
    if st.button("🗑️ Reset ALL data", use_container_width=True):
        pd.DataFrame(columns=TRADE_COLUMNS).to_csv(TRADES_CSV, index=False)
        pd.DataFrame(columns=DAILY_COLUMNS).to_csv(DAILY_CSV, index=False)
        st.success("All data cleared.")

# ---------------- PAGE 1 — JOURNAL ----------------
if page.startswith("📝"):
    # Texte d'accueil demandé (anglais, exact)
    st.markdown("""
**Welcome to your trading journal !**  
This tool helps you **track your trades** and **see your progress** over time — simply and without hassle.  
Stay disciplined, take honest notes… and watch your equity curve grow 📈.
""")

    # --- Quick Trade Entry ---
    st.subheader("Quick Trade Entry")
    with st.form("quick_trade_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([1,1,1,2])
        with c1:
            t_date = st.date_input("Trade Date", value=date.today())
            t_time = st.time_input("Time", value=dtime(datetime.now().hour, datetime.now().minute))
        with c2:
            session = st.selectbox("Session", SESSIONS, index=1)  # London par défaut
            ticker = st.text_input("Pair (Ticker)", placeholder="DJ30, XAUUSD…").upper()
        with c3:
            entry = st.number_input("Entry Price", min_value=0.0, step=0.0001, format="%.4f")
            exit_  = st.number_input("Exit Price",  min_value=0.0, step=0.0001, format="%.4f")
        with c4:
            side = st.selectbox("Side", ["Long","Short"], index=0)
            notes = st.text_area("Notes (optional)", height=70)
            qty = st.number_input("Lot size (Quantity)", min_value=0.0, step=0.01, value=0.10, format="%.2f")
            result_usd = st.number_input("Result ($) — your own P/L", step=1.0, value=0.0, format="%.2f",
                                         help="Ex: +200 = 200$ profit, -47 = 47$ loss")

        if st.form_submit_button("➕ Add trade", use_container_width=True):
            if not ticker or entry <= 0 or exit_ <= 0 or qty <= 0:
                st.error("Please fill Pair, Entry Price, Exit Price and Lot size (>0).")
            else:
                new_row = pd.DataFrame([{
                    "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    "date": t_date.isoformat(),
                    "time": t_time.strftime("%H:%M"),
                    "session": session,
                    "ticker": ticker.upper(),
                    "side": side,
                    "quantity": float(qty),
                    "entry": float(entry),
                    "exit": float(exit_),
                    "strategy": "",      # laissé vide, colonne masquée dans l'UI
                    "notes": notes,
                    "result_usd": float(result_usd),
                }])
                df = load_trades()
                save_trades(pd.concat([df, new_row], ignore_index=True))
                st.success(f"Saved: {ticker.upper()} {side} | Qty={qty:.2f} | Result=${result_usd:.2f}")

    # --- Daily Notes ---
    st.markdown("### Daily Notes")
    with st.form("daily_notes_form", clear_on_submit=True):
        d1, d2, d3 = st.columns([1,1,2])
        with d1:
            j_date = st.date_input("Date", value=date.today())
            mood = st.selectbox("Mood", MOODS, index=1)
            day_type = st.selectbox("Day type", DAY_TYPES, index=0)
        with d2:
            confidence = st.slider("Confidence", 0, 100, 70)
            day_result = st.selectbox("Result of the day", DAY_RESULT, index=0)
            day_pl = st.number_input("Daily P/L (no fees)", value=0.0, step=1.0)
            sessions_used = st.multiselect("Sessions attended", SESSIONS)
            checklist_ok = st.checkbox("Checklist OK (rules respected)", value=True)
        with d3:
            day_notes = st.text_area("Global notes (day)", placeholder="What went well / what to improve", height=110)
            lesson = st.text_input("Key lesson (one sentence)")
        if st.form_submit_button("Save daily notes", use_container_width=True):
            ddf = load_daily()
            ddf = ddf[ddf["date"] != j_date]  # garde la dernière version de la journée
            new_row = pd.DataFrame([{
                "date": j_date.isoformat(),
                "mood": mood,
                "confidence": confidence,
                "day_type": day_type,
                "day_result": day_result,
                "day_pl": day_pl,
                "sessions": ",".join(sessions_used),
                "day_notes": day_notes,
                "lesson": lesson,
                "checklist_ok": bool(checklist_ok),
                "screenshot_path": ""
            }])
            save_daily(pd.concat([ddf, new_row], ignore_index=True))
            st.success("Daily notes saved.")

    # --- Manage Trades (Edit/Delete) ---
    st.markdown("### Manage Trades (Edit / Delete)")
    tdf = load_trades()
    if tdf.empty:
        st.info("No trades yet.")
    else:
        if "delete" not in tdf.columns:
            tdf["delete"] = False
        from streamlit import column_config as cc
        edited = st.data_editor(
            tdf,
            use_container_width=True,
            num_rows="fixed",
            # On cache 'id' et 'strategy' en ne les mettant pas dans l'ordre des colonnes
            column_order=["date","time","session","ticker","side","quantity","entry","exit","notes","result_usd","delete"],
            column_config={
                "date": cc.DateColumn("date", format="YYYY-MM-DD"),
                "time": cc.Column("time", help="HH:MM"),
                "session": cc.SelectboxColumn("session", options=SESSIONS),
                "ticker": cc.Column("ticker"),
                "side": cc.SelectboxColumn("side", options=["Long","Short"]),
                "quantity": cc.NumberColumn("quantity", step=0.01, min_value=0.0),
                "entry": cc.NumberColumn("entry", step=0.0001, format="%.4f", min_value=0.0),
                "exit": cc.NumberColumn("exit", step=0.0001, format="%.4f", min_value=0.0),
                "notes": cc.Column("notes"),
                "result_usd": cc.NumberColumn("result_usd", step=1.0),
                "delete": cc.CheckboxColumn("delete"),
            },
            hide_index=True,
        )
        c1, c2 = st.columns(2)
        if c1.button("💾 Save changes (trades)", use_container_width=True):
            edited = edited[edited.get("delete", False) == False].drop(columns=["delete"], errors="ignore")
            if not edited.empty:
                edited["date"] = pd.to_datetime(edited["date"], errors="coerce").dt.date
                for c in ["quantity","entry","exit","result_usd"]:
                    if c in edited: edited[c] = pd.to_numeric(edited[c], errors="coerce").fillna(0.0)
                edited["ticker"] = edited["ticker"].astype(str).str.upper()
            save_trades(edited)
            st.success("Trades saved.")
        if c2.button("↩️ Reload trades", use_container_width=True):
            st.rerun()

    # --- Manage Daily Notes (Edit/Delete) ---
    st.markdown("### Manage Daily Notes (Edit / Delete)")
    ndf = load_daily()
    if ndf.empty:
        st.info("No daily notes yet.")
    else:
        if "delete" not in ndf.columns:
            ndf["delete"] = False
        from streamlit import column_config as cc
        edited_notes = st.data_editor(
            ndf,
            use_container_width=True,
            num_rows="fixed",
            column_config={
                "date": cc.DateColumn("date", format="YYYY-MM-DD"),
                "mood": cc.SelectboxColumn("mood", options=MOODS),
                "confidence": cc.NumberColumn("confidence", min_value=0, max_value=100, step=1),
                "day_type": cc.SelectboxColumn("day_type", options=DAY_TYPES),
                "day_result": cc.SelectboxColumn("day_result", options=DAY_RESULT),
                "day_pl": cc.NumberColumn("day_pl", step=1.0),
                "sessions": cc.Column("sessions", help="Comma-separated (Asia,London,NY)"),
                "day_notes": cc.Column("day_notes"),
                "lesson": cc.Column("lesson"),
                "checklist_ok": cc.CheckboxColumn("checklist_ok"),
                "screenshot_path": cc.Column("screenshot_path"),
                "delete": cc.CheckboxColumn("delete"),
            },
            hide_index=True,
        )
        c3, c4 = st.columns(2)
        if c3.button("💾 Save changes (daily)", use_container_width=True):
            edited_notes = edited_notes[edited_notes.get("delete", False) == False].drop(columns=["delete"], errors="ignore")
            if not edited_notes.empty:
                edited_notes["date"] = pd.to_datetime(edited_notes["date"], errors="coerce").dt.date
                if "confidence" in edited_notes: edited_notes["confidence"] = pd.to_numeric(edited_notes["confidence"], errors="coerce").fillna(0).clip(0,100)
                if "day_pl" in edited_notes: edited_notes["day_pl"] = pd.to_numeric(edited_notes["day_pl"], errors="coerce").fillna(0.0)
                if "sessions" in edited_notes: edited_notes["sessions"] = edited_notes["sessions"].astype(str).str.replace(", ", ",")
            save_daily(edited_notes)
            st.success("Daily notes saved.")
        if c4.button("↩️ Reload daily", use_container_width=True):
            st.rerun()

# ---------------- PAGE 2 — PROGRESS ----------------
else:
    st.subheader("Progress Overview")

    trades = load_trades()
    daily  = load_daily()

    if trades.empty and daily.empty:
        st.info("No data yet. Go to the Journal page to add entries.")
    else:
        # On n'utilise que result_usd pour les stats
        trades["_pl_for_stats"] = pd.to_numeric(trades["result_usd"], errors="coerce").fillna(0.0)

        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            start = st.date_input("Start", value=trades["date"].min() if not trades.empty else date.today())
        with c2:
            end = st.date_input("End", value=trades["date"].max() if not trades.empty else date.today())
        with c3:
            pairs = sorted(trades["ticker"].dropna().unique().tolist()) if not trades.empty else []
            sel = st.multiselect("Pairs", pairs)

        flt = trades.copy()
        if not flt.empty:
            if start: flt = flt[flt["date"] >= start]
            if end:   flt = flt[flt["date"] <= end]
            if sel:   flt = flt[flt["ticker"].isin(sel)]

        k1,k2,k3 = st.columns(3)
        if flt.empty:
            for k in (k1,k2,k3): k.markdown("—")
        else:
            wins = (flt["_pl_for_stats"]>0).sum(); total=len(flt)
            k1.metric("Total trades", total)
            k2.metric("Win rate", f"{(wins/total*100):.1f}%")
            k3.metric("Total P/L ($)", f"{flt['_pl_for_stats'].sum():.2f}")

            # Equity Curve (cumul dans le temps) — animé
            st.markdown("### Equity curve - Results ($) over time")
            st.caption("• X-axis = Date • Y-axis = Equity ($), cumulative sum of your Result($)")
            curve = flt.sort_values("date")[["date","_pl_for_stats"]].copy()
            if not curve.empty:
                curve["date"] = pd.to_datetime(curve["date"])
                curve["Equity"] = curve["_pl_for_stats"].cumsum()
                curve = curve.groupby("date", as_index=False)["Equity"].last()
                animate_line_chart(curve, "date", "Equity", total_seconds=2.0)

            # Weekly / Monthly
            st.markdown("### Weekly/Monthly Results ($)")
            tmp = flt.copy()
            tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
            weekly  = tmp.resample('W-MON', on='date')["_pl_for_stats"].sum().rename("Weekly P/L ($)")
            monthly = tmp.resample('MS',     on='date')["_pl_for_stats"].sum().rename("Monthly P/L ($)")
            st.bar_chart(weekly)
            st.bar_chart(monthly)

        st.markdown("### Daily Notes (range)")
        if not daily.empty:
            dflt = daily.copy()
            if start: dflt = dflt[dflt["date"] >= start]
            if end:   dflt = dflt[dflt["date"] <= end]
            st.dataframe(dflt.sort_values("date", ascending=False), use_container_width=True)

        st.markdown("### Trades Table")
        # On cache 'id' ici aussi
        st.dataframe(
            flt.drop(columns=["id"], errors="ignore").sort_values(["date","time"], ascending=False),
            use_container_width=True
        )

st.caption("Result($) is your manual P/L · Equity = cumulative Result($) over time · Weekly/Monthly = period sums · data in data/")
