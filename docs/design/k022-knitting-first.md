# K022: knitting-first tabletop machine

Status: proposed design only. Date: 2026-10-07. Decision owner: Daniel (futuroptimist).

## Outcome and scope

Build toward the simplest reproducible machine that helps make a small, finished tabletop textile
or doily. Prioritize knitting **v1k**; defer the legacy crochet **v1c** mechanism. Function, stitch
reliability, assembly, and repair matter more than appearance. The first shape remains open until
the sample gate below; a plain rectangular mat is the lowest-complexity candidate, not a locked
product requirement. A decorative round lace doily is a later capability unless experiments justify
it sooner. Different patterns, outlines, and eventually three-dimensional forms follow evidence,
not calendar promises.

This proposal adds no CAD, app, firmware, motion execution, procurement, or deployment. It does not
certify a machine or authorize a build. The next authorized implementation should first deliver an
assembled OpenSCAD model and a browser simulation, using Three.js or a comparable local renderer.
There is no validated K022 hardware or simulation result yet. All numerical targets below are
proposed acceptance thresholds, not measurements or supplier guarantees.

## Reconcile the existing repository

The [knitting specification](../robotic-knitting-machine.md) explicitly says flat-bed knitting but
also specifies cut-down circular hand-knitting needles moved along X/Y. Circular hand needles are
not a circular knitting machine, and a moving needle alone does not specify loop retention,
knock-over, yarn capture, or fabric take-down. Do not treat that document as a completed mechanism.

The [v1c design](../wove-v1c-design.md) and current viewer lead with a CoreXY crochet gantry, SKR
controller, hook, and future heated-bed features. The [pattern CLI](../pattern-cli.md) demonstrates
crochet-inspired motion. These are historical references, not the v1k baseline or evidence of real
stitches. K022 proposes reversing the product order and targeting ESP32. No legacy executable
behavior changes in this PR. A later implementation must update entry points and viewer labels so
that the legacy plaza and the new evidence-backed machine cannot be confused.

### Mechanism alternatives and recommendation

| Alternative | Small finished textile route | Main cost or uncertainty |
| --- | --- | --- |
| Single flat bed | Panel plus edge finishing | Reversal, hold-down, friction |
| Circular cylinder | Tube, or panel with reversal | Disk shaping, ring accuracy, take-down |
| Robotic hand needles | Varied knit structures | Coordinated motion and loop transfer |
| Crochet gantry (v1c) | Shaped flat crochet | Capture, retention, fabric registration |

**Recommend one short flat bed with purchased steel latch needles, a passive cam carriage, one
driven travel axis, one yarn, and passive adjustable take-down.** Avoid individual needle motors,
a second bed, automatic transfers, and an X/Y/Z gantry in the first machine. A simple carriage
must knit in both directions or the design must explicitly add a non-knitting return cycle; this
proposal chooses bidirectional knitting as a hypothesis to validate, not an existing capability.

Circular machines remain a serious fallback if their measured stitch reliability and total build
effort beat the flat bed for the selected finished sample. The addi manufacturer demonstrates flat
panels on a circular machine [S1]; this supports the alternative, not compatibility with Wove.
Neither mechanism inherently creates a flat circular doily. Compare complete output and finishing
work, not only motor count. Select the route after the manual stitch gate; record why any reversal
of the recommendation occurred. Do not buy a donor machine as part of this design task.

## First sample and mechanism contract

At the sample gate, freeze one yarn specification, needle part number, gauge, stitch structure,
outline, finishing recipe, and dimensions. Candidate envelope: a 100-150 mm tabletop mat with
roughly 24 active needles, subject to measured relaxed gauge. Needle pitch is a hardware dimension;
finished stitch gauge must be measured after the specified wash or blocking process. The candidate
needle count does not guarantee that size. Freeze an attainable target before powered trials.

