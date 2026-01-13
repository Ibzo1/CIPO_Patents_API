# Industrial Design API - Technical Documentation

## 1. Executive Summary

The Industrial Design API is a Django REST Framework-based web service that provides read-only access to Canadian Industrial Design registration data from the Canadian Intellectual Property Office (CIPO). The API exposes comprehensive industrial design application and assignment information through RESTful endpoints with built-in filtering, search, and pagination capabilities.

**Key Technologies:**
- Django 5.1.1
- Django REST Framework 3.14.0
- PostgreSQL Database
- drf-yasg (Swagger/OpenAPI documentation)
- Waitress WSGI Server

---

## 2. Project Purpose

This API serves as a data access layer for industrial design information, enabling:
- Programmatic access to industrial design applications and registrations
- Search and filter capabilities across multiple data dimensions
- Integration with external systems requiring industrial design data
- Support for applications needing Canadian IP data

The system is designed as a read-only API, ensuring data integrity while providing flexible query capabilities.

---

## 3. System Architecture

### 3.1 Application Structure

```
dd_industrial_design_API/
├── DB_Main/                    # Django project configuration
│   ├── settings.py            # Application settings
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
├── industrial_designs/         # Main application
│   ├── models.py              # Database models
│   ├── views.py               # API viewsets
│   ├── serializers.py         # Data serializers
│   ├── urls.py                # URL routing
│   └── migrations/            # Database migrations
├── serve.py                   # Production server entry point
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

### 3.2 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | Django | 5.1.1 | Core application framework |
| API Framework | Django REST Framework | 3.14.0 | RESTful API implementation |
| Database | PostgreSQL | - | Primary data storage |
| Database Adapter | psycopg2-binary | 2.9.10 | PostgreSQL connectivity |
| API Documentation | drf-yasg | 1.21.7 | Swagger/OpenAPI docs |
| Filtering | django-filter | 23.1 | Advanced query filtering |
| Production Server | Waitress | - | WSGI HTTP server |
| CORS Support | django-cors-headers | 4.6.0 | Cross-origin requests |

### 3.3 Database Configuration

**Database:** `IndustrialDesign`
**Schema:** `id_csv_2024_03_07`
**Connection Details:**
- Host: localhost
- Port: 5432
- User: Azhari

All models utilize the unmanaged model pattern (`managed = False`), meaning Django does not control database schema creation or migrations. The database schema is maintained externally.

---

## 4. Data Models

The system contains 10 primary models organized into two categories:

### 4.1 Application Models

#### ApplicationMain
The primary model containing core industrial design application information.

**Key Fields:**
- `application_number` - Unique application identifier
- `design_title` - Title of the design
- `design_status` - Current status of the application
- `filing_date` - Date application was filed
- `publication_date` - Date design was published
- `registration_date` - Date design was registered
- `registration_number` - Assigned registration number
- `registration_expiry_date` - When registration expires
- `priority_date` - Priority claim date
- `international_registration_number` - Hague system number

#### ApplicationClassification
Product classification information for applications.

**Key Fields:**
- `application_number` - Links to ApplicationMain
- `classification_number` - International classification code
- `classification_kind` - Type of classification
- `product_description` - Description of the product

#### ApplicationInterestedParty
Parties involved in the application (owners, designers, agents).

**Key Fields:**
- `application_number` - Links to ApplicationMain
- `first_name`, `last_name` - Individual names
- `organization_name` - Company/organization
- `role` - Role in application (owner, designer, agent)
- `address`, `city`, `province_state`, `postal_code` - Contact information
- `country`, `country_code` - Country information

#### ApplicationImage
Image assets associated with applications.

**Key Fields:**
- `application_number` - Links to ApplicationMain
- `filename` - Image file identifier
- `colour`, `colour_type` - Color information
- `image_kind`, `image_kind_code` - Type of image

#### ApplicationDescription
Textual descriptions of industrial designs.

**Key Fields:**
- `application_number` - Links to ApplicationMain
- `design_description` - Full text description
- `design_description_language_code` - Language of description
- `design_description_text_sequence_number` - Ordering sequence

#### ApplicationDescriptionTxtFormat
Alternative text-formatted descriptions.

**Key Fields:**
- Similar to ApplicationDescription but with different formatting

#### ApplicationCorrection
Records corrections made to published applications.

**Key Fields:**
- `application_number` - Links to ApplicationMain
- `correction_date` - When correction was made
- `publication_identifier` - Reference to publication
- `publication_section` - Section being corrected

### 4.2 Assignment Models

#### AssignmentMain
Records of ownership transfers and assignments.

**Key Fields:**
- `assignment_number` - Unique assignment identifier
- `application_number` - Links to ApplicationMain
- `assignment_type`, `assignment_type_code` - Type of assignment
- `assignment_status` - Current status
- `assignment_registration_date` - When recorded
- `ownership_change_prior_to_filing` - Pre-filing ownership changes

#### AssignmentInterestedParty
Parties involved in assignments (assignors/assignees).

**Key Fields:**
- `assignment_number` - Links to AssignmentMain
- `first_name`, `last_name` - Individual names
- `organization_name` - Company/organization
- `role`, `role_code` - Role in assignment
- Address and location fields

#### AssignmentCorrection
Corrections to published assignments.

**Key Fields:**
- `assignment_number` - Links to AssignmentMain
- `correction_date` - When correction was made
- `publication_identifier`, `publication_section` - Publication references

---

## 5. API Endpoints

All endpoints are prefixed with `/api/` and support standard REST operations (GET only).

### 5.1 Base Endpoints

| Endpoint | Purpose | Model |
|----------|---------|-------|
| `/api/main/` | Core application data | ApplicationMain |
| `/api/application_classification/` | Product classifications | ApplicationClassification |
| `/api/application_correction/` | Application corrections | ApplicationCorrection |
| `/api/application_description/` | Design descriptions | ApplicationDescription |
| `/api/application_description_txt_format/` | Text-format descriptions | ApplicationDescriptionTxtFormat |
| `/api/application_image/` | Image metadata | ApplicationImage |
| `/api/application_interested_party/` | Application parties | ApplicationInterestedParty |
| `/api/assignment_main/` | Assignment records | AssignmentMain |
| `/api/assignment_interested_party/` | Assignment parties | AssignmentInterestedParty |
| `/api/assignment_correction/` | Assignment corrections | AssignmentCorrection |

### 5.2 Standard Operations

Each endpoint supports:

#### List View
```
GET /api/main/
```
Returns paginated list of records.

#### Detail View
```
GET /api/main/{id}/
```
Returns single record by ID.

#### By Number Lookup
```
GET /api/main/by-number/{application_number}/
```
Returns all records matching application/assignment number.

### 5.3 Query Parameters

#### Filtering
- **Field-based filters**: `?field_name=value`
- **Date range filters**:
  - `?filing_date_after=2023-01-01`
  - `?filing_date_before=2024-12-31`
- **Numeric range filters**: `?id_after=1000&id_before=2000`

#### Search
```
?search=keyword
```
Searches across all text fields defined in the viewset's `search_fields`.

#### Ordering
```
?ordering=field_name
?ordering=-field_name  # Descending
```

#### Omit Filter
```
?omit=keyword
?omit=field:keyword    # Field-specific exclusion
?omit=word1,word2      # Multiple keywords
```
Excludes records containing specified keywords.

### 5.4 API Documentation

Interactive documentation available at:

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **OpenAPI JSON**: `/swagger.json`
- **OpenAPI YAML**: `/swagger.yaml`

### 5.5 Health Check

```
GET /health/
```
Returns: `{"status": "ok"}`

---

## 6. API Usage Examples

### 6.1 Basic Queries

**Get all applications:**
```bash
curl http://api.opic-cipo.ca/api/main/
```

**Get specific application by ID:**
```bash
curl http://api.opic-cipo.ca/api/main/12345/
```

**Get application by application number:**
```bash
curl http://api.opic-cipo.ca/api/main/by-number/123456/
```

### 6.2 Search and Filter

**Search for applications:**
```bash
curl "http://api.opic-cipo.ca/api/main/?search=furniture"
```

**Filter by date range:**
```bash
curl "http://api.opic-cipo.ca/api/main/?filing_date_after=2024-01-01&filing_date_before=2024-12-31"
```

**Filter and sort:**
```bash
curl "http://api.opic-cipo.ca/api/main/?design_status=Registered&ordering=-filing_date"
```

**Exclude specific keywords:**
```bash
curl "http://api.opic-cipo.ca/api/main/?omit=abandoned"
```

### 6.3 Related Data Queries

**Get all parties for an application:**
```bash
curl "http://api.opic-cipo.ca/api/application_interested_party/?application_number=123456"
```

**Get classifications for an application:**
```bash
curl "http://api.opic-cipo.ca/api/application_classification/?application_number=123456"
```

**Get all assignments for an application:**
```bash
curl "http://api.opic-cipo.ca/api/assignment_main/?application_number=123456"
```

---

## 7. Installation and Setup

### 7.1 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip package manager
- Virtual environment (recommended)

### 7.2 Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd dd_industrial_design_API
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure database:**
Edit `DB_Main/settings.py` with your PostgreSQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'IndustrialDesign',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
```

