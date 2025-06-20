import os
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Message:
    """Represents a message in the conversation."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime

@dataclass
class EssaySession:
    """Represents an essay writing session."""
    session_id: str
    topic: Optional[str] = None
    messages: List[Message] = None
    current_stage: str = "topic_selection"  # topic_selection, brainstorming, outline, writing, revision
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []

class EssayTutor:
    """Main class for the essay writing tutor."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the essay tutor with OpenAI API key."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to the constructor.")
        
        self.client = openai.AsyncOpenAI(api_key=self.api_key)
        self.sessions: Dict[str, EssaySession] = {}
        
        # System prompt for the essay tutor
        self.system_prompt = """You are an expert essay writing tutor. Your role is to help students learn how to write effective essays through a structured, step-by-step approach.

Your teaching methodology:
1. Start by helping students choose a clear, focused topic
2. Guide them through brainstorming ideas and organizing thoughts
3. Help them create a structured outline
4. Assist with writing clear, coherent paragraphs
5. Provide feedback on revision and improvement

Key principles to emphasize:
- Clear thesis statements
- Logical organization and flow
- Strong topic sentences
- Supporting evidence and examples
- Proper transitions between ideas
- Conclusion that reinforces the main argument

Be encouraging, patient, and specific in your feedback. Ask clarifying questions when needed and provide concrete suggestions for improvement. Always maintain a supportive, educational tone."""

    async def create_session(self, session_id: str) -> EssaySession:
        """Create a new essay writing session."""
        session = EssaySession(session_id=session_id)
        self.sessions[session_id] = session
        return session

    async def get_response(self, session_id: str, user_message: str) -> str:
        """Get a response from the AI tutor for a given session and user message."""
        if session_id not in self.sessions:
            await self.create_session(session_id)
        
        session = self.sessions[session_id]
        
        # Add user message to session
        session.messages.append(Message(
            role="user",
            content=user_message,
            timestamp=datetime.now()
        ))
        
        # Prepare conversation history for OpenAI
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history (last 10 messages to avoid token limits)
        for msg in session.messages[-10:]:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to session
            session.messages.append(Message(
                role="assistant",
                content=assistant_response,
                timestamp=datetime.now()
            ))
            
            return assistant_response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            session.messages.append(Message(
                role="assistant",
                content=error_msg,
                timestamp=datetime.now()
            ))
            return error_msg

    def get_session_history(self, session_id: str) -> List[Message]:
        """Get the conversation history for a session."""
        if session_id not in self.sessions:
            return []
        return self.sessions[session_id].messages.copy()

    def get_session_info(self, session_id: str) -> Optional[EssaySession]:
        """Get session information."""
        return self.sessions.get(session_id)

    async def reset_session(self, session_id: str) -> bool:
        """Reset a session, clearing all messages."""
        if session_id in self.sessions:
            self.sessions[session_id] = EssaySession(session_id=session_id)
            return True
        return False

# Simple CLI interface for testing
async def main():
    """Simple CLI interface for testing the essay tutor."""
    print("Welcome to the Essay Writing Tutor!")
    print("Type 'quit' to exit, 'reset' to start over, 'history' to see conversation history")
    
    tutor = EssayTutor()
    session_id = "test_session"
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye! Keep practicing your essay writing!")
                break
            elif user_input.lower() == 'reset':
                await tutor.reset_session(session_id)
                print("Session reset. Let's start fresh!")
                continue
            elif user_input.lower() == 'history':
                history = tutor.get_session_history(session_id)
                print("\nConversation History:")
                for msg in history:
                    print(f"{msg.role.capitalize()}: {msg.content}")
                continue
            elif not user_input:
                continue
            
            print("Tutor: ", end="", flush=True)
            response = await tutor.get_response(session_id, user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\nGoodbye! Keep practicing your essay writing!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 