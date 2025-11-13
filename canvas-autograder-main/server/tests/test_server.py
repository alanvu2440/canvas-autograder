import pytest
import json
import responses
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import server
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHelloEndpoint:
    """Tests for the /api/hello endpoint."""

    def test_hello_endpoint_success(self, client):
        """Test that the hello endpoint returns the correct message."""
        response = client.get('/api/hello')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Hello from Flask backend!"

    def test_hello_endpoint_method_not_allowed(self, client):
        """Test that POST method is not allowed on hello endpoint."""
        response = client.post('/api/hello')

        assert response.status_code == 405  # Method Not Allowed


class TestSubmitUrlEndpoint:
    """Tests for the /api/submit-url endpoint."""

    @patch('server.clone_repo')
    @patch('server.grade_python')
    @patch('server.get_last_commit_date')
    def test_submit_url_python_success(self, mock_get_commit, mock_grade, mock_clone, client, temp_dir):
        """Test successful submission with Python code."""
        # Setup mocks
        mock_clone.return_value = None
        mock_grade.return_value = (
            [
                {"input": "5 3", "expected_output": "8", "output": "8", "passed": True, "points": 10},
                {"input": "10 20", "expected_output": "30", "output": "30", "passed": True, "points": 15}
            ],
            25,  # total_points
            25   # earned_points
        )
        mock_get_commit.return_value = "2024-01-15T10:30:00Z"

        # Make request
        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [
                        {'input': '5 3', 'expected_output': '8', 'points': 10},
                        {'input': '10 20', 'expected_output': '30', 'points': 15}
                    ],
                    'language': 'python'
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Python test cases executed"
        assert data['score']['earned_points'] == 25
        assert data['score']['total_points'] == 25
        assert data['score']['percentage'] == 100.0
        assert data['last_commit_date'] == "2024-01-15T10:30:00Z"
        assert len(data['results']) == 2

    @patch('server.clone_repo')
    @patch('server.grade_java')
    @patch('server.get_last_commit_date')
    def test_submit_url_java_success(self, mock_get_commit, mock_grade, mock_clone, client):
        """Test successful submission with Java code."""
        mock_clone.return_value = None
        mock_grade.return_value = (
            [{"input": "test", "expected_output": "test", "output": "test", "passed": True, "points": 10}],
            10,
            10
        )
        mock_get_commit.return_value = "2024-01-15T10:30:00Z"

        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}],
                    'language': 'java'
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Java test cases executed"

    @patch('server.clone_repo')
    @patch('server.grade_cpp')
    @patch('server.get_last_commit_date')
    def test_submit_url_cpp_success(self, mock_get_commit, mock_grade, mock_clone, client):
        """Test successful submission with C++ code."""
        mock_clone.return_value = None
        mock_grade.return_value = (
            [{"input": "test", "expected_output": "test", "output": "test", "passed": True, "points": 10}],
            10,
            10
        )
        mock_get_commit.return_value = "2024-01-15T10:30:00Z"

        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}],
                    'language': 'cpp'
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "C++ test cases executed"

    def test_submit_url_no_url_provided(self, client):
        """Test submission with no URL."""
        response = client.post(
            '/api/submit-url',
            data=json.dumps({
                'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}]
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['message'] == "No URL provided"

    def test_submit_url_test_cases_not_list(self, client):
        """Test submission with test_cases not being a list."""
        response = client.post(
            '/api/submit-url',
            data=json.dumps({
                'url': 'https://github.com/test/repo',
                'test_cases': 'not a list'
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['message'] == "Test cases must be a list"

    @patch('server.clone_repo')
    def test_submit_url_clone_fails(self, mock_clone, client):
        """Test submission when repository cloning fails."""
        mock_clone.side_effect = Exception("Failed to clone repository")

        response = client.post(
            '/api/submit-url',
            data=json.dumps({
                'url': 'https://github.com/test/invalid-repo',
                'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}]
            }),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Failed to clone repo" in data['message']

    @patch('server.clone_repo')
    @patch('server.get_last_commit_date')
    def test_submit_url_main_file_not_found(self, mock_get_commit, mock_clone, client):
        """Test submission when main file is not found."""
        mock_clone.return_value = None
        mock_get_commit.return_value = None

        with patch('os.path.exists', return_value=False):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}],
                    'language': 'python'
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "main.py or Main.java not found" in data['message']
        assert data['score']['earned_points'] == 0
        assert data['score']['total_points'] == 0

    @patch('server.clone_repo')
    @patch('server.grade_python')
    @patch('server.get_last_commit_date')
    def test_submit_url_grading_exception(self, mock_get_commit, mock_grade, mock_clone, client):
        """Test submission when grading raises an exception."""
        mock_clone.return_value = None
        mock_grade.side_effect = Exception("Grading error occurred")
        mock_get_commit.return_value = None

        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}],
                    'language': 'python'
                }),
                content_type='application/json'
            )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Grading error occurred" in data['message']

    @patch('server.clone_repo')
    @patch('server.grade_python')
    @patch('server.get_last_commit_date')
    def test_submit_url_partial_pass(self, mock_get_commit, mock_grade, mock_clone, client):
        """Test submission where only some test cases pass."""
        mock_clone.return_value = None
        mock_grade.return_value = (
            [
                {"input": "5 3", "expected_output": "8", "output": "8", "passed": True, "points": 10},
                {"input": "10 20", "expected_output": "30", "output": "25", "passed": False, "points": 15}
            ],
            25,  # total_points
            10   # earned_points (only first test passed)
        )
        mock_get_commit.return_value = "2024-01-15T10:30:00Z"

        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [
                        {'input': '5 3', 'expected_output': '8', 'points': 10},
                        {'input': '10 20', 'expected_output': '30', 'points': 15}
                    ],
                    'language': 'python'
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['score']['earned_points'] == 10
        assert data['score']['total_points'] == 25
        assert data['score']['percentage'] == 40.0

    @patch('server.clone_repo')
    @patch('server.grade_python')
    @patch('server.get_last_commit_date')
    def test_submit_url_zero_total_points(self, mock_get_commit, mock_grade, mock_clone, client):
        """Test submission with zero total points."""
        mock_clone.return_value = None
        mock_grade.return_value = ([], 0, 0)
        mock_get_commit.return_value = None

        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [],
                    'language': 'python'
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['score']['percentage'] == 0

    def test_submit_url_method_not_allowed(self, client):
        """Test that GET method is not allowed on submit-url endpoint."""
        response = client.get('/api/submit-url')

        assert response.status_code == 405

    def test_submit_url_empty_json(self, client):
        """Test submission with empty JSON body."""
        response = client.post(
            '/api/submit-url',
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_submit_url_no_json(self, client):
        """Test submission with no JSON body."""
        response = client.post('/api/submit-url')

        assert response.status_code == 400

    @patch('server.clone_repo')
    @patch('server.grade_python')
    @patch('server.get_last_commit_date')
    def test_submit_url_default_language(self, mock_get_commit, mock_grade, mock_clone, client):
        """Test that language defaults to 'python' if not specified."""
        mock_clone.return_value = None
        mock_grade.return_value = (
            [{"input": "test", "expected_output": "test", "output": "test", "passed": True, "points": 10}],
            10,
            10
        )
        mock_get_commit.return_value = None

        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}]
                    # No language specified
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        # Should use Python by default
        mock_grade.assert_called_once()


