# 🌍 Conversational english serious game

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)](https://github.com/TomSchimansky/CustomTkinter)
![Pygame](https://img.shields.io/badge/Pygame-2.0.1-red.svg)

## 🚀 Overview

An interactive, gamified application designed to make English learning engaging and fun! This quizz based application is designed to help users improve their English vocabulary and grammar skills through a series of questions and answers using both text and audio. The application also includes a custom level creation feature, allowing users to create their own quizzes and share them with others.

### ✨ Features

- 🎮 Engaging Quiz Gameplay
- 📝 Custom Level Creation
- 🔊 Audio Support for Questions
- 🖊️ Question Editor

## 📸 Screenshots

[Placeholder for app screenshots - recommend taking screenshots of main menu, game screen, level creation, etc.]


## 🛠 Technologies Used

- Python 3.8+
- CustomTkinter
- Pygame
- PIL (Python Imaging Library)

## 🔧 Prerequisites

- Python 3.8 or higher
- pip package manager

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/archibald-carrion/Conversational-english-serious-game
cd Conversational-english-serious-game
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 How to Run

```bash
python main.py
```

## Development of the Application
### Model-View-Controller (MVC) Architecture
The application is designed using the Model-View-Controller (MVC) architecture, which separates the application into three main components:
- **Model**: Contains the data and logic of the application.
- **View**: Contains the user interface elements of the application.
- **Controller**: Handles user input and updates the model and view accordingly.

```mermaid
graph TD;
    View["View<br>Defines display (UI)<br>e.g. user clicks 'add to cart'"] -->|User interacts| Controller["Controller<br>Contains control logic<br>e.g. receives update from view then notifies model to 'add item'"];
    Controller -->|Updates data| Model["Model<br>Defines data structure<br>e.g. updates application to reflect added item"];
    Model -->|Notifies update| View;
```