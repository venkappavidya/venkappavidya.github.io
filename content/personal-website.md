---
title: My Journey Creating a Personal Webpage with AI Tools
date: March 2025
order: 1
kind: Essay
tags: AI, Web Development, Personal
excerpt: What worked, what did not, and where an engineer still has to take the wheel when building a personal site alongside Claude and ChatGPT.
---

When I set out to build my personal webpage, I decided to lean on AI tools to move faster. It saved
me real time, but more usefully it gave me a clear view of where modern web development is genuinely
improved by AI assistance, and where it is not.

## The tools I actually used

I worked with two assistants, and for different reasons.

**Claude** generated my initial page template. Having a solid foundation to build on made the whole
project manageable; not starting from an empty file removes the hardest part of any side project.

**ChatGPT** handled specific error solving. I already knew how to prompt it effectively from prior
work, which made it the faster option whenever something broke mid-development.

## What worked well

The initial template from Claude was genuinely helpful and saved significant time. But I needed to
take control of the visual direction. Neither assistant proposed a colour scheme that matched what I
had in mind, so I had to specify exactly what I wanted rather than accept the defaults.

The same applied to motion. I had to be precise about the transitions I wanted and hand over specific
code snippets for the model to modify. That collaborative pattern, where I directed and the AI
executed, produced a far more personal result than letting it make every decision.

### Where the tools were strongest

- **Rapid debugging.** The models caught and fixed errors quickly, including precisely adjusting CSS
  media queries when my navigation menu rendered incorrectly on mobile.
- **Accelerated development.** Development time shrank from days to hours, which meant I could run
  several design iterations instead of settling for the first workable version.
- **Code optimisation.** I got efficiency suggestions I might have missed: CSS variables for
  consistent colours, better HTML structure for accessibility.
- **Learning.** Working this way expanded my own web development knowledge, particularly around
  modern CSS techniques and responsive design.

## The challenge: context management

The main problem I ran into was context. When I kept prompting against the same page, the model would
eventually forget earlier code and replace it with something new, creating more issues than it solved.

The fix was specificity. Instead of asking for general improvements, I identified the exact section
that needed to change and requested a targeted edit. That single adjustment made the whole process
dramatically more efficient.

## Assistants versus app builders

As a software engineer, I prefer pairing an assistant like Claude or ChatGPT with a development
environment such as Replit. The side-by-side view keeps the process transparent and controllable in a
way that all-in-one app builders do not.

I appreciate the help with scaffolding and debugging, but I still prefer to handle certain parts
myself. My engineering background means I usually know exactly where and what to change to get the
result I want, and it is faster to just do it than to describe it.

## Advice for anyone building their own page

1. **Start from a template.** Vercel offers seamless deployment and strong template options for
   personal sites. Building from scratch is rarely worth it.
2. **Use AI for the initial build.** Let it create the structure, but be specific about layout,
   colours, and functionality.
3. **Keep modifications simple.** Use AI for straightforward HTML and CSS changes, and track your
   content in a JSON or Markdown file so the site stays easy to manage.
4. **Know the complexity limit.** For a simple personal page, AI handles most of the work. Complex
   sites still require real UI development expertise.
5. **Iterate.** Spend the time AI saves you on refinement, not on shipping the first draft.
6. **Read the generated code.** Studying what the model produced is one of the better ways to improve
   your own development skills.
7. **Plan your content first.** A clear content strategy before you write any code produces a far
   more cohesive result.

## Closing thought

I am genuinely impressed by how accessible webpage creation has become. For a personal site, these
tools handle much of the heavy lifting, which frees you to focus on personalisation and content.
Having built for the web both with and without AI assistance, I can say the landscape has changed for
the better, as long as you stay the one making the decisions.
