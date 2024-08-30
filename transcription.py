import os
from google.cloud import speech
from google.cloud.speech_v1 import enums

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

# Initialize the Speech client
speech_client = speech.SpeechClient()

# URI of the media file stored in Google Cloud Storage
media_uri = 'sample-0.mp3'
audio = speech.RecognitionAudio(uri=media_uri)

# Configure the request for regular recognition
config = speech.RecognitionConfig(
    sample_rate_hertz=48000,                # Sample rate in Hertz
    enable_automatic_punctuation=True,      # Auto punctuation enabled
    language_code='en-US',                  # Language of the audio
    audio_channel_count=2                   # Stereo audio with 2 channels
)

# Configure the request for enhanced recognition using the "video" model
config_enhanced = speech.RecognitionConfig(
    sample_rate_hertz=48000,
    enable_automatic_punctuation=True,
    language_code='en-US',
    use_enhanced=True,                      # Use enhanced model for better accuracy
    model='video'                           # Model optimized for video transcription
)

# Initiate the long-running transcription process
operation = speech_client.long_running_recognize(config=config, audio=audio)

print("Transcription in progress, please wait...")

try:
    # Retrieve the transcription result with a timeout
    response = operation.result(timeout=90)

    # Process and print the transcription results
    for result in response.results:
        # Access the first (best) alternative transcription
        transcript = result.alternatives[0].transcript
        confidence = result.alternatives[0].confidence

        # Print the transcript and confidence (optional)
        print(f"Transcript: {transcript}")
        # print(f"Confidence: {confidence:.2f}")  # Uncomment if you want to see the confidence score

except Exception as e:
    print(f"An error occurred during transcription: {str(e)}")

