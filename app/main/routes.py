from flask import Blueprint, render_template, request, jsonify, session
import uuid
import os
from werkzeug.utils import secure_filename
from app.rag.constants import max_history_turns
from app.rag.pipeline import run_rag
from app.logger import setup_logger
from flask import current_app


app_logger = setup_logger("app", "logs/app.log")


main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

@main.before_app_request
def initialize_session():
    if "chat_sessions" not in session:
        session["chat_sessions"] = {}

    if "current_chat" not in session:
        chat_id = str(uuid.uuid4())
        session["current_chat"] = chat_id
        session["chat_sessions"][chat_id] = []


def build_chat_context(chat_history, max_turns=max_history_turns):
    """
    Build conversational context from previous turns.
    Uses last `max_turns` interactions.
    """
    context_lines = []
    for turn in chat_history[-max_turns:]:
        context_lines.append(f"User: {turn['user']}")
        context_lines.append(f"Assistant: {turn['bot']}")
    return "\n".join(context_lines)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.before_app_request
def reset_chat_on_startup():
    """
    Clears chat session once per server start.
    """
    if current_app.config.get("RESET_CHAT_ON_STARTUP"):
        session.clear()
        current_app.config["RESET_CHAT_ON_STARTUP"] = False


@main.route('/')
def index():
    if 'chat_sessions' not in session:
        session['chat_sessions'] = {}
    if 'current_chat' not in session:
        session['current_chat'] = str(uuid.uuid4())
        session['chat_sessions'][session['current_chat']] = []
    return render_template('index.html')


@main.route('/chat', methods=['POST'])
def chat():
    # ---- ALWAYS initialize first ----
    chat_id = session.get('current_chat')

    if not chat_id:
        chat_id = str(uuid.uuid4())
        session['current_chat'] = chat_id

    if 'chat_sessions' not in session:
        session['chat_sessions'] = {}

    if chat_id not in session['chat_sessions']:
        session['chat_sessions'][chat_id] = []

    app_logger.info(f"Chat request received | Chat ID: {chat_id}")

    user_message = request.json.get('message')

    if not user_message:
        app_logger.warning("Empty message received")
        return jsonify({'response': 'Please enter a valid message.'})

    # ---- File checks ----
    if not os.path.exists(UPLOAD_FOLDER):
        app_logger.warning("Upload folder not found")
        return jsonify({
    'response': '📄 Please upload a document first so I can help you with it.'
})

    files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.lower().endswith(tuple(ALLOWED_EXTENSIONS))
    ]

    if not files:
        app_logger.warning("No documents uploaded")
        return jsonify({'response': 'Please upload a document first.'})

    latest_file = max(
        files,
        key=lambda f: os.path.getmtime(os.path.join(UPLOAD_FOLDER, f))
    )

    pdf_path = os.path.join(UPLOAD_FOLDER, latest_file)
    app_logger.info(f"Running RAG on file: {latest_file}")

    # ---- Conversational memory ----
    chat_history = session['chat_sessions'][chat_id]
    conversation_context = build_chat_context(chat_history)

    if conversation_context:
        enhanced_query = (
            f"Conversation so far:\n{conversation_context}\n\n"
            f"Current question:\n{user_message}"
        )
    else:
        enhanced_query = user_message

    # ---- RAG ----
    try:
        rag_output = run_rag(
            pdf_path=pdf_path,
            query=enhanced_query
        )
        bot_response = rag_output["result"]
    except Exception as e:
        app_logger.exception("RAG pipeline failed")
        return jsonify({'response': 'An internal error occurred. Please try again.'})

    # ---- Save chat ----
    session['chat_sessions'][chat_id].append({
        'user': user_message,
        'bot': bot_response
    })
    session.modified = True

    app_logger.info("Chat response sent successfully")
    return jsonify({'response': bot_response})



@main.route('/history', methods=['GET'])
def history():
    chat_sessions = session.get('chat_sessions', {})
    return jsonify(chat_sessions)


@main.route('/new_chat', methods=['POST'])
def new_chat():
    chat_id = str(uuid.uuid4())
    session['current_chat'] = chat_id
    session['chat_sessions'][chat_id] = []
    session.modified = True
    return jsonify({'chat_id': chat_id})


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'success': True, 'filename': filename})
    app_logger.info(f"File uploaded: {filename}")
    return jsonify({'error': 'Invalid file type'}), 400
