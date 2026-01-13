# Canadian Patents & Trademarks API - Developer Guide

## Architecture Overview

This is a Django REST API serving Canadian intellectual property data from CIPO (Canadian Intellectual Property Office). The system has **dual-app architecture** with separate apps for patents (`patents/`) and trademarks (`trademarks/`), each with their own PostgreSQL database (though currently unified to single DB).

### Key Data Relationships

- **Patents**: `PT_Main` is the core model with patent numbers as primary keys, related to multiple child tables:
  - `PT_Abstract`, `PT_Claim`, `PT_Disclosure` (patent content)
  - `PT_Interested_Party` (owners/agents), `PT_Priority_Claim` (foreign claims)
  - `PT_IPC_Classification` (classification codes)
- **Trademarks**: `TM_Main` with application numbers, similar relational structure with TM_* models

## Critical Patterns

### API Endpoints Structure
```
/api/pt/pt_main/              # Individual patent records
/api/pt/pt_main_detail/       # Patents with nested related data
/api/pt/pt_abstract/          # Abstract text only
/api/pt/pt_claim/             # Claims only
```

### Dynamic Field Selection
Uses `drf-dynamic-fields` - add `?fields=patent_number,filing_date` to limit response fields. The detail endpoint supports `?include=abstracts,claims` or `?include=all` for nested data control.

### Filtering Patterns
All ViewSets use consistent range filtering:
```python
patent_number_after = django_filters.NumberFilter(field_name='patent_number', lookup_expr='gte')
patent_number_before = django_filters.NumberFilter(field_name='patent_number', lookup_expr='lte')
```

### Database Routing (Currently Disabled)
The `db_router.py` implements multi-database routing - patents to 'default', trademarks to 'trademarks_db'. Currently using unified database in `settings.py`.

## Development Workflows

### Data Import Commands
Located in `patents/management/commands/` and `trademarks/management/commands/`:
```bash
python manage.py import_main          # Import PT_Main data
python manage.py import_abstracts     # Import abstracts
python manage.py run_all_imports      # Batch import all tables
```

Import commands expect ZIP files with pipe-delimited CSV data, handle field mapping through `CSV_TO_MODEL_MAP` dictionaries.

### Running the Server
```bash
python manage.py runserver            # Development server
python serve.py                       # Production-like server
```

### API Documentation
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`
- Schema exports: `/swagger.json`, `/swagger.yaml`

## Model Conventions

### Field Naming
- Foreign keys always point to primary models (e.g., `patent_number` → `PT_Main`)
- Date fields use `_date` suffix, codes use `_code` suffix
- Bilingual fields: `_english` / `_french` suffixes
- Text sequences: `_sequence_number` fields for ordering

### Meta Classes
```python
class Meta:
    unique_together = ('patent_number', 'sequence_field')  # Composite keys
    db_table = 'custom_table_name'                         # Explicit table names
```

### Serializer Patterns
- Base serializers extend `DynamicFieldsMixin`
- Nested serializers for detail endpoints (e.g., `PTAbstractNested`)
- String representation for foreign keys in some serializers

## Key Dependencies

- `django-filter`: Range and search filtering
- `drf-yasg`: OpenAPI schema generation
- `psycopg2-binary`: PostgreSQL adapter
- `drf-dynamic-fields`: Response field selection
- `django-extensions`: Development utilities

## File Organization

- `models.py`: All models for an app in single file
- `serializers.py`: Base + nested serializers
- `views.py`: Main ViewSets with filters
- `views_detail.py`: Special detail endpoints with includes
- `schema.py`: Custom parameter documentation
- `management/commands/`: Data import scripts

## API Query Patterns

### Bulk Data Export
```bash
# Large page sizes for database ingestion (up to 10K records)
?page_size=5000

# Filter out null dates for clean datasets  
?has_filing_date=true&filing_date_after=2020-01-01
```

### Field Selection & Nested Data
```bash
# Limit response fields to reduce bandwidth
?fields=patent_number,filing_date,application_patent_title_english

# Include nested relationships (detail endpoints only)
?include=abstracts,claims,interested_parties
```

## Common Issues & Solutions

1. **Large Response Sizes**: Use `fields` parameter and pagination controls (`page_size`)
2. **Object String IDs**: Text endpoints (`pt_abstract`, `pt_claim`, `pt_disclosure`) now return numeric `patent_number` instead of object strings
3. **Null Date Filtering**: Use `has_filing_date=true` to exclude records with null filing dates
4. **Database Connections**: Check PostgreSQL connection settings in `settings.py`
5. **Import Failures**: Verify CSV field mapping in command files
6. **CORS**: Configured via `django-cors-headers` for API access