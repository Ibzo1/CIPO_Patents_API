# dd_Full_API

## Overview

**DD Full API** is a unified backend system that provides access to **Patents**, **Industrial Designs**, and **Trademarks** data through standardized APIs, along with a **frontend client** for interacting with these services. <br>

> _Project description placeholder:_  
> _todo_

---

## Repository Structure

This repository contains four main components:

### Backend APIs (Three Lines of Business)

Each line of business is implemented as an independent Django-based API. All APIs follow the same standardized configuration and execution pattern.

1) [📁 Patents API](https://github.com/cipo-research/dd_Full_API/tree/main/dd_patents_API)
2) [📁 Industrial Design API](https://github.com/cipo-research/dd_Full_API/tree/main/dd_industrial_design_API)
3) [📁 Trademarks API](https://github.com/cipo-research/dd_Full_API/tree/main/dd_trademarks_API)

Each API can be run independently and has its own environment configuration, database connection, and documentation.

---

### Frontend Client

The client is the frontend interface used to interact with the backend APIs.
- Frontend Application <br>
  [📁 client](https://github.com/cipo-research/dd_Full_API/tree/main/client)

- Client Documentation:  
  [client/README.md](https://github.com/cipo-research/dd_Full_API/blob/main/client/README.md)

---

## Documentation

### General Documentation

[Standardization Walkthrough](https://github.com/cipo-research/dd_Full_API/blob/main/docs/Standardization_Walkthrough.md)

Covers:
- Environment variable standardization
- Database configuration
- Unified runner (`run.py`)

---

### Technical Documentation

#### Industrial Designs API

- **Technical Documentation**
  - Patents API - Technical Documentation (TODO)
  - [Industrial Design API - Technical Documentation](https://github.com/cipo-research/dd_Full_API/blob/main/dd_industrial_design_API/TECHNICAL_DOCUMENTATION.md)
  - Trademarks API - Technical Documentation (TODO)

Includes system architecture, code structure, and implementation details.

---

## How Everything Fits Together

- Three independent backend APIs provide domain-specific services.
- All backend services use standardized configuration and execution.
- The frontend client consumes the APIs.
- Documentation is split between general setup and service-specific technical details.

---

## Archive

Derived from three archived repositories (retained for reference purposes only):
1) [dd_patents_API](https://github.com/cipo-research/dd_patents_API)
2) [dd_industrial_design_API](https://github.com/cipo-research/dd_industrial_design_API)
3) [dd_TM_API](https://github.com/cipo-research/dd_TM_API)
---

## Contributors

- [Ibraheem Azhar](https://github.com/Ibzo1) - API Head Architect and Developer  
- [Michael Haddad](https://github.com/MichaelHaddad47) - Frontend Lead 
- [Mostafa El-Khouly](https://github.com/mostafa-ek) - Backend Developer  
- [Chloé Arsenault](https://github.com/ChloeA86) - Project Manager
