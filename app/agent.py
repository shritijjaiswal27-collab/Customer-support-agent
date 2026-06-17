# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.events.event import Event
from google.adk.workflow import Workflow
from google.genai import types

from app.tools import track_package, calculate_shipping_rates

# Setup environment variables safely for local execution
try:
    _, project_id = google.auth.default()
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
except Exception:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "mock-project")
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id

os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


class Classification(BaseModel):
    is_shipping_related: bool = Field(
        description="True if the user query is related to shipping (rates, tracking, delivery, returns, etc.), False if it is unrelated (general chat, jokes, other topics)."
    )
    explanation: str = Field(
        description="A short explanation of the classification decision."
    )


classify_agent = LlmAgent(
    name="classify_agent",
    model="gemini-flash-latest",
    instruction="""Analyze the user message and classify whether it is related to shipping.
Shipping-related queries include questions about rates, tracking, delivery status, shipping methods, returns, packaging, or similar topics.
Unrelated queries include greetings, general talk, questions about other topics, coding, math, history, weather, etc.
Provide your answer strictly matching the output schema.""",
    output_schema=Classification,
)


def route_classification(node_input: dict) -> Event:
    is_shipping = node_input.get("is_shipping_related", False)
    route = "shipping" if is_shipping else "unrelated"
    return Event(output=node_input, route=route)


shipping_faq_agent = LlmAgent(
    name="shipping_faq_agent",
    model="gemini-flash-latest",
    instruction="""You are a friendly customer support representative for a shipping company.
Answer the user's shipping-related questions using the available tools:
- For tracking questions, use the `track_package` tool.
- For rates questions, use the `calculate_shipping_rates` tool.
For other shipping questions (e.g. delivery procedures, returns), answer using simulated shipping company info. Be professional, helpful, and concise.""",
    tools=[track_package, calculate_shipping_rates],
)


def decline_node(node_input: dict) -> Event:
    msg = "I'm sorry, but I can only assist with shipping-related inquiries such as rates, tracking, delivery, and returns. How can I help you with your shipping needs today?"
    content = types.Content(role="model", parts=[types.Part.from_text(text=msg)])
    return Event(output=msg, content=content)


customer_support_workflow = Workflow(
    name="customer_support_workflow",
    edges=[
        ('START', classify_agent),
        (classify_agent, route_classification),
        (route_classification, {
            'shipping': shipping_faq_agent,
            'unrelated': decline_node
        }),
    ],
    description="Customer support workflow that routes shipping-related queries to FAQ and declines unrelated queries.",
)

root_agent = customer_support_workflow

app = App(
    root_agent=root_agent,
    name="app",
)
