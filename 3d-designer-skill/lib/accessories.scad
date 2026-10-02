// accessories.scad — display accessories shared by the turntable projects.

// ---------------------------------------------------------------------------
// card_easel: centred stand for ONE sleeved trading card (63 x 88 card, ~66.5 x 91 x 0.5–1 mm in a
// penny sleeve; a 2.3 mm toploader also fits).  Round base drops into a matching recess in the plate
// so the card sits exactly on the rotation axis.  The slot and the back-rest lean back by `lean`
// degrees so the card faces slightly up toward a camera in front of it.
//   slot_w     3.2  : sleeved card or toploader; the card rests against the back wall, so it never flops
//   slot_depth 20   : how far the card sinks in (holds it against knocks; leaves the art visible)
//   lip_h      10   : front lip height above the slot floor (hides only the bottom of the card)
//   center_hole     : clearance hole for a hub boss on the plate (v1 turntable) — 0 for a flat plate
// Prints flat, no supports (12° lean on the front face is well under the overhang limit).
// ---------------------------------------------------------------------------
module card_easel(base_d = 96, base_t = 2, slot_len = 70, slot_w = 3.2, slot_depth = 20, lean = 12,
                  block_w = 78, back_d = 11, front_d = 5, lip_h = 10, floor_t = 3, center_hole = 0) {
    H = base_t + floor_t + slot_depth + 2;             // back-rest height
    difference() {
        union() {
            cylinder(d = base_d, h = base_t, $fn = 120);
            // leaning block: bottom rectangle to top rectangle shifted back by H*tan(lean)
            hull() {
                translate([-block_w / 2, -back_d, 0]) cube([block_w, back_d + front_d, 0.01]);
                translate([-block_w / 2, -back_d - H * tan(lean), H - 0.01]) cube([block_w, back_d + front_d, 0.01]);
            }
        }
        // the slot, tilted about its floor line, centred on the axis
        translate([0, 0, base_t + floor_t]) rotate([lean, 0, 0]) translate([-slot_len / 2, -slot_w / 2, 0]) cube([slot_len, slot_w, 80]);
        // everything in front of the slot above the lip is removed (leaves a low front lip, tall back-rest)
        translate([0, 0, base_t + floor_t]) rotate([lean, 0, 0]) translate([-100, slot_w / 2 + 2.4, lip_h]) cube([200, 100, 100]);
        // rounded finger notch in the middle of the lip so the card is easy to grab
        translate([0, front_d + 2, base_t + floor_t + lip_h]) rotate([90, 0, 0]) cylinder(d = 18, h = 30, $fn = 48);
        if (center_hole > 0) translate([0, 0, -1]) cylinder(d = center_hole, h = base_t + 2, $fn = 48);
    }
}
