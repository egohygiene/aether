Anime Prompting Architecture Specification

1. Architectural Thesis

The "anime" system should not be designed as a collection of prompt templates.

It should be designed as a small domain-specific language and compiler pipeline for cinematic generative animation.

The system should separate:

1. creative intent
2. project-wide identity
3. narrative structure
4. scene design
5. media references
6. animation behavior
7. model capabilities
8. model-facing prompt text

The authoring format may be detailed and expressive.

The final Gemini or Veo prompt should usually be short, concrete, and constrained.

This produces the following architecture:

creative intent
    ↓
project specification
    ↓
scene intermediate representation
    ↓
validation and normalization
    ↓
strategy selection
    ↓
model-specific lowering
    ↓
prompt simplification
    ↓
Gemini / Veo prompt

The system should preserve rich intent internally while exposing only the minimum necessary information to the animation model.

---

2. Critique of the Current Architecture

What Is Already Correct

The current architecture correctly separates several concepts that were previously conflated:

- Visual DNA
- Character DNA
- narrative strategy
- scene generation strategy
- animation prompts
- transition language

It also correctly recognizes that narrative construction and model generation are independent.

For example:

- A linear story may use first-frame-only generation.
- A fragmented story may use first-and-last-frame generation.
- A hybrid story may mix all four generation strategies.

The current distinction between story strategy and scene generation strategy should remain.

The strongest current principle is:

one beginning
one ending
one primary motion
one emotional purpose

This should become a formal scene invariant rather than informal advice.

Where the Current Architecture Is Still Too Prompt-Centric

Several current concepts are described in terms of prompt-writing rather than scene semantics.

For example:

- “Gemini prompt template”
- “prompt enhancement”
- “transition language”

These concepts should exist later in the compilation pipeline.

The source specifications should describe what the scene is, not how Gemini should be instructed.

Instead of storing:

prompt: >
  Slowly push the camera toward the glowing tree...

The source representation should store:

camera:
  movement: push_in
  speed: slow
  target: tree

subject_motion:
  type: breathing
  intensity: subtle

destination:
  composition: close_view_of_tree

emotion:
  purpose: awe

Prompt text should be generated from this semantic representation.

---

3. Missing Abstractions

3.1 Project Specification

A project needs a canonical top-level specification containing global identity and production constraints.

project:
  id: constellations
  title: Constellations
  format: music_video
  aspect_ratio: "9:16"
  target_duration_seconds: 48
  default_clip_duration_seconds: 8
  narrative_strategy: hybrid

This becomes the root of inheritance.

---

3.2 Emotional Arc

Visual DNA describes how the project looks.

It does not fully describe how the project should emotionally evolve.

A separate emotional arc should define progression over time.

emotional_arc:
  opening:
    state: isolation
    energy: restrained
    clarity: low

  development:
    state: awakening
    energy: rising
    clarity: emerging

  resolution:
    state: connection
    energy: peaceful
    clarity: complete

Individual scenes can reference positions within this arc:

emotion:
  state: wonder
  arc_position: development
  intensity: 0.65
  purpose: first recognition of interconnectedness

This prevents every scene from independently attempting to express the entire song.

---

3.3 Symbol Registry

Recurring symbols should not be duplicated across scenes as free text.

They should be defined once.

symbols:
  constellation_thread:
    meaning: invisible connection between living beings
    appearance:
      form: thin luminous thread
      palette_role: accent
      behavior: slowly reveals itself
    continuity:
      preserve_shape_language: true

  tree_of_life:
    meaning: growth and interconnected consciousness
    appearance:
      material: crystalline
      glow: internal

Scenes then reference symbols:

symbols:
  - id: constellation_thread
    role: emerging_revelation

This improves consistency and allows the compiler to include only relevant symbol details.

---

3.4 Environment DNA

Environment identity should be independent from both Visual DNA and scene composition.

environments:
  cosmic_ocean:
    geography: endless reflective water beneath deep space
    horizon: low
    atmosphere: thin violet haze
    lighting_source: diffuse celestial glow
    persistent_elements:
      - distant stars
      - soft water reflections

