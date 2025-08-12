def calculate_monthly_salaries(employee_data: dict) -> dict:

    """     
    Calculates the monthly salary of all employees in each subsidiary company of a parent company.

    [Args]
    data (dict): A dictionary with the name of the subsidiary companies as the keys(strings) and a list 
                 containing thier employees' details as the values. Within each list are dictionaries containing 
                 the following details about each employee:
                - 'name' (str): The name of the employee.
                - 'job' (str): The job title of the employee.
                - 'hourly_rates' (int()): The amount payable per hour worked.
                - 'weekly_hours_worked' (int): The number of hours worked by the employee.
                - 'contract hours' (int): The number of hours expected to be worked per contract agreement.

    [Return]
    dict: A dictionary with subsidiary company names as the keys(strings) and a list containing streamlined employee details as the values.
          Within each list are dictionaries containing an updated version of the employee details, with keys:
          - 'name' (str): The name of the employee.
          - 'job' (str): The job title of the employee.
          - 'monthly_salary' (int): The monthly salary of the employee.

    """ 

    # Initialize an empty dictionary to store final results
    employee_details_per_subsidiary = {}

    # Iterate over each company and their personnel data
    for subsidiary_names, personnel_data in employee_data.items():

        # Initialize an empty list to aggregate streamlined details of the current company's employee 
        employee_list = []

        # Loop over each employee's details
        for employee_details in personnel_data:
            
            # Extract employee wage attributes
            hourly_rate = employee_details.get('hourly_rate', 0)
            weekly_hours_worked = employee_details.get('weekly_hours_worked', 0)
            contract_hours = employee_details.get('contract_hours', 0)

            # Calculate monthly salary
            if weekly_hours_worked <= contract_hours:
                monthly_salary = weekly_hours_worked * hourly_rate * 4
            else:
                overtime_worked = weekly_hours_worked - contract_hours
                overtime_salary = overtime_worked * hourly_rate * 1.5
                contract_salary = contract_hours * hourly_rate 
                monthly_salary = (contract_salary + overtime_salary) * 4
            
            # Update the employee details with the monthly salary
            employee_details.update({"monthly_salary": monthly_salary})

            # Append employee details to the company's list
            employee_list.append({"name" : employee_details['name'],
                                  "job" : employee_details['job'],
                                  "monthly_salary" : int(employee_details["monthly_salary"])})
        
        # Add the list of employees to the company in the result dictionary
        employee_details_per_subsidiary[subsidiary_names] = employee_list

    return employee_details_per_subsidiary


def global_company_statistics(salary_data: dict) -> dict:

    """     
    Calculates the global minimum, average, and maximum salaries of all employees in the company.

    [Args]
    salary_data (dict): A dictionary with the subsidiary company names as the keys(strings) and a list containing 
                 thier employees details as the values.
                 Within each list are dictionaries containing the following details about each employee:
                 - 'name' (str): The name of the employee.
                 - 'job' (str): The job title of the employee.
                 - 'monthly_salary' (int): The lowest of the employee salaries across all companies.

    [Return]
    dict: A dictionary containing the global salary statistics, with keys:
          - 'average_salary' (float): The average of salaries across all subsidiary companies combined.
          - 'highest_salary' (int): The highest of employee salaries across all subsidiary companies combined.
          - 'lowest_salary' (int): The lowest of employee salaries across all subsidiary companies combined.

    """

    # Get the list of subsidiary company names
    subsidiaries = list(salary_data.keys())

    # Get all employee salaries across subsidiaries
    if all_salaries := [
        employee['monthly_salary']
        for subsidiary in subsidiaries
        for employee in salary_data[subsidiary]
    ]:
        return {
            "average_salary": sum(all_salaries) / len(all_salaries),
            "highest_salary": max(all_salaries),
            "lowest_salary": min(all_salaries)
        }
    else:
        return {
            "average_salary": 0,
            "highest_salary": 0,
            "lowest_salary": 0
        }
    

def subsidiary_company_statistics(salary_data: dict) -> dict:

    """     
    Calculates the minimum, average, and maximum salaries of all employees in each subsidiary company.

    [Args]
    data (dict): A dictionary with the subsidiary company names as the keys(strings) and a list containing 
                 thier employees details as the values.
                 Within each list are dictionaries containing the following details about each employee:
                 - 'name' (str): The name of the employee.
                 - 'job' (str): The job title of the employee.
                 - 'monthly_salary' (int): The lowest of the employee salaries across all companies.

    [Return]
    dict: A dictionary containing the salary statistics for each subsidiary company, with keys:
          - 'average_salary' (float): The average employee salary in the subsidiary company.
          - 'highest_salary' (int): The highest employee salary.
          - 'lowest_salary' (int): The lowest employee salary.
          - 'employee_salary' (list): A list of the employees details contained in a dictionary. Each dictionary has the following keys:
            - 'name' (str): The name of the employee.
            - 'job' (str): The job title of the employee.
            - 'monthly_salary': The monthly salary of the employee.

    """ 
    # Initialize an empty dictionary to store each subsidiary company statistics
    subsidiary_employee_statistics =  {}

    # Get the list of subsidiary company names
    subsidiaries = list(salary_data.keys())

    # Iterate over each subsidiary company and their employee data
    for subsidiary in subsidiaries:
        if all_employee_salaries := [
            employee['monthly_salary'] for employee in salary_data[subsidiary]
        ]:
            subsidiary_employee_statistics[subsidiary] = {
                "average_salary": sum(all_employee_salaries) / len(all_employee_salaries),
                "highest_salary": max(all_employee_salaries),
                "lowest_salary": min(all_employee_salaries),
                "employee_salary": salary_data[subsidiary]
            }

    return subsidiary_employee_statistics