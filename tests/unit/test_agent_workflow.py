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
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from google.adk.runners import InMemoryRunner
from google.genai import types


class MockGenerateContentResponse:
    def __init__(self, text: str):
        self.text = text
        self.usage_metadata = None
        self.model_version = None
        self.candidates = [
            MagicMock(
                content=types.Content(
                    parts=[types.Part(text=text)]
                )
            )
        ]

    def __getattr__(self, name):
        return None


@pytest.mark.asyncio
async def test_shipping_query_routing():
    """Verify that shipping-related queries route to the FAQ agent and use tools."""
    mock_class_response = MockGenerateContentResponse(
        '{"is_shipping_related": true, "explanation": "User wants to track package."}'
    )
    mock_faq_response = MockGenerateContentResponse(
        "Your package 12345 is in transit."
    )

    async def mock_generate_content(*args, **kwargs):
        config = kwargs.get("config")
        system_instruction = getattr(config, "system_instruction", None)
        inst_str = ""
        if system_instruction:
            if isinstance(system_instruction, str):
                inst_str = system_instruction
            else:
                inst_str = "".join(p.text for p in getattr(system_instruction, "parts", []) if p.text)

        if "classify" in inst_str.lower():
            return mock_class_response
        else:
            return mock_faq_response

    with patch("google.genai.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.aio.models.generate_content = AsyncMock(side_effect=mock_generate_content)

        from app.agent import app
        runner = InMemoryRunner(app=app)

        with patch.dict(os.environ, {"GOOGLE_GENAI_USE_VERTEXAI": "False", "GEMINI_API_KEY": "mock_key"}):
            session = await runner.session_service.create_session(app_name="app", user_id="test_user")
            
            outputs = []
            async for event in runner.run_async(
                user_id="test_user",
                session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part.from_text(text="Where is package 12345?")]),
            ):
                if event.output is not None:
                    outputs.append(event.output)

            assert any("in transit" in str(out) for out in outputs)


@pytest.mark.asyncio
async def test_unrelated_query_routing():
    """Verify that unrelated queries route to the decline node."""
    mock_class_response = MockGenerateContentResponse(
        '{"is_shipping_related": false, "explanation": "User asks about unrelated topic."}'
    )

    async def mock_generate_content(*args, **kwargs):
        return mock_class_response

    with patch("google.genai.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.aio.models.generate_content = AsyncMock(side_effect=mock_generate_content)

        from app.agent import app
        runner = InMemoryRunner(app=app)

        with patch.dict(os.environ, {"GOOGLE_GENAI_USE_VERTEXAI": "False", "GEMINI_API_KEY": "mock_key"}):
            session = await runner.session_service.create_session(app_name="app", user_id="test_user")
            
            outputs = []
            async for event in runner.run_async(
                user_id="test_user",
                session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part.from_text(text="What is the capital of France?")]),
            ):
                if event.output is not None:
                    outputs.append(event.output)

            assert any("only assist with shipping-related inquiries" in str(out) for out in outputs)
