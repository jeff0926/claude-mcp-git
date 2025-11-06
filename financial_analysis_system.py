#!/usr/bin/env python3
"""
Quarterly Financial Analysis Multi-Agent System
KISS Architecture with MCP as Code Pattern

This system implements a DAG-based multi-agent workflow for financial analysis.
All heavy data processing happens in code; only small summaries are passed between agents.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass


# ============================================================================
# SIMULATED MCP ENVIRONMENT (MCP as Code)
# ============================================================================

@dataclass
class Transaction:
    """Represents a single financial transaction."""
    transaction_id: str
    date: datetime
    amount: float
    category: str


class FinanceDatabaseMCP:
    """
    Simulates an MCP endpoint for financial data.
    In production, this would connect to a real database via MCP protocol.
    """

    @staticmethod
    def get_transactions(start_date: datetime, end_date: datetime, limit: int = 100000) -> List[Transaction]:
        """
        Simulates retrieving large transaction dataset.
        This represents the MCP code execution environment processing.

        Returns simulated transaction data - in production this would query a real DB.
        """
        print(f"[MCP] Simulating retrieval of {limit} transactions...")

        transactions = []
        current_date = start_date

        for i in range(limit):
            # Generate realistic transaction data
            days_offset = random.randint(0, (end_date - start_date).days)
            trans_date = start_date + timedelta(days=days_offset)

            # Simulate varying revenue amounts
            base_amount = random.uniform(100, 5000)

            transactions.append(Transaction(
                transaction_id=f"TXN-{i:06d}",
                date=trans_date,
                amount=base_amount,
                category=random.choice(["sales", "subscription", "service"])
            ))

        print(f"[MCP] Retrieved {len(transactions)} transactions from database")
        return transactions


# ============================================================================
# DATA AGENT - Executes Heavy Processing in Code Environment
# ============================================================================

class DataAgent:
    """
    Data Agent: Retrieves and processes large datasets using MCP as Code pattern.

    CRITICAL: All data filtering and aggregation happens HERE in code.
    Only small aggregated results are returned to the orchestrator.
    """

    def __init__(self):
        self.name = "DataAgent"
        self.mcp = FinanceDatabaseMCP()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute data retrieval and aggregation.

        Process:
        1. Retrieve 100,000 transactions via MCP
        2. Filter for Q3 (July-September)
        3. Aggregate to calculate totals
        4. Return ONLY the aggregated metrics (not raw data)
        """
        print(f"\n{'='*70}")
        print(f"[{self.name}] Starting data retrieval and aggregation...")
        print(f"{'='*70}")

        # Define Q3 date range (July 1 - September 30, 2024)
        q3_start = datetime(2024, 7, 1)
        q3_end = datetime(2024, 9, 30)

        # MCP as Code: Retrieve large dataset
        all_transactions = self.mcp.get_transactions(
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
            limit=100000
        )

        # EXECUTE FILTERING IN CODE (prevents context overload)
        print(f"[{self.name}] Filtering {len(all_transactions)} transactions for Q3...")
        q3_transactions = [
            t for t in all_transactions
            if q3_start <= t.date <= q3_end
        ]

        print(f"[{self.name}] Found {len(q3_transactions)} Q3 transactions")

        # EXECUTE AGGREGATION IN CODE
        print(f"[{self.name}] Aggregating Q3 revenue...")
        total_q3_revenue = sum(t.amount for t in q3_transactions)

        # Calculate monthly breakdown for trend analysis
        monthly_revenues = self._calculate_monthly_revenues(q3_transactions)
        avg_monthly_revenue = sum(monthly_revenues.values()) / len(monthly_revenues)

        # Output ONLY the small aggregated metrics (not 100k rows!)
        result = {
            "total_q3_revenue": round(total_q3_revenue, 2),
            "average_monthly_revenue": round(avg_monthly_revenue, 2),
            "monthly_breakdown": {
                k: round(v, 2) for k, v in monthly_revenues.items()
            },
            "transaction_count": len(q3_transactions)
        }

        print(f"[{self.name}] ✓ Aggregation complete")
        print(f"[{self.name}] Total Q3 Revenue: ${result['total_q3_revenue']:,.2f}")
        print(f"[{self.name}] Avg Monthly Revenue: ${result['average_monthly_revenue']:,.2f}")
        print(f"[{self.name}] Transaction Count: {result['transaction_count']:,}")

        return result

    def _calculate_monthly_revenues(self, transactions: List[Transaction]) -> Dict[str, float]:
        """Helper to calculate revenue by month."""
        monthly = {"July": 0.0, "August": 0.0, "September": 0.0}

        for t in transactions:
            if t.date.month == 7:
                monthly["July"] += t.amount
            elif t.date.month == 8:
                monthly["August"] += t.amount
            elif t.date.month == 9:
                monthly["September"] += t.amount

        return monthly


