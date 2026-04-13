working-student/
├── client/                      # Giao diện người dùng (React/Next.js hoặc IDE extension)
│   ├── src/
│   │   ├── wizard/              # Guided Intake UI (6 pha, form validation, conditional questions)
│   │   ├── planner/             # Plan review UI (step editor, rationale display, confidence badge)
│   │   ├── executor/            # Execution tracker (step status, sample preview, approve/rollback)
│   │   ├── observability/       # Session history, cost tracker, escalation dashboard
│   │   └── api/                 # REST/WebSocket clients → core backend
│   └── public/
│
├── core/                        # Orchestration Layer (Python/FastAPI)
│   ├── intake/                  # Phase manager, context assembler, input validator
│   ├── planner/                 # Skill matcher, template loader, plan generator
│   ├── executor/                # Step runner, checkpoint manager, rollback logic, sample-first gate
│   ├── session/                 # State persistence, plan serialization (YAML/JSON), versioning
│   └── main.py                  # FastAPI entrypoint, routing, middleware
│
├── mal/                         # Model Abstraction Layer
│   ├── providers/               # Claude, OpenAI, DeepSeek, Ollama adapters
│   ├── schemas/                 # Pydantic models: IntakeResult, ExecutionPlan, MCPToolCall
│   ├── translator.py            # Canonical ↔ model-specific prompt/tool format
│   ├── validator.py             # JSON Schema validation, auto-retry (max 3x), fallback routing
│   └── router.py                # Auto model selection (cost/perf/task_type)
│
├── skills/                      # Knowledge Layer (Markdown + YAML/JSON configs)
│   ├── data-streaming/          # DLT nodes, sources, transformers, patterns
│   ├── data-management/         # Grist table design, column types, permissions
│   ├── no-code/                 # Superset chart types, dashboard layouts, filters
│   ├── engineering-domain/      # Signal theory, units, sampling, common analyses
│   ├── templates/               # Reusable workflow configs (pre-validated)
│   └── README.md                # Skill authoring guide, versioning policy
│
├── integration/                 # Integration Layer (MCP Gateway)
│   ├── gateway.py               # Tool router, health checks, circuit breaker, rate limiter
│   ├── clients/                 # DLT MCP, Grist MCP, Superset MCP clients
│   ├── tools/                   # Tool definitions, parameter schemas, MCP spec mapping
│   └── mocks/                   # Local MCP stubs for testing without real services
│
├── observability/               # Monitoring & Analytics
│
├── config/                      # Environment & Feature Flags
│   ├── settings.py              # Pydantic BaseSettings, env var mapping
│   ├── models.yaml              # Model routing rules, token budgets, fallback chains
│   └── features.yaml            # Skill enablement, wizard phases, escalation thresholds
│
├── tests/                       # Testing Suite
│   ├── unit/                    # MAL, planner, executor, session state
│   ├── integration/             # End-to-end: intake → plan → MCP execution
│   ├── golden/                  # Known-good configs per skill (CI-gated)
│   └── fixtures/                # Sample TDMS/CSV, mock MCP responses, error cases
│
├── scripts/                     # Dev & CI Utilities
│   ├── validate_skills.py       # Lint skills, check broken references, run golden tests
│   ├── generate_tool_schemas.py # Auto-generate MCP tool defs from platform APIs
│   └── seed_templates.py        # Populate DB with starter workflow configs
│
├── docs/                        # Architecture, API spec, contributor guide
├── docker-compose.yml           # Local dev: backend, UI, DB, MCP mocks, observability stack
├── Makefile                     # make dev, make test, make validate-skills, make run
└── pyproject.toml               # Dependencies, build config, linting rules