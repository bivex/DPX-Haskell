---
name: gemini-frontend-design
description: >-
  Generates distinctive, production-grade frontend interfaces using Gemini 3 Pro's creative capabilities
  and multi-step design thinking workflow. Avoids generic templates and AI slop through bold aesthetic directions.
---

# 🎨 Gemini 3 Pro Frontend Design Skill

This skill leverages Gemini 3 Pro's creative capabilities to generate distinctive, production-grade frontend interfaces. It uses a multi-step workflow: Gemini provides creative direction and initial implementation, then Claude refines and polishes the output.

---

## 🔄 Workflow

### Step 1: Parse User Requirements
Extract from user input:
- **Component/Page Type:** What are we building? (landing page, dashboard, form, card, pricing table, etc.)
- **Purpose:** What problem does it solve? Who uses it?
- **Technical Constraints:** Framework (React, Vue, vanilla, Svelte), styling (Tailwind, CSS Modules, inline, vanilla CSS).
- **Aesthetic Hints:** Any mentioned preferences (dark mode, brutalist, minimal, luxury, playful, cyber, etc.)

---

### Step 2: Call Gemini 3 Pro for Design Generation
Execute this Python command to generate the design with Gemini 3 Pro:

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
requirements = """{REQUIREMENTS}"""

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=f"""You are an elite frontend designer known for creating distinctive, memorable interfaces that avoid generic "AI slop" aesthetics.

REQUIREMENTS:
{requirements}

DESIGN THINKING PROCESS:
1. **Purpose Analysis**: What problem does this solve? Who uses it?
2. **Aesthetic Direction**: Choose ONE bold direction and commit fully:
   - Brutally minimal (precision, negative space, restraint)
   - Maximalist chaos (layered, textured, overwhelming)
   - Retro-futuristic (CRT vibes, neon, chrome)
   - Organic/natural (flowing shapes, earth tones, textures)
   - Luxury/refined (gold accents, serif fonts, dark themes)
   - Playful/toy-like (rounded corners, bright colors, bouncy animations)
   - Editorial/magazine (dramatic typography, asymmetric layouts)
   - Brutalist/raw (exposed structure, unconventional, harsh)
   - Art deco/geometric (patterns, gold, symmetry)
   - Industrial/utilitarian (monospace, yellow/black, functional)
3. **Typography**: Choose distinctive fonts - NEVER use Inter, Roboto, Arial, or generic system fonts. Pick characterful display fonts paired with refined body fonts.
4. **Color Palette**: Commit to a cohesive scheme. Dominant colors with sharp accents beat timid, evenly-distributed palettes.
5. **Signature Element**: What ONE thing will make this unforgettable?

OUTPUT FORMAT:
## Design Direction
[Explain your chosen aesthetic in 2-3 sentences]
## Signature Element
[The ONE memorable thing about this design]
## Color Palette
- Primary: [hex]
- Secondary: [hex]
- Accent: [hex]
- Background: [hex]
- Text: [hex]
## Typography
- Display Font: [font name from Google Fonts]
- Body Font: [font name from Google Fonts]
## Code
```[html/jsx/vue based on requirements]
[Complete, production-ready code with:
- All CSS included (inline styles, styled-components, or Tailwind based on context)
- Animations and micro-interactions
- Responsive design
- Semantic HTML
- Accessibility attributes
- Google Fonts import if needed]
```

CRITICAL RULES:
- NO purple gradients on white backgrounds
- NO generic card layouts
- NO cookie-cutter component patterns
- NEVER use overused fonts (Inter, Space Grotesk, Roboto)
- MAKE IT MEMORABLE - someone should remember this design
- COMMIT to your aesthetic direction - half-measures fail
- INCLUDE working animations and hover states
- USE unexpected layouts: asymmetry, overlap, diagonal flow, grid-breaking
""",
    config=types.GenerateContentConfig(
        system_instruction='You are an elite frontend designer and developer. You create distinctive, production-grade interfaces with bold aesthetic choices. Your code is always complete, functional, and ready for production. You never produce generic or templated designs.',
        temperature=0.9
    )
)
print(response.text)
```

---

### Step 3: Review and Refine Output
1. **Validate code** — Ensure it is syntactically valid, complete, and functional.
2. **Check aesthetic commitment** — Is the direction bold, distinctive, and devoid of generic AI slop?
3. **Verify typography** — Confirm distinctive Google Fonts or characterful display typefaces are imported.
4. **Enhance animations** — Add smooth transitions, hover effects, and micro-interactions.
5. **Fix issues** — Ensure responsiveness and accessibility attributes.

---

### Step 4: Present Final Design
- **Design Direction & Rationale**
- **The Signature Element**
- **Color Palette & Typography Choices**
- **Complete, Production-Grade Code**

---

## 🎯 Multi-Shot Design Exploration
For complex projects, explore multiple distinct aesthetic directions:
1. *Minimal Direction* (`brutally minimal`)
2. *Editorial / Magazine* (`editorial typography`)
3. *Cyber / Retro-futuristic* (`CRT vibes & neon`)
Synthesize the best elements or let the user choose.
