// ============================================================================
//  Whatnot card-display turntable  v2 "crown drive"  —  slim right-angle version
//
//  Drive train:  GA12-N20 12 V gearmotor lying flat (shaft horizontal, radial)
//                ->  12T printed spur pinion (module 1)
//                ->  42T printed crown (face) gear on the vertical axis   (3.5:1)
//                ->  hex coupling  ->  plate hub  ->  plate.
//  Axis:         a FIXED printed post (or 8 mm steel rod).  The crown gear and the
//                plate hub each carry their own 608 bearing on that post; a spacer tube
//                between the inner races carries the plate weight down to the base.
//                Nothing rotates against printed plastic; the post never wears.
//  Electrical:   12 V jack -> rocker (spin/hold) -> PWM controller + knob -> motor.
//
//  Parts: base, lid, crown, pinion, hub, spacer, plate, motor_strap, card_easel,
//         assembly / exploded / section / gears / interference (views)
//  z = 0 is the underside of the base.  Every dimension is a parameter.
// ============================================================================
include <../../lib/gears.scad>
include <../../lib/hardware.scad>

part = "assembly";
ghost_hardware = true;
interference_pair = -1;

// ---------------- user-facing parameters ----------------
plate_d     = 210;    // H2S bed is 350 x 320: anything up to ~300 prints in one piece
plate_t     = 6;
plate_lip_h = 1.5;
plate_lip_w = 4;

base_d  = 165;           // 165 lets base + lid share one H2S plate
wall    = 2.4;
floor_t = 2.4;
lid_t   = 3;

gear_m        = 1;
pinion_teeth  = 12;
crown_teeth   = 42;      // 3.5:1  ->  20 RPM motor: 5.7 RPM max, ~2.3 RPM at 40 % duty
pinion_w      = 7;       // tooth width along the motor axis
pinion_hub_h  = 3;       // extra bore length on the gearbox side
crown_backlash = 0.2;
crown_disc_t  = 4;

axle    = "printed";     // "printed" post (no hardware) or "steel" 8 mm rod pressed into the floor
post_d  = 7.85;          // printed post diameter: 608 bore is 8.00, printed round posts come out ~+0.1
rod_d   = 8;

fit_tight = 0.15; fit_loose = 0.4;
m3_tap_d = 2.6; m3_clear_d = 3.4; m3_head_d = 6.4;
pcb_bay_size = [55, 40, 16];   // PWM module footprint (L x W x max component height)

$fn = 96;

// ---------------- derived layout ----------------
base_r = base_d / 2; inner_r = base_r - wall;
R      = crown_pitch_radius(crown_teeth, gear_m);   // 21
r_in   = R - 2.5; r_out = R + 3.5;                 // tooth radial span 18.5 .. 24.5
crown_od = 2 * (r_out + 1.5);

ring_z1   = floor_t + 1.5;                          // top of the inner-race ring on the floor
brgA_z0   = ring_z1;            brgA_z1 = brgA_z0 + b608_w;       // crown bearing
crown_z0  = brgA_z0;                                // crown bottom face (bearing flush)
crown_root  = crown_z0 + crown_disc_t;
crown_pitch = crown_root + 1.25 * gear_m;
crown_tip   = crown_root + crown_tooth_height(gear_m);
crown_pocket_top = brgA_z1 + 0.3;
crown_hub_top    = crown_pocket_top + 1.5;          // bridged ceiling over the bearing pocket
crown_hub_d = 28;
hex_af = 23.6; hex_h = 3;                           // drive hex on top of the crown
hex_z0 = crown_hub_top;

pinion_rp = gear_pitch_radius(pinion_teeth, gear_m);
pinion_ra = gear_outer_radius(pinion_teeth, gear_m);
motor_axis_z = crown_pitch + pinion_rp;             // 15.15
pinion_top   = motor_axis_z + pinion_ra;
pinion_r0 = r_in - 0.5; pinion_r1 = r_out + 0.5;    // teeth span along the motor axis
motor_face_r = pinion_r1 + pinion_hub_h + 0.5;      // gearbox face radius
motor_pos = [motor_face_r, 0, motor_axis_z];