This makes environment continuity enforceable.

---

3.5 Shot Specification

A scene and a shot should not necessarily be the same abstraction.

A scene is an emotional or narrative unit.

A shot is a continuous camera event.

Most current Gemini clips should compile to one shot, but the distinction is still valuable.

scene:
  id: awakening

  shots:
    - id: awakening_push
      continuous: true

For current Gemini constraints, validation may enforce:

Gemini scene generation:
one scene → one shot

Future models may support multi-shot scenes without changing the project representation.

---

3.6 Subject Motion and World Motion

Camera motion, character motion, environment motion, and transformation should be stored separately.

motion:
  camera:
    type: push_in
    speed: slow

  subject:
    type: float
    intensity: subtle

  environment:
    type: drifting_particles
    intensity: minimal

  transformation:
    type: constellation_reveal
    progression: gradual

The compiler may choose one as the primary motion and demote the others to supporting motion.

---

3.7 Continuity Contract

Each scene should declare what must remain stable and what is allowed to change.

continuity:
  preserve:
    - character.identity
    - character.clothing
    - environment.geometry
    - lighting.direction
    - camera.axis

  mutable:
    - constellation.visibility
    - particle.density
    - character.position

  prohibited:
    - additional_characters
    - wardrobe_change
    - environment_replacement

This is more precise than repeatedly saying “maintain continuity.”

---

3.8 Transition Contract

Transitions should describe the relationship between two scenes, not just visual prose.

transition:
  from: scene_03
  to: scene_04

  continuity_element:
    type: constellation_thread

  motion_match:
    direction: upward

  visual_match:
    source: glowing_thread
    destination: galaxy_river

  transition_mode: morph
  edit_fallback: dissolve

Transitions can then be implemented through:

- generated motion
- first-and-last-frame interpolation
- post-production editing
- a dedicated bridge scene

---

3.9 Model Capability Profile

Model behavior should not leak into scene definitions.

Each backend should declare capabilities and limits.

models:
  gemini_veo:
    supports:
      first_frame: true
      last_frame: true
      storyboard: true
      prompt_only: true

    preferences:
      maximum_primary_motions: 1
      concise_prompt: true
      continuous_camera: true

    weaknesses:
      - complex_multi_stage_transformations
      - simultaneous_subject_actions
      - dense_negative_constraints
      - long_specification_prompts

A future model might support:

models:
  future_model:
    preferences:
      structured_prompt: true
      multi_shot: true

The source scene does not need to change.

---

3.10 Generation Attempt and Evaluation Records

Generated outputs should be treated as reproducible experiments.

attempt:
  id: scene_03_attempt_04
  scene: scene_03
  backend: gemini_veo
  compiler_version: "0.4.0"
  seed: null
  prompt_hash: sha256:...
  references:
    - first_frame.png
    - last_frame.png
  result: scene_03_attempt_04.mp4

evaluation:
  identity_consistency: 0.9
  motion_naturalness: 0.6
  camera_quality: 0.8
  emotional_resonance: 0.9
  transition_accuracy: 0.7

  failures:
    - character_pose_too_rigid
    - constellation_appeared_too_suddenly

This creates a feedback dataset for future prompt refinement.

---

4. Recommended Specification Layers

The framework should use five major layers.

Layer 1: Intent

Human creative meaning.

What does the song mean?
What should the audience feel?
What emotional transformation occurs?

Layer 2: World

Persistent project identity.

Visual DNA
Character DNA
Environment DNA
Symbol registry
Palette
Rendering rules

Layer 3: Narrative

How the complete work is constructed.

Narrative strategy
Emotional arc
Scene ordering
Anchor scenes
Bridge scenes
Pacing

Layer 4: Scene Intermediate Representation

Model-independent description of one scene.

Initial state
Final state
Primary motion
Supporting motion
Emotional purpose
Continuity contract
References

Layer 5: Backend Output

Model-specific submission materials.

Gemini prompt
Reference image ordering
First/last-frame assignment
Negative constraints
Model settings

