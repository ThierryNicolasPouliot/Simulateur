# Simulateur

![Django](https://img.shields.io/badge/Django-3.2-blue)
![React](https://img.shields.io/badge/React-18.3.1-blue)
![Vite](https://img.shields.io/badge/Vite-2.9.9-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue)

## Project Overview

Simulateur is a stock market simulation platform built using Django for the backend and React with Vite for the frontend. The platform allows users to create and manage companies, stocks, and scenarios to simulate stock market events and track their outcomes. It includes an admin interface to manage the simulation settings and control the flow of the simulation.

![Diagram](//www.plantuml.com/plantuml/dpng/ZLJBRjim4BppAmYVOWW9qgjEATe6BOgc0QoU1PfQEOJv4CXb0hVeltTfsHJLo80lfYNkpimEXte8A3n6erdOApi8BmoNMeJm4T6hRKJu9ftTgD_0xnaxxl1FpWp27lWVLbbXeEORAhKxLcs5t0Tq_f1V_JtrqBEJ-zGXn-QQFpeFQcU_m-7c1BXc5Igv1pyX3bv9e5hj1BAAaB2DGoSGkff_fgLH1YQI1eHvhyg0sO8FDVz178rBluyAT7VpAu1_zgvN6jOJIF4sOSMGzFoqq3ZwcHhNQLmjR24FYNusLz9J86-KYLgW8Zy1aRI5H80qWcy3mb3pfvYaighNKM8ybhPUu4G1hs2nvbzeIOHUxNP9NZF-AQWaME6LU-z61q5wDIJenOFBTQhlbOmQ3wqcLbtiH7zKbkLcrcVdiNTwf7LlTj6vRAxpV3Ie2YaS2mTq34rXOEE53K8cyg_gg3SH3MVMcVTPIqhLrDVYOIZS4CP5YzdUUTnIpfPYzWHlfvD3NM19Pn4i5k6DMwt22tJj76b-Z1btVBpon9GPQA1vBcQpNPH_3ijLH3bZ9NRnzbNek9pEfTYJ5a6qj7F-XAm-hFZjBL_TtzsjJj-8cbDo0YkJKbJHlnGQgXglDNSzos5F1GNUcQJcoaeTQRoBfGbpgIvJqx9mVOkEXTrokEpwzIsZZqN3eYUqvAXJxOi8B3_dAKk32y3BbGithUOUfFDTOAEk_phIfIYXp_EMPSLCfm05Da_7LJfY8Fm7i5qq-Xy0)


![Diagram](https://www.plantuml.com/plantuml/dpng/NP5DRiCW48Ntd6AKLRBe1Iov2f7ODSeY1x2cUEICYWU4iVfp-WAncpeRMthV6zvZE4u9Ovf7fz0c7q7t8uiAMMFB0IN1xihZx32nbpCA3XHtW1DSpqykIuAH_HrkcVcoDvI1AZDRfWUIL87UWaliAPwy_wZmSbAgTeENrvpTGEtTJN_Tzeb7wcRXT53NStLb4wKv_3TbLf1fm4R2H9qlATrxZfbMg1lWV0oZun_giFGhJA_9LO4ytdyhrRRms0-yUH-WRPKh_yyREu8uYx0C2W3oz79-tlN-K2Mzr0aExT9cNxztR0g-d1eOCTdRbfFqQhcgAVlmJpSrQ-67Mbs1UdNCm_dHVm40)
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

### Running the Daphne Server for ASGI

To run the Daphne server with the ASGI application, use the following command:

```bash
daphne -p 8000 simulateur.asgi:application
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License

## Data

The project includes the following CSV files for initial data setup:

```plaintext
.
├── data
│   ├── companies.csv
│   ├── cryptocurrencies.csv
│   ├── custom_stats.csv
│   ├── events.csv
│   ├── portfolios.csv
│   ├── scenarios.csv
│   ├── simulation_settings.csv
│   ├── stocks.csv
│   ├── teams.csv
│   ├── transaction_history.csv
│   ├── triggers.csv
│   └── users.csv
```

## File Structure

Here is a brief overview of the project file structure:

```plaintext
.
├── Dockerfile
├── data
├── db.sqlite3
├── docker-compose.yml
├── manage.py
├── package-lock.json
├── package.json
├── requirements.txt
├── simulateur
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── simulation
│   ├── admin.py
│   ├── apps.py
│   ├── channels
│   │   ├── consumers.py
│   │   └── routing.py
│   ├── decorators.py
│   ├── logic
│   │   ├── event_handlers.py
│   │   ├── price_update.py
│   │   ├── queue.py
│   │   ├── simulation_manager.py
│   │   ├── transactions.py
│   │   └── utils.py
│   ├── management
│   │   ├── commands
│   │   │   ├── clean_database.py
│   │   │   ├── seed_database.py
│   │   │   ├── start_simulation.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── templates
│   │   └── simulation
│   │       ├── admin_dashboard.html
│   │       ├── buy_sell.html
│   │       ├── graph.html
│   │       ├── home.html
│   │       ├── market_overview.html
│   │       ├── team_dashboard.html
│   │       └── user_dashboard.html
│   ├── tests.py
│   ├── urls.py
│   └── views
│       ├── auth_views.py
│       ├── company_views.py
│       ├── dashboard_views.py
│       ├── event_views.py
│       ├── portfolio_views.py
│       ├── scenario_views.py
│       ├── simulation_graph_views.py
│       └── simulation_views.py
├── staticfiles
└── staticfiles.json
```

## Run the Complete System

To run the complete system, you can use Docker Compose for setting up the entire environment with one command:

```bash
docker-compose up --build
```

This command will build and start the Django and Vite servers along with any other required services defined in the `docker-compose.yml` file.
