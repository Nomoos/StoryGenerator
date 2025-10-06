import torch

print("Torch:", torch.__version__)
print("CUDA version:", torch.version.cuda)
print("Device:", torch.cuda.get_device_name(0))
print("Available:", torch.cuda.is_available())