export interface Product {
  id: string
  name: string | null
  idea_text: string
  summary: string | null
  target_users: string | null
  goal: string | null
  status: string
  created_at: string
}

export interface DiscoveryResponse {
  product: Product
  follow_up_questions: string[]
  is_complete: boolean
}

export interface Feature {
  id: string
  product_id: string
  feature_id: string
  name: string
  overview: string | null
  sort_order: number
  status: string
}

export interface PRDVersion {
  id: string
  feature_id: string
  version_number: number
  content: Record<string, unknown>
  summary: string | null
  status: string
  is_current: boolean
}

export interface UserStory {
  id: string
  story_id: string
  role: string
  action: string
  benefit: string
  status: string
  is_approved: boolean
}

export interface UXFlow {
  id: string
  flow_type: string
  title: string
  content: string
}

export interface UseCase {
  id: string
  use_case_id: string
  title: string
  given: string
  when: string
  then: string
  status: string
  is_approved: boolean
}

export interface Requirement {
  id: string
  req_id: string
  req_type: string
  title: string
  description: string
}

export interface TestCase {
  id: string
  test_id: string
  title: string
  description: string
  test_type: string
  status: string
}

export interface CodeGenerateResponse {
  feature_id: string
  artifacts_count: number
  commit_sha: string | null
  push_status: string
  generation_report: {
    backend_files?: number
    bot_files?: number
    total_files?: number
  }
}

export interface GitHubPushResponse {
  branch: string
  commit_sha: string
  status: string
}

export interface DeployResponse {
  id: string
  target: string
  status: string
  endpoints: Record<string, string> | null
  logs: string | null
  error_message: string | null
}

export interface Traceability {
  feature_id: string
  user_stories_count: number
  use_cases_count: number
  requirements_count: number
  test_cases_count: number
  code_artifacts_count: number
}
