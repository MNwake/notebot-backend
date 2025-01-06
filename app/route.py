import json
import os
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from database import CallDetails
from models import CallDetailsModel, UserLogin, UserRegister

from services.auth_service import AuthService
from services.transcription_service import TranscriptionService


UPLOAD_DIR = "./temp_chunks"  # Directory to store chunks
sessions = {}  # Dictionary to keep track of sessions and associated data

#
class NoteBotRoute:
    def __init__(self, connection_manager, server_memory):
        self.router = APIRouter(tags=["NoteBot"])
        self.manager = connection_manager
        self.memory = server_memory
        self.transcription_service = TranscriptionService()
        self.define_routes()

    def define_routes(self):

        @self.router.get("/ping")
        async def pingpong():
            return "pong"

        @self.router.post("/register")
        async def register_user(user: UserRegister):
            # Delegate the registration process to AuthService
            print(f"Register User: {user.full_name}")
            print(f"Register User: {user.email}")
            return await AuthService.register_user(user)

        @self.router.post("/login")
        async def login_user(user: UserLogin):
            # Delegate the login process to AuthService
            return await AuthService.login_user(user)

        @self.router.get("/calls")
        async def get_all_call_details():
            try:
                # Query all CallDetails documents from MongoDB
                call_details_list = CallDetails.objects.all()

                # Convert each CallDetails document to a dictionary using to_dict()
                call_details_dicts = [call_detail.to_dict() for call_detail in call_details_list]

                # Return the list of call details as JSON
                return {"call_details": call_details_dicts}

            except Exception as e:
                print(f"Error retrieving call details: {str(e)}")

        @self.router.post("/upload_call_details")
        async def upload_call_details(
                session_id: str = Form(...),  # Session ID to keep track of file parts
                chunk_index: int = Form(...),  # Chunk index for ordering
                total_chunks: int = Form(...),  # Total number of chunks expected
                call_details: Optional[str] = Form(None),  # Call details JSON, sent with the first chunk
                file: UploadFile = File(...)
        ):
            try:
                # Ensure the upload directory exists
                os.makedirs(UPLOAD_DIR, exist_ok=True)

                # Create a directory for the session if it does not exist
                session_path = os.path.join(UPLOAD_DIR, session_id)
                os.makedirs(session_path, exist_ok=True)

                # If call details are provided, store them for this session
                if call_details and session_id not in sessions:
                    call_details_dict = json.loads(call_details)
                    sessions[session_id] = {
                        "call_details": call_details_dict,
                        "received_chunks": 0
                    }
                    print(f"Received call details for session {session_id}")

                # Save the current chunk
                chunk_path = os.path.join(session_path, f"chunk_{chunk_index}")
                with open(chunk_path, "wb") as chunk_file:
                    chunk_file.write(await file.read())

                # Update the session's received chunk count
                sessions[session_id]["received_chunks"] += 1
                print(f"Received chunk {chunk_index + 1}/{total_chunks} for session {session_id}")

                # Check if all chunks are received
                if sessions[session_id]["received_chunks"] == total_chunks:
                    # Assemble chunks into one file
                    final_path = os.path.join(UPLOAD_DIR, f"{session_id}.m4a")
                    with open(final_path, "wb") as final_file:
                        for i in range(total_chunks):
                            chunk_file_path = os.path.join(session_path, f"chunk_{i}")
                            with open(chunk_file_path, "rb") as chunk:
                                final_file.write(chunk.read())

                    print(f"All chunks received for session {session_id}. File assembled at {final_path}")

                    # Retrieve and process the call details
                    call_details_dict = sessions[session_id]["call_details"]
                    print('call details dict')
                    call_details_model = CallDetailsModel(**call_details_dict)
                    print(call_details_model.date)
                    print('call details model')

                    # Proceed with the transcription process
                    result = await self.transcription_service.transcribe_audio(call_details_model, final_path)
                    print('got result')
                    # Clean up chunks and session data
                    for i in range(total_chunks):
                        os.remove(os.path.join(session_path, f"chunk_{i}"))
                    os.rmdir(session_path)
                    del sessions[session_id]

                    return {"message": "File assembled and processed successfully", "data": result}

                return {"message": f"Chunk {chunk_index + 1} received successfully"}
            except json.JSONDecodeError as e:
                print(f"Failed to parse call details JSON: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Failed to parse call details JSON: {str(e)}")
            except Exception as e:
                print(f"Error during chunk upload: {str(e)}")
                raise HTTPException(status_code=400, detail="Failed to upload chunk")
