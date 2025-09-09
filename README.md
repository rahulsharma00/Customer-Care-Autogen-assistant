# Features

## Multi-Agent System
Three specialized agents for different query types:

- **Return Agent**: Handles return-related questions  
- **Orders Agent**: Manages order-related inquiries  
- **Payment Agent**: Addresses payment-related issues  

## Knowledge Base Integration
Uses a **JSON-based knowledge base** for accurate responses.

## Friendly Interface
Clean **Streamlit chat interface** with persistent conversation history.

## Follow-up Questions
Random friendly follow-ups to encourage continued engagement.

# Project Structure

The project consists of **two main Python files**:

1. **backend.py**  
   - Contains all the core logic and multi-agent system implementation.  
   - Handles query classification and response generation using the knowledge base.  

2. **app.py**  
   - Implements a **Streamlit app** for user interaction.  
   - Provides a simple and friendly chat interface connected to the backend logic.  
