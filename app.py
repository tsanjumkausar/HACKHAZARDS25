import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import traceback
from gtts import gTTS
import tempfile

API_KEY = "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"

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG") 
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

st.title("🖼 LlaMA-ViSIONX")
st.write("Upload an image, and the LlaMA-ViSIONX will describe it!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    base64_image = encode_image(image)
    client = Groq(api_key=API_KEY)

    if "description" not in st.session_state:
        st.session_state.description = ""

    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    with st.spinner("Analyzing image... ⏳"):
        try:
            # Get detailed description of the image if not already generated
            if not st.session_state.description:
                detailed_prompt = "Provide a detailed description of the following image:"
                chat_completion = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": detailed_prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                            ],
                        }
                    ],
                )
                st.session_state.description = chat_completion.choices[0].message.content

            description = st.session_state.description
            st.success("✅ Analysis Complete!")
            st.write("### 🔍 Description:")
            st.write(description)

            # Generate audio description
            tts = gTTS(text=description, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                temp_filename = tmp_file.name
            try:
                tts.save(temp_filename)
                st.audio(temp_filename, format="audio/mp3")
            except Exception as e:
                st.error(f"⚠️ Audio generation failed: {e}")

            # Generate related questions based on the description
            if not st.session_state.questions:
                question_prompt = f"Based on the following description, generate 5 relevant questions that a user might want to ask:\n\n{description}\n\nQuestions:"
                question_completion = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": question_prompt,
                        }
                    ],
                )
                questions_text = question_completion.choices[0].message.content
                # Parse questions from the response (assuming numbered list)
                questions = []
                for line in questions_text.splitlines():
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith("-")):
                        # Remove numbering or bullet
                        question = line.lstrip("0123456789. -").strip()
                        if question:
                            questions.append(question)
                if not questions:
                    # fallback to some default questions if parsing fails
                    questions = [
                        "What emotions are depicted in this image?",
                        "Can you describe the setting or location?",
                        "What objects or people are prominent?",
                        "What story could this image be telling?",
                        "What colors stand out the most?"
                    ]

                st.session_state.questions = questions

        except Exception as e:
            error_message = f"⚠ Error: {e}"
            st.error(error_message)
            st.text("Detailed traceback:")
            st.text(traceback.format_exc())

    if st.session_state.questions:
        st.write("### ❓ Related Questions:")
        for question in st.session_state.questions:
            if st.button(question):
                if question not in st.session_state.answers:
                    with st.spinner("Getting answer... ⏳"):
                        try:
                            answer_completion = client.chat.completions.create(
                                model="meta-llama/llama-4-scout-17b-16e-instruct",
                                messages=[
                                    {
                                        "role": "user",
                                        "content": [
                                            {"type": "text", "text": f"Please provide a concise but informative answer to the question: {question}"},
                                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                                        ],
                                    }
                                ],
                            )
                            answer = answer_completion.choices[0].message.content
                            st.session_state.answers[question] = answer
                        except Exception as e:
                            st.session_state.answers[question] = f"Error getting answer: {e}"
                st.write(f"*Q:* {question}")
                st.write(f"*A:* {st.session_state.answers.get(question, 'No answer available.')}")

st.write("Powered by Llama-4 Scout 🚀")

# Chatbot section
import datetime

st.write("---")
st.write("## 💬 Chatbot")

# Welcome message and instructions
st.write("Welcome to the chatbot! Ask any question and get answers powered by Llama-4 Scout.")
st.write("Type your question below and press Enter. Use the 'Clear Chat' button to reset the conversation.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

client = Groq(api_key=API_KEY)

def get_chat_response(user_input, chat_history):
    messages = []
    for speaker, message in chat_history:
        role = "user" if speaker == "You" else "assistant"
        messages.append({"role": role, "content": message})
    messages.append({"role": "user", "content": user_input})

    try:
        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def format_message(speaker, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if speaker == "You":
        return f"*You [{timestamp}]:* {message}"
    else:
        return f"*Bot [{timestamp}]:* {message}"

def clear_chat():
    st.session_state.chat_history = []

if st.button("Clear Chat"):
    clear_chat()

user_input = st.text_input("You:", key="input")

if user_input:
    if user_input.strip() == "":
        st.warning("Please enter a valid message.")
    else:
        response = get_chat_response(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

for speaker, message in st.session_state.chat_history:
    st.markdown(format_message(speaker, message))
