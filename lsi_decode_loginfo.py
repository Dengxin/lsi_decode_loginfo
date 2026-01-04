#!/usr/bin/env python

from __future__ import print_function
import sys

def decode_lsi_loginfo_numbers(val):
    """While this is the official breakdown it's not quite that normal for some codes"""
    t = (val >> 28) & 0xF
    origin = (val >> 24) & 0xF
    code = (val >> 16) & 0xFF
    spec = val & 0xFFFF
    return (t, origin, code, spec)

# ==============================================================================
# IOP (I/O Processor) Sub-Codes
# ==============================================================================

iop_config_page = ["Sub Code", 0x0000FFFF, {
    0x00000000: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE", None, "Invalid config page"),
    0x00000100: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_RT", None, "Route Table Entry not found"),
    0x00000200: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_PN", None, "Invalid Page Number"),
    0x00000300: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_FORM", None, "Invalid FORM"),
    0x00000700: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_DEFAULT", None, "Default Page not found"),
    0x00000800: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_STATE", None, "FW Downgrade active, cannot access persistent pages"),
}]

iop_boot = ["Sub Code", 0x0000FFFF, {
    0x00000000: ("IOP_LOGINFO_CODE_INVALID_SAS_ADDRESS", None, "Invalid SAS Address"),
    0x00000101: ("IOP_LOGINFO_CODE_FLASH_NOT_PRESENT", None, "Flash not present"),
    0x00000102: ("IOP_LOGINFO_CODE_FLASH_ERASE_FAILED", None, "Flash erase failed"),
    0x00000103: ("IOP_LOGINFO_CODE_FLASH_WRITE_FAILED", None, "Bad image header"),
    0x00000104: ("IOP_LOGINFO_CODE_FLASH_WRITE_FAILED_4", None, "Bad image write"),
    0x00000105: ("IOP_LOGINFO_CODE_FLASH_WRITE_FAILED_5", None, "MegaRAID Header"),
    0x00000106: ("IOP_LOGINFO_CODE_FLASH_WRITE_FAILED_6", None, "Common Boot Block"),
    0x00000401: ("IOP_LOGINFO_CODE_IMAGE_BOOTLOADER_NOT_PRESENT", None, ""),
    0x00000402: ("IOP_LOGINFO_CODE_IMAGE_MAIN_CHECKSUM_FAILURE", None, ""),
    0x00000403: ("IOP_LOGINFO_CODE_IMAGE_EXT_CHECKSUM_FAILURE", None, ""),
    0x00000404: ("IOP_LOGINFO_CODE_IMAGE_INIT_NOT_PRESENT", None, ""),
    0x00000405: ("IOP_LOGINFO_CODE_IMAGE_INIT_ADDRESS_ERROR", None, ""),
    0x00000406: ("IOP_LOGINFO_CODE_IMAGE_NOT_MODEL_TO_FWDL", None, "Tried FW download when code running from flash"),
    0x00000407: ("IOP_LOGINFO_CODE_IMAGE_FLASH_SIZE_NOT_MATCH", None, ""),
    0x00000408: ("IOP_LOGINFO_CODE_IMAGE_ENCRYPT_HASH_NOT_PRESENT", None, ""),
    0x00000409: ("IOP_LOGINFO_CODE_IMAGE_ENCRYPT_HASH_INVALID", None, ""),
    0x00000410: ("IOP_LOGINFO_CODE_IMAGE_NVDATA_CHECK_FAILED", None, "DevID, Rev, or other mismatch"),
    0x00000411: ("IOP_LOGINFO_CODE_IMAGE_SBR_CHECK_FAILED", None, "DevID, Checksum, or other mismatch"),
    0x00000412: ("IOP_LOGINFO_CODE_IMAGE_REQUIRES_POR", None, "Download requires Power On Reset"),
    0x00000414: ("IOP_LOGINFO_CODE_IMAGE_SUPDEV_CHECK_FAILED", None, "Supported Devices check failed"),
    0x00000416: ("IOP_LOGINFO_CODE_IMAGE_FW_SIGNATURE_FAILED", None, "Incorrect signature"),
    0x00000422: ("IOP_LOGINFO_CODE_IMAGE_CBB_UNSIGNED", None, "FW Download CBB unsigned"),
    0x00000423: ("IOP_LOGINFO_CODE_IMAGE_APP_UNSIGNED", None, "FW Download APP unsigned"),
    0x00000424: ("IOP_LOGINFO_CODE_IMAGE_INVALID_BIOS", None, "FW Download BIOS format invalid"),
    0x00000600: ("IOP_LOGINFO_CODE_PORT_ENABLE_RESOURCES_INSUF", None, "Insufficient resources for backend PCIe"),
    0x00000601: ("IOP_LOGINFO_CODE_PORT_ENABLE_PDB_PLL_NOT_LOCKED", None, "PDB PLL not locked"),
    0x00000602: ("IOP_LOGINFO_CODE_PORT_ENABLE_PDB_LNK_CFG_INVALID", None, "Backend PCIe link config invalid"),
    0x00000620: ("IOP_LOGINFO_CODE_IOCINIT_HOST_PAGE_SIZE_INVALID", None, "Host page size not supported"),
}]

