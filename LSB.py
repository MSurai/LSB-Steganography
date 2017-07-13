from PIL import Image


def main():
    filename = "antigone.txt"

    with open(filename, 'r') as myfile:
        msg = myfile.read().replace('\n', '')

    # msg = "Hallo Welt! Hier ist Text, der in einem Bild versteckt wurde. Noch ein bisschen mehr Text um auch wirklich etwas zu verstecken."

    print("msg:")
    print(msg)

    img = Image.open("Garten1.jpeg")
    encrypt(img, msg)

    img = Image.open("hidden.png")
    decrypted = decrypt(img)

    print("decrypted:")
    print(decrypted)


def encrypt(img, msg):
    img = img.convert("RGB")
    bin_msg = ""

    for char in msg:
        bin_msg += format(ord(char), "08b")

    while len(bin_msg) % 8 != 0:
        bin_msg += "0"

    x = 0
    y = 0

    bin_msg = list(bin_msg)
    while len(bin_msg) > 0:
        while len(bin_msg) < 6:
            bin_msg.append("0")

        r, g, b = img.getpixel((x, y))
        r = apply_bitmask(r, "".join(bin_msg[0:2]))
        g = apply_bitmask(g, "".join(bin_msg[2:4]))
        b = apply_bitmask(b, "".join(bin_msg[4:6]))
        img.putpixel((x, y), (r, g, b))

        bin_msg = bin_msg[6:]

        x += 1
        if x >= img.width:
            x = 0
            y += 1

    # for i in range(0, len(bin_msg), 6):
    #     while len(bin_msg) < 6:
    #         bin_msg += "0"
    #
    #     r, g, b = img.getpixel((x, y))
    #     r = apply_bitmask(r, bin_msg[i:i+2])
    #     g = apply_bitmask(g, bin_msg[i+2:i+4])
    #     b = apply_bitmask(b, bin_msg[i+4:i+6])
    #     img.putpixel((x, y), (r, g, b))
    #
        # x += 1
        # if x >= img.width:
        #     x = 0
        #     y += 1

    img.save("hidden.png")


def apply_bitmask(value, mask):
    value = list(format(value, "08b"))
    mask = format(int(mask), "08")

    # for i in range(8):
    #     if mask[i] == "1":
    #         value[i] = mask[i]

    value[6:] = mask[6:]

    value = int("".join(value), 2)
    return value


def decrypt(img):
    img = img.convert("RGB")  # RGBA -> RGB: remove alpha layer
    bin_msg = ""

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for val in pixel:
                bin_msg += format(val, "08b")[-2:]

    while len(bin_msg) % 8 != 0:
        bin_msg += "0"

    msg = ""

    print_tmp = True

    for i in range(0, len(bin_msg), 8):
        tmp = int(bin_msg[i:i + 8], 2)
        if 32 <= tmp <= 126:
            msg += chr(tmp)
        # msg += chr(int(bin_msg[i:i + 8], 2))

    return msg


if __name__ == '__main__':
    main()


