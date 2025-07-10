#!/usr/bin/env python3
"""
🌀 Sacred Geometry Engine
Core implementation of Sacred Geometry patterns for AAR processing

This module implements the fundamental Sacred Geometry patterns:
- Circle: Complete functionality, proper error handling
- Triangle: Stable architecture with three-tier validation
- Spiral: Progressive enhancement and iterative improvement
- Golden Ratio: Optimal proportions in API design (φ = 1.618)
- Fractal: Self-similar patterns at multiple scales
"""

import hashlib
import json
import math
from datetime import datetime
from typing import Any, Dict, List

import structlog

logger = structlog.get_logger(__name__)


class SacredGeometryEngine:
    """Core Sacred Geometry processing engine"""

    def __init__(self):
        self.phi = (1 + math.sqrt(5)) / 2  # Golden Ratio φ = 1.618...
        self.is_initialized = False
        self.patterns = {
            "circle": self._circle_pattern,
            "triangle": self._triangle_pattern,
            "spiral": self._spiral_pattern,
            "golden_ratio": self._golden_ratio_pattern,
            "fractal": self._fractal_pattern,
        }

    async def initialize(self):
        """Initialize Sacred Geometry engine"""
        logger.info("🌀 Initializing Sacred Geometry Engine")

        # Validate mathematical constants
        assert (
            abs(self.phi - 1.618033988749895) < 1e-10
        ), "Golden ratio calculation error"

        # Initialize pattern processors
        await self._initialize_patterns()

        self.is_initialized = True
        logger.info("✅ Sacred Geometry Engine initialized", phi=self.phi)

    async def _initialize_patterns(self):
        """Initialize Sacred Geometry pattern processors"""
        # Pre-compute common Golden Ratio values
        self.phi_powers = {0: 1, 1: self.phi, 2: self.phi**2, 3: self.phi**3}

        # Initialize Fibonacci sequence for spiral calculations
        self.fibonacci = [1, 1]
        for i in range(2, 20):
            self.fibonacci.append(self.fibonacci[i - 1] + self.fibonacci[i - 2])

        logger.debug(
            "Pattern processors initialized",
            phi_powers=list(self.phi_powers.keys()),
            fibonacci_length=len(self.fibonacci),
        )

    def is_healthy(self) -> bool:
        """Check if Sacred Geometry engine is healthy"""
        return self.is_initialized and abs(self.phi - 1.618033988749895) < 1e-10

    def validate_patterns(self, patterns: List[str]) -> bool:
        """Validate that requested patterns are supported"""
        return all(pattern in self.patterns for pattern in patterns)

    def generate_aar_id(self, mission_id: str) -> str:
        """Generate AAR ID using Sacred Geometry principles"""
        # Use Golden Ratio to create unique but meaningful IDs
        timestamp = datetime.now().isoformat()
        combined = f"{mission_id}_{timestamp}_{self.phi}"

        # Create hash and apply Golden Ratio proportioning
        hash_obj = hashlib.sha256(combined.encode())
        hex_digest = hash_obj.hexdigest()

        # Extract Golden Ratio proportioned sections
        phi_section = int(len(hex_digest) / self.phi)
        aar_id = hex_digest[:phi_section]

        logger.debug(
            "Generated AAR ID",
            mission_id=mission_id,
            aar_id=aar_id,
            phi_section=phi_section,
        )

        return f"aar_{aar_id}"

    async def validate_data(self, data: Dict) -> Dict[str, Any]:
        """Validate data against Sacred Geometry patterns"""
        validation_results = {}

        for pattern_name in self.patterns:
            try:
                pattern_func = self.patterns[pattern_name]
                result = await pattern_func(data, validate_only=True)
                validation_results[pattern_name] = {
                    "valid": result.get("valid", False),
                    "score": result.get("score", 0.0),
                    "details": result.get("details", {}),
                }
            except Exception as e:
                logger.error(
                    "Pattern validation failed", pattern=pattern_name, error=str(e)
                )
                validation_results[pattern_name] = {
                    "valid": False,
                    "score": 0.0,
                    "error": str(e),
                }

        # Calculate overall compliance
        valid_patterns = sum(
            1 for r in validation_results.values() if r.get("valid", False)
        )
        overall_score = sum(
            r.get("score", 0) for r in validation_results.values()
        ) / len(validation_results)

        return {
            "overall_compliance": overall_score,
            "valid_patterns": valid_patterns,
            "total_patterns": len(validation_results),
            "pattern_results": validation_results,
            "timestamp": datetime.now().isoformat(),
        }

    async def _circle_pattern(
        self, data: Dict, validate_only: bool = False
    ) -> Dict[str, Any]:
        """Circle: Complete functionality, proper error handling"""
        try:
            # Check for completeness - all required fields present
            required_fields = ["mission_id", "mission_type", "context_data"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return {
                    "valid": False,
                    "score": 0.0,
                    "details": {"missing_fields": missing_fields},
                }

            # Check for circularity - data references form complete cycles
            circular_score = self._calculate_circular_completeness(data)

            # Check for proper error handling patterns
            error_handling_score = self._check_error_handling_patterns(data)

            overall_score = (circular_score + error_handling_score) / 2

            return {
                "valid": overall_score >= 0.7,
                "score": overall_score,
                "details": {
                    "circular_completeness": circular_score,
                    "error_handling": error_handling_score,
                    "complete_fields": len(data) - len(missing_fields),
                },
            }

        except Exception as e:
            logger.error("Circle pattern validation failed", error=str(e))
            return {"valid": False, "score": 0.0, "error": str(e)}

    async def _triangle_pattern(
        self, data: Dict, validate_only: bool = False
    ) -> Dict[str, Any]:
        """Triangle: Stable architecture with three-tier validation"""
        try:
            # Three-tier validation: Structure, Content, Context
            structure_score = self._validate_structural_integrity(data)
            content_score = self._validate_content_quality(data)
            context_score = self._validate_contextual_relevance(data)

            # Triangular stability check - all three tiers must be balanced
            scores = [structure_score, content_score, context_score]
            balance_factor = 1 - (max(scores) - min(scores))  # Penalty for imbalance

            overall_score = (sum(scores) / 3) * balance_factor

            return {
                "valid": overall_score >= 0.7 and all(s >= 0.5 for s in scores),
                "score": overall_score,
                "details": {
                    "structure": structure_score,
                    "content": content_score,
                    "context": context_score,
                    "balance_factor": balance_factor,
                },
            }

        except Exception as e:
            logger.error("Triangle pattern validation failed", error=str(e))
            return {"valid": False, "score": 0.0, "error": str(e)}

    async def _spiral_pattern(
        self, data: Dict, validate_only: bool = False
    ) -> Dict[str, Any]:
        """Spiral: Progressive enhancement and iterative improvement"""
        try:
            # Check for spiral growth patterns in data
            spiral_growth = self._detect_spiral_growth(data)

            # Check for iterative improvement indicators
            iteration_quality = self._assess_iteration_quality(data)

            # Check for progressive enhancement patterns
            enhancement_progression = self._evaluate_enhancement_progression(data)

            # Fibonacci-based scoring
            fib_alignment = self._check_fibonacci_alignment(data)

            overall_score = (
                spiral_growth
                + iteration_quality
                + enhancement_progression
                + fib_alignment
            ) / 4

            return {
                "valid": overall_score >= 0.6,
                "score": overall_score,
                "details": {
                    "spiral_growth": spiral_growth,
                    "iteration_quality": iteration_quality,
                    "enhancement_progression": enhancement_progression,
                    "fibonacci_alignment": fib_alignment,
                },
            }

        except Exception as e:
            logger.error("Spiral pattern validation failed", error=str(e))
            return {"valid": False, "score": 0.0, "error": str(e)}

    async def _golden_ratio_pattern(
        self, data: Dict, validate_only: bool = False
    ) -> Dict[str, Any]:
        """Golden Ratio: Optimal proportions in API design (φ = 1.618)"""
        try:
            # Check proportional relationships in data structure
            proportion_score = self._analyze_proportional_relationships(data)

            # Check for Golden Ratio in numerical values
            numerical_golden_ratio = self._find_golden_ratios_in_values(data)

            # Check for optimal API design proportions
            api_design_score = self._evaluate_api_design_proportions(data)

            # Overall Golden Ratio compliance
            overall_score = (
                proportion_score + numerical_golden_ratio + api_design_score
            ) / 3

            return {
                "valid": overall_score >= 0.618,  # Use φ^-1 as threshold
                "score": overall_score,
                "details": {
                    "proportional_relationships": proportion_score,
                    "numerical_golden_ratios": numerical_golden_ratio,
                    "api_design_proportions": api_design_score,
                    "phi_threshold": 0.618,
                },
            }

        except Exception as e:
            logger.error("Golden Ratio pattern validation failed", error=str(e))
            return {"valid": False, "score": 0.0, "error": str(e)}

    async def _fractal_pattern(
        self, data: Dict, validate_only: bool = False
    ) -> Dict[str, Any]:
        """Fractal: Self-similar patterns at multiple scales"""
        try:
            # Check for self-similarity at different scales
            self_similarity = self._detect_self_similarity(data)

            # Check for recursive patterns
            recursive_patterns = self._analyze_recursive_patterns(data)

            # Check for scale invariance
            scale_invariance = self._evaluate_scale_invariance(data)

            # Check for fractal dimensions
            fractal_dimension = self._calculate_fractal_dimension(data)

            overall_score = (
                self_similarity
                + recursive_patterns
                + scale_invariance
                + fractal_dimension
            ) / 4

            return {
                "valid": overall_score >= 0.65,
                "score": overall_score,
                "details": {
                    "self_similarity": self_similarity,
                    "recursive_patterns": recursive_patterns,
                    "scale_invariance": scale_invariance,
                    "fractal_dimension": fractal_dimension,
                },
            }

        except Exception as e:
            logger.error("Fractal pattern validation failed", error=str(e))
            return {"valid": False, "score": 0.0, "error": str(e)}

    # Helper methods for pattern validation

    def _calculate_circular_completeness(self, data: Dict) -> float:
        """Calculate how complete/circular the data structure is"""
        # Simple heuristic: check for cross-references and completeness
        total_fields = len(data)
        if total_fields == 0:
            return 0.0

        # Count fields that reference other fields (circular references)
        circular_refs = 0
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # Check for references to other keys in the data
                value_str = str(value).lower()
                for other_key in data.keys():
                    if other_key != key and other_key.lower() in value_str:
                        circular_refs += 1
                        break

        return min(circular_refs / total_fields, 1.0)

    def _check_error_handling_patterns(self, data: Dict) -> float:
        """Check for proper error handling patterns in data"""
        error_indicators = ["error", "exception", "try", "catch", "finally", "handle"]

        data_str = json.dumps(data).lower()
        found_indicators = sum(
            1 for indicator in error_indicators if indicator in data_str
        )

        return min(found_indicators / len(error_indicators), 1.0)

    def _validate_structural_integrity(self, data: Dict) -> float:
        """Validate structural integrity (Triangle tier 1)"""
        try:
            # Check for well-formed JSON structure
            json.dumps(data)

            # Check for reasonable nesting depth (< 10 levels)
            max_depth = self._calculate_max_depth(data)
            depth_score = max(0, 1 - (max_depth - 5) / 10) if max_depth > 5 else 1.0

            # Check for balanced structure
            balance_score = self._calculate_structure_balance(data)

            return (depth_score + balance_score) / 2

        except Exception:
            return 0.0

    def _validate_content_quality(self, data: Dict) -> float:
        """Validate content quality (Triangle tier 2)"""
        if not data:
            return 0.0

        # Check for meaningful content (not just empty values)
        meaningful_fields = 0
        total_fields = 0

        for key, value in data.items():
            total_fields += 1
            if value and str(value).strip():
                meaningful_fields += 1

        return meaningful_fields / total_fields if total_fields > 0 else 0.0

    def _validate_contextual_relevance(self, data: Dict) -> float:
        """Validate contextual relevance (Triangle tier 3)"""
        # Check for context-related fields
        context_fields = ["context", "background", "environment", "situation", "scope"]

        context_score = 0
        for field in context_fields:
            if any(field in str(key).lower() for key in data.keys()):
                context_score += 1

        return min(context_score / len(context_fields), 1.0)

    def _detect_spiral_growth(self, data: Dict) -> float:
        """Detect spiral growth patterns in data"""
        # Look for sequential or progressive data structures
        sequential_indicators = ["step", "phase", "iteration", "version", "level"]

        data_str = json.dumps(data).lower()
        found_sequences = sum(
            1 for indicator in sequential_indicators if indicator in data_str
        )

        return min(found_sequences / len(sequential_indicators), 1.0)

    def _assess_iteration_quality(self, data: Dict) -> float:
        """Assess iteration quality indicators"""
        iteration_indicators = ["improve", "enhance", "refine", "iterate", "evolve"]

        data_str = json.dumps(data).lower()
        found_iterations = sum(
            1 for indicator in iteration_indicators if indicator in data_str
        )

        return min(found_iterations / len(iteration_indicators), 1.0)

    def _evaluate_enhancement_progression(self, data: Dict) -> float:
        """Evaluate progressive enhancement patterns"""
        # Look for version numbers, timestamps, or progression indicators
        if isinstance(data, dict):
            # Check for versioning patterns
            version_fields = [
                k for k in data.keys() if "version" in k.lower() or "v" in k.lower()
            ]
            timestamp_fields = [
                k
                for k in data.keys()
                if any(t in k.lower() for t in ["time", "date", "created", "updated"])
            ]

            progression_score = (
                len(version_fields) + len(timestamp_fields)
            ) / 4  # Normalize to 0-1
            return min(progression_score, 1.0)

        return 0.5  # Default moderate score

    def _check_fibonacci_alignment(self, data: Dict) -> float:
        """Check for Fibonacci sequence alignment in data"""
        # Look for numerical values that align with Fibonacci sequence
        numbers = self._extract_numbers_from_data(data)
        if not numbers:
            return 0.5

        fib_matches = 0
        for num in numbers:
            if int(num) in self.fibonacci:
                fib_matches += 1

        return min(fib_matches / len(numbers), 1.0)

    def _analyze_proportional_relationships(self, data: Dict) -> float:
        """Analyze proportional relationships for Golden Ratio compliance"""
        numbers = self._extract_numbers_from_data(data)
        if len(numbers) < 2:
            return 0.5

        ratios = []
        for i in range(len(numbers) - 1):
            if numbers[i] != 0:
                ratio = numbers[i + 1] / numbers[i]
                ratios.append(ratio)

        if not ratios:
            return 0.5

        # Check how many ratios are close to Golden Ratio
        golden_ratio_matches = sum(1 for r in ratios if abs(r - self.phi) < 0.1)

        return min(golden_ratio_matches / len(ratios), 1.0)

    def _find_golden_ratios_in_values(self, data: Dict) -> float:
        """Find Golden Ratio occurrences in numerical values"""
        numbers = self._extract_numbers_from_data(data)
        if not numbers:
            return 0.5

        golden_matches = sum(1 for num in numbers if abs(num - self.phi) < 0.01)

        return min(golden_matches / len(numbers), 1.0)

    def _evaluate_api_design_proportions(self, data: Dict) -> float:
        """Evaluate API design proportions against Golden Ratio"""
        if not isinstance(data, dict):
            return 0.0

        # Check if the number of fields follows Golden Ratio proportions
        total_fields = len(data)
        if total_fields == 0:
            return 0.0

        # Ideal distribution: ~62% main content, ~38% metadata/context
        content_fields = 0
        meta_fields = 0

        for key in data.keys():
            if any(
                meta in key.lower() for meta in ["meta", "context", "info", "config"]
            ):
                meta_fields += 1
            else:
                content_fields += 1

        if total_fields == 0:
            return 0.0

        content_ratio = content_fields / total_fields
        optimal_content_ratio = 1 / self.phi  # ≈ 0.618

        # Score based on how close we are to the golden ratio
        ratio_deviation = abs(content_ratio - optimal_content_ratio)
        score = max(0, 1 - ratio_deviation * 2)  # Scale deviation to 0-1

        return score

    def _detect_self_similarity(self, data: Dict) -> float:
        """Detect self-similar patterns in data structure"""
        if not isinstance(data, dict):
            return 0.0
        # Check for similar structures at different levels
        structure_patterns: Dict[str, int] = {}
        self._analyze_structure_patterns(data, structure_patterns, 0)

        # Count how many patterns repeat
        repeated_patterns = sum(
            count for count in structure_patterns.values() if count > 1
        )
        total_patterns = len(structure_patterns)

        return repeated_patterns / total_patterns if total_patterns > 0 else 0.0

    def _analyze_recursive_patterns(self, data: Dict) -> float:
        """Analyze recursive patterns in data"""
        # Look for recursive structures or references
        recursive_score = 0
        total_checks = 0

        def check_recursion(obj, path=[]):
            nonlocal recursive_score, total_checks
            total_checks += 1

            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in path:  # Recursive reference detected
                        recursive_score += 1
                    check_recursion(value, path + [key])
            elif isinstance(obj, list):
                for item in obj:
                    check_recursion(item, path)

        check_recursion(data)

        return recursive_score / total_checks if total_checks > 0 else 0.0

    def _evaluate_scale_invariance(self, data: Dict) -> float:
        """Evaluate scale invariance properties"""
        # Check if patterns remain consistent at different scales
        # This is a simplified heuristic
        if not isinstance(data, dict):
            return 0.0
        # Count nesting levels and their consistency
        level_counts: Dict[int, int] = {}
        self._count_nesting_levels(data, level_counts, 0)

        if not level_counts:
            return 0.0

        # Check if distribution follows power law (fractal characteristic)
        levels = sorted(level_counts.keys())
        if len(levels) < 2:
            return 0.5

        # Simple power law check
        consistency_score = 0
        for i in range(len(levels) - 1):
            ratio = (
                level_counts[levels[i]] / level_counts[levels[i + 1]]
                if level_counts[levels[i + 1]] > 0
                else 1
            )
            if 1.5 <= ratio <= 3.0:  # Reasonable power law range
                consistency_score += 1

        return consistency_score / (len(levels) - 1) if len(levels) > 1 else 0.5

    def _calculate_fractal_dimension(self, data: Dict) -> float:
        """Calculate approximate fractal dimension of data structure"""
        # Simplified fractal dimension calculation
        if not isinstance(data, dict):
            return 0.0
        # Count elements at each scale (nesting level)
        scale_counts: Dict[int, int] = {}
        self._count_elements_by_scale(data, scale_counts, 1)

        if len(scale_counts) < 2:
            return 0.5

        # Calculate dimension using box-counting method approximation
        scales = sorted(scale_counts.keys())
        if len(scales) < 2:
            return 0.5

        # Use first and last scale for simplification
        first_scale = scales[0]
        last_scale = scales[-1]

        if scale_counts[last_scale] == 0 or first_scale == last_scale:
            return 0.5

        dimension = math.log(
            scale_counts[first_scale] / scale_counts[last_scale]
        ) / math.log(last_scale / first_scale)

        # Normalize to 0-1 range
        return min(abs(dimension) / 3, 1.0)

    # Utility methods

    def _extract_numbers_from_data(self, data: Any) -> List[float]:
        """Extract all numerical values from data structure"""
        numbers = []

        def extract_recursive(obj):
            if isinstance(obj, (int, float)):
                numbers.append(float(obj))
            elif isinstance(obj, dict):
                for value in obj.values():
                    extract_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_recursive(item)
            elif isinstance(obj, str):
                # Try to extract numbers from strings
                import re

                found_numbers = re.findall(r"-?\d+\.?\d*", obj)
                for num_str in found_numbers:
                    try:
                        numbers.append(float(num_str))
                    except ValueError:
                        pass

        extract_recursive(data)
        return numbers

    def _calculate_max_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth of data structure"""
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(
                self._calculate_max_depth(value, current_depth + 1)
                for value in obj.values()
            )
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(
                self._calculate_max_depth(item, current_depth + 1) for item in obj
            )
        else:
            return current_depth

    def _calculate_structure_balance(self, data: Dict) -> float:
        """Calculate structural balance of data"""
        if not data:
            return 0.0
        # Check balance between different value types
        type_counts: Dict[str, int] = {}
        for value in data.values():
            value_type = type(value).__name__
            type_counts[value_type] = type_counts.get(value_type, 0) + 1

        if not type_counts:
            return 0.0

        # Calculate entropy-like measure of balance
        total = sum(type_counts.values())
        entropy = -sum(
            (count / total) * math.log2(count / total) for count in type_counts.values()
        )
        max_entropy = math.log2(len(type_counts))

        return entropy / max_entropy if max_entropy > 0 else 1.0

    def _analyze_structure_patterns(self, obj: Any, patterns: Dict, level: int):
        """Analyze structural patterns at different levels"""
        if isinstance(obj, dict):
            pattern_key = f"dict_level_{level}_keys_{len(obj)}"
            patterns[pattern_key] = patterns.get(pattern_key, 0) + 1

            for value in obj.values():
                self._analyze_structure_patterns(value, patterns, level + 1)
        elif isinstance(obj, list):
            pattern_key = f"list_level_{level}_items_{len(obj)}"
            patterns[pattern_key] = patterns.get(pattern_key, 0) + 1

            for item in obj:
                self._analyze_structure_patterns(item, patterns, level + 1)

    def _count_nesting_levels(self, obj: Any, level_counts: Dict, level: int):
        """Count elements at each nesting level"""
        level_counts[level] = level_counts.get(level, 0) + 1

        if isinstance(obj, dict):
            for value in obj.values():
                self._count_nesting_levels(value, level_counts, level + 1)
        elif isinstance(obj, list):
            for item in obj:
                self._count_nesting_levels(item, level_counts, level + 1)

    def _count_elements_by_scale(self, obj: Any, scale_counts: Dict, scale: int):
        """Count elements at different scales for fractal dimension calculation"""
        scale_counts[scale] = scale_counts.get(scale, 0) + 1

        if isinstance(obj, dict) and obj:
            for value in obj.values():
                self._count_elements_by_scale(value, scale_counts, scale * 2)
        elif isinstance(obj, list) and obj:
            for item in obj:
                self._count_elements_by_scale(item, scale_counts, scale * 2)
