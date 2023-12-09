from pydub.utils import mediainfo
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import zscore
import numpy as np

class Sound:
    def __init__(self, file_path):
        # Constructor method, initializes the object
        self.file_path = file_path
        self.duration = self.get_mp3_duration(file_path)
        self.praat_object = parselmouth.Sound(file_path)
        self.pitch_contour = self.praat_object.to_pitch()
        self.formants_object = self.praat_object.to_formant_burg(max_number_of_formants=5.0)
        self.spectrogram = self.praat_object.to_spectrogram()
        self.f1_series = self.get_formant_values(formant_number=1, start_time=0, end_time=self.duration, interval=0.01)
        self.f2_series = self.get_formant_values(formant_number=2, start_time=0, end_time=self.duration, interval=0.01)
        self.f1_series_no_outliers = self.remove_outliers(self.f1_series)
        self.f2_series_no_outliers = self.remove_outliers(self.f2_series)
        self.average_f1 = self.calculate_average_formant(self.f1_series_no_outliers)
        self.average_f2 = self.calculate_average_formant(self.f2_series_no_outliers)
        self.difference_f1_f2 = self.average_f2 - self.average_f1

    def get_mp3_duration(self, file_path):
        # Alternative method using mediainfo
        info = mediainfo(file_path)
        duration_seconds = float(info['duration'])

        return duration_seconds

    def get_formant_values(self, formant_number, start_time, end_time, interval):
        result = []
        current_time = start_time

        while current_time <= end_time:
            value = self.formants_object.get_value_at_time(formant_number, current_time)

            # Check if the value is not NaN before appending to the result
            if not math.isnan(value):
                result.append((round(current_time, 2), round(value, 2)))

            current_time += interval

        return result

    def remove_outliers(self, formant_values, threshold=0.7):
        # Extract the values from the tuples in formant_values
        values = [value for _, value in formant_values]

        # Calculate the Z-scores for the values
        z_scores = zscore(values)

        # Keep only the values with Z-scores within the specified threshold
        filtered_values = [formant_values[i] for i in range(len(formant_values)) if abs(z_scores[i]) <= threshold]

        return filtered_values

    def calculate_average_formant(self, formant_list):  # [(t, formant), ...]
        if not formant_list:
            return None  # Handle the case where the list is empty

            # Extract the y values from the tuples
        y_values = [y for _, y in formant_list]

        # Calculate the average of the y values
        average_y = sum(y_values) / len(y_values)

        return average_y

    def draw_spectrogram_with_formants(self, ax, dynamic_range=70):
        X, Y = self.spectrogram.x_grid(), self.spectrogram.y_grid()
        sg_db = 10 * np.log10(self.spectrogram.values)

        # Plot the spectrogram on the given Axes
        im = ax.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='cividis')

        # Plot Formant 1
        formant_times_1, formant_freqs_1 = zip(*self.f1_series_no_outliers)
        ax.scatter(formant_times_1, formant_freqs_1, label='Formant 1', color='red', marker='o')

        # Plot Formant 2
        formant_times_2, formant_freqs_2 = zip(*self.f2_series_no_outliers)
        ax.scatter(formant_times_2, formant_freqs_2, label='Formant 2', color='blue', marker='o')

        ax.set_ylim([self.spectrogram.ymin, self.spectrogram.ymax])
        ax.set_xlabel("time [s]")
        ax.set_ylabel("frequency [Hz]")
        ax.legend()


