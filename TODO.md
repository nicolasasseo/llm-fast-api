# TODO

## ✅ Completed Refactoring

- [x] **Remove excess code:** Eliminated user registration, authentication, and password management
- [x] **Simplify to in-memory approach:** Removed database dependencies and created simple chat API
- [x] **System prompt support:** Added system prompt handling in chat requests
- [x] **Efficient prompt construction:** Using in-memory conversation history

## Next Steps

- [ ] **Add prompt converter:** Implement logic to convert OpenAI-style role-based message lists into the correct prompt format for different LLM backends (Ollama/vLLM)
- [ ] **Add automated tests:** Ensure correct prompt formatting and LLM responses
- [ ] **Port to EC2:** Plan and begin porting to EC2 for production/deployment with security protocols and reverse proxying

---

**Notes:**

- The API is now stateless and simple, perfect for integration with your company's application
- System prompts are handled per request, allowing dynamic agent behavior
- Conversation history is maintained in memory for context
- Ready for the next phase of development (prompt converter, testing, deployment)
