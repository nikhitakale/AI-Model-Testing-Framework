"""Base classes for AI model testing"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class TestStatus(Enum):
    """Test execution status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TestResult:
    """Result of a single test"""
    test_name: str
    status: TestStatus
    score: Optional[float] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "test_name": self.test_name,
            "status": self.status.value,
            "score": self.score,
            "message": self.message,
            "metadata": self.metadata,
            "execution_time_ms": self.execution_time_ms
        }


class BaseModelTester(ABC):
    """Abstract base class for model testers"""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
        self.results: List[TestResult] = []
    
    @abstractmethod
    def test_inference(self, input_data: Any) -> TestResult:
        """Test model inference"""
        pass
    
    @abstractmethod
    def test_performance(self, num_requests: int = 100) -> TestResult:
        """Test model performance"""
        pass
    
    def add_result(self, result: TestResult):
        """Add test result"""
        self.results.append(result)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        
        return {
            "model_name": self.model_name,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0,
            "results": [r.to_dict() for r in self.results]
        }
