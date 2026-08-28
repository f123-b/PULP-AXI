# PULP AXI Verification Lab

面向数字 IC / SoC 验证岗位的可复现学习项目。上游 DUT 选用 ETH Zurich / University of Bologna 的 `pulp-platform/axi`，本仓库增加验证计划、Python reference model、SVA 示例、回归测试和 CI；不把上游 RTL 冒充为原创。

## 当前验证对象
- AXI4-Lite → APB4 bridge: `axi_lite_to_apb`
- 上游固定 commit: `4da15979747f326bde2f9869c64e587ce599772c`

## 已实现
- 地址译码与对齐 reference model
- AXI DECERR / SLVERR 响应映射检查
- zero-strobe no-op 场景
- APB setup/access 与 wait-state SVA 示例
- pytest regression
- GitHub Actions 固定上游版本并检查目标 RTL
- verification plan / coverage closure 规划

## 本地运行
```bash
make test
make fetch-upstream
```

## 下一阶段
1. 增加可综合 wrapper，把 PULP `axi_lite_to_apb` 接入 Verilator/VCS/Questa。
2. 增加 constrained-random transaction generator。
3. 增加 scoreboard、functional coverage 和 fail-seed replay。
4. 商业仿真器环境下迁移为 UVM agent / sequence / scoreboard / covergroup。

详见 `docs/VERIFICATION_PLAN.md` 和 `UPSTREAM.md`。
