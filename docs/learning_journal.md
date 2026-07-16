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

## Day 4

### Goal
Implement real-time response streaming and low-level terminal animations to drastically enhance the application's user experience (UX).

### Learned
- Transitioned the core API architecture from unary response blocking to `client.models.generate_content_stream()`, shifting data delivery from bulk buffering to granular chunk iterations.
- Utilized the `flush=True` property within Python standard outputs to manually override standard terminal line-buffering, forcing text modules onto the screen the exact millisecond they are processed.
- Learned to manipulate the `\r` (Carriage Return) control character to seamlessly reset the terminal's typewriter cursor back to index 0 of the active line without triggering a new line feed.
- Implemented string accumulator patterns to stitch disparate chunk fragments back into a contiguous string array, ensuring structured chat payload contexts remain valid for historical appending.
- Engineered a sequential Boolean state switch (`first_chunk = True`) to keep a clean "Thinking..." text module visible right up until the exact moment data packets arrive, wiping the temporary visual queue via white-out space strings before text printing begins.

## Day 5

### Goal
Integrate a local vector database and implement Retrieval-Augmented Generation (RAG) to ground chatbot responses in custom document data.

### Learned
- Modified the stateful chat loop to intercept user queries and convert them into vectors using `client.models.embed_content()` with the `text-embedding-004` model.
- Connected a local disk-persistent vector store using `chromadb.PersistentClient()` to handle text fragment indexing and mathematical similarity searches.
- Engineered a synchronized loop parsing pipeline that matches text chunks, unique ID tags, and float arrays into parallel lists to satisfy ChromaDB storage schemas.
- Developed an `augmented_prompt` layout wrapper to merge retrieved document text with user queries, ensuring proper data context injection before streaming to the model.


## Day 6

### Goal
Implement advanced source tracking, safe payload routing, and a high-performance incremental ingestion system to scale the RAG pipeline.

### Learned
- Built a robust multi-file tracking loop that iterates over a localized repository directory, automatically indexing multiple knowledge sources simultaneously.
- Upgraded the data loader and text-splitter to attach persistent metadata payloads (`'source'` file and `'page'` numbers) to every text block, allowing the chatbot to display exact verified sources at the end of each response.
- Implemented an independent `active_prompt` runtime state variable inside the chat engine to route data-heavy context blocks securely to Gemini without polluting the clean user conversation history.
- Utilized Python `set` collection properties during the retrieval phase to filter out redundant citations automatically, rendering clean and non-repeating source lists to the user interface.
- Engineered a persistent database check using ChromaDB metadata lookups (`collection.get(where=...)`) to verify previously indexed assets, skipping identical files instantly on startup and dropping initialization latency to milliseconds.