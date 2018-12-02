#!/usr/bin/python

from __future__ import print_function

import json
import argparse
import sys

device_lookup = {
    (0x62, 0x00): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x01): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x63, 0x02): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x63, 0x11): {'id_shift': 5, 'fuses': 'pic_fuses'},

    (0x63, 0x12): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x14): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x17): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x20): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x63, 0x21): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x63, 0x22): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x63, 0x23): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x34): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x37): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x41): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x42): {'id_shift': 5, 'fuses': 'pic_fuses'},
    # (0x63, 0x54): {'id_shift': 5, 'fuses': 'pic_fuses', 'name': '"PIC16F818/9"'},
    (0x63, 0x54): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x63, 0x61): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x63, 0x62): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x63, 0x73): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0x81): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x63, 0x82): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x63, 0x91): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x63, 0x92): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x63, 0xA4): {'fuses': 'pic_fuses'},
    (0x63, 0xB3): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0xC4): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x63, 0xC7): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x64, 0x01): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x64, 0x02): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x64, 0x11): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x64, 0x12): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x65, 0x00): {'fuses': 'pic_fuses'},
    (0x65, 0x04): {'fuses': 'pic_fuses'},
    (0x65, 0x05): {'fuses': 'pic_fuses'},
    (0x65, 0x13): {'fuses': 'pic_fuses'},
    (0x65, 0x16): {'fuses': 'pic_fuses'},
    (0x65, 0x23): {'fuses': 'pic_fuses'},
    (0x66, 0x01): {'fuses': 'pic_fuses'},
    (0x66, 0x02): {'fuses': 'pic_fuses'},
    (0x66, 0x03): {'fuses': 'pic_fuses'},
    (0x66, 0x04): {'fuses': 'pic_fuses'},
    (0x66, 0x07): {'fuses': 'pic_fuses'},
    (0x66, 0x13): {'fuses': 'pic_fuses'},
    (0x66, 0x17): {'fuses': 'pic_fuses'},
    (0x66, 0x23): {'fuses': 'pic_fuses'},

    (0x71, 0x00): {'fuses': 'avr2_fuses'},
    (0x71, 0x01): {'fuses': 'avr_fuses'},
    (0x71, 0x0A): {'fuses': 'avr3_fuses'},
    (0x71, 0x20): {'fuses': 'avr2_fuses'},
    (0x71, 0x21): {'fuses': 'avr_fuses'},
    (0x71, 0x22): {'fuses': 'avr2_fuses'},
    (0x71, 0x2A): {'fuses': 'avr3_fuses'},
    (0x71, 0x43): {'fuses': 'avr2_fuses'},
    (0x71, 0x44): {'fuses': 'avr_fuses'},
    (0x71, 0x48): {'fuses': 'avr3_fuses'},
    (0x71, 0x49): {'fuses': 'avr3_fuses'},
    (0x71, 0x61): {'fuses': 'avr_fuses'},
    (0x71, 0x6B): {'fuses': 'avr3_fuses'},
    (0x71, 0x85): {'fuses': 'avr2_fuses'},
    (0x73, 0x10): {'fuses': 'avr2_fuses'},
    (0x73, 0x12): {'fuses': 'avr2_fuses'},

    (0x17, 0x00): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x01): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x18, 0x02): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x18, 0x11): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x12): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x14): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x17): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x20): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x18, 0x21): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x18, 0x22): {'id_shift': 4, 'fuses': 'pic_fuses'},
    (0x18, 0x23): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x34): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x37): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x41): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x42): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x54): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x18, 0x61): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x18, 0x62): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x18, 0x73): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0x81): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x18, 0x82): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x18, 0x91): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x18, 0x92): {'id_shift': 5, 'fuses': 'pic2_fuses'},
    (0x18, 0xA4): {'fuses': 'pic_fuses'},
    (0x18, 0xB3): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0xC4): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x18, 0xC7): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x19, 0x01): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x19, 0x02): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x19, 0x11): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x19, 0x12): {'id_shift': 5, 'fuses': 'pic_fuses'},
    (0x1A, 0x00): {'fuses': 'pic_fuses'},
    (0x1A, 0x04): {'fuses': 'pic_fuses'},
    (0x1A, 0x05): {'fuses': 'pic_fuses'},
    (0x1A, 0x13): {'fuses': 'pic_fuses'},
    (0x1A, 0x16): {'fuses': 'pic_fuses'},
    (0x1A, 0x23): {'fuses': 'pic_fuses'},
    (0x1B, 0x01): {'fuses': 'pic_fuses'},
    (0x1B, 0x02): {'fuses': 'pic_fuses'},
    (0x1B, 0x03): {'fuses': 'pic_fuses'},
    (0x1B, 0x04): {'fuses': 'pic_fuses'},
    (0x1B, 0x07): {'fuses': 'pic_fuses'},
    (0x1B, 0x13): {'fuses': 'pic_fuses'},
    (0x1B, 0x17): {'fuses': 'pic_fuses'},
    (0x1B, 0x23): {'fuses': 'pic_fuses'},

    (0x1D, 0x00): {'fuses': 'avr2_fuses'},
    (0x1D, 0x01): {'fuses': 'avr_fuses'},
    (0x1D, 0x0A): {'fuses': 'avr3_fuses'},
    (0x1D, 0x20): {'fuses': 'avr2_fuses'},
    (0x1D, 0x21): {'fuses': 'avr_fuses'},
    (0x1D, 0x22): {'fuses': 'avr2_fuses'},
    (0x1D, 0x2A): {'fuses': 'avr3_fuses'},
    (0x1D, 0x43): {'fuses': 'avr2_fuses'},
    (0x1D, 0x44): {'fuses': 'avr_fuses'},
    (0x1D, 0x48): {'fuses': 'avr3_fuses'},
    (0x1D, 0x49): {'fuses': 'avr3_fuses'},
    (0x1D, 0x61): {'fuses': 'avr_fuses'},
    (0x1D, 0x6B): {'fuses': 'avr3_fuses'},
    (0x1D, 0x85): {'fuses': 'avr2_fuses'},
    (0x1E, 0x10): {'fuses': 'avr2_fuses'},
    (0x1E, 0x12): {'fuses': 'avr2_fuses'},
}

