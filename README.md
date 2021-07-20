# MACD-indicator
Simple implementation of MACD indicator

I present to you my simple implementation of MACD indicator. 
About MACD: short for moving average convergence/divergence, is a trading indicator used in technical analysis of stock prices.
The program need to work proper input csv file, located in ‘csv’ folder. Program takes specified number of price samples from csv file. Then calculate MACD and SIGNAL values and then carry out the simulation. At the end print the profit/loss of algorithm and profit/loss after one-time purchase at the beginning and hold till the end. 
Presented algorithm based on knowledge that if value of MACD indicator is greater than zero then it’s ‘less’ trusted. There are many improvements of this algorithm such as: make decisions based on the MACD and SIGNAL line slope, or another strategy: be happy with 5-7 % profit and sell immediately when you lose more than 3-5 %.

