import streamlit as st
from transformers import pipeline


MODEL_ID = "Trotskitten/fake_news_detector"

LABEL_MAP = {
    "LABEL_0": "FAKE",
    "LABEL_1": "REAL",
    "0": "FAKE",
    "1": "REAL",
    "FAKE": "FAKE",
    "REAL": "REAL",
}

EXAMPLE_HEADLINES = [
    "Government announces new funding package for public schools",
    "Scientists confirm drinking coffee makes people invisible overnight",
    "Local election results certified after official vote count",
    "Celebrity secretly bought the moon, leaked documents reveal",
    "Health officials release updated flu vaccination guidance",
]


st.set_page_config(
    page_title="Fake News Headline Classifier",
    layout="centered",
)


st.markdown(
    """
    <style>
        .main .block-container {
            max-width: 860px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }
        .app-header {
            border-bottom: 1px solid rgba(120, 120, 120, 0.25);
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
        }
        .app-subtitle {
            color: #5f6b7a;
            font-size: 1.05rem;
            line-height: 1.55;
            margin-top: 0.35rem;
        }
        .prediction-real {
            color: #087f5b;
            font-weight: 700;
        }
        .prediction-fake {
            color: #c92a2a;
            font-weight: 700;
        }
        .small-muted {
            color: #6c757d;
            font-size: 0.92rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading model from Hugging Face Hub...")
def load_classifier():
    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        tokenizer=MODEL_ID,
    )


def normalize_label(raw_label: str) -> str:
    label = str(raw_label).strip().upper()
    if label in LABEL_MAP:
        return LABEL_MAP[label]

    if label.startswith("LABEL_"):
        label_id = label.replace("LABEL_", "", 1)
        return LABEL_MAP.get(label_id, label)

    return label


def classify_headline(classifier, headline: str) -> tuple[str, float, str]:
    result = classifier(headline, truncation=True)

    if isinstance(result, list) and result and isinstance(result[0], list):
        result = result[0]

    prediction = result[0] if isinstance(result, list) else result
    raw_label = prediction.get("label", "")
    score = float(prediction.get("score", 0.0))

    return normalize_label(raw_label), score, raw_label


def set_headline(headline: str) -> None:
    st.session_state.headline = headline


def clear_headline() -> None:
    st.session_state.headline = ""


if "headline" not in st.session_state:
    st.session_state.headline = ""


with st.sidebar:
    st.header("Model")
    st.write(f"`{MODEL_ID}`")
    st.caption("Binary labels: 0 = FAKE, 1 = REAL")

    st.divider()
    st.header("Disclaimer")
    st.info(
        "This model predicts from learned headline patterns. "
        "It does not verify factual truth, sources, evidence, or current events."
    )


st.markdown(
    """
    <div class="app-header">
        <h1>Fake News Headline Classifier</h1>
        <p class="app-subtitle">
            Classify a news-style headline as <strong>FAKE</strong> or
            <strong>REAL</strong> using a fine-tuned Hugging Face Transformer model.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Headline")
headline = st.text_area(
    label="Enter a headline",
    key="headline",
    height=120,
    placeholder="Paste or type a news headline here...",
    label_visibility="collapsed",
)

col_a, col_b = st.columns([1, 1])
with col_a:
    classify_clicked = st.button("Classify headline", type="primary", use_container_width=True)
with col_b:
    st.button("Clear", on_click=clear_headline, use_container_width=True)

st.markdown("#### Example Headlines")
example_cols = st.columns(1)
for index, example in enumerate(EXAMPLE_HEADLINES):
    example_cols[0].button(
        example,
        key=f"example_{index}",
        on_click=set_headline,
        args=(example,),
        use_container_width=True,
    )

st.divider()

if classify_clicked:
    cleaned_headline = headline.strip()

    if not cleaned_headline:
        st.warning("Please enter a headline before running the classifier.")
    else:
        try:
            classifier = load_classifier()
            label, confidence, raw_label = classify_headline(classifier, cleaned_headline)

            label_class = "prediction-real" if label == "REAL" else "prediction-fake"
            st.markdown(
                f"""
                <h3>Prediction:
                    <span class="{label_class}">{label}</span>
                </h3>
                """,
                unsafe_allow_html=True,
            )

            st.metric("Confidence", f"{confidence:.2%}")
            st.progress(min(max(confidence, 0.0), 1.0))

            if raw_label != label:
                st.caption(f"Model output label: `{raw_label}` mapped to `{label}`")

            st.markdown(
                """
                <p class="small-muted">
                    Treat this output as a model prediction, not as a fact-check.
                </p>
                """,
                unsafe_allow_html=True,
            )
        except Exception as exc:
            st.error("The model could not be loaded or the headline could not be classified.")
            st.exception(exc)
else:
    st.caption("Enter a headline or select an example, then run the classifier.")
