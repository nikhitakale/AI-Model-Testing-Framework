"""Test example for evaluation metrics"""

import pytest
from src.evaluation.metrics import EvaluationMetrics, ModelComparator


def test_bleu_score():
    """Test BLEU score calculation"""
    reference = "the cat is on the mat"
    candidate = "the cat is on the mat"
    
    score = EvaluationMetrics.calculate_bleu(reference, candidate)
    
    assert score > 0.9  # Should be high for identical strings


def test_rouge_score():
    """Test ROUGE score calculation"""
    reference = "the cat sat on the mat"
    candidate = "the cat is on the mat"
    
    scores = EvaluationMetrics.calculate_rouge(reference, candidate)
    
    assert "rouge1" in scores
    assert "rouge2" in scores
    assert "rougeL" in scores
    assert all(0 <= score <= 1 for score in scores.values())


def test_exact_match():
    """Test exact match calculation"""
    reference = "Paris"
    
    assert EvaluationMetrics.calculate_exact_match(reference, "Paris") == 1.0
    assert EvaluationMetrics.calculate_exact_match(reference, "paris") == 1.0
    assert EvaluationMetrics.calculate_exact_match(reference, "London") == 0.0


def test_f1_score():
    """Test F1 score calculation"""
    reference = ["the", "cat", "sat", "on", "mat"]
    candidate = ["the", "cat", "is", "on", "mat"]
    
    score = EvaluationMetrics.calculate_f1_score(reference, candidate)
    
    assert 0 <= score <= 1


def test_semantic_similarity():
    """Test semantic similarity"""
    text1 = "the quick brown fox"
    text2 = "the quick brown dog"
    
    score = EvaluationMetrics.calculate_semantic_similarity(text1, text2)
    
    assert 0 <= score <= 1
    assert score > 0.5  # Should have decent overlap


def test_diversity_score():
    """Test diversity score"""
    texts = [
        "hello world",
        "goodbye world",
        "hello universe"
    ]
    
    score = EvaluationMetrics.calculate_diversity_score(texts)
    
    assert 0 <= score <= 1


def test_model_comparator():
    """Test model comparison"""
    model_results = {
        "model_a": [
            {"status": "passed", "score": 0.9, "execution_time_ms": 100},
            {"status": "passed", "score": 0.8, "execution_time_ms": 120}
        ],
        "model_b": [
            {"status": "passed", "score": 0.7, "execution_time_ms": 80},
            {"status": "failed", "score": 0.5, "execution_time_ms": 90}
        ]
    }
    
    comparison = ModelComparator.compare_models(model_results)
    
    assert "models" in comparison
    assert "metrics" in comparison
    assert "best_model" in comparison
    assert len(comparison["models"]) == 2
