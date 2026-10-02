# Wiring — spin / hold switch and variable speed

```
  12 V adapter          KCD1 rocker            PWM speed controller              JGY-370
  (5.5x2.1 jack)        (spin / hold)          (12 V, ≥2 A)                      worm-gear motor
  ┌─────────┐           ┌──────────┐           ┌──────────────────────┐          ┌─────────┐
  │  + ●────┼───────────┤ ●      ● ├───────────┤ VIN+          MOTOR+ ├──────────┤ +       │
  │         │           └──────────┘           │                      │          │  M      │
  │  − ●────┼──────────────────────────────────┤ VIN−          MOTOR− ├──────────┤ −       │
  └─────────┘                                  │                      │          └─────────┘
                                               │  POT: CW  WIPER CCW  │
                                               └───┬─────┬─────┬──────┘
                                                   │     │     │        panel potentiometer B10K
                                                   └─────┴─────┴──────  (3 wires, order as marked
                                                                          on your board)
```

Also drawn in `wiring.svg` (open in any browser).

## Step by step

1. **Jack.** Fit the DC-022B in the 12 mm hole on the rear wall. The centre pin is **+**, the sleeve is **−** (check your adapter: "centre positive").
2. **Switch.** Snap the KCD1 into the rectangular cutout on the front-left of the base. It goes in series with the **positive** wire between the jack and the controller. Off = the plate holds still for showing one card, On = spin.
3. **Controller.** Stick the PWM board in the rectangular bay with double-sided foam tape (or hot glue on two corners). Connect jack − → `VIN−`, switch → `VIN+`, and the motor leads to `MOTOR+` / `MOTOR−`. Direction is set by motor polarity: swap the two motor wires if the plate turns the wrong way.
4. **Speed knob.** Mount the potentiometer in the 7 mm hole on the front-right (the small slot takes the anti-rotation tab). Wire its three pins to the board's pot pads with the same order the board's own pot used (outer-wiper-outer). If your board came with the pot on a lead, just plug it in.
5. **Motor.** Solder or crimp the two leads onto the motor tabs before you clamp it into the cradle; route them under the strap.

## Speed calibration

The pinion:gear ratio is 3:1, so plate RPM = motor RPM ÷ 3.

| Motor version | 100 % duty | ~40 % duty (typical lowest smooth speed for a worm gearbox) |
|---|---|---|
| JGY-370 10 RPM | 3.3 RPM (18 s/turn) | 1.3 RPM |
| **JGY-370 15 RPM (recommended)** | **5.0 RPM (12 s/turn)** | **2.0 RPM (30 s/turn)** |
| JGY-370 20 RPM | 6.7 RPM | 2.7 RPM |

Turn the knob down until the plate stalls, then back up a touch: that is the floor. Below ~30 % duty, brushed worm-gear motors cog and stall; if you want a lower floor use the 10 RPM motor.

## Notes
- Worm gearboxes are self-locking: with the switch off the plate stays put even if bumped. Do not force-turn the plate by hand with power off, it stresses the gearbox; lift the plate off the hub instead.
- Most PWM boards already have a flyback diode across the motor output. If yours does not, add a 1N5819 across the motor tabs, cathode (band) to +.
- Current draw is under 0.5 A; a 12 V 1 A adapter is plenty. Fuse optional (1 A polyfuse in the + lead).
