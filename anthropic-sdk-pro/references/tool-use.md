# Tool Use / Function Calling

> Section 5 from the Anthropic SDK reference. Covers JSON Schema tools, agentic loop, Zod-based tools, tool choice options, and structured output via tools.

---

## Defining Tools with JSON Schema

```ts
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  tools: [
    {
      name: "suggest_skills",
      description: "Suggest relevant skills for a job role in the Vietnamese market",
      input_schema: {
        type: "object",
        properties: {
          role: { type: "string", description: "Job title/role" },
          industry: { type: "string", description: "Industry sector" },
          count: { type: "number", description: "Number of skills to suggest" },
        },
        required: ["role"],
      },
    },
  ],
  messages: [{ role: "user", content: "What skills should a frontend developer have?" }],
})

// Check for tool use in response
for (const block of response.content) {
  if (block.type === "tool_use") {
    console.log(block.name)  // "suggest_skills"
    console.log(block.input) // { role: "frontend developer", industry: "Technology", count: 10 }
    console.log(block.id)    // "toolu_01..."
  }
}
```

## Handling Tool Results (Agentic Loop)

```ts
// After getting tool_use response, feed back the result
const toolResult = await executeSkillSuggestion(block.input)

const followUp = await anthropic.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  tools: [/* same tools */],
  messages: [
    { role: "user", content: "What skills should a frontend developer have?" },
    { role: "assistant", content: response.content },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: block.id,
          content: JSON.stringify(toolResult),
        },
      ],
    },
  ],
})
```

## Zod-Based Tools (SDK Helper)

```ts
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod"
import { z } from "zod"

const skillTool = betaZodTool({
  name: "suggest_skills",
  inputSchema: z.object({
    role: z.string().describe("Job title/role"),
    industry: z.string().optional().describe("Industry sector"),
  }),
  description: "Suggest relevant skills for a job role",
  run: async (input) => {
    // Your implementation here
    return { skills: ["React", "TypeScript", "Node.js"] }
  },
})

// Auto-runs tools in a loop
const result = await anthropic.beta.messages.toolRunner({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Suggest skills for a frontend developer" }],
  tools: [skillTool],
})
```

## Tool Choice Options

```ts
// Let model decide (default)
tool_choice: { type: "auto" }

// Force use of any tool
tool_choice: { type: "any" }

// Force use of specific tool
tool_choice: { type: "tool", name: "suggest_skills" }

// Prevent tool use
tool_choice: { type: "none" }
```

## Structured Output via Tools

For guaranteed JSON schema conformance, use `strict: true`:

```ts
tools: [
  {
    name: "extract_cv_data",
    description: "Extract structured CV data from text",
    input_schema: { /* JSON Schema */ },
    strict: true,  // Guarantees output matches schema exactly
  },
],
tool_choice: { type: "tool", name: "extract_cv_data" },
```
