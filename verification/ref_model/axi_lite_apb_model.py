"""Small transaction-level reference model for AXI4-Lite -> APB4 verification.

This is original verification support code. It is intentionally independent of
PULP AXI RTL and is used as a golden model for directed/random tests.
"""
from dataclasses import dataclass
from enum import IntEnum

class AxiResp(IntEnum):
    OKAY = 0b00
    SLVERR = 0b10
    DECERR = 0b11

@dataclass(frozen=True)
class AddressRule:
    start: int
    end: int
    slave: int

@dataclass(frozen=True)
class ApbRequest:
    paddr: int
    pwrite: bool
    pwdata: int = 0
    pstrb: int = 0
    slave: int = 0

@dataclass(frozen=True)
class AxiReadResponse:
    data: int
    resp: AxiResp

@dataclass(frozen=True)
class AxiWriteResponse:
    resp: AxiResp

class AxiLiteToApbReferenceModel:
    def __init__(self, rules: list[AddressRule], data_width: int = 32):
        if data_width % 8:
            raise ValueError("data_width must be byte aligned")
        self.rules = list(rules)
        self.data_width = data_width
        self.bytes_per_beat = data_width // 8
        self.data_mask = (1 << data_width) - 1
        self.strb_mask = (1 << self.bytes_per_beat) - 1

    def decode(self, addr: int) -> int | None:
        hits = [r.slave for r in self.rules if r.start <= addr < r.end]
        if len(hits) > 1:
            raise ValueError(f"overlapping address rules for 0x{addr:x}")
        return hits[0] if hits else None

    def align(self, addr: int) -> int:
        return addr & ~(self.bytes_per_beat - 1)

    def write_request(self, addr: int, data: int, strb: int):
        slave = self.decode(addr)
        if slave is None:
            return None, AxiWriteResponse(AxiResp.DECERR)
        if (strb & self.strb_mask) == 0:
            return None, AxiWriteResponse(AxiResp.OKAY)
        return ApbRequest(self.align(addr), True, data & self.data_mask,
                          strb & self.strb_mask, slave), None

    def read_request(self, addr: int):
        slave = self.decode(addr)
        if slave is None:
            return None, AxiReadResponse(0, AxiResp.DECERR)
        return ApbRequest(self.align(addr), False, slave=slave), None

    @staticmethod
    def complete_write(pslverr: bool) -> AxiWriteResponse:
        return AxiWriteResponse(AxiResp.SLVERR if pslverr else AxiResp.OKAY)

    @staticmethod
    def complete_read(prdata: int, pslverr: bool) -> AxiReadResponse:
        return AxiReadResponse(prdata, AxiResp.SLVERR if pslverr else AxiResp.OKAY)
