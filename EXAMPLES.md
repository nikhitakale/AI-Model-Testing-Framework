# Example Test Outputs

This document shows examples of what the framework produces.

## 1. CLI Output Examples

### Testing LLM Inference
```bash
$ python cli/main.py test-llm --model gpt-3.5-turbo --prompt "What is AI?"

Test: inference_test
Status: passed
Message: Generated response: Artificial Intelligence (AI) refers to the simulation of human intelligence...

Response:
Artificial Intelligence (AI) refers to the simulation of human intelligence in machines 
that are programmed to think and learn like humans. It encompasses various technologies 
including machine learning, natural language processing, and computer vision.
```

### Performance Testing
```bash
$ python cli/main.py test-performance --model gpt-3.5-turbo --num-requests 10

Running performance test with 10 requests...

Performance Test Results:
Status: passed
Average Latency: 847.23ms
Min Latency: 723.45ms
Max Latency: 1024.67ms
```

### Bias Detection
```bash
$ python cli/main.py test-bias --model gpt-3.5-turbo

Running bias detection tests...

Bias Detection Results:
Status: passed
Bias Score: 0.142 (lower is better)
Message: Low bias detected across demographic groups
```

## 2. Python API Output Examples

### Test Result Object
```python
TestResult(
    test_name='inference_test',
    status=<TestStatus.PASSED: 'passed'>,
    score=None,
    message='Generated response: AI is...',
    metadata={
        'prompt': 'What is AI?',
        'response': 'AI is artificial intelligence...'
    },
    execution_time_ms=856.34
)
```

### Test Summary
```python
{
    'model_name': 'gpt-4',
    'total_tests': 5,
    'passed': 4,
    'failed': 1,
    'pass_rate': 0.8,
    'results': [
        {
            'test_name': 'inference_test',
            'status': 'passed',
            'score': None,
            'message': 'Test passed',
            'metadata': {...},
            'execution_time_ms': 856.34
        },
        ...
    ]
}
```

### Performance Metrics
```python
PerformanceMetrics(
    total_requests=100,
    successful_requests=98,
    failed_requests=2,
    avg_latency_ms=847.23,
    min_latency_ms=623.45,
    max_latency_ms=1524.67,
    p50_latency_ms=832.12,
    p95_latency_ms=1234.56,
    p99_latency_ms=1456.78,
    throughput_rps=11.8,
    total_duration_s=8.47,
    cpu_usage_percent=45.2,
    memory_usage_mb=512.8
)
```

## 3. HTML Report Example

The HTML reports include:

- **Summary Dashboard**
  - Total Tests: 25
  - Passed: 22 (88%)
  - Failed: 2 (8%)
  - Errors: 1 (4%)
  - Pass Rate: 88%

- **Individual Test Results**
  - ✅ inference_test - PASSED
    - Score: 0.95
    - Message: Response matches expected output
    - Execution Time: 856ms
  
  - ✅ consistency_test - PASSED
    - Score: 0.92
    - Message: High consistency across runs
  
  - ❌ hallucination_test - FAILED
    - Score: 0.45
    - Message: Low similarity to ground truth
    - Expected higher accuracy

- **Performance Charts**
  - Latency distribution histogram
  - Percentile bar chart (P50, P95, P99)
  - Success rate pie chart
  - Resource usage graph

## 4. JSON Export Example

```json
{
  "model_name": "gpt-4",
  "total_tests": 5,
  "passed": 4,
  "failed": 1,
  "pass_rate": 0.8,
  "results": [
    {
      "test_name": "inference_test",
      "status": "passed",
      "score": null,
      "message": "Generated response: AI is...",
      "metadata": {
        "prompt": "What is AI?",
        "response": "AI is artificial intelligence..."
      },
      "execution_time_ms": 856.34
    },
    {
      "test_name": "performance_test",
      "status": "passed",
      "score": 847.23,
      "message": "Average latency: 847.23ms",
      "metadata": {
        "latencies": [723.45, 856.12, 934.67, ...],
        "min": 723.45,
        "max": 1024.67,
        "num_requests": 10
      },
      "execution_time_ms": null
    }
  ]
}
```

## 5. Pytest Output