iop_raid_accel = ["Sub Code", 0x0000FFFF, {
    0x00000001: ("IOP_LOGINFO_SUBCODE_RACC_COMPLETE_W_ERROR", None, "IO completed with error"),
    0x00000002: ("IOP_LOGINFO_SUBCODE_RACC_FAIL_REQUEST", None, "Request failed"),
    0x00000004: ("IOP_LOGINFO_SUBCODE_RACC_EEDP_GUARD_ERROR", None, "Guard Miscompare Halt"),
    0x00000008: ("IOP_LOGINFO_SUBCODE_RACC_EEDP_REF_TAG_ERROR", None, "Ref Tag Miscompare Halt"),
    0x00000010: ("IOP_LOGINFO_SUBCODE_RACC_EEDP_APP_TAG_ERROR", None, "App Tag Miscompare Halt"),
    0x00000100: ("IOP_LOGINFO_SUBCODE_RACC_DMA_0_COMP_Q_FULL", None, ""),
    0x00000400: ("IOP_LOGINFO_SUBCODE_RACC_DMA_0_HALT_ERROR", None, ""),
}]

iop_code = ["Code", 0x00FF0000, {
    0x00010000: ("IOP_LOGINFO_CODE_BOOT", iop_boot, ""),
    0x00030000: ("IOP_LOGINFO_CODE_CONFIG", iop_config_page, ""),
    0x00040000: ("IOP_LOGINFO_CODE_DIAG_MSG_ERROR", None, "Error handling diag msg - or'd with diag status"),
    0x00050000: ("IOP_LOGINFO_CODE_TASK_TERMINATED", None, "SCSI I/O task terminated"),
    0x00060000: ("IOP_LOGINFO_CODE_ENCL_MGMT", None, "Enclosure Management Error"),
    0x00070000: ("IOP_LOGINFO_CODE_SCSI_IO_NOT_REGISTERED", None, "Unregistered/Blocked SCSI I/O device"),
    0x00090000: ("IOP_LOGINFO_CODE_ISTWI", None, "ISTWI Bus Error (Reserved/Not Present)"),
    0x000A0000: ("IOP_LOGINFO_CODE_PWR_MGMT", None, "Power Management Status"),
    0x000B0000: ("IOP_LOGINFO_CODE_RACC_ERROR", iop_raid_accel, "RAID Accelerator Error"),
}]

# ==============================================================================
# PL (Protocol Layer) Sub-Codes
# ==============================================================================

