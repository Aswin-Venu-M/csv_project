# CSV User Data Processing API

This Django REST Framework API processes user data from CSV files, validating and storing the information in a database.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

## API Usage

### Upload CSV File
- **Endpoint**: POST `/api/users/upload/`
- **Content-Type**: `multipart/form-data`
- **File Field**: `file` (must be a .csv file)

The CSV file should have the following columns:
- name (non-empty string)
- email (valid email address)
- age (integer between 0 and 120)

### Response Format
```json
{
    "total_records": 10,
    "successful_records": 8,
    "failed_records": 2,
    "errors": [
        {
            "row": 3,
            "errors": {
                "email": ["Invalid email format"],
                "age": ["Age must be between 0 and 120"]
            }
        }
    ]
}
``` 