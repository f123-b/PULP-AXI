# AXI4-Lite → APB4 Verification Plan

## Scope
Target the PULP AXI `axi_lite_to_apb` bridge as the reference DUT. The plan separates stimulus, checking, assertions and coverage so it can be migrated to UVM/VCS/Questa later.

## Features / testpoints
| Feature | Directed test | Random test | Checker | Coverage |
|---|---|---|---|---|
| AXI write → APB write | aligned/unaligned address | random addr/data/strb | scoreboard | address region × strobe |
| AXI read → APB read | each slave region | random addresses | scoreboard | address region |
| Decode error | unmapped address | random holes | expected DECERR | response |
| APB slave error | PSLVERR | randomized slave error | expected SLVERR | response × op |
| Backpressure | delayed PREADY | random delay | protocol monitor | wait cycles |
| Reset | reset idle/access | randomized reset | state checker | reset phase |

## Closure criterion
- All directed tests pass.
- Random regression has no reproducible mismatches.
- Every functional coverpoint and required cross is hit, or waived with rationale.
- Assertions are clean across regression.
