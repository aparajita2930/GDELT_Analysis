import math
count=0
sp=0
sp2=0
l=[1,2,3,4,5,6]
def combination(N, M, part_sum=[]):
        global count
        global sp
	global sp2
	global l
        sum_val = sum(part_sum)

        if sum_val == M and len(part_sum)==N:
                #print("sum(%s)=%s" % (part_sum, M))
                count=count+1
		p=1
                for i in range(len(part_sum)):
                        p=p*part_sum[i]
                sp=sp+p
		sp2=sp2+(p**2)
        if sum_val >= M:
                return
        for i in range(0,6):
                n1 = l[i]
                combination(N, M, part_sum + [n1])

def exp_prod_std(N, M):
	combination(N,M)
	global count
	global sp
	global sp2
	exp_val=sp/float(count)
	print 'Expected value of product: '
	print "{0:.10f}".format(exp_val)
	print 'Standard deviation of product: '
	print "{0:.10f}".format(math.sqrt((sp2+(count*(exp_val**2))-(2*exp_val*sp))/float(count-1)))
	count=0; sp=0; sp2=0



exp_prod_std(8, 24)
#Output - Expected value of product: 1859.9329541659
#	- Standard deviation of product: 855.0742120877

exp_prod_std(50, 150)
#Output - Expected value of product: 
#	- Standard deviation of product: 



