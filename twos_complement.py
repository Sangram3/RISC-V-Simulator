def dec_to_2s(data, digits):
  return (hex(2**(digits*4) - data))

def Twos_to_dec(hex):
  return -(2**((len(hex)-2)*4) - int(hex, 16))
