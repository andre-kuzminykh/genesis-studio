const BASE = '/api/v1'

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

// Products
export const createProduct = (idea_text: string) =>
  request<import('../types').DiscoveryResponse>('POST', '/products/', { idea_text })

export const submitDiscovery = (productId: string, question: string, answer: string) =>
  request<import('../types').DiscoveryResponse>('POST', `/products/${productId}/discovery`, { question, answer })

export const generateFeatureMap = (productId: string) =>
  request<import('../types').Feature[]>('POST', `/products/${productId}/features`)

export const approveFeatureMap = (productId: string, featureIds: string[]) =>
  request('POST', `/products/${productId}/features/approve`, { feature_ids: featureIds })

// Features
export const generatePrdDraft = (featureId: string) =>
  request<import('../types').PRDVersion>('POST', `/features/${featureId}/prd/draft`)

export const approveStories = (featureId: string, storyIds: string[]) =>
  request<import('../types').UserStory[]>('POST', `/features/${featureId}/stories/approve`, { story_ids: storyIds, approved: true })

export const generateUx = (featureId: string) =>
  request<import('../types').UXFlow[]>('POST', `/features/${featureId}/ux/generate`)

export const generateUseCases = (featureId: string) =>
  request<import('../types').UseCase[]>('POST', `/features/${featureId}/use-cases/generate`)

export const approveUseCases = (featureId: string, useCaseIds: string[]) =>
  request<import('../types').UseCase[]>('POST', `/features/${featureId}/use-cases/approve`, { use_case_ids: useCaseIds, approved: true })

export const generateRequirements = (featureId: string) =>
  request<import('../types').Requirement[]>('POST', `/features/${featureId}/requirements/generate`)

export const generateTests = (featureId: string) =>
  request<import('../types').TestCase[]>('POST', `/features/${featureId}/tests/generate`)

export const approveTests = (featureId: string, testIds: string[]) =>
  request<import('../types').TestCase[]>('POST', `/features/${featureId}/tests/approve`, { test_ids: testIds, approved: true })

export const generateCode = (featureId: string, targetBranch = 'main') =>
  request<import('../types').CodeGenerateResponse>('POST', `/features/${featureId}/code/generate`, { target_branch: targetBranch })

export const pushToGithub = (featureId: string, targetBranch = 'main') =>
  request<import('../types').GitHubPushResponse>('POST', `/features/${featureId}/github/push`, { target_branch: targetBranch })

export const deployLocal = (featureId: string, target = 'both') =>
  request<import('../types').DeployResponse>('POST', `/features/${featureId}/deploy/local`, { target })

export const getTraceability = (featureId: string) =>
  request<import('../types').Traceability>('GET', `/features/${featureId}/traceability`)

// GitHub
export const connectGithub = (productId: string, owner: string, repoName: string) =>
  request('POST', `/github/connect/${productId}`, { owner, repo_name: repoName })
