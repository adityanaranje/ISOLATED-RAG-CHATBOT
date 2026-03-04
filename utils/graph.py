from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from utils.retrieval import get_retriever
from utils.config import llm
from langchain_core.documents import Document


class GraphState(TypedDict):
    query : str
    context : List[Document]
    answer: str
    rag_needed: bool
    complete_context : List[Document]
    partial_context : List[Document]
    zero_related: bool
    answer_related:bool
    max_tries: int
    bot_id: str


def is_rag_needed(state:GraphState):
    query  = state["query"]

    prompt = f"""
    You are provided query from user.
    Check whether retrieval is needed for the given query.
    Query:
    {query}
    Return only True or False in one word.
    """
    ragNeeded = llm.invoke(prompt)
    return {"rag_needed":ragNeeded.content.strip().lower() == 'true'}


def complete_retrival(state:GraphState):
    context = "\n\n".join([d.page_content for d in state['complete_context']])

    prompt = f'''
    You are a helpful assistant.
    Answer only from the provided context.
    If answer not found, say "I don't know".

    Context:
    {context}

    Question:
    {state['query']}
    '''

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "context": state['context']
    }


def direct_llm_answer(state:GraphState):
    prompt = f'''
    You are a helpful assistant.
    Answer the following query in summarise way.
    If answer not found, say "I don't know".


    Question:
    {state['query']}
    '''

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


def partial_retrival(state:GraphState):
    context = "\n\n".join([d.page_content for d in state['partial_context']])

    prompt = f'''
    You are a helpful assistant.
    Answer from the provided context and your knowledge.
    If answer not found, say "I don't know".

    Context:
    {context}

    Question:
    {state['query']}
    '''

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "context": state['context']
    }


def retrieveVectors(state:GraphState):
    retriever = get_retriever(state['bot_id'])
    docs = retriever.invoke(state['query'])
    return {
        "context": docs
    }


def check_retrieved_context(state: GraphState):

    complete_context = []
    partial_context = []

    for doc in state["context"]:
        text = doc.page_content

        prompt = f"""
        Score how useful this CONTEXT is for answering the QUERY.
        Return ONLY a number between 0 and 1.

        Query:
        {state['query']}

        Context:
        {text}
        """

        score_response = llm.invoke(prompt)

        try:
            score = float(score_response.content.strip())
        except:
            score = 0.0

        if score >= 0.8:
            complete_context.append(doc)
        elif score >= 0.4:
            partial_context.append(doc)

    return {
        "complete_context": complete_context,
        "partial_context": partial_context,
        "zero_related": len(complete_context) == 0 and len(partial_context) == 0
    }

def answer_related(state:GraphState):
    prompt = f'''
    You are a question answer expert.
    Based on below query and answer tell is the answer related to query.
    Return only True or False in one word.

    Response should be one word only.
    Query:
    {state["query"]}

    Answer:
    {state['answer']}
    '''
    response = llm.invoke(prompt)

    return {
        "answer_related": response.content
    }


def maximum_tries(state: GraphState):
    return {
        "max_tries": state["max_tries"] + 1
    }


def route_rag1(state:GraphState):
    return 'True' if state['rag_needed'] else 'False'

def route_rag2(state:GraphState):
    if len(state['complete_context']) > 0:
        response = 'Complete Retrival'
    elif len(state['partial_context']) >0:
        response = 'Partial Retrival'
    else:
        response = 'Zero Related'
    return response

def route_rag3(state:GraphState):
    return 'Yes' if str(state['answer_related']).strip().lower() == 'true' else 'No'



def route_rag4(state:GraphState):
    return '>=3' if state['max_tries']>=3 else '<3'


def get_graph():
    builder = StateGraph(GraphState)

    builder.add_node("isRagNeeded",is_rag_needed)
    builder.add_node("retrieveVectors", retrieveVectors)
    builder.add_node("checkRetrieve", check_retrieved_context)
    builder.add_node("completeRetrival", complete_retrival)
    builder.add_node("partialRetrival", partial_retrival)
    builder.add_node("directllm", direct_llm_answer)
    builder.add_node("answerRelated", answer_related)
    builder.add_node("maxTries", maximum_tries)

    builder.set_entry_point("isRagNeeded")

    builder.add_conditional_edges(
        "isRagNeeded",
        route_rag1,
        {
            'True':'retrieveVectors',
            'False':'directllm'
        }
    )

    builder.add_edge('retrieveVectors', 'checkRetrieve')

    builder.add_conditional_edges(
        "checkRetrieve",
        route_rag2,
        {
            "Complete Retrival":"completeRetrival",
            "Partial Retrival":"partialRetrival",
            "Zero Related":"directllm"
        }
    )

    builder.add_edge('completeRetrival', "answerRelated")
    builder.add_edge('partialRetrival', "answerRelated")
    builder.add_edge('directllm', "answerRelated")

    builder.add_conditional_edges(
        "answerRelated",
        route_rag3,
        {
            'Yes':END,
            'No':"maxTries"
        }
    )

    builder.add_conditional_edges(
        "maxTries",
        route_rag4,
        {
            ">=3" : END,
            "<3":"retrieveVectors"
        }
    )
    
    return builder.compile()