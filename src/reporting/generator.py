"""Report generation module"""

import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


class ReportGenerator:
    """Generate comprehensive test reports"""
    
    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_style("whitegrid")
    
    def generate_html_report(
        self,
        test_results: List[Dict[str, Any]],
        report_title: str = "AI Model Test Report"
    ) -> str:
        """Generate HTML report"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report_title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .summary {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .test-result {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }}
                .passed {{ border-left-color: #27ae60; }}
                .failed {{ border-left-color: #e74c3c; }}
                .error {{ border-left-color: #f39c12; }}
                .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
                .metric-label {{ font-weight: bold; color: #7f8c8d; }}
                .metric-value {{ font-size: 24px; color: #2c3e50; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #34495e; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{report_title}</h1>
                <p>Generated: {timestamp}</p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                {self._generate_summary_html(test_results)}
            </div>
            
            <div class="test-results">
                <h2>Test Results</h2>
                {self._generate_test_results_html(test_results)}
            </div>
        </body>
        </html>
        """
        
        report_path = self.output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        report_path.write_text(html)
        
        return str(report_path)
    
    def _generate_summary_html(self, test_results: List[Dict[str, Any]]) -> str:
        """Generate summary section"""
        total = len(test_results)
        passed = sum(1 for r in test_results if r.get("status") == "passed")
        failed = sum(1 for r in test_results if r.get("status") == "failed")
        errors = sum(1 for r in test_results if r.get("status") == "error")
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        return f"""
        <div class="metric">
            <div class="metric-label">Total Tests</div>
            <div class="metric-value">{total}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Passed</div>
            <div class="metric-value" style="color: #27ae60;">{passed}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Failed</div>
            <div class="metric-value" style="color: #e74c3c;">{failed}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Errors</div>
            <div class="metric-value" style="color: #f39c12;">{errors}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Pass Rate</div>
            <div class="metric-value">{pass_rate:.1f}%</div>
        </div>
        """
    
    def _generate_test_results_html(self, test_results: List[Dict[str, Any]]) -> str:
        """Generate test results section"""
        html = ""
        
        for result in test_results:
            status = result.get("status", "unknown")
            test_name = result.get("test_name", "Unknown Test")
            message = result.get("message", "")
            score = result.get("score")
            
            score_html = f"<p><strong>Score:</strong> {score:.3f}</p>" if score is not None else ""
            
            html += f"""
            <div class="test-result {status}">
                <h3>{test_name}</h3>
                <p><strong>Status:</strong> {status.upper()}</p>
                {score_html}
                <p><strong>Message:</strong> {message}</p>
            </div>
            """
        
        return html
    
    def generate_performance_chart(
        self,
        metrics: Dict[str, Any],
        chart_title: str = "Performance Metrics"
    ) -> str:
        """Generate performance visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(chart_title, fontsize=16)
        
        # Latency distribution
        if "latencies" in metrics.get("metadata", {}):
            latencies = metrics["metadata"]["latencies"]
            axes[0, 0].hist(latencies, bins=30, color='skyblue', edgecolor='black')
            axes[0, 0].set_title('Latency Distribution')
            axes[0, 0].set_xlabel('Latency (ms)')
            axes[0, 0].set_ylabel('Frequency')
        
        # Summary metrics
        summary_metrics = {
            'Avg': metrics.get('avg_latency_ms', 0),
            'P50': metrics.get('p50_latency_ms', 0),
            'P95': metrics.get('p95_latency_ms', 0),
            'P99': metrics.get('p99_latency_ms', 0)
        }
        axes[0, 1].bar(summary_metrics.keys(), summary_metrics.values(), color='lightcoral')
        axes[0, 1].set_title('Latency Percentiles')
        axes[0, 1].set_ylabel('Latency (ms)')
        
        # Success rate
        total = metrics.get('total_requests', 0)
        successful = metrics.get('successful_requests', 0)
        failed = total - successful
        axes[1, 0].pie([successful, failed], labels=['Success', 'Failed'], 
                      autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
        axes[1, 0].set_title('Success Rate')
        
        # Resource usage
        resources = {
            'CPU %': metrics.get('cpu_usage_percent', 0),
            'Memory MB': metrics.get('memory_usage_mb', 0) / 10  # Scale for visibility
        }
        axes[1, 1].bar(resources.keys(), resources.values(), color='lightskyblue')
        axes[1, 1].set_title('Resource Usage')
        
        plt.tight_layout()
        
        chart_path = self.output_dir / f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(chart_path)
    
    def export_json(self, data: Dict[str, Any], filename: str = "test_results.json") -> str:
        """Export results to JSON"""
        json_path = self.output_dir / filename
        
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(json_path)
