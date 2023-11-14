# Habit Tracker 
## Overview
Habit Tracker is a simple Python application designed to help you track your daily and weekly habits. With this tool, you can create new habits, mark them as completed, view your habits, and monitor your longest streaks.

## Table of Contents

- [Features](#features)
- [Technical Details](#technical-details)
- [Usage](#usage)
- [Unit Testing](#unit-testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- Create and manage daily or weekly habits
- Track completion status and dates
- View and analyze habit data
- Calculate and display longest streaks
- When entering habit names, ensure they are spelled correctly
- Viewing by periodicities, ensure the habit has the correct periodicity otherwise solution outputs "'habit_name' not found"

## Technical Details

### Dependencies
- [Anaconda](https://www.anaconda.com/products/distribution) installed
- Libraries: pandas, numpy, matplotlib, datetime
- Python 3.11.4
- [SQLite3](https://www.sqlite.org/index.html) installed

### Installation

1. Clone the repository: `git clone https://github.com/JediPriAmo/Habit_tracker_Portfolio.git`
2. Navigate to the project directory: `cd Habit_tracker_Portfolio`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Open the Anaconda environment.
2. Launch the CMD.exe Prompt.
3. In the prompt, execute 'jupyter lab'.
4. In jupyter lab, select 'New launher' with the blue "+" icon in the toolbar.
5. Open the main Jupyter notebook and copy & paste code from "Habit_tracker_script.py" file.
6. Write the directory/ path to the "2new_habit_tracker.db" file in establishing connection to the database at the beginning of the script.
7. Run the code cells or execute the script.
8. Follow the main menu options.
9. Select "View longest streak for ALL habits" for a quick summary of all the predefined habits.

## Unit Testing
1. In anaconda environment, open jupyter lab.
2. Drag "Habit_tracker_script.py" & "Habittracker_Analytics_unittest.py" to the file browser in jupyter lab.
3. Open a new notebook.
4. You can copy & paste entire code from "Habittracker_Analytics_unittest.py" and run it.
5 Or you can input the following in cell:

```bash
%run -i Habittracker_Analytics_unittest.py

