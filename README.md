# Odoo Library Management System

This project is a custom Odoo module for managing a library, including books, authors, and a borrowing system. It is built for Odoo 18 and demonstrates best practices for custom addon development.

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

This project follows the standard Odoo development structure, separating custom addons from the core Odoo source code.

```
project/
├── custom_addons/            # All custom modules reside here
│   └── library_management/
├── odoo/                     # Core Odoo 18 source code
└── venv/                     # Python virtual environment
```

## Setup and Installation

### Prerequisites

- Ubuntu (or a compatible Linux distribution)
- Python 3.10+
- PostgreSQL 12+
- Git

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

## How to Run

After the initial installation, you can start the server for daily development using this command:

```bash
./odoo/odoo-bin -d odoo-dev --addons-path=odoo/addons,custom_addons --dev=all
```

## VS Code Configuration

To enable code completion and hints in Visual Studio Code, a `.vscode/settings.json` file has been included with the following configuration, which tells the Python extension where to find the source modules:

```json
{
    "python.analysis.extraPaths": [
        "./odoo",
        "./custom_addons"
    ]
}
```