pl_generic_sub = ["Sub Code", 0x0000FFFF, {
    # 6.7 Open Failure Sub Codes
    0x00000100: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE", None, "Open Failure"),
    0x00000101: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_NO_DEST_TIMEOUT", None, "Open Reject (No Dest)"),
    0x00000102: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_PATHWAY_BLOCKED", None, "Open Reject (Pathway Blocked)"),
    0x00000103: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_RSVD_CONT0", None, ""),
    0x00000109: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ORR", None, "Open Reject (Retry)"),
    0x0000010A: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_BREAK", None, "Break Received"),
    0x0000010C: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_TIMEOUT", None, "Open Timeout"),
    0x00000111: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_BAD_DEST", None, "Open Reject (Bad Dest)"),
    0x00000112: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_RATE_NOT_SUPPORTED", None, "Open Reject (Rate Not Supported)"),
    0x00000113: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_PROTOCOL_NOT_SUPPORTED", None, "Open Reject (Protocol Not Supported)"),
    0x00000114: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ZONE_VIOLATION", None, "Open Reject (Zone Violation)"),
    0x00000118: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_STP_RESOURCES_BSY", None, "Open Reject (STP Resources Busy)"),
    0x00000119: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_WRONG_DEST", None, "Open Reject (Wrong Dest)"),
    0x0000011A: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ORR_TIMEOUT", None, "Open Reject (Retry) Timeout"),
    0x0000011C: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_AWT_MAXED", None, "Arbitration Wait Timer Maxed"),
    0x00000120: ("PL_LOGINFO_SUB_CODE_TARGET_BUS_RESET", None, "Received HARD_RESET primitive in Target Mode"),
    
    # 6.8 Tx Transport Layer Errors
    0x00000300: ("PL_LOGINFO_SUB_CODE_TX_TRANSPORT_LAYER", None, ""),
    0x00000301: ("PL_LOGINFO_SUB_CODE_TX_CONNECTED", None, "TxCtx Connected"),
    0x00000303: ("PL_LOGINFO_SUB_CODE_TX_NAK", None, "TxCtx NAK"),
    0x00000304: ("PL_LOGINFO_SUB_CODE_TX_SMP_BACKOFF", None, "TxCtx SMP Backoff"),
    0x00000306: ("PL_LOGINFO_SUB_CODE_TX_BACK_OFF", None, "TxCtx Backoff"),
    0x0000030A: ("PL_LOGINFO_SUB_CODE_TX_EEDP", None, "TxCtx EEDP Error"),
    0x00000310: ("PL_LOGINFO_SUB_CODE_TX_DISCONNECTION", None, "TxFM Disconnected"),
    0x00000311: ("PL_LOGINFO_SUB_CODE_TX_NAK_RCVD", None, "TxFM NAK Received"),
    0x00000320: ("PL_LOGINFO_SUB_CODE_TX_BAD_SGE", None, "TxDMA Bad SGE Fetch"),
    0x00000321: ("PL_LOGINFO_SUB_CODE_TX_FETCH_ERROR", None, "TxDMA Fetch Error"),
    0x00000324: ("PL_LOGINFO_SUB_CODE_TX_DATO", None, "DMA Activate Timeout"),

    # 6.9 Rx Transport Layer Errors
    0x00000430: ("PL_LOGINFO_SUB_CODE_RX_TRANSPORT_LAYER", None, ""),
    0x00000431: ("PL_LOGINFO_SUB_CODE_RX_WRONG_REL_OFFSET", None, "Data offset error"),
    0x00000432: ("PL_LOGINFO_SUB_CODE_RX_FRAME_LENGTH", None, "Frame length mismatch"),
    0x00000433: ("PL_LOGINFO_SUB_CODE_RX_ZERO_WDL", None, "Zero WDL in Xfer Rdy"),
    0x00000434: ("PL_LOGINFO_SUB_CODE_RX_OVERRUN", None, "Overrun"),
    0x00000435: ("PL_LOGINFO_SUB_CODE_RX_CDP_FRAME", None, "CDP Frame Received"),
    0x00000439: ("PL_LOGINFO_SUB_CODE_RETRANSMIT_XFER_RDY", None, "Retransmit bit set in Xfer Rdy"),
    0x0000043B: ("PL_LOGINFO_SUB_CODE_RX_EEDP", None, "EEDP Error"),
    0x0000043C: ("PL_LOGINFO_SUB_CODE_RX_EEDP_RESET", None, "EEDP Reset"),
    0x0000043D: ("PL_LOGINFO_SUB_CODE_RX_BAD_SGE", None, "Bad SGE Fetch"),
    0x0000043E: ("PL_LOGINFO_SUB_CODE_RX_FETCH_ERROR", None, "Fetch Error"),
    0x00000440: ("PL_LOGINFO_SUB_CODE_RX_WRONG_DATA_XFER", None, "Wrong Data Transfer"),
    0x00000442: ("PL_LOGINFO_SUB_CODE_RX_DMA_OVERFLOW", None, "RxDMA Overflow"),
    0x00000443: ("PL_LOGINFO_SUB_CODE_RX_DMA_PARITY_ERROR", None, "RxDMA Parity Error"),

    # Discovery & SATA
    0x00000500: ("PL_LOGINFO_SUB_CODE_INTERNAL_IO_TIMED_OUT", None, "Internal SCSI IO Timed Out"),
    0x00000610: ("PL_LOGINFO_SUB_CODE_SATA_READ_LOG_RECEIVE_DATA_ERR", None, "ReadLogExt Data Error"),
    0x00000630: ("PL_LOGINFO_SUB_CODE_SATA_ERR_IN_RCV_SET_DEV_BIT_FIS", None, "Error in Set Device Bits FIS"),
    0x00000635: ("PL_LOGINFO_SUB_CODE_SATA_INIT_RETRIES_EXCEEDED", None, "SATA Init Retries Exceeded"),
    0x00000B10: ("PL_LOGINFO_SUB_CODE_RX_FM_CURRENT_FRAME_ERROR", None, "Rx Frame Manager Current Frame Error"),
    0x00000B41: ("PL_LOGINFO_SUB_CODE_RX_FM_INVALID_TAG_DMA_SETUP_FIS", None, "FPDMA FIS Invalid Tag"),
    0x00000B50: ("PL_LOGINFO_SUB_CODE_RX_FM_NCQ_DISABLED", None, "NCQ Disabled"),
    0x00000D00: ("PL_LOGINFO_SUB_CODE_SATA_LINK_DOWN", None, "SATA Direct-Attach Link Down"),
    0x00000D01: ("PL_LOGINFO_SUB_CODE_ABORT_SATA_RX_STAT", None, "SATA Rx Transfer Aborted"),
    0x00000D02: ("PL_LOGINFO_SUB_CODE_SATA_UNEXPECTED_FRAME", None, "Received unexpected SATA FIS"),
    0x00000E00: ("PL_LOGINFO_SUB_CODE_DISCOVERY_SATA_INIT_W_IOS", None, "SATA Init started with outstanding IOs"),
    0x00000E01: ("PL_LOGINFO_SUB_CODE_DISCOVERY_REMOTE_SEP_RESET", None, "Remote SEP requires reset"),
    0x00000E02: ("PL_LOGINFO_SUB_CODE_RCVD_UNCONFIRMED_RESP_FRAME", None, "Received unconfirmed Response Frame"),
    0x00000E03: ("PL_LOGINFO_SUB_CODE_DISCOVERY_SATA_INIT_NEEDED_W_IOS", None, "SATA Init needed with outstanding IOs"),
    0x00000E04: ("PL_LOGINFO_SUB_CODE_PCIE_DEV_INIT_NEEDED_W_IOS", None, "PCIe Device Init started with outstanding IOs"),
    0x00000E05: ("PL_LOGINFO_SUB_CODE_RESET_RETURNED_MISSING_DEV", None, "Reset previously missing drives"),
    0x00000E80: ("PL_LOGINFO_SUB_CODE_INVALID_TM_NOT_END_DEVICE", None, "TM sent to device that is not End Device"),
    0x00000F00: ("PL_LOGINFO_SUB_CODE_LINK_HUNG", None, "TM sent to device connected to stuck link"),
    0x00001000: ("PL_LOGINFO_SUB_CODE_DSCVRY_SATA_INIT_TIMEOUT", None, "SATA Init timed out on drive"),
    0x00001010: ("PL_LOGINFO_SUB_CODE_PCIE_ERR_FATAL_MALFORMED_TLP_RECIEVED", None, "PCIe Fatal: Malformed TLP"),
    0x00001012: ("PL_LOGINFO_SUB_CODE_PCIE_ERR_FATAL_COMPLETION_TIMEOUT_ERROR", None, "PCIe Fatal: Completion Timeout"),
    0x00001013: ("PL_LOGINFO_SUB_CODE_PCIE_ERR_FATAL_FLOW_CONTROL_PROT_ERROR", None, "PCIe Fatal: Flow Control Protocol Error"),
    0x00001014: ("PL_LOGINFO_SUB_CODE_PCIE_ERR_FATAL_DATA_LINK_PROT_ERROR", None, "PCIe Fatal: Data Link Protocol Error"),
    0x00001015: ("PL_LOGINFO_SUB_CODE_PCIE_ERR_FATAL_SURPRISE_DOWN_ERROR", None, "PCIe Fatal: Surprise Down"),
    0x00001019: ("PL_LOGINFO_SUB_CODE_PCIE_ERR_NFATAL_ECRC_ERROR", None, "PCIe Non-Fatal: ECRC Error"),
    0x0000101C: ("PL_LOGINFO_SUB_CODE_PCIE_ERR_NFATAL_POISONED_TLP_ERROR", None, "PCIe Non-Fatal: Poisoned TLP"),
    0x0000101F: ("PL_LOGINFO_SUB_CODE_PCI_ERROR_AER_FATAL", None, "PCIe Root Port detected FATAL error"),
    0x00001020: ("PL_LOGINFO_SUB_CODE_PCI_ERROR_AER_NON_FATAL", None, "PCIe Root Port detected NON-FATAL error"),
}]

