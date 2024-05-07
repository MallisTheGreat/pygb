import os
import sys

def init_cart_tables():
    lic = [None] * 0xA5
    lic[0x00] = "None"
    lic[0x01] = "Nintendo R&D1"
    lic[0x08] = "Capcom"
    lic[0x13] = "Electronic Arts"
    lic[0x18] = "Hudson Soft"
    lic[0x19] = "b-ai"
    lic[0x20] = "kss"
    lic[0x22] = "pow"
    lic[0x24] = "PCM Complete"
    lic[0x25] = "san-x"
    lic[0x28] = "Kemco Japan"
    lic[0x29] = "seta"
    lic[0x30] = "Viacom"
    lic[0x31] = "Nintendo"
    lic[0x32] = "Bandai"
    lic[0x33] = "Ocean/Acclaim"
    lic[0x34] = "Konami"
    lic[0x35] = "Hector"
    lic[0x37] = "Taito"
    lic[0x38] = "Hudson"
    lic[0x39] = "Banpresto"
    lic[0x41] = "Ubi Soft"
    lic[0x42] = "Atlus"
    lic[0x44] = "Malibu"
    lic[0x46] = "angel"
    lic[0x47] = "Bullet-Proof"
    lic[0x49] = "irem"
    lic[0x50] = "Absolute"
    lic[0x51] = "Acclaim"
    lic[0x52] = "Activision"
    lic[0x53] = "American sammy"
    lic[0x54] = "Konami"
    lic[0x55] = "Hi tech entertainment"
    lic[0x56] = "LJN"
    lic[0x57] = "Matchbox"
    lic[0x58] = "Mattel"
    lic[0x59] = "Milton Bradley"
    lic[0x60] = "Titus"
    lic[0x61] = "Virgin"
    lic[0x64] = "LucasArts"
    lic[0x67] = "Ocean"
    lic[0x69] = "Electronic Arts"
    lic[0x70] = "Infogrames"
    lic[0x71] = "Interplay"
    lic[0x72] = "Broderbund"
    lic[0x73] = "sculptured"
    lic[0x75] = "sci"
    lic[0x78] = "THQ"
    lic[0x79] = "Accolade"
    lic[0x80] = "misawa"
    lic[0x83] = "lozc"
    lic[0x86] = "Tokuma Shoten Intermedia"
    lic[0x87] = "Tsukuda Original"
    lic[0x91] = "Chunsoft"
    lic[0x92] = "Video system"
    lic[0x93] = "Ocean/Acclaim"
    lic[0x95] = "Varie"
    lic[0x96] = "Yonezawa/s’pal"
    lic[0x97] = "Kaneko"
    lic[0x99] = "Pack in soft"
    lic[0xA4] = "Konami (Yu-Gi-Oh!)"

    return lic

def init_rom_tables():
    roms = ["ROM ONLY",
    "MBC1",
    "MBC1+RAM",
    "MBC1+RAM+BATTERY",
    "0x04 ???",
    "MBC2",
    "MBC2+BATTERY",
    "0x07 ???",
    "ROM+RAM 1",
    "ROM+RAM+BATTERY 1",
    "0x0A ???",
    "MMM01",
    "MMM01+RAM",
    "MMM01+RAM+BATTERY",
    "0x0E ???",
    "MBC3+TIMER+BATTERY",
    "MBC3+TIMER+RAM+BATTERY 2",
    "MBC3",
    "MBC3+RAM 2",
    "MBC3+RAM+BATTERY 2",
    "0x14 ???",
    "0x15 ???",
    "0x16 ???",
    "0x17 ???",
    "0x18 ???",
    "MBC5",
    "MBC5+RAM",
    "MBC5+RAM+BATTERY",
    "MBC5+RUMBLE",
    "MBC5+RUMBLE+RAM",
    "MBC5+RUMBLE+RAM+BATTERY",
    "0x1F ???",
    "MBC6",
    "0x21 ???",
    "MBC7+SENSOR+RUMBLE+RAM+BATTERY"]

    return roms

class cartridge:
    pass

class cartridge_context:
    data = []
    cart_header = cartridge()

cart_ctx = cartridge_context()

license_code = init_cart_tables()
rom_types = init_rom_tables()

def init_tables():
    lc = init_cart_tables
    rt = init_rom_tables()
    return [lc, rt]

def get_license_code(code):
    code = int.from_bytes(code, byteorder='big')
    if(code <= 0xA4):
        return license_code[code]
    
    return "UNKNOWN"

def get_rom_type(code):
    code = int.from_bytes(code, byteorder='big')
    if(code <= 0x22):
        return rom_types[code]
    
    return "UNKNOWN"

def load_cartridge(cart_name):
    print("")

    cart_ctx.filename = cart_name

    try:
        f = open(cart_name, "rb")
    except FileNotFoundError:
        print("File not found! Enter valid cart path")

    print("Opened ", cart_ctx.filename)

    cart_ctx.size = f.seek(0, os.SEEK_END)

    print("Cart size: ", cart_ctx.size, "B")

    f.seek(0)
    byte = f.read(1)
    while byte:
        cart_ctx.data.append(byte)
        byte = f.read(1)

    f.close()

    index = 0x100
    cart_ctx.cart_header.entry = b''.join(cart_ctx.data[ index : (index+4) ])
    index += 4
    cart_ctx.cart_header.logo = b''.join(cart_ctx.data[ index : (index+0x30) ])
    index += 0x30
    cart_ctx.cart_header.title = b''.join(cart_ctx.data[ index : (index+16) ])
    index += 16
    cart_ctx.cart_header.new_license_code = b''.join(cart_ctx.data[ index : (index+2) ])
    index += 2
    cart_ctx.cart_header.sgb_flag = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.type = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.rom_size = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.ram_size = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.dest_code = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.license_code = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.version = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.checksum = b''.join(cart_ctx.data[ index : (index+1) ])
    index += 1
    cart_ctx.cart_header.global_checksum = b''.join(cart_ctx.data[ index : (index+2) ])
    index += 2

    print("")
    print("ROM title: ", ''.join(map(chr, cart_ctx.cart_header.title)))
    print("Type: ", get_rom_type(cart_ctx.cart_header.type))
    print("ROM size: ", 32 << int.from_bytes(cart_ctx.cart_header.rom_size, byteorder='big'), "KB")
    print("RAM size: ", int.from_bytes(cart_ctx.cart_header.ram_size, byteorder='big'))
    print("License code: ", get_license_code(cart_ctx.cart_header.new_license_code))
    print("ROM version: ", int.from_bytes(cart_ctx.cart_header.version, byteorder='big'))
    print("Checksum: ", int.from_bytes(cart_ctx.cart_header.checksum, byteorder='big'))
    print("")

if len(sys.argv) != 2:
    print("Usage: cart.py [ROM]")
    exit()

def cart_read(address):
    return cart_ctx.data[address]

def cart_write(address, data):
    print("Not yet implemented")
    exit()

load_cartridge(sys.argv[1])