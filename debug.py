import cv2
import numpy as np
import os

path = "Images"
myList = os.listdir(path)

for obj in myList:
    if not obj.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    
    filepath = f"{path}/{obj}"
    img = cv2.imread(filepath)
    
    print(f"\n--- {obj} ---")
    if img is None:
        print("  ERROR: cv2.imread returned None - file may be corrupt")
        continue
    
    print(f"  Shape: {img.shape}")
    print(f"  Dtype: {img.dtype}")
    print(f"  Min value: {img.min()}")
    print(f"  Max value: {img.max()}")
    
    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(f"  RGB Shape: {img_rgb.shape}")
    print(f"  RGB Dtype: {img_rgb.dtype}")
    
    # Check if it's truly 8bit
    if img.dtype != np.uint8:
        print(f"  WARNING: Image is not 8bit! dtype={img.dtype}")
        # Try to convert to uint8
        img_fixed = (img / img.max() * 255).astype(np.uint8)
        print(f"  Fixed dtype: {img_fixed.dtype}")
    else:
        print("  Image is 8bit uint8 - OK")

print("\nDone!")