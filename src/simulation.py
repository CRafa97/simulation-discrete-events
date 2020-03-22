from tools import *
    
# RATES
# arrives
lb_arr = 1 / 20
mean = 10
var = 5
# download / upload
lb_down_up =  1 / 30
# fix airplane
rot = [(0, 0.9), (1,0.1)]
lb_fix = 1 / 15
# reload
lb_rel = 1 / 30

def simulate(T):
    # time var
    t = 0

    # count vars
    na = 0
 
    # states
    SS = { i : 0 for i in range(5) } # empty system
    n = 0
    
    # outputs (i - airplain)
    A = { i : [] for i in range(5) }
    D = { i : [] for i in range(5) }

    # events
    ta = exponential(lb_arr)
    td = {i: 2**32 for i in range(5)} 

    while True:
        if min(ta, t, *td.values()) > T:
            break

        if ta == min(ta, *td.values()):
            t = ta
            ta = t + exponential(lb_arr)
            na += 1

            queue = True
            
            for i in range(5):
                if td[i] == 2**32:
                    A[i].append(t)
                    SS[i] = na
                    y = departure()
                    td[i] = y + t
                    queue = False
                    break
            
            if queue:
                n += 1
        else:
            t = min(td.values())
            idx = -1
            for i in range(5):
                if td[i] == t:
                    td[i] = 2**32
                    idx = i
                    break
            D[i].append(t)
            SS[i] = 0

            # dequeue
            if n > 0:
                n -= 1
                na += 1
                A[i].append(t)
                SS[i] = na
                y = departure()
                td[i] = y + t

    times = {}
    for i in range(5):
        arr = A[i]
        dep = D[i]
        acc = 0

        for j in range(1, len(A[i])):
            acc += arr[j] - dep[j - 1]
        acc += arr[0]
        
        times[i] = acc

    return times

def departure():
    common = normal(mean, var) + normal(mean, var)
    t_reload = exponential(lb_rel)
    
    t_fix = exponential(lb_fix) * inverse_method(rot)
    t_down_up = exponential(lb_down_up)

    return common + min(t_reload, t_fix + t_down_up)

if __name__ == "__main__":
    T = 10080
    ans = simulate(T)
    print(ans)