hub_od = 34; hub_socket_af = hex_af + fit_loose; hub_socket_depth = hex_h + 0.3;
hub_z0   = hex_z0 + 0.3;
brgB_z0  = hub_z0 + hub_socket_depth;   brgB_z1 = brgB_z0 + b608_w;   // hub bearing
hub_ledge = 1;
lid_z0   = pinion_top + 1.0;  lid_z1 = lid_z0 + lid_t;                 // base height
lid_hole_d = hub_od + 2;
flange_d = 50; flange_t = 3;
flange_z0 = lid_z1 + 1.0;                           // 1 mm running gap above the lid
plate_z0 = flange_z0; plate_z1 = plate_z0 + plate_t;
total_h  = plate_z1 + plate_lip_h;
post_top = brgB_z1 + 0.5;
spacer_z0 = brgA_z1; spacer_z1 = brgB_z0;

strap_boss_dy = n20_w / 2 + 0.3 + 2 + 3.5;
cradle_x0 = motor_face_r - 1; cradle_x1 = motor_face_r + n20_len + n20_term_len + 2;
lid_screw_r = inner_r - 3.5; lid_screw_angles = [30, 90, 150, 210, 270, 330];
pcb_center = [-50, 0];
switch_x = -25; pot_x = 25; jack_x = -40;
panel_zc = floor_t + (lid_z0 - 2 - floor_t) / 2;   // centred between floor and lid lip

// ---------- checks ----------
motor_far = cradle_x1 + 1;
pcb_far = sqrt(pow(abs(pcb_center[0]) + pcb_bay_size[1] / 2 + 2, 2) + pow(pcb_bay_size[0] / 2 + 2, 2));
echo(str("CHECK base_height=", lid_z1, " total_height=", total_h, " plate_d=", plate_d, " base_d=", base_d));
echo(str("CHECK ratio=", crown_teeth / pinion_teeth, " crown_R=", R, " motor_axis_z=", motor_axis_z, " pinion_top=", pinion_top));
echo(str("CHECK motor_far_radius=", motor_far, " inner_r=", inner_r, " pcb_far_radius=", pcb_far, " crown_rim_gap=", abs(pcb_center[0]) - pcb_bay_size[1] / 2 - 2 - crown_od / 2));
echo(str("CHECK bearing_span=", (brgB_z0 + brgB_z1) / 2 - (brgA_z0 + brgA_z1) / 2, " post_top=", post_top));
echo(str("CHECK hex_corner=", hex_af / cos(30), " crown_hub_d=", crown_hub_d, " hub_wall=", (hub_od - hub_socket_af / cos(30)) / 2));
echo(str("CHECK panel_zc=", panel_zc, " panel_room=", lid_z0 - 2 - floor_t, " pcb_top=", floor_t + 1 + 1.6 + pcb_bay_size[2]));

// ============================================================================
module m3_boss(h, d = 7) { difference() { cylinder(d = d, h = h); translate([0, 0, h - 8]) cylinder(d = m3_tap_d, h = 9, $fn = 20); } }

module base() {
    difference() {
        union() {
            difference() { cylinder(r = base_r, h = lid_z0); translate([0, 0, floor_t]) cylinder(r = inner_r, h = lid_z0); }
            // axle: printed post (or a boss for the steel rod) + inner-race ring
            if (axle == "printed") cylinder(d = post_d, h = post_top, $fn = 64);
            cylinder(d = 12, h = ring_z1);
            for (a = lid_screw_angles) rotate(a) translate([lid_screw_r, 0, 0]) m3_boss(lid_z0);
            motor_cradle();
            translate([pcb_center[0], pcb_center[1], 0]) pcb_bay_walls();
        }
        if (axle == "steel") translate([0, 0, -1]) cylinder(d = rod_d - 0.2, h = ring_z1 + 2, $fn = 48);
        // panel: rocker (turned sideways to fit the low wall), pot, jack
        translate([switch_x, -base_r, panel_zc]) cube([kcd1_cut[1], 3 * wall, kcd1_cut[0]], center = true);
        translate([pot_x, -base_r, panel_zc]) rotate([90, 0, 0]) { cylinder(d = pot_hole_d, h = 3 * wall, center = true);
            translate([pot_hole_d / 2 + pot_key_w / 2, 0, 0]) cube([pot_key_w, 1.6, 3 * wall], center = true); }
        translate([jack_x, base_r, panel_zc]) rotate([90, 0, 0]) cylinder(d = jack_hole_d, h = 3 * wall, center = true);
        for (a = [45, 135, 225, 315]) rotate(a) translate([base_r - 14, 0, -0.01]) cylinder(d = 12.4, h = 0.8);
        translate(motor_pos) n20(clearance = 0.3);
    }
}

