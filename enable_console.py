import sys
import struct

def enable_console(exe_path):
    try:
        with open(exe_path, 'r+b') as f:
            f.seek(0x3C)
            pe_offset = struct.unpack('<I', f.read(4))[0]
            
            # PE Signature (4 bytes) + File Header (20 bytes) = 24 bytes
            opt_header_offset = pe_offset + 24
            
            subsystem_offset = opt_header_offset + 68
            f.seek(subsystem_offset)
            current_subsystem = struct.unpack('<H', f.read(2))[0]
            
            print(f"Current Subsystem: {current_subsystem} (2=GUI, 3=Console)")
            
            if current_subsystem == 2:
                print("Patching to CONSOLE mode (3)...")
                f.seek(subsystem_offset)
                f.write(struct.pack('<H', 3))
                print("Done! The EXE will now open with a black console window.")
            elif current_subsystem == 3:
                print("File is already in Console mode.")
            else:
                print("Unknown subsystem type. Aborting to be safe.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        enable_console(sys.argv[1])
    else:
        print("Usage: python enable_console.py <path_to_exe>")