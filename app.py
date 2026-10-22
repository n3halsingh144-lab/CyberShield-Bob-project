"""
CyberShield SOC — Security Operations Center Dashboard
Built with Python + Streamlit (fake/demo data only)
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import random
import time
import datetime
import uuid

# ─────────────────────────────────────────────
#  PAGE CONFIG & DARK THEME INJECTION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CyberShield SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS for dark theme + colour helpers
st.markdown("""
<style>
    /* ── Dark background ── */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
    }
    /* ── Cards ── */
    .soc-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 18px 22px;
        text-align: center;
    }
    .soc-card h2 { font-size: 2.4rem; margin: 4px 0; }
    .soc-card p  { color: #8b949e; margin: 0; font-size: 0.85rem; letter-spacing: .05em; text-transform: uppercase; }
    /* ── Severity badges ── */
    .sev-low      { background:#1a4731; color:#3fb950; padding:2px 8px; border-radius:12px; font-size:.78rem; font-weight:600; }
    .sev-medium   { background:#3a2d00; color:#d29922; padding:2px 8px; border-radius:12px; font-size:.78rem; font-weight:600; }
    .sev-high     { background:#3d1f00; color:#f0883e; padding:2px 8px; border-radius:12px; font-size:.78rem; font-weight:600; }
    .sev-critical { background:#4a0d0d; color:#f85149; padding:2px 8px; border-radius:12px; font-size:.78rem; font-weight:600; }
    /* ── Table rows ── */
    [data-testid="stDataFrame"] { background: #161b22 !important; }
    /* ── Header bar ── */
    .top-bar { display:flex; justify-content:space-between; align-items:center;
               background:#161b22; border:1px solid #30363d; border-radius:8px;
               padding:10px 20px; margin-bottom:16px; }
    .top-bar h1 { font-size:1.5rem; margin:0; color:#58a6ff; }
    .top-bar span { color:#8b949e; font-size:.9rem; }
    /* ── Buttons ── */
    .stButton > button { border-radius:6px; font-size:.82rem; }
    /* ── Priority colours ── */
    .pri-p1 { color:#f85149; font-weight:700; }
    .pri-p2 { color:#f0883e; font-weight:700; }
    .pri-p3 { color:#d29922; font-weight:700; }
    .pri-p4 { color:#3fb950; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONSTANTS / LOOKUP TABLES
# ─────────────────────────────────────────────
ALERT_TYPES = ["Phishing", "Brute Force", "Malware", "SQL Injection", "DDoS"]
SEVERITIES  = ["Low", "Medium", "High", "Critical"]
STATUSES    = ["New", "Acknowledged", "Escalated", "False Positive", "Closed"]
PRIORITIES  = ["P1 – Critical", "P2 – High", "P3 – Medium", "P4 – Low"]
ANALYSTS    = ["Alice Chen", "Bob Patel", "Carlos Ruiz", "Diana Osei", "Evan Müller"]
INC_STATUSES = ["Open", "Investigating", "Contained", "Resolved"]

SEV_COLOUR = {
    "Low":      "#3fb950",
    "Medium":   "#d29922",
    "High":     "#f0883e",
    "Critical": "#f85149",
}

# Fake source IPs pool
IP_POOL = [f"192.168.{random.randint(1,10)}.{random.randint(1,254)}" for _ in range(30)] + \
          [f"10.0.{random.randint(0,5)}.{random.randint(1,254)}" for _ in range(20)] + \
          [f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(20)]

# ─────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
def _init_state():
    """Initialise all session-state keys once."""
    if "alerts" not in st.session_state:
        st.session_state.alerts = _generate_alerts(40)   # seed with 40 historical alerts
    if "incidents" not in st.session_state:
        st.session_state.incidents = _generate_incidents(5)
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()
    if "selected_alert" not in st.session_state:
        st.session_state.selected_alert = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

# ─────────────────────────────────────────────
#  FAKE DATA GENERATORS
# ─────────────────────────────────────────────
def _new_alert(offset_seconds: int = 0) -> dict:
    """Return a single randomly generated alert dict."""
    sev = random.choices(SEVERITIES, weights=[30, 40, 20, 10])[0]
    return {
        "ID":         f"ALT-{uuid.uuid4().hex[:6].upper()}",
        "Timestamp":  (datetime.datetime.now() - datetime.timedelta(seconds=offset_seconds)).strftime("%Y-%m-%d %H:%M:%S"),
        "Source IP":  random.choice(IP_POOL),
        "Type":       random.choice(ALERT_TYPES),
        "Severity":   sev,
        "Status":     "New",
    }

def _generate_alerts(n: int) -> list[dict]:
    """Seed the alert list with n historical alerts spread over the last hour."""
    return [_new_alert(offset_seconds=random.randint(0, 3600)) for _ in range(n)]

def _generate_incidents(n: int) -> list[dict]:
    """Create n fake incident tickets."""
    incidents = []
    for i in range(n):
        inc_id = f"INC-{1000 + i}"
        created = datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 48))
        incidents.append({
            "ID":          inc_id,
            "Title":       f"{random.choice(ALERT_TYPES)} Campaign Detected",
            "Priority":    random.choice(PRIORITIES),
            "Assignee":    random.choice(ANALYSTS),
            "Status":      random.choice(INC_STATUSES),
            "Created":     created.strftime("%Y-%m-%d %H:%M"),
            "Notes":       "Initial triage complete. Awaiting further analysis.",
            "Evidence":    [
                f"Packet capture: pcap_{inc_id}.pcap",
                f"Log extract: logs_{inc_id}.gz",
                f"Memory dump: mem_{inc_id}.bin",
            ],
            "Chain":       [
                {"Time": created.strftime("%H:%M"), "Actor": "System",          "Action": "Incident auto-created"},
                {"Time": (created + datetime.timedelta(minutes=5)).strftime("%H:%M"),
                 "Actor": random.choice(ANALYSTS), "Action": "Assigned and acknowledged"},
            ],
        })
    return incidents

# ─────────────────────────────────────────────
#  LIVE ALERT FEED (add 1-3 alerts every 5 s)
# ─────────────────────────────────────────────
def _maybe_add_alerts():
    """Append new alerts if 5 seconds have elapsed since last update."""
    now = time.time()
    if now - st.session_state.last_update >= 5:
        for _ in range(random.randint(1, 3)):
            st.session_state.alerts.insert(0, _new_alert())   # newest first
        # Keep list manageable (last 200 alerts)
        st.session_state.alerts = st.session_state.alerts[:200]
        st.session_state.last_update = now

# ─────────────────────────────────────────────
#  SEVERITY BADGE HTML
# ─────────────────────────────────────────────
def _badge(sev: str) -> str:
    cls = f"sev-{sev.lower()}"
    return f'<span class="{cls}">{sev}</span>'

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    """Render navigation, filters and search in the sidebar."""
    with st.sidebar:
        st.image("https://img.icons8.com/nolan/64/shield.png", width=48)  # decorative icon
        st.markdown("## 🛡️ CyberShield SOC")
        st.markdown("---")

        # ── Navigation ──
        page = st.radio("Navigation", ["Dashboard", "Incidents"], label_visibility="collapsed")
        st.session_state.page = page
        st.markdown("---")

        # ── Filters (Dashboard only) ──
        if page == "Dashboard":
            st.markdown("### 🔍 Filters")
            sev_filter  = st.multiselect("Severity",  SEVERITIES,  default=SEVERITIES)
            type_filter = st.multiselect("Type",      ALERT_TYPES, default=ALERT_TYPES)
            stat_filter = st.multiselect("Status",    STATUSES,    default=STATUSES)
            search      = st.text_input("Search (IP or Alert ID)", placeholder="e.g. 192.168 or ALT-")
            st.markdown("---")
            st.caption("⏱ Auto-refreshes every 5 seconds")
            return sev_filter, type_filter, stat_filter, search
        return SEVERITIES, ALERT_TYPES, STATUSES, ""

# ─────────────────────────────────────────────
#  DASHBOARD PAGE
# ─────────────────────────────────────────────
def render_dashboard(sev_filter, type_filter, stat_filter, search):
    """Main dashboard: header, cards, table, charts."""

    # ── Top bar with title + live clock ──
    clock = datetime.datetime.now().strftime("%A, %d %b %Y  |  %H:%M:%S")
    st.markdown(f"""
    <div class="top-bar">
        <h1>🛡️ CyberShield SOC</h1>
        <span>🕐 {clock}</span>
    </div>""", unsafe_allow_html=True)

    # ── Summary cards ──
    alerts = st.session_state.alerts
    total     = len(alerts)
    critical  = sum(1 for a in alerts if a["Severity"] == "Critical")
    open_inc  = sum(1 for a in alerts if a["Status"] in ("New", "Acknowledged", "Escalated"))
    resolved  = sum(1 for a in alerts if a["Status"] in ("False Positive", "Closed"))

    c1, c2, c3, c4 = st.columns(4)
    for col, value, label, colour in [
        (c1, total,    "Total Alerts",         "#58a6ff"),
        (c2, critical, "Critical Alerts",      "#f85149"),
        (c3, open_inc, "Open Incidents",       "#f0883e"),
        (c4, resolved, "Resolved / Closed",    "#3fb950"),
    ]:
        col.markdown(f"""
        <div class="soc-card">
            <h2 style="color:{colour}">{value}</h2>
            <p>{label}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filter alerts ──
    df = pd.DataFrame(alerts)
    mask = (
        df["Severity"].isin(sev_filter) &
        df["Type"].isin(type_filter) &
        df["Status"].isin(stat_filter)
    )
    if search:
        mask &= (
            df["Source IP"].str.contains(search, case=False, na=False) |
            df["ID"].str.contains(search, case=False, na=False)
        )
    filtered = df[mask].copy()

    # ─────────────────────────────────────────
    #  CHARTS  (top row)
    # ─────────────────────────────────────────
    ch1, ch2, ch3 = st.columns(3)

    # Chart 1: Alerts over time (last 12 hours, bucketed by hour)
    with ch1:
        st.markdown("##### Alerts Over Time (last 12 h)")
        if not filtered.empty:
            filtered["_ts"] = pd.to_datetime(filtered["Timestamp"])
            filtered["_hour"] = filtered["_ts"].dt.floor("h")
            time_series = filtered.groupby("_hour").size().reset_index(name="Count")
            time_series = time_series.set_index("_hour").sort_index()
            st.line_chart(time_series["Count"], height=180, use_container_width=True)
        else:
            st.info("No data")

    # Chart 2: Alerts by type
    with ch2:
        st.markdown("##### Alerts by Type")
        if not filtered.empty:
            type_counts = filtered["Type"].value_counts()
            st.bar_chart(type_counts, height=180, use_container_width=True)
        else:
            st.info("No data")

    # Chart 3: Severity distribution (bar chart with colour hint via caption)
    with ch3:
        st.markdown("##### Severity Distribution")
        if not filtered.empty:
            sev_counts = filtered["Severity"].value_counts().reindex(SEVERITIES, fill_value=0)
            st.bar_chart(sev_counts, height=180, use_container_width=True)
            # Small colour legend
            legend_html = "  ".join([f'<span class="sev-{s.lower()}">{s}: {sev_counts[s]}</span>' for s in SEVERITIES])
            st.markdown(legend_html, unsafe_allow_html=True)
        else:
            st.info("No data")

    st.markdown("---")

    # ─────────────────────────────────────────
    #  LIVE ALERTS TABLE
    # ─────────────────────────────────────────
    st.markdown(f"##### 🚨 Live Alerts  <span style='color:#8b949e;font-size:.8rem'>({len(filtered)} shown)</span>", unsafe_allow_html=True)

    if filtered.empty:
        st.warning("No alerts match the current filters.")
        return

    # Build display dataframe with severity colour column (emoji hack for tables)
    SEV_EMOJI = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}
    display_df = filtered[["ID", "Timestamp", "Source IP", "Type", "Severity", "Status"]].copy()
    display_df["Severity"] = display_df["Severity"].map(lambda s: f"{SEV_EMOJI.get(s,'')} {s}")

    # Allow row selection via a selectbox below the table for action buttons
    st.dataframe(
        display_df.reset_index(drop=True),
        use_container_width=True,
        height=260,
        hide_index=True,
    )

    # ─────────────────────────────────────────
    #  ALERT ACTIONS
    # ─────────────────────────────────────────
    st.markdown("##### ⚡ Alert Actions")
    alert_ids = filtered["ID"].tolist()
    if alert_ids:
        selected_id = st.selectbox("Select Alert", alert_ids, key="alert_select")

        # Find the alert in the master list
        def _get_alert_idx(aid):
            for i, a in enumerate(st.session_state.alerts):
                if a["ID"] == aid:
                    return i
            return None

        idx = _get_alert_idx(selected_id)
        if idx is not None:
            a = st.session_state.alerts[idx]
            st.markdown(
                f"**Selected:** `{a['ID']}` | {a['Timestamp']} | `{a['Source IP']}` | "
                f"{a['Type']} | {_badge(a['Severity'])} | `{a['Status']}`",
                unsafe_allow_html=True,
            )

            col_a, col_b, col_c, col_d = st.columns(4)
            if col_a.button("✅ Acknowledge",      key="ack"):
                st.session_state.alerts[idx]["Status"] = "Acknowledged"
                st.success(f"{selected_id} → Acknowledged")
            if col_b.button("🔺 Escalate",         key="esc"):
                st.session_state.alerts[idx]["Status"] = "Escalated"
                st.warning(f"{selected_id} → Escalated")
            if col_c.button("❌ Mark False Positive", key="fp"):
                st.session_state.alerts[idx]["Status"] = "False Positive"
                st.info(f"{selected_id} → False Positive")
            if col_d.button("📋 Create Incident",  key="ci"):
                # Auto-create a new incident from the selected alert
                new_inc = {
                    "ID":       f"INC-{1000 + len(st.session_state.incidents)}",
                    "Title":    f"{a['Type']} from {a['Source IP']}",
                    "Priority": "P1 – Critical" if a["Severity"] == "Critical" else
                                "P2 – High"     if a["Severity"] == "High"     else
                                "P3 – Medium"   if a["Severity"] == "Medium"   else "P4 – Low",
                    "Assignee": random.choice(ANALYSTS),
                    "Status":   "Open",
                    "Created":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Notes":    f"Auto-created from alert {selected_id}.",
                    "Evidence": [f"Alert export: {selected_id}.json"],
                    "Chain":    [{"Time": datetime.datetime.now().strftime("%H:%M"),
                                  "Actor": "Analyst", "Action": f"Incident created from {selected_id}"}],
                }
                st.session_state.incidents.append(new_inc)
                st.session_state.alerts[idx]["Status"] = "Escalated"
                st.success(f"Incident {new_inc['ID']} created and alert escalated.")

# ─────────────────────────────────────────────
#  INCIDENTS PAGE
# ─────────────────────────────────────────────
def render_incidents():
    """Incident management page."""
    st.markdown("""
    <div class="top-bar">
        <h1>📋 Incident Management</h1>
        <span>Ticket Workflow</span>
    </div>""", unsafe_allow_html=True)

    incidents = st.session_state.incidents

    if not incidents:
        st.info("No incidents yet. Create one from the Dashboard by selecting an alert and clicking 'Create Incident'.")
        return

    # ── Incident summary table ──
    summary_rows = []
    for inc in incidents:
        summary_rows.append({
            "ID":       inc["ID"],
            "Title":    inc["Title"],
            "Priority": inc["Priority"],
            "Assignee": inc["Assignee"],
            "Status":   inc["Status"],
            "Created":  inc["Created"],
        })
    summary_df = pd.DataFrame(summary_rows)

    # Colour-code priority column with emoji
    PRI_EMOJI = {"P1 – Critical": "🔴", "P2 – High": "🟠", "P3 – Medium": "🟡", "P4 – Low": "🟢"}
    summary_df["Priority"] = summary_df["Priority"].map(lambda p: f"{PRI_EMOJI.get(p,'')} {p}")

    st.dataframe(summary_df, use_container_width=True, hide_index=True, height=200)
    st.markdown("---")

    # ── Incident detail panel ──
    inc_ids = [inc["ID"] for inc in incidents]
    chosen  = st.selectbox("Select Incident to Manage", inc_ids)
    inc_obj = next((i for i in incidents if i["ID"] == chosen), None)

    if not inc_obj:
        return

    st.markdown(f"### {inc_obj['ID']} — {inc_obj['Title']}")

    left, right = st.columns([2, 1])

    with left:
        # ── Metadata ──
        m1, m2 = st.columns(2)
        m1.markdown(f"**Priority:** {inc_obj['Priority']}")
        m2.markdown(f"**Created:** {inc_obj['Created']}")

        # Editable assignee
        new_assignee = st.selectbox("Assignee", ANALYSTS,
                                    index=ANALYSTS.index(inc_obj["Assignee"]) if inc_obj["Assignee"] in ANALYSTS else 0,
                                    key=f"assignee_{chosen}")
        inc_obj["Assignee"] = new_assignee

        # ── Status workflow ──
        st.markdown("**Status Workflow:**")
        wf_cols = st.columns(len(INC_STATUSES))
        for i, status in enumerate(INC_STATUSES):
            is_current = (inc_obj["Status"] == status)
            btn_style  = "primary" if is_current else "secondary"
            if wf_cols[i].button(
                f"{'▶ ' if is_current else ''}{status}",
                key=f"wf_{chosen}_{status}",
                type=btn_style,
            ):
                # Add chain-of-custody entry
                inc_obj["Chain"].append({
                    "Time":  datetime.datetime.now().strftime("%H:%M"),
                    "Actor": inc_obj["Assignee"],
                    "Action": f"Status changed to {status}",
                })
                inc_obj["Status"] = status
                st.rerun()

        # ── Notes ──
        st.markdown("**Notes:**")
        new_notes = st.text_area("", value=inc_obj["Notes"], height=120, key=f"notes_{chosen}",
                                 label_visibility="collapsed")
        if st.button("💾 Save Notes", key=f"save_notes_{chosen}"):
            inc_obj["Notes"] = new_notes
            inc_obj["Chain"].append({
                "Time": datetime.datetime.now().strftime("%H:%M"),
                "Actor": inc_obj["Assignee"],
                "Action": "Notes updated",
            })
            st.success("Notes saved.")

    with right:
        # ── Evidence log ──
        st.markdown("**🗂️ Evidence Log:**")
        for ev in inc_obj["Evidence"]:
            st.markdown(f"- `{ev}`")

        # Add evidence
        new_ev = st.text_input("Add Evidence Item", key=f"ev_{chosen}", placeholder="filename or description")
        if st.button("➕ Add", key=f"add_ev_{chosen}"):
            if new_ev.strip():
                inc_obj["Evidence"].append(new_ev.strip())
                inc_obj["Chain"].append({
                    "Time": datetime.datetime.now().strftime("%H:%M"),
                    "Actor": inc_obj["Assignee"],
                    "Action": f"Evidence added: {new_ev.strip()}",
                })
                st.success("Evidence added.")

        st.markdown("---")

        # ── Chain of custody ──
        st.markdown("**🔗 Chain of Custody:**")
        for entry in inc_obj["Chain"]:
            st.markdown(f"`{entry['Time']}` **{entry['Actor']}** — {entry['Action']}")

    st.markdown("---")

    # ── Download report ──
    report_lines = [
        f"CYBERSHIELD SOC — INCIDENT REPORT",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"{'='*60}",
        f"Incident ID : {inc_obj['ID']}",
        f"Title       : {inc_obj['Title']}",
        f"Priority    : {inc_obj['Priority']}",
        f"Assignee    : {inc_obj['Assignee']}",
        f"Status      : {inc_obj['Status']}",
        f"Created     : {inc_obj['Created']}",
        f"",
        f"NOTES",
        f"{'─'*40}",
        inc_obj["Notes"],
        f"",
        f"EVIDENCE LOG",
        f"{'─'*40}",
        *[f"  - {e}" for e in inc_obj["Evidence"]],
        f"",
        f"CHAIN OF CUSTODY",
        f"{'─'*40}",
        *[f"  [{e['Time']}] {e['Actor']}: {e['Action']}" for e in inc_obj["Chain"]],
        f"",
        f"{'='*60}",
        f"END OF REPORT — CyberShield SOC (Demo Data)",
    ]
    report_text = "\n".join(report_lines)

    st.download_button(
        label="⬇️ Download Incident Report (.txt)",
        data=report_text,
        file_name=f"{inc_obj['ID']}_report.txt",
        mime="text/plain",
        key=f"dl_{chosen}",
    )

# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────
def main():
    _init_state()
    _maybe_add_alerts()   # inject new live alerts if 5 s have passed

    # Render sidebar and capture filters
    sev_filter, type_filter, stat_filter, search = render_sidebar()

    if st.session_state.page == "Dashboard":
        render_dashboard(sev_filter, type_filter, stat_filter, search)
    else:
        render_incidents()

    # Auto-rerun every 5 seconds to simulate live feed
    time.sleep(0.1)
    st.rerun()


if __name__ == "__main__":
    main()
