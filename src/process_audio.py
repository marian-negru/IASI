import torch

def pad_audio(audio, window_size, step_size):
    padding = (len(audio) - window_size) % step_size
    padding = step_size - padding
    audio = torch.cat((audio, torch.zeros(padding)))

    return audio

def windowing(audio, window_size=32000, overlap=0.0, window_type='rectangular'):
    step_size = int(window_size * (1 - overlap))
    
    if window_type == 'hann':
        window_function = torch.hann_window(window_size)
    elif window_type == 'hamming':
        window_function = torch.hamming_window(window_size)
    elif window_type == 'rectangular':
        window_function = torch.ones((window_size, ))
    else:
        raise ValueError(f"Unsupported window type for {window_type}")
    
    # pad audio
    audio = pad_audio(audio, window_size, step_size)

    windows = []
    for start in range(0, len(audio) - window_size + 1, step_size):
        segment = audio[start:start + window_size]
        windowed_segment = segment * window_function
        windows.append(windowed_segment)

    return torch.stack(windows)

def dewindowing(windows, window_size=32000, overlap=0.0, window_type='rectangular'):
    step_size = int(window_size * (1 - overlap))

    if window_type == 'hann':
        window_function = torch.hann_window(window_size)
    elif window_type == 'hamming':
        window_function = torch.hamming_window(window_size)
    elif window_type == 'rectangular':
        window_function = torch.ones((window_size, ))
    else:
        raise ValueError(f"Unsupported window type for {window_type}")

    audio_length = step_size * (windows.size(0) - 1) + window_size
    audio = torch.zeros(audio_length)
    overlap_counter = torch.zeros(audio_length)

    # Use OLA
    for i, window in enumerate(windows):
        start = i * step_size
        audio[start:start + window_size] += window * window_function
        overlap_counter[start:start + window_size] += window_function

    # Normalize overlapping regions
    nonzero_mask = overlap_counter > 0
    audio[nonzero_mask] /= overlap_counter[nonzero_mask]

    return audio
    
    

