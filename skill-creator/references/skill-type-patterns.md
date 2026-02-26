# Skill Type Patterns

Reference architecture for each skill type. Use these patterns when building new skills.

## Scoring Pattern

```
skill-name-scoring/
├── SKILL.md              # Criteria table + grade scale + output format
├── references/
│   ├── overview.md       # Weights, grading scale, scoring methodology
│   ├── scoring-workflow.md  # Step-by-step scoring process
│   └── criteria/         # 1 file per criterion
│       ├── criterion-1.md
│       └── criterion-2.md
└── evals/
    └── eval-scoring.json
```

**Key sections in SKILL.md:** Criteria table (10 rows, weights sum to 100), Grade scale (A-F), Output format (scorecard table).

## Fix Pattern

```
skill-name-fix/
├── SKILL.md              # Severity priority table + fix process
├── references/
│   ├── overview.md       # Fix priority framework
│   ├── implementation-workflow.md  # Step-by-step fix process
│   └── fix-patterns/     # 1 file per fix category
│       ├── pattern-1.md
│       └── pattern-2.md
└── evals/
    └── eval-fix.json
```

**Key sections in SKILL.md:** Fix process (consume scoring output), Severity table (Critical/High/Medium/Low with SLA), Fix pattern references.

## Generate Pattern

```
skill-name-generate/
├── SKILL.md              # Output specs + decision table
├── references/
│   ├── conventions.md    # Naming, structure, style rules
│   └── templates/        # Output templates per type
│       ├── template-1.md
│       └── template-2.md
├── scripts/
│   └── scaffold.py       # Generate boilerplate
└── evals/
    └── eval-generate.json
```

**Key sections in SKILL.md:** Output specifications table, Decision table (user wants → action → template), Conventions reference.

## Migrate Pattern

```
skill-name-migrate/
├── SKILL.md              # Breaking changes summary + process
├── references/
│   ├── breaking-changes.md   # All breaking changes detailed
│   ├── migration-steps.md    # Ordered step-by-step process
│   └── codemods/             # Automated transformations
│       ├── codemod-1.md
│       └── codemod-2.md
├── scripts/
│   └── check-migration.py   # Verify migration completeness
└── evals/
    └── eval-migrate.json
```

**Key sections in SKILL.md:** Breaking changes table (change, severity, codemod?), Migration process, Version compatibility notes.

## Review Pattern

```
skill-name-review/
├── SKILL.md              # Review criteria + output format
├── references/
│   ├── review-criteria.md    # All criteria detailed
│   ├── common-issues.md      # Frequently found issues + fixes
│   ├── output-format.md      # Review report structure
│   └── criteria/             # Detailed criteria files
│       ├── criterion-1.md
│       └── criterion-2.md
└── evals/
    └── eval-review.json
```

**Key sections in SKILL.md:** Criteria table, Output format (issue entry template), Severity levels.

## Test Pattern

```
skill-name-test/
├── SKILL.md              # Test strategy + naming conventions
├── references/
│   ├── test-setup.md         # Environment, fixtures, mocks
│   └── test-patterns/        # Patterns per test type
│       ├── unit.md
│       ├── integration.md
│       └── e2e.md
├── scripts/
│   └── run-tests.py          # Test runner with coverage
└── evals/
    └── eval-test.json
```

**Key sections in SKILL.md:** Strategy table (layer, what, tool, target), Naming conventions, Coverage targets.

## General Pattern

```
skill-name/
├── SKILL.md              # Overview + workflow/task sections
├── references/
│   ├── overview.md       # Detailed concepts
│   └── topic-*.md        # One file per topic
├── scripts/              # Optional
│   └── helper.py
├── assets/               # Optional
│   └── template.ext
└── evals/
    └── eval-skill.json
```

**Key sections in SKILL.md:** When to Use, Process/Workflow, Quick Reference index.
