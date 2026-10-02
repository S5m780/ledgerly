# v2 design notes — the "motor sideways into a bevel" idea, examined

## What was proposed
Replace the worm gearbox with a reduction gearmotor lying flat, driving the vertical shaft through a
bevel pair, so the base can be thinner.

## Where the idea is right
- **Height is the right target.** In v1 the base is 42 mm because the JGY-370 worm *gearbox* is 26 mm
  tall along its output shaft, the spur gear plane sits above it, and two 608 bearings are stacked on
  the rod above that. None of those three is the motor can.
- **A flat motor with a right-angle stage can be much lower.** With a 12 × 10 mm N20 gearmotor lying
  on its side the drive stage is 22 mm tall, and the base comes out at **26 mm** (v1: 42). Overall
  height with the plate is **35 mm** (v1: 56).

## Where it is wrong or risky
1. **The worm gearbox already puts the motor sideways.** A JGY-370 is a right-angle gearbox: the can is
   horizontal in v1 too. Swapping it does not by itself save height; the stack-up does.
2. **A true bevel pair is the wrong right-angle gear for FDM.** Bevel teeth are conical on both gears,
   both cone apexes must coincide (mounting distance on *both* axes to ±0.1 mm), and the driven bevel
   has undercut flanks that print badly. The FDM-friendly equivalent is a **crown (face) gear**: a flat
   disc with rack-shaped teeth driven by an ordinary spur pinion. It prints teeth-up with zero
   overhang, the pinion is a standard gear, and axial position of the pinion is uncritical (±0.5 mm).
   That is what v2 uses. It is the same kinematics the user asked for (horizontal motor, vertical shaft).
3. **You give up self-locking.** A worm holds the plate when power is off; a spur/crown train can be
   turned by hand. With a 1:1000 N20 the train is *practically* non-backdrivable, but forcing the plate
   round by hand will strip the N20's brass gears. For a display this is acceptable; it is a real
   trade-off, not a free win.
4. **Noise on a livestream.** Every printed gear mesh adds a tick. An N20 at 12 V also whines at
   higher ratios. Mitigations built in: module-1 teeth with 0.2 mm backlash, PETG, a dab of PTFE grease
   on the crown, and the lowest-speed motor that still reaches 5 RPM (20 RPM version). The v1 worm
   drive is the quieter of the two designs.
5. **Torque is fine, stiffness needs care.** A 20 RPM N20 gives roughly 2 kg·cm; after 3.5:1 that is
   ~7 kg·cm at the plate, ten times what a plate of cards needs. What matters for a thin base is
   *tilt stiffness* of the plate, and that comes from bearing spacing or bearing diameter, not from
   the gear type.

## The change that actually makes it slim: a fixed axle with the bearings inside the moving parts
- The post is fixed to the base. The crown gear carries a 608 in a pocket on its underside; the plate
  hub carries a second 608 in its housing. The two bearings are 12.4 mm apart on the post, which is as
  stiff as v1's rotating rod with less height, and no printed surface rubs.
- The plate weight goes hub → bearing → spacer tube → bearing → base. The crown only transmits torque
  through a hex coupling, so gear loading never bends the post.
- The post is printed (Ø7.85, 100 % infill) because it never rotates against anything: the inner races
  are stationary on it. An 8 mm steel rod is a one-line option (`axle = "steel"`).

## Other optimisations folded into v2
- Base diameter 180 → 170 mm (the motor is 60 mm long instead of 85).
- No grub screws, no rod to cut, no hex boss on the plate top: the hub bolts to the plate from
  underneath with three screws and the plate top is clean.
- The rocker switch turns 90° to fit the 19 mm tall wall.
- The interference view now includes the spacer, both bearings, the strap and the plate.
- Parts are auto-plated for the H2S (`python -m designer plate`): two plates, no supports, no glue.

## What I would still watch
- **Pinion on a 3 mm D-shaft.** Printed 3 mm bores are at the edge of FDM accuracy. The pinion has a
  10 mm long bore (7 mm teeth + 3 mm hub) and is printed at 100 % infill; if it spins on the shaft,
  a drop of CA glue fixes it for good.
- **Crown ceiling bridge.** The bearing pocket in the crown is bridged over 22 mm at 1.5 mm thick;
  Bambu Studio's bridge detection handles it, or print the crown at 0.12 mm layers.
- If the plate ever wobbles more than you like, upgrade the hub bearing to a 6806 (30 × 42 × 7) — the
  housing has the wall for it — rather than adding a third bearing.

## Verdict
Keep the sideways-motor idea, do it with a crown gear and a fixed axle, and accept the two real costs
(not self-locking, a little more gear noise). The result is 16 mm lower than v1 at the base, 21 mm lower
overall, cheaper (N20 ≈ $4 vs JGY-370 ≈ $12) and simpler to assemble.

## Card easel (revision after feedback)
One slot, on the rotation axis, so the card turns about its own centre instead of orbiting. The easel's
Ø96 base drops into a 0.8 mm recess in the plate top, so it cannot creep off-centre while spinning. Slot
3.2 mm wide for a sleeved card (a toploader also fits), 20 mm deep so a knock does not tip it, and the slot
and back-rest lean 12° back so a camera in front sees the face square-on rather than foreshortened. The
front lip is only 10 mm with a finger notch, so the artwork stays visible and the card is easy to pull.
Plate thickness went 6 → 7 mm to keep 3 mm of material between the recess and the hub pocket.
