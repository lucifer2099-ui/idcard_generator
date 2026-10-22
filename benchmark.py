import time
import numpy as np
import cv2

def paste_original(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    for i in range(rows):
        for j in range(cols):
            bg[center[0] + i, center[1] + j] = avatar[i, j]
    return bg

def paste_optimized(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    bg[center[0]:center[0]+rows, center[1]:center[1]+cols] = avatar
    return bg

# Create dummy data
avatar = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
bg1 = np.zeros((1000, 1000, 3), dtype=np.uint8)
bg2 = np.zeros((1000, 1000, 3), dtype=np.uint8)
zoom_size = (500, 670) # Output is 670 rows, 500 cols
center = (100, 100)

print("Benchmarking original...")
start = time.time()
paste_original(avatar, bg1, zoom_size, center)
orig_time = time.time() - start
print(f"Original: {orig_time:.5f}s")

print("Benchmarking optimized...")
start = time.time()
paste_optimized(avatar, bg2, zoom_size, center)
opt_time = time.time() - start
print(f"Optimized: {opt_time:.5f}s")

print(f"Speedup: {orig_time/opt_time:.2f}x")
print("Results match:", np.array_equal(bg1, bg2))
