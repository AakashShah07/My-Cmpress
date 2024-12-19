import lzma
import os

def compress_file(input_file, output_file, compression_level=lzma.PRESET_DEFAULT, chunk_size=1024*1024):
    """
    Compresses a file using the LZMA algorithm with streaming.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output compressed file.
        compression_level (int): Compression preset (0-9, higher is better but slower).
        chunk_size (int): Size of chunks to read and compress at a time.
    """
    try:
        with open(input_file, 'rb') as infile, lzma.open(output_file, 'wb', preset=compression_level) as outfile:
            while chunk := infile.read(chunk_size):
                outfile.write(chunk)
        print(f"✅ File '{input_file}' compressed successfully to '{output_file}'.")
    except Exception as e:
        print(f"❌ Error compressing file: {e}")

def decompress_file(input_file, output_file=None, chunk_size=1024*1024):
    """
    Decompresses a file using the LZMA algorithm with streaming.

    Args:
        input_file (str): Path to the compressed input file.
        output_file (str): Path to the decompressed output file (optional).
        chunk_size (int): Size of chunks to read and decompress at a time.
    """
    try:
        # Automatically deduce the output file extension if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_decompressed"

        with lzma.open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            while chunk := infile.read(chunk_size):
                outfile.write(chunk)
        print(f"✅ File '{input_file}' decompressed successfully to '{output_file}'.")
    except Exception as e:
        print(f"❌ Error decompressing file: {e}")

# Example Usage
if __name__ == "__main__":
    input_file = "temp.txt"  # Original image file
    compressed_file = "compressed_file.lzma"  # Compressed output file
    decompressed_file = "text2_recovered2.txt"  # Explicit decompressed file name

    # Compress the file
    compress_file(input_file, compressed_file, compression_level=lzma.PRESET_EXTREME)

    # Decompress the file (explicitly specifying the decompressed output name)
    decompress_file(compressed_file, decompressed_file)
