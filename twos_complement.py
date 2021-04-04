def dec_to_2s(data, digits):
  return (hex(2**digits - data))

def Twos_to_dec(hex):
  return 2**((len(hex)-2)*4) - int(hex, 16)
