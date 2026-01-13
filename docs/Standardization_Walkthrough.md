Standardization Walkthrough
Standardized  configuration and execution for dd_patents_API, 

dd_trademarks_API
, and dd_industrial_design_API.

Changes Made
1. Environment Variables
Each repository now has a 

.env
 file (and 

.env.example
) containing:

DEBUG
SECRET_KEY
ENVIRONMENT
PORT (Specific to each service: 8080, 8082, 8083)
ALLOWED_HOSTS
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
2. Settings Refactoring
The 

DB_Main/settings.py
 file in each repository has been updated to:

Load variables using python-dotenv.
Remove hardcoded secrets and database credentials.
Standardize Filters: Added django_filters to INSTALLED_APPS in all repos.
Standardize Pagination: All repos now use 

FlexiblePageNumberPagination
.
3. Unified Runner Script (

run.py
)
A 

run.py
 script has been added to the root of each repository.

How to Run
You can now run each service independently in separate terminals using the following commands:

Patents API (Port 8080)
cd c:\dd_Full_API\dd_patents_API
# Development (Django Dev Server)
python run.py --dev
# Production (Waitress)
python run.py --prod
# Run Migrations
python run.py --migrate
Trademarks API (Port 8082)
cd c:\dd_Full_API\dd_trademarks_API
# Development (Django Dev Server)
python run.py --dev
# Production (Waitress)
python run.py --prod
# Run Migrations
python run.py --migrate
Industrial Designs API (Port 8083)
cd c:\dd_Full_API\dd_industrial_design_API
# Development (Django Dev Server)
python run.py --dev
# Production (Waitress)
python run.py --prod
# Run Migrations
python run.py --migrate
TIP

You can edit the 

.env
 file in each directory to change settings like DEBUG mode or Database credentials without touching the code.