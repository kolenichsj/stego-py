import os

#based on code by Dr Eric Cole

def hideinHTML(overt_inPath: str, overt_outPath: str, covert_Path: str):
    """Converts bytes of covert file to spaces and tabs and replaces the existing tabs and spaces in overt file"""
    ONE = bytes(chr(32), encoding='UTF-8') # space
    ZERO = bytes(chr(9), encoding='UTF-8') # tab

    with open(overt_inPath, 'rb', buffering=16) as overt_in, open(overt_outPath, 'wb', buffering=16) as overt_out, open(covert_Path, 'rb', buffering=16) as covert_in:
        nextchar = overt_in.read(1)
        nextcovbyte = covert_in.read(1)
        mask = 1
        if not (nextchar == b'' and nextcovbyte==b''):
            overt_out.write(bytes('<!--' + '{:08X}'.format(os.path.getsize(covert_Path)) + '-->', 'utf-8'))
        
        while not (nextchar == b'' and nextcovbyte==b''):
            if ((nextchar in ([b' ', b'\t', b''])) and nextcovbyte!=b''):
                if nextcovbyte[0] & mask == 0:
                    overt_out.write(ZERO)
                else:
                    overt_out.write(ONE)

                mask = mask<<1

                if (mask & 256==256):
                    nextcovbyte = covert_in.read(1)
                    mask = 1
            else:
                overt_out.write(nextchar)
            nextchar = overt_in.read(1)

def getFromHTML(overt_inPath: str, covert_outPath: str):
    """Converts tabs and spaces in overt file to bytes of covert file"""
    ONE = bytes(chr(32), encoding='UTF-8') # space
    ZERO = bytes(chr(9), encoding='UTF-8') # tab
    with open(overt_inPath, 'rb', buffering=16) as overt_in, open(covert_outPath, 'wb', buffering=16) as covert_out:
        nextchar = overt_in.read(15)
        if (len(nextchar)==15):
            marker = nextchar.decode('utf-8')
            totalbits = int(marker[4:12],16)*8
            
        nextchar = overt_in.read(1)
        mask = 1
        nextbyte=0
        bitcount = 0
        
        while (nextchar != b'' and bitcount < totalbits):
            if (nextchar == ONE):
                nextbyte = nextbyte | mask
                mask = mask<<1
                bitcount+=1
            elif (nextchar == ZERO):
                mask = mask<<1
                bitcount+=1

            if (mask & 256==256):
                covert_out.write(bytes([nextbyte]))
                mask = 1
                nextbyte=0

            nextchar = overt_in.read(1)
