// gears.scad — involute spur gear library for FDM printing
// Part of 3d-designer-skill (MIT). All units mm, angles degrees (OpenSCAD).
//
// involute_gear(teeth, m, thickness, ...)  — spur gear, tooth profile is a true involute
// gear_pitch_radius(teeth, m)             — helper
// gear_outer_radius(teeth, m)             — helper
// gear_center_distance(t1, t2, m)         — helper for placing a gear pair

function gear_pitch_radius(teeth, m)  = m * teeth / 2;
function gear_base_radius(teeth, m, pa = 20) = gear_pitch_radius(teeth, m) * cos(pa);
function gear_outer_radius(teeth, m)  = gear_pitch_radius(teeth, m) + m;          // addendum = 1.0 m
function gear_root_radius(teeth, m, clearance = 0.25) = gear_pitch_radius(teeth, m) - (1 + clearance) * m;
function gear_center_distance(t1, t2, m) = m * (t1 + t2) / 2;

// involute function inv(a) = tan(a) - a, with a in degrees, result in radians
function _inv(a) = tan(a) - a * PI / 180;
function _rad(a) = a * PI / 180;
function _deg(r) = r * 180 / PI;

// polar angle (deg) of the flank point at radius r, measured from the tooth centre line
function _flank_angle(r, rb, rp, pa, half_thick_rad) =
    _deg(half_thick_rad + _inv(pa) - _inv(acos(min(1, rb / r))));

module _tooth2d(teeth, m, pa, backlash, clearance, steps = 12) {
    rp = gear_pitch_radius(teeth, m);
    rb = gear_base_radius(teeth, m, pa);
    ra = gear_outer_radius(teeth, m);
    rr = gear_root_radius(teeth, m, clearance);
    r0 = max(rb, rr);                          // involute starts at the base circle
    half_thick = PI / (2 * teeth) - backlash / (2 * rp);   // radians at pitch circle
    // right flank, root -> tip
    right = [ for (i = [0 : steps]) let(r = r0 + (ra - r0) * i / steps, a = _flank_angle(r, rb, rp, pa, half_thick))
              [ r * cos(a), -r * sin(a) ] ];
    // left flank, tip -> root
    left  = [ for (i = [steps : -1 : 0]) let(r = r0 + (ra - r0) * i / steps, a = _flank_angle(r, rb, rp, pa, half_thick))
              [ r * cos(a), r * sin(a) ] ];
    a0 = _flank_angle(r0, rb, rp, pa, half_thick);
    // extend the flank radially down to the root circle when the base circle is above it
    root_r = [ [ (rr - 0.5) * cos(a0), -(rr - 0.5) * sin(a0) ] ];
    root_l = [ [ (rr - 0.5) * cos(a0),  (rr - 0.5) * sin(a0) ] ];
    polygon(concat(root_r, right, left, root_l));
}

module involute_gear2d(teeth, m, pa = 20, backlash = 0.1, clearance = 0.25) {
    rr = gear_root_radius(teeth, m, clearance);
    union() {
        circle(r = rr, $fn = max(48, teeth * 4));
        for (i = [0 : teeth - 1]) rotate(i * 360 / teeth) _tooth2d(teeth, m, pa, backlash, clearance);
    }
}

// Full 3D spur gear.
//  bore        : through-hole diameter (0 = solid)
//  bore_flat   : distance across the D-flat (0 = round bore).  e.g. 5.5 for a 6 mm D-shaft
//  hub_d/hub_h : optional hub cylinder on top (hub_h = 0 disables)
//  chamfer     : small edge chamfer on tooth tips for easy meshing after printing
module involute_gear(teeth, m, thickness = 8, pa = 20, backlash = 0.1, clearance = 0.25,
                     bore = 0, bore_flat = 0, hub_d = 0, hub_h = 0, chamfer = 0.4, grub_d = 0) {
    ra = gear_outer_radius(teeth, m);
    difference() {
        union() {
            // gear body; tip chamfer top & bottom via intersection with a revolved envelope (never hull(): it fills the tooth gaps)
            if (chamfer > 0) {
                intersection() {
                    linear_extrude(thickness) involute_gear2d(teeth, m, pa, backlash, clearance);
                    rotate_extrude($fn = max(96, teeth * 4)) polygon([[0, 0], [ra - chamfer, 0], [ra + 0.01, chamfer], [ra + 0.01, thickness - chamfer], [ra - chamfer, thickness], [0, thickness]]);
                }
            } else {
                linear_extrude(thickness) involute_gear2d(teeth, m, pa, backlash, clearance);
            }
            if (hub_h > 0) cylinder(d = hub_d, h = thickness + hub_h, $fn = 64);
        }
        if (bore > 0) translate([0, 0, -1]) d_bore(bore, bore_flat, thickness + hub_h + 2);
        if (grub_d > 0 && hub_h > 0)   // radial grub screw through the hub
            translate([0, 0, thickness + hub_h / 2]) rotate([0, 90, 0]) cylinder(d = grub_d, h = hub_d, $fn = 24);
    }
}

// D-shaped bore: diameter d, `flat` = distance across the flat (0 = round).
// The flat is at y = flat - d/2 (material kept on the +y side of the shaft is removed).
module d_bore(d, flat = 0, h = 10) {
    if (flat > 0) {
        intersection() {
            cylinder(d = d, h = h, $fn = 48);
            translate([-d, -d, 0]) cube([2 * d, flat + d / 2, h]);
        }
    } else {
        cylinder(d = d, h = h, $fn = 48);
    }
}
