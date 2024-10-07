# Book Management System

## Overview
An intelligent book management system that allows users to manage books and reviews. It leverages the Gemini generative AI model to generate summaries and provides recommendations based on user preferences.

## Setup Instructions
1. Set up a PostgreSQL database and add its URL to the `.env` file.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run migrations to set up the database tables.
4. Start the FastAPI server using `uvicorn app.main:app --reload`.
