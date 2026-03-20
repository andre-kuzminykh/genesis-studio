"""Shared enums used across multiple models.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
import enum


class ProductStatus(str, enum.Enum):
    draft = "draft"
    discovery_in_progress = "discovery_in_progress"
    feature_map_draft = "feature_map_draft"
    feature_map_approved = "feature_map_approved"
    in_development = "in_development"
    archived = "archived"


class FeatureStatus(str, enum.Enum):
    draft = "draft"
    feature_selected = "feature_selected"
    prd_draft_created = "prd_draft_created"
    stories_approved = "stories_approved"
    ux_approved = "ux_approved"
    use_cases_approved = "use_cases_approved"
    requirements_generated = "requirements_generated"
    tests_generated = "tests_generated"
    tests_approved = "tests_approved"
    code_generated = "code_generated"
    pushed_to_github = "pushed_to_github"
    deployed_local = "deployed_local"
    deploy_failed = "deploy_failed"


class PRDVersionStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"
    superseded = "superseded"


class UserStoryStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"
    rejected = "rejected"


class UseCaseStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"


class RequirementType(str, enum.Enum):
    functional = "functional"
    non_functional = "non_functional"


class TestCaseType(str, enum.Enum):
    unit = "unit"
    integration = "integration"
    e2e = "e2e"
    acceptance = "acceptance"


class TestCaseStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskType(str, enum.Enum):
    backend = "backend"
    bot = "bot"
    shared = "shared"


class ChangeRequestStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    applied = "applied"


class UXFlowType(str, enum.Enum):
    telegram_preview = "telegram_preview"
    mermaid_user_flow = "mermaid_user_flow"
    mermaid_sequence = "mermaid_sequence"
    mermaid_state = "mermaid_state"


class ArtifactType(str, enum.Enum):
    backend = "backend"
    bot = "bot"
    shared = "shared"
    test = "test"
    config = "config"


class GitOperationType(str, enum.Enum):
    commit = "commit"
    push = "push"
    read = "read"


class GitOperationStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class DeploymentStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"


class DeploymentTarget(str, enum.Enum):
    backend = "backend"
    bot = "bot"
    both = "both"
