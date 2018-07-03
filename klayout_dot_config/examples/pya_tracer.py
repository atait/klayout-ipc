''' Automatically launches a subprocess klayout and drops into debug shell
'''

import lyipc.client as ipc
import os
import time
import numpy as np
from functools import partial

import pya
import sys
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)

debug_file = os.path.realpath('debuglobal.gds')

layout = pya.Layout()
dbu = layout.dbu = 0.001
TOP = layout.create_cell('TOP')
l1 = layout.insert_layer(pya.LayerInfo(1, 0))
l2 = layout.insert_layer(pya.LayerInfo(2, 0))


def intercept_pyainsert(write_load_delay=0.01):
    pya.Shapes.old_insert = pya.Shapes.insert
    def new_insert(self, *args, **kwargs):
        retval = pya.Shapes.old_insert(self, *args, **kwargs)
        layout.write(debug_file)
        time.sleep(write_load_delay)
        ipc.load(debug_file)
        return retval
    pya.Shapes.insert = new_insert


def simple_create():
    intercept_pyainsert(0.02)

    for i in range(21):
        for j in range(21):
            box = pya.DBox(0, 0, 10, 10)
            box.move(15 * i, 15 * j)
            TOP.shapes(l1).insert(box)
    TOP.shapes(l2).insert(pya.DBox(0,0,500,500))


def tough_create():
    intercept_pyainsert(1e-4)

    for i in range(51):
        for j in range(51):
            box = pya.DBox(0, 0, 10, 10)
            box.move(15 * i, 15 * j)
            TOP.shapes(l1).insert(box)
    TOP.shapes(l2).insert(pya.DBox(0,0,1000,1000))


tough_create()


