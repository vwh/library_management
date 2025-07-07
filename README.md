# Odoo Library Management System

This project is a custom Odoo module for managing a library, including books, authors, and a borrowing system. It is built for Odoo 18 and demonstrates best practices for custom addon development.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Development Setup](#development-setup)
- [Screenshots](#screenshots)

## Features

- **Book Management**: Create and manage a catalog of books with titles, authors, descriptions, and publish dates.
- **Author Management**: Maintain a database of authors and see a list of all books they have written.
- **Borrowing System**: 
    - Record book borrowings, linking a book to a borrower (Odoo contact).
    - Automatically calculates a return date (7 days from borrowing).
    - A clear button to mark books as returned.
    - A filter to quickly see which books are currently borrowed.
- **Clear Navigation**: All features are accessible under a top-level "Library" menu in the Odoo UI.


## Project Structure

```
project/
├── custom_addons/            # Custom modules directory
│   └── library_management/   # Main library module
├── odoo/                     # Core Odoo 18 source
├── venv/                     # Python virtual environment
```

## Prerequisites

- **OS**: Ubuntu 20.04+ (or compatible Linux distribution)
- **Python**: 3.10 or higher
- **Database**: PostgreSQL 12+
- **Version Control**: Git

## Installation

### 1. Clone the Odoo Source

It is assumed you have already cloned the Odoo 18 source code into the `odoo/` directory.

### 2. Install System Dependencies

Before installing Python packages, you must install the required system-level libraries for Odoo. The Odoo source code includes a helpful script for this on Debian-based systems (like Ubuntu).

```bash
sudo sh odoo/setup/debinstall.sh
```

### 3. Set Up the Virtual Environment

It is highly recommended to use a Python virtual environment to isolate project dependencies.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install Odoo's Python dependencies
pip install -r odoo/requirements.txt
```

### 4. Create the Database

Ensure your PostgreSQL user has create permissions, then create a new database for this project.

```bash
createdb odoo-dev
```

### 5. Clone the Custom Addon

This project's custom module is available in a separate repository. Clone it and move it contents to root directory so Odoo can find it.

```bash
git clone https://github.com/vwh/library_management
mv library_management/* .
```

## Running the Application

After the initial installation, you can start the server for daily development using this command:

```bash
./odoo/odoo-bin -d odoo-dev --addons-path=odoo/addons,custom_addons --dev=all
```

### Access the Application

Once started, access your Odoo instance at:
- **URL**: `http://localhost:8069`
- **Database**: `odoo-dev`
- **Default Admin**: `admin` / `admin`

## Development Setup

### VS Code Configuration

The project includes VS Code settings for optimal development experience:

```json
{
    "python.analysis.extraPaths": [
        "./odoo",
        "./custom_addons"
    ]
}
```

## Screenshots

### Book Management

**Book List View**
![Book List View](https://github.com/user-attachments/assets/bc8f92e4-2fbc-4c03-8623-17d1f4587426)

**Book Form View**
![Book Form View](https://github.com/user-attachments/assets/7c6d5734-9aa2-4c7c-b4d0-47350c7db8ad)

### Author Management

**Author List View**
![Author Management](https://github.com/user-attachments/assets/09d9dd00-981e-40e1-a6dd-3bb9132170c5)

### Borrowing System

**Borrowing Records List**
![Borrowing Records](https://github.com/user-attachments/assets/3ea09961-276d-4708-a20e-e470092b1941)

**Borrowing Form View**
![Borrowing Form](https://github.com/user-attachments/assets/59e39b5a-8369-4863-9588-e905cfdcbd4a)
