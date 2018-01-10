import argparse
import math
import itertools
import regex #NEW LIBRARY, HAD TO INSTALL

def __init__():
    parser = argparse.ArgumentParser(description="determine if a binary string is random")
    parser.add_argument('string',type=str,help="the binary string to analyze")

    parser.add_argument('-c',type=float,default=1.96,help="the distance from the origin on the normal curve")
    parser.add_argument('-p',type=float,default=0.5,help="the probability for a 1")
    parser.add_argument('-k',type=int,default=1,help="length of substring for approximate entropy, ApEn(k)")

    args = parser.parse_args()

    print(args.string)
    print(args.c)
    print(args.p)
    interval = (calc_interval(args.p,len(args.string),args.c))
    sampleavg = (calc_sampleavg(args.string.count('1'),len(args.string)))

    print("the interval is (%f,%f)." %(interval[0],interval[1]))
    print("the sample average is %f." %sampleavg);

    if sampleavg >= interval[0] and sampleavg <= interval[1]:
        print("not reject")
    else:
        print("reject")

    print calc_approx_entropy(args.string,1)
    print calc_approx_entropy(args.string,2)

def calc_interval(p, n, c):
    lower_bound = (p - c*math.sqrt((p*(1-p))/float(n)))
    upper_bound = (p + c*math.sqrt((p*(1-p))/float(n)))
    return (lower_bound, upper_bound)

def calc_sampleavg(sn,n):
    return float(sn)/n

''' bin_string is the binary string to analyze, 
    k is the value in ApEn(k)'''
def calc_approx_entropy(bin_string, k):
    if k == 1:
        return calc_H(bin_string, k)
    elif k > 1:
        return calc_H(bin_string, k) - calc_H(bin_string, k-1)
    else:
        print("k error")

def calc_H(bin_string, k):
    #generate all binary strings of length k
    bin_kstrs = dict()
    for seq in itertools.product("01", repeat=k):
        s = "".join(seq)
        bin_kstrs[s] = len(regex.findall(s,bin_string, overlapped=True))
    print bin_kstrs
    h_value = 0
    for key in bin_kstrs:
        p = bin_kstrs[key]/float(len(bin_string)-k+1)
        if p == 0:
            continue
        h_value -= p*math.log(p,2)
    return h_value
    #bin_kstrs = ["".join(seq) for seq in itertools.product("01", repeat=k)]




if __name__ == '__main__':
    __init__()