# Quick Start Guide

## Let's Get You Testing in 5 Minutes!

### 1. Fire Up Your Environment

```bash
# Wake up the virtual environment (if you haven't already)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Quick health check
python -c "from src.llm.tester import LLMTester; print('We\'re good to go!')"
```

### 2. Drop in Your API Keys

Create a `.env` file in the project root (just copy the example):

```bash
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=your-key-here
```

💡 **PrPick Your Testing Style

**Option A: The Easy Button**

```bash
# Just run everything and see what happens!
python examples/run_tests.py
```

**Option B: Command Line Ninja**

```bash
# Ask the AI a question
python cli/main.py test-llm --prompt "What is artificial intelligence?"

# Push it to see how fast it goes
python cli/main.py test-performance --num-requests 20

# See all your options
python cli/main.py list-tests
```

**Option C: Code It Yourself**

```python
from src.llm.tester import LLMTester
import os

# Set up the tester
tester = LLMTester(
    model_name="gpt-3.5-turbo",
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Ask it something
result = tester.test_inference("What is machine learning?")
print(f"Status: {result.status.value}")
print(f"Answer: {result.metadata['response']}")
```bash
python examples/run_tests.py
```
the Full Test Suite (If You're Thorough)

```bash
# Test everything
pytest

# See what's covered (with pretty charts!)
pytest --cov=src --cov-report=html

# Just test one thing
# Run specific test category
pytest tests/test_performance.py -v
```
Make a Pretty Report

```python
from src.reporting.generator import ReportGenerator

generator = ReportGenerator(output_dir="./reports")
report_path = generator.generate_html_report(
    test_results,
    "My First AI Test Report"
)
print(f"Report ready! Check it out: {report_path}")
```

Then peek into the `reports/` folder - you'll find some nice HTML reports and charts!

## What You Get

- **LLM Testing**: Try any LLM from OpenAI, Anthropic, or HuggingFace
- **Bias Detection**: Make sure your AI plays fair with everyone
- **Performance Benchmarks**: Speed tests, resource checks, all the good stuff
- **Quality Metrics**: BLEU, ROUGE, F1 scores (fancy, right?)
- **Beautiful Reports**: HTML reports that actually look good
- **Professional Reports**: HTML reports with charts
## What's Next?

Ready to dive deeper? Check out:
- [Full Documentation](README.md) - All the details
- [Examples](EXAMPLES.md) - Real-world testing scenarios  
- [Project Overview](PROJECT_OVERVIEW.md) - Architecture and design

Got questions? Hit a snag? The docs have your back! 

Happy testing!
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

## Pro Tips

- Use `temperature=0.0` for consistency testing
- Run bias tests on diverse demographic groups
- Monitor P95/P99 latencies for production systems
- Generate reports after each test run
- Compare multiple models side-by-side

---

**You're all set! Start testing AI models like a pro!**
