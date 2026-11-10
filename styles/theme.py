"""
Bioron Solutions Brand Styling & Theme Engine
Colors inspired directly by the official Bioron logo:
- Foliage Green: #3B7A2F / #2E5F24
- Earth Loam Brown: #7A4419 / #5C3212
- Olive / Spring Accent: #8BBF43 / #A7C957
- Background: #F9FAF7
"""

BIORON_GREEN = "#3B7A2F"
BIORON_BROWN = "#7A4419"
BIORON_OLIVE = "#8BBF43"
BIORON_DARK = "#1E291E"
BIORON_LIGHT_BG = "#F9FAF7"
BIORON_CARD_BG = "#FFFFFF"

CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #F8FAF6;
    }

    /* Primary Headers */
    h1, h2, h3 {
        color: #1E291E !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E6ECE3 !important;
    }

    /* Bioron Brand Card */
    .bioron-header-card {
        background: linear-gradient(135deg, #3B7A2F 0%, #295321 65%, #7A4419 100%);
        color: white !important;
        padding: 24px 28px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(59, 122, 47, 0.25);
    }
    .bioron-header-card h1, .bioron-header-card h2, .bioron-header-card p {
        color: white !important;
        margin: 0;
    }

    /* Metric Cards */
    .bioron-metric-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        border: 1px solid #E7ECE4;
        border-top: 4px solid #3B7A2F;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .bioron-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0,0,0,0.07);
    }
    .bioron-metric-brown {
        border-top: 4px solid #7A4419 !important;
    }
    .bioron-metric-olive {
        border-top: 4px solid #8BBF43 !important;
    }
    .metric-title {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #1E291E;
        line-height: 1.2;
    }
    .metric-subtext {
        font-size: 12px;
        color: #3B7A2F;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Kanban Board Styling */
    .kanban-column {
        background-color: #F1F4EE;
        border-radius: 12px;
        padding: 14px;
        min-height: 580px;
        border: 1px solid #E2E8DE;
    }
    .kanban-col-header {
        font-size: 14px;
        font-weight: 700;
        padding-bottom: 10px;
        margin-bottom: 12px;
        border-bottom: 2px solid #D5DFD1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .kanban-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #E5EADF;
        border-left: 5px solid #3B7A2F;
        transition: all 0.2s ease;
    }
    .kanban-card:hover {
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        border-color: #CBD5E1;
    }
    .kanban-card-title {
        font-size: 14px;
        font-weight: 700;
        color: #1E291E;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .kanban-card-desc {
        font-size: 12px;
        color: #475569;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    .kanban-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .badge-p0 { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
    .badge-p1 { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .badge-p2 { background-color: #DBEAFE; color: #1E40AF; border: 1px solid #BFDBFE; }
    .badge-p3 { background-color: #F3F4F6; color: #374151; border: 1px solid #E5E7EB; }

    .badge-dept {
        background-color: #EBF3E8;
        color: #2E5F24;
        border: 1px solid #D6E6D1;
    }
    .badge-assignee {
        background-color: #F7EFE9;
        color: #7A4419;
        border: 1px solid #ECCEC0;
    }

    /* Auth Box */
    .login-container {
        max-width: 460px;
        margin: 40px auto;
        padding: 32px 36px;
        background-color: #FFFFFF;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(59, 122, 47, 0.12);
        border: 1px solid #E5EBDD;
        text-align: center;
    }
    .login-role-pill {
        display: inline-block;
        background-color: #EBF5E9;
        color: #3B7A2F;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 16px;
    }

    /* Role Badges */
    .role-badge-admin { background-color: #7A4419; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 700; }
    .role-badge-ceo { background-color: #3B7A2F; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 700; }
    .role-badge-cto { background-color: #0284C7; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 700; }
    .role-badge-coo { background-color: #8BBF43; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 700; }

    /* Custom Streamlit Buttons */
    div.stButton > button:first-child {
        background-color: #3B7A2F;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 18px;
        font-weight: 600;
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        background-color: #2D5E24;
        color: white;
        box-shadow: 0 4px 10px rgba(59, 122, 47, 0.3);
    }
</style>
"""

def render_metric_card(title, value, subtext="", card_type="green"):
    border_class = "bioron-metric-card"
    if card_type == "brown":
        border_class += " bioron-metric-brown"
    elif card_type == "olive":
        border_class += " bioron-metric-olive"

    html = f"""
    <div class="{border_class}">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """
    return html
