// Original learning/verification assertions for an AXI4-Lite -> APB4 bridge.
// Bind/adapt signal names to the concrete DUT wrapper in a commercial simulator flow.
module axi_lite_apb_properties (
  input logic clk_i,
  input logic rst_ni,
  input logic psel,
  input logic penable,
  input logic pready,
  input logic [31:0] paddr,
  input logic pwrite,
  input logic [31:0] pwdata
);
  apb_access_after_setup: assert property (@(posedge clk_i) disable iff (!rst_ni)
    penable |-> $past(psel && !penable));

  apb_wait_stable: assert property (@(posedge clk_i) disable iff (!rst_ni)
    psel && penable && !pready |=> $stable({psel, penable, paddr, pwrite, pwdata}));
endmodule
