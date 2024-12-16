from __future__ import absolute_import, division, print_function, unicode_literals
import sys
sys.path.append("..")
import glob
import os
import argparse
import json
from re import S
import torch
import librosa
import soundfile as sf
from env import AttrDict
from dataset import mag_pha_stft, mag_pha_istft
from models.model import MPNet

from rich.progress import track

#
from src.simplify_model import pruning, quantization
from src.process_audio import windowing, dewindowing
import copy
#

h = None
device = None

def load_checkpoint(filepath, device):
    assert os.path.isfile(filepath)
    print("Loading '{}'".format(filepath))
    checkpoint_dict = torch.load(filepath, map_location=device)
    print("Complete.")
    return checkpoint_dict

def scan_checkpoint(cp_dir, prefix):
    pattern = os.path.join(cp_dir, prefix + '*')
    cp_list = glob.glob(pattern)
    if len(cp_list) == 0:
        return ''
    return sorted(cp_list)[-1]

def inference(a):
    model = MPNet(h).to(device)

    state_dict = load_checkpoint(a.checkpoint_file, device)
    model.load_state_dict(state_dict['generator'])

    test_indexes = os.listdir(a.input_noisy_wavs_dir)

    os.makedirs(a.output_dir, exist_ok=True)

    model.eval()
    
    if not os.path.exists(a.output_dir):
        os.makedirs(a.output_dir)
    
    ####################
    #dtype = torch.float16
    model = pruning(copy.deepcopy(model), mode='global')
    #model = quantization(copy.deepcopy(model), dtype=dtype)
    #model = model.to(dtype)
    #model = model.half()
    ####################
    
    with torch.no_grad():
        for index in track(test_indexes):
            noisy_wav, _ = librosa.load(os.path.join(a.input_noisy_wavs_dir, index), sr=h.sampling_rate)
            noisy_wav = torch.from_numpy(noisy_wav).to(device)
            norm_factor = torch.sqrt(len(noisy_wav) / torch.sum(noisy_wav ** 2.0)).to(device)
 
            ###################
            if len(noisy_wav) >= 2 * h.segment_size:  # change this number
                overlap = 0.0
                window_type = 'rectangular'
                noisy_wav = (noisy_wav * norm_factor)
                noisy_windows = windowing(noisy_wav, h.segment_size, overlap=overlap, window_type=window_type)
                generated_windows = torch.zeros_like(noisy_windows)
                for idx_window, noisy_window in enumerate(noisy_windows):
                    noisy_window = noisy_window[None, ...]
                    noisy_amp, noisy_pha, noisy_com = mag_pha_stft(noisy_window, h.n_fft, h.hop_size, h.win_size, h.compress_factor)
                    #with torch.autocast(device_type='cpu', dtype=torch.float16):
                    #with torch.cuda.amp.autocast():  # use mixed precision
                    amp_g, pha_g, com_g = model(noisy_amp, noisy_pha)
                    audio_g_window = mag_pha_istft(amp_g, pha_g, h.n_fft, h.hop_size, h.win_size, h.compress_factor)
                    generated_windows[idx_window] = audio_g_window
                audio_g = dewindowing(generated_windows, h.segment_size, overlap=overlap, window_type=window_type)
                audio_g = audio_g[:len(noisy_wav)]  # remove padding
            #################

            else:
                noisy_wav = (noisy_wav * norm_factor).unsqueeze(0)
                noisy_amp, noisy_pha, noisy_com = mag_pha_stft(noisy_wav, h.n_fft, h.hop_size, h.win_size, h.compress_factor)
                #with torch.autocast(device_type='cpu', dtype=torch.float16):
                #with torch.cuda.amp.autocast():  # use mixed precision
                amp_g, pha_g, com_g = model(noisy_amp, noisy_pha)
                audio_g = mag_pha_istft(amp_g, pha_g, h.n_fft, h.hop_size, h.win_size, h.compress_factor)

            audio_g = audio_g / norm_factor

            output_file = os.path.join(a.output_dir, index)

            sf.write(output_file, audio_g.squeeze().cpu().numpy(), h.sampling_rate, 'PCM_16')


def main():
    print('Initializing Inference Process..')

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_noisy_wavs_dir', default='./Noisy_files/')
    parser.add_argument('--output_dir', default='./Predict_files_prune_global_random/')
    parser.add_argument('--checkpoint_file', default='./best_ckpt/g_best_vb')
    a = parser.parse_args()

    config_file = os.path.join(os.path.split(a.checkpoint_file)[0], 'config.json')
    with open(config_file) as f:
        data = f.read()

    global h
    json_config = json.loads(data)
    h = AttrDict(json_config)

    torch.manual_seed(h.seed)
    global device
    if torch.cuda.is_available():
        torch.cuda.manual_seed(h.seed)
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    print(F'device is {device}')
    inference(a)


if __name__ == '__main__':
    main()