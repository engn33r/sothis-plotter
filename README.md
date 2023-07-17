# sothis-plotter

Makes pretty plots from [sothis](https://github.com/rainshowerLabs/sothis) JSON output

## Installation

This tool is designed for Python 3.8+. Install the matplotlib dependency with:

```bash
pip3 install matplotlib
```

## Example

You can test this tool on an example dataset from Uniswap V2 provided in this repository:
```bash
python3 plotter.py -i json_examples/univ2_eth_usdc.json -d
```

![Plot](./example_plot.png)

To generate a dataset similar to the example provided in this repository, run sothis to pull storage slot 0 ([`totalSupply`](https://evm.storage/eth/17715162/0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc)) for the Uniswap v2 ETH/USDC pool:
```bash
sothis --mode fast_track --source_rpc https://eth.llamarpc.com --contract_address 0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc --storage_slot 0 --origin_block 14343000 --terminal_block 14345000 --filename univ2_eth_usdc.json
```
