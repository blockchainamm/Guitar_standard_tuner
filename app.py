# Import required libraries
import numpy as np
import pyaudio
import time


SAMPLE_RATE = 44100


def generate_sample(freq, duration, volume):

    amplitude = 6000
    total_samples = np.round(SAMPLE_RATE * duration)
    w = 2.0 * np.pi * freq / SAMPLE_RATE
    k = np.arange(0, total_samples)

    return np.round(amplitude * np.sin(k * w))


# Frequency arrary for notes in standard guitar tuning from high to low pitch string
# The notes is as follows E (1-high E), B(2), G(3), D(4), A(5), E(6-low E)
freq_array = np.array([329.63, 246.94, 196.00, 146.83, 110.00, 82.41])

# reversing using list slicing
# The notes is as follows E(6-low E), A(5), D(4), G(3), B(2), E (1-high E)
rev_freq = freq_array[::-1] 

tones, tones1 = [], []
 
for freq in rev_freq:

    tone = np.array(generate_sample(freq, 2.0, 1.0), dtype=np.int16)    
    
    # Appending the tones to a list
    tones.append(tone)

    tone1 = np.array(generate_sample(freq, 1.0, 1.0), dtype=np.int16)    
    
    # Appending the tones to a list
    tones1.append(tone1)


def fmain():
    # Instantiate PyAudio and initialize PortAudio system resources (1)
    p = pyaudio.PyAudio()

    # Open stream (2)
    stream = p.open(format=p.get_format_from_width(width=2), channels=2, rate=SAMPLE_RATE, output=True)

    # Play samples from the tones list with a interval of 1 second between successive notes (3)
    for tone in tones:
        stream.write(tone)
        time.sleep(1) # wait for 1 second between tones

    # Play samples from the tones1 list with a shorter delay between notes
    for tone1 in tones1:
        stream.write(tone1)
        time.sleep(0.1) # wait for 0.1 second between tones
        
    stream.stop_stream()
    # Close stream (4)
    stream.close()
    
    # Release PortAudio system resources (5)
    p.terminate()


fmain()