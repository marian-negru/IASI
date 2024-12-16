import os
import torch
import librosa

#import torchmetrics  # in case you want better audio metrics
#torchmetrics.functional.audio.signal_noise_ratio(predict, target)
#torchmetrics.functional.audio.scale_invariant_signal_distortion_ratio(predict, target)

metric_function = torch.nn.L1Loss(reduction='mean')  # you can try different functions

def compute_metric(predict, target):    
    metric = metric_function(predict, target)
    
    return metric

def check_differences():
    path_original = '../MP-SENet/Predict_files_original/'  # modify this
    path_pruned = '../MP-SENet/Predict_files_prune_global_random/'   # modify this
    sr = 16000  # this should be 16 kHz
    metric_total = 0
    for file in sorted(os.listdir(path_original)):
        wav_original, _ = librosa.load(os.path.join(path_original, file), sr=sr)
        wav_pruned, _ = librosa.load(os.path.join(path_pruned, file), sr=sr)
        # call compute_metric
        metric = compute_metric(torch.from_numpy(wav_pruned), torch.from_numpy(wav_original))
        #print(f'metric is {metric:e}')
        metric_total += metric
    metric_total /= len(os.listdir(path_original))
    print(f'metric total is {metric_total:e}')


if __name__ == '__main__':
    check_differences()
