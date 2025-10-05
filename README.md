# search-api

A FastAPI-based web service that helps find hotels within a specified radius of events and calculates travel times using different transportation modes.

## Quick Start

### Prerequisites

- Python 3.13+
- Docker
- Minikube
- Tilt
- kubectl

### Setup (Recommended)

The easiest way to run the development environment is using Tilt with Minikube:

1. Clone the repository:
```bash
git clone git@github.com:WDoyle123/search-api.git
cd search-api
```

2. Start the development environment:
```bash
./scripts/start-dev.sh
```

This script will:
- Check and start Minikube with the profile `search-api`
- Create the necessary Kubernetes namespace
- Set up port forwarding for API (8000) and database (5432)
- Launch Tilt for hot-reloading development

The application will be available at:
- **API**: http://localhost:8000
- **Database**: localhost:5432

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/v1/docs
- **ReDoc**: http://localhost:8000/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/v1/openapi.json

## API Endpoints

### Search Hotels

```http
GET /v1/search?event_id=1&radius_km=10&modes=walking,driving&sort_by=travel_time
```

**Parameters:**
- `event_id` (required): ID of the event to search around
- `radius_km` (optional, default=10): Search radius in kilometers (1-100)
- `modes` (optional, default="walking"): Comma-separated travel modes
- `sort_by` (optional, default="travel_time"): Sort by "distance" or "travel_time"

**Supported Travel Modes:**
- `walking`
- `driving` 
- `public_transport`

### List All Hotels

```http
GET /v1/search/hotels
```

### List All Events

```http
GET /v1/search/events
```

## Example Response

```json
[
  {
    "hotelID": 102,
    "latitude": 51.5094,
    "longitude": -0.1183,
    "distance_km": 1.1,
    "estimated_travel": {
      "driving": 132,
      "public_transport": 638,
      "walking": 792
    }
]
```

## Development

### Development Dependencies

```bash
pip install -r dev-requirements.txt
```

### Running Tests

```bash
pytest
```

### Tilt Development

The project uses Tilt for Kubernetes-based development with live reloading:

- **Tiltfile**: Configures Docker builds with live updates
- **Hot Reloading**: Changes to `app/` directory trigger automatic rebuilds
- **Port Forwarding**: Automatic port forwarding for API (8000) and database (5432)
- **Kubernetes**: Full deployment in Minikube for production-like environment

## Project Structure

```
.
├── app/
│   ├── calculations/    # Travel time and distance calculations
│   ├── routes/          # API route definitions
│   ├── config.py        # Configuration settings
│   ├── db.py            # Database connection and session management
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # SQLAlchemy database models
│   └── schemas.py       # Pydantic models for request/response
├── manifests/           # Kubernetes deployment manifests
│   └── base/            # Base Kubernetes configurations
├── scripts/
│   └── start-dev.sh     # Development environment startup script
├── tests/               # Test suite
├── requirements.txt     # Production dependencies
├── dev-requirements.txt # Development dependencies
├── Tiltfile             # Tilt configuration for development
└── Dockerfile           # Container configuration
```
