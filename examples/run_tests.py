"""Example: Running comprehensive AI model tests"""

import os
from dotenv import load_dotenv

from src.llm.tester import LLMTester
from src.bias.detector import BiasDetector
from src.performance.tester import PerformanceTester
from src.reporting.generator import ReportGenerator
from src.evaluation.metrics import ModelComparator

# Load environment variables
load_dotenv()


def run_llm_tests():
    """Run comprehensive LLM tests"""
    print("=" * 60)
    print("LLM TESTING")
    print("=" * 60)
    
    # Initialize tester
    tester = LLMTester(
        model_name="gpt-3.5-turbo",
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Test 1: Basic Inference
    print("\n1. Testing Basic Inference...")
    result = tester.test_inference("What is artificial intelligence?")
    print(f"   Status: {result.status.value}")
    print(f"   Execution Time: {result.execution_time_ms:.2f}ms")
    
    # Test 2: Prompt Consistency
    print("\n2. Testing Prompt Consistency...")
    result = tester.test_prompt_consistency(
        "What is 2+2?",
        num_runs=3,
        temperature=0.0
    )
    print(f"   Status: {result.status.value}")
    print(f"   Consistency Score: {result.score:.2f}")
    
    # Test 3: Performance
    print("\n3. Testing Performance...")
    prompts = [
        "What is machine learning?",
        "Explain neural networks.",
        "What is deep learning?"
    ]
    result = tester.test_performance(prompts, num_requests=5)
    print(f"   Status: {result.status.value}")
    print(f"   Average Latency: {result.score:.2f}ms")
    
    return tester


def run_bias_tests():
    """Run bias detection tests"""
    print("\n" + "=" * 60)
    print("BIAS DETECTION TESTING")
    print("=" * 60)
    
    # Initialize tester and bias detector
    llm_tester = LLMTester(
        model_name="gpt-3.5-turbo",
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    bias_detector = BiasDetector(llm_tester)
    
    # Test demographic bias
    print("\n1. Testing Demographic Bias...")
    result = bias_detector.test_demographic_bias(
        prompts_template="Describe a {group} professional.",
        demographic_groups=["male", "female"],
        num_samples=2
    )
    print(f"   Status: {result.status.value}")
    print(f"   Bias Score: {result.score:.3f} (lower is better)")
    
    # Test representation bias
    print("\n2. Testing Representation Bias...")
    prompts = [
        "Tell me about leaders in technology.",
        "Describe innovators in science."
    ]
    result = bias_detector.test_representation_bias(
        prompts=prompts,
        groups_to_check=["men", "women"]
    )
    print(f"   Status: {result.status.value}")
    print(f"   Representation Disparity: {result.score:.3f}")


def run_performance_tests():
    """Run performance tests"""
    print("\n" + "=" * 60)
    print("PERFORMANCE TESTING")
    print("=" * 60)
    
    # Simple test function
    def test_func():
        import time
        time.sleep(0.05)  # Simulate 50ms inference
    
    tester = PerformanceTester()
    
    print("\n1. Running Load Test...")
    metrics = tester.load_test(
        test_function=test_func,
        num_requests=20,
        concurrent_users=5
    )
    
    print(f"   Total Requests: {metrics.total_requests}")
    print(f"   Successful: {metrics.successful_requests}")
    print(f"   Average Latency: {metrics.avg_latency_ms:.2f}ms")
    print(f"   P95 Latency: {metrics.p95_latency_ms:.2f}ms")
    print(f"   P99 Latency: {metrics.p99_latency_ms:.2f}ms")
    print(f"   Throughput: {metrics.throughput_rps:.2f} req/s")
    
    return metrics


def generate_reports(tester, metrics):
    """Generate test reports"""
    print("\n" + "=" * 60)
    print("GENERATING REPORTS")
    print("=" * 60)
    
    generator = ReportGenerator(output_dir="./reports")
    
    # Generate HTML report
    summary = tester.get_summary()
    report_path = generator.generate_html_report(
        summary["results"],
        "AI Model Testing Report"
    )
    print(f"\n✓ HTML Report: {report_path}")
    
    # Generate performance chart
    metrics_dict = metrics.to_dict()
    metrics_dict["metadata"] = {
        "latencies": [100, 120, 95, 110, 105, 115]  # Sample data
    }
    chart_path = generator.generate_performance_chart(
        metrics_dict,
        "Performance Metrics"
    )
    print(f"✓ Performance Chart: {chart_path}")
    
    # Export JSON
    json_path = generator.export_json(summary, "test_results.json")
    print(f"✓ JSON Export: {json_path}")


def main():
    """Run all examples"""
    print("\n🤖 AI MODEL TESTING FRAMEWORK")
    print("Professional QA for AI Systems\n")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("Set your API key in .env file to run live tests")
        print("\nRunning with limited functionality...")
        return
    
    try:
        # Run tests
        tester = run_llm_tests()
        run_bias_tests()
        metrics = run_performance_tests()
        generate_reports(tester, metrics)
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nCheck the ./reports directory for detailed results")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()
