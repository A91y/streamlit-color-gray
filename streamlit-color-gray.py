import cv2
import os
import numpy as np
import streamlit as st
from pathlib import Path
from streamlit_image_comparison import image_comparison

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

st.set_page_config(page_title="AyDecoloriser", layout="centered")


with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


st.markdown("# Decoloriser")
st.markdown("##### by Ayush")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Now do something with the image! For example, let's display it:
    # st.image(opencv_image, channels="BGR")

    img = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_comparison(
        img1=img,
        img2=grayimg,
        label1="Original",
        label2="Black and White",
        make_responsive=True,
        show_labels=True,
    )

    uploaded_file_name = uploaded_file.name
    grayimg_name = uploaded_file_name.replace(".", " ").split()
    extension = grayimg_name[-1]
    grayimg_name.insert(-1, "_grayed.")
    grayimg_name = "".join(grayimg_name)
    # file_ = "img/" + grayimg_name
    file_ = grayimg_name
    cv2.imwrite(file_, cv2.cvtColor(grayimg, cv2.COLOR_RGB2BGR))

    with open(file_, "rb") as file:
        btn = st.download_button(
            label="Download Grayed image",
            data=file,
            file_name=grayimg_name,
            mime=f"image/{extension}"
        )
    os.remove(file_)
