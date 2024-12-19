import random
from sympy import isprime, mod_inverse
import lzma

def generate_keys(p):
    """
    Generate ElGamal public and private keys.
    Args:
        p (int): A large prime number.
    Returns:
        tuple: (public_key, private_key)
    """
    g = random.randint(2, p - 1)
    x = random.randint(2, p - 2)  # Private key
    y = pow(g, x, p)  # Public key component
    public_key = (p, g, y)
    private_key = x
    return public_key, private_key

def elgamal_encrypt(public_key, plaintext_bytes):
    """
    Encrypt data using ElGamal encryption.
    Args:
        public_key (tuple): ElGamal public key (p, g, y).
        plaintext_bytes (bytes): Data to encrypt.
    Returns:
        list: Encrypted ciphertext as (c1, c2) pairs.
    """
    p, g, y = public_key
    k = random.randint(2, p - 2)  # Random ephemeral key
    c1 = pow(g, k, p)
    ciphertext = []
    for byte in plaintext_bytes:
        c2 = (byte * pow(y, k, p)) % p
        ciphertext.append((c1, c2))
    return ciphertext

def elgamal_decrypt(private_key, p, ciphertext):
    """
    Decrypt ElGamal encrypted data.
    Args:
        private_key (int): ElGamal private key.
        p (int): Prime number used in encryption.
        ciphertext (list): Encrypted data as (c1, c2) pairs.
    Returns:
        bytes: Decrypted plaintext bytes.
    """
    plaintext_bytes = []
    for c1, c2 in ciphertext:
        s = pow(c1, private_key, p)
        s_inv = mod_inverse(s, p)  # Compute modular inverse of s
        byte = (c2 * s_inv) % p
        plaintext_bytes.append(byte)
    return bytes(plaintext_bytes)

def compress_file(input_file, output_file):
    """Compress a file using LZMA."""
    with open(input_file, 'rb') as infile, lzma.open(output_file, 'wb') as outfile:
        outfile.write(infile.read())

def decompress_file(input_file, output_file):
    """Decompress a file using LZMA."""
    with lzma.open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        outfile.write(infile.read())

# Example Usage
if __name__ == "__main__":
    # Generate ElGamal Keys
    p = 2**17 - 1  # A prime number for simplicity (replace with a larger prime in real use)
    if not isprime(p):
        raise ValueError("p must be a prime number.")
    
    public_key, private_key = generate_keys(p)
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    # Compress a file
    input_file = "temp.txt"
    compressed_file = "compressed_file.lzma"
    compress_file(input_file, compressed_file)
    print(f"Compressed file created: {compressed_file}")

    # Encrypt the compressed file
    with open(compressed_file, 'rb') as f:
        plaintext_bytes = f.read()

    encrypted_file = "compressed_file_encrypted.elg"
    ciphertext = elgamal_encrypt(public_key, plaintext_bytes)
    with open(encrypted_file, 'w') as f:
        for c1, c2 in ciphertext:
            f.write(f"{c1},{c2}\n")
    print(f"Encrypted file created: {encrypted_file}")

    # Decrypt the file
    decrypted_file = "compressed_file_decrypted.lzma"
    with open(encrypted_file, 'r') as f:
        ciphertext = [tuple(map(int, line.strip().split(','))) for line in f]

    decrypted_bytes = elgamal_decrypt(private_key, p, ciphertext)
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted_bytes)
    print(f"Decrypted file created: {decrypted_file}")

    # Decompress the file
    output_file = "NewTemp.txt"
    decompress_file(decrypted_file, output_file)
    print(f"Recovered file created: {output_file}")