pl_config_err = ["Sub Code", 0x0000FFFF, {
    0x00000000: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE", None, ""),
    0x00000001: ("PL_LOGINFO_CODE_CONFIG_PL_NOT_INITIALIZED", None, "PL not initialized"),
    0x00000002: ("PL_LOGINFO_CODE_CONFIG_BACKEND_PCIE_SUPPORT_DISABLED", None, "Backend PCIe disabled"),
    0x00000003: ("PL_LOGINFO_CODE_CONFIG_SWITCH_INFO_ACCESS_FAILED", None, "Failed to get backend PCIe switch info"),
    0x00000100: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_PT", None, "Invalid Page Type"),
    0x00000200: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_NUM_PHYS", None, "Invalid Number of Phys"),
    0x00000300: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_NOT_IMP", None, "Page Not Handled"),
    0x00000400: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_NO_DEV", None, "No Device Found"),
    0x00000500: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_FORM", None, "Invalid FORM"),
    0x00000600: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_PHY", None, "Invalid Phy"),
    0x00000700: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_NO_OWNER", None, "No Owner Found"),
    0x00000800: ("PL_LOGINFO_CODE_CONFIG_INVALID_PAGE_LINK", None, "Invalid Link Number"),
}]

pl_smp_sub = ["Sub Code", 0x0000FFFF, {
    0x0000000A: ("PL_LOGINFO_CODE_SMP_FAILED_ABORT", None, "Expander Missing"),
    0x0000000D: ("PL_LOGINFO_CODE_SMP_FAILED_XFER_ERROR", None, "Tx Frame Manager Xfer Error"),
    0x0000000E: ("PL_LOGINFO_CODE_SMP_FAILED_TIMEOUT", None, "Timeout"),
    0x00000014: ("PL_LOGINFO_CODE_SMP_FAILED_DMA_ERROR", None, "Tx DMA Error"),
    0x00000020: ("PL_LOGINFO_CODE_SMP_FAILED_HW_TIMEOUT", None, "Link Timeout"),
    0x00000021: ("PL_LOGINFO_CODE_SMP_FAILED_LINK_ERROR", None, "Link Error"),
    0x00000030: ("PL_LOGINFO_CODE_SMP_FAILED_BACK_OFF", None, "Transceiver Backoff"),
    0x00000031: ("PL_LOGINFO_CODE_SMP_FAILED_NO_CONNECTION", None, "No Connection"),
    0x00000100: ("PL_LOGINFO_CODE_SMP_FAILED_OPEN_FAIL", None, "Open Fail"),
}]

