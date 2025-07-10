#!/usr/bin/env python3
"""
🗄️ Database Manager
Database management for AAR storage and retrieval

This module handles persistent storage of AAR data, results, and metadata
using SQLite with optional PostgreSQL support.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)


class DatabaseManager:
    """Database manager for AAR data persistence"""

    def __init__(self, db_path: str = "/app/data/aar_database.db"):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    async def initialize(self):
        """Initialize database connection and create tables"""
        logger.info("🗄️ Initializing database", db_path=self.db_path)

        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # Connect to database
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Enable column access by name

        # Create tables
        await self._create_tables()

        logger.info("✅ Database initialized successfully")

    async def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
        logger.info("🗄️ Database connection closed")

    async def is_healthy(self) -> bool:
        """Check database health"""
        try:
            if not self.connection:
                return False

            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            return cursor.fetchone() is not None
        except Exception as e:
            logger.error("Database health check failed", error=str(e))
            return False

    async def store_aar(self, aar_result) -> bool:
        """Store AAR result in database"""
        try:
            if not self.connection:
                logger.error("Database connection not available")
                return False

            cursor = self.connection.cursor()

            # Store main AAR record
            cursor.execute(
                """
                INSERT INTO aars (
                    aar_id, mission_id, compliance_score,
                    report_content, metadata, generated_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    aar_result.aar_id,
                    aar_result.mission_id,
                    aar_result.compliance_score,
                    json.dumps(aar_result.report_content),
                    json.dumps(aar_result.metadata),
                    aar_result.generated_at.isoformat(),
                    "completed",
                ),
            )

            self.connection.commit()

            logger.info("✅ AAR stored successfully", aar_id=aar_result.aar_id)
            return True

        except Exception as e:
            logger.error("Failed to store AAR", error=str(e))
            if self.connection:
                self.connection.rollback()
            return False

    async def get_aar_status(self, aar_id: str) -> Optional[Dict[str, Any]]:
        """Get AAR status by ID"""
        try:
            if not self.connection:
                return None

            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT aar_id, mission_id, status, compliance_score,
                       generated_at, created_at
                FROM aars
                WHERE aar_id = ?
            """,
                (aar_id,),
            )

            row = cursor.fetchone()
            if row:
                return {
                    "aar_id": row["aar_id"],
                    "mission_id": row["mission_id"],
                    "status": row["status"],
                    "compliance_score": row["compliance_score"],
                    "generated_at": row["generated_at"],
                    "created_at": row["created_at"],
                }
            return None

        except Exception as e:
            logger.error("Failed to get AAR status", aar_id=aar_id, error=str(e))
            return None

    async def get_aar_report(self, aar_id: str) -> Optional[Dict[str, Any]]:
        """Get full AAR report by ID"""
        try:
            if not self.connection:
                return None

            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT aar_id, mission_id, compliance_score,
                       report_content, metadata, generated_at, status
                FROM aars
                WHERE aar_id = ?
            """,
                (aar_id,),
            )

            row = cursor.fetchone()
            if row:
                return {
                    "aar_id": row["aar_id"],
                    "mission_id": row["mission_id"],
                    "compliance_score": row["compliance_score"],
                    "report_content": json.loads(row["report_content"]),
                    "metadata": json.loads(row["metadata"]),
                    "generated_at": row["generated_at"],
                    "status": row["status"],
                }
            return None

        except Exception as e:
            logger.error("Failed to get AAR report", aar_id=aar_id, error=str(e))
            return None

    async def list_aars(
        self, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List AAR records with pagination"""
        try:
            if not self.connection:
                return []

            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT aar_id, mission_id, status, compliance_score,
                       generated_at, created_at
                FROM aars
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """,
                (limit, offset),
            )

            rows = cursor.fetchall()
            return [
                {
                    "aar_id": row["aar_id"],
                    "mission_id": row["mission_id"],
                    "status": row["status"],
                    "compliance_score": row["compliance_score"],
                    "generated_at": row["generated_at"],
                    "created_at": row["created_at"],
                }
                for row in rows
            ]

        except Exception as e:
            logger.error("Failed to list AARs", error=str(e))
            return []

    async def get_compliance_stats(self) -> Dict[str, Any]:
        """Get Sacred Geometry compliance statistics"""
        try:
            if not self.connection:
                return {}

            cursor = self.connection.cursor()

            # Get basic stats
            cursor.execute(
                """
                SELECT
                    COUNT(*) as total_aars,
                    AVG(compliance_score) as avg_compliance,
                    MIN(compliance_score) as min_compliance,
                    MAX(compliance_score) as max_compliance
                FROM aars
                WHERE status = 'completed'
            """
            )

            stats_row = cursor.fetchone()

            # Get compliance distribution
            cursor.execute(
                """
                SELECT
                    CASE
                        WHEN compliance_score >= 90 THEN 'excellent'
                        WHEN compliance_score >= 80 THEN 'good'
                        WHEN compliance_score >= 70 THEN 'acceptable'
                        ELSE 'needs_improvement'
                    END as compliance_level,
                    COUNT(*) as count
                FROM aars
                WHERE status = 'completed'
                GROUP BY compliance_level
            """
            )

            distribution_rows = cursor.fetchall()

            return {
                "total_aars": stats_row["total_aars"] if stats_row else 0,
                "average_compliance": stats_row["avg_compliance"] if stats_row else 0,
                "min_compliance": stats_row["min_compliance"] if stats_row else 0,
                "max_compliance": stats_row["max_compliance"] if stats_row else 0,
                "compliance_distribution": {
                    row["compliance_level"]: row["count"] for row in distribution_rows
                },
            }

        except Exception as e:
            logger.error("Failed to get compliance stats", error=str(e))
            return {}

    async def _create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()

        # Create AARs table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS aars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aar_id TEXT UNIQUE NOT NULL,
                mission_id TEXT NOT NULL,
                compliance_score REAL NOT NULL,
                report_content TEXT NOT NULL,
                metadata TEXT NOT NULL,
                generated_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_aar_id ON aars(aar_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mission_id ON aars(mission_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON aars(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON aars(created_at)")

        # Create Sacred Geometry patterns table for detailed analysis
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sg_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aar_id TEXT NOT NULL,
                pattern_name TEXT NOT NULL,
                pattern_score REAL NOT NULL,
                pattern_details TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (aar_id) REFERENCES aars(aar_id)
            )
        """
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_sg_aar_id ON sg_patterns(aar_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_sg_pattern ON sg_patterns(pattern_name)"
        )

        self.connection.commit()
        logger.debug("Database tables created successfully")

    async def store_sg_pattern_details(
        self, aar_id: str, pattern_results: Dict[str, Any]
    ):
        """Store detailed Sacred Geometry pattern analysis"""
        try:
            if not self.connection:
                return False

            cursor = self.connection.cursor()

            for pattern_name, pattern_data in pattern_results.items():
                cursor.execute(
                    """
                    INSERT INTO sg_patterns (
                        aar_id, pattern_name, pattern_score, pattern_details
                    ) VALUES (?, ?, ?, ?)
                """,
                    (
                        aar_id,
                        pattern_name,
                        pattern_data.get("score", 0.0),
                        json.dumps(pattern_data),
                    ),
                )

            self.connection.commit()
            return True

        except Exception as e:
            logger.error("Failed to store SG pattern details", error=str(e))
            if self.connection:
                self.connection.rollback()
            return False

    async def get_pattern_trends(
        self, pattern_name: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get trends for a specific Sacred Geometry pattern"""
        try:
            if not self.connection:
                return []

            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT
                    sp.aar_id,
                    a.mission_id,
                    sp.pattern_score,
                    sp.created_at
                FROM sg_patterns sp
                JOIN aars a ON sp.aar_id = a.aar_id
                WHERE sp.pattern_name = ?
                ORDER BY sp.created_at DESC
                LIMIT ?
            """,
                (pattern_name, limit),
            )

            rows = cursor.fetchall()
            return [
                {
                    "aar_id": row["aar_id"],
                    "mission_id": row["mission_id"],
                    "pattern_score": row["pattern_score"],
                    "created_at": row["created_at"],
                }
                for row in rows
            ]

        except Exception as e:
            logger.error("Failed to get pattern trends", error=str(e))
            return []
