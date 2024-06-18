# Simulateur

![Django](https://img.shields.io/badge/Django-3.2-blue)
![React](https://img.shields.io/badge/React-18.3.1-blue)
![Vite](https://img.shields.io/badge/Vite-2.9.9-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue)

## Project Overview

Simulateur is a stock market simulation platform built using Django for the backend and React with Vite for the frontend. The platform allows users to create and manage companies, stocks, and scenarios to simulate stock market events and track their outcomes. It includes an admin interface to manage the simulation settings and control the flow of the simulation.

![Diagram](https://www.plantuml.com/plantuml/dpng/bLLDRzim3BtxLmWvDIjQT5UVMcGhLWpR2YGx6uhCf4BqOL1KqspOVvzanusSA3LooOVvI3wIZ_Iz8uxajIhSHfg68zTCAExS0n7AfITu4jRCvHzWTqNHMjZCweQR7VjRN1kkeMIp5uwF4bHTN2-vs3Yok2lP0jve_rJpjye54BYIFHc2DVJu1gM0AjYbzhfaZyhotaaQIPAhgeKCJS8ZWg6SAJ2aoZSr9wXBzYLyBQI6plYlhs1ELcmYVz6L4a9O1Basts5tjIzlMbnV5ZxWEKR6NQcfNvT80K5lIxgGy9hXhY7RLIVo3RwOKxx1QTO5S7rcc8gRusnBYsYtK5VQ6jWDRHhq4Z0C-KTeuCB6pzPozTi1FgDTIGNJG-BaQSplmz-I_JAmiE7Zu3WzmuG2xy7aOY7J3CDCpLzVmL2sw1gSGDcGj6QWOHbK8MZ806AKYdRDC0IXNAy1gpYHinfSTA2BEFI1psPyvSf3lk9v483YCUGSYAHPkvWwRcRi-ybYHaEt7H9EZ2HrIEO8ccFBIdb1larJ8QTpN0GOZj9UL7p-jDHojPB2AzfL2bv13KDvRAcSsxTdYxIogYDYjoQllrwY5jbUOIxUZupCsxiIx2BTOmaPv73Jfwaik75SHDRVP5jkvDRqH0TwVwSVKWPVeA4c3f5E1SErzIPLS_wqVAJWK1DkW7x2jbKIILB37C8Q0aE3SJL-gQHxWJgp7BabIz8zr5gQMOY9LiM4xbtGWwQSwZnqny0sCuH30TFzBcT0xQMOlgzO1h7eBEqG-tVZvFE4tTomoTtjxMJ_kYbPK9WhKaKbgF0hYYkWkYFAxAherwG59F7w92MJHYXVWyj1qzJZm8JMEBpdEexhxkmuyFZLD-xH7z0Kckbj-4hMl6Glt1MH_4Vs_lzuDpF8V3dZBhdDBnc2i5Yx8XL_GZrtrKicEjpGwoXTkhr1SzpmDMGSCgCSntvAXzF3xy7KNgl_)

## Features

- Create and manage companies with detailed backstories and stock information.
- Simulate stock market events and scenarios.
- Manage teams and user profiles with financial details.
- Admin dashboard to control simulation parameters and monitor progress.
- Secure access and operations restricted to superadmins.

## Requirements

- Python 3.10
- Node.js and npm
- Django 3.2
- React 18.3.1
- Vite 2.9.9

## Installation

### Backend (Django)

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Apply Migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Create a Superuser**:

    ```bash
    python manage.py createsuperuser
    ```

4. **Run the Server**:

    ```bash
    python manage.py runserver
    ```

### Frontend (React with Vite)

1. **Install Dependencies**:

    ```bash
    npm install
    ```

2. **Run Development Server**:

    ```bash
    npm run dev
    ```

3. **Build for Production**:

    ```bash
    npm run build
    ```

## Usage

### Superadmin Commands

To create a superadmin, use the Django management command:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the superadmin credentials.

### Running the Project

1. **Start the Django Server**:

    ```bash
    python manage.py runserver
    ```

2. **Start the Vite Development Server**:

    ```bash
    npm run dev
    ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License