"""Prompt testing utilities"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class PromptType(Enum):
    """Types of prompts"""
    INSTRUCTION = "instruction"
    QUESTION = "question"
    COMPLETION = "completion"
    CONVERSATION = "conversation"
    CREATIVE = "creative"


@dataclass
class PromptTestCase:
    """A single prompt test case"""
    prompt: str
    expected_output: Optional[str] = None
    expected_keywords: Optional[List[str]] = None
    prompt_type: PromptType = PromptType.INSTRUCTION
    metadata: Optional[Dict[str, Any]] = None


class PromptValidator:
    """Validator for prompt testing"""
    
    @staticmethod
    def validate_response(response: str, test_case: PromptTestCase) -> Dict[str, Any]:
        """Validate response against test case expectations"""
        results = {
            "valid": True,
            "checks": {}
        }
        
        # Check for expected keywords
        if test_case.expected_keywords:
            found_keywords = []
            missing_keywords = []
            
            for keyword in test_case.expected_keywords:
                if keyword.lower() in response.lower():
                    found_keywords.append(keyword)
                else:
                    missing_keywords.append(keyword)
            
            keyword_score = len(found_keywords) / len(test_case.expected_keywords)
            results["checks"]["keywords"] = {
                "score": keyword_score,
                "found": found_keywords,
                "missing": missing_keywords
            }
            
            if keyword_score < 0.5:
                results["valid"] = False
        
        # Check for expected output similarity
        if test_case.expected_output:
            similarity = PromptValidator._calculate_similarity(
                response, test_case.expected_output
            )
            results["checks"]["similarity"] = {
                "score": similarity,
                "threshold": 0.6
            }
            
            if similarity < 0.6:
                results["valid"] = False
        
        # Basic quality checks
        results["checks"]["length"] = len(response)
        results["checks"]["empty"] = len(response.strip()) == 0
        
        if len(response.strip()) == 0:
            results["valid"] = False
        
        return results
    
    @staticmethod
    def _calculate_similarity(text1: str, text2: str) -> float:
        """Calculate text similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)


# Predefined prompt test suites
PROMPT_TEST_SUITES = {
    "basic_qa": [
        PromptTestCase(
            prompt="What is the capital of France?",
            expected_keywords=["Paris"],
            prompt_type=PromptType.QUESTION
        ),
        PromptTestCase(
            prompt="Explain quantum computing in simple terms.",
            expected_keywords=["quantum", "computing", "bits"],
            prompt_type=PromptType.INSTRUCTION
        ),
    ],
    "instruction_following": [
        PromptTestCase(
            prompt="List 5 benefits of exercise.",
            expected_keywords=["1.", "2.", "3.", "4.", "5."],
            prompt_type=PromptType.INSTRUCTION
        ),
        PromptTestCase(
            prompt="Summarize this in one sentence: [text]",
            prompt_type=PromptType.INSTRUCTION
        ),
    ],
    "creative": [
        PromptTestCase(
            prompt="Write a haiku about technology.",
            prompt_type=PromptType.CREATIVE
        ),
    ]
}