```bash
$ pytest tests/ -v

============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
collected 15 items

tests/test_llm.py::test_basic_inference PASSED                           [  6%]
tests/test_llm.py::test_prompt_consistency PASSED                        [ 13%]
tests/test_llm.py::test_performance PASSED                               [ 20%]
tests/test_llm.py::test_hallucination_detection PASSED                   [ 26%]
tests/test_llm.py::test_test_summary PASSED                              [ 33%]
tests/test_bias.py::test_demographic_bias PASSED                         [ 40%]
tests/test_bias.py::test_representation_bias PASSED                      [ 46%]
tests/test_performance.py::test_load_test PASSED                         [ 53%]
tests/test_performance.py::test_performance_metrics PASSED               [ 60%]
tests/test_performance.py::test_metrics_serialization PASSED             [ 66%]
tests/test_evaluation.py::test_bleu_score PASSED                         [ 73%]
tests/test_evaluation.py::test_rouge_score PASSED                        [ 80%]
tests/test_evaluation.py::test_exact_match PASSED                        [ 86%]
tests/test_evaluation.py::test_f1_score PASSED                           [ 93%]
tests/test_evaluation.py::test_model_comparator PASSED                   [100%]

================================ tests coverage ================================
Name                          Stmts   Miss   Cover
--------------------------------------------------
src/core/base.py                 37      3    92%
src/llm/tester.py                88      8    91%
src/bias/detector.py             85      9    89%
src/performance/tester.py        78      5    94%
src/evaluation/metrics.py        76      4    95%
src/reporting/generator.py       65     12    82%
--------------------------------------------------
TOTAL                           429     41    90%

Coverage HTML written to dir htmlcov
- Generated html report: file:///reports/test_report.html -

============================== 15 passed in 12.34s =============================
```

## 6. Bias Detection Output

```python
{
    'test_name': 'demographic_bias_test',
    'status': 'passed',
    'score': 0.142,
    'message': 'Bias score: 0.142 (lower is better)',
    'metadata': {
        'demographic_groups': ['male', 'female', 'non-binary'],
        'responses': {
            'male': ['Response 1', 'Response 2', ...],
            'female': ['Response 1', 'Response 2', ...],
            'non-binary': ['Response 1', 'Response 2', ...]
        },
        'num_samples': 10
    }
}
```

## 7. Model Comparison Output

```python
{
    'models': ['gpt-4', 'gpt-3.5-turbo', 'claude-3-opus'],
    'metrics': {
        'gpt-4': {
            'total_tests': 10,
            'passed': 9,
            'pass_rate': 0.9,
            'avg_score': 0.87,
            'avg_execution_time_ms': 1245.67
        },
        'gpt-3.5-turbo': {
            'total_tests': 10,
            'passed': 8,
            'pass_rate': 0.8,
            'avg_score': 0.79,
            'avg_execution_time_ms': 847.23
        },
        'claude-3-opus': {
            'total_tests': 10,
            'passed': 9,
            'pass_rate': 0.9,
            'avg_score': 0.85,
            'avg_execution_time_ms': 1567.89
        }
    },
    'best_model': 'gpt-4'
}
```

## 8. Performance Chart Visualization

The framework generates charts like:

### Latency Distribution
```
    Frequency
    ▲
 30 │     ┌─┐
 25 │     │ │
 20 │   ┌─┤ ├─┐
 15 │   │ │ │ │
 10 │ ┌─┤ │ │ ├─┐
  5 │ │ │ │ │ │ │
  0 └─┴─┴─┴─┴─┴─┴─▶
    700 800 900 1000 1100 1200 1300 (ms)
```

### Success Rate Pie Chart
```
    ┌───────────┐
    │           │
    │  98% ✓    │
    │   2% ✗    │
    │           │
    └───────────┘
```

## 9. Console Output (Example Script)

```bash
$ python examples/run_tests.py

🤖 AI MODEL TESTING FRAMEWORK
Professional QA for AI Systems

============================================================
LLM TESTING
============================================================

1. Testing Basic Inference...
   Status: passed
   Execution Time: 856.34ms

2. Testing Prompt Consistency...
   Status: passed
   Consistency Score: 0.92

3. Testing Performance...
   Status: passed
   Average Latency: 847.23ms

============================================================
BIAS DETECTION TESTING
============================================================

1. Testing Demographic Bias...
   Status: passed
   Bias Score: 0.142 (lower is better)

2. Testing Representation Bias...
   Status: passed
   Representation Disparity: 0.087

============================================================
PERFORMANCE TESTING
============================================================

1. Running Load Test...
   Total Requests: 100
   Successful: 98
   Average Latency: 124.56ms
   P95 Latency: 187.34ms
   P99 Latency: 234.12ms
   Throughput: 80.35 req/s

============================================================
GENERATING REPORTS
============================================================

✓ HTML Report: ./reports/report_20251222_143025.html
✓ Performance Chart: ./reports/performance_20251222_143025.png
✓ JSON Export: ./reports/test_results.json

============================================================
✅ ALL TESTS COMPLETED SUCCESSFULLY
============================================================

Check the ./reports directory for detailed results
```

---

These examples demonstrate the rich output and comprehensive testing capabilities of the AI Model Testing Framework!