pl_pcie_sub = ["Sub Code", 0x0000FFFF, {
    # 6.11 General PCIe Errors & 6.10 PCIe Device Sub Codes
    0x00000000: ("PL_LOGINFO_CODE_PCI_BAD_SGL_ERROR", None, "Generic PCIe Bad SGL"),
    0x00000007: ("PL_LOGINFO_CODE_PCI_BAD_SGLOFFSET", None, "Bad SGL Offset in request"),
    0x00000008: ("PL_LOGINFO_CODE_FXENGINE_BAD_DLAS_PLBNTA", None, "DLAS contains PLB-NTA (Not Allowed)"),
    0x0000000B: ("PL_LOGINFO_CODE_FXENGINE_DATALEN_GT_SGLLEN", None, "DataLength > SGL Length"),
    0x0000000C: ("PL_LOGINFO_CODE_NVME_FXREQUESTOR_ERROR", None, "NVMe FxRequestor Error"),
    0x0000000D: ("PL_LOGINFO_CODE_NVME_FXCOMPLETOR_ERROR", None, "NVMe FxCompletor Error"),
    0x0000000E: ("PL_LOGINFO_CODE_PCI_REQUEST_ERROR", None, "PCIe Device Request Error"),
    0x0000000F: ("PL_LOGINFO_CODE_PCI_COMPLETE_ERROR", None, "PCIe Device Complete Error"),
    0x00000011: ("PL_LOGINFO_CODE_PCI_SGE_DMA_FAILED", None, "Failed to DMA SGE"),
    0x00000013: ("PL_LOGINFO_CODE_PCI_SGE_INVALID_BYTE_COUNT", None, "Invalid Byte Count"),
    0x00000016: ("PL_LOGINFO_CODE_PCI_FXCORE_BAD_DEVHANDLE", None, "Invalid DevHandle for backend PCIe device"),
    0x0000001B: ("PL_LOGINFO_CODE_PCI_DEVHANDLE_MISMATCH_COMPLETION", None, "DevHandle Mismatch"),
    0x00000100: ("PL_LOGINFO_CODE_PCI_CONFIG_MODIFIED_LINK_PHY_MAPPING", None, "Link-Phy mapping modified"),
    0x00000200: ("PL_LOGINFO_CODE_NVME_ENCAP_MDTS_VIOLATION", None, "Data len > MDTS"),
    0x00000201: ("PL_LOGINFO_CODE_NVME_ENCAP_BAD_CMD_LENGTH", None, "Encap command length invalid"),
    0x00000202: ("PL_LOGINFO_CODE_NVME_ENCAP_DEV_INIT_FAILED", None, "Device not successfully initialized"),
    0x00000203: ("PL_LOGINFO_CODE_NVME_ENCAP_NO_IO_QUEUES", None, "Device has no IO queues"),
    0x000002C0: ("PL_LOGINFO_CODE_NVME_DRV_RECOVERY_INVALID_COMMAND", None, "Invalid Recovery Command"),
    0x00000400: ("PL_LOGINFO_CODE_NVME_SGE_NOT_DWORD_ALIGNED", None, "SGE Address not DWord aligned"),
    0x00000404: ("PL_LOGINFO_CODE_NVME_SKIPCOUNT_EXCEEDS_SGL_LENGTH", None, "SkipCount > Total SGL Length"),
    0x00000405: ("PL_LOGINFO_CODE_NVME_ILLEGAL_SGE_WITHIN_DEVSECTOR", None, "Unaligned SGE boundary"),
    0x00000800: ("PL_LOGINFO_SUB_CODE_NVME_ASYNC_PERSISTENT_ERROR", None, "Async Persistent Error"),
    0x00000801: ("PL_LOGINFO_SUB_CODE_NVME_INIT_TIMEOUT_OR_FAILURE", None, "NVMe Init Failed/Timeout"),
    0x00000803: ("PL_LOGINFO_SUB_CODE_NVME_IOERROR_BAD_SQID", None, "Bad SQID on IO Completion"),
    0x00000804: ("PL_LOGINFO_SUB_CODE_NVME_IOERROR_BAD_CID", None, "Bad CID on IO Completion"),
    0x0000080B: ("PL_LOGINFO_SUB_CODE_NVME_ASYNC_EVENT_TIMEOUT", None, "Async Event Timeout"),
    0x00000812: ("PL_LOGINFO_SUB_CODE_FXCORE_REQUESTOR_ACCESS_ERROR", None, "FxCore Access Error"),
    0x00000813: ("PL_LOGINFO_SUB_CODE_NVME_ADMIN_COMPQ_HEAD_WRITE_FAILED", None, "Admin CompQ Head Write Failed"),
}]

