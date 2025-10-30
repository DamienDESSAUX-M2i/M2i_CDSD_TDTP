itermax = 1_000
iter = 0
stop_signal = False
while (iter < itermax) and (stop_signal == False):
    user_input = float(input("Saisir un nombre entre 1 et 3 : "))
    if 1 <= user_input <= 3:
        stop_signal = True
    iter += 1