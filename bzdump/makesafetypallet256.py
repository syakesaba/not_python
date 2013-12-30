rgb = []

for r in range(0x0, 0x100, 0x33):
    for g in range(0x0, 0x100, 0x33):
        for b in range(0x0, 0x100, 0x33):
            rgb.append( b | (g<<8) | (r<<16))
for gr in range(0x0, 0x1000000, 0x111111):
    rgb.append(gr)
rgb.append(0xC0C0C0)
rgb.append(0x808080)
rgb.append(0x800000)
rgb.append(0x800080)
rgb.append(0x008000)
rgb.append(0x008080)
#rgb[255] = 0xffffff
print map(lambda n: "%06x" % n, rgb)
print len(rgb)
