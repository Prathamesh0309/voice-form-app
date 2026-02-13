import streamlit as st
from datetime import datetime
from whisper_utils import transcribe_audio
from extractor import extract_form_fields


# import your extraction logic
# from extractor import extract_form_fields

st.set_page_config(
    page_title="Voice Form Autofill",
    layout="centered"
)

st.title("🎙️ Voice-Based Form Autofill")
st.caption("Speak naturally. Review before submitting.")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
FIELDS = [
    "first_name",
    "last_name",
    "email",
    "phone",
    "pan",
    "address"
]

for field in FIELDS:
    st.session_state.setdefault(field, "")

st.session_state.setdefault("confidence", {})
st.session_state.setdefault("needs_review", [])
st.session_state.setdefault("transcript", "")
st.session_state.setdefault("form_populated", False)


# -------------------------------
# GLOBAL RECORDING
# -------------------------------
st.subheader("Record once to fill the form")

audio = st.audio_input("🎙 Record your details")
transcript = "My name is Rajesh Sharma. Email is rsharma@gmail.com. Phone 888 eight eight one five 1 eight 1 . PAN is ABCDP1234Q. Address is K-102, Green Park, sector 11, New Delhi"
st.session_state.transcript = transcript
if audio:
    with st.spinner("Transcribing & extracting…"):
        # hard-coded transcript for now
        transcript = "My name is Prathamesh Deshpande. Email is prathamesh@gmail.com. Phone nine eight four double two one zero six seven eight nine. PAN is ABCDP1234Q. Address is 123 East Main Street Arizona."
        st.session_state.transcript = transcript
    
st.session_state.setdefault("form_populated",True)

if st.session_state.get("transcript") and not st.session_state.get("form_populated"):
    result = extract_form_fields(st.session_state.transcript)
    for k, v in result["data"].items():
        st.session_state[k] = v or ""
    st.session_state.confidence = result["confidence"]
    st.session_state.needs_review = result["needs_review"]
    st.session_state.form_populated = True

st.divider()

# -------------------------------
# TRANSCRIPT (DEBUG / REVIEW)
# -------------------------------
if st.session_state.transcript:
    with st.expander("📝 View Transcript"):
        st.write(st.session_state.transcript)

# -------------------------------
# FORM UI
# -------------------------------
st.subheader("Review & Edit")

def field_label(name):
    return name.replace("_", " ").title()

for field in FIELDS:
    col1, col2 = st.columns([5, 1])

    with col1:
        value = st.text_input(
            field_label(field),
            value=st.session_state[field],
            key=f"input_{field}"
        )

        st.session_state[field] = value

        if field in st.session_state.needs_review:
            st.warning("Needs review")
            print(st.session_state.needs_review)
    with col2:
        st.caption("🎙 Re-record")
        st.audio_input(
            label=f"Re-record {field}",
            key=f"audio_{field}"
        )

st.divider()

# -------------------------------
# CONFIDENCE DISPLAY
# -------------------------------
if st.session_state.confidence:
    st.subheader("Extraction Confidence")

    for field, score in st.session_state.confidence.items():
        st.progress(score)
        st.caption(f"{field_label(field)}: {int(score * 100)}%")

# -------------------------------
# SUBMIT
# -------------------------------
if st.button("✅ Submit"):
    missing = [f for f in FIELDS if not st.session_state[f]]

    if missing:
        st.error(f"Missing fields: {', '.join(missing)}")
    else:
        st.success("Form submitted successfully 🎉")
        st.json({
            "submitted_at": datetime.now().isoformat(),
            "data": {f: st.session_state[f] for f in FIELDS}
        })
