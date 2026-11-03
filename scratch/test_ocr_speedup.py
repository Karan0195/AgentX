import time
from PIL import Image
import numpy as np

# Test blank page detection speed
img_blank = Image.new("RGB", (1240, 1754), color="white")
t0 = time.time()
img_np = np.array(img_blank)
is_blank = np.std(img_np) < 5
t_check = time.time() - t0
print(f"Blank check on 1240x1754 image: {t_check*1000:.2f}ms (is_blank={is_blank})")

# Test 150 DPI vs 300 DPI OCR speed
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()

# Image with some text
from PIL import ImageDraw
img_150 = Image.new("RGB", (1240, 1754), color="white")
d = ImageDraw.Draw(img_150)
d.text((100, 100), "VOTER CARD ID: ABC1234567\nName: Ramesh Patil\nAge: 45", fill="black")

t0 = time.time()
res150, _ = ocr(np.array(img_150))
t150 = time.time() - t0
print(f"150 DPI OCR time: {t150:.3f}s (Result: {len(res150 or [])} lines)")
