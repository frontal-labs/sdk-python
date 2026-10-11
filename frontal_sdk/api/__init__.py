"""API resources for the Frontal Python SDK.

This package re-exports the typed API resources from the ``resources``
sub-package for backward compatibility, while providing a clean
``api.*`` namespace for new code.

Typical usage::

    from frontal_sdk import Frontal
    from frontal_sdk.api import agents, ai, workflows

    with Frontal() as client:
        agent = client.agents.define("MyAgent")
        result = client.ai.generate_text(...)
        runs = client.workflows.use("wf_123").executions()
"""
from frontal_sdk.resources import (  # noqa: F401
    Agents,
    AgentAccessor,
    AgentBuilder,
    AI,
    AsyncAI,
    Audit,
    Auth,
    Billing,
    Blob,
    Connectors,
    Data,
    FunctionAccessor,
    FunctionBuilder,
    Functions,
    Governance,
    Lineage,
    Observability,
    Ontology,
    Pipelines,
    Schedules,
    Webhooks,
    WorkflowAccessor,
    WorkflowApprovals,
    WorkflowBuilder,
    WorkflowSteps,
    WorkflowTemplates,
    Workflows,
    SyncAI,
    tool,
)

# Add lowercase convenience aliases for API imports
agents = Agents
ai = AI
audit = Audit
auth = Auth
billing = Billing
blob = Blob
connectors = Connectors
data = Data
functions = Functions
governance = Governance
lineage = Lineage
observability = Observability
ontology = Ontology
pipelines = Pipelines
schedules = Schedules
webhooks = Webhooks
workflow_accessor = WorkflowAccessor
workflow_approvals = WorkflowApprovals
workflow_builder = WorkflowBuilder
workflow_steps = WorkflowSteps
workflow_templates = WorkflowTemplates
workflows = Workflows
syncai = SyncAI