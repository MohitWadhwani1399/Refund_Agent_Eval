import sys
from pathlib import Path
from uuid import uuid4

from deepeval import evaluate
from deepeval.test_case import LLMTestCase, ToolCall

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))

from agent import agent
from dataset import dataset
from model import eval_model

from deepeval.metrics import ToolCorrectnessMetric
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
        expected_tools=golden.expected_tools,
        tools_called=tools_called
    )
    dataset.add_test_case(test_case)            


metrics = [ToolCorrectnessMetric(threshold=0.8,model=eval_model, include_reason=True)]
evaluate(test_cases=dataset.test_cases, metrics=metrics)
