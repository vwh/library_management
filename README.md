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
![Book List View](https://github.com/user-attachments/assets/e5e5056a-ddf6-4bc2-b883-f4b72c9bc133)

**Book Form View**
![Book Form View](https://github.com/user-attachments/assets/7c6d5734-9aa2-4c7c-b4d0-47350c7db8ad)

### Author Management

**Author List View**
![Author Management](https://github.com/user-attachments/assets/09d9dd00-981e-40e1-a6dd-3bb9132170c5)

**Author View**
![Author View](https://github.com/user-attachments/assets/42a94415-b101-497d-9e73-74e94f886d87)

**Author Form View**
![Author Form](https://github.com/user-attachments/assets/ddda55bf-cde3-4127-92bc-3ea3a72a99df)

### Borrowing System

**Borrowing Records List**
![Borrowing Records](https://github.com/user-attachments/assets/6cde2ba4-775d-49ad-b726-b9a4c2baf942)

**Borrowing Form View**
![Borrowing Form](https://github.com/user-attachments/assets/59e39b5a-8369-4863-9588-e905cfdcbd4a)

**Product**
<img width="1072" height="712" alt="image" src="https://github.com/user-attachments/assets/8aa878d0-38c7-4730-bc89-2d7d9ad81309" />

**Sales order**
<img width="1635" height="651" alt="image" src="https://github.com/user-attachments/assets/5a1686bd-81f8-4fbb-83ae-a5f1a1e8a086" />

**Invoice**
<img width="1623" height="721" alt="image" src="https://github.com/user-attachments/assets/87759cc2-ab9a-4e3f-8220-ffd0ccecf977" />

**Library Memberships View**
<img width="1130" height="217" alt="image" src="https://github.com/user-attachments/assets/0ea8ee0c-d4d0-44ea-9d83-7c62d364dcbe" />

