# Evaluation protocols

The results below use different protocols. They should not be combined into an official benchmark score or treated as matched leaderboard comparisons.

## LIBERO

The representative set contains Spatial tasks 0 and 3, Object tasks 1 and 9, and LIBERO-10 task 5. Each task uses ten fixed initial states and at most 300 steps. The base policy succeeds in 48/50 trials. It has 47,570,534 stored parameters and does not include the separately trained feedback head.

A separate Spatial-0 stress test uses 50 initial states. This release contains neither the simulator state files nor the checkpoint needed to execute those rollouts.

## RLBench

Fifteen tasks use eight seeds each (730072–730079), giving 104/120 successes. This evaluation set was used during development. Task-specific adapters are selected from the instruction before execution, not selected after observing outcomes.

The selected-task configuration has 54,550,093 parameters: 47,570,534 shared backbone parameters, 6,972,327 embodiment-adapter parameters, and 7,232 selected task-adapter parameters. The complete task bank stores 21,568 parameters, giving 54,564,429 in the full stored configuration. These are not Top-2 active-parameter counts.

LIBERO and RLBench both use Franka Panda, with different environments and action conventions. This comparison supports environment/interface transfer, rather than a change in physical robot structure.

## ARX5 offline agreement

The validation split contains seven tasks. Each task uses 4,096 sampled windows, calibrated-derived state inputs, and regression-anchor weight 1.0 (bypassing latent flow sampling). A window passes when its first predicted step is within 0.08 radians for every arm joint and within 0.002 meters for the gripper. An episode passes if at least 95% of its evaluated windows pass.

The task counts are 81/82, 88/101, 97/97, 99/120, 88/95, 115/125, and 99/110 in the order recorded in `data/paper_results.json`. Their equal-task macro average is 91.86%; this is not a pooled episode rate. The validation split was used for model selection, so it is not an independent blind test. Agreement is not physical task success.

## SO-ARM101 physical evaluation

Two arms provide twelve normalized joint/gripper command coordinates: five joints and one gripper per arm. The policy uses global and wrist RGB and an eight-step action horizon. Joint coordinates use the controller's [-100,100] scale and grippers [0,100], not degrees.

- Tape removal and handover: transfer the tape to the other arm and release it on the table; 18/20.
- Tape placement: release the tape inside the box; 26/30.
- Bottle-cap placement: place the cap and return the bottle to the table; 10/15. Tightening is not required.

The three tasks total 65 physical trials. The 53,753,814-parameter policy uses a separate auxiliary image decoder of approximately 0.34M parameters for analysis. Refinement freezes the visual encoder, while shared dynamics and embodiment modules are trainable. Retention on the original LIBERO tasks was not tested for this refinement.

Trajectory-based action/image errors are distinct from completion counts. The analyzed recordings also enter adaptation; disjoint validation blocks within a recording do not establish generalization to independent episodes. The public aggregate counts are not a substitute for per-trial recordings.

## Feedback intervention

The main mechanism study uses twenty LIBERO-Spatial/Object tasks, six independently trained seeds, and four fixed initial states per task: 480 paired rollouts per condition. Only the feedback input is replaced by zeros at evaluation. Weights, tasks, and starting states are matched; observations and actions can subsequently diverge.

Feedback gives 353/480 successes versus 319/480 without it. Of the paired episodes, 64 succeed only with feedback and 30 only without it. An exact McNemar test evaluates this paired difference. A separate seed sign test uses five positive and one negative seed difference; its p-value is 0.21875. The episode and seed tests answer different questions.

The feedback input includes dynamics residuals, routing weights, and event predictions. Zeroing the entire vector does not isolate future-prediction semantics. For the separate five-task policy, adding the feedback head gives 47/50 versus 48/50 with the feedback input zeroed.

## Action interfaces and parameter accounting

- LIBERO: seven-dimensional Cartesian-delta/gripper actions.
- ARX5: 16-dimensional latent actions decoded to six absolute joints and a gripper.
- RLBench: 16-dimensional latent actions decoded to seven intermediate coordinates, followed by task corrections and environment-specific position/quaternion/gripper conversion.
- SO-ARM101: a fixed 12-to-16-dimensional codec; predicted future features refine flow conditioning, and decoded deltas are added to the current state before command bounding.

The 47.57M stored backbone has approximately 33.10M contributing under final Top-2 routing. The 108,088-parameter LIBERO feedback head is additional. The 256 updated instruction scalars are already included in the shared checkpoint and must not be counted twice.
