# TODO

## Refactor for Company Integration

- [ ] **Require and use system prompt:** When starting a new chat, require a system prompt (agent definition) as part of the agent creation flow, and use it as the first message in the conversation history.
- [ ] **Remove excess code:** Eliminate user registration, authentication, and password management, since user management will be handled by the company's main application.
- [ ] **Implement prompt converter:** Add logic to convert OpenAI-style role-based message lists (including the system prompt) into the correct prompt format for the selected LLM (Ollama or vLLM).
- [ ] **Simplify chat API:** Only support chat conversations (with history) and return the LLM's answer, matching the OpenAI Chat Completions API style. Remove endpoints and logic not needed for this core functionality.

## Testing

- [ ] **(Recommended) Add automated tests:** Ensure correct prompt formatting and LLM responses, especially after refactoring.

## Production/Deployment

- [ ] **Port to EC2:** After the core chat API is working, plan and begin porting to EC2 for production/deployment. This includes setting up security protocols, reverse proxying, and other company-grade deployment practices.

---

**Notes:**

- The API should be stateless regarding users (no user DB), but may support session or conversation IDs if needed by the company app.
- The prompt converter is essential for portability between Ollama and vLLM.
- Automated tests are optional but highly recommended for reliability after changes.
