import React, { useState, useEffect } from 'react';

const App = () => {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        console.log("message !!!!")
        const response = await fetch('http://localhost:8080/employees');
        console.log(response)
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        setEmployees(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchEmployees();
  }, []);


  return (
    <div className='container'>
      <h1>Liste des employées</h1>
    <table className="table table-striped table-bordered table-hover">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">First Name</th>
          <th scope="col">Last Name</th>
          <th scope="col">Email</th>
          <th scope="col">Phone Number</th>
          <th scope="col">Department</th>
        </tr>
      </thead>
      <tbody>
        {employees.map((employee, index) => (
          <tr key={employee.id}>
            <td>{employee.id}</td>
            <td>{employee.firstName}</td>
            <td>{employee.lastName}</td>
            <td>{employee.email}</td>
            <td>{employee.phoneNumber}</td>
            <td>{employee.department}</td>
          </tr>
        ))}
      </tbody>
    </table>
    </div>
  );
};

export default App;
