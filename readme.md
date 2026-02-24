
## Try it out
- http://load-balancer-frontline-academy-107751714.us-west-1.elb.amazonaws.com/

## Inspiration

Frontline workers in education and healthcare are expected to learn constantly—new protocols, policies, compliance updates, and best practices—but they rarely have the time (or energy) to sit through long trainings or dig through dense PDFs during a shift. In practice, learning happens in stolen moments: between classes, on breaks, during handoffs, or right before a task.

We built **Frontline Academy** to meet them exactly where they are.

Our inspiration came from a simple gap we kept seeing: organizations already have the information frontline teams need, but it’s trapped inside documents. Meanwhile, most learning tools are built for desk-based workflows—long modules, generic quizzes, and one-size-fits-all content that doesn’t adapt to what someone actually needs in the moment.

So we asked: **What if any training PDF could instantly become a personalized, role-relevant quiz with feedback—on demand?**  
That became the core idea behind Frontline Academy: turn existing materials into quick, targeted practice that reinforces understanding, boosts confidence, and fits real frontline schedules.

## What it does

**Frontline Academy** is a RAG-based web application that turns any frontline training PDF into an interactive, personalized quiz experience for **educators** and **healthcare workers**.

1. **Upload a PDF**
   - The user uploads a training document (policies, protocols, onboarding guides, manuals, etc.).

2. **RAG-powered understanding**
   - The app chunks the document, creates **embeddings**, and stores them in a vector database.
   - When the user selects the **quiz type** and specifies their requirements (difficulty, number of questions, topics/sections), the app performs a **vector search** to retrieve the most relevant passages.

3. **Quiz generation tailored to the user**
   - Using the retrieved context, the system generates a quiz aligned to what the user asked for (e.g., quick check, deep understanding, scenario-based questions).

4. **Instant grading + feedback**
   - After the user completes the quiz, the app provides:
     - Correct answers
     - Explanations grounded in the PDF content
     - Actionable feedback on what the user missed and what to review

The result is **on-demand learning** that fits into frontline schedules—fast, relevant, and always tied back to the source material.

## How we built it

We built **Frontline Academy** as a RAG-based web app using:

- **Streamlit** for the user-facing web interface (PDF upload, quiz configuration, quiz-taking UI, and feedback view)
- **FastAPI (Python)** as the backend service layer to handle document ingestion, retrieval, and quiz/feedback generation
- **MongoDB Atlas Vector Search** to store embeddings and perform fast semantic retrieval over PDF chunks
- **Gemini LLM API** to generate quiz questions from retrieved context and provide answer evaluation + feedback

### High-level flow

1. **PDF ingestion**
   - User uploads a PDF in Streamlit
   - Backend extracts text, chunks it into manageable sections, and attaches metadata (page numbers / section titles when available)

2. **Embeddings + storage**
   - Each chunk is converted into an embedding
   - Chunks + embeddings + metadata are stored in **MongoDB Atlas**
   - **Atlas Vector Search** indexes the embeddings for semantic retrieval

3. **Retrieval (RAG)**
   - When the user selects a quiz type and requirements, the backend:
     - builds a retrieval query based on the user’s intent (topic, difficulty, question style)
     - runs a **vector search** to fetch the most relevant chunks

4. **Quiz generation + grading**
   - Retrieved chunks are passed to **Gemini** with a structured prompt
   - Gemini generates quiz questions grounded in the retrieved content
   - After the user submits answers, Gemini evaluates responses and returns:
     - correct answers
     - explanations tied to source context
     - targeted feedback on gaps and misunderstandings

This architecture keeps the quiz content **grounded in the PDF**, while still being personalized to the frontline worker’s needs.

## Challenges we ran into

One of our biggest challenges was **retrieval quality**.

Frontline Academy depends on pulling the *right* PDF passages before generating a quiz, but we found it was difficult to reliably search a user’s quiz request **directly** in the database—especially when users described what they wanted in natural language (“make it scenario-based,” “focus on medication safety,” “hard questions from chapter 3,” etc.). Those requests often didn’t match the wording of the PDF, which led to weaker vector search results.

### How we solved it

To improve retrieval, we introduced an extra step:

- We use the LLM to **rewrite the user’s request into high-signal keywords and search phrases**
- Those keywords are then embedded and used as the query for **MongoDB Atlas Vector Search**
- This consistently pulled more relevant chunks, which made the generated quizzes more accurate, grounded, and aligned to the user’s intent

This shift—from “search the raw user prompt” to “search an LLM-generated keyword query”—significantly improved our end-to-end quiz quality.

## Accomplishments that we're proud of

- Built an end-to-end **RAG quiz pipeline**: PDF → chunking/embeddings → vector retrieval → quiz generation → grading + feedback.
- Delivered **personalized quiz creation** based on user-selected quiz type, difficulty, and focus areas—grounded in the uploaded document.
- Improved retrieval quality by adding an **LLM-powered keyword/query generation layer** before vector search.
- Created a simple, usable experience in **Streamlit** that makes training feel quick and interactive for busy frontline roles.

## What we learned

- Retrieval is everything: even a great model can’t help if the app pulls the wrong context.
- Users describe learning goals in natural language, so bridging the gap between **intent** and **document language** is critical.
- Good chunking + metadata dramatically improves relevance and explanations.
- Tight prompting + structured outputs make quiz generation and feedback far more consistent.

## What's next for Frontline Academy

- Add **role-specific quiz modes** (nurse vs teacher) with scenario templates and rubrics.
- Support **multi-document libraries** (upload once, quiz anytime) with tagging by topic/unit.
- Provide **citations to exact PDF sections/pages** in feedback for faster review.
- Add basic **progress tracking** (strengths/weaknesses) to guide what users should practice next.
