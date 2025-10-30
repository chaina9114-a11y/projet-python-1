# app.py — Streamlit Trading Journal (Notion-style UI)
# -------------------------------------------------
# Aesthetic, journal-like web app to log trades with a Notion-inspired layout.
# Focused on visual polish + rich inputs first. Data will be stored in CSV.
# -------------------------------------------------

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from pathlib import Path
from typing import List

APP_TITLE = "🗒️ Trading Journal — Notion Style"
DATA_DIR = Path("data")
CSV_PATH = DATA_DIR / "trades.csv"

BASE_COLUMNS = [
    "id", "timestamp", "date", "time", "market", "ticker", "side",
    "quantity", "entry", "stop", "target", "exit", "fees",
    "risk_ccy", "risk_pct", "strategy", "setup", "tags", "mood", "confidence",
    "notes", "rr_planned", "rr_realized", "pnl", "r_multiple"
]

DEFAULT_STRATEGIES = [
    "Breakout", "Pullback", "Reversal", "Trend Following", "Range", "News"
]
DEFAULT_TAGS = [
    "London", "NY", "Asia", "High Vol", "Low Vol", "FOMO", "Plan", "Discipline"
]
MOODS = ["😄", "🙂", "😐", "😕", "😫"]

# -----------------------------
# Utilities
# -----------------------------

def ensure_datafile():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        df = pd.DataFrame(columns=BASE_COLUMNS)
        df.to_csv(CSV_PATH, index=False)


def load_trades() -> pd.DataFrame:
    ensure_datafile()
    df = pd.read_csv(CSV_PATH)
    # Coerce types
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        # Strings
        for col in ["market","ticker","side","strategy","setup","tags","mood","notes"]:
            if col in df:
                df[col] = df[col].astype(str)
        # Numerics
        for col in ["quantity","entry","stop","target","exit","fees","risk_ccy","risk_pct",
                    "rr_planned","rr_realized","pnl","r_multiple","confidence"]:
            if col in df:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def save_trades(df: pd.DataFrame):
    df.to_csv(CSV_PATH, index=False)


def append_trade(row: dict):
    df = load_trades()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_trades(df)


def reset_journal():
    df = pd.DataFrame(columns=BASE_COLUMNS)
    save_trades(df)


# -----------------------------
# Calculations
# -----------------------------

def compute_rr_planned(side: str, entry: float, stop: float, target: float) -> float:
    if entry and stop and target and entry > 0:
        if side == "Long":
            risk = entry - stop
            reward = target - entry
        else:  # Short
            risk = stop - entry
            reward = entry - target
        if risk <= 0:
            return 0.0
        return round(reward / risk, 2)
    return 0.0


def compute_pnl(side: str, entry: float, exit_: float, qty: float, fees: float) -> float:
    if not all([qty is not None, entry is not None, exit_ is not None]):
        return 0.0
    direction = 1 if side == "Long" else -1
    return direction * (exit_ - entry) * qty - (fees or 0.0)


def compute_r_multiple(pnl: float, risk_ccy: float, qty: float, entry: float, stop: float) -> float:
    # Prefer explicit risk in currency; else derive from entry/stop * qty
    if risk_ccy and risk_ccy > 0:
        denom = risk_ccy
    else:
        if entry and stop and qty and qty > 0:
            per_unit = abs(entry - stop)
            denom = per_unit * qty
        else:
            return 0.0
    return round(pnl / denom, 2) if denom > 0 else 0.0


# -----------------------------
# Styles (Notion-like)
# -----------------------------
CUSTOM_CSS = """
<style>
/***** Base *****/
:root { --card-bg: #0f1115; --muted: #8b8b8b; --accent: #6ee7b7; --chip:#1f2937; }
.block-container { padding-top: 2rem; }
h1, h2, h3 { letter-spacing: 0.2px; }

/* Card */
.card { border-radius: 16px; padding: 16px 18px; background: var(--card-bg); border: 1px solid #222531; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
.card + .card { margin-top: 12px; }
.card h4 { margin: 0 0 8px 0; font-size: 1.05rem; }
.meta { color: var(--muted); font-size: 0.9rem; }
.badge { display:inline-block; padding: 4px 8px; border-radius: 999px; background:#111827; border:1px solid #303340; margin-right:6px; font-size:0.8rem; }
.tag { display:inline-block; padding: 2px 8px; border-radius: 999px; background: var(--chip); margin-right:6px; font-size:0.78rem; }
.kpi { border-radius: 14px; padding: 16px; border:1px solid #222531; background:#0b0d12; text-align:center; }
.kpi .val { font-size:1.4rem; font-weight:600; }

/* Inputs */
textarea, input { border-radius: 12px !important; }
</style>
"""

