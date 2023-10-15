# sothis-plotter

Makes pretty plots from [sothis](https://github.com/rainshowerLabs/sothis) JSON output

## Installation

This tool is designed for Python 3.8+. Install the matplotlib dependency with:

```bash
pip3 install matplotlib
```

## Simple Example

You can test this tool on an example dataset from Uniswap V2 provided in this repository:
```bash
python3 plotter.py -i json_examples/univ2_eth_usdc.json -d
```

![Plot](./example_plot.png)

To generate a dataset similar to the example provided in this repository, run sothis to pull storage slot 0 ([`totalSupply`](https://evm.storage/eth/17715162/0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc)) for the Uniswap v2 ETH/USDC pool:
```bash
sothis --mode fast_track --source_rpc https://eth.llamarpc.com --contract_address 0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc --storage_slot 0 --origin_block 14343000 --terminal_block 14345000 --filename univ2_eth_usdc.json
```
## Chainlink ETH Price Example

Historic on-chain price can be pulled from Chainlink aggregators.

1. Start [blutgang](https://github.com/rainshowerLabs/blutgang) for caching speed boost when querying data

`blutgang`

2. Collect historic Chainlink data with sothis, using blutgang local RPC caching server for speed boost. The contract and storage slot used here is for [the mainnet ETH/USD price](https://data.chain.link/ethereum/mainnet/crypto-usd/eth-usd):
```bash
sothis --mode fast_track --source_rpc http://127.0.0.1:3000 --contract_address 0x50ce56a3239671ab62f185704caedf626352741e --storage_slot 44328162026580455436095296388066680819728981146521451465192564316796958161166 --origin_block 18300000 --terminal_block 18355500 --query_interval 100 --filename eth-price.json
```

3. Plot sothis data
```bash
python3 plotter.py -i eth-price.json -d -c eth-price.csv
```

![Chainlink Data Plot](./eth_price_example.png)

![Coingecko Plot](./eth_price_coingecko.png)

## Advanced Example

The tripool_example directory contains data for a more advanced example. The tripool example uses sothis-plotter primarily to convert the sothis data to csv data. A separate Python script does the plotting for this special case where 3 input CSV files are used.

The steps to recreate this data are the following.

1. Start [blutgang](https://github.com/rainshowerLabs/blutgang) for caching speed boost when querying data

`blutgang`

2. Identify the storage slot for the [Curve stableswap tripool](https://etherscan.io/address/0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7#code) balances array

`cast keccak 0x0000000000000000000000000000000000000000000000000000000000000001`

Returns: 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6

DAI = 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6

USDC = 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf7

USDT = 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf8

3. Use sothis to collect tripool JSON data from blockchain. The start/end blocks in this example are chosen to show the impact of the March 2023 USDC depeg:

`sothis --mode fast_track --source_rpc http://127.0.0.1:3000 --contract_address 0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7 --storage_slot 80084422859880547211683076133703299733277748156566366325829078699459944778998 --origin_block 16790000 --terminal_block 16810000 --query_interval 100 --filename tripool_dai.json`

`sothis --mode fast_track --source_rpc http://127.0.0.1:3000 --contract_address 0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7 --storage_slot 80084422859880547211683076133703299733277748156566366325829078699459944778999 --origin_block 16790000 --terminal_block 16810000 --query_interval 100 --filename tripool_usdc.json`

`sothis --mode fast_track --source_rpc http://127.0.0.1:3000 --contract_address 0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7 --storage_slot 80084422859880547211683076133703299733277748156566366325829078699459944779000 --origin_block 16790000 --terminal_block 16810000 --query_interval 100 --filename tripool_usdt.json`

4. Convert JSON data to csv:

`python3 plotter.py -i tripool_dai.json -d -c dai.csv`

`python3 plotter.py -i tripool_usdc.json -d -c usdc.csv`

`python3 plotter.py -i tripool_usdt.json -d -c usdt.csv`

5. Plot the csv files with the custom plotting script:

`python3 tripool_plot.py`

![Plot](./tripool_example/tripool_plot.png)