"""AI Model Testing Framework Configuration"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class TestConfig:
    """Configuration for AI model testing"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    huggingface_token: Optional[str] = None
    
    # Model Settings
    default_model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # Testing Settings
    test_environment: str = "development"
    log_level: str = "INFO"
    enable_performance_tests: bool = True
    enable_bias_tests: bool = True
    
    # Performance Thresholds
    performance_threshold_ms: int = 5000
    concurrent_requests: int = 10
    
    # Reporting
    report_output_dir: str = "./reports"
    enable_html_reports: bool = True
    
    def __post_init__(self):
        """Load configuration from environment variables"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY", self.openai_api_key)
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", self.anthropic_api_key)
        self.huggingface_token = os.getenv("HUGGINGFACE_TOKEN", self.huggingface_token)
        self.default_model = os.getenv("DEFAULT_MODEL", self.default_model)
        
    @classmethod
    def from_env(cls) -> "TestConfig":
        """Create configuration from environment variables"""
        return cls()


# Global configuration instance
config = TestConfig.from_env()
