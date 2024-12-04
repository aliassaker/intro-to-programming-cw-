def encode_message_in_bmp(input_bmp, output_bmp, message):
    """
    Encodes a secret message into a BMP picture using least significant bit or LSB modification.
    """
    # Make sure the message ends with a unique marker like `'\0'` to indicate its ending.
    message += '\0'
    # Transform the message into its binary form.
    message_bits = ''.join(f'{ord(c):08b}' for c in message)

    # Access the input BMP picture using binary read mode.
    with open(input_bmp, 'rb') as bmp_file:
        # Extract the BMP header by reading the first 54 bytes, which is the standard bytes for BMP pictures.
        header = bmp_file.read(54)
        if header[:2] != b'BM':
            raise ValueError("not a valid BMP file.")
        
        # Retrieve the remaining data from the BMP picture, which contains the pixel array.
        pixel_data = bytearray(bmp_file.read())

    # put the secret message in the smallest bit in the bmp picture
    bit_index = 0
    for i in range(len(pixel_data)):
        if bit_index < len(message_bits):
            # Modify the smallest bit of each byte
            pixel_data[i] = (pixel_data[i] & 0xFE) | int(message_bits[bit_index])
            bit_index += 1
        else:
            break

    # Check if the whole message was put in the smallest bit of the bmp picture
    if bit_index < len(message_bits):
        raise ValueError("this message is too big to hide in this BMP image.")

    # Save the modified pixel data to the output BMP picture
    with open(output_bmp, 'wb') as output_file:
        output_file.write(header)         # Write the BMP header
        output_file.write(pixel_data)    # Write the modified pixel data

    print(f"Message successfully hidden in {output_bmp}!")

def decode_message_from_bmp(stego_bmp):
    """
    Decodes a secret message hidden in a BMP file.
    """
    # Open the stego BMP picture in binary read mode
    with open(stego_bmp, 'rb') as bmp_file:
        # Skip the BMP header (54 bytes)
        bmp_file.seek(54)
        pixel_data = bmp_file.read()

    # Extract the smallest bits from the pixel data
    bits = []
    for byte in pixel_data:
        bits.append(byte & 1)  # Extract the smallest bit

    # Group bits into bytes and convert to characters
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        char = chr(int(''.join(map(str, byte)), 2))
        if char == '\0':  # Stop at the null terminator
            break
        chars.append(char)

    # Return the reconstructed message
    return ''.join(chars)

# Main program
if __name__ == "__main__":
    # Define file paths
    input_bmp = "/Users/aliassaker/Downloads/flowers.bmp"  # Path to the input BMP file
    output_bmp = "/Users/aliassaker/Downloads/stego_flowers.bmp"  # Path for the output BMP file

    # Define the secret message
    secret_message = "dr. shaimaa, sherine, and shorouk are the best!"

    try:
        # first step, Encode the message into the BMP file
        encode_message_in_bmp(input_bmp, output_bmp, secret_message)
        print("Message successfully hidden!")

        # Second step, Decode the message from the BMP file to verify
        retrieved_message = decode_message_from_bmp(output_bmp)
        print("Retrieved message:", retrieved_message)
    except Exception as e:
        # Print any errors that happened during encoding and decoding
        print(f"An error occurred: {e}")