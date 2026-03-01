# Prompt Engineering Best Practices

> Section 14 from the Anthropic SDK reference. Covers general principles, system prompt template, temperature guidelines, output format control, avoiding common Claude behaviors, and structured output reliability.

---

## General Principles (from Anthropic docs)

1. **Be clear and direct**: Think of Claude as a brilliant new employee who needs explicit context
2. **Add context/motivation**: Explain *why* you want something, not just *what*
3. **Use XML tags**: `<instructions>`, `<context>`, `<input>`, `<output>` to structure prompts
4. **Give Claude a role**: Set role in system prompt for focused behavior
5. **Use examples**: 3-5 diverse examples in `<example>` tags dramatically improve accuracy

## System Prompt Template for CViet

```ts
const SYSTEM_TEMPLATE = `You are an expert CV writer and career advisor specializing in the Vietnamese job market.

<context>
- Target audience: Vietnamese job seekers, students graduating, bilingual professionals
- Market: Vietnam 2026 job market
- Standards: ATS-friendly, professional, quantifiable achievements
</context>

<rules>
- {LANG_INSTRUCTION}
- Return ONLY the requested output format, no explanations
- Use action verbs for bullet points
- Include quantifiable metrics where possible
- Keep technical terms in English (programming languages, tools, frameworks)
- Maintain professional tone appropriate for Vietnamese business culture
</rules>

<output_format>
{FORMAT_INSTRUCTION}
</output_format>`
```

## Temperature Guidelines for CV Tasks

| Task | Temperature | Reasoning |
|------|------------|-----------|
| Bullet enhancement | 0.3 | Structured, predictable improvements |
| Summary generation | 0.5 | Slightly creative but professional |
| Skill suggestions | 0.2 | Factual, market-based |
| Translation | 0.1 | Accuracy over creativity |
| Cover letter | 0.7 | Needs personality and creativity |

## Controlling Output Format

Instead of "Don't use markdown", use:
```
Return your response as plain bullet points, one per line, starting with a bullet character.
Do not use headers, bold text, or numbered lists.
```

## Avoiding Common Claude Behaviors

1. **Preamble/disclaimers**: Add "Respond directly without preamble. Do not start with 'Here is...' or 'Based on...'"
2. **Over-explanation**: Add "Return ONLY the requested content, no commentary"
3. **Excessive markdown**: Match your prompt style to desired output style
4. **Hedging language**: Add "Be confident and direct in your suggestions"

## Structured Output Reliability

For JSON output, use these techniques in order of reliability:

1. **Best**: Use `output_config` with `json_schema` (guaranteed schema conformance)
2. **Good**: Use tools with `strict: true` as a structured output mechanism
3. **Acceptable**: Instruct in prompt + regex extraction (`text.match(/\{[\s\S]*\}/)`)

```ts
// Option 1: Structured Output (most reliable)
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  output_config: {
    format: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          skills: {
            type: "array",
            items: { type: "string" }
          }
        },
        required: ["skills"]
      }
    }
  },
  messages: [{ role: "user", content: "List 5 skills for a frontend developer" }],
})
// response.content[0].text is guaranteed valid JSON matching schema
```

---

## Sources

- [Anthropic SDK TypeScript](https://github.com/anthropics/anthropic-sdk-typescript)
- [Anthropic API Messages Reference](https://platform.claude.com/docs/en/api/messages)
- [Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Anthropic Rate Limits](https://platform.claude.com/docs/en/api/rate-limits)
- [Anthropic Prompt Engineering](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Anthropic Build Overview](https://platform.claude.com/docs/en/docs/build-with-claude/overview)
- [Vercel AI SDK Anthropic Provider](https://ai-sdk.dev/providers/ai-sdk-providers/anthropic)
- [Vercel AI SDK Next.js Getting Started](https://ai-sdk.dev/docs/getting-started/nextjs-app-router)
- [@anthropic-ai/sdk on npm](https://www.npmjs.com/package/@anthropic-ai/sdk)
- [Anthropic Prompt Injection Defenses](https://www.anthropic.com/research/prompt-injection-defenses)
