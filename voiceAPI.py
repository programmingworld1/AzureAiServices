import asyncio
import pyaudio
from azure.core.credentials import AzureKeyCredential
from azure.ai.voicelive.aio import connect
from azure.ai.voicelive.models import (
    RequestSession, Modality, InputAudioFormat, OutputAudioFormat, ServerVad, ServerEventType,
    UserMessageItem, InputTextContentPart
)

API_KEY = ""
ENDPOINT = "https://dqwdwfsfsdfewf.cognitiveservices.azure.com/"
MODEL = "gpt-4o"

SAMPLE_RATE = 24000
CHANNELS = 1

async def main():
    p = pyaudio.PyAudio()
    speaker = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        output=True
    )

    async with connect(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(API_KEY),
        model=MODEL,
    ) as conn: # This opens a WebSocket connection to the Voice Live API. The connection is used to send messages, receive responses, and process events in real time. The connection will remain open until we exit the async with block, at which point it will be automatically closed.
        session = RequestSession(
            modalities=[Modality.TEXT, Modality.AUDIO], # the API streams back both spoken audio / text transcript at the same time, which is why we can print the tex and play the audio.
            instructions="You are a helpful assistant.",
            input_audio_format=InputAudioFormat.PCM16, # the format of audio you send to the API (microphone input).
            output_audio_format=OutputAudioFormat.PCM16, # the format of audio the API sends back to you (the spoken response you hear through the speakers).
            turn_detection=ServerVad( # tells the API how to detect when you've finished speaking — so it knows when to stop listening and start responding
                threshold=0.5, # the sensitivity of the voice activity detection (VAD). A lower threshold means more sensitivity, which can lead to earlier detection of speech but also more false positives. A higher threshold means less sensitivity, which can reduce false positives but may require louder or clearer speech to trigger.
                prefix_padding_ms=300, # the amount of audio (in milliseconds) to include before the detected end of speech. This can help ensure that the beginning of your response isn't cut off.
                silence_duration_ms=500 # the amount of silence (in milliseconds) to consider as the end of speech. This helps the API determine when to stop listening and start responding.
            ),
        )
        await conn.session.update(session=session) # send the session configuration to the API

        # sends your message to the API
        await conn.conversation.item.create(item=UserMessageItem(
            content=[InputTextContentPart(text="Hello, how are you?")]
        ))
        await conn.response.create() # trigger the API to start generating a response based on the message we just sent. The API will stream back both the spoken audio and the text transcript of the response as it's being generated, which is why we can process both at the same time in the loop below.

        # receives the streaming response back from the API
        async for evt in conn:
            if evt.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DELTA: # the API streams back the text transcript of the response in small chunks as it's being generated. This event is triggered each time a new chunk of transcript is available. We print that chunk to the console as it's being generated.
                print(evt.delta.encode("cp1252", errors="replace").decode("cp1252"), end="", flush=True)
            elif evt.type == ServerEventType.RESPONSE_AUDIO_DELTA: # the API streams back the audio response in small chunks as it's being generated. This event is triggered each time a new chunk of audio is available. We write that chunk to the speakers to play it in real time as it's being generated.
                speaker.write(evt.delta)
            elif evt.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
                print()  # print a newline after the full transcript of the response has been printed. This event is triggered once after the final chunk of audio has been streamed and the full transcript of the response is available. It's a good place to print a newline to separate this response from the next one in the console output.
            elif evt.type == ServerEventType.RESPONSE_DONE:
                break # When the code exits this block (either normally after the break, or due to an error), Python automatically calls the cleanup code that closes the WebSocket connection. The break only exits the for loop. After the break, the code reaches the end of the async with block, and that's what closes the connection — not the break itself.

    # The WebSocket connection is automatically closed when we exit the async with block above. These lines are just to clean up the audio resources after we're done processing the response from the API.
    # are for closing the speaker (PyAudio), not the WebSocket connection. 
    # - speaker.stop_stream() — stops the audio stream (no more audio can be written to it)
    # # - speaker.close() — releases the audio device itself
    # - p.terminate() — shuts down the entire PyAudio instance
    # They clean up at different levels. You need all three because PyAudio has multiple layers — the stream, the device, and the PyAudio engine. Skipping any of them can leave resources     
    # locked.
    # all three lines are purely about your speakers:
    speaker.stop_stream() 
    speaker.close() 
    p.terminate() 

asyncio.run(main())
