# lsi_decode_loginfo

A Python tool to decode LSI Logic (Broadcom) storage controller LogInfo codes, making troubleshooting storage issues significantly easier.

This tool parses the cryptic 32-bit LogInfo integers found in kernel logs (e.g., mpt3sas, megaraid_sas) and breaks them down into their hierarchical components: Type, Origin, Code, and specific Sub-Codes.

## Features

*   **Recursive Parsing**: Automatically traverses the multi-level structure of LogInfo codes (Type -> Origin -> Code -> SubCode).
*   **Fuzzy Matching**: Includes logic to identify the closest parent code definition if a specific sub-code is not defined in the dictionary.
*   **Comprehensive Definitions**: Includes definitions for IOP, PL (Protocol Layer), IR (Integrated RAID), and FC (Fibre Channel) codes.

## Usage

Run the script providing the LogInfo code as a hexadecimal argument:

```bash
./lsi_decode_loginfo.py 0x31170000
```

Or use the help flag for more info:

```bash
./lsi_decode_loginfo.py -h
```

### Helper Script

Included is `list_all_codes.py`, which iterates through all defined codes in the library and prints them out. This is useful for generating documentation or searching for a specific string.

```bash
./list_all_codes.py
```

## Sample Output

**Input:**
```bash
./lsi_decode_loginfo.py 0x31170000
```

**Output:**
```text
Value     	31170000h
Type:     	30000000h	SAS 
Origin:   	01000000h	PL 
Code:     	00170000h	PL_LOGINFO_CODE_IO_DEVICE_MISSING_DELAY_RETRY Missing Device Delay Retry
```

## Background

This tool is based on open sources, mostly Linux kernel header files. While official LSI documentation detailing every code exists, it is not publicly available. This tool bridges that gap for sysadmins and storage engineers.

If the tool fails to parse a specific LogInfo code, and you have access to LSI/Broadcom support, please ask them for the decoding. If you share that information, it can be added to this tool to benefit the community.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Author

*   **Eric Deng** (dengxin@gmail.com)
