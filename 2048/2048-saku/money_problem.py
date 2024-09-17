import random

money = 0
n_sims = 100000

# ALT 1
for i in range(n_sims):
    dice = random.randint(1, 6)

    if dice == 1 or dice == 2:
        money = money + 3

print("Alternative 1: ", money/n_sims)


# ALT 2
money = 0
for i in range(n_sims):
    dice = random.randint(1, 6)

    if dice == 1 or dice == 2:
        money = money + 0
    else:
        money = money + 0.8

print("Alternative 2: ", money/n_sims)


E_Alt1 = 1/6*1.5 + 1/6*1.5 + 4*(1/6*0)
print("E(ALT1) =", E_Alt1)

E_Alt2 = 2*(1/6*0) + 4*(1/6*0.8)
print("E(ALT2) =", E_Alt2)
