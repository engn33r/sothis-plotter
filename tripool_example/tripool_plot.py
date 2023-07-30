import matplotlib.pyplot as plt
import pandas as pd

dai = pd.read_csv('dai.csv', header=None)
usdc = pd.read_csv('usdc.csv', header=None)
usdt = pd.read_csv('usdt.csv', header=None)

# Change DAI 1e18 decimals to match 1e6 decimals of USDC and USDT
dai_lower_decimals = []
for i in range(len(dai[1])):
	dai_lower_decimals.append(int(dai[1][i])/(10**12))

plt.plot(dai[0], dai_lower_decimals, label='DAI', color="tab:orange")
plt.plot(usdc[0], usdc[1], label='USDC', color="tab:blue")
plt.plot(usdt[0], usdt[1], label='USDT', color="tab:green")

# Set text
plt.title('DAI-USDC-USDT weights of Curve Tripool')
plt.xlabel('Block number')
plt.ylabel('Amount in pool')

# Show legend and plot
plt.legend()
plt.show()