---

5. Recommended File Organization

anime-project/
├── anime.yaml
├── song/
│   ├── metadata.yaml
│   ├── lyrics.txt
│   ├── analysis.yaml
│   └── timing.yaml
├── dna/
│   ├── visual.yaml
│   ├── motion.yaml
│   ├── camera.yaml
│   └── environments.yaml
├── characters/
│   ├── protagonist.yaml
│   ├── secondary-character.yaml
│   └── references/
├── symbols/
│   ├── constellation-thread.yaml
│   ├── tree-of-life.yaml
│   └── galaxy-heart.yaml
├── narrative/
│   ├── strategy.yaml
│   ├── emotional-arc.yaml
│   ├── sequence.yaml
│   └── transitions.yaml
├── scenes/
│   ├── scene-001.yaml
│   ├── scene-002.yaml
│   └── scene-003.yaml
├── assets/
│   ├── references/
│   ├── first-frames/
│   ├── last-frames/
│   ├── storyboards/
│   └── audio/
├── backends/
│   ├── gemini.yaml
│   ├── sora.yaml
│   └── defaults.yaml
├── builds/
│   └── gemini/
│       ├── scene-001/
│       │   ├── prompt.txt
│       │   ├── manifest.json
│       │   └── references.json
│       └── scene-002/
├── outputs/
│   ├── raw/
│   ├── selected/
│   └── final/
└── evaluations/
    ├── scene-001.yaml
    └── scene-002.yaml

For smaller projects, the system may permit a single-file format:

anime.yaml

The CLI can support both:

monolithic authoring
modular authoring

Internally, both should normalize into the same representation.

---

6. Canonical Project Specification

schema_version: "1.0"

project:
  id: constellations
  title: Constellations
  type: music_video
  aspect_ratio: "9:16"
  narrative_strategy: hybrid
  default_scene_duration_seconds: 8

song:
  title: Constellations
  audio: assets/audio/constellations.wav
  emotional_core: discovering that apparent separation is an illusion

inherit:
  visual_dna: dna/visual.yaml
  motion_dna: dna/motion.yaml
  camera_dna: dna/camera.yaml

characters:
  - characters/protagonist.yaml

symbols:
  - symbols/constellation-thread.yaml
  - symbols/tree-of-life.yaml

narrative:
  emotional_arc: narrative/emotional-arc.yaml
  sequence: narrative/sequence.yaml
  transitions: narrative/transitions.yaml

backend:
  default: gemini
  configuration: backends/gemini.yaml

---

7. Canonical Scene Intermediate Representation

The scene IR is the most important specification in the system.

schema_version: "1.0"

scene:
  id: scene-003
  title: Recognition
  role: anchor
  duration_seconds: 8

narrative:
  purpose: the character recognizes that the stars are connected
  arc_position: awakening
  previous_scene: scene-002
  next_scene: scene-004

emotion:
  primary: awe
  secondary: vulnerability
  intensity:
    start: 0.35
    end: 0.75

generation:
  strategy: first_last
  backend: inherit

references:
  first_frame:
    path: assets/first-frames/scene-003.png
    authority: exact

  last_frame:
    path: assets/last-frames/scene-003.png
    authority: exact

state:
  initial:
    subject: character floating in still cosmic water
    constellation_visibility: absent
    camera_distance: wide

  final:
    subject: same character floating naturally
    constellation_visibility: fully visible
    camera_distance: medium

motion:
  primary:
    domain: camera
    type: push_in
    direction: forward
    speed: slow
    easing: smooth

  supporting:
    - domain: subject
      type: natural_floating
      intensity: subtle

    - domain: environment
      type: water_ripple
      intensity: minimal

transformation:
  subject: constellation
  type: gradual_reveal
  onset: delayed
  progression: continuous
  completion: final_frame

continuity:
  preserve:
    - composition
    - character.identity
    - character.clothing
    - environment
    - perspective
    - lighting.direction
    - art_style

  prohibit:
    - additional_characters
    - rigid_t_pose
    - camera_orbit
    - hard_cut
    - sudden_constellation_appearance

