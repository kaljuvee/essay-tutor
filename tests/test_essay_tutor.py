#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Simple test script for the Essay Tutor application.
Tests basic functionality and writes results to JSON files.
"""

import asyncio
import json
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

# Import the essay tutor
from agent.essay_tutor import EssayTutor, EssaySession, Message

def create_data_directory():
    """Create the data directory if it doesn't exist."""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created data/ directory")

def save_test_results(test_name, results):
    """Save test results to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/{test_name}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"Test results saved to: {filename}")
    return filename

async def test_basic_functionality():
    """Test basic functionality of the EssayTutor."""
    print("\n=== Testing Basic Functionality ===")
    
    results = {
        "test_name": "basic_functionality",
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    # Test 1: Initialization
    try:
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            with patch('agent.essay_tutor.openai.AsyncOpenAI') as mock_client:
                mock_instance = AsyncMock()
                mock_client.return_value = mock_instance
                
                tutor = EssayTutor()
                
                test_result = {
                    "test": "initialization",
                    "status": "PASS",
                    "details": "EssayTutor initialized successfully"
                }
                results["tests"].append(test_result)
                print("✓ Initialization test passed")
                
    except Exception as e:
        test_result = {
            "test": "initialization",
            "status": "FAIL",
            "details": str(e)
        }
        results["tests"].append(test_result)
        print(f"✗ Initialization test failed: {e}")
    
    # Test 2: Session creation
    try:
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            with patch('agent.essay_tutor.openai.AsyncOpenAI') as mock_client:
                mock_instance = AsyncMock()
                mock_client.return_value = mock_instance
                
                tutor = EssayTutor()
                session = await tutor.create_session("test_session")
                
                test_result = {
                    "test": "session_creation",
                    "status": "PASS",
                    "details": f"Session created with ID: {session.session_id}"
                }
                results["tests"].append(test_result)
                print("✓ Session creation test passed")
                
    except Exception as e:
        test_result = {
            "test": "session_creation",
            "status": "FAIL",
            "details": str(e)
        }
        results["tests"].append(test_result)
        print(f"✗ Session creation test failed: {e}")
    
    # Test 3: Mock conversation
    try:
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            with patch('agent.essay_tutor.openai.AsyncOpenAI') as mock_client:
                mock_instance = AsyncMock()
                mock_client.return_value = mock_instance
                
                # Mock OpenAI response
                mock_response = MagicMock()
                mock_response.choices = [MagicMock()]
                mock_response.choices[0].message.content = "Hello! I'm your essay writing tutor. How can I help you today?"
                mock_client.chat.completions.create.return_value = mock_response
                
                tutor = EssayTutor()
                response = await tutor.get_response("conversation_test", "Hello")
                
                test_result = {
                    "test": "mock_conversation",
                    "status": "PASS",
                    "details": f"Got response: {response[:50]}..."
                }
                results["tests"].append(test_result)
                print("✓ Mock conversation test passed")
                
    except Exception as e:
        test_result = {
            "test": "mock_conversation",
            "status": "FAIL",
            "details": str(e)
        }
        results["tests"].append(test_result)
        print(f"✗ Mock conversation test failed: {e}")
    
    return results

async def test_conversation_flow():
    """Test conversation flow with multiple messages."""
    print("\n=== Testing Conversation Flow ===")
    
    results = {
        "test_name": "conversation_flow",
        "timestamp": datetime.now().isoformat(),
        "conversation": []
    }
    
    try:
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            with patch('agent.essay_tutor.openai.AsyncOpenAI') as mock_client:
                mock_instance = AsyncMock()
                mock_client.return_value = mock_instance
                
                # Mock different responses for different messages
                responses = [
                    "Hello! I'm your essay writing tutor. What topic would you like to write about?",
                    "Great choice! 'Climate Change' is a very relevant topic. Let's start by brainstorming some key points.",
                    "Excellent! Here's a suggested outline for your essay on climate change...",
                    "That's a good start! Let me help you develop your thesis statement..."
                ]
                
                tutor = EssayTutor()
                session_id = "flow_test"
                
                # Simulate a conversation
                messages = [
                    "Hello, I want to write an essay",
                    "I want to write about climate change",
                    "Can you help me create an outline?",
                    "How do I write a good thesis statement?"
                ]
                
                for i, message in enumerate(messages):
                    # Mock the response
                    mock_response = MagicMock()
                    mock_response.choices = [MagicMock()]
                    mock_response.choices[0].message.content = responses[i] if i < len(responses) else "Thank you for your question!"
                    mock_client.chat.completions.create.return_value = mock_response
                    
                    response = await tutor.get_response(session_id, message)
                    
                    conversation_entry = {
                        "user_message": message,
                        "tutor_response": response,
                        "timestamp": datetime.now().isoformat()
                    }
                    results["conversation"].append(conversation_entry)
                    
                    print(f"User: {message}")
                    print(f"Tutor: {response}")
                    print("-" * 50)
                
                test_result = {
                    "test": "conversation_flow",
                    "status": "PASS",
                    "details": f"Completed conversation with {len(messages)} messages"
                }
                results["tests"] = [test_result]
                
    except Exception as e:
        test_result = {
            "test": "conversation_flow",
            "status": "FAIL",
            "details": str(e)
        }
        results["tests"] = [test_result]
        print(f"✗ Conversation flow test failed: {e}")
    
    return results

async def test_session_management():
    """Test session management functionality."""
    print("\n=== Testing Session Management ===")
    
    results = {
        "test_name": "session_management",
        "timestamp": datetime.now().isoformat(),
        "sessions": {}
    }
    
    try:
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            with patch('agent.essay_tutor.openai.AsyncOpenAI') as mock_client:
                mock_instance = AsyncMock()
                mock_client.return_value = mock_instance
                
                tutor = EssayTutor()
                
                # Create multiple sessions
                session_ids = ["session1", "session2", "session3"]
                
                for session_id in session_ids:
                    session = await tutor.create_session(session_id)
                    session.topic = f"Topic for {session_id}"
                    
                    session_info = {
                        "session_id": session.session_id,
                        "topic": session.topic,
                        "current_stage": session.current_stage,
                        "message_count": len(session.messages)
                    }
                    results["sessions"][session_id] = session_info
                
                # Test session history
                for session_id in session_ids:
                    history = tutor.get_session_history(session_id)
                    results["sessions"][session_id]["history_length"] = len(history)
                
                # Test session info retrieval
                for session_id in session_ids:
                    session_info = tutor.get_session_info(session_id)
                    if session_info:
                        results["sessions"][session_id]["retrieved"] = True
                    else:
                        results["sessions"][session_id]["retrieved"] = False
                
                # Test session reset
                reset_result = await tutor.reset_session("session1")
                results["reset_test"] = {
                    "session_id": "session1",
                    "reset_successful": reset_result,
                    "messages_after_reset": len(tutor.sessions["session1"].messages)
                }
                
                test_result = {
                    "test": "session_management",
                    "status": "PASS",
                    "details": f"Managed {len(session_ids)} sessions successfully"
                }
                results["tests"] = [test_result]
                
                print(f"✓ Session management test passed - {len(session_ids)} sessions created")
                
    except Exception as e:
        test_result = {
            "test": "session_management",
            "status": "FAIL",
            "details": str(e)
        }
        results["tests"] = [test_result]
        print(f"✗ Session management test failed: {e}")
    
    return results

async def test_error_handling():
    """Test error handling scenarios."""
    print("\n=== Testing Error Handling ===")
    
    results = {
        "test_name": "error_handling",
        "timestamp": datetime.now().isoformat(),
        "errors": []
    }
    
    # Test 1: No API key
    try:
        with patch.dict(os.environ, {}, clear=True):
            EssayTutor()
            error_result = {
                "test": "no_api_key",
                "status": "FAIL",
                "details": "Should have raised ValueError"
            }
            results["errors"].append(error_result)
            print("✗ No API key test failed - should have raised error")
    except ValueError as e:
        error_result = {
            "test": "no_api_key",
            "status": "PASS",
            "details": str(e)
        }
        results["errors"].append(error_result)
        print("✓ No API key test passed")
    
    # Test 2: OpenAI API error
    try:
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            with patch('agent.essay_tutor.openai.AsyncOpenAI') as mock_client:
                mock_instance = AsyncMock()
                mock_client.return_value = mock_instance
                
                # Mock OpenAI error
                mock_client.chat.completions.create.side_effect = Exception("API Error")
                
                tutor = EssayTutor()
                response = await tutor.get_response("error_test", "Hello")
                
                if "Sorry, I encountered an error" in response:
                    error_result = {
                        "test": "openai_api_error",
                        "status": "PASS",
                        "details": "Error handled gracefully"
                    }
                    results["errors"].append(error_result)
                    print("✓ OpenAI API error test passed")
                else:
                    error_result = {
                        "test": "openai_api_error",
                        "status": "FAIL",
                        "details": "Error not handled properly"
                    }
                    results["errors"].append(error_result)
                    print("✗ OpenAI API error test failed")
                    
    except Exception as e:
        error_result = {
            "test": "openai_api_error",
            "status": "FAIL",
            "details": str(e)
        }
        results["errors"].append(error_result)
        print(f"✗ OpenAI API error test failed: {e}")
    
    return results

async def main():
    """Run all tests and save results."""
    print("Starting Essay Tutor Tests...")
    print("=" * 50)
    
    # Create data directory
    create_data_directory()
    
    # Run tests
    test_functions = [
        test_basic_functionality,
        test_conversation_flow,
        test_session_management,
        test_error_handling
    ]
    
    for test_func in test_functions:
        try:
            results = await test_func()
            save_test_results(results["test_name"], results)
        except Exception as e:
            print(f"Error running {test_func.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print("All tests completed! Check the data/ directory for results.")

if __name__ == "__main__":
    asyncio.run(main()) 