# ============================================================================
# ANALYSIS AGENT - Performs Reasoning on Aggregated Data
# ============================================================================

class AnalysisAgent:
    """
    Analysis Agent: Performs forecasting and trend analysis.

    Receives ONLY aggregated metrics from Data Agent (not raw data).
    Generates insights and forecasts for next quarter.
    """

    def __init__(self):
        self.name = "AnalysisAgent"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute analysis on aggregated data.

        Input: Small aggregated metrics from DataAgent
        Output: Key findings, forecast, and risk factors
        """
        print(f"\n{'='*70}")
        print(f"[{self.name}] Starting financial analysis...")
        print(f"{'='*70}")

        # Extract aggregated inputs (small data only!)
        total_revenue = context["total_q3_revenue"]
        avg_monthly = context["average_monthly_revenue"]
        monthly_breakdown = context["monthly_breakdown"]

        print(f"[{self.name}] Analyzing Q3 metrics...")

        # Perform trend analysis
        july_rev = monthly_breakdown["July"]
        august_rev = monthly_breakdown["August"]
        september_rev = monthly_breakdown["September"]

        # Calculate month-over-month growth
        july_to_august_growth = ((august_rev - july_rev) / july_rev) * 100
        august_to_september_growth = ((september_rev - august_rev) / august_rev) * 100
        avg_growth_rate = (july_to_august_growth + august_to_september_growth) / 2

        # Simple linear forecast for Q4
        q4_forecast = avg_monthly * 3 * (1 + avg_growth_rate / 100)

        # Generate key findings
        findings = []

        # Growth analysis
        if avg_growth_rate > 5:
            findings.append(f"Strong growth momentum with {avg_growth_rate:.1f}% average monthly growth")
        elif avg_growth_rate > 0:
            findings.append(f"Moderate growth observed at {avg_growth_rate:.1f}% monthly average")
        else:
            findings.append(f"Declining trend detected with {avg_growth_rate:.1f}% monthly change")

        # Revenue stability
        revenue_variance = max(monthly_breakdown.values()) - min(monthly_breakdown.values())
        variance_pct = (revenue_variance / avg_monthly) * 100

        if variance_pct > 15:
            findings.append(f"High revenue volatility detected ({variance_pct:.1f}% variance)")
        else:
            findings.append(f"Stable revenue pattern with {variance_pct:.1f}% variance")

        # Performance assessment
        if september_rev > august_rev > july_rev:
            findings.append("Consistent month-over-month improvement throughout Q3")
        elif september_rev < august_rev:
            findings.append("September revenue declined compared to August - investigate causes")

        # Risk factors
        risk_factors = []
        if avg_growth_rate < 0:
            risk_factors.append("Negative growth trend may impact Q4 targets")
        if variance_pct > 20:
            risk_factors.append("High volatility indicates unstable revenue streams")
        if september_rev < avg_monthly * 0.9:
            risk_factors.append("September underperformance requires attention")

        result = {
            "total_q3_revenue": total_revenue,
            "average_monthly_revenue": avg_monthly,
            "growth_rate": round(avg_growth_rate, 2),
            "q4_forecast": round(q4_forecast, 2),
            "key_findings": findings,
            "risk_factors": risk_factors if risk_factors else ["No significant risks identified"],
            "monthly_breakdown": monthly_breakdown
        }

        print(f"[{self.name}] ✓ Analysis complete")
        print(f"[{self.name}] Growth Rate: {avg_growth_rate:.2f}%")
        print(f"[{self.name}] Q4 Forecast: ${q4_forecast:,.2f}")
        print(f"[{self.name}] Key Findings: {len(findings)} insights generated")

        return result


# ============================================================================
# REPORT AGENT - Generates Executive Summary
# ============================================================================

class ReportAgent:
    """
    Report Agent: Creates professional narrative report.

    Receives insights from Analysis Agent and generates
    a polished 3-paragraph executive summary.
    """

    def __init__(self):
        self.name = "ReportAgent"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate final executive summary report.

        Input: Analysis findings and forecast
        Output: Professional 3-paragraph narrative
        """
        print(f"\n{'='*70}")
        print(f"[{self.name}] Generating executive summary...")
        print(f"{'='*70}")

        # Extract analysis results
        total_revenue = context["total_q3_revenue"]
        avg_monthly = context["average_monthly_revenue"]
        growth_rate = context["growth_rate"]
        q4_forecast = context["q4_forecast"]
        findings = context["key_findings"]
        risks = context["risk_factors"]
        monthly = context["monthly_breakdown"]

        # Generate professional narrative report
        report = self._generate_narrative(
            total_revenue, avg_monthly, growth_rate,
            q4_forecast, findings, risks, monthly
        )

        result = {
            "report": report,
            "executive_summary": report,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_q3_revenue": total_revenue,
                "q4_forecast": q4_forecast,
                "growth_rate": growth_rate
            }
        }

        print(f"[{self.name}] ✓ Report generation complete")

        return result

    def _generate_narrative(self, total_revenue: float, avg_monthly: float,
                           growth_rate: float, q4_forecast: float,
                           findings: List[str], risks: List[str],
                           monthly: Dict[str, float]) -> str:
        """Generate the 3-paragraph executive summary."""

        # Paragraph 1: Q3 Performance Overview
        para1 = (
            f"Q3 2024 Financial Performance Summary\n\n"
            f"The third quarter of 2024 concluded with total revenue of ${total_revenue:,.2f}, "
            f"representing an average monthly revenue of ${avg_monthly:,.2f}. "
            f"Monthly performance showed progression from ${monthly['July']:,.2f} in July, "
            f"to ${monthly['August']:,.2f} in August, and ${monthly['September']:,.2f} in September. "
            f"This quarterly performance reflects a {growth_rate:+.1f}% average month-over-month growth rate."
        )

        # Paragraph 2: Key Findings and Analysis
        findings_text = " ".join(findings)
        para2 = (
            f"\n\nKey Analysis and Trends\n\n"
            f"{findings_text} Our analysis indicates that the current trajectory "
            f"demonstrates {'strong' if growth_rate > 3 else 'moderate' if growth_rate > 0 else 'concerning'} "
            f"business momentum. The revenue patterns observed in Q3 suggest "
            f"{'sustained operational efficiency' if growth_rate > 0 else 'need for strategic intervention'} "
            f"moving into the final quarter of the year."
        )

        # Paragraph 3: Q4 Forecast and Recommendations
        risks_text = " ".join(risks)
        para3 = (
            f"\n\nQ4 Forecast and Strategic Outlook\n\n"
            f"Based on linear projection from Q3 trends, we forecast Q4 2024 revenue of ${q4_forecast:,.2f}. "
            f"Risk assessment identifies the following considerations: {risks_text} "
            f"We recommend {'maintaining current growth initiatives and monitoring key performance indicators' if growth_rate > 0 else 'implementing corrective measures to reverse declining trends'} "
            f"to ensure achievement of annual targets. Management should focus on "
            f"{'capitalizing on momentum' if growth_rate > 3 else 'stabilizing revenue streams' if growth_rate > 0 else 'urgent turnaround strategies'} "
            f"for optimal Q4 performance."
        )

        return para1 + para2 + para3


