import torch
import torch.nn.utils.prune as prune
from time import perf_counter

def pruning(model, mode='global', amount=0.2):
    if mode == 'local':
        for name, module in model.named_modules():
            if hasattr(module, 'weight'):  # some modules do not have a weight attribute
                # prune % amount of connections in all 2D-conv layers
                if isinstance(module, torch.nn.Conv2d):
                    prune.l1_unstructured(module, name='weight', amount=amount)  # Use L1 or Random
                    prune.remove(module, 'weight')  # This makes pruning permanent
                    
                ### Add code for pruning Linear layers

    elif mode == 'global':
        parameters_to_prune = []
        for name, module in model.named_modules():
            if hasattr(module, 'weight'):  # some modules do not have a weight attribute
                parameters_to_prune.append((module, 'weight'))
        prune.global_unstructured(
            parameters_to_prune,
            pruning_method=prune.RandomUnstructured,  # use L1Unstructured or RandomUnstructured
            amount=amount,
        )
        for name, module in model.named_modules():
            if hasattr(module, 'weight'):  # some modules do not have a weight attribute
                prune.remove(module, 'weight')  # This makes pruning permanent

    print(dict(model.named_buffers()).keys())  # to verify that all masks exist

    num_params = 0
    for p in model.parameters():
        num_params += p.numel()
    print('Total Parameters: {:.3f}M'.format(num_params/1e6))

    return model


# Note: torch.ao.quantization... is prefered for newer python versions
def quantization(model, dtype=torch.float16):
    # Change model weights to specified dtype
    for param in model.parameters():
        if param.requires_grad:
            param.data = param.data.to(dtype=dtype)

    # Change buffers (if any) to dtype as well
    for buffer_name, buffer in model.named_buffers():
        buffer.data = buffer.data.to(dtype=dtype)

    return model

