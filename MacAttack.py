from __future__ import print_function

__author__ = 'russell'
Data = [
    0x4e, 0x6f, 0x20, 0x6f, 0x6e, 0x65, 0x20, 0x68, 0x61, 0x73, 0x20, 0x63, 0x6f, 0x6d, 0x70, 0x6c,
    0x65, 0x74, 0x65, 0x64, 0x20, 0x6c, 0x61, 0x62, 0x20, 0x32, 0x20, 0x73, 0x6f, 0x20, 0x67, 0x69,
    0x76, 0x65, 0x20, 0x74, 0x68, 0x65, 0x6d, 0x20, 0x61, 0x6c, 0x6c, 0x20, 0x61, 0x20, 0x30
]

selection = raw_input("Extension message:  ")
if selection == "":
    print("Using ' Except Russell'")
    data = " Except Russell".encode('hex')
else:
    data = selection.encode('hex')
import struct


def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def sha1(message):
    """SHA-1 Hashing Function
    A custom SHA-1 hashing function implemented entirely in Python.
    Arguments:
        message: The input message string to hash.
    Returns:
        A hex SHA-1 digest of the input message.
    """
    # Initializing variables to be the digest of our message
    # f4b645e8
    # 9faaec2f
    # f8e443c5
    # 95009c16
    # dbdfba4b

    # Initialize variables:
    h0 = 0xF4B645E8
    h1 = 0x9FAAEC2F
    h2 = 0xF8E443C5
    h3 = 0x95009C16
    h4 = 0xDBDFBA4B

    # h0 = 0xe5e9fa1b
    # h1 = 0xa31ecd1a
    # h2 = 0xe84f75ca
    # h3 = 0xaa474f3a
    # h4 = 0x663f05f4

    message
    # # Pre-processing:
    original_bit_len = len(message) * 8 + 1024
    original_byte_len = original_bit_len / 8
    # original_byte_len = len(message)
    # original_bit_len = original_byte_len * 8
    # append the bit '1' to the message
    message += b'\x80'

    # append 0 <= k < 512 bits '0', so that the resulting message length (in bits)
    #    is congruent to 448 (mod 512)
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)

    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    message += struct.pack(b'>Q', original_bit_len)
    # Process the message in successive 512-bit chunks:
    # break message into 512-bit chunks
    for i in range(0, len(message), 64):
        w = [0] * 80
        # break chunk into sixteen 32-bit big-endian words w[i]
        for j in range(16):
            w[j] = struct.unpack(b'>I', message[i + j * 4:i + j * 4 + 4])[0]
        # Extend the sixteen 32-bit words into eighty 32-bit words:
        for j in range(16, 80):
            w[j] = _left_rotate(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)

        # Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(80):
            if 0 <= i <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid ~
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
                             a, _left_rotate(b, 30), c, d)

        # sAdd this chunk's hash to result so far:
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    # Produce the final hash value (big-endian):
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


originalMessage = "4e6f206f6e652068617320636f6d706c65746564206c6162203220736f2067697665207468656d20616c6c20612030"
# This is adding a 1 bit at the beginning of the padding
originalMessage += "80"
# We stop at 512 so that we have 8 bits to add the length of the key to the end
while len(originalMessage) * 4 % 512 != 504:
    originalMessage += "0"
# This is adding the length of the key to the padding 128 bits
originalMessage += "80"

newMessage = originalMessage + data
print("Msg:  " + newMessage)
print("New Digest:  " + sha1(data))
print(sha1("7365637265748000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003020746861742063616e20626520736861726564"))
# if __name__ == '__main__':
#     # Imports required for command line parsing. No need for these elsewhere
#     import argparse
#     import sys
#     import os
#
#     # Parse the incoming arguments
#     parser = argparse.ArgumentParser()
#     parser.add_argument('input', nargs='?',
#                         help='input file or message to hash')
#     args = parser.parse_args()
#
#     data = None
#
#     if args.input is None:
#         # No argument given, assume message comes from standard input
#         try:
#             # sys.stdin is opened in text mode, which can change line endings,
#             # leading to incorrect results. Detach fixes this issue, but it's
#             # new in Python 3.1
#             data = sys.stdin.detach().read()
#         except AttributeError:
#             # Linux ans OSX both use \n line endings, so only windows is a
#             # problem.
#             if sys.platform == "win32":
#                 import msvcrt
#
#                 msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
#             data = sys.stdin.read().encode()
#     elif os.path.isfile(args.input):
#         # An argument is given and it's a valid file. Read it
#         with open(args.input, 'rb') as f:
#             data = f.read()
#     else:
#         data = args.input
#
#     # Show the final digest
#     print('sha1-digest:', sha1(data))
