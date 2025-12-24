# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Setup Environment

```bash
# Activate virtual environment (if not already activated)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Verify installation
python -c "from src.llm.tester import LLMTester; print('✓ Framework ready!')"
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=your-key-here
```

### 3. Run Your First Test

**Option A: Using the CLI**

```bash
# Test LLM inference
python cli/main.py test-llm --prompt "What is artificial intelligence?"

# Run performance test
python cli/main.py test-performance --num-requests 20

# List all available tests
python cli/main.py list-tests
```

**Option B: Using Python Code**

```python
from src.llm.tester import LLMTester
import os

# Initialize tester
tester = LLMTester(
    model_name="gpt-3.5-turbo",
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Run a simple test
result = tester.test_inference("What is machine learning?")
print(f"Status: {result.status.value}")
print(f"Response: {result.metadata['response']}")
```

**Option C: Run Example Script**

```bash
python examples/run_tests.py
```

### 4. Run Test Suite

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test category
pytest tests/test_performance.py -v
```

### 5. Generate Reports

```python
from src.reporting.generator import ReportGenerator

generator = ReportGenerator(output_dir="./reports")
report_path = generator.generate_html_report(
    test_results,
    "My First AI Test Report"
)
print(f"Report created: {report_path}")
```

Check `reports/` directory for generated HTML reports and charts!

## 📊 What's Included

- **LLM Testing**: Test any LLM (OpenAI, Anthropic, HuggingFace)
- **Bias Detection**: Automated fairness testing
- **Performance Benchmarks**: Latency, throughput, resource usage
- **Quality Metrics**: BLEU, ROUGE, F1 scores
- **Professional Reports**: HTML reports with charts

## 🎯 Next Steps

1. **Customize Tests**: Edit files in `tests/` directory
2. **Add More Models**: Extend `src/llm/tester.py`
3. **Create Custom Metrics**: Add to `src/evaluation/metrics.py`
4. **Automate Testing**: Integrate with CI/CD

## 🆘 Troubleshooting

**Import Errors?**
```bash
pip install -e .
```

**API Key Issues?**
```bash
# Check .env file exists
cat .env

# Verify it's loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

**Tests Failing?**
```bash
# Install all dependencies
pip install -r requirements.txt

# Run simple test
pytest tests/test_performance.py
```

## 💡 Pro Tips

- Use `temperature=0.0` for consistency testing
- Run bias tests on diverse demographic groups
- Monitor P95/P99 latencies for production systems
- Generate reports after each test run
- Compare multiple models side-by-side

---

**You're all set! Start testing AI models like a pro! 🚀**
