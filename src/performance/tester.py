"""Performance testing utilities"""

import time
import psutil
import threading
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np


@dataclass
class PerformanceMetrics:
    """Performance test metrics"""
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    throughput_rps: float
    total_duration_s: float
    cpu_usage_percent: float
    memory_usage_mb: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "min_latency_ms": round(self.min_latency_ms, 2),
            "max_latency_ms": round(self.max_latency_ms, 2),
            "p50_latency_ms": round(self.p50_latency_ms, 2),
            "p95_latency_ms": round(self.p95_latency_ms, 2),
            "p99_latency_ms": round(self.p99_latency_ms, 2),
            "throughput_rps": round(self.throughput_rps, 2),
            "total_duration_s": round(self.total_duration_s, 2),
            "cpu_usage_percent": round(self.cpu_usage_percent, 2),
            "memory_usage_mb": round(self.memory_usage_mb, 2)
        }


class PerformanceTester:
    """Tester for model performance"""
    
    def __init__(self):
        self.process = psutil.Process()
    
    def load_test(
        self,
        test_function: Callable,
        num_requests: int = 100,
        concurrent_users: int = 10
    ) -> PerformanceMetrics:
        """Run load test with concurrent requests"""
        
        latencies = []
        errors = []
        
        cpu_samples = []
        memory_samples = []
        
        # Monitor resources in background
        monitoring = True
        
        def monitor_resources():
            while monitoring:
                cpu_samples.append(self.process.cpu_percent(interval=0.1))
                memory_samples.append(self.process.memory_info().rss / 1024 / 1024)
                time.sleep(0.5)
        
        monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
        monitor_thread.start()
        
        start_time = time.time()
        
        # Execute requests concurrently
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(self._execute_request, test_function) 
                      for _ in range(num_requests)]
            
            for future in as_completed(futures):
                result = future.result()
                if result["success"]:
                    latencies.append(result["latency"])
                else:
                    errors.append(result["error"])
        
        end_time = time.time()
        monitoring = False
        monitor_thread.join(timeout=1)
        
        # Calculate metrics
        total_duration = end_time - start_time
        
        if latencies:
            latencies_array = np.array(latencies)
            metrics = PerformanceMetrics(
                total_requests=num_requests,
                successful_requests=len(latencies),
                failed_requests=len(errors),
                avg_latency_ms=float(np.mean(latencies_array)),
                min_latency_ms=float(np.min(latencies_array)),
                max_latency_ms=float(np.max(latencies_array)),
                p50_latency_ms=float(np.percentile(latencies_array, 50)),
                p95_latency_ms=float(np.percentile(latencies_array, 95)),
                p99_latency_ms=float(np.percentile(latencies_array, 99)),
                throughput_rps=len(latencies) / total_duration,
                total_duration_s=total_duration,
                cpu_usage_percent=float(np.mean(cpu_samples)) if cpu_samples else 0.0,
                memory_usage_mb=float(np.mean(memory_samples)) if memory_samples else 0.0
            )
        else:
            metrics = PerformanceMetrics(
                total_requests=num_requests,
                successful_requests=0,
                failed_requests=len(errors),
                avg_latency_ms=0.0,
                min_latency_ms=0.0,
                max_latency_ms=0.0,
                p50_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                throughput_rps=0.0,
                total_duration_s=total_duration,
                cpu_usage_percent=float(np.mean(cpu_samples)) if cpu_samples else 0.0,
                memory_usage_mb=float(np.mean(memory_samples)) if memory_samples else 0.0
            )
        
        return metrics
    
    @staticmethod
    def _execute_request(test_function: Callable) -> Dict[str, Any]:
        """Execute a single request and measure latency"""
        try:
            start_time = time.time()
            test_function()
            latency = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "latency": latency,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "latency": None,
                "error": str(e)
            }
    
    def stress_test(
        self,
        test_function: Callable,
        duration_seconds: int = 60,
        ramp_up_seconds: int = 10,
        max_concurrent_users: int = 50
    ) -> List[PerformanceMetrics]:
        """Run stress test with gradual load increase"""
        
        metrics_over_time = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            elapsed = time.time() - start_time
            
            # Calculate current load level
            if elapsed < ramp_up_seconds:
                current_users = int((elapsed / ramp_up_seconds) * max_concurrent_users)
            else:
                current_users = max_concurrent_users
            
            current_users = max(1, current_users)
            
            # Run load test for this interval
            metrics = self.load_test(
                test_function,
                num_requests=current_users * 10,
                concurrent_users=current_users
            )
            
            metrics_over_time.append(metrics)
        
        return metrics_over_time
