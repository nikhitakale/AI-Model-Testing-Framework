# AI Model Testing Framework

Hey there! Welcome to a testing framework that actually speaks human. We're here to help you test your AI models without all the corporate jargon and robotic messages.

## Quick Demo

See the framework in action:

<!-- Replace this with your actual video link once uploaded -->
[![Demo Video](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge)](https://github.com/YOUR_USERNAME/YOUR_REPO/assets/demo.mp4)

**Or check out this quick example:**

```bash
# Run a quick LLM test
python cli/main.py test-llm --prompt "What is AI?"

# Output:
# Hmm, let me think about this...
# Here's what I found:
# Status: Looking good!
# Got a nice detailed response! Here's a preview: Artificial Intelligence...
```

## What Can It Do?

### LLM Testing
- **Inference Testing**: See if your model actually knows what it's talking about
- **Prompt Consistency**: Check if it gives the same answer twice (spoiler: sometimes it doesn't!)
- **Hallucination Detection**: Catch your AI when it's making stuff up
- **Multi-Provider Support**: Works with OpenAI, Anthropic, and HuggingFace - we're not picky!

### Bias & Fairness (Because AI Should Be Fair!)
- **Demographic Bias Detection**: Make sure your AI treats everyone equally
- **Sentiment Bias Analysis**: Check if it's nicer to some groups than others
- **Representation Bias**: See if everyone gets a fair mention
- **Automated Bias Scoring**: Numbers that tell you if something's off

### Performance Testing (How Fast Can It Go?)
- **Load Testing**: See if it can handle a crowd
- **Latency Analysis**: Measure how long you'll be waiting (with fancy percentiles!)
- **Stress Testing**: Push it 'til it breaks (responsibly)
- **Resource Monitoring**: Watch those CPUs sweat

### Evaluation Metrics (The Nerdy Stuff)
- **BLEU & ROUGE Scores**: Industry standard ways to score text
- **F1 Score**: Math that tells you how good the match is
- **Semantic Similarity**: Does it actually mean the same thing?
- **Model Comparison**: Battle of the AIs - which one wins?

### Reporting (Make It Pretty!)
- **HTML Reports**: Beautiful reports you can actually show your boss
- **Performance Charts**: Graphs that make sense (finally!)
- **JSON Export**: For when you need to get programmatic
- **Dashboard Metrics**: Real-time stats to watch your tests run

## Getting Started

It's super easy, promise!

```bash
# Grab the code
git clone <your-repo-url>
cd ai-model-testing-framework

# Set up your Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install everything you need
pip install -r requirements.txt

# Install the framework
pip install -e .
```Let's Go!

### 1. Set Up Your API Keys

First things first - we need your API keys:

```bash
cp .env.example .env
```

Then pop in your keys:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
HUGGINGFACE_TOKEN=your_token_here
```

### 2. Take It for a Spin

The easiest way to get started:

```bash
python examples/run_tests.py
```

### 3. Or Use the CLI (If You're Feeling Fancy)

```bash
# Ask the AI something
python cli/main.py test-llm --prompt "What is AI?"

# See how fast it goes
python cli/main.py test-performance --num-requests 50

# Check for bias
python cli/main.py test-bias

# Make a pretty report
python cli/main.py generate-report

# See what else you can do
python cli/main.py
# List available tests
aitest list-tests
```

## 📚 Usage Examples

### LLM Testing

```python
from src.llm.tester import LLMTester

# Initialize tester
tester = LLMTester(
    model_name="gpt-4",
    provider="openai",
    api_key="your-api-key"
)

# Test inference
result = tester.test_inference("What is machine learning?")
print(f"Status: {result.status}")
print(f"Response: {result.metadata['response']}")

# Test consistency
result = tester.test_prompt_consistency(
    "What is 2+2?",
    num_runs=5,
    temperature=0.0
)
print(f"Consistency Score: {result.score}")

# Test performance
prompts = ["Question 1", "Question 2", "Question 3"]
result = tester.test_performance(prompts, num_requests=10)
print(f"Avg Latency: {result.score}ms")
```

### Bias Detection

```python
from src.llm.tester import LLMTester
from src.bias.detector import BiasDetector

llm_tester = LLMTester(model_name="gpt-4", provider="openai")
bias_detector = BiasDetector(llm_tester)

# Test demographic bias
result = bias_detector.test_demographic_bias(
    prompts_template="Describe a {group} engineer.",
    demographic_groups=["male", "female", "non-binary"],
    num_samples=10
)
print(f"Bias Score: {result.score:.3f}")

# Test representation bias
prompts = ["Tell me about tech leaders.", "Describe scientists."]
result = bias_detector.test_representation_bias(
    prompts=prompts,
    groups_to_check=["men", "women"]
)
print(f"Representation Disparity: {result.score:.3f}")
```

### Performance Testing

```python
from src.performance.tester import PerformanceTester

tester = PerformanceTester()

# Define test function
def my_inference():
    # Your model inference code
    pass

# Load test
metrics = tester.load_test(
    test_function=my_inference,
    num_requests=1000,
    concurrent_users=50
)

print(f"Throughput: {metrics.throughput_rps:.2f} req/s")
print(f"P95 Latency: {metrics.p95_latency_ms:.2f}ms")
print(f"CPU Usage: {metrics.cpu_usage_percent:.2f}%")
```

### Evaluation & Comparison

```python
from src.evaluation.metrics import EvaluationMetrics, ModelComparator

# Calculate BLEU score
bleu = EvaluationMetrics.calculate_bleu(reference, candidate)

# Calculate ROUGE scores
rouge = EvaluationMetrics.calculate_rouge(reference, candidate)

# Compare models
comparison = ModelComparator.compare_models({
    "gpt-4": model1_results,
    "claude-3": model2_results
})
print(f"Best Model: {comparison['best_model']}")
```

### Report Generation

```python
from src.reporting.generator import ReportGenerator

generator = ReportGenerator(output_dir="./reports")

# Generate HTML report
report_path = generator.generate_html_report(
    test_results=results,
    report_title="Monthly AI Model QA Report"
)

# Generate performance charts
chart_path = generator.generate_performance_chart(
    metrics=performance_metrics,
    chart_title="Load Test Results"
)

# Export to JSON
json_path = generator.export_json(data, "results.json")
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_llm.py

# Run with verbose output
pytest -v

# Generate HTML test report
pytest --html=reports/test_report.html
```

## 📊 Project Structure

```
ai-model-testing-framework/
├── src/
│   ├── core/
│   │   └── base.py              # Base classes and enums
│   ├── llm/
│   │   ├── tester.py            # LLM testing
│   │   └── prompts.py           # Prompt utilities
│   ├── bias/
│   │   └── detector.py          # Bias detection
│   ├── performance/
│   │   └── tester.py            # Performance testing
│   ├── evaluation/
│   │   └── metrics.py           # Evaluation metrics
│   ├── reporting/
│   │   └── generator.py         # Report generation
│   └── config.py                # Configuration
├── tests/
│   ├── test_llm.py              # LLM tests
│   ├── test_bias.py             # Bias tests
│   ├── test_performance.py      # Performance tests
│   └── test_evaluation.py       # Evaluation tests
├── cli/
│   └── main.py                  # CLI interface
├── examples/
│   └── run_tests.py             # Example usage
├── reports/                      # Generated reports
├── .env.example                 # Environment template
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
├── pyproject.toml              # Project config
└── README.md                    # This file
```

## 🔧 Configuration

Configure testing via environment variables or `src/config.py`:

```python
# Model settings
DEFAULT_MODEL = "gpt-4"
TEMPERATURE = 0.7
MAX_TOKENS = 1000

# Performance thresholds
PERFORMANCE_THRESHOLD_MS = 5000
CONCURRENT_REQUESTS = 10

# Testing settings
ENABLE_PERFORMANCE_TESTS = True
ENABLE_BIAS_TESTS = True
```

## 📈 Metrics & Scoring

### Bias Scores
- **< 0.2**: Low bias (excellent)
- **0.2 - 0.5**: Moderate bias (acceptable)
- **> 0.5**: High bias (needs attention)

### Performance Thresholds
- **Latency**: < 5000ms per request
- **Throughput**: > 10 requests/sec
- **Success Rate**: > 95%

### Quality Scores
- **BLEU**: 0-1 (higher is better)
- **ROUGE**: 0-1 (higher is better)
- **F1**: 0-1 (higher is better)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- OpenAI API
- Anthropic API
- HuggingFace Transformers
- pytest
- matplotlib & seaborn

## 📞 Support

For issues and questions:
- GitHub Issues: [your-repo]/issues
- Documentation: [your-docs-url]
- Email: support@example.com

## 🗺️ Roadmap

- [ ] Support for more LLM providers
- [ ] Advanced hallucination detection
- [ ] Automated test generation
- [ ] CI/CD integration templates
- [ ] Real-time monitoring dashboard
- [ ] A/B testing capabilities
- [ ] Model drift detection
- [ ] Adversarial testing

---

**Stand out as an AI QA professional with comprehensive, automated AI model testing!** 🚀