module motor_cradle() {
    pad_top = motor_axis_z - n20_h / 2;
    wall_top = motor_axis_z + n20_h / 2;
    // pad under the motor
    translate([cradle_x0, -(n20_w / 2 + 2.3), 0]) cube([cradle_x1 - cradle_x0, n20_w + 4.6, pad_top]);
    // side walls
    for (s = [-1, 1]) translate([cradle_x0 + 2, s > 0 ? n20_w / 2 + 0.3 : -(n20_w / 2 + 2.3), 0]) cube([cradle_x1 - cradle_x0 - 2, 2, wall_top]);
    // rear stop with a wire notch
    difference() {
        translate([cradle_x1 - 2, -(n20_w / 2 + 2.3), 0]) cube([2, n20_w + 4.6, wall_top]);
        translate([cradle_x1 - 3, -3, pad_top]) cube([4, 6, 20]);
    }
    // strap bosses
    for (s = [-1, 1]) translate([(cradle_x0 + cradle_x1) / 2, s * strap_boss_dy, 0]) m3_boss(wall_top);
}

module motor_strap() {
    // flat bar over the motor, screwed to the two cradle bosses (boss tops are level with the motor top)
    w = 8; t = 2.4; L = 2 * strap_boss_dy + 7;
    translate([(cradle_x0 + cradle_x1) / 2, 0, motor_axis_z + n20_h / 2]) difference() {
        translate([-w / 2, -L / 2, 0]) cube([w, L, t]);
        for (s = [-1, 1]) translate([0, s * strap_boss_dy, -1]) cylinder(d = m3_clear_d, h = 10, $fn = 20);
    }
}

module pcb_bay_walls() {
    L = pcb_bay_size[0]; W = pcb_bay_size[1]; h = 6; t = 2;
    difference() {
        translate([-(W / 2 + t), -(L / 2 + t), 0]) cube([W + 2 * t, L + 2 * t, h]);
        translate([-W / 2, -L / 2, -1]) cube([W, L, h + 2]);
        for (s = [-1, 1]) translate([s * (W / 2 + t), 0, h - 2]) cube([2 * t + 1, 8, 5], center = true);
    }
}

module lid() {
    difference() {
        union() {
            translate([0, 0, lid_z0]) cylinder(r = base_r, h = lid_t);
            translate([0, 0, lid_z0 - 2]) difference() {
                cylinder(r = inner_r - fit_loose / 2, h = 2);
                translate([0, 0, -1]) cylinder(r = inner_r - fit_loose / 2 - 2, h = 4);
                for (a = lid_screw_angles) rotate(a) translate([lid_screw_r, 0, -1]) cylinder(d = 7 + fit_loose, h = 4);
            }
        }
        translate([0, 0, lid_z0 - 1]) cylinder(d = lid_hole_d, h = 10);
        for (a = lid_screw_angles) rotate(a) translate([lid_screw_r, 0, lid_z0 - 1]) {
            cylinder(d = m3_clear_d, h = 10, $fn = 20);
            translate([0, 0, 1 + lid_t - 1.8]) cylinder(d1 = m3_clear_d, d2 = m3_head_d, h = 1.8, $fn = 24);
        }
        for (i = [-1, 0, 1]) translate([motor_pos[0] + 15, i * 6, lid_z0 - 1]) cube([20, 2, 10], center = true);   // vents over the motor
    }
}

module crown() {
    translate([0, 0, crown_z0]) difference() {
        union() {
            crown_gear(crown_teeth, gear_m, disc_t = crown_disc_t, r_in = r_in, r_out = r_out, backlash = crown_backlash);
            cylinder(d = crown_hub_d, h = crown_hub_top - crown_z0);
            translate([0, 0, crown_hub_top - crown_z0]) cylinder(d = hex_af / cos(30), h = hex_h, $fn = 6);
        }
        // bearing pocket from below (opens at the bed when printed teeth-up), 1.5 mm bridged ceiling
        translate([0, 0, -1]) cylinder(d = b608_od + fit_tight, h = 1 + b608_w + 0.3);
        translate([0, 0, -1]) cylinder(d = 11, h = 30);   // spacer / post clearance
    }
}

