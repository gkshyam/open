import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
from pptx import Presentation
import io, os

# -------------------- LOAD API --------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="OpenCV Documentation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- GFG-LIKE FORMAL CSS --------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
.block-container {
    padding-top: 1rem;
}

.doc-title {
    font-size: 32px;
    font-weight: 700;
    color: #22c55e;
}
.doc-subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
}

.doc-box {
    background: #020617;
    padding: 22px;
    border-radius: 8px;
    border: 1px solid #1e293b;
}

.ai-box {
    background: #020617;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #1e293b;
}

.copy-btn {
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="doc-title">OpenCV Documentation</div>', unsafe_allow_html=True)
st.markdown('<div class="doc-subtitle">GeeksForGeeks-style learning with AI Help Desk</div>', unsafe_allow_html=True)

# -------------------- LEFT NAVIGATION --------------------
st.sidebar.title("📘 Topics")
topic = st.sidebar.radio("Navigate", [
    "Introduction",
    "Image Basics",
    "Filtering",
    "Segmentation",
    "Morphology",
    "Edge Detection",
    "Feature Extraction",
    "Object Detection"
])

# -------------------- MAIN + RIGHT PANEL LAYOUT --------------------
main_col, right_col = st.columns([3.5, 1.5])

# ===================== MAIN DOCUMENTATION AREA =====================
with main_col:
    st.markdown('<div class="doc-box">', unsafe_allow_html=True)

    if topic == "Introduction":
        st.markdown("## Introduction to Image Processing")
        st.write("""
Image processing is the technique of enhancing and analyzing images using algorithms.
OpenCV is the most widely used open-source library for computer vision.
""")

    elif topic == "Image Basics":
        st.markdown("## Image Basics")
        st.write("""
✔ Pixels  
✔ Resolution  
✔ Grayscale vs RGB  
✔ Histograms  
""")

    elif topic == "Filtering":
        st.markdown("## Image Filtering")
        st.write("""
✔ Mean Filter  
✔ Gaussian Filter  
✔ Median Filter  
""")

    elif topic == "Segmentation":
        st.markdown("## Segmentation")
        st.write("""
✔ Thresholding  
✔ K-Means  
✔ Watershed  
""")

    elif topic == "Morphology":
        st.markdown("## Morphology")
        st.write("""
✔ Dilation  
✔ Erosion  
✔ Opening  
✔ Closing  
""")

    elif topic == "Edge Detection":
        st.markdown("## Edge Detection")
        st.write("""
✔ Sobel  
✔ Prewitt  
✔ Canny  
""")

    elif topic == "Feature Extraction":
        st.markdown("## Feature Extraction")
        st.write("""
✔ Harris  
✔ SIFT  
✔ SURF  
✔ ORB  
""")

    elif topic == "Object Detection":
        st.markdown("## Object Detection")
        st.write("""
✔ Haar Cascades  
✔ YOLO  
✔ SSD  
""")

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== RIGHT AI HELP DESK =====================
with right_col:
    st.markdown('<div class="ai-box">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI Help Desk")

    # ---- SESSION MEMORY ----
    if "doc_context" not in st.session_state:
        st.session_state.doc_context = ""

    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""

    # ---- FILE UPLOAD ----
    uploaded = st.file_uploader("Upload PDF / PPTX", type=["pdf", "pptx"])

    if uploaded:
        extracted_text = ""

        if uploaded.name.endswith(".pdf"):
            reader = PdfReader(uploaded)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text

        elif uploaded.name.endswith(".pptx"):
            pres = Presentation(io.BytesIO(uploaded.read()))
            for slide in pres.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        extracted_text += shape.text + "\n"

        st.session_state.doc_context = extracted_text
        st.success("Document loaded & remembered")

    # ---- PROMPT ----
    user_prompt = st.text_input("Your Task")

    if st.button("Generate"):
        if not user_prompt:
            st.warning("Enter a task")
        else:
            final_prompt = f"""
You are an OpenCV & Image Processing expert.

Documentation:
{st.session_state.doc_context[:6000]}

Task:
{user_prompt}

Return ONLY valid Python code.
"""
            with st.spinner("Generating..."):
                res = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": final_prompt}],
                    temperature=0.1
                )

                code = res.choices[0].message.content.strip()

                if code.startswith("```"):
                    code = code.replace("```python", "").replace("```", "")

                st.session_state.generated_code = code

    # ---- OUTPUT + COPY ----
    if st.session_state.generated_code:
        st.code(st.session_state.generated_code, language="python")

        st.download_button(
            "📋 Copy Code",
            st.session_state.generated_code,
            file_name="generated_code.py",
            mime="text/plain"
        )

    st.markdown('</div>', unsafe_allow_html=True)
