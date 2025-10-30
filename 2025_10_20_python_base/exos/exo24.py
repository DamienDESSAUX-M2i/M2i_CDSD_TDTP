from math import log, ceil

capital = 10_000
taux = 0.1

print(f"Le capital est doublé au bout de la {ceil(log(2)/log(1+taux))}e année.")

itermax = 1_000
iter = 0
capital_visé = 2*capital
while (iter < itermax) and (capital < capital_visé):
    capital *= (1 + taux)
    iter += 1
print(f"Le capital est doublé au bout de la {iter}e année.")