transition:
  incoming:
    visual_element: reflected_starlight

  outgoing:
    visual_element: constellation_line
    motion_direction: upward

This representation is intentionally more expressive than the final prompt.

---

8. Scene Invariants

The validator should enforce or warn about the following.

Hard Invariants

For Gemini-oriented scenes:

exactly one initial state
exactly one final state
at most one primary motion
exactly one emotional purpose
exactly one generation strategy

Soft Constraints

Warnings should be produced when:

- more than two supporting motions exist
- more than one major transformation exists
- a scene contains multiple camera motions
- final state is not visually distinguishable from initial state
- emotional purpose is abstract but has no visual manifestation
- prompt-only strategy is used for identity-sensitive character scenes
- storyboard strategy is used without clearly ordered keyframes
- first-and-last strategy contains incompatible geometry
- continuity requirements conflict with transformation requirements

Example diagnostic:

ANIME-W104:
Scene "scene-003" defines three transformation events.

Gemini performs more reliably with one primary transformation.

Suggested resolution:
- retain "constellation reveal"
- move "clothing glow" to supporting environmental motion
- move "sky opening" to the next scene

---

9. Narrative Strategies

The three narrative strategies should be formalized as policies rather than templates.

Fragmented

narrative_strategy:
  type: fragmented

  continuity_requirements:
    narrative: low
    visual: high
    symbolic: high
    temporal: optional

  editing_priority:
    - rhythm
    - emotional contrast
    - recurring imagery

Linear

narrative_strategy:
  type: linear

  continuity_requirements:
    narrative: high
    spatial: high
    temporal: high
    visual: high

  scene_rule:
    final_state_becomes_next_initial_state: true

Hybrid

narrative_strategy:
  type: hybrid

  authoring:
    linear_understructure: true

  editing:
    reorder_allowed: true
    repeat_allowed: true
    symbolic_continuity_required: true

Hybrid should probably be the default for music videos.

It preserves emotional meaning without making editing rigid.

---

10. Generation Strategies

These should be called generation strategies or conditioning strategies, not storytelling strategies.

First Frame

Best for:

- organic motion
- atmospheric scenes
- scenes where the destination is intentionally open
- low-risk character movement

Compiler requirements:

first frame
scene purpose
primary motion
mood
minimal continuity constraints

First + Last

Best for:

- intentional transformations
- camera destinations
- scene-to-scene continuity
- controlled narrative progression

Compiler requirements:

exact first frame
exact last frame
one continuous movement
primary transformation
transition quality

This should likely be the preferred default.

Storyboard

Best for:

- multiple meaningful phases
- complex spatial progression
- visual sequences that cannot be represented by a single destination

Storyboard should not automatically mean “include every frame description in the prompt.”

The images should communicate progression.

The text should explain only:

ordering
primary motion
continuity
timing emphasis

Prompt Only

Best for:

- abstract bridges
- particles
- energy fields
- cosmic tunnels
- environmental establishing shots
- non-identity-sensitive material

Prompt-only generation should have stronger Visual DNA injection because no image anchors the style.

---

11. Prompt Compilation Pipeline

The compiler should operate in explicit stages.

Stage 1: Load

Read:

- project specification
- inherited DNA
- character definitions
- scene specification
- backend profile
- media references

Stage 2: Resolve Inheritance

Produce a fully resolved scene.

project defaults
    ↓
Visual DNA
    ↓
environment defaults
    ↓
character identity
    ↓
scene overrides
    ↓
backend overrides

No inheritance markers should remain after this phase.

Stage 3: Validate

Check:

- schema validity
- missing references
- contradictory states
- too many motions
- impossible continuity requirements
- incompatible first and last frames
- unsupported model features

Stage 4: Normalize

Map synonyms to canonical terms.

zoom toward → push_in
move closer → push_in
slow dolly forward → push_in

Normalize intensity:

barely moving → subtle
gentle → subtle
soft → subtle

Normalize direction:

