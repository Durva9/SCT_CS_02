from PIL import Image # type: ignore
import numpy as np
import os


def load_image(image_path):
    """Load an image and convert to numpy array"""
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        return img, img_array
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None


def save_image(img_array, output_path):
    """Save numpy array as image"""
    try:
        img = Image.fromarray(img_array.astype('uint8'))
        img.save(output_path)
        print(f"✓ Image saved successfully: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False


def encrypt_swap_pixels(img_array, swap_pattern='rb'):
    """
    Encrypt by swapping pixel channel values
    swap_pattern options: 'rb' (red-blue), 'rg' (red-green), 'gb' (green-blue)
    """
    encrypted = img_array.copy()
    
    if len(encrypted.shape) == 3 and encrypted.shape[2] >= 3:
        if swap_pattern == 'rb':
            # Swap red and blue channels
            encrypted[:, :, 0], encrypted[:, :, 2] = img_array[:, :, 2].copy(), img_array[:, :, 0].copy()
            print("Swapped Red and Blue channels")
        elif swap_pattern == 'rg':
            # Swap red and green channels
            encrypted[:, :, 0], encrypted[:, :, 1] = img_array[:, :, 1].copy(), img_array[:, :, 0].copy()
            print("Swapped Red and Green channels")
        elif swap_pattern == 'gb':
            # Swap green and blue channels
            encrypted[:, :, 1], encrypted[:, :, 2] = img_array[:, :, 2].copy(), img_array[:, :, 1].copy()
            print("Swapped Green and Blue channels")
    else:
        print("Image must be in color (RGB) format for swapping")
        return img_array
    
    return encrypted


def decrypt_swap_pixels(img_array, swap_pattern='rb'):
    """
    Decrypt by swapping back pixel channel values
    Since swapping is reversible, same operation decrypts
    """
    return encrypt_swap_pixels(img_array, swap_pattern)


def encrypt_math_operation(img_array, key=50, operation='add'):
    """
    Encrypt by applying mathematical operation to each pixel
    operation options: 'add', 'subtract', 'xor', 'multiply'
    """
    encrypted = img_array.copy().astype(np.int32)
    
    if operation == 'add':
        encrypted = (encrypted + key) % 256
        print(f"Added {key} to each pixel value")
    elif operation == 'subtract':
        encrypted = (encrypted - key) % 256
        print(f"Subtracted {key} from each pixel value")
    elif operation == 'xor':
        encrypted = encrypted ^ key
        print(f"Applied XOR with key {key}")
    elif operation == 'multiply':
        encrypted = (encrypted * key) % 256
        print(f"Multiplied each pixel by {key}")
    
    return encrypted.astype(np.uint8)


def decrypt_math_operation(img_array, key=50, operation='add'):
    """
    Decrypt by reversing the mathematical operation
    """
    decrypted = img_array.copy().astype(np.int32)
    
    if operation == 'add':
        decrypted = (decrypted - key) % 256
        print(f"Reversed: Subtracted {key} from each pixel value")
    elif operation == 'subtract':
        decrypted = (decrypted + key) % 256
        print(f"Reversed: Added {key} to each pixel value")
    elif operation == 'xor':
        decrypted = decrypted ^ key
        print(f"Reversed: Applied XOR with key {key}")
    elif operation == 'multiply':
        # Multiply inverse in modulo 256
        # For simplicity, we'll use a different approach
        print("Note: Multiply operation may not be perfectly reversible")
        decrypted = img_array  # Cannot easily reverse multiplication in mod 256
    
    return decrypted.astype(np.uint8)


def main():
    print("=" * 60)
    print("IMAGE ENCRYPTION TOOL - PIXEL MANIPULATION")
    print("=" * 60)
    
    while True:
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. Encrypt image (Swap Pixels)")
        print("2. Decrypt image (Swap Pixels)")
        print("3. Encrypt image (Mathematical Operation)")
        print("4. Decrypt image (Mathematical Operation)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            # Encrypt with pixel swapping
            image_path = input("\nEnter the path to your image: ").strip()
            img, img_array = load_image(image_path)
            
            if img_array is not None:
                print("\nSwap patterns:")
                print("1. Red-Blue (rb)")
                print("2. Red-Green (rg)")
                print("3. Green-Blue (gb)")
                swap_choice = input("Choose swap pattern (1/2/3): ").strip()
                
                swap_patterns = {'1': 'rb', '2': 'rg', '3': 'gb'}
                swap_pattern = swap_patterns.get(swap_choice, 'rb')
                
                encrypted = encrypt_swap_pixels(img_array, swap_pattern)
                
                output_path = input("Enter output filename (e.g., encrypted_swap.png): ").strip()
                save_image(encrypted, output_path)
                print(f"\n✓ Encryption complete! Remember your swap pattern: {swap_pattern}")
        
        elif choice == '2':
            # Decrypt with pixel swapping
            image_path = input("\nEnter the path to encrypted image: ").strip()
            img, img_array = load_image(image_path)
            
            if img_array is not None:
                print("\nSwap patterns:")
                print("1. Red-Blue (rb)")
                print("2. Red-Green (rg)")
                print("3. Green-Blue (gb)")
                swap_choice = input("Choose the same swap pattern used for encryption (1/2/3): ").strip()
                
                swap_patterns = {'1': 'rb', '2': 'rg', '3': 'gb'}
                swap_pattern = swap_patterns.get(swap_choice, 'rb')
                
                decrypted = decrypt_swap_pixels(img_array, swap_pattern)
                
                output_path = input("Enter output filename (e.g., decrypted.png): ").strip()
                save_image(decrypted, output_path)
                print(f"\n✓ Decryption complete!")
        
        elif choice == '3':
            # Encrypt with mathematical operation
            image_path = input("\nEnter the path to your image: ").strip()
            img, img_array = load_image(image_path)
            
            if img_array is not None:
                print("\nMathematical operations:")
                print("1. Add (recommended)")
                print("2. Subtract (recommended)")
                print("3. XOR (recommended)")
                print("4. Multiply (not reversible)")
                op_choice = input("Choose operation (1/2/3/4): ").strip()
                
                operations = {'1': 'add', '2': 'subtract', '3': 'xor', '4': 'multiply'}
                operation = operations.get(op_choice, 'add')
                
                try:
                    key = int(input("Enter encryption key (1-255): ").strip())
                    if key < 1 or key > 255:
                        print("Key must be between 1 and 255")
                        continue
                except ValueError:
                    print("Invalid key! Using default key 50")
                    key = 50
                
                encrypted = encrypt_math_operation(img_array, key, operation)
                
                output_path = input("Enter output filename (e.g., encrypted_math.png): ").strip()
                save_image(encrypted, output_path)
                print(f"\n✓ Encryption complete! Remember your key: {key} and operation: {operation}")
        
        elif choice == '4':
            # Decrypt with mathematical operation
            image_path = input("\nEnter the path to encrypted image: ").strip()
            img, img_array = load_image(image_path)
            
            if img_array is not None:
                print("\nMathematical operations:")
                print("1. Add")
                print("2. Subtract")
                print("3. XOR")
                print("4. Multiply")
                op_choice = input("Choose the same operation used for encryption (1/2/3/4): ").strip()
                
                operations = {'1': 'add', '2': 'subtract', '3': 'xor', '4': 'multiply'}
                operation = operations.get(op_choice, 'add')
                
                try:
                    key = int(input("Enter the same encryption key used: ").strip())
                except ValueError:
                    print("Invalid key!")
                    continue
                
                decrypted = decrypt_math_operation(img_array, key, operation)
                
                output_path = input("Enter output filename (e.g., decrypted.png): ").strip()
                save_image(decrypted, output_path)
                print(f"\n✓ Decryption complete!")
        
        elif choice == '5':
            print("\nThank you for using Image Encryption Tool!")
            break
        
        else:
            print("\nInvalid choice! Please enter 1-5.")


if __name__ == "__main__":
    main()