def main_create():
    dbu = layout.dbu = 0.001
    TOP = layout.create_cell('TOP')
    lsi = layout.insert_layer(pya.LayerInfo(22, 0))
    lsip = layout.insert_layer(pya.LayerInfo(3, 0))
    lsin = layout.insert_layer(pya.LayerInfo(4, 0))
    lsipp = layout.insert_layer(pya.LayerInfo(1, 0))
    lsinp = layout.insert_layer(pya.LayerInfo(2, 0))
    lvc = layout.insert_layer(pya.LayerInfo(31, 0))
    lv2 = layout.insert_layer(pya.LayerInfo(32, 0))
    lm1 = layout.insert_layer(pya.LayerInfo(14, 0))
    lm2 = layout.insert_layer(pya.LayerInfo(16, 0))
    origin = pya.DPoint(0, 0)
    ex = pya.DPoint(1, 0)

    from SiEPIC.utils.layout import layout_ring, layout_waveguide, layout_arc2, layout_disk, layout_section
    radius = 10
    width = 0.5
    gap = .2
    ring_center = origin
    layout_ring(TOP, lsi, ring_center, radius, width)
    y = radius + width + gap
    x = radius * 2
    for ySign in [-1, 1]:
        layout_waveguide(TOP, lsi, [pya.DPoint(-x, y * ySign), pya.DPoint(x, y * ySign)], width)

    # Layout doping layers
    r_offset = 0.  # a few nanometers
    safe_distance = .6  # safe distance between edge of waveguide and doped region
    doped_contact_width = 4

    N_doped_inner_radius = radius + r_offset
    Np_doped_inner_radius = N_doped_inner_radius + width / 2 + safe_distance  # safe gap for N+
    Npp_doped_inner_radius = Np_doped_inner_radius + 0.25
    N_doped_outer_radius = N_doped_inner_radius + doped_contact_width
    Np_doped_outer_radius = N_doped_outer_radius
    Npp_doped_outer_radius = N_doped_outer_radius

    Ndoped_angles = (np.pi / 18 - np.pi / 2, 0)
    inverted_Ndoped_angles = (np.pi - Ndoped_angles[1], np.pi - Ndoped_angles[0])
    doping_safe_bounds = (-radius - width / 2 + safe_distance, radius - (-width / 2 + safe_distance))
    # Si N, Np and Npp
    arcs = [(N_doped_inner_radius, N_doped_outer_radius, lsin),
            (Npp_doped_inner_radius, Npp_doped_outer_radius, lsinp)]
    for r1, r2, layer in arcs:
        dpoly = layout_arc2(TOP, layer, ring_center, r1,
                            r2, *Ndoped_angles, ex, y_bounds=doping_safe_bounds)
        dpoly2 = layout_arc2(TOP, layer, ring_center, r1,
                             r2, *inverted_Ndoped_angles, ex, y_bounds=doping_safe_bounds)
    npp_mod_dpoly_right = dpoly
    npp_mod_dpoly_left = dpoly2

    Si_VC_inclusion = 0.2 + 0.05
    VC_M1_inclusion = 0.4 + 0.05
    VC_min_width = 1.5 + 0.05
    M1_M1_exclusion = 1.2 + 0.05

    P_doped_outer_radius = radius + r_offset
    Pp_doped_outer_radius = P_doped_outer_radius - width / 2 - safe_distance  # safe gap for N+
    Ppp_doped_outer_radius = Pp_doped_outer_radius - 0.25
    P_doped_inner_radius = Ppp_doped_outer_radius - Si_VC_inclusion * 2 - VC_min_width
    Pp_doped_inner_radius = P_doped_inner_radius
    Ppp_doped_inner_radius = P_doped_inner_radius

    # Si P, Pp and Ppp
    Pdoped_angles = (-np.pi - Ndoped_angles[1], Ndoped_angles[1])
    arcs = [(P_doped_inner_radius, P_doped_outer_radius, lsip),
            (Ppp_doped_inner_radius, Ppp_doped_outer_radius, lsipp)]
    for r1, r2, layer in arcs:
        dpoly = layout_arc2(TOP, layer, ring_center, r1,
                            r2, *Pdoped_angles, ex, y_bounds=doping_safe_bounds)
    ppp_mod_dpoly = dpoly

    # **** Vias to M1

    def make_shape_from_dpolygon(dpoly, resize_dx, layer):
        dbu = 0.001
        dpoly.resize(resize_dx, dbu)
        # if resize_dx > dbu:
        #     dpoly.round_corners(resize_dx, 100)
        dpoly.layout(TOP, layer)
        return dpoly

    make_via_from_arc_dpolygon = partial(make_shape_from_dpolygon,
                                         resize_dx=-VC_M1_inclusion,
                                         layer=lvc)

    # P-side Modulator
    ppp_doped_via = make_shape_from_dpolygon(ppp_mod_dpoly,
                                             resize_dx=-Si_VC_inclusion,
                                             layer=lvc)

    # N-side Modulator
    make_via_from_arc_dpolygon(npp_mod_dpoly_left)
    make_via_from_arc_dpolygon(npp_mod_dpoly_right)

    # **** M1
    make_m1_from_via_dpolygon = partial(make_shape_from_dpolygon,
                                        resize_dx=VC_M1_inclusion,
                                        layer=lm1)
    # make_m1_from_via_dpolygon(n_doped_inner_via)
    # make_m1_from_via_dpolygon(n_doped_outer_via)

    # M1 modulator N
    arcs = [(Npp_doped_inner_radius, Npp_doped_outer_radius, lsinp)]
    for r1, r2, layer in arcs:
        dpoly = layout_arc2(TOP, lm1, ring_center, r1,
                            r2, inverted_Ndoped_angles[0] - 2 * np.pi, Ndoped_angles[1], ex)

    # M1 modulator P
    dpoly = layout_section(TOP, lm1, ring_center, Ppp_doped_outer_radius,
                           *Pdoped_angles, ex)
    m1_disk_radius = 7 - 2.01 + VC_M1_inclusion
    dpoly = layout_disk(TOP, lm1, ring_center,
                        m1_disk_radius)
    make_m1_from_via_dpolygon(ppp_doped_via)

    M1_VL_inclusion = 1.5 + 0.05
    VL_VC_exclusion = 2
    VL_ML_inclusion = 2
    VL_min_width = 2

    # **** Vias to M2
    VL_section_radius = Ppp_doped_inner_radius + Si_VC_inclusion - VL_VC_exclusion
    VL_section_angles = (Pdoped_angles[0] + np.arcsin(M1_VL_inclusion / VL_section_radius),
                         Pdoped_angles[1] - np.arcsin(M1_VL_inclusion / VL_section_radius))

    p_via_dpolygon_list = list()
    p_via_dpolygon_list.append(layout_section(TOP, None, ring_center, VL_section_radius,
                                              *VL_section_angles, ex))
    if m1_disk_radius - M1_VL_inclusion > VL_min_width / 2:
        p_via_dpolygon_list.append(layout_disk(TOP, None, ring_center,
                                               m1_disk_radius - M1_VL_inclusion))
    else:
        pass
    dpolys = pya.EdgeProcessor().simple_merge_p2p(
        [dpoly.to_itype(layout.dbu) for dpoly in p_via_dpolygon_list], False, False, 1)
    dpoly = dpolys[0].to_dtype(layout.dbu)  # pya.DPolygon
    dpoly = DSimplePolygon(list(dpoly.each_point_hull()))
    TOP.shapes(lv2).insert(dpoly)

    # # M1 traces

    # via_default_dict = {k: getattr(cp, k)
    #                     for k in ("angle_ex", "ML", "M1", "VL")}

    elec_port_clearance = 15
    port_width = 10
    port_via_width = 5  # pylint: disable=unused-variable

    # heater ports

    # lh_port_position = ring_center - (0.5 * port_width + 1.5) * ex + \
    #     (drop_bus_wg_height + elec_port_clearance - port_width / 2) * ey

    # ViaMLM1("left_heater_port").place_cell(TOP, lh_port_position,
    #                                        params=dict(via_default_dict, ml_width=port_width))

    # rh_port_position = ring_center + (0.5 * port_width + 1.5) * ex + \
    #     (drop_bus_wg_height + elec_port_clearance - port_width / 2) * ey

    # ViaMLM1("right_heater_port").place_cell(TOP, rh_port_position,
    #                                         params=dict(via_default_dict, ml_width=port_width))

    # p_modulator port

    layout_disk(TOP, lm2, ring_center,
                VL_section_radius + VL_ML_inclusion)
    p_mod_port_position = ring_center

    # n_modulator port

    # n_mod_port_position = ring_center - main_bus_wg_height * ey - port_width * ey / 2

    # ViaMLM1("n_modulator_port").place_cell(TOP, n_mod_port_position,
    #                                        params=dict(via_default_dict, ml_width=port_width))


# main_create()
