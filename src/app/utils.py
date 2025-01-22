import pandas as pd

def validate_tables_schema(df, target_schema):
    """
    Valida que las columnas de un DataFrame coincidan con el esquema objetivo.
    """
    if len(df.columns) != len(target_schema):
        return False
    return True

def process_data_employees(df, target_schema):
    """
    Procesa un DataFrame de empleados y lo transforma para coincidir con el esquema objetivo.
    """
    df.columns = target_schema
    df['name'] = df['name'].fillna('NULL') 
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce').fillna(pd.to_datetime('1900-01-01T00:00:00Z'))
    df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype('Int64')
    df['department_id'] = df['department_id'].fillna('0')
    df['job_id'] = df['job_id'].fillna('0')

    data = df[['id', 'name', 'datetime', 'department_id', 'job_id']].where(pd.notnull(df), None).values.tolist()

    return data
