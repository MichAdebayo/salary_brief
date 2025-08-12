from load_data import load_employee_data
from salary_accounting import calculate_monthly_salaries, global_company_statistics, subsidiary_company_statistics
from display_results import print_statistics
from export_data import generate_csv

if __name__ == "__main__":
    # Load employee data
    employee_data = load_employee_data()
    # Calculate global employee salaries
    global_employee_salaries = calculate_monthly_salaries(employee_data)
    # Calculate global salary statistics
    global_statistics = global_company_statistics(global_employee_salaries)
    # Calculate subsidiary salary statistics
    subsidiary_statistics = subsidiary_company_statistics(global_employee_salaries)
    # Print subsidiary salary statistics
    print_statistics(subsidiary_statistics)
    # Generate CSV
    generate_csv(subsidiary_statistics)