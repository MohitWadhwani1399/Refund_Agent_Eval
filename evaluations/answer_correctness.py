import sys
from pathlib import Path
from uuid import uuid4

from deepeval import evaluate
from deepeval.test_case import LLMTestCase, SingleTurnParams, ToolCall

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))

from agent import agent
from dataset import dataset
from model import eval_model

from deepeval.metrics import GEval
from deepeval.integrations.langchain import CallbackHandler


for golden in dataset.goldens:
    response = agent.invoke(
        {"messages":[{"role":"user","content":golden.input}]},
        config={"configurable":{"thread_id": str(uuid4())}, "callbacks": [CallbackHandler()]}
    )

    actual_output = response["structured_response"].answer
    tools_called = []

    for message in response["messages"]:
        for tool_call in getattr(message, "tool_calls", []) or []:        
            tools_called.append(ToolCall(name=tool_call["name"], input_parameters=tool_call["args"]))


    # Deterministic Test Case Generation
    test_case = LLMTestCase(
        input=golden.input,
        actual_output=actual_output,
        expected_output=golden.expected_output,
    )
    dataset.add_test_case(test_case)            


metrics = [GEval(
    name="answer_correctness",
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ],
    evaluation_steps=[
        "Make Sure that actual output is semantically equivalent to expected output.",        
    ],
    threshold=0.8,
    model=eval_model,
    verbose_mode=True
)]
evaluate(test_cases=dataset.test_cases, metrics=metrics)