# -----------------------------
# Streamlit App
# -----------------------------

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.title(APP_TITLE)

with st.sidebar:
    st.subheader("⚙️ Journal Controls")
    if st.button("🗑️ Reset journal (clear all)", use_container_width=True):
        reset_journal()
        st.success("Journal cleared. Fresh start ✨")
    st.caption("Astuce: les changements d'UI ne suppriment pas les données; ce bouton, si.")

# ---- New Entry Form (Notion-like) ----
st.markdown("### ✍️ New Entry")
with st.container(border=True):
    c1, c2, c3, c4 = st.columns([1.2,1,1,1])
    with c1:
        trade_date = st.date_input("Date", value=date.today())
        trade_time = st.time_input("Time", value=time(datetime.now().hour, datetime.now().minute))
        market = st.selectbox("Market", ["Indices","FX","Crypto","Commodities"], index=0)
        ticker = st.text_input("Ticker / Pair", placeholder="DJ30, XAUUSD, EURUSD…").upper()
        side = st.segmented_control("Side", ["Long","Short"], selection_mode="single")
    with c2:
        quantity = st.number_input("Quantity", min_value=0.0, step=1.0, help="Contracts / units / lots")
        entry = st.number_input("Entry", min_value=0.0, step=0.0001, format="%.4f")
        stop = st.number_input("Stop", min_value=0.0, step=0.0001, format="%.4f")
        target = st.number_input("Target", min_value=0.0, step=0.0001, format="%.4f")
    with c3:
        exit_ = st.number_input("Exit", min_value=0.0, step=0.0001, format="%.4f")
        fees = st.number_input("Fees", min_value=0.0, step=0.01)
        risk_ccy = st.number_input("Risk (currency)", min_value=0.0, step=0.01, help="Optionnel si tu fournis stop/qty")
        risk_pct = st.number_input("Risk %", min_value=0.0, max_value=100.0, step=0.1)
    with c4:
        strategy = st.selectbox("Strategy", DEFAULT_STRATEGIES, index=0)
        setup = st.text_input("Setup name", placeholder="3-bar play, OB retest…")
        tags = st.multiselect("Tags", DEFAULT_TAGS)
        mood = st.selectbox("Mood", MOODS, index=1)
        confidence = st.slider("Confidence", min_value=0, max_value=100, value=70)

    rr_planned = compute_rr_planned(side, entry, stop, target)
    st.caption(f"Planned R:R ≈ **{rr_planned:.2f}**")

    notes = st.text_area("Notes", placeholder="Context, thesis, why now, management plan…", height=100)

    if st.button("➕ Add Entry", type="primary", use_container_width=True):
        if not ticker or quantity <= 0 or entry <= 0:
            st.error("Veuillez remplir au minimum Ticker, Quantity et Entry.")
        else:
            pnl = compute_pnl(side, entry, exit_, quantity, fees)
            r_mult = compute_r_multiple(pnl, risk_ccy, quantity, entry, stop)
            row = {
                "id": f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "timestamp": datetime.combine(trade_date, trade_time).isoformat(),
                "date": trade_date.isoformat(),
                "time": trade_time.strftime("%H:%M"),
                "market": market,
                "ticker": ticker,
                "side": side,
                "quantity": quantity,
                "entry": entry,
                "stop": stop,
                "target": target,
                "exit": exit_,
                "fees": fees,
                "risk_ccy": risk_ccy,
                "risk_pct": risk_pct,
                "strategy": strategy,
                "setup": setup,
                "tags": ",".join(tags) if tags else "",
                "mood": mood,
                "confidence": confidence,
                "notes": notes,
                "rr_planned": rr_planned,
                "rr_realized": 0.0,
                "pnl": pnl,
                "r_multiple": r_mult,
            }
            append_trade(row)
            st.success(f"Entry saved: {ticker} {side} | PnL={pnl:.2f} | R={r_mult:.2f} | RR plan={rr_planned:.2f}")

