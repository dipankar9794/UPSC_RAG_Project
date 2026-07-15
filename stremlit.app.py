import streamlit as st
import ollama
import os
import math


st.set_page_config(
    page_title="UPSC Exam Assistant",
    layout="centered"
)


st.title("📚 UPSC Exam Information Assistant")


st.write("""
Welcome to the **UPSC Exam Information Assistant** powered by 
**Ollama + Retrieval Augmented Generation (RAG)**.

Ask questions related to:

- UPSC Exam Details - Syllabus- Eligibility Criteria- Age Limit- Attempts- Exam Pattern- IAS, IPS, IFS- Selection Process- Preparation Information
""")


EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3"
DATASET_PATH = "D:/summer/project genai/upsc.txt"

def create_chunks(text, chunk_size=500):

    words = text.split()

    chunks = []

    current_chunk = []

    current_length = 0


    for word in words:

        current_chunk.append(word)

        current_length += len(word)


        if current_length >= chunk_size:

            chunks.append(
                " ".join(current_chunk)
            )

            current_chunk = []

            current_length = 0



    if current_chunk:

        chunks.append(
            " ".join(current_chunk)
        )


    return chunks


@st.cache_resource
def initialize_vector_db():


    if not os.path.exists(DATASET_PATH):

        st.error(
            "UPSC dataset file not found!"
        )

        return []



    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        text = file.read()



    dataset = create_chunks(text)



    vector_db = []


    progress_bar = st.progress(0)

    status_text = st.empty()



    for i, chunk in enumerate(dataset):


        status_text.text(
            f"Generating embedding {i+1}/{len(dataset)}..."
        )


        try:

            response = ollama.embed(

                model=EMBEDDING_MODEL,

                input=chunk

            )


            embedding = response.embeddings[0]



            vector_db.append(

                (
                    chunk,
                    embedding
                )

            )


        except Exception as e:

            st.error(
                f"Ollama Embedding Error: {e}"
            )

            return []



        progress_bar.progress(
            (i+1)/len(dataset)
        )



    progress_bar.empty()

    status_text.empty()


    return vector_db


with st.spinner(
    "Loading UPSC Knowledge Base..."
):

    VECTOR_DB = initialize_vector_db()




def cosine_similarity(a,b):


    dot_product = sum(
        x*y for x,y in zip(a,b)
    )


    norm_a = math.sqrt(
        sum(
            x*x for x in a
        )
    )


    norm_b = math.sqrt(
        sum(
            y*y for y in b
        )
    )


    if norm_a == 0 or norm_b == 0:

        return 0



    return dot_product/(norm_a*norm_b)



def retrieve(query, top_n=3):


    response = ollama.embed(

        model=EMBEDDING_MODEL,

        input=query

    )


    query_embedding = response.embeddings[0]



    similarities = []



    for chunk, embedding in VECTOR_DB:


        score = cosine_similarity(

            query_embedding,

            embedding

        )


        similarities.append(

            (
                chunk,
                score
            )

        )



    similarities.sort(

        key=lambda x:x[1],

        reverse=True

    )



    return similarities[:top_n]



with st.sidebar:


    st.header("📖 UPSC Knowledge Base")


    st.success(

        f"Loaded {len(VECTOR_DB)} UPSC knowledge chunks"

    )


    st.markdown("---")


    st.subheader(
        "Retrieved Context"
    )


    context_placeholder = st.empty()


    context_placeholder.info(

        "Relevant UPSC information will appear here."

    )



input_query = st.text_input(

    "ASK UPSC RELATED QUESTIONS:",

    placeholder="Example: What is UPSC eligibility criteria?"

)




if input_query:


    retrieved_knowledge = retrieve(input_query)



    with context_placeholder.container():


        for i, (chunk, similarity) in enumerate(retrieved_knowledge):


            st.write(
                f"**Result {i+1}**"
            )


            st.write(
                f"Similarity Score: `{similarity:.4f}`"
            )


            

            st.write(
                chunk[:300] + "..."
            )


            st.markdown("---")





    context = "\n\n".join(

        [

            chunk

            for chunk, similarity in retrieved_knowledge

        ]

    )





    instruction_prompt = f"""

You are a UPSC Exam Assistant.

Answer the user only using the provided context.

Do not create or assume information.

If information is not available, reply:

"I don't have enough information in my knowledge base."


Context:

{context}

"""





    st.subheader(
        "🤖 UPSC Assistant Response"
    )



    response_placeholder = st.empty()


    full_response = ""



    try:


        stream = ollama.chat(

            model=LANGUAGE_MODEL,


            messages=[


                {

                    "role":"system",

                    "content":instruction_prompt

                },


                {

                    "role":"user",

                    "content":input_query

                }


            ],


            stream=True

        )



        for chunk in stream:


            token = chunk["message"]["content"]


            full_response += token



            response_placeholder.markdown(

                full_response + "▌"

            )



        response_placeholder.markdown(
            full_response
        )



    except Exception as e:


        st.error(
            f"LLM Error: {e}"
        )