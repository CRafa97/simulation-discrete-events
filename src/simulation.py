from tools import *
from random import choice    

# RATES
# arrives
lb_arr = 1 / 20
mean = 10
var = 5
# download / upload
lb_down_up =  1 / 30
# fix airplane
rot = [(0, 0.9), (1, 0.1)]
lb_fix = 1 / 15
# reload
lb_rel = 1 / 30

def simulate(T, rnd = False):
    # time var
    t = 0

    # count vars
    na = 0
 
    # states
    SS = { i : 0 for i in range(5) } # empty system
    q = []
    
    # outputs
    A = { i : [] for i in range(5) }
    D = { i : [] for i in range(5) }

    # events
    ta = exponential(lb_arr)
    td = {i: 2**32 for i in range(5)} 

    #log
    f = open('./report.txt', 'w')

    while True:
        if min(ta, t, *td.values()) > T:
            break

        if ta == min(ta, *td.values()):
            t = ta
            na += 1
            f.writelines(f"{t} minutos -- Un avion arriba al aeropuerto, identificador {na}\n")
            ta = t + exponential(lb_arr)

            free = [p_id for p_id, a_id in SS.items() if a_id == 0]

            if free:
                idx = free[0] if not rnd else choice(free)
                A[idx].append(t)
                SS[idx] = na
                f.writelines(f"{t} minutos -- Avion {SS[idx]} entra en la pista {idx + 1}\n")
                y = departure()
                td[idx] = y + t
            else:
                f.writelines(f"{t} minutos -- Avion {na} espera para entrar en una pista\n")
                q.append(na)
        else:
            t = min(td.values())
            pidx = [p_id for p_id, d in td.items() if d == t][0]
            D[pidx].append(t)
            f.writelines(f"{t} minutos -- Avion {SS[pidx]} abandona el aeropuerto por la pista {pidx + 1}\n")
            SS[pidx] = 0
            td[pidx] = 2**32

            # dequeue
            if len(q) > 0:
                nxt = q.pop(-1)
                A[pidx].append(t)
                SS[pidx] = nxt
                f.writelines(f"{t} minutos -- Avion {SS[pidx]} entra en la pista {pidx + 1}\n")
                y = departure()
                td[pidx] = y + t

    f.close()

    return A, D

def compute_times(A, D):
    
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

    return common + t_fix + max(t_reload, t_down_up)

if __name__ == "__main__":
    T = 10080
    A, D = simulate(T, rnd=True)
    ans = compute_times(A, D)
    print('Tiempo Total para cada pista:')
    print('-----------------------------')
    for p, t in ans.items():
        print(f"Pista {p + 1}: {t}")