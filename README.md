# Workflow Analytics

Analytics and metrics for multi-agent workflows.

## Features

- **Performance Metrics** - Track workflow performance
- **Agent Statistics** - Monitor agent utilization
- **Trend Analysis** - Analyze workflow trends
- **Reporting** - Generate analytics reports

## Quick Start

```python
from workflow_analytics import WorkflowAnalytics

wa = WorkflowAnalytics()
wa.track_workflow("wf-1", {"duration": 10, "tasks": 5})
metrics = wa.get_metrics()
```

## License

MIT
