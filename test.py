import unittest
from flask_testing import TestCase
from integration_and_api_development import app



class TestChatbotAPI(TestCase):
    # Set up the Flask app for testing
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_chatbot_query(self):
        # Test the chatbot query processing endint
        response = self.client.post(
            '/chatbot/query',
            json={"query": "Tell me about the latest tech news", "context": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json)

    def test_chain_of_thought(self):
        # Test Chain of Thought processing logic
        response = self.client.post(
            '/chatbot/query',
            json={"query": "How is the weather today?", "context": "Weather in New York"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json)
        self.assertIn("Given the context", response.json["response"])


# Run the tests
if __name__ == "__main__":
    unittest.main()
