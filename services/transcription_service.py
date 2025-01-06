import os
import json
from pprint import pprint

from dotenv import load_dotenv
from fastapi import HTTPException

from models import CallDetailsModel, TokenUsageModel, TranscriptionResponseModel
from settings import Config
from utils import NOTE_TYPE_DESCRIPTORS


from openai import OpenAI
import assemblyai as aai

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment
openai_api_key = Config.OPEN_API_KEY
assemblyai_api_key = Config.ASSEMBLYAI_API_KEY

client = OpenAI(api_key=openai_api_key)
aai.settings.api_key = assemblyai_api_key


class TranscriptionService:
    aai_config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()

    async def transcribe_audio(self, call_details: CallDetailsModel, file_path: str):
        print('starting transcribe audio')
        try:
            # Check if the file path exists
            if not os.path.exists(file_path):
                raise HTTPException(status_code=400, detail="File not found")

            print(f"Audio file found at: {file_path}")

            # Check the file size
            file_size = os.path.getsize(file_path)
            file_size_gb = file_size / (1024 * 1024 * 1024)  # Convert file size to GB

            print(f"File size: {file_size_gb:.2f} GB")
            print("*" * 20)

            if file_size_gb > 2.0:
                print("File size exceeds 2GB, using large file transcription")
                # Step 1: Transcribe the large audio using the chunking method
                transcription_model = await self.transcribe_large_file(file_path)
            else:
                print("File size is within limit, using standard transcription")
                # Step 1: Transcribe the audio using AssemblyAI
                transcription_model = await self.transcribe_with_assemblyai(file_path)

            print("finished transcribing with AssemblyAI or large file method")
            print("*" * 20)
            print("save transcription to call details")
            # Serialize the transcription model to JSON string or plain text for saving if needed
            call_details.transcription = transcription_model
            print("completed transcription to call details")
            print("*" * 20)

            print("starting meeting minutes")
            # Step 2: Generate meeting minutes with note type responses
            results, token_usage = await self.meeting_minutes(call_details)
            print("end meeting minutes")
            print("*" * 20)

            print("Assigning title and note_type_responses")
            # Assign the title and note type responses to CallDetailsModel
            call_details.title = results['title']
            call_details.note_type_responses = results['note_type_responses']
            print("end title and note_type_responses")
            print("*" * 20)

            print("Start Token usage")
            # Step 3: Accumulate token usage
            token_usage_model = await self.accumulate_token_usage(token_usage, call_details.minutes_elapsed)
            print("End Token usage")
            print("*" * 20)

            print("Save")
            # Save the token usage and associate it with call details
            call_details.token_usage = token_usage_model.save()
            print("*" * 20)
            print("Save")

            # Step 4: Save the CallDetailsModel to MongoDB
            call_details_document = call_details.save()
            print("*" * 20)

            # Step 5: Return the saved document as a dictionary to be sent back to the client
            return call_details_document.to_dict()

        except Exception as e:
            print(f"Error during transcription processing: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to process audio file: {str(e)}")

    async def transcribe_with_assemblyai(self, file_location: str):
        try:
            print(f"Starting AssemblyAI transcription for file: {file_location}")
            # Transcribe the local file using AssemblyAI
            with open(file_location, "rb") as audio_file:
                # Upload file to AssemblyAI
                transcript = self.transcriber.transcribe(
                    audio_file,
                    config=self.aai_config
                )
                # Process the transcription result into your model format
                transcription_model = TranscriptionResponseModel(
                    utterances=[{
                        "speaker": utterance.speaker,
                        "start": utterance.start,
                        "end": utterance.end,
                        "text": utterance.text,
                        "confidence": utterance.confidence
                    } for utterance in transcript.utterances]
                )

                print("Transcription completed with AssemblyAI")
                pprint(transcription_model)
                return transcription_model

        except Exception as e:
            print(f"AssemblyAI transcription failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    async def meeting_minutes(self, call_details: CallDetailsModel):
        print("inside Meeting minutes")
        print("-" * 20)
        # Extract roles of participants who are hosts
        host_role = [participant.role for participant in call_details.participants if participant.isHost]
        roles = ', '.join(host_role)
        print("set host role and roles")
        # Extract participant names and count
        participant_names = [participant.name for participant in call_details.participants]
        participant_count = len(call_details.participants)
        print("set participant names and count")
        # Use callType since customCallType no longer exists
        call_type = call_details.callType
        notes = call_details.notes if call_details.notes else "No additional notes provided."
        print('set call type and notes')

        # Prepare a breakdown of each utterance with speaker and text
        utterance_breakdown = "\n".join(
            [f"Speaker {utterance.speaker}: {utterance.text}" for utterance in call_details.transcription.utterances]
        )

        # Prepare the note type requests based on the provided list
        note_type_requests = []
        for note_type in call_details.notetype:
            # Get the description for the note type from the NOTE_TYPE_DESCRIPTORS dictionary
            description = NOTE_TYPE_DESCRIPTORS.get(note_type, f"Provide details for '{note_type}'.")
            # Add specific instructions based on the note type, emphasizing Markdown formatting
            note_type_requests.append(
                f"\"{note_type}\": \"{description}. (Use Markdown Formatting in this response).\""
            )
        print("set note type requests")
        print("-" * 20)

        # Join the custom instructions for each requested note type
        note_type_instructions = ",\n".join(note_type_requests)
        print("note type instructions")
        # Construct the system message with updated call type reference, utterance breakdown, and dynamic note type requests
        system_message = f"""
        You are a highly skilled AI specializing in conversation analysis and trained to assist {roles} based on their specific responsibilities and tasks.
        Based on the following transcription from a {call_type}, please generate the requested information for each of the specified note types.
        The call includes {participant_count} participants: {', '.join(participant_names)}.
        Additional context provided in the notes: '{notes}'.

        Please respond in JSON format, ensuring that the values of each key are written in Markdown.

        Important: Respond **only** in the following JSON format and nothing else:

        ```json
        {{
            "title": "Your title summarizing the main focus here.",
            "note_type_responses": {{
                {note_type_instructions}
            }}
        }}
        ```
        """
        print("generated system message")

        print("-" * 20)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": utterance_breakdown}  # Use the transcription text from the model
                ]
            )

            raw_response = response.choices[0].message.content.strip()
            print(f"Raw GPT response: {raw_response}")
            print("*" * 20)

            # Clean up the response by removing code block markers
            if raw_response.startswith("```json"):
                raw_response = raw_response[7:]
            if raw_response.endswith("```"):
                raw_response = raw_response[:-3]

            # Parse the response into JSON
            result = json.loads(raw_response)

            # Collect token usage data from the API response
            combined_token_usage = {
                "total_tokens": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }

            return result, combined_token_usage

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            raise HTTPException(status_code=500, detail="Failed to parse GPT response")
        except Exception as e:
            print(f"General error: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    async def accumulate_token_usage(self, combined_token_usage, minutes_elapsed):
        input_token_rate = 0.150 / 1_000_000
        output_token_rate = 0.600 / 1_000_000
        transcription_cost = minutes_elapsed * (0.37 / 60)

        prompt_tokens = combined_token_usage.get('prompt_tokens', 0)
        completion_tokens = combined_token_usage.get('completion_tokens', 0)

        input_cost = prompt_tokens * input_token_rate
        output_cost = completion_tokens * output_token_rate
        total_cost = transcription_cost + input_cost + output_cost

        token_usage_model = TokenUsageModel(
            transcription_cost=transcription_cost,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost
        )

        return token_usage_model

    async def transcribe_large_file(self, file_location: str):
        try:
            # Split the audio file into smaller chunks
            chunk_files = self.split_audio(file_location)
            transcription_results = []

            for chunk_file in chunk_files:
                with open(chunk_file, "rb") as audio_file:
                    # Upload file to AssemblyAI and transcribe
                    transcript = self.transcriber.transcribe(audio_file, config=self.aai_config)

                    # Collect each chunk's transcription results
                    transcription_results.extend([{
                        "speaker": utterance.speaker,
                        "start": utterance.start,
                        "end": utterance.end,
                        "text": utterance.text,
                        "confidence": utterance.confidence
                    } for utterance in transcript.utterances])

            # Combine the transcriptions into a single model
            transcription_model = TranscriptionResponseModel(utterances=transcription_results)
            print("Transcription completed for all chunks")
            pprint(transcription_model)
            return transcription_model

        except Exception as e:
            print(f"Transcription failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    def split_audio(self, file_location: str):
        # Use FFmpeg to split the audio file
        output_pattern = os.path.join(os.path.dirname(file_location), "output_chunk_%03d.mp3")
        split_command = f"ffmpeg -i {file_location} -f segment -segment_time 1800 -segment_overlap 5 -c copy {output_pattern}"
        os.system(split_command)

        # Get the list of chunked audio files
        return glob.glob(os.path.join(os.path.dirname(file_location), "output_chunk_*.mp3"))