class TestServerEdgeCases:
    """Tests for edge cases and error handling."""

    def test_invalid_endpoint(self, client):
        """Test accessing a non-existent endpoint."""
        response = client.get('/api/nonexistent')

        assert response.status_code == 404

    @patch('server.clone_repo')
    @patch('server.grade_python')
    @patch('server.get_last_commit_date')
    def test_submit_url_commit_date_none(self, mock_get_commit, mock_grade, mock_clone, client):
        """Test submission when commit date cannot be retrieved."""
        mock_clone.return_value = None
        mock_grade.return_value = (
            [{"input": "test", "expected_output": "test", "output": "test", "passed": True, "points": 10}],
            10,
            10
        )
        mock_get_commit.return_value = None

        with patch('os.path.exists', return_value=True):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}],
                    'language': 'python'
                }),
                content_type='application/json'
            )

        assert response.status_code == 200
        data = json.loads(response.data)
        # last_commit_date should be None
        assert data['last_commit_date'] is None

    @patch('server.clone_repo')
    @patch('server.get_last_commit_date')
    def test_submit_url_unsupported_language(self, mock_get_commit, mock_clone, client):
        """Test submission with unsupported programming language."""
        mock_clone.return_value = None
        mock_get_commit.return_value = None

        with patch('os.path.exists', return_value=False):
            response = client.post(
                '/api/submit-url',
                data=json.dumps({
                    'url': 'https://github.com/test/repo',
                    'test_cases': [{'input': 'test', 'expected_output': 'test', 'points': 10}],
                    'language': 'ruby'  # Unsupported language
                }),
                content_type='application/json'
            )

        # Should return 200 but with error message
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "main.py or Main.java not found" in data['message']
