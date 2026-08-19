# Product Decisions — UPSC AI

## 1. Approach

I chose to evolve an existing RAG-based UPSC assistant into a
premium product experience instead of rebuilding the underlying
AI system from scratch.

The existing application uses a focused UPSC knowledge base,
embeddings, similarity-based retrieval, and Ollama for response
generation.

The redesign focuses on presenting this functionality as a
clearer product experience with:

- A focused hero section
- A clear value proposition
- A primary CTA
- A product preview
- A simple explanation of the RAG workflow
- The actual UPSC AI assistant
- Responsive desktop and mobile layouts

## 2. Product Trade-offs

The main trade-off was prioritizing the user-facing experience
and clarity of the product within the available time rather than
introducing unnecessary backend complexity.

I kept the existing retrieval pipeline because it was already
functional and allowed the redesign to focus on usability,
presentation, and product communication.

The interface intentionally avoids fabricated user counts,
testimonials, logos, or unsupported performance claims.

## 3. AI Assistance

AI tools were used as implementation and iteration assistance
during development.

They helped with areas such as:

- UI structure
- CSS and responsive layout ideas
- Code organization
- Debugging
- Documentation

The resulting implementation was reviewed and tested manually,
including the existing RAG workflow and responsive layouts.

## 4. What I Would Improve With More Time

With additional time, I would improve:

1. Production deployment of the inference layer.
2. Better document ingestion and chunking.
3. Persistent vector storage instead of rebuilding embeddings.
4. More robust error handling when the model service is unavailable.
5. Evaluation of retrieval quality using a small benchmark set.
6. Authentication and user-specific history if required.
7. More extensive accessibility and cross-browser testing.

## 5. Key Design Principle

The redesign was guided by one principle:

Make the AI capability understandable before making the
interface complicated.

The homepage therefore explains the workflow while allowing
the user to reach the actual product quickly.