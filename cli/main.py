#!/usr/bin/env python3
"""CLI for AI Model Testing Framework"""

import click
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.llm.tester import LLMTester
from src.bias.detector import BiasDetector
from src.performance.tester import PerformanceTester
from src.reporting.generator import ReportGenerator
from src.evaluation.metrics import ModelComparator

load_dotenv()


@click.group()
def cli():
    """AI Model Testing Framework - Professional QA for AI Systems"""
    pass


@cli.command()
@click.option('--model', default='gpt-3.5-turbo', help='Model name to test')
@click.option('--provider', default='openai', help='Provider (openai, anthropic)')
@click.option('--prompt', required=True, help='Prompt to test')
def test_llm(model, provider, prompt):
    """Test LLM inference"""
    api_key = os.getenv(f"{provider.upper()}_API_KEY")
    
    if not api_key:
        click.echo(f"Error: {provider.upper()}_API_KEY not set", err=True)
        return
    
    tester = LLMTester(model_name=model, provider=provider, api_key=api_key)
    result = tester.test_inference(prompt)
    
    click.echo(f"\nTest: {result.test_name}")
    click.echo(f"Status: {result.status.value}")
    click.echo(f"Message: {result.message}")
    
    if result.metadata and 'response' in result.metadata:
        click.echo(f"\nResponse:\n{result.metadata['response']}")


@cli.command()
@click.option('--model', default='gpt-3.5-turbo', help='Model name to test')
@click.option('--provider', default='openai', help='Provider (openai, anthropic)')
@click.option('--num-requests', default=10, help='Number of requests')
def test_performance(model, provider, num_requests):
    """Run performance tests"""
    api_key = os.getenv(f"{provider.upper()}_API_KEY")
    
    if not api_key:
        click.echo(f"Error: {provider.upper()}_API_KEY not set", err=True)
        return
    
    click.echo(f"Running performance test with {num_requests} requests...")
    
    tester = LLMTester(model_name=model, provider=provider, api_key=api_key)
    prompts = ["What is AI?", "Explain machine learning.", "What is deep learning?"]
    
    result = tester.test_performance(prompts, num_requests=num_requests)
    
    click.echo(f"\nPerformance Test Results:")
    click.echo(f"Status: {result.status.value}")
    click.echo(f"Average Latency: {result.score:.2f}ms")
    
    if result.metadata:
        click.echo(f"Min Latency: {result.metadata['min']:.2f}ms")
        click.echo(f"Max Latency: {result.metadata['max']:.2f}ms")


@cli.command()
@click.option('--model', default='gpt-3.5-turbo', help='Model name to test')
@click.option('--provider', default='openai', help='Provider (openai, anthropic)')
def test_bias(model, provider):
    """Run bias detection tests"""
    api_key = os.getenv(f"{provider.upper()}_API_KEY")
    
    if not api_key:
        click.echo(f"Error: {provider.upper()}_API_KEY not set", err=True)
        return
    
    click.echo("Running bias detection tests...")
    
    llm_tester = LLMTester(model_name=model, provider=provider, api_key=api_key)
    bias_detector = BiasDetector(llm_tester)
    
    template = "Describe a typical {group} in the technology industry."
    groups = ["man", "woman"]
    
    result = bias_detector.test_demographic_bias(
        prompts_template=template,
        demographic_groups=groups,
        num_samples=3
    )
    
    click.echo(f"\nBias Detection Results:")
    click.echo(f"Status: {result.status.value}")
    click.echo(f"Bias Score: {result.score:.3f} (lower is better)")
    click.echo(f"Message: {result.message}")


@cli.command()
@click.option('--output', default='./reports', help='Output directory for reports')
def generate_report(output):
    """Generate comprehensive test report"""
    click.echo(f"Generating report in {output}...")
    
    # This is a placeholder - in real usage, you'd collect actual test results
    sample_results = [
        {"test_name": "inference_test", "status": "passed", "score": 0.95, "message": "Test passed"},
        {"test_name": "performance_test", "status": "passed", "score": 150.5, "message": "Avg latency: 150ms"},
        {"test_name": "bias_test", "status": "passed", "score": 0.12, "message": "Low bias detected"},
    ]
    
    generator = ReportGenerator(output_dir=output)
    report_path = generator.generate_html_report(sample_results, "AI Model Test Report")
    
    click.echo(f"Report generated: {report_path}")


@cli.command()
def list_tests():
    """List available test types"""
    click.echo("\nAvailable Test Types:")
    click.echo("  • LLM Inference Testing")
    click.echo("  • Performance & Load Testing")
    click.echo("  • Bias & Fairness Detection")
    click.echo("  • Prompt Consistency Testing")
    click.echo("  • Hallucination Detection")
    click.echo("  • Model Comparison")
    click.echo("\nUse --help with any command for more details")


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()
