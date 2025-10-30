from math import log, ceil

population = int(input("Population : "))
taux = float(input("Taux : "))
population_visee = int(input("Population vidée : "))

# Qolution sans boucle
print(f"Il faudra {ceil((log(population_visee)-log(population))/log(1+taux))} années pour atteindre la population visée")

# Solution avec boucle
itermax = 1_000
iter = 0
while (iter < itermax) and (population < population_visee):
    population *= 1 + taux
    iter += 1
print(f"Il faudra {iter} année pour atteindre la population visée")