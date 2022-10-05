#!/usr/bin/env python3

###########################################################
# A simple bitarray to manage large amounts (billions+) of bits
###########################################################

# Before you use this code, have a look at bitarray on PyPI.org
# https://pypi.org/project/bitarray/
# https://pypi.org/project/bitarray/ is a lot more powerful.

# $ pip install bitarray
# $ echo "dummy bits" > data # our bits file
# $ python
# Python 3.10.7
# >>> from bitarray import bitarray
# >>> b = bitarray()
# >>> b
# bitarray()
# >>> with open('data',"rb") as file:
# ...     b.fromfile(file)
# ...
# >>> b
# bitarray('0110011001101111011011110110110000001010')
# >>> b[0]
# 0
# >>> b[1]
# 1
# >>> b[0] = 1
# >>> b[0]
# 1
# >>> b
# bitarray('1110011001101111011011110110110000001010')
# >>>
# >>> with open('data',"wb") as file:
# ...     b.tofile(file)
# ...
# >>>
# @disp2458 ~$ cat data # note how first bit changed
# �ool
#

# # For small amount of bits (up to ca. 4300 bits)
# # this trivial solution just using an interger is
# # sufficient. Above 4300 bits it will create errors.
# # Note this works, right-to-left. First bit is the right-most bit.
# def get_normalized_bit(value, bit_index):
#   return (value >> bit_index) & 1
# def set_bit(value, bit_index):
#   return value | (1 << bit_index)
# def clear_bit(value, bit_index):
#   return value & ~(1 << bit_index)
# def toggle_bit(value, bit_index):
#   return value ^ (1 << bit_index)
# # you read from a file into a bytearray
# # ba = bytearray(1_000_000)
# ba = bytearray(10)
# index=2 # example
# b = ba[index] # b represents a byte (but is int)
# b = set_bit(b, 5) # as example we set bit 5 (0-7)
# ba[index] = b # write it back to bytearray
# # ba == bytearray(b'\x00\x00 \x00\x00\x00\x00\x00\x00\x00')
# b = ba[index]
# b = set_bit(b, 6)
# ba[index] = b
# # ba == bytearray(b'\x00\x00`\x00\x00\x00\x00\x00\x00\x00')
# b = ba[index]
# b = set_bit(b, 4)
# ba[index] = b
# # ba == bytearray(b'\x00\x00p\x00\x00\x00\x00\x00\x00\x00')
# print(ba)
# # end of tiny trivial bitarray solution


# the better solution based on a bytearray. Should be able to
# handle billions of bits.
# Note: bits are represented left-to-right, the first bit is the left-most.
def get_bit_in_bytearray(ba, bit_index):
    if (bit_index // 8 >= len(ba)) or (bit_index < 0):
        raise Exception("you shouln't do that")
    b = ba[bit_index // 8]
    return (b >> (7 - bit_index % 8)) & 1


def set_bit_in_bytearray(ba, bit_index):
    b = ba[bit_index // 8]
    b = b | (1 << (7 - bit_index % 8))
    ba[bit_index // 8] = b
    return


def set_byte_in_bytearray(ba, byte_index, val):
    ba[byte_index] = val
    return ba


def clear_bit_in_bytearray(ba, bit_index):
    b = ba[bit_index // 8]
    b = b & ~(1 << (7 - bit_index % 8))
    ba[bit_index // 8] = b
    return


def toggle_bit_in_bytearray(ba, bit_index):
    b = ba[bit_index // 8]
    b = b ^ (1 << (7 - bit_index % 8))
    ba[bit_index // 8] = b
    return (b >> (7 - bit_index % 8)) & 1  # return new value


def print_bits_in_bytearray(ba):
    for i in range(len(ba)):
        end = "\n" if (i % 8 == 7) or (i == len(ba) - 1) else " "
        print(f"{ba[i]:08b}", end=end)


# you read (a piece) from a file into a bytearray
# basize = 125_000_000 # size in bytes, 1 billion bits
basize = 10  # size in bytes
bsize = basize * 8  # size in bits, bits available
maxindex = bsize - 1  # maximum index
ba = bytearray(basize)
# some initial state, this would come from file
set_byte_in_bytearray(ba, 0, 0b1000_0000)  # set bit 0
set_byte_in_bytearray(ba, 1, 0b1000_1000)  # set bit 8 and 12
set_byte_in_bytearray(ba, 2, 0)  # bits 16..23 are 0
set_byte_in_bytearray(ba, 3, 0b0000_0001)  # set bit 31
print("initial state: bits 0, 8, 12, 31 are set")
print_bits_in_bytearray(ba)
# now play
set_bit_in_bytearray(ba, 2)
print("added bit 2")
print_bits_in_bytearray(ba)

toggle_bit_in_bytearray(ba, 8)
print("toggled bit 8")
print_bits_in_bytearray(ba)

toggle_bit_in_bytearray(ba, 8)
print("toggled bit 8")
print_bits_in_bytearray(ba)

set_bit_in_bytearray(ba, maxindex)
print(f"set bit {maxindex}")
print_bits_in_bytearray(ba)

clear_bit_in_bytearray(ba, 8)
print("cleared bit 8")
print_bits_in_bytearray(ba)

bit = get_bit_in_bytearray(ba, maxindex)
print(f"get bit {maxindex}: {bit}")

toggle_bit_in_bytearray(ba, maxindex)
print(f"toggled bit {maxindex}")
print_bits_in_bytearray(ba)

bit = get_bit_in_bytearray(ba, maxindex)
print(f"get bit {maxindex}: {bit}")

print("error coming")
try:
    get_bit_in_bytearray(ba, maxindex + 1)  # error
except Exception as e:
    print(f"exception: {e}")

# # output generated:
# # =================
# initial state: bits 0, 8, 12, 31 are set
# 10000000 10001000 00000000 00000001 00000000 00000000 00000000 00000000
# 00000000 00000000
# added bit 2
# 10100000 10001000 00000000 00000001 00000000 00000000 00000000 00000000
# 00000000 00000000
# toggled bit 8
# 10100000 00001000 00000000 00000001 00000000 00000000 00000000 00000000
# 00000000 00000000
# toggled bit 8
# 10100000 10001000 00000000 00000001 00000000 00000000 00000000 00000000
# 00000000 00000000
# set bit 79
# 10100000 10001000 00000000 00000001 00000000 00000000 00000000 00000000
# 00000000 00000001
# cleared bit 8
# 10100000 00001000 00000000 00000001 00000000 00000000 00000000 00000000
# 00000000 00000001
# get bit 79: 1
# toggled bit 79
# 10100000 00001000 00000000 00000001 00000000 00000000 00000000 00000000
# 00000000 00000000
# get bit 79: 0
# error coming
# exception: you shouln't do that

# end of program
