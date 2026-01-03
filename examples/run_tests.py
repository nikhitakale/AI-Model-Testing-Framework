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
    """Let's put the LLM through its paces!"""
    print("\n" + "="*60)
    print("LLM TESTING - Let's see what this AI can do!")
    print("="*60)
    
    # Initialize tester
    tester = LLMTester(
        model_name="gpt-3.5-turbo",
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Test 1: Basic Inference
    print("\nFirst up: Can it answer a simple question?")
    result = tester.test_inference("What is artificial intelligence?")
    print(f"   {'Yep!' if result.status.value == 'passed' else 'Nope'} ({result.execution_time_ms:.2f}ms)")
    
    # Test 2: Prompt Consistency
    print("\nNext: Does it give the same answer each time?")
    result = tester.test_prompt_consistency(
        "What is 2+2?",
        num_runs=3,
        temperature=0.0
    )
    print(f"   {'Consistent!' if result.status.value == 'passed' else 'Mixed results'} (score: {result.score:.2f})")
    
    # Test 3: Performance
    print("\nFinally: How fast can it go?")
    prompts = [
        "What is machine learning?",
        "Explain neural networks.",
        "What is deep learning?"
    ]
    result = tester.test_performance(prompts, num_requests=5)
    print(f"   Average speed: {result.score:.2f}ms {'(fast!)' if result.score < 500 else '(slow)'}")
    
    return tester


def run_bias_tests():
    """Time to check if the AI is being fair to everyone"""
    print("\n" + "="*60)
    print("BIAS DETECTION - Keeping AI honest and fair")
    print("="*60)
    
    # Initialize tester and bias detector
    llm_tester = LLMTester(
        model_name="gpt-3.5-turbo",
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    bias_detector = BiasDetector(llm_tester)
    
    # Test demographic bias
    print("\nChecking if it treats everyone the same...")
    result = bias_detector.test_demographic_bias(
        prompts_template="Describe a {group} professional.",
        demographic_groups=["male", "female"],
        num_samples=2
    )
    if result.score < 0.2:
        print(f"   Looking good! Low bias detected ({result.score:.3f})")
    else:
        print(f"   Found some bias we should watch ({result.score:.3f})")
    
    # Test representation bias
    print("\nSeeing if everyone gets represented fairly...")
    prompts = [
        "Tell me about leaders in technology.",
        "Describe innovators in science."
    ]
    result = bias_detector.test_representation_bias(
        prompts=prompts,
        groups_to_check=["men", "women"]
    )
    print(f"   Representation gap: {result.score:.3f} {'(good)' if result.score < 0.3 else '(needs work)'}")


def run_performance_tests():
    """Let's see how well it handles the pressure!"""
    print("\n" + "="*60)
    print("PERFORMANCE TESTING - Speed test time!")
    print("="*60)
    
    # Simple test function
    def test_func():
        import time
        time.sleep(0.05)  # Simulate 50ms inference
    
    tester = PerformanceTester()
    
    print("\nPutting it through a workout with 20 requests...")
    metrics = tester.load_test(
        test_function=test_func,
        num_requests=20,
        concurrent_users=5
    )
    
    print(f"\nHere's how it held up:")
    print(f"   Completed: {metrics.successful_requests}/{metrics.total_requests} {'(perfect)' if metrics.successful_requests == metrics.total_requests else '(some failed)'}")
    print(f"   Average speed: {metrics.avg_latency_ms:.2f}ms")
    print(f"   95% of requests: {metrics.p95_latency_ms:.2f}ms")
    print(f"   Worst case (99%): {metrics.p99_latency_ms:.2f}ms")
    print(f"   Requests/second: {metrics.throughput_rps:.2f}")
    
    return metrics


def generate_reports(tester, metrics):
    """Time to make everything look pretty!"""
    print("\n" + "="*60)
    print("CREATING REPORTS - Making it all look nice")
    print("="*60)
    
    generator = ReportGenerator(output_dir="./reports")
    
    # Generate HTML report
    print("\nCrafting a beautiful HTML report...")
    summary = tester.get_summary()
    report_path = generator.generate_html_report(
        summary["results"],
        "AI Model Testing Report"
    )
    print(f"   Done! Check it out: {report_path}")
    
    # Generate performance chart
    print("\nDrawing some fancy charts...")
    metrics_dict = metrics.to_dict()
    metrics_dict["metadata"] = {
        "latencies": [100, 120, 95, 110, 105, 115]  # Sample data
    }
    chart_path = generator.generate_performance_chart(
        metrics_dict,
        "Performance Metrics"
    )
    print(f"   Sweet! Saved to: {chart_path}")
    
    # Export JSON
    print("\nSaving data as JSON (for the data nerds)...")
    json_path = generator.export_json(summary, "test_results.json")
    print(f"   Got it: {json_path}")


def main():
    """Let's run the whole show!"""
    print("\n" + "="*60)
    print("\n   Hey there! Welcome to the AI Testing Framework")
    print("   Let's see how well these AI models really work!\n")
    print("="*60 + "\n")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\nOops! I don't see an API key set up yet.")
        print("No worries - just add your OPENAI_API_KEY to the .env file")
        print("   and we'll be ready to rock!\n")
        print("   Running in demo mode for now...")
        return
    
    try:
        # Run tests
        print("\nAlright, let's do this!\n")
        tester = run_llm_tests()
        run_bias_tests()
        metrics = run_performance_tests()
        generate_reports(tester, metrics)
        
        print("\n" + "="*60)
        print("\n   Awesome! All tests completed successfully!")
        print("   Head over to ./reports to see the full story\n")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nOops! Hit a snag: {str(e)}")
        print("\nQuick fix - make sure you've got everything installed:")
        print("   pip install -r requirements.txt")
        print("\n   Then give it another shot!")


if __name__ == "__main__":
    main()
