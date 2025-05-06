import argparse

MODE_J2U = 'j2u'
MODE_U2J = 'u2j'

def encode_j1939_to_uint32(priority, pdu_f, pdu_s, source):
    """
    Encodes J1939 fields into a 29-bit CAN ID as a UINT32.
    
    :param priority: J1939 priority (3 bits)
    :param pdu_f: PDU Format (8 bits)
    :param pdu_s: PDU Specific (8 bits)
    :param source: Source Address (8 bits)
    :return: 29-bit CAN ID as unsigned 32-bit integer
    """
    can_id = (priority & 0x7) << 26
    can_id |= (pdu_f & 0xFF) << 16
    can_id |= (pdu_s & 0xFF) << 8
    can_id |= (source & 0xFF)
    return can_id

def decode_uint32_to_j1939(can_id):
    """
    Decodes a 29-bit CAN ID (as UINT32) into J1939 fields.

    :param can_id: 29-bit CAN ID as unsigned 32-bit integer
    :return: Tuple containing (priority, pdu_f, pdu_s, source)
    """
    priority = (can_id >> 26) & 0x7
    pdu_f = (can_id >> 16) & 0xFF
    pdu_s = (can_id >> 8) & 0xFF
    source = can_id & 0xFF
    return priority, pdu_f, pdu_s, source

def handle_encode_mode():
    """Handles the J1939 to UINT32 encoding mode."""
    priority = int(input("Enter priority (0-7): "))
    if not 0 <= priority <= 7:
        raise ValueError("Priority must be between 0 and 7.")
    pdu_f = int(input("Enter PDU Format (0-255): "), 0) # Allow hex input
    if not 0 <= pdu_f <= 255:
        raise ValueError("PDU Format must be between 0 and 255.")
    pdu_s = int(input("Enter PDU Specific (0-255): "), 0) # Allow hex input
    if not 0 <= pdu_s <= 255:
         raise ValueError("PDU Specific must be between 0 and 255.")
    source = int(input("Enter Source Address (0-255): "), 0) # Allow hex input
    if not 0 <= source <= 255:
         raise ValueError("Source Address must be between 0 and 255.")

    can_id = encode_j1939_to_uint32(priority, pdu_f, pdu_s, source)
    print(f"\nEncoded CAN ID: 0x{can_id:08X}")

def handle_decode_mode():
    """Handles the UINT32 to J1939 decoding mode."""
    can_id_str = input("Enter CAN ID (e.g., 0x18EA00F9): ")
    can_id = int(can_id_str, 0) # Auto-detect base (hex/dec)
    if not 0 <= can_id <= 0x1FFFFFFF: # Validate 29-bit range
         raise ValueError("CAN ID must be a valid 29-bit value (0 to 0x1FFFFFFF).")

    priority, pdu_f, pdu_s, source = decode_uint32_to_j1939(can_id)
    print(f"\nDecoded J1939 Fields:")
    print(f"  Priority: {priority} (0x{priority:X})")
    print(f"  PDU Format (PF): {pdu_f} (0x{pdu_f:02X})")
    print(f"  PDU Specific (PS): {pdu_s} (0x{pdu_s:02X})")
    print(f"  Source Address (SA): {source} (0x{source:02X})")

def main():
    parser = argparse.ArgumentParser(description='Encode/Decode J1939 CAN IDs.')
    parser.add_argument('mode', choices=[MODE_J2U, MODE_U2J], help=f'Operation mode: {MODE_J2U} (J1939 to uint32) or {MODE_U2J} (uint32 to J1939)')
    args = parser.parse_args()

    try:
        if args.mode == MODE_J2U:
            handle_encode_mode()
        elif args.mode == MODE_U2J:
            handle_decode_mode()

    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
