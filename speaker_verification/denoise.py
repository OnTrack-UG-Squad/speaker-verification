import noisereduce as nr
import numpy as np

from speaker_verification.deep_speaker.audio import (
    NUM_FRAMES,
    SAMPLE_RATE,
    audio_read,
)

def denoise(input_file: str) -> (np.ndarray, int):
    """
    Denoise audio file using noisereduce.
    """
    # Read audio data
    data = audio_read(input_file)

    # Section of data that is noisy.
    # Since we don't know, just select the whole data
    noise_clip = data

    # Perform noise reduction
    noise_reduced_data = nr.reduce_noise(audio_clip=data, noise_clip=noise_clip, verbose=False)

    # Uncomment close below when integrating to audio.py
    
    '''
    logger.debug(f'denoise: {noise_reduced_data}')
    '''

    return noise_reduced_data