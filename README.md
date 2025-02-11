# Company Chat Assistant

A Flask-based web application that answers natural language queries about company employees and departments using an SQLite database.

## Features

- Answer questions about:
  - Department employees
  - Department managers
  - Hiring dates
  - Salary expenses
- Error handling for:
  - Invalid departments
  - Incorrect date formats
  - Empty results

## Setup

1. Clone repository:

   ```bash
   git clone https://github.com/yourusername/company-chat-assistant.git
   cd company-chat-assistant
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```bash
   python init_db.py
   ```

## Usage

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:8080`

3. Type your questions in natural language, for example:
   - "Who works in the Sales department?"
   - "When was John Smith hired?"
   - "What is the total salary expense for IT?"