pl_fastpath_sub = ["Sub Code", 0x0000FFFF, {
    0x00000001: ("PL_LOGINFO_FAST_PATH_ENGINE_IOEXCP_INVALID_DESCR_TYPE", None, "Invalid Descriptor Type"),
    0x00000002: ("PL_LOGINFO_FAST_PATH_ENGINE_IOEXCP_INVALID_DEVICE_HANDLE", None, "Invalid Device Handle"),
    0x00000003: ("PL_LOGINFO_FAST_PATH_ENGINE_IOEXCP_VF_MISMATCH", None, "VF Mismatch"),
    0x00000004: ("PL_LOGINFO_FAST_PATH_ENGINE_REQUESTOR_TIMER_OVERFLOW_ERROR", None, "Requestor Timer Overflow"),
    0x00000005: ("PL_LOGINFO_FAST_PATH_ENGINE_COMPLETOR_TIMER_OVERFLOW_ERROR", None, "Completor Timer Overflow"),
}]

pl_encl_mgmt_err = ["Sub Code", 0x0000FFFF, {
    0x00000000: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_FRAME_FAILURE", None, "Can't get SMP Frame"),
    0x00000010: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_READ_ERROR", None, "Error occurred on SMP Read"),
    0x00000020: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_WRITE_ERROR", None, "Error occurred on SMP Write"),
    0x00000040: ("PL_LOGINFO_CODE_ENCL_MGMT_NOT_SUPPORTED_ON_ENCL", None, "Encl Mgmt services not available for this WWID"),
    0x00000060: ("PL_LOGINFO_CODE_ENCL_MGMT_BAD_SLOT_NUM", None, "Invalid Slot Number in SEP Msg"),
    0x00000070: ("PL_LOGINFO_CODE_ENCL_MGMT_SGPIO_NOT_PRESENT", None, "SGPIO not present/enabled"),
    0x00000080: ("PL_LOGINFO_CODE_ENCL_MGMT_GPIO_NOT_CONFIGURED", None, "GPIO not configured"),
    0x000000B0: ("PL_LOGINFO_CODE_ENCL_MGMT_SES_FRAME_ALLOC_ERROR", None, "Can't get frame for SES command"),
    0x000000C0: ("PL_LOGINFO_CODE_ENCL_MGMT_SES_IO_ERROR", None, "I/O execution error"),
    0x000000D0: ("PL_LOGINFO_CODE_ENCL_MGMT_SES_RETRIES_EXHAUSTED", None, "SEP I/O retries exhausted"),
    0x00000100: ("PL_LOGINFO_DA_SEP_NOT_PRESENT", None, "SEP not present when msg received"),
    0x00000101: ("PL_LOGINFO_DA_SEP_SINGLE_THREAD_ERROR", None, "Can only accept 1 msg at a time"),
    0x00000104: ("PL_LOGINFO_DA_SEP_DID_NOT_RECEIVE_ACK", None, "SEP didn't rcv ACK"),
    0x00000105: ("PL_LOGINFO_DA_SEP_BAD_STATUS_HDR_CHKSUM", None, "SEP stopped or sent bad chksum in Hdr"),
    0x0000010C: ("PL_LOGINFO_DA_SEP_UNSUPPORTED_COMMAND", None, "SEP doesn't support CDB opcode"),
}]

