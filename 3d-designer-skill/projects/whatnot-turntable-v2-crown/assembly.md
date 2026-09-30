# Assembly — turntable v2 (crown drive)

Ten minutes with a 2 mm hex key and a Phillips screwdriver. Wiring is identical to v1: see
`../whatnot-turntable/wiring.md` and `wiring.svg` (jack → rocker → PWM → motor, knob on the PWM pot pads).

## Before printing
Measure the N20 you received. `n20_gb_len` (gearbox length, 9–12 mm) and `n20_shaft_len` are the only
numbers that move the pinion; set them in `lib/hardware.scad` and re-run `python -m designer run`.

## Steps
1. **Crown.** Press a 608 into the pocket under the crown gear (pocket opens at the flat face). Push it in
   square with the flat of a hex-key handle until it bottoms on the ceiling.
2. **Drop the crown onto the post**, bearing first. Its inner race lands on the 12 mm ring around the post
   and the crown floats 1.5 mm above the floor. Spin it: it should coast.
3. **Spacer** over the post onto the crown's inner race.
4. **Pinion.** Push the pinion onto the N20's D-shaft, hub towards the gearbox, until the hub is 0.5 mm
   from the gearbox face. Solder or crimp the two motor leads.
5. **Motor** into the cradle, shaft pointing at the centre, and screw the strap down with two M3 × 8. The
   pinion should mesh with the crown with a hair of backlash; turn the crown by hand and feel for tight
   spots. If it binds, back the motor out 0.3 mm with a slip of paper under the rear stop.
6. **Electronics.** PWM board on foam tape in its bay, rocker into the sideways cutout, pot and jack in
   their holes. Wire per the diagram, test the motor direction, swap leads if needed.
7. **Hub.** From the flange side push the second 608 through the hex socket into its pocket; it stops on
   the ledge. Screw the hub flange into the plate's underside pocket with three M3 × 6 countersunk.
8. **Lid** over the post, six M3 × 8. The hub housing passes through the lid hole.
9. **Plate + hub** down over the post: the hub bearing slides on, the hex socket drops over the crown's
   hex boss, the flange floats 1 mm above the lid. Done; lift straight up to remove for shipping.
10. Rubber feet in the four recesses, plug in, switch on, set the knob.
