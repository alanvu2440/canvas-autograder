import pytest
import os
from utils.grader import grade_python, grade_java, grade_cpp


class TestGradePython:
    """Tests for Python grading functionality."""

    def test_grade_python_all_pass(self, sample_python_script, sample_test_cases):
        """Test grading Python script where all test cases pass."""
        results, total_points, earned_points = grade_python(sample_python_script, sample_test_cases)

        assert len(results) == 2
        assert total_points == 25  # 10 + 15
        assert earned_points == 25  # All tests passed
        assert all(r["passed"] for r in results)
        assert results[0]["output"] == "hello"
        assert results[1]["output"] == "world"

    def test_grade_python_partial_pass(self, sample_python_script):
        """Test grading Python script where some test cases fail."""
        test_cases = [
            {"input": "hello", "expected_output": "hello", "points": 10},
            {"input": "world", "expected_output": "WRONG", "points": 15},
        ]
        results, total_points, earned_points = grade_python(sample_python_script, test_cases)

        assert len(results) == 2
        assert total_points == 25
        assert earned_points == 10  # Only first test passed
        assert results[0]["passed"] is True
        assert results[1]["passed"] is False

    def test_grade_python_all_fail(self, sample_python_script):
        """Test grading Python script where all test cases fail."""
        test_cases = [
            {"input": "hello", "expected_output": "WRONG1", "points": 10},
            {"input": "world", "expected_output": "WRONG2", "points": 15},
        ]
        results, total_points, earned_points = grade_python(sample_python_script, test_cases)

        assert len(results) == 2
        assert total_points == 25
        assert earned_points == 0
        assert not any(r["passed"] for r in results)

    def test_grade_python_with_addition(self, sample_python_add_script, sample_add_test_cases):
        """Test grading Python script that performs addition."""
        results, total_points, earned_points = grade_python(sample_python_add_script, sample_add_test_cases)

        assert len(results) == 2
        assert total_points == 25
        assert earned_points == 25
        assert all(r["passed"] for r in results)

    def test_grade_python_empty_test_cases(self, sample_python_script):
        """Test grading with empty test cases list."""
        results, total_points, earned_points = grade_python(sample_python_script, [])

        assert len(results) == 0
        assert total_points == 0
        assert earned_points == 0

    def test_grade_python_invalid_script(self, temp_dir):
        """Test grading with non-existent Python script."""
        fake_script = os.path.join(temp_dir, "fake.py")
        test_cases = [{"input": "test", "expected_output": "test", "points": 10}]

        results, total_points, earned_points = grade_python(fake_script, test_cases)

        assert len(results) == 1
        assert earned_points == 0
        assert results[0]["passed"] is False

    def test_grade_python_timeout(self, temp_dir):
        """Test grading Python script that takes too long."""
        script_path = os.path.join(temp_dir, "main.py")
        with open(script_path, "w") as f:
            f.write("""
import time
time.sleep(15)  # Longer than 10 second timeout
print("done")
""")

        test_cases = [{"input": "", "expected_output": "done", "points": 10}]
        results, total_points, earned_points = grade_python(script_path, test_cases)

        assert len(results) == 1
        assert earned_points == 0
        assert results[0]["passed"] is False
        assert "timeout" in results[0]["error"].lower()

    def test_grade_python_syntax_error(self, temp_dir):
        """Test grading Python script with syntax error."""
        script_path = os.path.join(temp_dir, "main.py")
        with open(script_path, "w") as f:
            f.write("print('missing closing quote)")

        test_cases = [{"input": "", "expected_output": "test", "points": 10}]
        results, total_points, earned_points = grade_python(script_path, test_cases)

        assert len(results) == 1
        assert earned_points == 0
        assert results[0]["passed"] is False