Single-bed plain knitting can curl. A mat only counts as finished if its declared border, seam,
backing, or other finishing process leaves it usable on a table. Compare the simplest hand finish
against added machine complexity; do not quietly assume that blocking permanently fixes curl.
Lace, automatic shaping, purl on one bed, and automatic cast-on or bind-off are not MVP claims.

The proposed loop cycle for each active needle is:

1. Retain the previous loop while the cam advances the needle enough to clear the latch.
2. Hold the fabric down so the old loop stays behind the open latch.
3. Present yarn at a defined guide height and timing, within the hook capture region.
4. Retract the needle; the old loop closes the latch and passes over the closed hook.
5. Draw the new loop through, retain it, and advance fabric under controlled take-down.

This sequence requires compatible hook/latch geometry, a measured cam profile, needle retention,
an adequate knock-over edge or sinker arrangement, and workable tension. Supplier descriptions
distinguish loop-forming parts and latch functions [S2, S3]; they do not validate our printed bed.
First prove one needle, then a short row including both edge needles and direction reversal.
If passive hold-down fails, compare a simple hold-down comb or sinkers before adding active axes.
Document failure images and the geometry change; stop motorization until manual stitches work.

## Simulation first, with explicit limits

The first implementation milestone is a reproducible assembled machine, not an ornamental scene.
OpenSCAD remains the dimensioned source. Export separate rigid parts with stable identifiers;
store assembly transforms, joint axes, motion limits, materials, and BOM references in a versioned
manifest. STL does not carry units or assembly joints: declare millimeters and a right-handed,
Z-up source frame, with one documented conversion into the browser scene. Pin exporter and renderer
versions and save source revision, parameter set, mesh hashes, and regeneration commands [S4, S5].

The browser loads that exact manifest and part set, shows assembled and exploded views, and offers
pause, single-step, reset, slow playback, joint limits, section views, and visible contact regions.
Include purchased needles, guide surfaces, fasteners, motor, belt, fabric path, guards, switches,
and cable clearance. A hidden fastener is still part of the assembly. Show yarn as a simplified
path plus loop-state annotations, with assumed tension and take-down clearly labeled.

| Evidence level | What a passing result establishes | What it does not establish |
| --- | --- | --- |
| Geometry | Nominal fit within stated tolerances | Print accuracy, wear, stiffness |
| Rigid motion | Joint sequence and swept clearance | Forces, missed steps, loop capture |
| Simplified yarn | Intended loop states and feed continuity | Friction, elasticity, real stitches |
| Physical sample | Named build/yarn/process passed trials | Other yarns, speeds, shapes |

Use badges such as "proposed", "simulation checked", and "physically tested" with evidence links.
Only call rigid motion validated after saving the checks and their limits. A scripted loop appearing
in the renderer is not a simulated physical stitch. Keep inferred yarn states distinct from measured
telemetry. The viewer must never turn prerecorded `home_state` metadata into permission to run.

Proposed simulation acceptance:

- Clean checkout regenerates the complete assembly and opens it locally without cloud credentials.
- Every visible rigid component has a stable ID, source or purchased-part entry, and transform.
- The model runs 100 complete carriage traversals, including both reversals, with deterministic
  state checkpoints. Check swept volumes, not only frame snapshots, and disclose mesh resolution.
- Enumerate intentional contacts (cam/needle butt, bearings, yarn surfaces); no other intersections
  are allowed across travel, cable sweep, fastener access, and a documented print tolerance sweep.
- Begin with a +/-0.25 mm print-fit sensitivity study, then replace it with measured printer data.
  Required clearance is the full tolerance stack plus margin, not a universal 0.25 mm gap.
- Inject an overtravel command, missing home, sensor fault, and interrupted run. Show rejection or
  a latched fault; never display an automatic restart. These are logic demonstrations, not proof
  that a physical emergency stop works.
- Export the chosen recipe, parameters, checks, and known failures alongside screenshots or video.
  No hardware control endpoint is present in the first browser milestone.

## Materials, provisional BOM, and assembly