st.divider()

# ---- KPIs ----
df = load_trades()

col_k1, col_k2, col_k3, col_k4, col_k5, col_k6 = st.columns(6)
if df.empty:
    for c in (col_k1, col_k2, col_k3, col_k4, col_k5, col_k6):
        with c: st.markdown('<div class="kpi"><div class="val">–</div><div class="meta">No data</div></div>', unsafe_allow_html=True)
else:
    wins = (df["pnl"] > 0).sum()
    total = len(df)
    win_rate = (wins/total)*100 if total else 0
    total_pnl = df["pnl"].sum()
    avg_r = df["r_multiple"].mean()
    eq = df["pnl"].cumsum()
    max_dd = (eq - eq.cummax()).min() if not eq.empty else 0

    col_k1.markdown(f'<div class="kpi"><div class="val">{total}</div><div class="meta">Total trades</div></div>', unsafe_allow_html=True)
    col_k2.markdown(f'<div class="kpi"><div class="val">{win_rate:.1f}%</div><div class="meta">Win rate</div></div>', unsafe_allow_html=True)
    col_k3.markdown(f'<div class="kpi"><div class="val">{avg_r:.2f}</div><div class="meta">Avg R</div></div>', unsafe_allow_html=True)
    col_k4.markdown(f'<div class="kpi"><div class="val">{total_pnl:.2f}</div><div class="meta">Total PnL</div></div>', unsafe_allow_html=True)
    col_k5.markdown(f'<div class="kpi"><div class="val">{max_dd:.2f}</div><div class="meta">Max DD</div></div>', unsafe_allow_html=True)
    col_k6.markdown(f'<div class="kpi"><div class="val">{df["confidence"].mean():.0f}%</div><div class="meta">Avg confidence</div></div>', unsafe_allow_html=True)

st.markdown("### 📈 Equity Curve")
if df.empty:
    st.info("No trades yet. Add an entry above.")
else:
    st.line_chart(df["pnl"].cumsum(), height=220)

# ---- Filters ----
st.markdown("### 🔎 Journal View")
fc1, fc2, fc3, fc4 = st.columns([1,1,1,2])
with fc1:
    f_ticker = st.text_input("Filter: Ticker")
with fc2:
    f_side = st.selectbox("Filter: Side", ["All","Long","Short"], index=0)
with fc3:
    f_strategy = st.selectbox("Filter: Strategy", ["All"] + DEFAULT_STRATEGIES, index=0)
with fc4:
    f_tag = st.text_input("Filter: Tag (contains)")

flt = df.copy()
if not flt.empty:
    if f_ticker:
        flt = flt[flt["ticker"].str.contains(f_ticker.upper(), na=False)]
    if f_side != "All":
        flt = flt[flt["side"] == f_side]
    if f_strategy != "All":
        flt = flt[flt["strategy"] == f_strategy]
    if f_tag:
        flt = flt[flt["tags"].fillna("").str.contains(f_tag, case=False, na=False)]

# ---- Card list (Notion-like) ----
if flt.empty:
    st.caption("No entries match your filters.")
else:
    for _, r in flt.sort_values("timestamp", ascending=False).iterrows():
        tags_html = " ".join([f'<span class="tag">{t.strip()}</span>' for t in str(r.get("tags","")) .split(',') if t.strip()])
        st.markdown(
            f'''<div class="card">
                <h4>{r['ticker']} · {r['side']} · <span class="badge">{r['strategy']}</span></h4>
                <div class="meta">{r['date']} {str(r['time'])} · Mood {r['mood']} · Conf {int(r.get('confidence',0))}% · RR plan {r.get('rr_planned',0):.2f} · R {r.get('r_multiple',0):.2f}</div>
                <div style="margin:8px 0;">{tags_html}</div>
                <div class="meta">Entry {r.get('entry','–')} · Stop {r.get('stop','–')} · Target {r.get('target','–')} · Exit {r.get('exit','–')} · Qty {r.get('quantity','–')} · PnL <b>{r.get('pnl',0):.2f}</b></div>
                <div style="margin-top:10px; white-space:pre-wrap;">{(r.get('notes') or '').strip()}</div>
            </div>''',
            unsafe_allow_html=True
        )

st.caption("Data saved locally in data/trades.csv · Use the reset button to wipe and start fresh.")