module pinion() {
    translate(motor_pos) rotate([0, -90, 0]) translate([0, 0, pinion_hub_h + 0.5]) rotate([0, 0, 180 / pinion_teeth])   // half-pitch phase: gap faces the crown tooth
        involute_gear(pinion_teeth, gear_m, pinion_w, backlash = 0.1, bore = n20_shaft_d - 0.05, bore_flat = n20_shaft_flat - 0.05,
                      hub_d = 7, hub_h = 0, chamfer = 0.3);
    // hub on the gearbox side (extra bore length)
    translate(motor_pos) rotate([0, -90, 0]) translate([0, 0, 0.5]) difference() {
        cylinder(d = 7, h = pinion_hub_h + 0.01, $fn = 32);
        translate([0, 0, -1]) d_bore(n20_shaft_d - 0.05, n20_shaft_flat - 0.05, 10);
    }
}

module hub() {
    difference() {
        union() {
            translate([0, 0, hub_z0]) cylinder(d = hub_od, h = flange_z0 - hub_z0 + 0.01);
            translate([0, 0, flange_z0]) cylinder(d = flange_d, h = flange_t);
        }
        translate([0, 0, hub_z0 - 1]) cylinder(d = hub_socket_af / cos(30), h = 1 + hub_socket_depth, $fn = 6);   // hex socket
        translate([0, 0, hub_z0 - 1]) cylinder(d = b608_od + fit_tight, h = 1 + hub_socket_depth + b608_w);        // bearing, inserted from below
        translate([0, 0, hub_z0 - 1]) cylinder(d = 18, h = 60);                                                    // post clearance / ledge hole
        for (a = [0, 120, 240]) rotate(a) translate([20, 0, flange_z0 - 1]) cylinder(d = m3_tap_d, h = 10, $fn = 20);
    }
}

module spacer() {
    translate([0, 0, spacer_z0]) difference() { cylinder(d = 10, h = spacer_z1 - spacer_z0, $fn = 48); translate([0, 0, -1]) cylinder(d = post_d + 0.5, h = 20, $fn = 48); }
}

module plate() {
    Rr = plate_d / 2; c = 0.6;
    profile = plate_lip_h > 0
        ? [[0, 0], [Rr, 0], [Rr, plate_t + plate_lip_h - c], [Rr - c, plate_t + plate_lip_h], [Rr - plate_lip_w, plate_t + plate_lip_h], [Rr - plate_lip_w, plate_t], [0, plate_t]]
        : [[0, 0], [Rr, 0], [Rr, plate_t - c], [Rr - c, plate_t], [0, plate_t]];
    difference() {
        translate([0, 0, plate_z0]) rotate_extrude($fn = 180) polygon(profile);
        translate([0, 0, plate_z0 - 1]) cylinder(d = flange_d + fit_loose, h = flange_t + 1);
        for (a = [0, 120, 240]) rotate(a) translate([20, 0, plate_z0 - 1]) {
            cylinder(d = m3_clear_d, h = 20, $fn = 20);
            translate([0, 0, 1 + plate_t - 1.8]) cylinder(d1 = m3_clear_d, d2 = m3_head_d, h = 1.81, $fn = 24);
        }
    }
}

module card_easel() {
    w = 90; d = 34; h = 12; tilt = 15;
    difference() {
        hull() { translate([-w / 2, -d / 2, 0]) cube([w, d, 2]); translate([-w / 2, -d / 2 + 6, 0]) cube([w, d - 6, h]); }
        translate([0, 2, h]) rotate([tilt, 0, 0]) translate([-42, -2.2, -9]) cube([84, 4.4, 20]);
        translate([0, -8, h]) rotate([tilt, 0, 0]) translate([-42, -1.1, -9]) cube([84, 2.2, 20]);
    }
}

// ============================================================================
module hardware_solid() {
    color("DimGray") translate(motor_pos) n20();
    color("Silver") translate([0, 0, brgA_z0]) bearing608();
    color("Silver") translate([0, 0, brgB_z0]) bearing608();
    if (axle == "steel") color("Silver") translate([0, 0, 0.5]) cylinder(d = rod_d, h = post_top - 0.5, $fn = 32);
}
module hardware_ghosts() { if (ghost_hardware) %hardware_solid(); else hardware_solid(); }

