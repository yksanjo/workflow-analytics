#!/usr/bin/env python3
"""Demo for Workflow Analytics."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import WorkflowAnalytics

def main():
    print("Workflow Analytics Demo")
    wa = WorkflowAnalytics()
    wa.track_workflow("wf1", {"duration": 10, "tasks_completed": 5, "agents_used": ["a1", "a2"]})
    wa.track_workflow("wf2", {"duration": 15, "tasks_completed": 8, "agents_used": ["a1", "a3"]})
    m = wa.get_metrics()
    print(f"Total: {m['total_workflows']}, Tasks: {m['total_tasks']}")
    print("Done!")

if __name__ == "__main__": main()
