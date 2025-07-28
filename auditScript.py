import pandas as pd

terminated = pd.read_csv('terminated_employees_clean.csv')
access = pd.read_csv('user_access_logs_clean.csv')

print("Data loaded successfully.")

terminated['termination_date'] = pd.to_datetime(terminated['termination_date'])
access['last_login'] = pd.to_datetime(access['last_login'])

print("Data types converted successfully.")

merged = pd.merge(access, terminated, left_on='user_id', right_on='employee_id',how='inner')

print("Data merged successfully.")

if {'user_id', 'employee_id', 'last_login', 'termination_date'}.issubset(merged.columns):
    violations = merged[
        (merged['user_id'] == merged['employee_id']) &
        (merged['last_login'] > merged['termination_date'])
    ]
else:
    print("Error: Required columns not found in merged DataFrame.")
    violations = pd.DataFrame()

if not violations.empty:
    print("Access violations found:")
    print(violations.shape)
    print(violations[['user_id', 'employee_id', 'last_login', 'termination_date']])

violations.to_csv('access_violations.csv', index=False)