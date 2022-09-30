
class Hkac:
    def __init__(self, candles):
        self.kandles = candles

        for idx in range(len(self.kandles)):
            if idx < 1 : 
                self.kandles[idx].append(self.kandles[idx][1])
                self.kandles[idx].append(self.kandles[idx][2])
                self.kandles[idx].append(self.kandles[idx][3])
                self.kandles[idx].append(self.kandles[idx][4])
                continue

            # Heikin-Ashi

            # Candle	Regular Candlestick	Heikin Ashi Candlestick
            # Open	Open0	(HAOpen(-1) + HAClose(-1))/2
            # High	High0	MAX(High0, HAOpen0, HAClose0)
            # Low	Low0	MIN(Low0, HAOpen0, HAClose0
            # Close	Close0	(Open0 + High0 + Low0 + Close0)/4

            HKOpen = (self.kandles[idx-1][6] + self.kandles[idx-1][9]) / 2
            HKClose = (self.kandles[idx][1] + self.kandles[idx][2] + self.kandles[idx][3] + self.kandles[idx][4]) / 4
            HKHigh = max(self.kandles[idx][2], HKOpen, HKClose)
            HKLow = min(self.kandles[idx][3], HKOpen, HKClose)

            self.kandles[idx].append(HKOpen)
            self.kandles[idx].append(HKHigh)
            self.kandles[idx].append(HKLow)
            self.kandles[idx].append(HKClose)
            # p(HKOpen, HKHigh, HKLow, HKClose) 

        pass