write_unlock_lookup = {
    0x0000: 0x0002,
    0x0001: 0x0002,
    0x0002: 0x0002,
    0x0003: 0x0002,
    0x0004: 0x0003,
    0x0005: 0x0003,
    0x0006: 0x0003,
    0x0007: 0x0003,
    0x0008: 0x0003,
    0x0009: 0x0003,
    0x000A: 0x0003,
    0x000B: 0x0003,
    0x000C: 0x0003,
    0x000D: 0x0002,
    0x000E: 0x0002,
    0x000F: 0x0003,
    0x0010: 0x0002,
    0x0011: 0x0001,
    0x0012: 0x0001,
    0x0013: 0x0002,
    0x0014: 0x0001,
    0x0015: 0x0003,
    0x0016: 0x0003,
    0x0017: 0x0001,
    0x0018: 0x00A4,
    0x0019: 0x0001,
    0x001A: 0x0001,
    0x001B: 0x0001,
    0x001C: 0x0096,
    0x001D: 0x006D,
    0x001E: 0x0074,
    0x001F: 0x0075,
    0x4E20: 0x0001,
    0x0021: 0x0001,
    0x0022: 0x0001,
    0x0023: 0x0001,
    0x0024: 0x0001,
    0x0025: 0x0001,
    0x0026: 0x0001,
    0x0027: 0x0001,
    0x0028: 0x0001,
    0x0029: 0x0001,
    0x002A: 0x00E0,
    0x002B: 0x00CF,
    0x002C: 0x0074,
    0x002D: 0x0001,
    0x002E: 0x0001,
    0x002F: 0x0001,
    0x0030: 0x0001,
    0x0031: 0x0001,
    0x0032: 0x0001,
    0x0033: 0x0001,
    0x0034: 0x00A6,
    0x0035: 0x007F,
    0x0036: 0x0001,
    0x0037: 0x0001,
    0x0038: 0x0001,
    0x0039: 0x00CF,
    0x003A: 0x0001,
    0x003B: 0x0001,
    0x003C: 0x0001,
    0x003D: 0x0001,
    0x003E: 0x0001,
    0x003F: 0x0148,
    0x0040: 0x01BA,
    0x0041: 0x0001,
    0x0042: 0x0001,
    0x0043: 0x0001,
    0x0044: 0x0001,
    0x0045: 0x0001,
    0x0046: 0x0154,
    0x0047: 0x019B,
    0x0048: 0x01DF,
    0x0049: 0x011E,
    0x004A: 0x01BA,
    0x004B: 0x01E7,
    0x004C: 0x004E,
    0x004D: 0x011B,
    0x004E: 0x0198,
    0x004F: 0x0025,
    0x0050: 0x0013,
    0x0051: 0x00BF,
    0x0052: 0x0001,
    0x0053: 0x0115,
    0x0054: 0x0198,
    0x0055: 0x0118,
    0x0056: 0x011E,
    0x0057: 0x0139,
    0x0058: 0x01E0,
    0x0059: 0x008F,
    0x005A: 0x01D6,
    0x005B: 0x00F1,
    0x005C: 0x0167,
    0x005D: 0x000D,
    0x005E: 0x0001,
    0x005F: 0x0001,
    0x0060: 0x01FF,
    0x0061: 0x00F1,
    0x0062: 0x0100,
    0x0063: 0x00D7,
    0x0064: 0x0005,
    0x0065: 0x0083,
    0x0066: 0x000D,
    0x0067: 0x0001,
    0x0068: 0x0041,
    0x0069: 0x01FF,
    0x006A: 0x0001,
    0x006B: 0x0100,
    0x006C: 0x0090,
    0x006D: 0x000A,
    0x006E: 0x0077,
    0x006F: 0x000A,
    0x0070: 0x0001,
    0x0071: 0x0021,
    0x0072: 0x01FF,
    0x0073: 0x0031,
    0x0074: 0x0100,
    0x0075: 0x0101,
    0x0076: 0x000E,
    0x0077: 0x00D0,
    0x0078: 0x000A,
    0x0079: 0x0001,
    0x007A: 0x0005,
    0x007B: 0x01FF,
    0x0080: 0x00FB,
    0x0081: 0x0001,
    0x0082: 0x0001,
    0x0083: 0x0003,
    0x0084: 0x0135,
    0x0085: 0x0002,
    0x0086: 0x00DD,
    0x0087: 0x0002,
    0x0088: 0x0005,
    0x0089: 0x0001,
    0x008A: 0x0001,
    0x008B: 0x000D,
    0x008C: 0x0005,
    0x008D: 0x00B1,
    0x008E: 0x0002,
    0x008F: 0x0062,
    0x0090: 0x0002,
    0x0091: 0x000A,
    0x0898: 0x01A2,
    0x186A0: 0x01FF,
    0x0020: 0x0001,
    0x00C8: 0x003E,
    0x2710: 0x0001,
    0x0320: 0x0015,
    0x1770: 0x009A,
    0x1388: 0x0034,
    0x0BB8: 0x01D3,
    0x05DC: 0x0001,
    0x03E8: 0x0002,
    0x01F4: 0x000D,
}