PLA is the default for cool, lightly loaded brackets, covers, spool supports, spacers, and trial bed
modules. Print coupons first. Record printer, filament batch, orientation, wall count, infill, and
clearance results; keep each part inside a 200 mm cube or document a modular joint. Orient parts
from the real load path and layer strength, not a blanket orientation rule. Prefer captive nuts to
hot insert installation where practical, and use one common fastener family where loads permit.

Exceptions must solve a measured problem: steel needles for smooth durable loop contact; metal
rails, bearings, motor mounts or spacers for stiffness and heat separation; smooth replaceable
liners for yarn abrasion; a suitable transparent guard for containment. Printed cam wear and bed
creep need testing. Change to a machined wear insert or a better-suited polymer only after recording
the failure, added cost, and revalidation. PLA is not the universal structural or thermal solution.
Inspect printed cam surfaces and needle channels after each prototype sample; log wear, debris,
and changes in sliding force. Stop trials if damage can affect needle retention or loop formation.

| Item | Initial quantity | Selection gate |
| --- | --- | --- |
| Matched steel latch needles | 24 active + 4 spares, provisional | Geometry, gauge, two sources |
| Printed bed, carriage, brackets, covers | One set | Fit, friction, wear, print volume |
| Metal rail and carriage bearings | One travel set | Stiffness and travel friction |
| Standard stepper, belt, pulleys and idler | One drive set | Measured force, torque and jam limit |
| ESP32 board and external stepper driver | One each | Pin, timing, voltage and fault audit |
| Enclosed low-voltage supply and logic regulator | One each | Measured load and fault behavior |
| Physical end switches | Two | Wiring fault detection and repeatability |
| Emergency stop and rated motor-power disconnect | One circuit | Independent power interruption |
| Guard with access interlock | One set | Reach, fragments, coast distance |
| Yarn guide, passive tensioner, take-down comb/weights | One set | No snagging or dropped loops |
| Fasteners, wire, connectors and fuse | Count at assembly freeze | Lengths and ratings |

This is a planning BOM, not an order list. The motor frame size alone is not a torque specification.
Set an initial **USD 300 parts-budget ceiling** for feasibility review, excluding printer, computer,
tools, shipping, tax, and labor; this is a decision budget, not a market quote. At BOM freeze, list
dated regional quotes, quantities, alternates, printing mass/time, consumables, and delivered total.
If the guarded working machine exceeds the budget, revisit the architecture with Daniel. Never
meet the ceiling by deleting guards or power isolation. No parts are purchased by this proposal.

Planned assembly order, to be proven and illustrated in a later build guide:

1. Print fit and sliding coupons; inspect needle channels and remove burrs without changing datums.
2. Assemble the base and rail against shared datums; measure alignment and free travel.
3. Fit the bed, retained needles, cam carriage, yarn guide, and passive take-down. Turn by hand.
4. Verify manual loops and edge reversal before connecting the drive. Record all adjustments.
5. Fit motor, belt, hard stops, switches, guards, and cable relief; check full travel without yarn.
6. With power disconnected, verify wiring, polarity, fuse, and the independent stop circuit.
7. A qualified builder commissions low-speed motion, measures stopping distance, and completes the
   calibration and fault gates before powered yarn trials. Never clear a jam while energized.

Supply a numbered illustrated parts list, actual fastener lengths, tools, orientation diagrams,
wiring drawing, adjustment order, troubleshooting table, and evidence log before a build release.
Do not ask a second builder to infer these from a browser rendering.

## ESP32 target, calibration, and safety decisions

Use an ESP32 as the target controller with an external current-limited stepper driver. Choose the
exact board and firmware only after a pin budget, boot-state audit, timing test, and driver logic
compatibility review. Espressif documents hardware timing and fault facilities [S6]; availability
depends on the chip and does not create a safety-rated controller. Do not assume the legacy Klipper
or SKR configuration runs on ESP32 unchanged. USB/local operation comes first; network access is
not required for motion and must not serve as an emergency stop.

