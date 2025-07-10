#!/bin/sh

# 🌀 Sacred Geometry AAR Processor Entrypoint
# Ensures proper initialization following Sacred Geometry principles

set -e

# Sacred Geometry initialization banner
echo "🌀 Sacred Geometry AAR Processor Container Starting..."
echo "📅 Date: $(date)"
echo "🔄 Circle Pattern: Complete initialization cycle"
echo "🔺 Triangle Pattern: Stable database connections"
echo "🌀 Spiral Pattern: Progressive enhancement enabled"

# Change to source directory
cd /app/src

# Start the AAR processor
echo "🚀 Starting Sacred Geometry AAR Processor..."
exec python aar_processor.py

# Start the AAR processor
echo "🚀 Starting Sacred Geometry AAR Processor..."
echo "📊 Monitoring integration: ${MONITORING_INTEGRATION_ENABLED:-enabled}"
echo "🎯 Sacred Geometry compliance target: ${SACRED_GEOMETRY_COMPLIANCE_TARGET:-95}%"

exec "$@"
