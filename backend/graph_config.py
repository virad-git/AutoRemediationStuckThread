"""
LangChain Graph/Workflow Configuration
Defines task graph for stuck thread analysis
"""

try:
    from langchain.graphs import Graph
except ImportError:
    Graph = None

# Graph definition for thread remediation workflow
REMEDIATION_GRAPH = {
    "nodes": [
        {
            "id": "analyze",
            "label": "Analyze Stuck Thread",
            "description": "Analyze thread dump and identify stuck threads"
        },
        {
            "id": "escalate",
            "label": "Escalate Severity",
            "description": "Determine escalation level based on analysis"
        },
        {
            "id": "plan",
            "label": "Create Remediation Plan",
            "description": "Generate step-by-step remediation plan"
        },
        {
            "id": "execute",
            "label": "Execute Restart",
            "description": "Execute WebLogic server restart"
        },
        {
            "id": "verify",
            "label": "Verify Recovery",
            "description": "Verify thread pool health post-restart"
        }
    ],
    "edges": [
        ("analyze", "escalate"),
        ("escalate", "plan"),
        ("plan", "execute"),
        ("execute", "verify")
    ]
}

# Escalation levels and corresponding actions
ESCALATION_LEVELS = {
    1: {
        "name": "Low",
        "description": "Monitor and document",
        "auto_action": False,
        "requires_approval": False
    },
    2: {
        "name": "Medium",
        "description": "Coordinate with team",
        "auto_action": False,
        "requires_approval": True
    },
    3: {
        "name": "High",
        "description": "Immediate action required",
        "auto_action": True,
        "requires_approval": True
    },
    4: {
        "name": "Critical",
        "description": "Urgent escalation",
        "auto_action": True,
        "requires_approval": True
    },
    5: {
        "name": "Emergency",
        "description": "Maximum escalation",
        "auto_action": True,
        "requires_approval": True
    }
}

def get_graph_structure():
    """Get the remediation workflow graph structure"""
    return REMEDIATION_GRAPH

def get_escalation_config(level: int) -> dict:
    """Get escalation configuration for given level"""
    return ESCALATION_LEVELS.get(level, ESCALATION_LEVELS[1])
