import asyncio
import httpx

# You must first start the server and then run this script
# poetry run uvicorn main:app --host 0.0.0.0 --port 8000


async def test_main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/ad/request/v2",
            json={
                "publisher": {
                    "publisher_id": 6,
                    "publisher_name": "Botify",
                    "publisher_type": "chatbot",
                },
                "visitor": {
                    "pub_user_id": "user123",
                    "email": "test@example.com",
                    "session_id": "session123",
                    "browser_id": "browser123",
                    "user_agent": "Mozilla/5.0",
                    "ip": "127.0.0.1",
                    "language": "en-US",
                },
                "chatbot_context": {
                    "bot_name": "TestBot",
                    "bot_description": "A test bot",
                    "topic": "general",
                    "conversations": [
                        {
                            "timestamp": 1626262626,
                            "role": "user",
                            "content": "Hello, how are you?",
                        },
                        {
                            "timestamp": 1626262627,
                            "role": "assistant",
                            "content": "I'''m doing well, thank you for asking!",
                        },
                    ],
                },
                "slots": [
                    {
                        "slot_id": 789,
                        "slot_name": "test_slot",
                        "formats": [{"width": 300, "height": 250}],
                    }
                ],
            },
        )

        print(response.json())


if __name__ == "__main__":
    asyncio.run(test_main())