pl_code = ["Code", 0x00FF0000, {
    0x00010000: ("PL_LOGINFO_CODE_OPEN_FAILURE", pl_generic_sub, "Open Failure"),
    0x00020000: ("PL_LOGINFO_CODE_INVALID_SGL", None, ""),
    0x00030000: ("PL_LOGINFO_CODE_WRONG_REL_OFF_OR_FRAME_LENGTH", None, ""),
    0x00040000: ("PL_LOGINFO_CODE_FRAME_XFER_ERROR", None, ""),
    0x00050000: ("PL_LOGINFO_CODE_TX_FM_CONNECTED_LOW", None, ""),
    0x00060000: ("PL_LOGINFO_CODE_SATA_NON_NCQ_RW_ERR_BIT_SET", None, ""),
    0x00070000: ("PL_LOGINFO_CODE_SCSI_IO_NOT_REGISTERED", None, "SCSI IO to unregistered device"),
    0x00080000: ("PL_LOGINFO_CODE_SATA_NCQ_FAIL_ALL_CMDS_AFTR_ERR", None, ""),
    0x00090000: ("PL_LOGINFO_CODE_SATA_ERR_IN_RCV_SET_DEV_BIT_FIS", None, ""),
    0x000A0000: ("PL_LOGINFO_CODE_RX_FM_INVALID_MESSAGE", None, ""),
    0x000B0000: ("PL_LOGINFO_CODE_RX_CTX_MESSAGE_VALID_ERROR", None, ""),
    0x000C0000: ("PL_LOGINFO_CODE_RX_FM_CURRENT_FRAME_ERROR", None, ""),
    0x000D0000: ("PL_LOGINFO_CODE_SATA_LINK_DOWN", None, ""),
    0x000E0000: ("PL_LOGINFO_CODE_DISCOVERY_SATA_INIT_W_IOS", None, ""),
    0x000F0000: ("PL_LOGINFO_CODE_CONFIG_ERROR", pl_config_err, ""),
    0x00100000: ("PL_LOGINFO_CODE_DSCVRY_SATA_INIT_TIMEOUT", None, ""),
    0x00110000: ("PL_LOGINFO_CODE_RESET", pl_generic_sub, "Reset occurred"),
    0x00120000: ("PL_LOGINFO_CODE_ABORT", pl_generic_sub, "Task Abort"),
    0x00130000: ("PL_LOGINFO_CODE_IO_NOT_YET_EXECUTED", None, "Aborted IO not yet submitted to HW"),
    0x00140000: ("PL_LOGINFO_CODE_IO_EXECUTED", None, "Aborted IO submitted to HW"),
    0x00150000: ("PL_LOGINFO_CODE_PERS_RESV_OUT_NOT_AFFIL_OWNER", None, "Affiliation Conflict"),
    0x00160000: ("PL_LOGINFO_CODE_NOT_AFFIL_OWNER", None, "Affiliation Conflict"),
    0x00170000: ("PL_LOGINFO_CODE_IO_DEVICE_MISSING_DELAY_RETRY", None, "Missing Device Delay Retry"),
    0x00180000: ("PL_LOGINFO_CODE_TARGET_MODE_ERROR", None, "Target Mode Error"),
    0x00190000: ("PL_LOGINFO_CODE_SENSE_DATA_LENGTH_ZERO", None, "SSP sense len is 0"),
    0x001B0000: ("PL_LOGINFO_CODE_TM_INVALID_REQUEST", None, "Invalid Task Mgmt Request"),
    0x001C0000: ("PL_LOGINFO_CODE_SMP_FAILED", pl_smp_sub, "SMP Failed"),
    0x00200000: ("PL_LOGINFO_CODE_ENCL_MGMT_ERR", pl_encl_mgmt_err, "Enclosure Management"),
    0x00220000: ("PL_LOGINFO_CODE_IO_REDUCED_FUNCTIONALITY_RETRY", None, ""),
    0x00230000: ("PL_LOGINFO_CODE_HOST_BASED_DISCOVERY", None, "Host Based Discovery Error"),
    0x00240000: ("PL_LOGINFO_FAST_PATH_ENGINE", pl_fastpath_sub, "FastPath Engine Error"),
    0x00260000: ("PL_LOGINFO_CODE_PCIE_ERROR", pl_pcie_sub, "PCIe/NVMe Error"),
    0x00270000: ("PL_LOGINFO_CODE_SATL", None, "SCSI-ATA Translation Error"),
    0x00340000: ("PL_LOGINFO_CODE_POWER_MANAGEMENT", None, "Power Management Error"),
}]

