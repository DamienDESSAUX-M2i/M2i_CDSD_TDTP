-- Question 1
SELECT *
FROM users
WHERE location = (
    SELECT location
    FROM users
    WHERE birth_date = (
        SELECT MIN(birth_date)
        FROM users
    )
);

-- Question 2
SELECT *
FROM users
WHERE salary < (
    SELECT AVG(salary)
    FROM users
    WHERE job = 'Developer'
);

-- Question 3
SELECT *
FROM users
WHERE salary > (
    SELECT AVG(salary)
    FROM users
    WHERE location IN (
        SELECT location
        FROM users
        WHERE first_name = 'John' AND last_name = 'Doe'
    )
);