module assembly(e = 0) {
    color("SlateGray") base();
    color("SlateGray") translate([0, 0, e * 0.5]) motor_strap();
    color("Gold") translate([0, 0, e * 0.3]) crown();
    color("Gold") translate([0, 0, e * 0.3]) pinion();
    color("Tomato") translate([0, 0, e * 0.6]) spacer();
    color("LightSteelBlue", 0.85) translate([0, 0, e]) lid();
    color("Tomato") translate([0, 0, e * 1.4]) hub();
    color("WhiteSmoke") translate([0, 0, e * 1.8]) plate();
    color("WhiteSmoke") translate([0, 40, plate_z1 + plate_lip_h + e * 2.2]) card_easel();
    hardware_ghosts();
}

if (part == "assembly") assembly();
else if (part == "exploded") assembly(e = 22);
else if (part == "section") difference() { assembly(); translate([-200, 0, -1]) cube([400, 400, 100]); }
else if (part == "gears") { crown(); pinion(); }
else if (part == "interference") {
    pairs = [["crown/pinion", 0], ["crown/base", 1], ["pinion/base", 2], ["pinion/lid", 3], ["crown/hub", 4],
             ["hub/lid", 5], ["base/lid", 6], ["motor/base", 7], ["motor/lid", 8], ["spacer/crown", 9],
             ["spacer/hub", 10], ["crown/lid", 11], ["hub/plate_screwspace", 12], ["strap/lid", 13], ["bearingB/hub", 14]];
    for (i = [0 : len(pairs) - 1]) if (interference_pair < 0 || interference_pair == i) {
        echo(str("INTERFERENCE pair ", i, " = ", pairs[i][0]));
        if (i == 0) intersection() { crown(); pinion(); }
        if (i == 1) intersection() { crown(); base(); }
        if (i == 2) intersection() { pinion(); base(); }
        if (i == 3) intersection() { pinion(); lid(); }
        if (i == 4) intersection() { crown(); hub(); }
        if (i == 5) intersection() { hub(); lid(); }
        if (i == 6) intersection() { base(); lid(); }
        if (i == 7) intersection() { base(); translate(motor_pos) n20(); }
        if (i == 8) intersection() { lid(); translate(motor_pos) n20(); }
        if (i == 9) intersection() { spacer(); crown(); }
        if (i == 10) intersection() { spacer(); hub(); }
        if (i == 11) intersection() { crown(); lid(); }
        if (i == 12) intersection() { hub(); translate([0, 0, brgA_z0]) bearing608(); }
        if (i == 13) intersection() { motor_strap(); lid(); }
        if (i == 14) intersection() { translate([0, 0, brgB_z0]) bearing608(); hub(); }
    }
}
else if (part == "base") base();
else if (part == "lid") translate([0, 0, lid_z1]) mirror([0, 0, 1]) lid();            // top face down
else if (part == "crown") translate([0, 0, -crown_z0]) crown();                      // teeth up, bearing pocket at the bed
else if (part == "pinion") pinion_flat();
else if (part == "hub") translate([0, 0, flange_z0 + flange_t]) mirror([0, 0, 1]) hub();   // flange down, pockets open up
else if (part == "spacer") translate([0, 0, -spacer_z0]) spacer();
else if (part == "plate") translate([0, 0, -plate_z0]) plate();
else if (part == "motor_strap") translate([0, 0, -(motor_axis_z + n20_h / 2)]) translate([-(cradle_x0 + cradle_x1) / 2, 0, 0]) motor_strap();
else if (part == "card_easel") card_easel();

// pinion laid flat for printing: hub side down
module pinion_flat() {
    translate([0, 0, 0]) rotate([0, 0, 0]) {
        // rebuild in local coordinates: axis along z, hub at the bottom
        difference() {
            union() {
                cylinder(d = 7, h = pinion_hub_h, $fn = 32);
                translate([0, 0, pinion_hub_h]) involute_gear(pinion_teeth, gear_m, pinion_w, backlash = 0.1, chamfer = 0.3);
            }
            translate([0, 0, -1]) d_bore(n20_shaft_d - 0.05, n20_shaft_flat - 0.05, 20);
        }
    }
}
