import json
import os
from typing import Optional
from fastapi import APIRouter, Form, File, UploadFile, HTTPException

from models import CallDetails, CallDetailsModel

from services.transcription_service import TranscriptionService

UPLOAD_DIR = "./temp_chunks"  # Directory to store chunks
sessions = {}  # Dictionary to keep track of sessions and associated data

router = APIRouter()
transcription_service = TranscriptionService()

@router.get("/calls")
async def get_all_call_details():
    try:
        call_details_list = CallDetails.objects.all()
        call_details_dicts = [call_detail.to_dict() for call_detail in call_details_list]
        return {"call_details": call_details_dicts}
    except Exception as e:
        print(f"Error retrieving call details: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving call details")

@router.post("/upload_call_details")
async def upload_call_details(
    session_id: str = Form(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    call_details: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        session_path = os.path.join(UPLOAD_DIR, session_id)
        os.makedirs(session_path, exist_ok=True)

        if call_details and session_id not in sessions:
            call_details_dict = json.loads(call_details)
            sessions[session_id] = {
                "call_details": call_details_dict,
                "received_chunks": 0,
            }

        chunk_path = os.path.join(session_path, f"chunk_{chunk_index}")
        with open(chunk_path, "wb") as chunk_file:
            chunk_file.write(await file.read())
        sessions[session_id]["received_chunks"] += 1

        if sessions[session_id]["received_chunks"] == total_chunks:
            final_path = os.path.join(UPLOAD_DIR, f"{session_id}.m4a")
            with open(final_path, "wb") as final_file:
                for i in range(total_chunks):
                    chunk_file_path = os.path.join(session_path, f"chunk_{i}")
                    with open(chunk_file_path, "rb") as chunk:
                        final_file.write(chunk.read())

            call_details_dict = sessions[session_id]["call_details"]
            call_details_model = CallDetailsModel(**call_details_dict)
            result = await transcription_service.transcribe_audio(call_details_model, final_path)

            for i in range(total_chunks):
                os.remove(os.path.join(session_path, f"chunk_{i}"))
            os.rmdir(session_path)
            del sessions[session_id]

            return {"message": "File assembled and processed successfully", "data": result}

        return {"message": f"Chunk {chunk_index + 1} received successfully"}
    except Exception as e:
        print(f"Error during chunk upload: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to upload chunk")
