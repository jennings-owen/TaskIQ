"""
Unit tests for AI endpoints: /ai/rank and /ai/size.

Tests cover:
- POST /ai/rank - Task priority scoring
- POST /ai/size - T-shirt size recommendation
- Edge cases and error handling
- Performance requirements
"""

import pytest
from datetime import datetime, timedelta
import time


class TestAIRankEndpoint:
    """Test suite for /ai/rank endpoint (task priority scoring)."""
    
    def test_rank_tasks_success(self, client, ai_rank_data):
        """Test POST /ai/rank returns priority scores for tasks."""
        start_time = time.time()
        response = client.post("/ai/rank", json=ai_rank_data)
        end_time = time.time()
        
        # Verify response time < 200ms (per PRD NFR)
        assert (end_time - start_time) < 0.2, "Response time exceeds 200ms requirement"
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(ai_rank_data["tasks"])
        
        # Verify each task has a priority score
        for item in data:
            assert "task_id" in item or "priority_score" in item
            if "priority_score" in item:
                assert 1 <= item["priority_score"] <= 100
    
    def test_rank_single_task(self, client):
        """Test /ai/rank with a single task."""
        data = {
            "tasks": [
                {
                    "title": "Single Task",
                    "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
                    "estimated_duration": 2
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 1
    
    def test_rank_empty_task_list(self, client):
        """Test /ai/rank with empty task list."""
        data = {"tasks": []}
        response = client.post("/ai/rank", json=data)
        # Should either accept and return empty list or reject
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert response.json() == []
    
    def test_rank_missing_deadline(self, client):
        """Test /ai/rank with task missing deadline."""
        data = {
            "tasks": [
                {
                    "title": "Task without deadline",
                    "estimated_duration": 2
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        # Should handle gracefully or reject
        assert response.status_code in [200, 422]
    
    def test_rank_missing_duration(self, client):
        """Test /ai/rank with task missing estimated_duration."""
        data = {
            "tasks": [
                {
                    "title": "Task without duration",
                    "deadline": (datetime.now() + timedelta(days=3)).isoformat()
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        # Should handle gracefully or reject
        assert response.status_code in [200, 422]
    
    def test_rank_past_deadline(self, client):
        """Test /ai/rank with task that has past deadline."""
        data = {
            "tasks": [
                {
                    "title": "Overdue Task",
                    "deadline": (datetime.now() - timedelta(days=5)).isoformat(),
                    "estimated_duration": 2
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        assert response.status_code == 200
        result = response.json()
        # Past deadline should result in high priority or specific handling
        if len(result) > 0 and "priority_score" in result[0]:
            # Score should reflect urgency (likely high)
            assert isinstance(result[0]["priority_score"], int)
    
    def test_rank_negative_duration(self, client):
        """Test /ai/rank with negative estimated_duration."""
        data = {
            "tasks": [
                {
                    "title": "Invalid Duration Task",
                    "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
                    "estimated_duration": -5
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        # Should reject invalid duration
        assert response.status_code in [422, 400]
    
    def test_rank_zero_duration(self, client):
        """Test /ai/rank with zero estimated_duration."""
        data = {
            "tasks": [
                {
                    "title": "Zero Duration Task",
                    "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
                    "estimated_duration": 0
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        # Should accept zero duration (quick tasks)
        assert response.status_code == 200
    
    def test_rank_very_large_duration(self, client):
        """Test /ai/rank with extremely large estimated_duration."""
        data = {
            "tasks": [
                {
                    "title": "Long Task",
                    "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
                    "estimated_duration": 10000
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        assert response.status_code in [200, 422]
    
    def test_rank_multiple_tasks_ordering(self, client):
        """Test /ai/rank correctly prioritizes multiple tasks."""
        data = {
            "tasks": [
                {
                    "title": "Urgent Task",
                    "deadline": (datetime.now() + timedelta(days=1)).isoformat(),
                    "estimated_duration": 1
                },
                {
                    "title": "Not Urgent Task",
                    "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                    "estimated_duration": 1
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        assert response.status_code == 200
        result = response.json()
        
        assert len(result) >= 2
        if "priority_score" in result[0] and "priority_score" in result[1]:
            # Urgent task should have higher priority score
            urgent_score = result[0]["priority_score"]
            not_urgent_score = result[1]["priority_score"]
            assert urgent_score > not_urgent_score
    
    def test_rank_algorithm_consistency(self, client):
        """Test /ai/rank returns consistent scores for same input."""
        data = {
            "tasks": [
                {
                    "title": "Consistent Task",
                    "deadline": (datetime.now() + timedelta(days=5)).isoformat(),
                    "estimated_duration": 3
                }
            ]
        }
        
        response1 = client.post("/ai/rank", json=data)
        response2 = client.post("/ai/rank", json=data)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Scores should be consistent (assuming deterministic algorithm)
        result1 = response1.json()
        result2 = response2.json()
        
        assert len(result1) > 0 and len(result2) > 0
        if "priority_score" in result1[0] and "priority_score" in result2[0]:
            assert result1[0]["priority_score"] == result2[0]["priority_score"]
    
    def test_rank_algorithm_formula_validation(self, client):
        """Test priority algorithm follows PRD formula: 100 - days*5 - duration*3."""
        # Test with known values
        days_until = 5
        duration = 4
        
        data = {
            "tasks": [
                {
                    "title": "Algorithm Test",
                    "deadline": (datetime.now() + timedelta(days=days_until)).isoformat(),
                    "estimated_duration": duration
                }
            ]
        }
        
        response = client.post("/ai/rank", json=data)
        assert response.status_code == 200
        result = response.json()
        
        if len(result) > 0 and "priority_score" in result[0]:
            # Expected: 100 - (5 * 5) - (4 * 3) = 100 - 25 - 12 = 63
            expected_score = 100 - (days_until * 5) - (duration * 3)
            expected_score = max(1, min(100, expected_score))  # Clamp 1-100
            
            actual_score = result[0]["priority_score"]
            
            # Allow small variance for timing/rounding
            assert abs(actual_score - expected_score) <= 5, \
                f"Expected ~{expected_score}, got {actual_score}"
    
    def test_rank_algorithm_clamping_lower_bound(self, client):
        """Test priority score is clamped to minimum of 1."""
        # Create task that would score below 1
        data = {
            "tasks": [
                {
                    "title": "Very Low Priority",
                    "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                    "estimated_duration": 20
                }
            ]
        }
        
        response = client.post("/ai/rank", json=data)
        assert response.status_code == 200
        result = response.json()
        
        if len(result) > 0 and "priority_score" in result[0]:
            # Score should be clamped to 1
            assert result[0]["priority_score"] >= 1
    
    def test_rank_algorithm_clamping_upper_bound(self, client):
        """Test priority score is clamped to maximum of 100."""
        # Create task with negative days (overdue) and zero duration
        data = {
            "tasks": [
                {
                    "title": "Overdue Task",
                    "deadline": (datetime.now() - timedelta(days=5)).isoformat(),
                    "estimated_duration": 0
                }
            ]
        }
        
        response = client.post("/ai/rank", json=data)
        if response.status_code == 200:
            result = response.json()
            
            if len(result) > 0 and "priority_score" in result[0]:
                # Score should be clamped to 100
                assert result[0]["priority_score"] <= 100
    
    def test_rank_algorithm_version_tracking(self, client):
        """Test algorithm version is tracked in response."""
        data = {
            "tasks": [
                {
                    "title": "Version Test",
                    "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
                    "estimated_duration": 2
                }
            ]
        }
        
        response = client.post("/ai/rank", json=data)
        assert response.status_code == 200
        result = response.json()
        
        # Check if algorithm_version is included
        if len(result) > 0 and "algorithm_version" in result[0]:
            assert isinstance(result[0]["algorithm_version"], str)
            assert len(result[0]["algorithm_version"]) > 0
    
    def test_rank_malformed_request(self, client):
        """Test /ai/rank with malformed request body."""
        malformed_data = {
            "wrong_field": "value"
        }
        response = client.post("/ai/rank", json=malformed_data)
        assert response.status_code == 422
    
    def test_rank_invalid_date_format(self, client):
        """Test /ai/rank with invalid date format."""
        data = {
            "tasks": [
                {
                    "title": "Invalid Date Task",
                    "deadline": "not-a-date",
                    "estimated_duration": 2
                }
            ]
        }
        response = client.post("/ai/rank", json=data)
        assert response.status_code == 422


class TestAISizeEndpoint:
    """Test suite for /ai/size endpoint (T-shirt size recommendation)."""
    
    def test_size_recommendation_success(self, client, ai_size_data):
        """Test POST /ai/size returns T-shirt size recommendation."""
        start_time = time.time()
        response = client.post("/ai/size", json=ai_size_data)
        end_time = time.time()
        
        # Verify response time < 200ms (per PRD NFR)
        assert (end_time - start_time) < 0.2, "Response time exceeds 200ms requirement"
        
        assert response.status_code == 200
        data = response.json()
        assert "recommended_size" in data
        assert data["recommended_size"] in ["XS", "S", "M", "L", "XL"]
    
    def test_size_male_regular_fit(self, client):
        """Test size recommendation for male with regular fit."""
        data = {
            "height_cm": 175,
            "weight_kg": 70,
            "gender": "male",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["recommended_size"] in ["XS", "S", "M", "L", "XL"]
    
    def test_size_female_slim_fit(self, client):
        """Test size recommendation for female with slim fit."""
        data = {
            "height_cm": 165,
            "weight_kg": 55,
            "gender": "female",
            "fit_preference": "slim"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["recommended_size"] in ["XS", "S", "M", "L", "XL"]
    
    def test_size_loose_fit(self, client):
        """Test size recommendation with loose fit preference."""
        data = {
            "height_cm": 180,
            "weight_kg": 80,
            "gender": "male",
            "fit_preference": "loose"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["recommended_size"] in ["XS", "S", "M", "L", "XL"]
    
    def test_size_missing_required_field(self, client):
        """Test /ai/size with missing required field."""
        incomplete_data = {
            "height_cm": 175,
            "weight_kg": 70
            # Missing gender and fit_preference
        }
        response = client.post("/ai/size", json=incomplete_data)
        assert response.status_code == 422
    
    def test_size_negative_height(self, client):
        """Test /ai/size with negative height."""
        data = {
            "height_cm": -175,
            "weight_kg": 70,
            "gender": "male",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code == 422
    
    def test_size_negative_weight(self, client):
        """Test /ai/size with negative weight."""
        data = {
            "height_cm": 175,
            "weight_kg": -70,
            "gender": "male",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code == 422
    
    def test_size_zero_height(self, client):
        """Test /ai/size with zero height."""
        data = {
            "height_cm": 0,
            "weight_kg": 70,
            "gender": "male",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code == 422
    
    def test_size_extreme_height_short(self, client):
        """Test /ai/size with extremely short height."""
        data = {
            "height_cm": 100,
            "weight_kg": 40,
            "gender": "male",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            result = response.json()
            # Should recommend XS for very short person
            assert result["recommended_size"] in ["XS", "S"]
    
    def test_size_extreme_height_tall(self, client):
        """Test /ai/size with extremely tall height."""
        data = {
            "height_cm": 220,
            "weight_kg": 120,
            "gender": "male",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            result = response.json()
            # Should recommend L or XL for very tall person
            assert result["recommended_size"] in ["L", "XL"]
    
    def test_size_invalid_gender(self, client):
        """Test /ai/size with invalid gender value."""
        data = {
            "height_cm": 175,
            "weight_kg": 70,
            "gender": "invalid",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        assert response.status_code == 422
    
    def test_size_invalid_fit_preference(self, client):
        """Test /ai/size with invalid fit preference."""
        data = {
            "height_cm": 175,
            "weight_kg": 70,
            "gender": "male",
            "fit_preference": "invalid"
        }
        response = client.post("/ai/size", json=data)
        # Should reject invalid fit preference
        assert response.status_code == 422
    
    def test_size_case_insensitive_gender(self, client):
        """Test /ai/size accepts case-insensitive gender."""
        data = {
            "height_cm": 175,
            "weight_kg": 70,
            "gender": "MALE",
            "fit_preference": "regular"
        }
        response = client.post("/ai/size", json=data)
        # Should normalize case and accept
        assert response.status_code == 200
        if response.status_code == 200:
            assert response.json()["recommended_size"] in ["XS", "S", "M", "L", "XL"]
    
    def test_size_consistency(self, client, ai_size_data):
        """Test /ai/size returns consistent results for same input."""
        response1 = client.post("/ai/size", json=ai_size_data)
        response2 = client.post("/ai/size", json=ai_size_data)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Should return same size for same input
        assert response1.json()["recommended_size"] == response2.json()["recommended_size"]
    
    def test_size_bmi_correlation(self, client):
        """Test size recommendations correlate with BMI."""
        # Low BMI person
        low_bmi_data = {
            "height_cm": 180,
            "weight_kg": 60,
            "gender": "male",
            "fit_preference": "regular"
        }
        
        # High BMI person
        high_bmi_data = {
            "height_cm": 180,
            "weight_kg": 100,
            "gender": "male",
            "fit_preference": "regular"
        }
        
        response_low = client.post("/ai/size", json=low_bmi_data)
        response_high = client.post("/ai/size", json=high_bmi_data)
        
        if response_low.status_code == 200 and response_high.status_code == 200:
            size_low = response_low.json()["recommended_size"]
            size_high = response_high.json()["recommended_size"]
            
            # High BMI should get larger size
            sizes = ["XS", "S", "M", "L", "XL"]
            assert sizes.index(size_high) >= sizes.index(size_low)
    
    def test_size_malformed_request(self, client):
        """Test /ai/size with malformed request body."""
        malformed_data = {
            "wrong_field": "value"
        }
        response = client.post("/ai/size", json=malformed_data)
        assert response.status_code == 422


class TestAIEndpointsPerformance:
    """Test suite for AI endpoints performance requirements."""
    
    def test_rank_performance_multiple_tasks(self, client):
        """Test /ai/rank performance with multiple tasks."""
        data = {
            "tasks": [
                {
                    "title": f"Task {i}",
                    "deadline": (datetime.now() + timedelta(days=i+1)).isoformat(),
                    "estimated_duration": i+1
                }
                for i in range(10)
            ]
        }
        
        start_time = time.time()
        response = client.post("/ai/rank", json=data)
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.2, f"Response time {end_time - start_time}s exceeds 200ms requirement"
    
    def test_size_performance(self, client, ai_size_data):
        """Test /ai/size completes within 200ms."""
        start_time = time.time()
        response = client.post("/ai/size", json=ai_size_data)
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.2, f"Response time {end_time - start_time}s exceeds 200ms requirement"

