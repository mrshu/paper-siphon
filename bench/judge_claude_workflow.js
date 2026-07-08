export const meta = {
  name: 'judge-claude',
  description: 'Blinded Claude vision judge: one agent per paper scores anonymized backend outputs against rendered page images',
  phases: [{ title: 'Judge' }],
}

// args: { papers: [{id, pagesDir, packetPath, verdictPath, images:[...], labels:[...]}], rubric: "..." }
const papers = args.papers
const rubric = args.rubric

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['scores', 'ranking'],
  properties: {
    scores: {
      type: 'object',
      additionalProperties: {
        type: 'object',
        additionalProperties: false,
        required: ['text', 'tables', 'math', 'structure', 'evidence'],
        properties: {
          text: { type: 'integer', minimum: 0, maximum: 10 },
          tables: { type: 'integer', minimum: 0, maximum: 10 },
          math: { type: 'integer', minimum: 0, maximum: 10 },
          structure: { type: 'integer', minimum: 0, maximum: 10 },
          evidence: { type: 'string' },
        },
      },
    },
    ranking: { type: 'array', items: { type: 'string' } },
  },
}

const results = await parallel(
  papers.map((p) => async () => {
    const imgList = p.images.map((im) => `- ${im}`).join('\n')
    const prompt = `${rubric}

You are judging paper "${p.id}".

STEP 1: Read these rendered page images of the paper (use the Read tool on each path):
${imgList}

STEP 2: Read the blinded converter outputs from this JSON file (use Read):
${p.packetPath}
It has {"labels": {"A": "<markdown>", "B": "<markdown>", ...}} — the START of each converter's Markdown.

STEP 3: Score every label on the four axes (0-10) with one line of page evidence, and rank all labels best->worst. Return via the StructuredOutput tool ONLY.`
    const verdict = await agent(prompt, {
      label: `judge:${p.id}`,
      phase: 'Judge',
      schema: SCHEMA,
    })
    return { paper: p.id, verdictPath: p.verdictPath, verdict }
  })
)

// Emit results so the orchestrator can write verdict files.
return results.filter(Boolean).map((r) => ({
  ...r,
  verdict: { ...r.verdict, judge: 'claude' },
}))
