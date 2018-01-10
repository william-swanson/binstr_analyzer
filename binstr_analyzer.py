import argparse
import math
import itertools
import regex #NEW LIBRARY, HAD TO INSTALL
import sys

def __init__():
    parser = argparse.ArgumentParser(description="Command line utility to help determine if a binary string is normal.")
    parser.add_argument('test',type=str,help="What statistical test do you want to run on the binary string?\nOptions: normcurve, apen, all")
    parser.add_argument('string',type=str,help="The binary string to analyze.")

    parser.add_argument('-c',type=float,default=1.96,help="The distance from the origin on the normal curve (default: two standard deviations).")
    parser.add_argument('-p',type=float,default=0.5,help="The probability for a 1 in the string.")

    parser.add_argument('-k',type=int,default=1,help="Length of substring for approximate entropy, i.e. ApEn(k).")

    args = parser.parse_args()

    if args.test.lower() == "normcurve":
        normcurve(args.string,args.c,args.p)
    elif args.test.lower() == "apen":
        apen(args.string,args.k)
    elif args.test.lower() == "all":
        normcurve(args.string,args.c,args.p)
        print("".join(["-" for i in range(50)]))
        apen(args.string,args.k)
    else:
        print("Unknown test parameter. Aborting.")
        sys.exit(0)

def apen(binstr, k):
    print("APPROXIMATE ENTROPY ANALYSIS")
    print("Binary String: %s" %binstr)
    print("K: %d\n" %k)
    print("Approximate Entropy (k=%d): %f" %(k,calc_approx_entropy(binstr,k)))

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

def normcurve(binstr,c,p):
    print("NORMAL CURVE ANALYSIS")
    print("Binary String: %s" %binstr)
    print("C: %f" %c)
    print("P: %f\n" %p)

    interval = (calc_interval(p,len(binstr),c))
    sampleavg = (calc_sampleavg(binstr.count('1'),len(binstr)))
    print("the interval is (%f,%f)." %(interval[0],interval[1]))
    print("the sample average is %f." %sampleavg)

    if sampleavg >= interval[0] and sampleavg <= interval[1]:
        print("Not reject")
    else:
        print("Reject")

if __name__ == '__main__':
    __init__()