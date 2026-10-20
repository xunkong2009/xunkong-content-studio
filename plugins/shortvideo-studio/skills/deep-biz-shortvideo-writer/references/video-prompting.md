# Video Prompting

## Purpose

Use this guide when the user wants the confirmed short-video script turned into prompts for Jimeng or similar video-generation models. The goal is not to rewrite the script, but to convert it into a small set of visually executable clip prompts.

## When To Use

- The script has already been written and the user says it is confirmed
- The user asks for `即梦 prompt`, `Jimeng prompt`, `视频生成 prompt`, `视频分镜提示词`, or similar packaging help
- The user wants a visual pack to generate B-roll, scene clips, or AI video assets from the script

## Default Assumptions

- Use `3:4` video unless the user specifies another ratio
- Default to realistic live-action unless the script obviously needs animation, collage, UI mockup, or surreal metaphor
- Use 4-8 prompts for one short video, not a long storyboard
- Treat each prompt as one clip idea lasting roughly 5-10 seconds

## Workflow

1. Confirm the script is stable enough to package. If major argument or structure changes are still likely, fix the script first.
2. Identify the script's major beats:
   - hook
   - explanation turn
   - case/example beat
   - ending frame
3. Decide whether the visuals should use:
   - realistic scene reenactment
   - business/consumer B-roll
   - symbolic metaphor shots
   - screen/UI style visuals
   - a mixed approach
4. Lock one visual world in `视觉总设定` so the prompts feel like one video rather than unrelated clips.
5. Write one prompt per beat. Each prompt should include:
   - subject
   - action
   - environment
   - camera framing or movement
   - lighting / mood
   - style cues
6. Add a short `负向约束` when it prevents obvious model failures.

## Prompt Rules

- Keep one prompt focused on one visual idea.
- Prefer concrete scenes over abstract summaries.
- If the script is analytical, default to B-roll and symbolic realism instead of trying to lip-sync every sentence.
- Use the same age, clothing, setting palette, and camera language when continuity matters.
- Avoid demanding readable long text on signs, menus, phone screens, or subtitles inside the generated video unless necessary.
- If a clip depends on a specific brand or public figure likeness, use safer descriptive phrasing unless the user explicitly wants direct brand recreation.

## Output Heuristics

- Hook prompt should be the most legible and thumb-stopping image
- Middle prompts should explain, not just decorate
- Ending prompt should visually upgrade the frame, not merely repeat the opening
- If the script names data, laws, or abstract mechanisms, translate them into scenes, objects, screens, crowds, workflows, or behavioral detail

## Failure Modes

- Repeating the same shot with tiny wording changes
- Stuffing multiple scenes into one prompt
- Writing prompts so abstract that the model produces generic stock footage
- Letting continuity drift across clips
- Treating prompts as subtitles or narration instead of visual instructions
