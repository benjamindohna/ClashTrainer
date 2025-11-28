# ClashTrainer

## Description
A simple training tool designed to help players of **Clash Royale** to improve in the game. Currently, the main features revolve around elixir awareness and basic but relevant calculations abilities. 

## Purpose and Scope
Most of the tools build for Clash Royale players so far mainly revolve around deck building and superficial matchup analysis. I believe far more sophisticated and useful tools can be built to help players improve their skills. 
The dream or end goal of this project is to sucessfully incorporate one or multiple models that can create common and relevant game situations, and subsequently not only find, but also explain the best move(s) for each of these situations. I believe this would build the foundation of the best way to improve: pattern recognition and awareness of best moves. 

## Demo
![Demo GIF](ClashTrainerDemo.gif)

## For Ogabek🤓
* Check out the amazing RegEX in the Terminal Fronted files. Thank God I implemented them!
* In get_key() function (of same files) there is try and finally. WOOOOOOW🙀

## Project Structure
ClashTrainer/
├── .gitignore            # Files to ignore in Git (must be kept!)
├── README.md             # Project description (must be kept!)
├── requirements.txt      # Python dependencies (must be kept!)
├── global_packages.txt   # Deprecated list of packages (recommend removing)
├── pytest.ini            # Pytest configuration
├── ClashTrainerDemo.gif  # GIF/Video for project functionality
├── run.py                # Main entry point (instead of main.py)
├── WebApp/               # Source code folder for web components
│   ├── routes/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   └── api.py
├── TerminalFrontend/     # Source code folder for terminal components
│   ├── multiple_cards_elixir_quiz.py
│   └── single_card_elixir_quiz.py
├── Backend/              # Source code folder for core logic
│   └── trade_calculations.py
├── Data/                 # Data and utility files
│   ├── cards.json        # External data file (must be kept!)
│   ├── cards_sample.json # Sample data file
│   ├── data_utils.py     # Functions for data manipulation
│   └── meta_score_scraping.py
├── tests/                # Test files
│   └── test_quiz_routes.py
├── myproject_env/        # Virtual Environment (must be in .gitignore)
└── __pycache__/          # Bytecode/Cache (must be in .gitignore)

## Project Structure
my_project/
├── .git/                 # Git repository (created automatically)
├── .gitignore            # Files to ignore in Git
├── README.md             # Project description
├── requirements.txt      # Python dependencies
├── main.py               # Main entry point
├── src/                  # Source code folder
│   ├── utils.py
│   └── config.py
├── tests/                # Test files
│   └── test_utils.py
└── data/                 # Data files (often in .gitignore)
    └── .gitkeep          # Empty file to track empty folder

## Project Outline & Features

Currently, the project is planned across these developmental phases:

### 1. Initial Prototype (Terminal Quiz)
* **Goal:** Simple quiz for Clash Royale cards running entirely in the terminal.
* **Mechanism:** User is shown a card name and inputs the correct elixir cost (e.g., Knight → 3).
* **Current Status:** **Implemented.** Uses a JSON card database.

### 2. Elixir Equation Challenges
* **Goal:** Expand the quiz into more strategic, math-based exercises.
* **Mechanism:** Present small scenarios (opponent plays X cards, player plays Y cards) and the user calculates the total elixir balance.

### 3. Web Version
* **Goal:** Move the training platform to a clean, intuitive website.
* **Mechanism:** Display card images and use interactive buttons for input, improving the user experience.

### 4. Advanced Learning Platform
* **Goal:** Add more complex challenges beyond simple elixir math.
* **Mechanism:** Include correct placement challenges using arena images, requiring users to select the optimal tile/placement for given scenarios.

---

## To-Do List

### Game Mechanics
* [ ] Implement a score tracking system.
* [ ] Introduce mixed difficulty modes.

### Future Scope
* [ ] Find new ideas how to provide value to players.
