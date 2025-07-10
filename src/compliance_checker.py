#!/usr/bin/env python3
"""
✅ Compliance Checker
Sacred Geometry compliance monitoring and validation

This module provides real-time compliance checking and monitoring
for Sacred Geometry pattern adherence.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from src.sacred_geometry_engine import SacredGeometryEngine

logger = structlog.get_logger(__name__)


class ComplianceChecker:
    """Sacred Geometry compliance checker and monitor"""

    def __init__(self, sacred_geometry_engine: SacredGeometryEngine):
        self.sacred_geometry = sacred_geometry_engine
        self.compliance_thresholds = {
            "excellent": 0.9,
            "good": 0.8,
            "acceptable": 0.7,
            "needs_improvement": 0.5,
            "critical": 0.3,
        }
        self.current_compliance = 0.0
        self.last_check: Optional[datetime] = None

    async def get_current_compliance(self) -> float:
        """Get current overall compliance level"""
        return self.current_compliance

    async def update_compliance(self, compliance_score: float):
        """Update current compliance score"""
        self.current_compliance = compliance_score
        self.last_check = datetime.now()

        logger.info(
            "📊 Compliance updated",
            score=compliance_score,
            level=self._get_compliance_level(compliance_score),
        )

    async def get_detailed_compliance(self) -> Dict[str, Any]:
        """Get detailed compliance information"""
        compliance_level = self._get_compliance_level(self.current_compliance)

        return {
            "current_score": self.current_compliance,
            "compliance_level": compliance_level,
            "last_updated": self.last_check.isoformat() if self.last_check else None,
            "thresholds": self.compliance_thresholds,
            "recommendations": self._get_compliance_recommendations(compliance_level),
            "pattern_status": await self._get_pattern_compliance_status(),
        }

    async def check_compliance_alerts(self) -> List[Dict[str, Any]]:
        """Check for compliance alerts and warnings"""
        alerts = []

        # Critical compliance alert
        if self.current_compliance < self.compliance_thresholds["critical"]:
            alerts.append(
                {
                    "level": "critical",
                    "message": f"Critical compliance level: {self.current_compliance:.1%}",
                    "action_required": "Immediate intervention required",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Low compliance warning
        elif self.current_compliance < self.compliance_thresholds["acceptable"]:
            alerts.append(
                {
                    "level": "warning",
                    "message": f"Low compliance level: {self.current_compliance:.1%}",
                    "action_required": "Review and improvement needed",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Stale data alert
        if (
            self.last_check and (datetime.now() - self.last_check).seconds > 3600
        ):  # 1 hour
            alerts.append(
                {
                    "level": "info",
                    "message": "Compliance data is stale",
                    "action_required": "Update compliance monitoring",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    async def validate_mission_compliance(
        self, mission_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate compliance for a specific mission"""
        try:
            validation_result = await self.sacred_geometry.validate_data(mission_data)
            compliance_score = validation_result["overall_compliance"]

            # Update current compliance if this is a significant mission
            if mission_data.get("priority", "normal") == "high":
                await self.update_compliance(compliance_score)

            return {
                "mission_compliance": compliance_score,
                "compliance_level": self._get_compliance_level(compliance_score),
                "pattern_results": validation_result["pattern_results"],
                "validation_timestamp": datetime.now().isoformat(),
                "recommendations": self._generate_mission_recommendations(
                    validation_result
                ),
            }

        except Exception as e:
            logger.error("Mission compliance validation failed", error=str(e))
            return {
                "mission_compliance": 0.0,
                "compliance_level": "error",
                "error": str(e),
                "validation_timestamp": datetime.now().isoformat(),
            }

    def _get_compliance_level(self, score: float) -> str:
        """Get compliance level based on score"""
        for level, threshold in self.compliance_thresholds.items():
            if score >= threshold:
                return level
        return "critical"

    def _get_compliance_recommendations(self, level: str) -> List[str]:
        """Get recommendations based on compliance level"""
        recommendations = {
            "excellent": [
                "Maintain current Sacred Geometry practices",
                "Share best practices with other teams",
                "Consider advanced pattern optimizations",
            ],
            "good": [
                "Continue current practices with minor refinements",
                "Focus on improving weaker patterns",
                "Regular compliance monitoring",
            ],
            "acceptable": [
                "Review and strengthen Sacred Geometry implementation",
                "Increase focus on pattern compliance",
                "Consider additional training or resources",
            ],
            "needs_improvement": [
                "Immediate review of Sacred Geometry practices required",
                "Implement structured improvement plan",
                "Increase monitoring frequency",
                "Consider expert consultation",
            ],
            "critical": [
                "Emergency intervention required",
                "Halt non-critical activities until compliance improved",
                "Implement immediate corrective measures",
                "Engage Sacred Geometry specialists",
            ],
        }

        return recommendations.get(level, ["Contact system administrator"])

    async def _get_pattern_compliance_status(self) -> Dict[str, str]:
        """Get compliance status for each Sacred Geometry pattern"""
        # This would integrate with the Sacred Geometry engine to get detailed pattern status
        # For now, returning placeholder data
        return {
            "circle": "good",
            "triangle": "excellent",
            "spiral": "acceptable",
            "golden_ratio": "good",
            "fractal": "needs_improvement",
        }

    def _generate_mission_recommendations(
        self, validation_result: Dict[str, Any]
    ) -> List[str]:
        """Generate specific recommendations for mission compliance"""
        recommendations = []

        for pattern_name, pattern_result in validation_result[
            "pattern_results"
        ].items():
            score = pattern_result.get("score", 0)
            if score < 0.7:
                recommendations.append(
                    f"Improve {pattern_name} pattern compliance (current: {score:.1%})"
                )

        if validation_result["overall_compliance"] < 0.8:
            recommendations.append(
                "Consider comprehensive Sacred Geometry review and optimization"
            )

        return recommendations

    async def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        compliance_data = await self.get_detailed_compliance()
        alerts = await self.check_compliance_alerts()

        return {
            "report_type": "sacred_geometry_compliance_report",
            "generated_at": datetime.now().isoformat(),
            "compliance_summary": {
                "current_score": compliance_data["current_score"],
                "compliance_level": compliance_data["compliance_level"],
                "last_updated": compliance_data["last_updated"],
            },
            "pattern_analysis": compliance_data["pattern_status"],
            "alerts_and_warnings": alerts,
            "recommendations": compliance_data["recommendations"],
            "thresholds": compliance_data["thresholds"],
            "next_review_recommended": self._calculate_next_review_date(),
        }

    def _calculate_next_review_date(self) -> str:
        """Calculate recommended next review date based on compliance level"""
        from datetime import timedelta

        if self.current_compliance >= self.compliance_thresholds["excellent"]:
            next_review = datetime.now() + timedelta(weeks=4)
        elif self.current_compliance >= self.compliance_thresholds["good"]:
            next_review = datetime.now() + timedelta(weeks=2)
        elif self.current_compliance >= self.compliance_thresholds["acceptable"]:
            next_review = datetime.now() + timedelta(weeks=1)
        else:
            next_review = datetime.now() + timedelta(days=1)

        return next_review.isoformat()
