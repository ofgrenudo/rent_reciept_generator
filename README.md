# Rent Receipt Generator

This web application facilitates quick and easy generation of rent payment receipts in PDF format. It was also developed as a practical project to learn Python’s FastAPI framework, as well as use tailwind css. I pretty much just plan on keeping this running on my home network. But others find it and decide its useful that's cool.

## Features

- User-friendly form for entering rent payment details
- Generates professional PDF receipts with tenant and landlord information
- Supports signatures and date formatting
- Dark mode interface with integrated Flatpickr date picker
- Can run locally or within a Docker container

## Requirements

Install the required Python packages:

```bash
pip install fastapi uvicorn python-multipart jinja2
```

### Running Locally
Use Poetry to start the application:

```bash
poetry run uvicorn main:app --reload --port 1234
```

Access the app at http://localhost:1234.

### Running with Docker
Build and run the Docker container:

```bash
docker build -t rent-receipt-app .
docker run -p 1234:1234 rent-receipt-app
```

Open http://localhost:1234 to use the application.
