"""Test example for LLM testing"""

import pytest
import os
from src.llm.tester import LLMTester
from src.core.base import TestStatus


@pytest.fixture
def llm_tester():
    """Create LLM tester fixture"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    
    return LLMTester(
        model_name="gpt-3.5-turbo",
        provider="openai",
        api_key=api_key
    )


def test_basic_inference(llm_tester):
    """Test basic model inference"""
    prompt = "What is 2 + 2?"
    result = llm_tester.test_inference(prompt)
    
    assert result.status == TestStatus.PASSED
    assert result.metadata is not None
    assert "response" in result.metadata
    assert "4" in result.metadata["response"]


def test_prompt_consistency(llm_tester):
    """Test prompt consistency"""
    prompt = "List three primary colors."
    result = llm_tester.test_prompt_consistency(prompt, num_runs=3, temperature=0.0)
    
    assert result.status == TestStatus.PASSED
    assert result.score is not None
    assert result.score >= 0.0 and result.score <= 1.0


def test_performance(llm_tester):
    """Test model performance"""
    prompts = [
        "What is the capital of France?",
        "Explain photosynthesis briefly.",
        "What is 10 * 15?"
    ]
    
    result = llm_tester.test_performance(prompts, num_requests=5)
    
    assert result.status == TestStatus.PASSED
    assert result.score is not None
    assert result.score > 0  # Should have some latency


def test_hallucination_detection(llm_tester):
    """Test hallucination detection"""
    prompt = "What is the capital of France?"
    ground_truth = "The capital of France is Paris."
    
    result = llm_tester.test_hallucination_detection(prompt, ground_truth)
    
    assert result.status == TestStatus.PASSED
    assert result.score is not None


def test_test_summary(llm_tester):
    """Test summary generation"""
    # Run a few tests
    llm_tester.test_inference("Hello, world!")
    llm_tester.test_inference("What is AI?")
    
    summary = llm_tester.get_summary()
    
    assert summary["model_name"] == "gpt-3.5-turbo"
    assert summary["total_tests"] == 2
    assert "passed" in summary
    assert "failed" in summary
