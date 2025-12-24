# AI Model Testing Framework

A comprehensive, professional-grade testing framework for AI/ML models with focus on quality assurance, bias detection, and performance benchmarking.

## 🎯 Features

### LLM Testing
- **Inference Testing**: Validate model outputs for accuracy and relevance
- **Prompt Consistency**: Measure response consistency across multiple runs
- **Hallucination Detection**: Compare outputs against ground truth
- **Multi-Provider Support**: OpenAI, Anthropic, and HuggingFace models

### Bias & Fairness
- **Demographic Bias Detection**: Test for biases across demographic groups
- **Sentiment Bias Analysis**: Measure sentiment variation across protected attributes
- **Representation Bias**: Analyze representation fairness in model outputs
- **Automated Bias Scoring**: Quantitative bias metrics

### Performance Testing
- **Load Testing**: Concurrent request handling and throughput measurement
- **Latency Analysis**: P50, P95, P99 percentile tracking
- **Stress Testing**: Progressive load increase testing
- **Resource Monitoring**: CPU and memory usage tracking

### Evaluation Metrics
- **BLEU & ROUGE Scores**: Standard NLP evaluation metrics
- **F1 Score**: Token-level precision and recall
- **Semantic Similarity**: Context-aware similarity measures
- **Model Comparison**: Side-by-side model evaluation

### Reporting
- **HTML Reports**: Professional, interactive test reports
- **Performance Charts**: Visual latency and throughput analysis
- **JSON Export**: Machine-readable test results
- **Dashboard Metrics**: Real-time test statistics

## 📦 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-model-testing-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## 🚀 Quick Start

### 1. Configure API Keys

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
HUGGINGFACE_TOKEN=your_token_here
```

### 2. Run Example Tests

```bash
python examples/run_tests.py
```

### 3. Use CLI

```bash
# Test LLM inference
aitest test-llm --model gpt-3.5-turbo --prompt "What is AI?"

# Run performance tests
aitest test-performance --model gpt-3.5-turbo --num-requests 50

# Test for bias
aitest test-bias --model gpt-3.5-turbo

# Generate report
aitest generate-report --output ./reports

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