toward subject → forward
rising → upward

This makes compilation deterministic.

Stage 5: Determine Visual Delta

Calculate what changes between the first and final state.

visual_delta:
  camera_distance:
    from: wide
    to: medium

  constellation_visibility:
    from: absent
    to: visible

  character_identity:
    unchanged: true

The visual delta should become the heart of the final prompt.

Stage 6: Rank Information

Assign every instruction a priority.

P0: reference authority
P1: primary motion
P2: required destination
P3: primary transformation
P4: identity continuity
P5: supporting motion
P6: mood
P7: decorative detail

Stage 7: Select Backend Strategy

The backend adapter decides how to express the scene.

For Gemini:

favor references
favor concrete motion
favor destination
remove redundant style prose
limit negative constraints

For another model:

emit structured shot description
include longer physical descriptions
support multiple phases

Stage 8: Simplify

Remove everything that does not materially affect generation.

Stage 9: Render

Produce:

- prompt text
- reference manifest
- generation strategy
- ordered image inputs
- backend options
- provenance metadata

Stage 10: Audit

Generate a human-readable explanation of what was included and omitted.

included:
  - exact first-frame authority
  - exact last-frame authority
  - slow push-in
  - gradual constellation reveal
  - awe

omitted:
  - full Visual DNA prose because reference images already encode style
  - detailed tattoo description because character identity is visible
  - water reflection description because it is unchanged

This makes compiler behavior understandable.

---

12. Prompt Simplification

Prompt simplification should be semantic, not merely text shortening.

A generic text summarizer may remove the wrong information.

The simplifier should operate on ranked scene fields.

Simplification Rule 1: Do Not Describe Visible Constants

When an exact first frame is supplied, avoid restating:

- clothing
- face
- composition
- palette
- background geometry
- art style

unless the model has repeatedly drifted on that property.

Simplification Rule 2: Describe the Delta

Prioritize what changes:

The camera slowly pushes forward.
The constellation gradually appears.
The motion ends at the supplied final frame.

Simplification Rule 3: Collapse Redundant Continuity Language

Instead of:

Do not redesign, reinterpret, alter, restyle, replace, transform, or modify...

Use:

Preserve the supplied artwork and character identity.

Simplification Rule 4: One Verb Per Motion Domain

Avoid:

The character floats, turns, reaches upward, breathes, looks around, and smiles.

Prefer:

The character floats naturally with minimal body movement.

Simplification Rule 5: Separate Motion From Mood

Mood should not be used as a substitute for physical behavior.

Weak:

The camera moves spiritually and emotionally.

Strong:

The camera slowly pushes toward the tree.
Mood: reverent awe.

Simplification Rule 6: Remove Internal Meaning Unless It Changes the Image

The internal scene specification may say:

The tree represents healing, compassion, wisdom, and the interconnected nature of consciousness.

The Gemini prompt may only need:

A slow, reverent push toward the crystalline tree.

The symbolic meaning informs scene design but may not help animation.

Simplification Rule 7: Limit Negative Instructions

Use negative instructions only for high-risk failure modes.

Recommended maximum:

two to four critical prohibitions

Example:

No cuts, no camera orbit, no new objects.

Simplification Rule 8: Prefer Ordered Sentences

A Gemini output prompt should usually follow:

reference authority
primary motion
transformation
destination
supporting motion
mood
critical constraints

---

13. Gemini Backend Template

The Gemini template should be intentionally small.

Use the supplied image as the exact first frame.
Use the supplied destination image as the exact final frame.

Create one continuous cinematic shot.

The camera slowly pushes forward.
During the movement, the constellation gradually becomes visible.
End naturally at the supplied final frame.

Keep the character floating naturally with only subtle body movement.

Mood: quiet awe.

Preserve the artwork, character identity, environment, and lighting.
No cuts, no orbit, and no sudden transformation.

This text should be compiler output, not authored source.

Different strategies should use different renderers.

---

14. Prompt Enhancement Architecture

Prompt enhancement should not mean “make the prompt longer and more cinematic.”

It should mean:

