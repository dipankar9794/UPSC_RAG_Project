import ollama
LANGUAGE_MODEL = "llama3"
EMBEDDING_MODEL = "nomic-embed-text"


with open(
    "D:/summer/project genai/upsc.txt",
    "r",
    encoding="utf-8",
    errors="ignore"
) as f:

    dataset = f.readlines()


print(f"Loaded {len(dataset)} UPSC knowledge records")


VECTOR_DB = []


def add_chunk_to_database(chunk):

    embedding = ollama.embed(
        model=EMBEDDING_MODEL,
        input=chunk
    )['embeddings'][0]


    VECTOR_DB.append(
        (chunk, embedding)
    )



for i, chunk in enumerate(dataset):

    add_chunk_to_database(chunk)

    print(
        f'Added chunk {i+1}/{len(dataset)} to the database'
    )



import math
def cosine_similarity(a, b):

    dot_product = sum(
        x * y 
        for x, y in zip(a, b)
    )


    norm_a = math.sqrt(
        sum(
            x * x 
            for x in a
        )
    )


    norm_b = math.sqrt(
        sum(
            y * y 
            for y in b
        )
    )


    if norm_a == 0 or norm_b == 0:

        return 0


    return dot_product / (norm_a * norm_b)




def retrieve(query, top_n=3):

    query_embedding = ollama.embed(
        model=EMBEDDING_MODEL,
        input=query
    )['embeddings'][0]


    similarities = []


    for chunk, embedding in VECTOR_DB:


        similarity = cosine_similarity(
            query_embedding,
            embedding
        )


        similarities.append(
            (chunk, similarity)
        )


    similarities.sort(
        key=lambda x: x[1],
        reverse=True
    )


    return similarities[:top_n]





input_query = input(
    'Ask me a question related to UPSC: '
)



retrieved_knowledge = retrieve(input_query)



print('Retrieved UPSC knowledge:')


for chunk, similarity in retrieved_knowledge:

    print(
        f' - (similarity: {similarity:.2f}) {chunk}'
    )




instruction_prompt = f'''
You are a helpful UPSC exam assistant.

Use only the following pieces of context to answer the question.
Don't make up any new information.

Context:

{'\n'.join(
    [
        f' - {chunk}' 
        for chunk, similarity in retrieved_knowledge
    ]
)}
'''



stream = ollama.chat(

    model=LANGUAGE_MODEL,

    messages=[

        {
            'role': 'system',
            'content': instruction_prompt
        },

        {
            'role': 'user',
            'content': input_query
        }

    ],

    stream=True,

)



print('UPSC Chatbot response:')


for chunk in stream:

    print(
        chunk['message']['content'],
        end='',
        flush=True
    )