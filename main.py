# terminal: streamlit run main.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Spirograph", layout="centered")

@st.cache_data(ttl=3600) # clear cache after 1h
def create_figure(R, r, d, freq1, freq2, amp1, amp2, k, seed):
    fig, ax = plt.subplots(figsize=(10, 10))

    R = R # big circle radius
    r = r # # small circle radius
    d = d # distance from the center of the small circle to the tracing point
    freq1 = freq1  # frequency of first sine wave
    freq2 = freq2  # frequency of second sine wave
    amp1 = amp1  # amplitude of first sine wave
    amp2 = amp2  # amplitude of second sine wave
    k = np.pi / k  # coefficient to adjust the shape of the pattern
    theta = np.linspace(0, 60 * np.pi, 10000)

    # x and y equations with sine and cosine waves
    x = (R - r) * np.cos(theta) + d * np.cos((R - r) / r * theta) + k * amp1 * np.sin(
        freq1 * theta) + k * amp2 * np.cos(freq2 * theta)
    y = (R - r) * np.sin(theta) - d * np.sin((R - r) / r * theta) + k * amp1 * np.cos(
        freq1 * theta) - k * amp2 * np.sin(freq2 * theta)

    ax.plot(x, y, linewidth=0.5, color="black")

    ax.axis('equal')
    ax.axis('off')
    return fig


@st.cache_data(ttl=3600)
def random_figure(seed):
    return [np.random.randint(1, 200), # R
            np.random.randint(1, 200), # r
            np.random.randint(1, 200), # d
            np.random.randint(1, 10),  # freq1
            np.random.randint(1, 10),  # freq2
            np.random.randint(1, 500), # amp1
            np.random.randint(1, 500), # amp2
            np.random.randint(1, 20)]  # k


st.subheader("Spirograph: Create geometric figures")

col1, col2 = st.columns([2, 6])
with col1:
    # counter for random_figure
    if 'count' not in st.session_state:
        st.session_state.count = 0

    # use default figure on first run otherwise use fig(seed) from random_button
    if st.session_state.count == 0:
        spiro = [1, 71, 192, 4, 4, 100, 74, 4]
    else:
        spiro = random_figure(st.session_state.count)

    # set seed to create different figures
    # seed needs to be random and can not be counter!
    # counter would create the same figures all over again
    random_button = st.button("New", use_container_width=True)
    if random_button:
        st.session_state.count = np.random.random()
        spiro = random_figure(st.session_state.count)

    # SLIDER MENU
    if st.checkbox('Expand Menu'):
        slider_label = "visible"
    else:
        slider_label = "collapsed"

    R = st.slider('Big circle radius: ', 0, 200, value=spiro[0], label_visibility=slider_label)
    r = st.slider('Small circle radius: ', 1, 200, value=spiro[1], label_visibility=slider_label)
    d = st.slider('Distance: ', 0, 200, value=spiro[2], label_visibility=slider_label)
    freq1 = st.slider('Frequency 1st wave: ', 0, 10, value=spiro[3], label_visibility=slider_label)
    freq2 = st.slider('Frequency 2nd wave: ', 0, 10, value=spiro[4], label_visibility=slider_label)
    amp1 = st.slider('Amplitude 1st wave: ', 0, 500, value=spiro[5], label_visibility=slider_label)
    amp2 = st.slider('Amplitude 2nd wave: ', 0, 500, value=spiro[6], label_visibility=slider_label)
    k = st.slider('Coefficient: ', 1, 25, value=spiro[7], label_visibility=slider_label)

with col2:
    st.pyplot(create_figure(R, r, d, freq1, freq2, amp1, amp2, k, np.random.random()))

    img = io.BytesIO()
    plt.savefig(img, format='png')

    st.download_button(
        label="Download image",
        data=img,
        file_name='image.png',
        mime="image/png",
        use_container_width=True
    )


