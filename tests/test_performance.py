"""Test example for performance testing"""

import pytest
import time
from src.performance.tester import PerformanceTester


def dummy_inference():
    """Dummy inference function for testing"""
    time.sleep(0.1)  # Simulate 100ms inference
    return "response"


def test_load_test():
    """Test load testing functionality"""
    tester = PerformanceTester()
    
    metrics = tester.load_test(
        test_function=dummy_inference,
        num_requests=20,
        concurrent_users=5
    )
    
    assert metrics.total_requests == 20
    assert metrics.successful_requests > 0
    assert metrics.avg_latency_ms > 0
    assert metrics.throughput_rps > 0


def test_performance_metrics():
    """Test performance metrics calculation"""
    tester = PerformanceTester()
    
    metrics = tester.load_test(
        test_function=dummy_inference,
        num_requests=10,
        concurrent_users=2
    )
    
    assert metrics.min_latency_ms > 0
    assert metrics.max_latency_ms >= metrics.min_latency_ms
    assert metrics.p50_latency_ms > 0
    assert metrics.p95_latency_ms > 0
    assert metrics.p99_latency_ms >= metrics.p95_latency_ms


def test_metrics_serialization():
    """Test metrics can be converted to dict"""
    tester = PerformanceTester()
    
    metrics = tester.load_test(
        test_function=dummy_inference,
        num_requests=5,
        concurrent_users=1
    )
    
    metrics_dict = metrics.to_dict()
    
    assert isinstance(metrics_dict, dict)
    assert "total_requests" in metrics_dict
    assert "avg_latency_ms" in metrics_dict
    assert "throughput_rps" in metrics_dict
