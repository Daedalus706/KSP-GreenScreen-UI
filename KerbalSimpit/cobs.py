def cobs_encode(data:list[bytes]) -> list[bytes]:
    encode = []         # Encoded byte list
    codep = 0           # Output code pointer
    code = 1            # Code value
    encode.append(0)    # Reserve space for the first code byte

    for byte in data:
        if byte: # Byte not zero, write it
            encode.append(byte)
            code += 1
        if not byte or code == 0xff: # Input is zero or block completed, restart
            encode[codep] = code
            code = 1
            codep = len(encode)
            encode.append(0) # Reserve space for the next code byte

    encode[codep] = code  # Write final code value
    return encode


def cobs_decode(buffer: list[bytes]) -> list[bytes]:
    byte = iter(buffer) # Encoded input byte pointer as an iterator
    decode = []         # Decoded output byte list
    code = 0xff         # Condition to read first block
    block = 0

    try:
        while True:
            if block > 1:
                # Decode block byte
                decode.append(next(byte))
                block -= 1
            else:
                if code != 0xff:
                    decode.append(0) # Encoded zero, write it
                # Get the next block length
                block = code = next(byte)
                if code == 0:  # Delimiter code found
                    break

    except StopIteration:
        pass
    return decode
