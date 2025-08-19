题目2
1.FFT算法
输入应该是数组，如果是实数就自动看作虚部为0的复数
输出是频域信号。
而在正则匹配中，就可以先用FFT将其转化为频域乘法，再用iFFT，达到加速计算的目的。

2.详细的正则匹配过程实现
代码（python）
import numpy as np
S = np.array([97,97, 98, 97, 99, 99, 97, 98, 97,98,99])  # "aabaccababc"
P_rev = np.array([99, 0, 97])                            # 反转后的 "a?c"
# 补零到长度 >= n + m - 1，并将其转化为频域信号
fft_size = 1 << (len(S) + len(P_rev) - 1).bit_length()   #长度为16，因为2的次幂计算速度更快
S_fft = np.fft.fft(S, fft_size)
P_rev_fft = np.fft.fft(P_rev, fft_size)
print(fft_size)
print(S_fft)
print(P_rev_fft)
# 频域乘法
conv_fft = S_fft * P_rev_fft
C = np.fft.ifft(conv_fft).real.round()  # 取实部并舍入误差
print(C)

输出结果为
C[ 9603.  9603. 19111. 19012. 19307. 19210. 19206. 19305. 19012. 19208. 19210.  9506.  9603.     0.     0.     0.]
分析
a?c字符串的平方和为97^2 + 0 + 99^2 = 19210
其中第6个，第11个，值为19210。
由我们给出的字符串例子也可以看出，这两个位置给出的均为字符串'a?c'中c字符的位置，字符串长度为3，可知匹配的起始位置是4和9.

3.进一步优化，我暂时没有思路。