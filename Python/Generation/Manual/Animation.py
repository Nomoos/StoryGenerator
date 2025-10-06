from diffusers import StableDiffusionPipeline
import torch
import numpy as np
from PIL import Image
import os

# 🔧 Načtení pipeline s modelem (musíš mít model stažený nebo použít HuggingFace login)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# 🔢 Pomocná funkce pro interpolaci latentního prostoru
def interpolate_latents(latent1, latent2, steps):
    return [(1 - alpha) * latent1 + alpha * latent2 for alpha in np.linspace(0, 1, steps)]

# 🎨 Prompty pro obrázky A a B
prompt_a = "a young girl looking down, sad expression, moody lighting, standing in a dimly lit school hallway, cinematic, shallow depth of field, photorealistic, 35mm, natural skin texture, soft shadows"
prompt_b = "a young girl looking forward with worried expression, brightly lit school hallway, realistic lighting, soft focus background, backpack on her shoulders, photorealistic, 35mm, shallow depth of field"

# Získání latentů pro oba obrázky
with torch.no_grad():
    latent_a = pipe(prompt_a, num_inference_steps=30, output_type="latent").images[0]
    latent_b = pipe(prompt_b, num_inference_steps=30, output_type="latent").images[0]

# 🌀 Interpoluj latenty
latent_sequence = interpolate_latents(latent_a, latent_b, steps=16)

# 🖼️ Vygeneruj obrázky ze sekvence latentů
output_dir = "output_frames"
os.makedirs(output_dir, exist_ok=True)

for i, latent in enumerate(latent_sequence):
    with torch.no_grad():
        image = pipe.decode_latents(latent.unsqueeze(0))[0]
        image = Image.fromarray((image * 255).astype(np.uint8))
        image.save(os.path.join(output_dir, f"frame_{i:03d}.png"))
