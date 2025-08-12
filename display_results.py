def print_statistics(subsidiary_data: dict) -> None:
    """     
    Prints the salary statistics for each subsidiary company, including individual employee details and 
    company-specific salary statistics.

    [Args]
    data (dict): A dictionary with the subsidiary company names and parent company name as the keys(strings) and a
                 dictionary as the value. Within each dictionary 'values' are the following keys:
                 - 'average_salary' (float): The average salary of the subsidiary or parent company.
                 - 'highest_salary' (int): The maximum salary earned in the subsidiary or parent company.
                 - 'lowest_salary' (int): The job title of the employee.
                 - 'employee_salary': A list with dictionaries. The keys for this list are:
                    - 'name' (str): The name of the employee.
                    - 'job' (str): The job title of the employee.
                    - 'monthly_salary' (int): The monthly salary of the employee.

    [Return]
    None: This function prints the statistics to the console and does not return a value.

    """ 
    
    # Loop through each company and its statistics in the aggregated data
    for company, statistics in subsidiary_data.items():
        print(f"Entreprise: {company}")

        # Check if "employee_details" key exists and is not empty
        if 'employee_salary' in statistics and statistics['employee_salary']:
            # Sort employee details by salary in descending order
            sorted_employee_details = sorted(statistics['employee_salary'], key=lambda x: x['monthly_salary'], reverse=True)

            # Print each employee's details with formatted columns
            for employee in sorted_employee_details:
                print(f'{employee['name']:<10} | {employee['job']:<15} | Salaire mensuel: {employee['monthly_salary']:.2f}€')

        # # Print company-specific salary statistics
        print("\n========================================================")
        print(f"Statistiques des salaires pour l'entreprise {company}:")
        print(f"Salaire moyen: {statistics['average_salary']:.2f}€")
        print(f"Salaire le plus élevé: {statistics['highest_salary']:.2f}€")
        print(f"Salaire le plus bas: {statistics['lowest_salary']:.2f}€")
        print("========================================================\n")