extract intent
detect ambiguity
convert abstractions to observable behavior
identify primary motion
identify destination
remove conflicts
compress language

The enhancer should be a structured transformation pipeline.

Enhancement Input

raw_prompt: >
  Make him float naturally while the constellation appears beautifully
  and the camera moves cinematically through the emotional space.

Semantic Extraction

camera:
  type: unknown_cinematic_motion

subject:
  motion: float_naturally

transformation:
  constellation: appear

mood:
  emotional

Ambiguity Resolution

camera:
  type: push_in
  speed: slow

subject:
  motion: natural_floating
  intensity: subtle

transformation:
  type: gradual_reveal

Conflict Detection

Potential issue:

camera movement and constellation reveal are both major events

Resolution:

camera push-in = primary motion
constellation reveal = synchronized transformation

Enhanced Output

Create one continuous shot with a slow cinematic push-in.
The character floats naturally with minimal movement.
As the camera advances, the constellation gradually appears.
Preserve the original composition and character identity.

The enhancement process should be inspectable.

It should return both:

enhanced prompt
structured interpretation

---

15. Prompt Enhancement Modes

The CLI could support several modes.

anime prompt enhance
anime prompt simplify
anime prompt diagnose
anime prompt compile
anime prompt explain

Enhance

Converts rough language into concrete scene behavior.

Simplify

Removes unnecessary detail while preserving intent.

Diagnose

Finds:

- too many motions
- contradictory camera instructions
- vague language
- excessive negative constraints
- missing destination
- unclear reference authority

Compile

Generates model-facing prompt and manifest from the scene IR.

Explain

Shows why each instruction was included.

---

16. Language Design Principles

The specification language should favor constrained vocabularies where useful.

Camera Motion Vocabulary

camera_motion:
  - static
  - push_in
  - pull_out
  - pan_left
  - pan_right
  - tilt_up
  - tilt_down
  - track_forward
  - track_backward
  - rise
  - descend
  - orbit
  - handheld_drift

The Gemini profile may forbid or discourage some motions.

gemini:
  discouraged:
    - orbit
    - handheld_drift

Transformation Vocabulary

transformations:
  - reveal
  - dissolve
  - materialize
  - bloom
  - fracture
  - merge
  - morph
  - illuminate
  - fade

Motion Intensity

intensity:
  - imperceptible
  - subtle
  - gentle
  - moderate
  - strong

Pacing

pacing:
  - still
  - meditative
  - slow
  - measured
  - energetic
  - rapid

Controlled vocabularies improve validation while allowing optional free-text extensions.

---

17. Escape Hatches

The language should not become so rigid that it suppresses creativity.

Each structured object may support:

notes:
  creative_intent: >
    The floating should feel less like zero gravity and more like the body
    is being gently supported by invisible water.

extensions:
  x-anime:
    buoyancy_reference: underwater_suspension

The compiler can use these notes during reasoning without necessarily copying them into the final prompt.

---

18. Reference Authority

Every reference should declare what it controls.

references:
  - path: protagonist-reference.png
    authority:
      - character.face
      - character.hair
      - character.glasses

  - path: scene-first-frame.png
    authority:
      - composition
      - environment
      - lighting
      - character.pose

  - path: palette-reference.png
    authority:
      - palette
      - glow_language

This prevents ambiguity when multiple images are supplied.

Reference order should be generated by the compiler according to backend behavior.

---

19. Identity Drift Protection

Character DNA should distinguish stable identity from scene-local appearance.

character:
  id: alan

  immutable:
    face_shape: ...
    hair: ...
    glasses: ...
    tattoo_map: ...
    body_proportions: ...

  wardrobe_variants:
    galaxy_hoodie:
      ...
    white_sweater:
      ...

  behavioral_identity:
    movement_quality: soft and physically relaxed
    default_expression: introspective
    gesture_scale: restrained

The compiler should not inject the full character specification when an authoritative image is present.

Instead it should determine a drift-risk score.

drift_risk:
  face: low
  tattoos: high
  clothing_logo: high

