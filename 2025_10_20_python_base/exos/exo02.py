# Question 1
# Après exécution A=B=2
# Question 2
# Le programme ne permet pas d'échanger les variables A et B
# Question 3
A = 1
B = 2
print(f"{A = } et {B = }")

C = A
A = B
B = C
print(f"{A = } et {B = }")

# Autre solution
A,B = B,A
print(f"{A = } et {B = }")