import streamlit as st
from sound_object import Sound
import advice
import tempfile
import os
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np


def main():
    st.title("Vowel Trainer")

    # File Path Input for File 1
    reference_file_option = st.radio("Choose option for reference sound:", ("Upload File", "Default Vowel"))

    if reference_file_option == "Upload File":
        reference_file_upload = st.file_uploader("Choose an MP3 file with the reference sound", type=["mp3"])
        if reference_file_upload is not None:
            reference_file = save_to_temp_file(reference_file_upload)
    else:
        # Provide a list of default vowel sounds in the same directory as the script
        default_vowel_sounds = [filename for filename in os.listdir() if filename.endswith(".mp3")]
        reference_file = st.selectbox("Choose a default vowel sound:", default_vowel_sounds)

    # File Path Input for File 2
    learner_file_upload = st.file_uploader("Choose an MP3 file with your own recording", type=["mp3"])
    if learner_file_upload is not None:
        learner_file = save_to_temp_file(learner_file_upload)

    # "Run" Button
    if st.button("Run"):
        reference_sound = Sound(reference_file)
        learner_sound = Sound(learner_file)

        # Display plots side by side with headings
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Reference Spectrogram")
            draw_spectrogram_with_formants(reference_sound)
            st.audio(reference_file, format="audio/mp3")
            st.write("Average F1: " + str(reference_sound.average_f1))
            st.write("Average F2: " + str(reference_sound.average_f2))
            st.write("Difference: " + str(reference_sound.difference_f1_f2))

        with col2:
            st.subheader("Your Spectrogram")
            draw_spectrogram_with_formants(learner_sound)
            st.audio(learner_file, format="audio/mp3")
            st.write("Average F1: " + str(learner_sound.average_f1))
            st.write("Average F2: " + str(learner_sound.average_f2))
            st.write("Difference: " + str(learner_sound.difference_f1_f2))

        st.write('\n')
        st.write(advice.adjust_mouth_position(reference_sound, learner_sound))


def save_to_temp_file(uploaded_file):
    # Save the content of the BytesIO object to a temporary file
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    return temp_file_path

def draw_spectrogram_with_formants(sound):
    # Create a new figure
    fig, ax = plt.subplots()

    # Call the draw_spectrogram_with_formants method with the Matplotlib Axes object
    sound.draw_spectrogram_with_formants(ax)

    # Display the Matplotlib figure in Streamlit
    st.pyplot(fig)


def get_audio_data(file_path):
    # Use pydub to load audio and convert to a numpy array
    audio = AudioSegment.from_mp3(file_path)
    audio_array = np.array(audio.get_array_of_samples(), dtype=np.int16)

    # Convert numpy array to bytes
    audio_bytes = audio_array.tobytes()

    return audio_bytes


if __name__ == "__main__":
    main()