The controller must own live homing, limits, speed, current limits, and a latched fault state.
Power-up, brownout, reset, disconnect, and unknown position must disable motion. Recovery requires
inspection, deliberate reset, and safe rehoming with yarn removed or secured; never resume a stale
job automatically. Keep the physical motor-power stop independent of application and firmware.
Power removal can cause coasting or loss of holding force: contain take-down weights and measure
the worst stop envelope. A guard/interlock must keep hands out until hazardous motion has stopped.

Before physical operation, a competent electrical/mechanical reviewer must specify and verify the
guard, access interlock, disconnect ratings, safe stopping behavior, and fault tests. This proposal
does not prescribe a safety certification or claim that an ESP32 input is a protective interlock.
Use a suitably certified enclosed external supply; no exposed mains wiring in the hobby assembly.
Select wire, connectors, fusing, and driver settings from actual ratings and measured load, with
strain relief and protected terminals. No heater, cutter, hot bed, or unattended operation in MVP.

Calibration records must include:

- Printer fit, bed alignment, needle pitch, needle travel, cam timing, and guide position.
- Measured carriage displacement and reversal backlash, not calculated microsteps alone.
- Ten home cycles with <=0.25 mm spread as an initial target; tighten if stitch clearances demand.
- Yarn identity and condition, relaxed gauge, take-down load, and measured tension range for the
  chosen recipe. Existing tension tables are hypotheses until reproduced on this yarn and machine.
- Low-speed trial force, current limit, speed/acceleration, motor/driver temperatures, and nearby
  printed-part temperature compared with actual material ratings and a documented margin.
- Emergency stop, access opening, stuck/open limit wire, reset, brownout, jam, and lost connection
  tests. Log stopping distance and residual motion. Set permitted speed from those measurements.

Yarn wrap and exposed needle points create entanglement and puncture hazards even at low speed.
Cover belts and the needle sweep, secure hair/clothing, and keep children and pets away. Isolate
power before threading, finishing, maintenance, or jam removal. A tension sensor may improve
detection later, but first builds still need supervision and physical protection.

## MVP acceptance and evidence ledger

The MVP is a reproducible **assisted** process producing a finished textile, not an autonomous
finished-object machine. Manual cast-on, threading, take-down setup, bind-off, and declared edge
finishing are allowed and must be timed and documented. Manual stitch correction during the powered
body knitting run is a failed trial. If Daniel requires automatic start and finish, revisit scope
before hardware work; do not relabel assistance as automation.

Freeze the recipe and acceptance target before testing. Proposed finished-sample gate:

- Three consecutive samples from one build, then one sample by an independent builder using the
  released instructions and BOM. Record every attempt, including failures, rather than selecting
  only successful outputs.
- No dropped stitches, yarn breaks, unintended holes, or manual loop repairs in the body run.
- Secured live loops and ends; no unraveling after the documented handling/wash process.
- Finished length and width within +/-10% of the frozen target after 24 hours relaxed conditioning.
- After the prescribed finishing and conditioning, unweighted edge lift <=5 mm on a level surface.
  Freeze the measurement method and photograph all edges; revisit the structure if it curls back.
- Report elapsed build time, assisted minutes per sample, machine time, finishing time, energy,
  yarn used, waste, jam count, and actual delivered cost. No throughput promise precedes these data.
- All safety and calibration gates pass at the tested speed. No result generalizes to other yarns
  or speed settings without rerunning the affected gates.

