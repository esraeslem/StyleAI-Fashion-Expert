import streamlit as st
from ultralytics import YOLO
import pandas as pd
from PIL import Image
import torch
import clip
import os

# --- SETUP ---
@st.cache_resource
def load_models():
    # 1. CHECK FOR CUSTOM MODEL
    if os.path.exists("scarf_model.pt"):
        # Use your new Scarf Brain!
        yolo_model = YOLO("scarf_model.pt")
        model_type = "🧣 Custom Scarf Model"
    else:
        # Fallback if file is missing
        yolo_model = YOLO("yolov8n.pt")
        model_type = "⚠️ Standard Model (Custom file missing)"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip_model, preprocess = clip.load("ViT-B/32", device=device)

    return yolo_model, clip_model, preprocess, model_type

try:
    yolo, clip_model, preprocess, model_status = load_models()
except Exception as e:
    st.error(f"Error: {e}")

# --- APP INTERFACE ---
st.set_page_config(page_title="StyleAI: Fashion Expert", page_icon="✨")
st.title("✨ StyleAI: The Intelligent Stylist")
st.caption(f"Currently running: **{model_status}**") # Tells you which brain is active

uploaded_file = st.file_uploader("Upload your outfit...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Your Look', use_column_width=True)

    if st.button("Analyze Style"):
        with st.spinner('Analyzing textures and patterns...'):
            results = yolo(image)

            detected = []
            for r in results:
                for box in r.boxes:
                    name = yolo.names[int(box.cls[0])]
                    detected.append(name)

            detected = list(set(detected))

        if detected:
            st.success(f"We detected: {', '.join([d.upper() for d in detected])}")

            for item in detected:
                st.markdown("---")
                # SCARF LOGIC (Now native to your model!)
                if item == 'scarf':
                    st.info("🧣 **Scarf Detected:** Great accessory! Use the **Third Piece Rule** to layer this over a coat.")
                elif item == 'tie':
                    st.info("👔 **Tie Detected:** Keep it professional. Ensure the tip hits your belt buckle.")
                else:
                    st.write(f"💡 **Styling Tip:** For the **{item.upper()}**, try applying the Sandwich Rule (match shoes to top).")
        else:
            st.warning("No fashion items found.")
