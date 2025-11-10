# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Signifigant Bit (LSB) encoding.

from PIL import Image
import os

def numberToBinary(num):
    """Converts a base-10 number into an 8-bit binary string."""
    binary = bin(num)[2:]      # Convert to binary and remove '0b'
    return binary.zfill(8)     # Pad to 8 bits

def binaryToNumber(binaryString):
    """Converts an 8-bit binary string back into a base-10 integer."""
    return int(binaryString, 2)

def encode(img, msg):
    pixels = img.load()
    width, height = img.size
    msgLength = len(msg)

    # Store message length in the RED value of pixel (0,0)
    r, g, b = pixels[0, 0]
    pixels[0, 0] = (msgLength, g, b)

    pixel_index = 0
    char_index = 0

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        r, g, b = pixels[x, y]
        r_bin = numberToBinary(r)
        g_bin = numberToBinary(g)
        b_bin = numberToBinary(b)

        if pixel_index % 3 == 0:
            letterBinary = numberToBinary(ord(msg[char_index]))
            g_bin = g_bin[:7] + letterBinary[0]
            b_bin = b_bin[:7] + letterBinary[1]

        elif pixel_index % 3 == 1:
            r_bin = r_bin[:7] + letterBinary[2]
            g_bin = g_bin[:7] + letterBinary[3]
            b_bin = b_bin[:7] + letterBinary[4]

        elif pixel_index % 3 == 2:
            r_bin = r_bin[:7] + letterBinary[5]
            g_bin = g_bin[:7] + letterBinary[6]
            b_bin = b_bin[:7] + letterBinary[7]
            char_index += 1

        pixels[x, y] = (binaryToNumber(r_bin), binaryToNumber(g_bin), binaryToNumber(b_bin))
        pixel_index += 1

    img.save("secretImg.png", "PNG")


def decode(img):
    pixels = img.load()
    r, g, b = pixels[0, 0]
    msgLength = r

    width, height = img.size
    msg = ""
    pixel_index = 0
    binary_letter = ""

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        r, g, b = pixels[x, y]
        r_bin = numberToBinary(r)
        g_bin = numberToBinary(g)
        b_bin = numberToBinary(b)

        if pixel_index % 3 == 0:
            binary_letter = g_bin[7] + b_bin[7]

        elif pixel_index % 3 == 1:
            binary_letter += r_bin[7] + g_bin[7] + b_bin[7]

        elif pixel_index % 3 == 2:
            binary_letter += r_bin[7] + g_bin[7] + b_bin[7]
            msg += chr(binaryToNumber(binary_letter))

        pixel_index += 1

    return msg


def main():
    # Example usage
    img = Image.open("pki.png")  # your original image
    message = "This is a secret message hidden in the image!"
    encode(img, message)
    img.close()

    new_img = Image.open("secretImg.png")
    print("Decoded Message:", decode(new_img))

if __name__ == "__main__":
    main()