def print_entry(ic, fd):
    try:
        chip_id = int(ic['chip_id'], 16)
    except ValueError:
        chip_id = 0

    write_unlock = write_unlock_lookup.get(ic['opts3'], 0x00)

    print("{", file=fd)
    print('\t.name = "{}",'.format(ic['name'].strip()), file=fd)
    print('\t.protocol_id = 0x{:02X},'.format(ic['protocol_id']), file=fd)
    print('\t.variant = 0x{:02X},'.format(ic['variant']), file=fd)
    print('\t.read_buffer_size = 0x{:04X},'.format(ic['read_buffer_size']), file=fd)
    print('\t.write_buffer_size = 0x{:04X},'.format(ic['write_buffer_size']), file=fd)
    print('\t.code_memory_size = 0x{:04X},'.format(ic['code_memory_size']), file=fd)
    print('\t.data_memory_size = 0x{:04X},'.format(ic['data_memory_size']), file=fd)
    print('\t.data_memory2_size = 0x{:04X},'.format(ic['data_memory2_size']), file=fd)
    print('\t.chip_id = 0x{:04X},'.format(chip_id), file=fd)
    print('\t.chip_id_bytes_count = 0x{:02X},'.format(ic['chip_id_bytes_count']), file=fd)
    print('\t.opts1 = 0x{:04X},'.format(ic['opts1']), file=fd)
    print('\t.opts2 = 0x{:04X},'.format(ic['opts2']), file=fd)
    print('\t.opts3 = 0x{:04X},'.format(ic['opts3']), file=fd)
    print('\t.opts4 = 0x{:04X},'.format(ic['opts4']), file=fd)
    print('\t.package_details = 0x{:08X},'.format(ic['package_details']), file=fd)
    print('\t.write_unlock = 0x{:04X},'.format(write_unlock), file=fd)
    if (ic['protocol_id'], ic['variant']) in device_lookup:
        extras = device_lookup[(ic['protocol_id'], ic['variant'])]
        for key, value in extras.items():
            print('\t.{} = {},'.format(key, value), file=fd)
    print("},", file=fd)

def main():
    chips = set()
    dups = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json", help="JSON dump of InfoIC(2Plus).dll", required=True)
    parser.add_argument("--output", dest="output", help="Output filename", type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()

    with open(args.json) as f:
        json_database = json.load(f)

    print('''
/*
 * {} - Device names and characteristics.
 *
 * This file is a part of Minipro.
 *
 * Minipro is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * Minipro is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 */

/* Note, this file really isn't copyrightable. */
'''.format(args.output.name), file=args.output)
    for mf in json_database:
        for ic in mf['ics']:
            if ic['name'] in chips:
                #print("Skipping duplicate IC {}".format(ic['name']), file=sys.stderr)
                dups += 1
            else:
                chips.add(ic["name"])
                print_entry(ic, args.output);
    print("{} duplicates found".format(dups), file=sys.stderr)


if __name__ == "__main__":
    main()
