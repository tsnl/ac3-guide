"""Timing goals and essential route objectives for each mission visit.

These compact checklist instructions do not promise an A rank. Full scoring,
optional-target and protection criteria remain in the linked rank reference.
All clocks are elapsed; + denotes time from the named event, and N/A means
no separate cutoff is cited.
"""


def step(time, clock, requirements):
    return dict(time=time, clock=clock, requirements=requirements)


def complete(requirements='All required targets'):
    return step('N/A', '', requirements)


MILESTONES = {
    1: [
        step('< 3:00', 'from mission start', '4× R-501'),
        step('After update', '', '1× R-101'),
    ],
    2: [
        step('< 4:00', 'from mission start', '8 radars'),
        step('After update', '', '4 bases + 1 bridge'),
    ],
    3: [
        step('During training', '', 'Follow Dision + destroy 6 practice targets'),
        step('After update', '', 'All required containers'),
    ],
    4: [
        step('< 3:00', 'from mission start', 'All initial required targets'),
        step('After update', '', 'All required reinforcements'),
    ],
    5: [
        step('< 3:00', 'from mission start', '4× F-15'),
        step('After update', '', '2× B-1C'),
    ],
    6: [
        step('During pursuit', '', 'Follow the recon plane below the canyon rim; do not shoot it'),
        step('After discovery', '', 'Destroy the secret base'),
    ],
    7: [
        step('< 3:30', 'from mission start', '4× A/F-117X'),
        step('< 5:00', 'same mission clock', '6× F/A-18I reinforcements'),
    ],
    8: [
        step('During escort', '', 'Protect the airship; clear its path'),
        step('<+30s', 'from hydrofoil appearance', 'Destroy the hydrofoil'),
    ],
    9: [step('< 3:00', 'from mission start', '5 required fighters')],
    10: [step('< 2:00', 'from mission start', 'All required targets')],
    11: [
        step('< 2:00', 'from mission start', '10 Antlions before landing'),
        step('After update', '', '3 required F/A-32Cs'),
    ],
    12: [step('< 5:00', 'from mission start', 'All required train cars; spare both neutral cars')],
    13: [step('< 4:30', 'from mission start', 'All nano-bites + allied-aircraft disinfection')],
    14: [step('< 9:00', 'from mission start', 'Destroy the armory; avoid radar detection')],
    15: [complete('All required targets; do not hit civilians')],
    16: [step('< 4:00', 'from mission start', 'All 12 fighters')],
    17: [complete('All required carrier targets')],
    18: [complete('All required targets + escape aircraft')],
    19: [step('< 3:00', 'from mission start', 'All grounded required aircraft before takeoff')],
    20: [
        step('Until 3:30', 'from mission start', 'Keep 1 initial required target alive'),
        step('<+45s', 'from hydrofoil appearance', 'All required targets, including hydrofoil'),
    ],
    21: [
        step('< 3:00', 'from mission start', 'Photograph all 4 hangars'),
        step('After update', '', 'All required reinforcements'),
    ],
    22: [step('< 5:00', 'from mission start', 'All power plants + core')],
    23: [complete()],
    24: [complete('6× R-531 Moburas')],
    25: [
        step('< 1:30', 'shuttle interception', 'Destroy the R-808 before landing'),
        step('After update', '', 'All remaining required targets'),
    ],
    26: [
        step('During escort', '', 'Protect the Antlions'),
        step('Before escape', '', 'Destroy the R-352'),
    ],
    27: [step('< 6:00', 'from mission start', 'All required bombing targets')],
    28: [step('< 9:00', 'from mission start', 'All required ships + submarines')],
    29: [complete()],
    30: [
        step('Before update', '', 'All required carrier targets'),
        step('<+3m', 'from X-49 appearance', 'Damage the X-49 until mission clear'),
    ],
    31: [step('< 4:00', 'from mission start', 'All required targets')],
    32: [complete('Both required targets')],
    33: [step('<+5m', 'from aircraft-control change', 'All remaining required targets')],
    34: [
        step('Before update', '', 'All required ground targets'),
        step('<+90s', 'from helicopter update', '3× V-22B'),
    ],
    35: [
        complete('All required submarine targets; protect the carrier'),
        step('Before impact', '', 'Intercept the cruise missile'),
    ],
    36: [complete('All required targets + escape aircraft')],
    37: [complete()],
    38: [step('< 3:00', 'from mission start', 'Both required phases')],
    39: [
        step('< 4:00', 'from mission start', '2× RF-12A2'),
        complete('All required targets + 3 oil tanks + 4 radars'),
    ],
    40: [step('< 3:00', 'from mission start', '7× F-22C; protect the shuttle')],
    41: [
        step('< 2:30', 'combat clock', 'All 4 satellites'),
        step('After combat', '', 'Complete re-entry alignment'),
    ],
    42: [complete('All required targets; protect the recovery units')],
    43: [complete('All required targets; avoid radar detection')],
    44: [complete()],
    45: [complete()],
    46: [step('< 3:00', 'from mission start', 'Damage the target until mission clear')],
    47: [step('< 5:30', 'from mission start', 'All required targets, including the generator')],
    48: [
        step('Before update', '', 'All initial required fighters'),
        step('<+90s', 'from carrier update', 'All 4 Sphyrna target points'),
    ],
    49: [step('< 4:00', 'from mission start', 'All required targets')],
    50: [complete('All required carrier targets')],
    51: [step('< 4:00', 'from mission start', 'Reach the tunnel exit')],
    52: [step('< 9:00', 'from mission start', 'Both required targets')],
}

# Scylla's post-combat choice is already shown in the Decision field.
# Lower-grade route visits must keep their different timing / target conditions.
ROUTE_MILESTONES = {
    (3, 7): [step('Opening choice', '', 'Return to base')],
    (5, 39): [MILESTONES[39][0], step('Before final TGT', '', 'All required targets; spare 1 oil tank or radar (D route)')],
    (8, 20): [step('< 3:30', 'from mission start', 'All initial required targets')],
    (9, 24): [step('Keith’s distress call', '', 'Destroy the R-311 pursuing Keith (D route)')],
    (12, 34): [step('>+90s', 'from helicopter update', 'Leave 1 escaping target alive')],
}
