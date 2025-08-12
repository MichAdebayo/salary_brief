import csv

def generate_csv(subsidiary_statistics, filename='salary_statistics_3_subsidiaries.csv'):

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header for individual salaries
        writer.writerow(['Company', 'Employee Name', 'Job Title', 'Monthly Salary (€)'])

        # Write the individual salary data
        for subsidiary, stats in subsidiary_statistics.items():
            if "employee_salary" in stats and stats["employee_salary"]:
                for employee in stats["employee_salary"]:
                    writer.writerow([subsidiary, employee["name"], employee["job"], round(employee["monthly_salary"], 2)])

        # Add a blank row
        writer.writerow([])

        # Write the header for salary statistics
        writer.writerow(['Company', 'Average Salary (€)', 'Highest Salary (€)', 'Lowest Salary (€)'])

        # Write the salary statistics data
        for subsidiary, stats in subsidiary_statistics.items():
            writer.writerow([subsidiary, round(stats['average_salary'], 2), stats['highest_salary'], stats['lowest_salary']])

    print(f'CSV file "{filename}" generated successfully.')