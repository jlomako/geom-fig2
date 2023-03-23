# terminal: streamlit run main.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


@st.cache_data(ttl=3600) # clear cache after 1h
def create_figure(number):
    fig, ax = plt.subplots(figsize=(10, 10))

    R = np.random.randint(1, 200)  # 85, 181, 73 big circle radius
    r1 = np.random.randint(1, 10)
    r2 = np.random.randint(0, 50)
    r = (R / r1) + r2  # small circle radius
    d = r * 1.5  # distance from the center of the small circle to the tracing point
    freq1 = np.random.randint(1, 10)  # frequency of first sine wave
    freq2 = np.random.randint(1, 10)  # frequency of second sine wave
    amp1 = np.random.randint(1, 500)  # amplitude of first sine wave
    amp2 = np.random.randint(1, 500)  # amplitude of second sine wave
    k = np.pi / (np.random.randint(1, 20))  # coefficient to adjust the shape of the pattern

    theta = np.linspace(0, 60 * np.pi, 10000)

    print(f"# R: {R}, r: {r}, r1: {r1}, r2: {r2}, freq1: {freq1}, freq2: {freq2}, amp1: {amp1}, amp2: {amp2}, k: {k}")

    # add sine and cosine waves to x and y equations
    x = (R - r) * np.cos(theta) + d * np.cos((R - r) / r * theta) + k * amp1 * np.sin(
        freq1 * theta) + k * amp2 * np.cos(freq2 * theta)
    y = (R - r) * np.sin(theta) - d * np.sin((R - r) / r * theta) + k * amp1 * np.cos(
        freq1 * theta) - k * amp2 * np.sin(freq2 * theta)

    ax.plot(x, y, linewidth=0.5, color="black")

    ax.axis('equal')
    ax.axis('off')
    return fig

selected = True

st.subheader("Generate random geometric figures")


if st.button("Refresh") or selected:
    # random floats to refresh cache
    st.pyplot(create_figure(np.random.random()))


fn = 'image.png'
img = io.BytesIO()
plt.savefig(img, format='png')

st.download_button(
    label="Save",
    data=img,
    file_name=fn,
    mime="image/png"
)