ir_code = ["Code", 0x00FFFFFF, {
    0x00010000: ("IR_LOGINFO_RAID_ACTION_ERROR", None, ""),
    0x00010001: ("IR_LOGINFO_VOLUME_CREATE_INVALID_LENGTH", None, ""),
    0x00010002: ("IR_LOGINFO_VOLUME_CREATE_DUPLICATE", None, ""),
    0x00010003: ("IR_LOGINFO_VOLUME_CREATE_NO_SLOTS", None, ""),
    0x00010004: ("IR_LOGINFO_VOLUME_CREATE_DMA_ERROR", None, ""),
    0x00010005: ("IR_LOGINFO_VOLUME_CREATE_INVALID_VOLUME_TYPE", None, ""),
    0x0001003A: ("IR_LOGINFO_COMPAT_ERROR_PHYS_DISK_NOT_FOUND", None, ""),
    0x0001003B: ("IR_LOGINFO_COMPAT_ERROR_MEMBERSHIP_COUNT", None, ""),
    0x0001003C: ("IR_LOGINFO_COMPAT_ERROR_NON_64K_STRIPE_SIZE", None, ""),
    0x0001003D: ("IR_LOGINFO_COMPAT_ERROR_IME_VOL_NOT_CURRENTLY_SUPPORTED", None, ""),
}]

type_sas = ["Origin", 0x0F000000, {
    0x00000000: ('IOP', iop_code, ""),
    0x01000000: ('PL', pl_code, ""),
    0x02000000: ('IR', ir_code, ""),
}]

# FC structures kept as original placeholders if used by other tools
fc_initiator = ["Code", 0x00FFFFFF, {
    0x0000000A: ('ERROR_LINK_FAILURE', None, 'Link failure occurred '),
}]

type_fc = ["Origin", 0x0F000000, {
    0x00000000: ('FCP Initiator', fc_initiator, ''),
}]

types = ["Type", 0xF0000000, {
    0x00000000: ('NONE', None, ""),
    0x10000000: ('SCSI', None, ""),
    0x20000000: ('FC', type_fc, ""),
    0x30000000: ('SAS', type_sas, ""),
    0x40000000: ('iSCSI', None, ""),
}]

def _decode_lsi_loginfo(d, val, unparsed):
    if d is None:
        return unparsed

    name = d[0]
    mask = d[1]
    vals = d[2]

    masked_val = mask & val
    unparsed = unparsed & ~mask

    info = vals.get(masked_val, None)
    name += ':'
    if info is not None:
        print('%-10s\t%08Xh\t%s %s' % (name, masked_val, info[0], info[2]))
        return _decode_lsi_loginfo(info[1], val, unparsed)
    else:
        submask = mask >> 8
        while submask > 0:
            highmask = mask & ~submask
            lowmask = submask
            lowval = lowmask & val
            highval = highmask & val
            if lowval != 0:
                info = vals.get(highval, None)
                if info is not None:
                    print('%-10s\t%08Xh\t%s %s'
                          % (name, highval, info[0], info[2]))
                    return _decode_lsi_loginfo(info[1], val, unparsed)
            submask >>= 8

        print('%-10s\t%08Xh\tUnknown code' % (name, masked_val))
        return unparsed

def decode_lsi_loginfo(val):
    print('%-10s\t%08Xh' % ('Value', val))
    unparsed = _decode_lsi_loginfo(types, val, val)
    if unparsed:
        print('%-10s\t%08Xh' % ('Unparsed', unparsed))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Must provide a loginfo number to decode, as in:')
        print('%s 0x31120000' % sys.argv[0])
        sys.exit(1)

    try:
        val = int(sys.argv[1], 0)
    except ValueError:
        print('Failure to parse the value "%s", it must be a number'
              % sys.argv[1])
        sys.exit(1)

    decode_lsi_loginfo(val)