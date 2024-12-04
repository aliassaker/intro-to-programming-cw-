import unittest
import os

class TestSteganography(unittest.TestCase):
    def setUp(self):
        # Paths for testing files
        self.input_bmp = "test_input.bmp"
        self.output_bmp = "test_output.bmp"
        self.secret_message = "Test message for steganography!"

        # Create a small BMP file for testing
        with open(self.input_bmp, 'wb') as bmp_file:
            # BMP Header (54 bytes) + Minimal Pixel Data (100 bytes)
            bmp_file.write(b'BM' + (54 + 100).to_bytes(4, 'little'))  # BMP signature and file size
            bmp_file.write(b'\x00\x00\x00\x00')  # Reserved
            bmp_file.write((54).to_bytes(4, 'little'))  # Offset to pixel array
            bmp_file.write((40).to_bytes(4, 'little'))  # DIB header size
            bmp_file.write((10).to_bytes(4, 'little'))  # Width
            bmp_file.write((10).to_bytes(4, 'little'))  # Height
            bmp_file.write((1).to_bytes(2, 'little'))  # Planes
            bmp_file.write((24).to_bytes(2, 'little'))  # Bits per pixel
            bmp_file.write(b'\x00\x00\x00\x00')  # Compression
            bmp_file.write(b'\x00\x00\x00\x00')  # Image size
            bmp_file.write(b'\x00\x00\x00\x00')  # X pixels per meter
            bmp_file.write(b'\x00\x00\x00\x00')  # Y pixels per meter
            bmp_file.write(b'\x00\x00\x00\x00')  # Colors used
            bmp_file.write(b'\x00\x00\x00\x00')  # Important colors
            bmp_file.write(bytearray([255] * 100))  # Pixel data (all white)

    def test_encode_decode(self):
        # Encode the secret message into the BMP file
        encode_message_in_bmp(self.input_bmp, self.output_bmp, self.secret_message)

        # Decode the secret message from the output BMP file
        decoded_message = decode_message_from_bmp(self.output_bmp)

        # Verify the decoded message matches the original
        self.assertEqual(decoded_message, self.secret_message)

    def test_message_too_large(self):
        # Create a message that exceeds the available space in the test BMP file
        large_message = "A" * 200  # Exceeds 100 bytes (pixel array size)

        with self.assertRaises(ValueError):
            encode_message_in_bmp(self.input_bmp, self.output_bmp, large_message)

    def tearDown(self):
        # Clean up the test files
        if os.path.exists(self.input_bmp):
            os.remove(self.input_bmp)
        if os.path.exists(self.output_bmp):
            os.remove(self.output_bmp)

# Run the tests
if __name__ == "__main__":
    unittest.main()