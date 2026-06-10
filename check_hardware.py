import torch
import psutil
import os

print("--- Hardware Diagnostic ---")

# GPU Check
if torch.cuda.is_available():
    print(f"GPU Found: {torch.cuda.get_device_name(0)}")
    vram_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"Total VRAM: {vram_total:.2f} GB")
else:
    print("No CUDA GPU detected.")

# RAM Check
ram = psutil.virtual_memory()
print(f"Total System RAM: {ram.total / (1024**3):.2f} GB")
print(f"Available RAM: {ram.available / (1024**3):.2f} GB")

# Conclusion for Fine-tuning
print("\n--- Feasibility Verdict ---")
if torch.cuda.is_available() and vram_total >= 3.5:
    print("RESULT: Possible for 2B models (Gemma-2B) using Unsloth + 4-bit quantization.")
    print("CPU Offloading Note: You CAN offload to RAM, but training 81 samples might take 1-2 hours instead of 5 minutes.")
else:
    print("RESULT: GPU training not recommended. Recommend using CPU-only inference with heavy prompting (ICL) in Ollama.")