Only high-risk details should be reinforced in the model-facing prompt.

---

20. Transition System

Transitions should exist at three levels.

Narrative Transition

What emotional or symbolic change connects the scenes?

isolation → recognition

Visual Transition

What visible element connects them?

constellation line → river of light

Edit Transition

How are the clips joined?

match cut
cross dissolve
motion match
light bloom
hard cut on beat

These must remain separate.

A generated clip does not always need to perform the entire transition.

Sometimes the correct solution is:

scene output ends with upward-moving particles
editor cuts to next scene beginning with upward-moving stars

The compiler should support an "edit_only" transition.

---

21. Build Artifacts

Each compiled scene should produce a build directory.

builds/gemini/scene-003/
├── prompt.txt
├── prompt.debug.txt
├── resolved-scene.yaml
├── manifest.json
├── references.json
└── diagnostics.json

"prompt.txt"

The exact submission prompt.

"prompt.debug.txt"

An annotated version showing field origins.

"resolved-scene.yaml"

The fully inherited scene representation.

"manifest.json"

Backend, compiler version, hashes, timing, and settings.

"references.json"

Ordered references and authority declarations.

"diagnostics.json"

Warnings, simplifications, and omitted details.

This makes builds reproducible and debuggable.

---

22. Suggested CLI

anime project init
anime project validate
anime scene create
anime scene validate
anime scene compile
anime scene render
anime scene evaluate
anime prompt enhance
anime prompt simplify
anime prompt diagnose
anime narrative validate
anime transition inspect
anime build

Example:

anime scene compile scenes/scene-003.yaml \
  --backend "gemini" \
  --output-directory "builds/gemini/scene-003"

A useful inspection command:

anime scene compile scenes/scene-003.yaml \
  --backend "gemini" \
  --explain

Possible output:

Primary motion:
  slow camera push-in

Primary transformation:
  gradual constellation reveal

Destination:
  exact supplied last frame

Omitted:
  14 Visual DNA fields already encoded by the images
  6 unchanged environment properties
  3 low-priority decorative motions

Warnings:
  supporting water motion may compete with subject floating

---

23. Internal Architecture

A maintainable implementation could use the following modules.

anime/
├── domain/
│   ├── project
│   ├── narrative
│   ├── scene
│   ├── character
│   ├── visual
│   ├── motion
│   └── transition
├── schemas/
├── parser/
├── inheritance/
├── validation/
├── normalization/
├── analysis/
│   ├── visual_delta
│   ├── motion_priority
│   ├── drift_risk
│   └── complexity
├── compiler/
│   ├── intermediate
│   ├── simplifier
│   └── renderer
├── backends/
│   ├── gemini
│   ├── sora
│   └── generic
├── evaluation/
├── manifests/
└── cli/

Backend adapters should implement a shared interface:

supports(scene)
validate(scene)
lower(scene)
simplify(lowered_scene)
render_prompt(lowered_scene)
build_manifest(scene)

---

24. Generic Backend Intermediate Representation

Before producing a Gemini prompt, the compiler should lower the full scene into a compact animation instruction representation.

animation_instruction:
  reference_mode: first_last
  first_frame_authority: exact
  last_frame_authority: exact

  shot:
    continuity: continuous
    camera_motion:
      type: push_in
      speed: slow

  transformation:
    subject: constellation
    type: gradual_reveal

  destination:
    type: supplied_last_frame

  supporting_motion:
    - natural_character_float

  mood:
    - quiet_awe

  preserve:
    - character_identity
    - environment
    - lighting
    - art_style

  prohibit:
    - cuts
    - orbit
    - sudden_reveal

This compact IR is then rendered differently for different models.

It is also easier to test than natural-language output.

---

25. Automated Complexity Budget

Each backend should define a complexity budget.

Example Gemini budget:

complexity_budget:
  primary_camera_motions: 1
  primary_subject_actions: 1
  primary_transformations: 1
  supporting_motions: 2
  emotional_descriptors: 2
  negative_constraints: 3
  destinations: 1

