#!/usr/bin/env python
# encoding: utf-8

def makeSafetyPallet256():
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
    for i in range(17):
        rgb.append(0x000000)
    rgb.append(0xffffff)
    return rgb
RGB = makeSafetyPallet256()
for x,c in enumerate(RGB):
    print "0x%02x:0x%06x" % (x,c)
print "colorcode.length = ",len(RGB)

