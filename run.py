import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io
import time

# ============================================
# SUPABASE CONFIGURATION
# ============================================
SUPABASE_URL = "https://qurakjquxsyunqmautak.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF1cmFranF1eHN5dW5xbWF1dGFrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzNDYzOTEsImV4cCI6MjA4MDkyMjM5MX0.aRn6yuQiqvVT5JllPqP640JPVrQ15rWUYe1woa2rAyg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="T-Shirt Inventory",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== BLACK + RED THEME CSS ==========
st.markdown("""
<style>
    .main, .stApp, section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    body, p, li, td, th, a {
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #dc143c !important;
        font-weight: 600 !important;
    }
    input[type="text"], input[type="password"], input[type="number"], textarea {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
        border-radius: 5px !important;
    }
    input::placeholder, textarea::placeholder {
        color: #999999 !important;
        opacity: 0.7 !important;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label,
    .stTextArea label, .stCheckbox label {
        color: #dc143c !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #dc143c !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    .stButton > button {
        background-color: #dc143c !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        height: 45px !important;
    }
    .stButton > button:hover {
        background-color: #b30000 !important;
        color: #ffffff !important;
        border: 2px solid #b30000 !important;
    }
    .stDownloadButton > button {
        background-color: #dc143c !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
    }
    .stDownloadButton > button:hover {
        background-color: #b30000 !important;
        color: #ffffff !important;
    }
    [data-baseweb="select"] {
        background-color: #dc143c !important;
    }
    [data-baseweb="select"] > div {
        background-color: #dc143c !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
    }
    [data-baseweb="select"] input {
        color: #ffffff !important;
        background-color: #dc143c !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: #ffffff !important;
    }
    [data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    [data-baseweb="popover"],
    [role="listbox"] {
        background-color: #dc143c !important;
    }
    [role="option"] {
        background-color: #dc143c !important;
        color: #ffffff !important;
    }
    [role="option"]:hover {
        background-color: #b30000 !important;
        color: #ffffff !important;
    }
    .stForm {
        background-color: #000000 !important;
        border: 2px solid #dc143c !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    .streamlit-expanderHeader {
        background-color: #000000 !important;
        color: #dc143c !important;
        font-weight: 600 !important;
        border: 1px solid #dc143c !important;
    }
    details[open] > .streamlit-expanderContent {
        background-color: #000000 !important;
        border: 1px solid #dc143c !important;
        border-top: none !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: 600 !important;
        background-color: #000000 !important;
        border-bottom: 3px solid transparent !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #dc143c !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #dc143c !important;
    }
    .dataframe, .stDataFrame {
        background-color: #000000 !important;
    }
    .dataframe thead tr th {
        background-color: #000000 !important;
        color: #dc143c !important;
        font-weight: 700 !important;
        border: 1px solid #dc143c !important;
    }
    .dataframe tbody tr td {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #dc143c !important;
    }
    .stSuccess {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #28a745 !important;
    }
    .stError {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #dc143c !important;
    }
    .stWarning {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #ffc107 !important;
    }
    .stInfo {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #17a2b8 !important;
    }
    hr {
        border-color: #dc143c !important;
        border-width: 2px !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #dc143c !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #ffffff !important;
    }
    [data-testid="column"] {
        background-color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONSTANTS
# ============================================
KIDS_SIZES = ["26", "28", "30", "32"]
ADULT_SIZES = ["34 (XS)", "36 (S)", "38 (M)", "40 (L)", "42 (XL)", "44 (XXL)", "46 (XXXL)"]
ORGANIZATIONS = ["Warehouse", "Organization 2", "Event Place"]

REASONS_IN = [
    "New Stock Arrival",
    "Transfer from Warehouse",
    "Transfer from Other Org",
    "Return/Exchange",
    "Other",
]

REASONS_OUT = [
    "Regular Distribution",
    "VIP Gift",
    "Event Distribution",
    "Transfer to Warehouse",
    "Transfer to Other Org",
    "Damaged/Lost",
    "Other",
]

# ============================================
# SESSION STATE
# ============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_org" not in st.session_state:
    st.session_state.user_org = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "first_load" not in st.session_state:
    st.session_state.first_load = True
if "event_cart" not in st.session_state:
    st.session_state.event_cart = []  # list of {category, size, quantity}

# ============================================
# DB HELPERS
# ============================================
def authenticate_user(user_id, password):
    try:
        resp = (
            supabase.table("users")
            .select("*")
            .eq("user_id", user_id)
            .eq("password", password)
            .execute()
        )
        data = resp.data or []
        return data[0] if data else None
    except Exception as e:
        st.error(f"Login error: {e}")
        return None

def get_stock_data(org):
    try:
        resp = supabase.table("stock").select("*").eq("organization", org).execute()
        return resp.data or []
    except Exception:
        return []

def get_current_stock(org, category, size):
    try:
        resp = (
            supabase.table("stock")
            .select("*")
            .eq("organization", org)
            .eq("category", category)
            .eq("size", size)
            .execute()
        )
        data = resp.data or []
        return data[0]["quantity"] if data else 0
    except Exception:
        return 0

def get_total_shirts(org):
    stock = get_stock_data(org)
    if not stock:
        return 0
    df = pd.DataFrame(stock)
    return int(df["quantity"].sum())

def update_stock(org, category, size, qty_change, user_name, action_type, reason):
    try:
        resp = (
            supabase.table("stock")
            .select("*")
            .eq("organization", org)
            .eq("category", category)
            .eq("size", size)
            .execute()
        )
        data = resp.data or []
        if data:
            current = data[0]["quantity"]
            new_qty = current + qty_change
            if new_qty < 0:
                return False, f"❌ Cannot remove {abs(qty_change)} shirts! Only {current} available in Size {size}"
            supabase.table("stock").update({"quantity": new_qty}).eq(
                "id", data[0]["id"]
            ).execute()
        else:
            if qty_change < 0:
                return False, f"❌ Cannot remove shirts! Size {size} has 0 stock"
            supabase.table("stock").insert(
                {
                    "organization": org,
                    "category": category,
                    "size": size,
                    "quantity": max(0, qty_change),
                }
            ).execute()

        supabase.table("transactions").insert(
            {
                "organization": org,
                "volunteer_name": user_name,
                "category": category,
                "size": size,
                "quantity": abs(qty_change),
                "action_type": action_type,
                "reason": reason,
                "timestamp": datetime.now().isoformat(),
            }
        ).execute()
        return True, "✅ Success"
    except Exception as e:
        return False, f"❌ Error: {e}"

def record_distribution_single(
    org, volunteer_name, category, size, qty, cust_name, cust_phone, cust_email
):
    try:
        current = get_current_stock(org, category, size)
        if current < qty:
            return (
                False,
                f"❌ Cannot distribute {qty} shirts of {category} {size}! Only {current} available",
            )
        ok, msg = update_stock(
            org, category, size, -qty, volunteer_name, "OUT", "Event Distribution"
        )
        if not ok:
            return False, msg
        supabase.table("customers").insert(
            {
                "organization": org,
                "volunteer_name": volunteer_name,
                "category": category,
                "size": size,
                "quantity": qty,
                "customer_name": cust_name,
                "customer_phone": cust_phone or "",
                "customer_email": cust_email or "",
                "timestamp": datetime.now().isoformat(),
            }
        ).execute()
        return True, "✅ Success"
    except Exception as e:
        return False, f"❌ Error: {e}"

# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    st.title("👕 T-Shirt Inventory System")
    st.subheader("Login")
    _, c, _ = st.columns([1, 2, 1])
    with c:
        st.markdown("---")
        uid = st.text_input("User ID", key="login_user_id", placeholder="Enter your user ID")
        pwd = st.text_input(
            "Password", type="password", key="login_password", placeholder="Enter your password"
        )
        st.write("")
        if st.button("Login", use_container_width=True):
            if uid and pwd:
                with st.spinner("Authenticating..."):
                    user = authenticate_user(uid, pwd)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user["user_id"]
                    st.session_state.user_org = user["organization"]
                    st.session_state.user_name = user["name"]
                    st.session_state.is_admin = user.get("is_admin", False)
                    st.session_state.first_load = True
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
            else:
                st.warning("⚠️ Please enter both User ID and Password")

# ============================================
# STOCK UPDATE UI (Warehouse / Org 2)
# ============================================
def stock_update_ui(org):
    st.title(f"📦 {org}")
    st.subheader("Stock Management")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write(f"**Volunteer:** {st.session_state.user_name}")
    with c2:
        st.metric("Total T-Shirts", get_total_shirts(org))
    st.markdown("---")

    st.subheader("👶 Kids T-Shirts")
    for size in KIDS_SIZES:
        with st.expander(f"Size {size}", expanded=False):
            current = get_current_stock(org, "Kids", size)
            st.metric(f"Current Stock - Size {size}", current)
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Stock IN**")
                qty_in = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"kids_in_{size}_{org}"
                )
                r_in = st.selectbox(
                    "Reason", REASONS_IN, key=f"kids_in_reason_{size}_{org}"
                )
                if st.button("Add Stock (IN)", key=f"kids_in_btn_{size}_{org}", use_container_width=True):
                    if qty_in > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org, "Kids", size, qty_in, st.session_state.user_name, "IN", r_in
                            )
                        if ok:
                            st.success(f"✅ Added {qty_in} shirts - {r_in}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")
            with c2:
                st.write("**Stock OUT**")
                qty_out = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"kids_out_{size}_{org}"
                )
                r_out = st.selectbox(
                    "Reason", REASONS_OUT, key=f"kids_out_reason_{size}_{org}"
                )
                if st.button("Remove Stock (OUT)", key=f"kids_out_btn_{size}_{org}", use_container_width=True):
                    if qty_out > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org,
                                "Kids",
                                size,
                                -qty_out,
                                st.session_state.user_name,
                                "OUT",
                                r_out,
                            )
                        if ok:
                            st.success(f"✅ Removed {qty_out} shirts - {r_out}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")

    st.markdown("---")
    st.subheader("👔 Adult T-Shirts")
    for size in ADULT_SIZES:
        with st.expander(size, expanded=False):
            current = get_current_stock(org, "Adults", size)
            st.metric(f"Current Stock - {size}", current)
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Stock IN**")
                qty_in = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"adult_in_{size}_{org}"
                )
                r_in = st.selectbox(
                    "Reason", REASONS_IN, key=f"adult_in_reason_{size}_{org}"
                )
                if st.button("Add Stock (IN)", key=f"adult_in_btn_{size}_{org}", use_container_width=True):
                    if qty_in > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org,
                                "Adults",
                                size,
                                qty_in,
                                st.session_state.user_name,
                                "IN",
                                r_in,
                            )
                        if ok:
                            st.success(f"✅ Added {qty_in} shirts - {r_in}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")
            with c2:
                st.write("**Stock OUT**")
                qty_out = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"adult_out_{size}_{org}"
                )
                r_out = st.selectbox(
                    "Reason", REASONS_OUT, key=f"adult_out_reason_{size}_{org}"
                )
                if st.button("Remove Stock (OUT)", key=f"adult_out_btn_{size}_{org}", use_container_width=True):
                    if qty_out > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org,
                                "Adults",
                                size,
                                -qty_out,
                                st.session_state.user_name,
                                "OUT",
                                r_out,
                            )
                        if ok:
                            st.success(f"✅ Removed {qty_out} shirts - {r_out}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")

# ============================================
# EVENT PLACE PAGE (customers + IN/OUT + cart)
# ============================================
def event_place_page():
    org = "Event Place"
    st.title("🎪 Event Place")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write(f"**Volunteer:** {st.session_state.user_name}")
    with c2:
        st.metric("Total T-Shirts", get_total_shirts(org))

    st.markdown("---")
    st.subheader("🧑‍🤝‍🧑 Customer & Cart")

    # Customer details (only name required)
    cust_name = st.text_input("Customer Name *", placeholder="Enter name")
    c1, c2, c3 = st.columns(3)
    with c1:
        cust_phone = st.text_input("Phone Number (optional)", placeholder="Enter phone")
    with c2:
        cust_email = st.text_input("Email Address (optional)", placeholder="Enter email")
    with c3:
        st.write("")

    st.write("")

    # Cart item adder
    st.markdown("**Add items to customer cart**")
    col_cat, col_size, col_qty = st.columns([1.5, 2, 1])
    with col_cat:
        cart_category = st.selectbox(
            "Category", ["Kids", "Adults"], key="event_cart_category"
        )
    with col_size:
        if cart_category == "Kids":
            cart_size = st.selectbox("Size", KIDS_SIZES, key="event_cart_kids_size")
        else:
            cart_size = st.selectbox("Size", ADULT_SIZES, key="event_cart_adult_size")
    with col_qty:
        cart_qty = st.number_input(
            "Quantity", min_value=1, value=1, step=1, key="event_cart_qty"
        )

    add_col, clear_col = st.columns([1, 1])
    with add_col:
        if st.button("Add to Cart", use_container_width=True):
            st.session_state.event_cart.append(
                {
                    "category": cart_category,
                    "size": cart_size,
                    "quantity": int(cart_qty),
                }
            )
    with clear_col:
        if st.button("Clear Cart", use_container_width=True):
            st.session_state.event_cart = []

    # Show cart
    if st.session_state.event_cart:
        st.write("")
        st.markdown("**Current Cart Items**")
        df_cart = pd.DataFrame(st.session_state.event_cart)
        st.dataframe(df_cart, use_container_width=True, hide_index=True)
    else:
        st.info("No items in cart yet")

    st.write("")
    # Distribute button (bottom of customer area)
    if st.button("Distribute T-Shirts to Customer", use_container_width=True):
        if not cust_name.strip():
            st.error("❌ Customer name is required")
        elif not st.session_state.event_cart:
            st.error("❌ Cart is empty, add at least one item")
        else:
            # First check stock for all items
            all_ok = True
            error_msg = ""
            for item in st.session_state.event_cart:
                available = get_current_stock(org, item["category"], item["size"])
                if available < item["quantity"]:
                    all_ok = False
                    error_msg = (
                        f"❌ Not enough stock for {item['category']} {item['size']}. "
                        f"Requested {item['quantity']} but only {available} available."
                    )
                    break
            if not all_ok:
                st.error(error_msg)
            else:
                # Process all items
                success_all = True
                for item in st.session_state.event_cart:
                    ok, msg = record_distribution_single(
                        org,
                        st.session_state.user_name,
                        item["category"],
                        item["size"],
                        item["quantity"],
                        cust_name.strip(),
                        cust_phone.strip(),
                        cust_email.strip(),
                    )
                    if not ok:
                        st.error(msg)
                        success_all = False
                        break
                if success_all:
                    st.success(
                        f"✅ Distributed {len(st.session_state.event_cart)} line items to {cust_name}"
                    )
                    st.session_state.event_cart = []
                    time.sleep(1)
                    st.rerun()

    st.markdown("---")
    st.subheader("📦 Event Place Stock Management")

    # Same IN/OUT controls as other orgs
    st.subheader("👶 Kids T-Shirts")
    for size in KIDS_SIZES:
        with st.expander(f"Size {size}", expanded=False):
            current = get_current_stock(org, "Kids", size)
            st.metric(f"Current Stock - Size {size}", current)
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Stock IN**")
                qty_in = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"ev_kids_in_{size}"
                )
                r_in = st.selectbox(
                    "Reason", REASONS_IN, key=f"ev_kids_in_reason_{size}"
                )
                if st.button("Add Stock (IN)", key=f"ev_kids_in_btn_{size}", use_container_width=True):
                    if qty_in > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org, "Kids", size, qty_in, st.session_state.user_name, "IN", r_in
                            )
                        if ok:
                            st.success(f"✅ Added {qty_in} shirts - {r_in}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")
            with c2:
                st.write("**Stock OUT**")
                qty_out = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"ev_kids_out_{size}"
                )
                r_out = st.selectbox(
                    "Reason", REASONS_OUT, key=f"ev_kids_out_reason_{size}"
                )
                if st.button("Remove Stock (OUT)", key=f"ev_kids_out_btn_{size}", use_container_width=True):
                    if qty_out > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org,
                                "Kids",
                                size,
                                -qty_out,
                                st.session_state.user_name,
                                "OUT",
                                r_out,
                            )
                        if ok:
                            st.success(f"✅ Removed {qty_out} shirts - {r_out}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")

    st.markdown("---")
    st.subheader("👔 Adult T-Shirts")
    for size in ADULT_SIZES:
        with st.expander(size, expanded=False):
            current = get_current_stock(org, "Adults", size)
            st.metric(f"Current Stock - {size}", current)
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Stock IN**")
                qty_in = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"ev_adult_in_{size}"
                )
                r_in = st.selectbox(
                    "Reason", REASONS_IN, key=f"ev_adult_in_reason_{size}"
                )
                if st.button("Add Stock (IN)", key=f"ev_adult_in_btn_{size}", use_container_width=True):
                    if qty_in > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org,
                                "Adults",
                                size,
                                qty_in,
                                st.session_state.user_name,
                                "IN",
                                r_in,
                            )
                        if ok:
                            st.success(f"✅ Added {qty_in} shirts - {r_in}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")
            with c2:
                st.write("**Stock OUT**")
                qty_out = st.number_input(
                    "Quantity", min_value=0, value=0, step=1, key=f"ev_adult_out_{size}"
                )
                r_out = st.selectbox(
                    "Reason", REASONS_OUT, key=f"ev_adult_out_reason_{size}"
                )
                if st.button("Remove Stock (OUT)", key=f"ev_adult_out_btn_{size}", use_container_width=True):
                    if qty_out > 0:
                        with st.spinner("Updating stock..."):
                            ok, msg = update_stock(
                                org,
                                "Adults",
                                size,
                                -qty_out,
                                st.session_state.user_name,
                                "OUT",
                                r_out,
                            )
                        if ok:
                            st.success(f"✅ Removed {qty_out} shirts - {r_out}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ Please enter quantity greater than 0")

    st.markdown("---")
    st.subheader("📊 Current Stock at Event Place")
    stock = get_stock_data(org)
    if stock:
        df = pd.DataFrame(stock)
        st.dataframe(df[["category", "size", "quantity"]], use_container_width=True, hide_index=True)
    else:
        st.info("No stock data available")

# ============================================
# ADMIN PANEL
# ============================================
def admin_panel():
    st.title("⚙️ Admin Panel")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Stock Overview", "User Management", "Transaction History", "Download Reports"]
    )

    with tab1:
        st.subheader("Stock Overview - All Organizations")
        for org in ORGANIZATIONS:
            with st.expander(f"📦 {org}", expanded=True):
                stock = get_stock_data(org)
                if stock:
                    df = pd.DataFrame(stock)
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric(
                            "Total Kids T-Shirts",
                            int(df[df["category"] == "Kids"]["quantity"].sum()),
                        )
                    with c2:
                        st.metric(
                            "Total Adult T-Shirts",
                            int(df[df["category"] == "Adults"]["quantity"].sum()),
                        )
                    with c3:
                        st.metric("Grand Total", int(df["quantity"].sum()))
                    st.dataframe(
                        df[["category", "size", "quantity"]],
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("No stock data available")

    with tab2:
        st.subheader("Create New User")
        with st.form("create_user"):
            c1, c2 = st.columns(2)
            with c1:
                new_uid = st.text_input("User ID *", placeholder="Enter unique user ID")
                new_pwd = st.text_input(
                    "Password *", type="password", placeholder="Enter password"
                )
                new_name = st.text_input(
                    "Full Name *", placeholder="Enter volunteer name"
                )
            with c2:
                new_org = st.selectbox("Organization *", ORGANIZATIONS)
                is_admin = st.checkbox("Grant Admin Access")
            submitted = st.form_submit_button("Create User", use_container_width=True)
        if submitted:
            if new_uid and new_pwd and new_name:
                try:
                    supabase.table("users").insert(
                        {
                            "user_id": new_uid,
                            "password": new_pwd,
                            "name": new_name,
                            "organization": new_org,
                            "is_admin": is_admin,
                        }
                    ).execute()
                    st.success(f"✅ User '{new_uid}' created successfully!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error creating user: {e}")
            else:
                st.error("❌ Please fill all required fields!")

        st.markdown("---")
        st.subheader("All Users")
        try:
            resp = supabase.table("users").select("*").execute()
            users = resp.data or []
            if users:
                df = pd.DataFrame(users)
                st.dataframe(
                    df[["user_id", "name", "organization", "is_admin"]],
                    use_container_width=True,
                    hide_index=True,
                )
        except Exception as e:
            st.error(f"Error loading users: {e}")

    with tab3:
        st.subheader("Transaction History with Reasons")
        for org in ORGANIZATIONS:
            with st.expander(f"📜 {org} Transactions", expanded=False):
                try:
                    resp = (
                        supabase.table("transactions")
                        .select("*")
                        .eq("organization", org)
                        .order("timestamp", desc=True)
                        .execute()
                    )
                    data = resp.data or []
                    if data:
                        df = pd.DataFrame(data)
                        cols = [
                            "volunteer_name",
                            "category",
                            "size",
                            "quantity",
                            "action_type",
                            "reason",
                            "timestamp",
                        ]
                        cols = [c for c in cols if c in df.columns]
                        st.dataframe(
                            df[cols], use_container_width=True, hide_index=True
                        )
                    else:
                        st.info("No transaction data")
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab4:
        st.subheader("Download Reports")
        for org in ORGANIZATIONS:
            st.write(f"**{org}**")
            c1, c2 = st.columns(2)
            with c1:
                stock = get_stock_data(org)
                if stock:
                    df = pd.DataFrame(stock)
                    try:
                        buf = io.BytesIO()
                        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                            df.to_excel(writer, index=False, sheet_name="Stock")
                        buf.seek(0)
                        st.download_button(
                            label=f"Download {org} Stock",
                            data=buf,
                            file_name=f"{org.replace(' ', '_')}_stock_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Error creating Excel file: {e}")
                else:
                    st.info("No stock data")
            with c2:
                try:
                    resp = (
                        supabase.table("transactions")
                        .select("*")
                        .eq("organization", org)
                        .execute()
                    )
                    data = resp.data or []
                    if data:
                        df = pd.DataFrame(data)
                        try:
                            buf = io.BytesIO()
                            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                                df.to_excel(writer, index=False, sheet_name="Transactions")
                            buf.seek(0)
                            st.download_button(
                                label=f"Download {org} Transactions",
                                data=buf,
                                file_name=f"{org.replace(' ', '_')}_transactions_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True,
                            )
                        except Exception as e:
                            st.error(f"Error creating Excel file: {e}")
                    else:
                        st.info("No transaction data")
                except Exception:
                    st.info("No transaction data")
            st.markdown("---")

        st.write("**Event Place - Customer Data**")
        try:
            resp = supabase.table("customers").select("*").execute()
            data = resp.data or []
            if data:
                df = pd.DataFrame(data)
                try:
                    buf = io.BytesIO()
                    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Customers")
                    buf.seek(0)
                    st.download_button(
                        label="Download Customer Data",
                        data=buf,
                        file_name=f"customers_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Error creating Excel file: {e}")
            else:
                st.info("No customer data")
        except Exception:
            st.info("No customer data")

# ============================================
# MAIN
# ============================================
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        with st.sidebar:
            st.title("👕 T-Shirt Inventory")
            st.write(f"**User:** {st.session_state.user_name}")
            st.write(f"**Organization:** {st.session_state.user_org}")
            if not st.session_state.is_admin:
                st.metric("My Total T-Shirts", get_total_shirts(st.session_state.user_org))
            st.markdown("---")
            if st.button("Logout", use_container_width=True):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if st.session_state.is_admin:
            admin_panel()
        elif st.session_state.user_org == "Event Place":
            event_place_page()
        else:
            stock_update_ui(st.session_state.user_org)

if __name__ == "__main__":
    main()
