import pytest
import os
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_python_script(temp_dir):
    """Create a sample Python script that reads input and prints it."""
    script_path = os.path.join(temp_dir, "main.py")
    with open(script_path, "w") as f:
        f.write("""
user_input = input()
print(user_input)
""")
    return script_path


@pytest.fixture
def sample_python_add_script(temp_dir):
    """Create a sample Python script that adds two numbers."""
    script_path = os.path.join(temp_dir, "main.py")
    with open(script_path, "w") as f:
        f.write("""
a, b = map(int, input().split())
print(a + b)
""")
    return script_path


@pytest.fixture
def sample_java_script(temp_dir):
    """Create a sample Java program that reads input and prints it."""
    script_path = os.path.join(temp_dir, "Main.java")
    with open(script_path, "w") as f:
        f.write("""
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input = scanner.nextLine();
        System.out.println(input);
        scanner.close();
    }
}
""")
    return script_path


@pytest.fixture
def sample_cpp_script(temp_dir):
    """Create a sample C++ program that reads input and prints it."""
    script_path = os.path.join(temp_dir, "main.cpp")
    with open(script_path, "w") as f:
        f.write("""
#include <iostream>
#include <string>
using namespace std;

int main() {
    string input;
    getline(cin, input);
    cout << input << endl;
    return 0;
}
""")
    return script_path


@pytest.fixture
def sample_test_cases():
    """Sample test cases for grading."""
    return [
        {"input": "hello", "expected_output": "hello", "points": 10},
        {"input": "world", "expected_output": "world", "points": 15},
    ]


@pytest.fixture
def sample_add_test_cases():
    """Sample test cases for addition program."""
    return [
        {"input": "5 3", "expected_output": "8", "points": 10},
        {"input": "10 20", "expected_output": "30", "points": 15},
    ]
