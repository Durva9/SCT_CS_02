# SCT_CS_02

Image Encryption Tool
A Python tool for encrypting and decrypting images using pixel manipulation techniques.
Description
This tool encrypts images by manipulating pixel values through channel swapping or mathematical operations, making images unrecognizable until decrypted with the correct key/pattern.
Requirements

Python 3.x
Pillow
NumPy

Install dependencies:
bashpip install -r requirements.txt
Usage
bashpython image_encryption.py
Encryption Methods
1. Pixel Swapping

Red-Blue (rb): Swap red and blue colour channels
Red-Green (rg): Swap red and green colour channels
Green-Blue (gb): Swap green and blue colour channels

2. Mathematical Operations

Add/Subtract: Add or subtract a key value (1-255) to each pixel
XOR: Applythe  XOR operation with a key
Multiply: Multiply pixels by key (not reversible)

Example
1. Choose an encryption method (swap or math operation)
2. Select your image file
3. Choose pattern/operation and enter key
4. Save the encrypted image
5. To decrypt: use the same pattern/key with the decrypt option
Features

Interactive menu interface
Multiple encryption techniques
Preserves image dimensions
Supports PNG, JPG, and other common formats
