"""Model evaluation metrics"""

from typing import List, Dict, Any, Optional
import numpy as np
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


class EvaluationMetrics:
    """Metrics for model evaluation"""
    
    @staticmethod
    def calculate_bleu(reference: str, candidate: str) -> float:
        """Calculate BLEU score"""
        reference_tokens = reference.split()
        candidate_tokens = candidate.split()
        
        smoothing = SmoothingFunction().method1
        score = sentence_bleu([reference_tokens], candidate_tokens, 
                             smoothing_function=smoothing)
        return score
    
    @staticmethod
    def calculate_rouge(reference: str, candidate: str) -> Dict[str, float]:
        """Calculate ROUGE scores"""
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], 
                                          use_stemmer=True)
        scores = scorer.score(reference, candidate)
        
        return {
            'rouge1': scores['rouge1'].fmeasure,
            'rouge2': scores['rouge2'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure
        }
    
    @staticmethod
    def calculate_exact_match(reference: str, candidate: str) -> float:
        """Calculate exact match score"""
        return 1.0 if reference.strip().lower() == candidate.strip().lower() else 0.0
    
    @staticmethod
    def calculate_f1_score(
        reference_tokens: List[str],
        candidate_tokens: List[str]
    ) -> float:
        """Calculate F1 score for token overlap"""
        common = set(reference_tokens) & set(candidate_tokens)
        
        if len(common) == 0:
            return 0.0
        
        precision = len(common) / len(candidate_tokens) if candidate_tokens else 0
        recall = len(common) / len(reference_tokens) if reference_tokens else 0
        
        if precision + recall == 0:
            return 0.0
        
        f1 = 2 * (precision * recall) / (precision + recall)
        return f1
    
    @staticmethod
    def calculate_perplexity(log_probabilities: List[float]) -> float:
        """Calculate perplexity"""
        if not log_probabilities:
            return float('inf')
        
        avg_log_prob = np.mean(log_probabilities)
        perplexity = np.exp(-avg_log_prob)
        return perplexity
    
    @staticmethod
    def calculate_semantic_similarity(text1: str, text2: str) -> float:
        """Calculate simple semantic similarity (Jaccard)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    @staticmethod
    def calculate_diversity_score(texts: List[str]) -> float:
        """Calculate diversity score across multiple texts"""
        if not texts:
            return 0.0
        
        unique_tokens = set()
        total_tokens = 0
        
        for text in texts:
            tokens = text.lower().split()
            unique_tokens.update(tokens)
            total_tokens += len(tokens)
        
        if total_tokens == 0:
            return 0.0
        
        return len(unique_tokens) / total_tokens


class ModelComparator:
    """Compare multiple models"""
    
    @staticmethod
    def compare_models(
        model_results: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Compare results from multiple models"""
        
        comparison = {
            "models": list(model_results.keys()),
            "metrics": {}
        }
        
        for model_name, results in model_results.items():
            total_tests = len(results)
            passed = sum(1 for r in results if r.get("status") == "passed")
            
            scores = [r.get("score", 0) for r in results if r.get("score") is not None]
            avg_score = np.mean(scores) if scores else 0
            
            exec_times = [r.get("execution_time_ms", 0) for r in results 
                         if r.get("execution_time_ms") is not None]
            avg_exec_time = np.mean(exec_times) if exec_times else 0
            
            comparison["metrics"][model_name] = {
                "total_tests": total_tests,
                "passed": passed,
                "pass_rate": passed / total_tests if total_tests > 0 else 0,
                "avg_score": avg_score,
                "avg_execution_time_ms": avg_exec_time
            }
        
        # Determine winner
        if comparison["metrics"]:
            best_model = max(comparison["metrics"].items(), 
                           key=lambda x: x[1]["pass_rate"])
            comparison["best_model"] = best_model[0]
        
        return comparison
