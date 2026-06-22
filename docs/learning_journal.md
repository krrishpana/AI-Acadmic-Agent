# Learning Journal

## Day 1

### Goal
Understand how LLM applications are built and initialize a professional repository structure.

### Learned
- Difference between an SDK and a raw API.
- The role of `genai.Client` as a secure gateway/manager.
- The functionality of `types.GenerateContentConfig` for tuning LLM behavior.
- LLMs are inherently stateless out of the box.


## Day 2

### Goal
Understand how LLM applications stores memory and retrieves it to use it throughout sessions.

### Learned
- Types of memory (short term, persistant histry and retrieval memory).
- Realized that the Gemini API does not naturally retain conversation state; the application must continuously pass the complete structured history with every new request.
- Learned why the modern `google-genai` SDK uses strict Pydantic enforcement, requiring raw data to be wrapped explicitly inside `types.Content` containers and `types.Part.from_text()` components.
- Discovered how Pydantic models validate data on ingestion, and how `.model_dump()` safely flattens complex objects into JSON-serializable Python dictionaries for disk storage.
- Utilized the `**` operator to cleanly reconstruct structured SDK configurations when reading from file storage.


## Day 3

### Goal
Implement dynamic system instructions (personas) and build structural, defensive error handling for a production-ready user experience.

### Learned
- Configured the model's behavior explicitly using system instructions within `types.GenerateContentConfig` to shift the chatbot's dynamic behavior across multiple selectable personas.
- Replaced abrupt `return` exits inside the chat loop with `break` mechanisms. This protects the active state, ensuring that sudden server or network errors gracefully terminate the session without destroying or corrupting existing chat history.
- Integrated a robust input validation helper using an infinite `while True` verification flow to intercept empty strings or deceptive spaces using `.strip()`, ensuring bad data never reaches the API.
-  Leveraged Python dictionary structures combined with dynamic iteration unpacking variables to decouple backend persona configurations from numeric selection inputs, allowing for flexible, maintainable application scaling.