#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path

from encoding_utils import configure_utf8_console, write_text_utf8

# Fix Windows console encoding for Unicode output (emojis, arrows)
configure_utf8_console()


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.

Example real scripts from other skills:
- pdf/scripts/fill_fillable_fields.py - Fills PDF form fields
- pdf/scripts/convert_pdf_to_images.py - Converts PDF pages to images
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here
    # This could be data processing, file conversion, API calls, etc.

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

Example real reference docs from other skills:
- product-management/references/communication.md - Comprehensive guide for status updates
- product-management/references/context_building.md - Deep-dive on gathering context
- bigquery/references/ - API references and query examples

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
"""

APACHE_LICENSE = """\
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

BEST_PRACTICES = """# Best Practices for {skill_title}

## Architecture & Design

### Do
- Follow single responsibility principle — one module, one job
- Use dependency injection over hard-coded imports for testability
- Design for immutability — create new objects, never mutate existing ones
- Separate business logic from I/O (database, network, file system)
- Use strong typing (TypeScript strict mode, Python type hints, Zod schemas)
- Keep functions small (< 50 lines), files focused (< 400 lines)

### Don't
- Don't mix concerns (UI logic in API routes, business logic in components)
- Don't use `any` type — it defeats the purpose of TypeScript
- Don't create abstractions for one-time operations — 3 similar lines > premature abstraction
- Don't design for hypothetical future requirements — solve today's problem

## Code Quality

### Naming
- Variables: descriptive, intention-revealing (`userEmail` not `e`, `isAuthenticated` not `flag`)
- Functions: verb + noun (`createUser`, `validatePayment`, `sendInvite`)
- Booleans: `is`/`has`/`can`/`should` prefix (`isActive`, `hasPermission`)
- Constants: UPPER_SNAKE_CASE for true constants (`MAX_RETRY_COUNT`)
- Files: kebab-case (`payment-service.ts`, `user-schema.ts`)

### Patterns
- Early returns over deeply nested if/else (guard clauses)
- Const by default, let only when reassignment is needed, never var
- Destructure at the point of use, not at function top
- Use optional chaining (`?.`) and nullish coalescing (`??`) over manual checks
- Template literals over string concatenation
- `async`/`await` over `.then()` chains

### Code Smells to Avoid
| Smell | Why It's Bad | Fix |
|-------|-------------|-----|
| Magic numbers/strings | Hard to understand and change | Extract to named constants |
| Deep nesting (> 3 levels) | Hard to read and test | Guard clauses, extract functions |
| God functions (> 100 lines) | Too many responsibilities | Split by concern |
| Boolean parameters | Unclear at call site | Use options object or separate functions |
| Comments explaining "what" | Code should be self-documenting | Rename variables/functions instead |
| Catch-all error handling | Hides real problems | Catch specific errors, log others |

## Security

### Input Validation
- Validate ALL external input at system boundaries (API routes, webhooks, form submissions)
- Use schema validation (Zod, Joi) — never trust `typeof` alone
- Sanitize HTML output to prevent XSS
- Parameterize all database queries — never interpolate user input into SQL
- Validate URLs: block `//` and `/\\` patterns (open redirect prevention)

### Authentication & Authorization
- Rate limit all auth endpoints (strict for POST, standard for GET)
- Never store secrets in code — use environment variables
- Validate JWT/session on every protected route, not just the first
- Use CSRF protection on all state-changing operations
- Hash passwords with bcrypt/argon2 — never SHA256/MD5
- Set secure cookie flags: `httpOnly`, `secure`, `sameSite`

### API Security
- Never leak internal errors to clients — return generic messages
- Validate payment amounts server-side before granting access
- Use HTTPS everywhere — redirect HTTP to HTTPS
- Set security headers: `X-Content-Type-Options`, `X-Frame-Options`, `CSP`
- Log security events (failed logins, permission denials) without PII

### Secrets Management
```
# .env.example — commit this (no real values)
DATABASE_URL=postgresql://user:pass@host:5432/db
STRIPE_SECRET_KEY=sk_test_xxx

# .env — NEVER commit this
DATABASE_URL=postgresql://real:credentials@prod:5432/db
STRIPE_SECRET_KEY=sk_live_real_key
```

## Error Handling

### Strategy
- Fail fast: throw on invalid state, don't return `null` silently
- Use typed errors: custom error classes with error codes
- Critical path vs non-fatal: payment processing = throw, email notification = log + continue
- Always clean up resources in `finally` blocks

### Patterns
```typescript
// GOOD: Specific error handling with context
try {{
  const result = await paymentService.charge(amount);
  return result;
}} catch (error) {{
  if (error instanceof InsufficientFundsError) {{
    return {{ error: 'Payment declined', code: 'INSUFFICIENT_FUNDS' }};
  }}
  // Re-throw unknown errors
  throw new PaymentError('Charge failed', {{ cause: error }});
}}

// BAD: Silent catch
try {{
  await sendEmail(user.email);
}} catch (e) {{
  // Silent failure — no one knows it broke
}}
```

### Error Table
| Error Category | Strategy | Example |
|---------------|----------|---------|
| Validation errors | Return 400 with field-level details | Missing required field, invalid email format |
| Authentication | Return 401, log attempt | Invalid token, expired session |
| Authorization | Return 403, log attempt | User accessing admin route |
| Not found | Return 404 | Resource doesn't exist |
| Rate limit | Return 429 with Retry-After header | Too many requests |
| External service | Retry with backoff, fallback | Stripe timeout, GitHub API 503 |
| Database | Retry transient, throw permanent | Connection lost vs constraint violation |
| Unexpected | Return 500 generic message, log full error | Unhandled exception |

## Performance

### General
- Measure before optimizing — don't guess bottlenecks
- Use database indexes for frequently queried columns
- Implement connection pooling for database connections
- Cache expensive computations (but invalidate correctly)
- Use pagination for list endpoints — never return unbounded results

### Frontend
- Lazy load routes and heavy components
- Optimize images (next/image, WebP, proper sizing)
- Minimize bundle size — check with `npx bundlecost` or build analyzer
- Use `useMemo`/`useCallback` only when profiler shows re-render problems
- Prefer CSS animations over JavaScript animations (GPU acceleration)

### Backend
- Use database transactions for multi-step writes
- Implement idempotent operations (webhooks, retries)
- Set appropriate timeouts on external API calls
- Use streaming for large responses
- Avoid N+1 queries — use includes/joins

## Testing

### Strategy
| Layer | What to Test | Tool |
|-------|-------------|------|
| Unit | Pure functions, utilities, validators | Vitest/Jest |
| Integration | API routes, database queries, service interactions | Vitest + test DB |
| E2E | Critical user flows (signup, purchase, dashboard) | Playwright/Cypress |

### Principles
- Test behavior, not implementation — "when X happens, Y should result"
- One assertion per test (or one logical assertion group)
- Use factories/fixtures over hardcoded test data
- Mock external services (Stripe, GitHub API), not internal modules
- Keep tests fast — under 10 seconds for unit suite

### Coverage Targets
| Area | Minimum | Target |
|------|---------|--------|
| Business logic | 80% | 95% |
| API routes | 70% | 90% |
| UI components | 50% | 70% |
| Utilities | 90% | 100% |

## Database

### Schema Design
- Use UUIDs or CUIDs for primary keys (not auto-increment integers)
- Add `createdAt` and `updatedAt` timestamps to all tables
- Use enums for fixed value sets (status, role, type)
- Add unique constraints for business identifiers (email, stripePaymentId)
- Index foreign keys and frequently filtered/sorted columns

### Migrations
- Never edit existing migrations — create new ones
- Test migrations on a copy of production data before deploying
- Always provide rollback scripts for destructive changes
- Use `migrate dev` locally, `migrate deploy` in CI/CD

### Queries
- Use transactions for multi-step operations
- Implement check-before-create for idempotent operations
- Use `select` to fetch only needed columns
- Use `include` carefully — avoid fetching entire relation trees

## Deployment

### Pre-Deploy Checklist
- [ ] All tests pass (`pnpm test`)
- [ ] Type check passes (`pnpm typecheck`)
- [ ] Lint passes (`pnpm lint`)
- [ ] No `console.log` in production code
- [ ] No hardcoded secrets or URLs
- [ ] Environment variables documented in `.env.example`
- [ ] Database migrations reviewed and tested
- [ ] Security headers configured
- [ ] Rate limiting enabled on all public endpoints
- [ ] Error monitoring configured (Sentry, LogRocket, etc.)

### Environment Variables
- Sync across 4 files: `env.d.ts` + `env.ts` + `.env.example` + test config
- Use `z.string().min(1)` for required env vars — catches empty strings
- Validate all env vars at startup — fail fast if missing
- Use separate values per environment (dev/staging/production)

## Documentation

### When to Document
- Public API endpoints (request/response examples)
- Non-obvious business logic ("why" not "what")
- Architecture decisions (ADRs for significant choices)
- Setup and deployment procedures

### When NOT to Document
- Self-explanatory code — rename instead of commenting
- Obvious function behavior — `getUserById` doesn't need a docstring
- TODOs without tickets — create an issue instead

## Resources

- [TODO: Official documentation URL]
- [TODO: API reference URL]
- [TODO: Community forum/Discord/GitHub discussions]
- [TODO: Related skills or tools]
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output Claude produces.

Example asset files from other skills:
- Brand guidelines: logo.png, slides_template.pptx
- Frontend builder: hello-world/ directory with HTML/React boilerplate
- Typography: custom-font.ttf, font-family.woff2
- Data: sample_data.csv, test_dataset.json

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Icons: .ico, .svg
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        write_text_utf8(skill_md_path, skill_content)
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    # Create LICENSE.txt
    license_path = skill_dir / 'LICENSE.txt'
    try:
        write_text_utf8(license_path, APACHE_LICENSE)
        print("✅ Created LICENSE.txt (Apache 2.0)")
    except Exception as e:
        print(f"❌ Error creating LICENSE.txt: {e}")
        return None

    # Create resource directories with example files
    try:
        # Create scripts/ directory with example script
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        write_text_utf8(example_script, EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ Created scripts/example.py")

        # Create references/ directory with example reference doc
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        write_text_utf8(example_reference, EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ Created references/api_reference.md")

        # Create references/best-practices.md
        best_practices = references_dir / 'best-practices.md'
        write_text_utf8(best_practices, BEST_PRACTICES.format(skill_title=skill_title))
        print("✅ Created references/best-practices.md")

        # Create assets/ directory with example asset placeholder
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        write_text_utf8(example_asset, EXAMPLE_ASSET)
        print("✅ Created assets/example_asset.txt")
    except Exception as e:
        print(f"❌ Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print("2. Customize or delete the example files in scripts/, references/, and assets/")
    print("3. Run the validator when ready to check the skill structure")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        print("\nSkill name requirements:")
        print("  - Hyphen-case identifier (e.g., 'data-analyzer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 40 characters")
        print("  - Must match directory name exactly")
        print("\nExamples:")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private")
        print("  init_skill.py custom-skill --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
