import argparse
import math
import itertools
import regex #NEW LIBRARY, HAD TO INSTALL
import sys
import matplotlib.pyplot as plt

def __init__():
    parser = argparse.ArgumentParser(description="Command line utility to help determine if a binary string is normal.")
    parser.add_argument('test',type=str,help="What statistical test do you want to run on the binary string?\nOptions: normcurve, apen, all")
    parser.add_argument('string',type=str,help="The binary string to analyze.")

    parser.add_argument('-c',type=float,default=1.96,help="The distance from the origin on the normal curve (default: two standard deviations).")
    parser.add_argument('-p',type=float,default=0.5,help="The probability for a 1 in the string.")

    parser.add_argument('-k',type=str,default='1',
                        help="Length of substring for approximate entropy, i.e. ApEn(k). A single integer will calculate a single ApEn.\
                        A string of the form a:b where a and b are integers will calculate all the ApEn values for k=[a,b].")
    parser.add_argument('--show-plt',action='store_true',help="Display a plot of the ApEn values for 1 up to k for singleton k. \
                        If k is given as a range, will only plot those points in the range.")

    args = parser.parse_args()

    if args.test.lower() == "normcurve":
        normcurve(args.string,args.c,args.p)
    elif args.test.lower() == "apen":
        apen(args.string,args.k,args.show_plt)
    elif args.test.lower() == "all":
        normcurve(args.string,args.c,args.p)
        print("".join(["-" for i in range(50)]))
        apen(args.string,args.k,args.show_plt)
    else:
        print("Unknown test parameter. Aborting.")
        sys.exit(0)

def apen(binstr, kval, show_plt):

    k = a = b = -1
    #TODO: should do some error checking to make sure there is no other garbage in the string/if there are extra :
    if ":" in kval:
        a,b = kval.split(":")
        a = int(a)
        b = int(b)
    else:
        k = int(kval)

    en_vals = []
    print("APPROXIMATE ENTROPY ANALYSIS")
    if k == -1:
        for i in range(a,b+1,1):
            approx_ent = calc_approx_entropy(binstr,i)
            print("Approximate Entropy (k=%d): %f" %(i,approx_ent))
            en_vals.append(approx_ent)
    else:
        approx_ent = calc_approx_entropy(binstr,k)
        print("Approximate Entropy (k=%d): %f" %(k,approx_ent))
        en_vals.append(approx_ent)

    if show_plt == True:
        plt.plot(range(1,len(en_vals)+1,1),en_vals,'ro')
        plt.show()

def calc_interval(p, n, c):
    lower_bound = (p - c*math.sqrt((p*(1-p))/float(n)))
    upper_bound = (p + c*math.sqrt((p*(1-p))/float(n)))
    return (lower_bound, upper_bound)

def calc_sampleavg(sn,n):
    return float(sn)/n

''' bin_string is the binary string to analyze, 
    k is the value in ApEn(k)'''
#TODO: should adjust this to be more efficient if a range of values are being calculated
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
    #print bin_kstrs
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