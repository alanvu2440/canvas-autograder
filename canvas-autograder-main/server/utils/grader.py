import os
import subprocess

def grade_python(main_py, test_cases):
    results = []
    total_points = 0
    earned_points = 0
    for case in test_cases:
        input_data = case.get("input", "")
        expected_output = str(case.get("expected_output", "")).strip()
        points = int(case.get("points", 1))
        total_points += points
        try:
            result = subprocess.run(
                ["python3", main_py],
                input=str(input_data),
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout.strip()
            error = result.stderr if result.stderr else "no error"
            passed = output == expected_output
            if passed:
                earned_points += points
        except Exception as e:
            output = ""
            error = str(e)
            passed = False
        results.append({
            "input": input_data,
            "expected_output": expected_output,
            "output": output,
            "error": error,
            "points": points,
            "passed": passed
        })
    return results, total_points, earned_points

def grade_java(main_java, repo_dir, test_cases):
    results = []
    total_points = 0
    earned_points = 0
    # Compile Java
    compile_proc = subprocess.run(
        ["javac", "Main.java"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    if compile_proc.returncode != 0:
        raise Exception(f"Java compilation failed: {compile_proc.stderr}")
    for case in test_cases:
        input_data = case.get("input", "")
        expected_output = str(case.get("expected_output", "")).strip()
        points = int(case.get("points", 1))
        total_points += points
        try:
            result = subprocess.run(
                ["java", "Main"],
                input=str(input_data),
                capture_output=True,
                text=True,
                timeout=10,
                cwd=repo_dir
            )
            output = result.stdout.strip()
            error = result.stderr if result.stderr else "no error"
            passed = output == expected_output
            if passed:
                earned_points += points
        except Exception as e:
            output = ""
            error = str(e)
            passed = False
        results.append({
            "input": input_data,
            "expected_output": expected_output,
            "output": output,
            "error": error,
            "points": points,
            "passed": passed
        })
    return results, total_points, earned_points

def grade_cpp(main_cpp, repo_dir, test_cases):
    results = []
    total_points = 0
    earned_points = 0

    # Compile C++
    executable = "main_cpp_exe"
    compile_proc = subprocess.run(
        ["g++", "main.cpp", "-o", executable],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    if compile_proc.returncode != 0:
        raise Exception(f"C++ compilation failed: {compile_proc.stderr}")

    # Run test cases
    for case in test_cases:
        input_data = case.get("input", "")
        expected_output = str(case.get("expected_output", "")).strip()
        points = int(case.get("points", 1))
        total_points += points
        try:
            result = subprocess.run(
                ["./" + executable],
                input=str(input_data),
                capture_output=True,
                text=True,
                timeout=10,
                cwd=repo_dir
            )
            output = result.stdout.strip()
            error = result.stderr if result.stderr else "no error"
            passed = output == expected_output
            if passed:
                earned_points += points
        except Exception as e:
            output = ""
            error = str(e)
            passed = False
        results.append({
            "input": input_data,
            "expected_output": expected_output,
            "output": output,
            "error": error,
            "points": points,
            "passed": passed
        })

    return results, total_points, earned_points