| Phase | Status now | Exit evidence and decision |
| --- | --- | --- |
| P0: design and recipe shortlist | Proposed in K022 | Daniel reviews scope, budget and assistance |
| P1: CAD and browser model | Not started | Rebuildable assembly, motion checks, limits |
| P2: manual stitch mechanism | After P1; not started | Loops, edges, reversal, chosen yarn |
| P3: guarded dry motion | Blocked by P2 | BOM, calibration, stop and fault evidence |
| P4: finished tabletop sample | Blocked by P3 | Consecutive samples and independent reproduction |
| P5: patterns and flat shapes | Deferred | New operations each earn simulation and sample gates |
| P6: three-dimensional textiles | Deferred | Transfer/shaping strategy and physical proof |
| C1: crochet v1c mechanism | Deferred separately | Loop retention and fabric registration proof |

Mechanical owner signs P1/P2 evidence; controls and safety reviewers sign P3; a second builder logs
P4 reproduction; Daniel approves scope and capability changes. These are unassigned roles, not
claims that reviewers or builders have been recruited. Each ledger update must link revision,
parameters, test procedure, raw results, failure notes, reviewer, and next decision. A failed gate
returns to the relevant design phase. Do not advance because a calendar milestone elapsed.

Later flat shapes may require changing active needle counts, holding needles, short rows, increases,
decreases, or transfers. Lace and three-dimensional work need their own needle/loop operations and
possibly more beds or actuators. Reserve modular bed and controller interfaces, but do not carry
that hardware cost into MVP before demonstrating need.

## Separate mechanisms, selectively shared abstractions

Knitting retains many live loops on needles; crochet needs its own hook/loop and fabric manipulation
strategy. Do not implement crochet by swapping a hook into the v1k carriage or by assuming identical
stitch commands. Preserve separate mechanism profiles, operation vocabularies, geometry, collision
sets, and acceptance samples.

Candidate shared abstractions are units, versioned machine profiles, assembly manifests, bounded
motion traces, test evidence, stop/fault reporting, and yarn calibration records. Reuse only after
each abstraction has a demonstrated meaning in both mechanisms. In particular, the legacy CLI's
yarn-feed axis is not proof of metered yarn delivery or valid knitting instructions. Define the
v1k operation contract first, then adapt only the compatible existing utilities.

## Domain and infrastructure dependencies

`wove.engineering` is the intended future public domain, not a deployment action or a verified DNS
configuration. Domain ownership/access, Cloudflare account and zone, DNS/TLS, deployment target,
and credentials require a separate authorized onboarding task. Sugarkube is a potential future
hosting/build dependency; its fit, repository contract, resources, backups, and operating owner
remain unverified. Nothing in P1-P4 requires it or a public internet service.

Future CI onboarding should pin OpenSCAD/browser tools, validate manifests and bounds, regenerate
assets, compare deterministic motion checkpoints, build docs, and retain evidence artifacts. Keep
untrusted PR checks separate from protected release credentials. Existing repo CI is used for this
documentation review; no workflow, secret, DNS record, Cloudflare setting, Sugarkube installation,
or unrelated Windows/production workload is changed here. A later hosting decision must include
cost, rollback, access ownership, and approval; machine operation remains local.

## Sources and limits

Checked 2026-10-07. These primary sources support mechanism and tooling context, not Wove tests.

- [S1: addi flat-panel example](https://addi.de/en/story/aermelschal-addiexpress/) demonstrates
  a circular machine used for flat panels and subsequent finishing.
- [S2: flat-knitting needles][s2] describes specialized needle and latch functions.
- [S3: circular-knitting parts][s3] identifies loop-forming and holding-down components.
- [S4: OpenSCAD command-line manual][s4] documents export options; reproducible assembly metadata
  is an additional Wove design requirement.
- [S5: Three.js documentation](https://threejs.org/docs/) provides the rendering tool reference;
  rendering is not a yarn physics solver.
- [S6: ESP32 MCPWM documentation][s6] describes timing and fault facilities, not machine safety.

[s2]: https://www.groz-beckert.com/en/products/knitting/flat-knitting.html
[s3]: https://www.groz-beckert.com/en/products/knitting/circular-knitting.html
[s4]:
  https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_OpenSCAD_in_a_command_line_environment
[s6]:
  https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/mcpwm.html