The compiler should calculate scene complexity.

complexity:
  score: 8
  backend_limit: 6
  status: simplify_required

It can then apply reductions:

remove decorative particle swirl
collapse breathing and floating into natural floating
move sky transformation to next scene
retain camera push-in and constellation reveal

---

26. Prompt Quality Evaluation

Prompt quality should be evaluated before generation.

Suggested checks:

prompt_quality:
  concrete_motion: pass
  single_primary_motion: pass
  destination_defined: pass
  emotional_purpose_defined: pass
  visible_delta_defined: pass
  reference_authority_clear: pass
  contradictory_constraints: pass
  excessive_description: warning
  negative_constraint_count: pass

After generation, output quality should be evaluated separately.

generation_quality:
  first_frame_fidelity:
  final_frame_fidelity:
  identity_consistency:
  camera_naturalness:
  physical_motion:
  transformation_timing:
  emotional_resonance:
  visual_cohesion:

Prompt quality and generation quality should never be conflated.

A valid prompt can still produce a poor sample.

---

27. Learning From Iterations

The system should support reusable failure patterns.

failure_patterns:
  rigid_float:
    symptoms:
      - arms extended unnaturally
      - static torso
      - t_pose appearance

    likely_causes:
      - vague floating instruction
      - no physical reference

    preferred_rewrite:
      from: character floats
      to: >
        character remains loosely suspended with relaxed shoulders,
        slightly bent arms, and subtle whole-body drift

  sudden_reveal:
    symptoms:
      - object appears instantly

    preferred_rewrite:
      from: constellation appears
      to: constellation gradually traces into view over the full shot

These can become compiler rewrite rules rather than repeatedly rediscovered prompt knowledge.

---

28. Recommended Specification Set

The first stable version should include:

anime-project.schema.yaml
visual-dna.schema.yaml
character-dna.schema.yaml
environment-dna.schema.yaml
symbol.schema.yaml
narrative.schema.yaml
emotional-arc.schema.yaml
scene.schema.yaml
transition.schema.yaml
backend-profile.schema.yaml
evaluation.schema.yaml

Do not begin with dozens of tiny specifications.

Start with a coherent core and extract files only when reuse becomes real.

---

29. Recommended Version-One Scope

Version one should focus on:

1. project inheritance
2. Visual DNA
3. Character DNA
4. scene IR
5. first-frame and first-plus-last strategies
6. Gemini backend
7. prompt simplification
8. diagnostics
9. build manifests
10. evaluation notes

Storyboard support should follow after the simpler strategies are stable.

Prompt-only support is easy to add, but should still use the same scene IR.

---

30. Final Architectural Principles

The system should follow these rules.

Author Richly, Compile Minimally

Store all creative intent.

Submit only what the model needs.

Describe States and Deltas

A scene is:

initial state
plus controlled change
equals final state

One Scene, One Cinematic Idea

A scene may contain detail, but it should have one dominant event.

Images Carry Appearance

Text should primarily carry motion, transformation, destination, and constraint.

Meaning Belongs Upstream

Symbolism and emotional interpretation shape scene design.

They do not always belong in the model-facing prompt.

Model Behavior Belongs in Backends

Gemini-specific prompt preferences should never contaminate the canonical scene model.

Simplification Is Compilation

Prompt shortening should be deterministic, priority-aware, and explainable.

Evaluation Is Part of the System

Every attempt should improve the framework’s knowledge about model behavior.

Preserve Human Direction

The framework should formalize and protect creative intent, not replace intuition with rigid automation.

---

31. Core Mental Model

The complete system can be summarized as:

Song meaning
    ↓
Emotional arc
    ↓
Narrative strategy
    ↓
Scene intention
    ↓
Initial and final visual states
    ↓
One primary motion
    ↓
Model-independent scene IR
    ↓
Backend-specific simplification
    ↓
Concise animation prompt
    ↓
Generated clip
    ↓
Evaluation and learned constraints

The source of truth is not the final prompt.

The source of truth is the resolved scene specification.

The prompt is merely one compiled artifact.

