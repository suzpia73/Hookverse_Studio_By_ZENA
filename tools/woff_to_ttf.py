import struct
import zlib
import os

def woff_to_ttf(woff_path, ttf_path):
    with open(woff_path, 'rb') as f:
        woff = f.read()

    magic, flavor, length, num_tables, _, total_sfnt_size, _, _, _, _, _, _, _ = struct.unpack('>4s4sIHHIIHHIIII', woff[:44])
    if magic != b'wOFF':
        raise ValueError("Not a WOFF file")

    # Compute SFNT header values
    entry_selector = 0
    while (1 << (entry_selector + 1)) <= num_tables:
        entry_selector += 1
    search_range = (1 << entry_selector) * 16
    range_shift = num_tables * 16 - search_range

    # Build SFNT header
    sfnt_header = struct.pack('>4sHHHH', flavor, num_tables, search_range, entry_selector, range_shift)

    # Read table directory
    woff_tables = []
    offset = 44
    for _ in range(num_tables):
        tag, tbl_offset, comp_len, orig_len, checksum = struct.unpack('>4sIIII', woff[offset:offset+20])
        woff_tables.append((tag, tbl_offset, comp_len, orig_len, checksum))
        offset += 20

    # Decompress tables
    ttf_tables = []
    table_data_offset = 12 + 16 * num_tables

    decompressed_data = bytearray()
    for tag, tbl_offset, comp_len, orig_len, checksum in woff_tables:
        data = woff[tbl_offset:tbl_offset+comp_len]
        if comp_len != orig_len:
            data = zlib.decompress(data)
        
        # Pad to 4 bytes
        pad = (4 - (len(data) % 4)) % 4
        padded_data = data + b'\x00' * pad
        
        current_offset = table_data_offset + len(decompressed_data)
        ttf_tables.append((tag, checksum, current_offset, orig_len))
        decompressed_data.extend(padded_data)

    # Build TTF table directory
    ttf_table_dir = bytearray()
    for tag, checksum, current_offset, orig_len in ttf_tables:
        ttf_table_dir.extend(struct.pack('>4sIII', tag, checksum, current_offset, orig_len))

    # Write complete TTF
    with open(ttf_path, 'wb') as f:
        f.write(sfnt_header)
        f.write(ttf_table_dir)
        f.write(decompressed_data)

    print(f"[+] Successfully converted {woff_path} to {ttf_path}!")
    print(f"    - Output size: {os.path.getsize(ttf_path)} bytes")

woff_to_ttf("assets/fonts/KyoboHand.woff", "assets/fonts/KyoboHandwriting2019.ttf")
