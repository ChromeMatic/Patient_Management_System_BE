# Patient Management System

Welcome to the **Patient Management System**, a high-performance backend built with **FastAPI**. This system is designed to streamline healthcare workflows by managing patient records efficiently.

---

## 🚀 Getting Started

Follow these steps to set up the project on your local machine.

### Prerequisites

* **Python 3.8+** installed on your system.
* **Docker** and **Docker Compose** (for database management).

---

## 🛠️ Local Installation

### 1. Set Up a Virtual Environment

It is recommended to use a virtual environment to keep dependencies isolated.

**Install virtualenv:**

```bash
pip install virtualenv

```

**Create the environment:**

```bash
virtualenv venv

```

**Activate the environment:**

* **Windows:**
```bash
venv\Scripts\activate

```


* **Linux / macOS:**
```bash
source venv/bin/activate

```


### 2. Install Dependencies

Once the virtual environment is active, install the required packages:

```bash
pip install -r requirements.txt

```

---

## 🐳 Docker Setup

This project uses **PostgreSQL** for the database and **pgAdmin** for database management, orchestrated via Docker Compose.

### Step 1: Install Docker

If you don't have Docker installed, follow these steps:

1. **Download:** Visit the [Docker Desktop website](https://www.docker.com/products/docker-desktop/) and download the installer for your OS.
2. **Install:**
* **Windows/macOS:** Run the installer and follow the wizard. (Windows users: Ensure "Use the WSL 2 based engine" is checked).
* **Linux:** Follow the specific [distribution guide](https://www.google.com/search?q=https://docs.docker.com/desktop/setup/install/linux-install/) (e.g., Ubuntu, Debian).


3. **Verify:** Open your terminal and run:
```bash
docker --version
docker-compose --version

```



### Step 2: Run the Infrastructure

Since the `docker-compose.yml` file is already provided, you can start the PostgreSQL database and pgAdmin with a single command:

```bash
docker-compose up -d

```

* **PostgreSQL:** Usually accessible on `localhost:5432`.
* **pgAdmin:** Usually accessible on `localhost:5050` (or the port defined in your file).

---

## 🚦 Running the Application

After setting up the database and the environment, start the FastAPI server:

```bash
fastapi dev mian.py   

```

The API documentation will be available at: `http://127.0.0.1:8000/docs`
