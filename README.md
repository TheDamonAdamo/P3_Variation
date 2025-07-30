# Starter code - OpenClassrooms WPS | P3

This repository contains the work that has been done so far on the chess tournament program.

### Data files

There are data files provided:
- JSON files for the chess clubs of Springfield and Cornville
- JSON files for two tournaments: one completed, and one in progress

### Models

This package contains the models already defined by the application:
* `Player` is a class that represents a chess player
* `Club` is a class that represents a chess club (including `Player`s)
* `ClubManager` is a manager class that allows to manage all clubs (and create new ones)

### Screens

This package contains classes that are used by the application to display information from the models on the screen.
Each screen returns a Command instance (= the action to be carried out).

### Commands

This package contains "commands" - instances of classes that are used to perform operations from the program.
Commands follow a *template pattern*. They **must** define the `execute` method.
When executed, a command returns a context.

### Main application

The main application is controlled by `manage_clubs.py`. Based on the current Context instance, it instantiates the screens and runs them. The command returned by the screen is then executed to obtain the next context.

The main application is an infinite loop and stops when a context has the attribute `run` set to False.


# P3-Application-Developer-Skills-Bootcamp - Chess Tournament Management

This repository contains a Python application for managing chess clubs, players, and now, tournaments.

## Project Structure Overview

This project has been structured to cleanly separate concerns:
- `commands/`: Contains the application logic and command handlers (like controllers).
    - `commands/models/`: New sub-package for all data model definitions (Club, ClubManager, Tournament, Player, Match, Round, DataManager).
- `data/`: Stores JSON data files for clubs and tournaments.
    - `data/clubs/`: Existing directory for club data.
    - `data/tournaments/`: New directory for tournament data.
    - `data/make_club.py`: Script to generate dummy club data.
    - `data/make_tournament.py`: New script to generate dummy tournament data.
- `screens/`: Contains user interface (UI) components.
    - `screens/clubs/`: Existing screens for club management.
    - `screens/players/`: Existing screens for player management.
    - `screens/tournament_screens/`: New screens for tournament management.
    - `screens/main_menu_screen.py`: New main menu to navigate the entire application.
- `main.py`: The application's entry point.
- `requirements.txt`: Lists Python dependencies.
- `flake8_report/`: Directory for static code analysis reports.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/OpenClassrooms-Student-Center/P3-Application-Developer-Skills-Bootcamp.git](https://github.com/OpenClassrooms-Student-Center/P3-Application-Developer-Skills-Bootcamp.git)
    cd P3-Application-Developer-Skills-Bootcamp
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Generate initial dummy data (optional but recommended for testing):**
    ```bash
    python data/make_club.py
    python data/make_tournament.py
    ```

2.  **Run the main application:**
    ```bash
    python main.py
    ```
    Follow the on-screen prompts to navigate through the menus.

## Running Tests and Linting

*(Instructions for running tests and linting would go here once testing framework is set up)*

## Features

### Existing Features:
* Club Management: Create, list, manage players within clubs, view, delete clubs.
* Player Management: Create, list, view, update player information (e.g., ELO).

### New Tournament Features:
* **Create Tournament:** Define new chess tournaments (name, location, dates, rounds).
* **Manage Tournament:**
    * Register players from existing club data.
    * Start/Advance Rounds: Implement Swiss-system pairing.
    * Enter Match Results: Record winners/draws for matches.
    * View Tournament Report: See player standings and round details.
* **Data Persistence:** Tournament data is saved to and loaded from JSON files.

## Development Notes

* **Models:** All core data structures (Club, Player, Match, Round, Tournament) are defined as classes in `commands/models/`.
* **Data Manager:** `commands/models/data_manager.py` handles all JSON serialization/deserialization for tournament-specific data, and loading players from existing club data.
* **UI (Screens):** User interaction is handled by classes in the `screens/` package. New tournament-specific screens are in `screens/tournament_screens/`.
* **Controllers (Commands):** High-level application logic resides in `commands/`. `commands/tournaments.py` is the main controller for tournament operations.

Feel free to explore and extend the application!
