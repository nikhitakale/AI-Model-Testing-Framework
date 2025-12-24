"""LLM Testing Module"""

import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
from anthropic import Anthropic
from ..core.base import BaseModelTester, TestResult, TestStatus


class LLMTester(BaseModelTester):
    """Tester for Large Language Models"""
    
    def __init__(self, model_name: str, provider: str = "openai", api_key: Optional[str] = None, **kwargs):
        super().__init__(model_name, **kwargs)
        self.provider = provider
        self.api_key = api_key
        
        if provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "anthropic":
            self.client = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def test_inference(self, prompt: str) -> TestResult:
        """Test basic inference"""
        try:
            start_time = time.time()
            
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                output = response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                output = response.content[0].text
            
            execution_time = (time.time() - start_time) * 1000
            
            result = TestResult(
                test_name="inference_test",
                status=TestStatus.PASSED if output else TestStatus.FAILED,
                message=f"Generated response: {output[:100]}...",
                execution_time_ms=execution_time,
                metadata={"prompt": prompt, "response": output}
            )
        except Exception as e:
            result = TestResult(
                test_name="inference_test",
                status=TestStatus.ERROR,
                message=str(e)
            )
        
        self.add_result(result)
        return result
    
    def test_performance(self, prompts: List[str], num_requests: int = 10) -> TestResult:
        """Test performance with multiple requests"""
        latencies = []
        
        try:
            for i in range(num_requests):
                prompt = prompts[i % len(prompts)]
                start_time = time.time()
                
                if self.provider == "openai":
                    self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=100
                    )
                elif self.provider == "anthropic":
                    self.client.messages.create(
                        model=self.model_name,
                        max_tokens=100,
                        messages=[{"role": "user", "content": prompt}]
                    )
                
                latency = (time.time() - start_time) * 1000
                latencies.append(latency)
            
            avg_latency = sum(latencies) / len(latencies)
            
            result = TestResult(
                test_name="performance_test",
                status=TestStatus.PASSED,
                score=avg_latency,
                message=f"Average latency: {avg_latency:.2f}ms",
                metadata={
                    "latencies": latencies,
                    "min": min(latencies),
                    "max": max(latencies),
                    "num_requests": num_requests
                }
            )
        except Exception as e:
            result = TestResult(
                test_name="performance_test",
                status=TestStatus.ERROR,
                message=str(e)
            )
        
        self.add_result(result)
        return result
    
    def test_prompt_consistency(self, prompt: str, num_runs: int = 5, temperature: float = 0.0) -> TestResult:
        """Test consistency of responses for the same prompt"""
        responses = []
        
        try:
            for _ in range(num_runs):
                if self.provider == "openai":
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature
                    )
                    responses.append(response.choices[0].message.content)
                elif self.provider == "anthropic":
                    response = self.client.messages.create(
                        model=self.model_name,
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature
                    )
                    responses.append(response.content[0].text)
            
            # Calculate consistency score (simple: all same = 1.0, all different = 0.0)
            unique_responses = len(set(responses))
            consistency_score = 1.0 - (unique_responses - 1) / num_runs
            
            result = TestResult(
                test_name="prompt_consistency_test",
                status=TestStatus.PASSED,
                score=consistency_score,
                message=f"Consistency score: {consistency_score:.2f}",
                metadata={
                    "prompt": prompt,
                    "num_unique_responses": unique_responses,
                    "responses": responses
                }
            )
        except Exception as e:
            result = TestResult(
                test_name="prompt_consistency_test",
                status=TestStatus.ERROR,
                message=str(e)
            )
        
        self.add_result(result)
        return result
    
    def test_hallucination_detection(self, prompt: str, ground_truth: str) -> TestResult:
        """Test for hallucinations by comparing with ground truth"""
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                output = response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                output = response.content[0].text
            
            # Simple similarity check (in production, use more sophisticated methods)
            similarity = self._calculate_similarity(output, ground_truth)
            
            result = TestResult(
                test_name="hallucination_detection_test",
                status=TestStatus.PASSED if similarity > 0.5 else TestStatus.FAILED,
                score=similarity,
                message=f"Similarity to ground truth: {similarity:.2f}",
                metadata={
                    "prompt": prompt,
                    "ground_truth": ground_truth,
                    "response": output
                }
            )
        except Exception as e:
            result = TestResult(
                test_name="hallucination_detection_test",
                status=TestStatus.ERROR,
                message=str(e)
            )
        
        self.add_result(result)
        return result
    
    @staticmethod
    def _calculate_similarity(text1: str, text2: str) -> float:
        """Calculate simple text similarity (Jaccard)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
