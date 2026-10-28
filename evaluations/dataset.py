from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall

dataset = EvaluationDataset(
    goldens=[
        Golden(
            input="I am user123, I want a refund for my pen and book",
            expected_output="A refund ticket of 28$ has been issued successfully for user123",
            expected_tools=[
                ToolCall(name="get_user_order_history",input_parameters={"user":"user123"}  ),
                ToolCall(name="calculate_right_refund_amount",input_parameters={"user":"user123","items":[{"name":"book"},{"name":"pen"}]}),
                ToolCall(name="issue_refund_ticket",input_parameters={"user":"user123", "refund_amount": 30}),
                ToolCall(name="get_today_date",input_parameters={}),
            ]
        ),
        Golden(
            input="I am user123, I want a refund for book",
            expected_output="A refund ticket of 21$ has been issued successfully for user123",
            expected_tools=[
                ToolCall(name="get_user_order_history",input_parameters={"user":"user123"}),
                ToolCall(name="calculate_right_refund_amount",input_parameters={"user":"user123","items":[{"name":"book"}]}),
                ToolCall(name="issue_refund_ticket",input_parameters={"user":"user123", "refund_amount": 21}),
                ToolCall(name="get_today_date",input_parameters={}),
            ]
        ),
        Golden(
            input="I am user123, I don't want a refund, I just want to know what I purchased",
            expected_output="You purchased a book and a pen.",
            expected_tools=[
                ToolCall(name="get_user_order_history",input_parameters={"user":"user123"}),
            ]
        ),
        Golden(
            input="I am a user342, I want a refund for book",
            expected_output="Tell the user that username is invalid and ask him/her to provide a valid username",
            expected_tools=[
                ToolCall(name="get_user_order_history",input_parameters={"user":"user342"})
            ]
        ),
        Golden(
            input="I am user126, I want a refund for water_bottle",
            expected_output="No refund beacuse purchase date is more than 30 days ago. No refund ticket was issued.",
            expected_tools=[
                ToolCall(name="get_user_order_history",input_parameters={"user":"user126"}),
                ToolCall(name="get_today_date",input_parameters={}),
            ]
        ),
        Golden(
            input="I am user126, I want a refund for water_bottle and backpack",
            expected_output="A refund ticket of 45$ has been issued successfully for backpack, however, no refund for water_bottle because purchase date is more than 30 days ago.",
            expected_tools=[
                ToolCall(name="get_user_order_history",input_parameters={"user":"user126"}),
                ToolCall(name="calculate_right_refund_amount",input_parameters={"user":"user126","items":[{"name":"backpack"}]}),
                ToolCall(name="issue_refund_ticket",input_parameters={"user":"user126", "refund_amount": 45}),
                ToolCall(name="get_today_date",input_parameters={}),
            ]
        ),
        Golden(
            input="I am user126, I want a refund for sneakers",
            expected_output="No refund issued as you haven't bought sneakers.",
            expected_tools=[
                ToolCall(name="get_user_order_history",input_parameters={"user":"user126"}),
            ]
        )
    ]
)