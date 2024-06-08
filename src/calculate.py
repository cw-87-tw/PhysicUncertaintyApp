import statistics as st
from math import sqrt

def MURound(x: float):
    mod = 1e10
    x *= mod
    x = str(int(x))
    if x == "0": return 0
    cnt = len(x) - 1 # 10 的多少次方
    x = x[:3] # 把後面都捨去掉
    # print(x)
    if x[2] != "0": res = (int(x[:2]) + 1) * (10 ** cnt) # 有第三位無條件進位
    else: res = int(x[:2]) * (10 ** cnt)
    res /= mod * 10 # 因為在處理的時候會多保留一位
    return res

def meanRound(x: float):
    mod = 1e10
    x *= mod
    x = str(int(x))
    if x == "0": return 0
    cnt = len(x) - 1 # 10 的多少次方
    x = x[:3] # 把後面都捨去掉
    if int(x[2]) >= 5: res = (int(x[:2]) + 1) * (10 ** cnt) # 第三位四捨五入
    else: res = int(x[:2]) * (10 ** cnt)
    res /= mod * 10
    return res


class Data:
    def __init__(self, x, lc_or_uc: float = 0.1):
        if isinstance(x, list):
            # 不確定度
            lc = lc_or_uc
            self.ua = st.pstdev(x) / sqrt(len(x)) # 標準差
            self.ub = lc / (2 * sqrt(3)) 
            self.uc = sqrt(self.ua * self.ua + self.ub * self.ub)
            self.value = st.mean(x)
        else:
            uc = lc_or_uc
            self.value = x
            self.uc = uc

    def __add__(self, other):
        if isinstance(other, Data): 
            return Data(self.value + other.value, sqrt(self.uc ** 2 + other.uc ** 2))
        else:
            return Data(self.value + other, self.uc)

    def __sub__(self, other):
        if isinstance(other, Data): 
            return Data(self.value - other.value, sqrt(self.uc ** 2 + other.uc ** 2))
        else:
            return Data(self.value - other, self.uc)

    def __mul__(self, other):
        if isinstance(other, Data): 
            return Data(self.value * other.value, sqrt((self.uc / self.value) ** 2 + (other.uc / other.value) ** 2) * abs(self.value * other.value))
        else:
            return Data(self.value * other, self.uc * abs(other))

    def __truediv__(self, other):
        if isinstance(other, Data): 
            return Data(self.value / other.value, sqrt((self.uc / self.value) ** 2 + (other.uc / other.value) ** 2) * abs(self.value / other.value))
        else:
            return Data(self.value / other, self.uc * abs(1 / other))
        

    def sqrt(self):
        return Data(sqrt(self.value), sqrt(self.uc))
    
    def abs(self):
        return Data(abs(self.value), self.uc)

    def __str__(self):
        return f"{meanRound(self.value)} ± {MURound(self.uc)}"

