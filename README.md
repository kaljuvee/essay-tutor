# Essay Tutor

An AI-powered essay writing tutor built with OpenAI and Streamlit that helps students improve their writing skills through interactive conversations.

## Features

- Interactive chat interface for essay writing assistance
- Session management for ongoing conversations
- AI-powered feedback and suggestions
- Modern web interface built with Streamlit

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd essay-tutor
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** Replace `your_openai_api_key_here` with your actual OpenAI API key. You can get one by signing up at [OpenAI's website](https://platform.openai.com/).

## Usage

### Running the Streamlit App

1. Make sure your virtual environment is activated
2. Run the Streamlit app:

```bash
streamlit run Home.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

### Running Tests

The project includes comprehensive tests for the essay tutor functionality. To run the tests:

```bash
# Run all tests
python tests/test_essay_tutor.py
```

The tests will:
- Test basic functionality (initialization, session creation, conversation)
- Test conversation flow with multiple messages
- Test session management features
- Test error handling
- Save test results to JSON files in the `data/` directory

### Test Results

Test results are automatically saved to the `data/` directory with timestamps. Each test run creates files like:
- `basic_functionality_YYYYMMDD_HHMMSS.json`
- `conversation_flow_YYYYMMDD_HHMMSS.json`
- `session_management_YYYYMMDD_HHMMSS.json`
- `error_handling_YYYYMMDD_HHMMSS.json`

## Project Structure

```
essay-tutor/
├── agent/
│   ├── __init__.py
│   └── essay_tutor.py          # Core essay tutor logic
├── data/                       # Test results and session data
├── tests/
│   ├── __init__.py
│   └── test_essay_tutor.py     # Test suite
├── Home.py                     # Streamlit web interface
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Dependencies

- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `streamlit` - Web application framework

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Make sure your `.env` file contains a valid OpenAI API key
2. **Import Errors**: Ensure your virtual environment is activated and dependencies are installed
3. **Port Already in Use**: If port 8501 is busy, Streamlit will automatically use the next available port

### Getting Help

If you encounter any issues:
1. Check that all dependencies are installed correctly
2. Verify your OpenAI API key is valid and has sufficient credits
3. Ensure your virtual environment is activated
4. Check the test results for any specific error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.