class TestGradeJava:
    """Tests for Java grading functionality."""

    def test_grade_java_all_pass(self, sample_java_script, temp_dir, sample_test_cases):
        """Test grading Java program where all test cases pass."""
        results, total_points, earned_points = grade_java(sample_java_script, temp_dir, sample_test_cases)

        assert len(results) == 2
        assert total_points == 25
        assert earned_points == 25
        assert all(r["passed"] for r in results)

    def test_grade_java_partial_pass(self, sample_java_script, temp_dir):
        """Test grading Java program where some test cases fail."""
        test_cases = [
            {"input": "hello", "expected_output": "hello", "points": 10},
            {"input": "world", "expected_output": "WRONG", "points": 15},
        ]
        results, total_points, earned_points = grade_java(sample_java_script, temp_dir, test_cases)

        assert len(results) == 2
        assert total_points == 25
        assert earned_points == 10

    def test_grade_java_compilation_error(self, temp_dir):
        """Test grading Java program with compilation error."""
        script_path = os.path.join(temp_dir, "Main.java")
        with open(script_path, "w") as f:
            f.write("""
public class Main {
    public static void main(String[] args) {
        System.out.println("missing semicolon")
    }
}
""")

        test_cases = [{"input": "test", "expected_output": "test", "points": 10}]

        with pytest.raises(Exception, match="Java compilation failed"):
            grade_java(script_path, temp_dir, test_cases)

    def test_grade_java_empty_test_cases(self, sample_java_script, temp_dir):
        """Test grading Java program with empty test cases."""
        results, total_points, earned_points = grade_java(sample_java_script, temp_dir, [])

        assert len(results) == 0
        assert total_points == 0
        assert earned_points == 0


class TestGradeCpp:
    """Tests for C++ grading functionality."""

    def test_grade_cpp_all_pass(self, sample_cpp_script, temp_dir, sample_test_cases):
        """Test grading C++ program where all test cases pass."""
        results, total_points, earned_points = grade_cpp(sample_cpp_script, temp_dir, sample_test_cases)

        assert len(results) == 2
        assert total_points == 25
        assert earned_points == 25
        assert all(r["passed"] for r in results)

    def test_grade_cpp_partial_pass(self, sample_cpp_script, temp_dir):
        """Test grading C++ program where some test cases fail."""
        test_cases = [
            {"input": "hello", "expected_output": "hello", "points": 10},
            {"input": "world", "expected_output": "WRONG", "points": 15},
        ]
        results, total_points, earned_points = grade_cpp(sample_cpp_script, temp_dir, test_cases)

        assert len(results) == 2
        assert total_points == 25
        assert earned_points == 10

    def test_grade_cpp_compilation_error(self, temp_dir):
        """Test grading C++ program with compilation error."""
        script_path = os.path.join(temp_dir, "main.cpp")
        with open(script_path, "w") as f:
            f.write("""
#include <iostream>
int main() {
    std::cout << "missing semicolon"
    return 0;
}
""")

        test_cases = [{"input": "test", "expected_output": "test", "points": 10}]

        with pytest.raises(Exception, match="C\\+\\+ compilation failed"):
            grade_cpp(script_path, temp_dir, test_cases)

    def test_grade_cpp_empty_test_cases(self, sample_cpp_script, temp_dir):
        """Test grading C++ program with empty test cases."""
        results, total_points, earned_points = grade_cpp(sample_cpp_script, temp_dir, [])

        assert len(results) == 0
        assert total_points == 0
        assert earned_points == 0

    def test_grade_cpp_runtime_error(self, temp_dir):
        """Test grading C++ program that crashes at runtime."""
        script_path = os.path.join(temp_dir, "main.cpp")
        with open(script_path, "w") as f:
            f.write("""
#include <iostream>
int main() {
    int* ptr = nullptr;
    *ptr = 5;  // Segmentation fault
    return 0;
}
""")

        test_cases = [{"input": "", "expected_output": "test", "points": 10}]
        results, total_points, earned_points = grade_cpp(script_path, temp_dir, test_cases)

        assert len(results) == 1
        assert earned_points == 0
        assert results[0]["passed"] is False


class TestGraderEdgeCases:
    """Tests for edge cases across all graders."""

    def test_points_calculation_with_zero_points(self, sample_python_script):
        """Test grading with test cases having zero points."""
        test_cases = [
            {"input": "hello", "expected_output": "hello", "points": 0},
            {"input": "world", "expected_output": "world", "points": 10},
        ]
        results, total_points, earned_points = grade_python(sample_python_script, test_cases)

        assert total_points == 10
        assert earned_points == 10

    def test_whitespace_handling(self, sample_python_script):
        """Test that output with extra whitespace is stripped correctly."""
        test_cases = [
            {"input": "hello", "expected_output": "hello", "points": 10},
        ]
        results, total_points, earned_points = grade_python(sample_python_script, test_cases)

        # The script outputs "hello" and it should match "hello" after stripping
        assert results[0]["passed"] is True

    def test_missing_points_field(self, sample_python_script):
        """Test grading with test cases missing points field (defaults to 1)."""
        test_cases = [
            {"input": "hello", "expected_output": "hello"},
            {"input": "world", "expected_output": "world"},
        ]
        results, total_points, earned_points = grade_python(sample_python_script, test_cases)

        assert total_points == 2  # Default 1 point per test case
        assert earned_points == 2