# ============================================================================
# DAG ORCHESTRATOR - Manages Sequential Agent Workflow
# ============================================================================

class DAGOrchestrator:
    """
    Simple DAG orchestrator following KISS principle.

    Manages sequential execution: DataAgent → AnalysisAgent → ReportAgent
    Each agent's output becomes the next agent's input context.
    """

    def __init__(self):
        self.agents = {
            "data": DataAgent(),
            "analysis": AnalysisAgent(),
            "report": ReportAgent()
        }
        self.execution_order = ["data", "analysis", "report"]

    def run(self) -> Dict[str, Any]:
        """
        Execute the DAG workflow sequentially.

        Returns: Final report from ReportAgent
        """
        print("\n" + "="*70)
        print("QUARTERLY FINANCIAL ANALYSIS SYSTEM - DAG EXECUTION")
        print("="*70)
        print(f"Workflow: {' → '.join(self.execution_order)}")
        print("="*70)

        context = {}

        # Execute agents in DAG order
        for agent_name in self.execution_order:
            agent = self.agents[agent_name]

            # Execute agent and update context
            result = agent.execute(context)
            context.update(result)

        print("\n" + "="*70)
        print("DAG EXECUTION COMPLETE")
        print("="*70)

        return context


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for the financial analysis system."""

    # Initialize and run the DAG orchestrator
    orchestrator = DAGOrchestrator()
    final_result = orchestrator.run()

    # Display final report
    print("\n" + "="*70)
    print("EXECUTIVE SUMMARY REPORT")
    print("="*70)
    print()
    print(final_result["report"])
    print()
    print("="*70)
    print(f"Report generated at: {final_result['metadata']['generated_at']}")
    print("="*70)


if __name__ == "__main__":
    main()
