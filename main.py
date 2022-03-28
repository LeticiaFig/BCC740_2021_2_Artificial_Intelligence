from environments import ToilletPaperEnv
from agents import ToilletPaperAgent
import numpy as np
import matplotlib.pyplot as plt

env1 = ToilletPaperEnv(10,2000,10000)

agent = ToilletPaperAgent(env1)

prices = []
tpnumber = []
spendings = []

for i in range(1000):
    prices.append(env1.price)
    tpnumber.append(env1.TPNumber)
    spendings.append(agent.spendings)
    agent.act()

#plt.plot(prices)
#plt.show()
plt.plot(tpnumber)
plt.show()
# plt.plot(spendings)
# plt.show()

# cumspe = np.cumsum(spendings)
# plt.plot(cumspe)
# plt.show()