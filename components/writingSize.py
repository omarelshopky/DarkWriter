from screeninfo import get_monitors

# Width, Margen
writingSize = {
    1920: {
         1080: [928, 102]
    },
    1680: {
        1050: [868, 102]
    },
    1600: {
        900: [760, 82]
    },
    1440: {
        900: [720, 82]
    },
    1400: {
        1050: [798, 102]
    },
    1366: {
        768: [702, 82]
    },
    1360: {
        768: [700, 82]
    },
    1280: {
        1024: [768, 102],
        960: [680, 82],
        800: [680, 82],
        768: [680, 82],
        720: [680, 82],
        600: [680, 82]
    }, 
    1152: {
        864: [648, 82]
    },
    1024: {
        768: [616, 82]
    },
    800: {
        600: [560, 82]
    }
}

def getSize():
    for m in get_monitors():
        if m.is_primary:
            height = m.height
            width = m.width

    return writingSize[width][height]