5. **Test the configuration:**
```bash
python manage.py check
```

6. **Run development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## 8. Configuration

### 8.1 Key Settings

**Debug Mode** (settings.py:169)
```python
DEBUG = True  # Set to False in production
```

**Allowed Hosts** (settings.py:223)
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'api.opic-cipo.ca']
```

**Pagination** (settings.py:174-175)
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}
```

**CORS Settings**
If using django-cors-headers, add to settings:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]
```

---

## 9. Deployment

### 9.1 Production Server

The application uses Waitress as the production WSGI server.

**Start production server:**
```bash
python serve.py
```

Server configuration (serve.py):
- Host: 0.0.0.0 (all interfaces)
- Port: 8080

### 9.2 Production Checklist

1. Set `DEBUG = False` in settings.py
2. Configure appropriate `ALLOWED_HOSTS`
3. Set secure `SECRET_KEY`
4. Configure static file serving
5. Set up SSL/TLS certificates
6. Configure firewall rules
7. Set up database backups
8. Configure logging and monitoring
9. Set appropriate file permissions
10. Use environment variables for sensitive data

### 9.3 Reverse Proxy Configuration

Example Nginx configuration:
```nginx
server {
    listen 80;
    server_name api.opic-cipo.ca;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 10. Code Architecture

### 10.1 Custom Filter Backend

**OmitFilterBackend** (views.py:35-66)

Custom Django filter that excludes records containing specified keywords. Supports:
- Simple keyword exclusion: `?omit=keyword`
- Field-specific exclusion: `?omit=field:keyword`
- Multiple keywords: `?omit=word1,word2`

### 10.2 Dynamic FilterSet Generation

**make_ab_filterset()** (views.py:75-89)

Dynamically generates Django FilterSet classes with `_after` and `_before` range filters for date and numeric fields. This provides automatic date/numeric range filtering without manual configuration.

### 10.3 ReadOnlyMixin

**ReadOnlyMixin** (views.py:91-113)

Base viewset providing:
- Read-only operations (list, retrieve)
- Dynamic filterset generation
- Ordering and search capabilities
- Custom `by-number` lookup endpoint

All viewsets inherit from this mixin to ensure consistent behavior.

---

## 11. Database Schema Details

### 11.1 Schema Naming
All tables reside in the PostgreSQL schema: `id_csv_2024_03_07`

### 11.2 Indexing
Primary indexes exist on:
- `id` (primary key) on all tables
- `application_number` on application-related tables
- `assignment_number` on assignment-related tables

### 11.3 Data Types
- Text fields: `TextField` (unlimited length)
- Dates: `DateField` (YYYY-MM-DD format)
- IDs: `BigAutoField` (64-bit integers)

---

## 12. Security Considerations

### 12.1 Current Configuration
- **Authentication**: None (public read-only API)
- **CORS**: Configured for specific domains
- **SQL Injection**: Protected by Django ORM
- **XSS**: JSON-only responses (no HTML rendering)

### 12.2 Recommendations
1. Implement rate limiting for production
2. Add API key authentication for tracking usage
3. Enable HTTPS only
4. Implement request logging
5. Set up monitoring and alerting
6. Regular security updates

---

## 13. Maintenance and Support

### 13.1 Logs
Django logging configured for database queries (settings.py:263-277).

View logs for debugging database interactions.

### 13.2 Database Updates
Since models are unmanaged (`managed = False`), schema changes must be performed directly on the PostgreSQL database.

### 13.3 Common Tasks

**Check API health:**
```bash
curl http://localhost:8000/health/
```

**View available routes:**
```bash
python manage.py show_urls  # Requires django-extensions
```

**Test database connection:**
```bash
python manage.py dbshell
```

---

## 14. Troubleshooting

### 14.1 Common Issues

**Database Connection Errors:**
- Verify PostgreSQL is running
- Check credentials in settings.py
- Ensure database exists: `IndustrialDesign`
- Verify user permissions

**Import Errors:**
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

**404 on API Endpoints:**
- Verify URL includes `/api/` prefix
- Check swagger documentation for exact paths

**Empty Results:**
- Verify database contains data
- Check schema name matches: `id_csv_2024_03_07`
- Review filter parameters

---

## 15. API Response Format

### 15.1 List Response
```json
{
  "count": 1500,
  "next": "http://api.opic-cipo.ca/api/main/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "application_number": "123456",
      "design_title": "Furniture Design",
      ...
    }
  ]
}
```

### 15.2 Detail Response
```json
{
  "id": 1,
  "application_number": "123456",
  "design_title": "Furniture Design",
  "design_status": "Registered",
  "filing_date": "2024-01-15",
  ...
}
```

### 15.3 Error Response
```json
{
  "detail": "Not found."
}
```

---

## 16. Performance Considerations

### 16.1 Pagination
Default page size: 50 records. Adjust via `PAGE_SIZE` in settings.py.

### 16.2 Database Optimization
- Indexed fields: `application_number`, `assignment_number`
- Use field-specific filters for better performance
- Limit result sets with date ranges

### 16.3 Caching
Consider implementing:
- Redis for query caching
- HTTP caching headers
- Database query result caching

---

## 17. Knowledge Transfer Notes

### 17.1 Key Understanding Points

1. **Read-Only Nature**: API provides only GET operations. No data modification capabilities.

2. **Unmanaged Models**: Database schema is controlled externally, not by Django migrations.

3. **Schema Organization**: All data resides in PostgreSQL schema `id_csv_2024_03_07`.

4. **Filtering Architecture**: Three-tier filtering system:
   - Django Filter (field-based)
   - Search (text search)
   - Omit (exclusion filtering)

5. **Number Lookups**: Special endpoint pattern `/by-number/{number}/` for application/assignment number queries.

### 17.2 Development Workflow

1. **Making Changes**: Modify views, serializers, or add endpoints in industrial_designs app
2. **Testing**: Use Swagger UI at `/swagger/` for interactive testing
3. **Deployment**: Run `python serve.py` for production deployment

### 17.3 Extension Points

To add new endpoints:
1. Define model in `models.py` (set `managed = False`)
2. Create serializer in `serializers.py`
3. Create viewset in `views.py` (inherit from `ReadOnlyMixin`)
4. Register in `urls.py` router

---

## Document Information

- **Document Version**: 1.0
- **Last Updated**: 2025-11-25
- **Project Repository**: dd_industrial_design_API
- **Database Schema Version**: id_csv_2024_03_07

---

## Appendix A: Full API Endpoint Reference

| HTTP Method | Endpoint Pattern | Description |
|-------------|-----------------|-------------|
| GET | `/health/` | API health check |
| GET | `/swagger/` | Interactive API documentation |
| GET | `/redoc/` | Alternative API documentation |
| GET | `/api/main/` | List all applications |
| GET | `/api/main/{id}/` | Get application by ID |
| GET | `/api/main/by-number/{app_num}/` | Get application by number |
| GET | `/api/application_classification/` | List classifications |
| GET | `/api/application_classification/{id}/` | Get classification by ID |
| GET | `/api/application_classification/by-number/{app_num}/` | Get classifications by app number |
| GET | `/api/application_correction/` | List corrections |
| GET | `/api/application_correction/{id}/` | Get correction by ID |
| GET | `/api/application_description/` | List descriptions |
| GET | `/api/application_description/{id}/` | Get description by ID |
| GET | `/api/application_description_txt_format/` | List text descriptions |
| GET | `/api/application_description_txt_format/{id}/` | Get text description by ID |
| GET | `/api/application_image/` | List images |
| GET | `/api/application_image/{id}/` | Get image by ID |
| GET | `/api/application_interested_party/` | List interested parties |
| GET | `/api/application_interested_party/{id}/` | Get party by ID |
| GET | `/api/assignment_main/` | List assignments |
| GET | `/api/assignment_main/{id}/` | Get assignment by ID |
| GET | `/api/assignment_main/by-number/{assign_num}/` | Get assignment by number |
| GET | `/api/assignment_interested_party/` | List assignment parties |
| GET | `/api/assignment_interested_party/{id}/` | Get assignment party by ID |
| GET | `/api/assignment_correction/` | List assignment corrections |
| GET | `/api/assignment_correction/{id}/` | Get assignment correction by ID |

---

## Appendix B: Environment Variables

For production deployments, consider using environment variables:

```bash
export DJANGO_SECRET_KEY='your-secret-key'
export DB_NAME='IndustrialDesign'
export DB_USER='your-username'
export DB_PASSWORD='your-password'
export DB_HOST='localhost'
export DB_PORT='5432'
export DEBUG='False'
export ALLOWED_HOSTS='api.opic-cipo.ca,localhost'
```

Load in settings.py:
```python
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

---

*End of Technical Documentation*
