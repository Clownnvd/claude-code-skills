# CV-Specific AI Patterns

> Section 8 from the Anthropic SDK reference. Covers all 6 CViet AI prompts: bullet enhancement, summary generation, skill suggestion, translation, ATS optimization, and cover letter generation.

---

## Bullet Point Enhancement

```ts
// System prompt for bullet enhancement
const BULLET_ENHANCE_SYSTEM = `You are an expert CV writer specializing in the Vietnamese job market.
{LANG_INSTRUCTION}
Rewrite the provided bullet points to be more impactful, specific, and ATS-friendly.
Use action verbs and include quantifiable metrics where possible.
Return ONLY the improved bullet points, one per line, starting with a bullet character.
Do not add explanations or commentary.`

// Usage in route handler (current CViet pattern)
const prompt = `Role/Position: ${role || "Software Engineer"}

Original bullet points:
${bullets.map((b: string, i: number) => `${i + 1}. ${b}`).join("\n")}

Rewrite these to be more impactful and professional:`

const { text } = await callClaude(prompt, system, session.user.id)

// Parse response
const improvedBullets = text
  .split("\n")
  .map((line: string) => line.replace(/^[*\-*\d\.]\s*/, "").trim())
  .filter((line: string) => line.length > 0)
```

## Professional Summary Generation

```ts
const SUMMARY_SYSTEM = `You are an expert CV writer. {LANG_INSTRUCTION}
Write a compelling professional summary (3-4 sentences) for a CV.
Focus on: key skills, years of experience, industry expertise, and career goals.
Return ONLY the summary paragraph, no headers or extra text.`

const prompt = `Name: ${name || "Candidate"}
Current role: ${headline || "Professional"}
Recent experience: ${expSummary}
Education: ${education}
Top skills: ${skillList}

Write a professional summary for this person:`
```

## Skill Suggestion by Industry

```ts
const SKILLS_SYSTEM = `You are a career counselor specializing in the Vietnamese job market 2026.
{LANG_INSTRUCTION}
Suggest relevant, in-demand skills for the given role.
Return ONLY a JSON object with skill categories, no explanation:
{
  "Technical": ["skill1", "skill2", ...],
  "Tools": ["tool1", ...],
  "Soft Skills": ["skill1", ...]
}
Each category should have 4-6 skills.`

// Parse with JSON extraction
const jsonMatch = text.match(/\{[\s\S]*\}/)
const skillGroups = jsonMatch ? JSON.parse(jsonMatch[0]) : {}
```

## Vietnamese/English Translation

```ts
const TRANSLATE_SYSTEM = `You are a professional CV translator specializing in Vietnamese <-> English translation.
Translate the CV content from ${from === "vi" ? "Vietnamese" : "English"} to ${to === "vi" ? "Vietnamese" : "English"}.
Keep technical terms, company names, and proper nouns as-is.
Maintain professional tone and CV-appropriate language.
Return ONLY the translated JSON with the same structure, no explanation.`

const prompt = `Translate this CV data from ${from} to ${to}:

${JSON.stringify(cvData, null, 2)}

Return only the translated JSON object with identical structure.`
```

## Language-Aware Instructions

```ts
// Pattern used across all CViet AI endpoints
const langInstruction = language === "vi"
  ? "Viết bằng tiếng Việt chuyên nghiệp."
  : "Write in professional English."
```

## ATS Optimization Prompt

```ts
const ATS_SYSTEM = `You are an ATS (Applicant Tracking System) optimization expert.
Analyze the CV content and suggest improvements to increase ATS compatibility:
1. Keyword matching for the target role
2. Standard section headers (e.g., "Work Experience" not "My Journey")
3. Proper date formatting (MM/YYYY)
4. Quantifiable achievements
5. Industry-standard terminology

Return a JSON object:
{
  "score": 0-100,
  "improvements": ["suggestion1", "suggestion2", ...],
  "missingKeywords": ["keyword1", "keyword2", ...],
  "formattingIssues": ["issue1", "issue2", ...]
}`
```

## Cover Letter Generation

```ts
const COVER_LETTER_SYSTEM = `You are a professional cover letter writer for the Vietnamese job market.
Write a compelling, personalized cover letter based on the CV data and job description.
Structure: Opening paragraph (hook) -> Body (2-3 paragraphs matching skills to job) -> Closing.
Keep it concise (250-350 words).
${langInstruction}`
```

---

## Quick Reference: CViet AI Endpoints

| Endpoint | File | Purpose | Model |
|----------|------|---------|-------|
| `/api/ai/enhance` | `src/app/api/ai/enhance/route.ts` | Improve bullet points | claude-sonnet-4-6 |
| `/api/ai/summary` | `src/app/api/ai/summary/route.ts` | Generate professional summary | claude-sonnet-4-6 |
| `/api/ai/skills` | `src/app/api/ai/skills/route.ts` | Suggest skills by role | claude-sonnet-4-6 |
| `/api/ai/translate` | `src/app/api/ai/translate/route.ts` | Translate CV (VI/EN) | claude-sonnet-4-6 |

All endpoints share the same pattern:
1. Auth check via Better Auth
2. AI limit check via `checkAILimit()`
3. Language-aware system prompt
4. `callClaude()` wrapper with usage tracking
5. Response parsing and serialization
