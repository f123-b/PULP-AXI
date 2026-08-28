from verification.ref_model.axi_lite_apb_model import (
    AddressRule, AxiLiteToApbReferenceModel, AxiResp
)

RULES = [AddressRule(0x0000, 0x1000, 0), AddressRule(0x1000, 0x2000, 1)]

def dut():
    return AxiLiteToApbReferenceModel(RULES)

def test_write_decodes_and_aligns_address():
    req, early = dut().write_request(0x1003, 0xDEADBEEF, 0xF)
    assert early is None
    assert req.slave == 1
    assert req.paddr == 0x1000
    assert req.pwdata == 0xDEADBEEF
    assert req.pstrb == 0xF

def test_read_decode_error():
    req, rsp = dut().read_request(0x4000)
    assert req is None
    assert rsp.resp == AxiResp.DECERR

def test_zero_strobe_is_noop_okay():
    req, rsp = dut().write_request(0x0040, 0x12345678, 0)
    assert req is None
    assert rsp.resp == AxiResp.OKAY

def test_apb_slave_error_maps_to_axi_slverr():
    assert dut().complete_write(True).resp == AxiResp.SLVERR
    assert dut().complete_read(0x55, True).resp == AxiResp.SLVERR

def test_overlap_is_detected():
    m = AxiLiteToApbReferenceModel([AddressRule(0, 0x100, 0), AddressRule(0x80, 0x180, 1)])
    try:
        m.decode(0x90)
    except ValueError:
        pass
    else:
        raise AssertionError("overlapping rules must be rejected")
