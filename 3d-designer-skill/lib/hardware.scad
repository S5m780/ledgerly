// hardware.scad — reference models of off-the-shelf parts used by 3d-designer-skill projects.
// These are ENVELOPES for cavities / clearance checks, not decorative models.
// Every dimension is a parameter: measure your part and override if it differs.

// ---------- JGY-370 12 V DC worm-gear motor (D-shaft 6 mm) ----------
// Orientation: output shaft points +Z from the gearbox top face, shaft axis at the origin.
// Motor body extends along +Y away from the gearbox.  Verify against your motor's drawing.
jgy_gb_len   = 37;    // gearbox length along the motor axis (Y)
jgy_gb_w     = 32;    // gearbox width (X)
jgy_gb_h     = 26;    // gearbox height along the output shaft (Z)  <-- sets the base height
jgy_shaft_from_end = 16; // shaft axis distance from the gearbox end face opposite the motor
jgy_body_d   = 24.4;  // "370" motor can diameter
jgy_body_len = 32;    // motor can length (excl. rear shaft / terminals)
jgy_shaft_d  = 6;     // D-shaft diameter
jgy_shaft_flat = 5.5; // across the flat
jgy_shaft_len = 14;   // shaft length above the gearbox face
jgy_term_len = 4;     // rear terminals / solder tabs

module jgy370(clearance = 0) {
    c = clearance;
    // gearbox: shaft at origin; box spans x ±w/2, y from -(shaft_from_end) to +(len - shaft_from_end)
    translate([-jgy_gb_w / 2 - c, -jgy_shaft_from_end - c, -jgy_gb_h - c])
        cube([jgy_gb_w + 2 * c, jgy_gb_len + 2 * c, jgy_gb_h + 2 * c]);
    // motor can, lying along +Y, its axis at the gearbox mid-height
    translate([0, jgy_gb_len - jgy_shaft_from_end - 0.01, -jgy_gb_h / 2])
        rotate([-90, 0, 0]) cylinder(d = jgy_body_d + 2 * c, h = jgy_body_len + jgy_term_len + c, $fn = 48);
    // output shaft (never add clearance; used for visual check only)
    cylinder(d = jgy_shaft_d, h = jgy_shaft_len, $fn = 24);
}

// ---------- 608 bearing (skate bearing) ----------
b608_od = 22; b608_id = 8; b608_w = 7; b608_inner_race_od = 12.1; b608_outer_race_id = 19.2;
module bearing608(clearance = 0) {
    difference() {
        cylinder(d = b608_od + 2 * clearance, h = b608_w, $fn = 64);
        translate([0, 0, -1]) cylinder(d = b608_id, h = b608_w + 2, $fn = 48);
    }
}

// ---------- Panel parts ----------
kcd1_cut = [13.2, 19.2];   // KCD1 rocker switch panel cutout (w x h)
pot_hole_d = 7.2;          // 6 mm shaft panel potentiometer (M7 bushing)
pot_key_w  = 3;            // anti-rotation tab slot
jack_hole_d = 12;          // DC-022B 5.5x2.1 barrel jack (M11 thread -> 12 mm hole; check yours)
pcb_bay = [60, 45, 18];    // generic PWM module bay (L x W x component height)
