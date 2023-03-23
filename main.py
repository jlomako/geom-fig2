# terminal: streamlit run main.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


@st.cache_data(ttl=3600) # clear cache after 1h
def create_figure(R, r, d, freq1, freq2, amp1, amp2, k, number):
    fig, ax = plt.subplots(figsize=(10, 10))

    R = R # big circle radius
    r = r # # small circle radius
    d = d # r * 1.5  # distance from the center of the small circle to the tracing point
    freq1 = freq1  # frequency of first sine wave
    freq2 = freq2  # frequency of second sine wave
    amp1 = amp1  # amplitude of first sine wave
    amp2 = amp2  # amplitude of second sine wave
    k = np.pi / k  # coefficient to adjust the shape of the pattern

    theta = np.linspace(0, 60 * np.pi, 10000)

    # print(f"# R: {R}, r: {r}, freq1: {freq1}, freq2: {freq2}, amp1: {amp1}, amp2: {amp2}, k: {k}")

    # add sine and cosine waves to x and y equations
    x = (R - r) * np.cos(theta) + d * np.cos((R - r) / r * theta) + k * amp1 * np.sin(
        freq1 * theta) + k * amp2 * np.cos(freq2 * theta)
    y = (R - r) * np.sin(theta) - d * np.sin((R - r) / r * theta) + k * amp1 * np.cos(
        freq1 * theta) - k * amp2 * np.sin(freq2 * theta)

    ax.plot(x, y, linewidth=0.5, color="black")

    ax.axis('equal')
    ax.axis('off')
    return fig

st.subheader("Spirograph: Generate geometric figures")


col1, col2 = st.columns([1, 4])

spiro = [1,71,192,4,4,100,74,4]

with col1:
    R = st.slider('R: ', 1, 200, value=spiro[0])
    r = st.slider('r: ', 1, 200, value=spiro[1])
    d = st.slider('d: ', 1, 200, value=spiro[2])
    freq1 = st.slider('freq1: ', 1, 10, value=spiro[3])
    freq2 = st.slider('freq2: ', 1, 10, value=spiro[4])
    amp1 = st.slider('amp1: ', 1, 500, value=spiro[5])
    amp2 = st.slider('amp2: ', 1, 500, value=spiro[6])
    k = st.slider('k: ', 1, 20, value=spiro[7])

with col2:
    st.pyplot(create_figure(R, r, d, freq1, freq2, amp1, amp2, k, np.random.random()))

    fn = 'image.png'
    img = io.BytesIO()
    plt.savefig(img, format='png')

    st.download_button(
        label="Save",
        data=img,
        file_name=fn,
        mime="image/png"
    )

