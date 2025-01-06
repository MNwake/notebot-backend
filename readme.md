# AI-Powered Note-Taking App Backend

This repository contains the backend code for an **AI-powered note-taking application**. The app is a work in progress and aims to revolutionize the way users interact with meeting, lecture, or discussion recordings by allowing them to query an AI agent for insights, summaries, and actionable items.

## **Overview**

The goal of this application is to enable users to:
1. **Record conversations, meetings, calls, or lectures.**
2. **Transcribe audio into text using advanced transcription tools.**
3. **Interact with an AI agent** to generate:
   - Summaries
   - To-do lists
   - Action items
   - Custom insights or products tailored to the context of the discussion.

This application is designed to be a powerful tool for:
- **Business professionals**: Organize and extract actionable insights from meetings.
- **Students**: Create study guides, summaries, and project notes from class discussions.
- **Project teams**: Streamline collaboration with concise summaries and task lists.

---

## **Key Features**
- **API Endpoints**: A RESTful API to handle requests from the frontend.
- **Audio Transcription**: Converts uploaded audio files into text using AssemblyAI.
- **OpenAI Integration**: Interacts with the OpenAI API to generate AI-powered insights and summaries.
- **User Authentication**: Secure user registration and login features.
- **MongoDB Integration**: Persistent storage for user data, call details, and AI outputs.

---

## **Project Status**
> 🚧 This project is currently under development. Some features may not yet be fully implemented.

---

## **Tech Stack**
- **Framework**: FastAPI (Python)
- **Database**: MongoDB (via MongoEngine)
- **APIs**: 
  - OpenAI for AI interactions.
  - AssemblyAI for audio transcription.
- **Authentication**: `passlib` for password hashing.
- **Environment Management**: `python-dotenv` for secure configuration.

---

## **Directory Structure**

```plaintext
.
├── app
│   ├── __init__.py
│   ├── models.py               # Pydantic models for data validation
│   ├── route.py                # API routes for NoteBot
├── database
│   ├── __init__.py
│   ├── call_details.py         # MongoDB models for call details
│   ├── database.py             # Database connection logic
│   ├── transcription.py        # Audio transcription handling
│   ├── user.py                 # User-related MongoDB models
├── models
│   ├── __init__.py
│   ├── base.py                 # Base Pydantic model with common validators
│   ├── call_details.py         # Call detail models
│   ├── transcription.py        # Transcription-related models
│   ├── user.py                 # User models
├── routes
│   ├── __init__.py
│   ├── call_routes.py          # Routes for managing call details
│   ├── user_routes.py          # Routes for user authentication
├── services
│   ├── auth_service.py         # Authentication service
│   ├── transcription_service.py # Transcription service
├── settings
│   ├── __init__.py
│   ├── config.py               # App configuration
├── utils
│   ├── __init__.py
│   ├── utils.py                # Utility functions
├── .env                        # Environment variables (excluded from Git)
├── .gitignore                  # Files and directories to ignore in Git
├── main.py                     # Entry point for the FastAPI application
└── README.md                   # Project documentation
