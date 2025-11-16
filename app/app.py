import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
from inputs import get_user_input

st.set_page_config(page_title="Hotel Booking Cancellation", page_icon="🏨", layout="wide")

# ---------- robust model loading (absolute path) ----------
@st.cache_resource
def load_model():
    root = Path(__file__).resolve().parent.parent
    model_path = root / "models" / "booking_cancellation_model.pkl"   # adjust if needed
    return joblib.load(model_path)

model = load_model()

# ---------- helper: align columns if saved model isn't a full preprocessing pipeline ----------
def align_columns(df: pd.DataFrame, model) -> pd.DataFrame:
    # Try to read expected feature names from estimator or pipeline
    if hasattr(model, "feature_names_in_"):
        needed = list(model.feature_names_in_)
    else:
        est = None
        if hasattr(model, "named_steps"):
            est = model.named_steps.get("model") or model.named_steps.get("clf")
        if est is not None and hasattr(est, "feature_names_in_"):
            needed = list(est.feature_names_in_)
        else:
            # Fallback: use whatever came in (best effort)
            needed = list(df.columns)

    # Add any missing expected columns as zeros; drop extras; enforce order
    for c in needed:
        if c not in df.columns:
            df[c] = 0
    df = df[needed]

    # Cast bools to int if your model was trained on integers
    for c in df.columns:
        if df[c].dtype == "bool":
            df[c] = df[c].astype(int)
    return df

# ---------- UI ----------
st.title("🏨 Hotel Booking Cancellation Prediction")

tab_input, tab_preview = st.tabs(["🧾 Input", "🔍 Preview & Predict"])

with tab_input:
    user_data, friendly_data = get_user_input()
    st.caption("Fill in the booking details, then go to **Preview & Predict**.")

with tab_preview:
    st.subheader("Data Preview (Feature → Value)")

    # Build a two-column preview table from the single-row user_df
    def tidy_preview(df: pd.DataFrame) -> pd.DataFrame:
        row = df.iloc[0].to_dict()
        # Pretty formatting for booleans and floats
        def fmt(v):
            if isinstance(v, bool):
                return "Yes" if v else "No"
            if isinstance(v, float):
                # show ints without .0, otherwise 2 decimals
                return f"{v:.2f}" if (v % 1) else f"{int(v)}"
            return v
        items = [(k, fmt(v)) for k, v in row.items()]
        return pd.DataFrame(items, columns=["Feature", "Value"])

    # Build preview table
    preview_df = pd.DataFrame(list(friendly_data.items()), columns=["Feature", "Value"])
    st.dataframe(preview_df, width= 'stretch', hide_index=True)

    st.divider()

    # Predict button below the preview table
    # if st.button("🔮 Predict"):
    #     try:
    #         aligned = align_columns(user_data.copy(), model)

    #         # Use model's own default threshold (predict) and show probability if available
    #         if hasattr(model, "predict_proba"):
    #             prob = float(model.predict_proba(aligned)[0, 1])
    #         else:
    #             prob = None

    #         pred = int(model.predict(aligned)[0])

    #         st.subheader("Result")
    #         if prob is not None:
    #             st.metric("Cancellation probability", f"{prob:.2%}")
    #         st.write("**Prediction:**", "⚠️ Likely Cancelled" if pred == 1 else "✅ Likely to Show")


    #     except Exception as e:
    #         st.error(f"Prediction failed: {e}")
    #         st.caption("Check that the saved model was trained on the same feature names and datatypes.")

if st.button("🔮 Predict"):
    try:
        aligned = align_columns(user_data.copy(), model)

        # Predict
        prob = float(model.predict_proba(aligned)[0, 1]) if hasattr(model, "predict_proba") else None
        pred = int(model.predict(aligned)[0])

        # Colors/text for outcome
        outcome_text = "✅ Likely to Show" if pred == 0 else "⚠️ Likely Cancelled"
        outcome_color = "#00c851" if pred == 0 else "#ff4b4b"

        # Centered box
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f"""
                <div style="
                    background-color:#1e1e1e;
                    border:2px solid #444;
                    border-radius:14px;
                    padding:28px 24px;
                    text-align:center;
                    box-shadow:0 6px 14px rgba(0,0,0,0.35);
                ">
                    <h2 style="margin:0 0 10px 0; color:#ffffff;">
                        🎯 Prediction Result
                    </h2>
                    <p style="font-size:22px; margin:12px 0; color:#66d9ef;">
                        Cancellation Probability: <strong>{prob:.2%}</strong>
                    </p>
                    <p style="font-size:24px; margin:8px 0; color:{outcome_color}; font-weight:700;">
                        Prediction: {outcome_text}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.caption("Check that the saved model was trained on the same feature names and datatypes.")
