"""Visit-specific play instructions, separating clocks from targets and A-rank cleanup.

The numerical A thresholds come from each mission's cited article. The ordering
of optional kills is a play plan: collect them before clearing a phase's last TGT.
Initial-wave kill budgets for 01, 02 and 05 are derived from the official guide's
unit lists (pp. 42, 44, 50) and the total A-rank thresholds. They are not additional
hidden rank conditions. See ranks.html#credits for sources.
"""


def step(time, clock, required, optional, total=''):
    return dict(time=time, clock=clock, required=required, optional=optional, total=total)


def total_step(count, required='Complete the remaining required targets.', optional='Destroy optional enemies before the last TGT to reach the total.'):
    return step('By completion', 'no separate A cutoff published', required, optional, f'{count}+ destroyed, required + optional combined.')


MILESTONES = {
    1: [
        step('< 3:00', 'from mission start', 'Destroy the 4 required R-501s.', 'Plan: take at least 2 initial optional aircraft before the last R-501.'),
        step('By completion', 'second wave', 'Destroy the final required R-101.', '5+ optional aircraft across both waves; take the remaining optional kills before the final TGT.', '10+ aircraft overall, including the 5 required aircraft.'),
    ],
    2: [
        step('< 4:00', 'from mission start', 'Destroy all 8 radar sites.', 'Take at least 10 of the 11 optional aircraft / GUN / MSSL units before the last radar.'),
        step('After update', 'before finishing', 'Destroy the 4 bases and the bridge.', 'No extra cleanup remains if you took 10 optional units in phase one.', '23+ destroyed overall: 13 required + 10 optional.'),
    ],
    3: [
        step('Before update', 'training phase', 'Earn 5,000+ points: 1,800 from the 6 practice targets and 3,200+ from following Dision closely.', 'No extra enemy kills required.'),
        step('After update', 'interception phase', 'Destroy the required containers and finish.', 'No extra enemy kills required.'),
    ],
    4: [
        step('< 3:00', 'from mission start', 'Destroy the initial required ship targets to trigger reinforcements.', 'Collect optional kills toward the 23 total before clearing the initial wave.'),
        total_step(23, 'Destroy the reinforcement targets.'),
    ],
    5: [
        step('< 3:00', 'from mission start', 'Destroy all 4 required F-15s to trigger the bombers.', 'Plan: take at least 2 initial optional fighters before the last F-15.'),
        step('By completion', 'bomber phase', 'Destroy both required B-1Cs.', '5+ optional fighters across both waves; finish needed escorts before the final bomber.', '11+ aircraft overall, including the 6 required aircraft.'),
    ],
    6: [
        step('During pursuit', '', 'Follow the recon plane below the canyon rim; do not shoot it. Discover the secret base.', 'No cleanup needed during the pursuit.'),
        total_step(8, 'Destroy the secret base to open No Clearance.', 'Destroy optional base enemies before the last TGT to reach the total.'),
    ],
    7: [
        step('< 3:30', 'from mission start', 'Shoot down all 4 initial A/F-117Xs.', 'None required for this milestone.'),
        step('< 5:00', 'same mission clock', 'Shoot down all 6 reinforcement F/A-18Is.', 'None required; this is a timed combat clear.'),
    ],
    8: [
        step('Before escape', 'airship escort', 'Protect the airship and clear the structures blocking its path.', 'No extra kill total required.'),
        step('< 0:30', 'from hydrofoil appearance', 'Sink the escaping hydrofoil.', 'No extra kills required.'),
    ],
    9: [step('< 3:00', 'from mission start', 'Shoot down all 5 initial required fighters.', 'None required for A; the later story choice is separate.')],
    10: [step('< 2:00', 'from mission start', 'Intercept the required high-altitude targets and finish.', 'No extra kills required.')],
    11: [
        step('< 2:00', 'Antlion phase', 'Destroy all 10 required Antlions before they land.', 'Collect optional escorts toward the 18 total before clearing this phase.'),
        total_step(18, 'Destroy the reinforcement targets.', 'Take additional optional fighters before the final TGT to reach the total.'),
    ],
    12: [step('< 5:00', 'from mission start', 'Destroy the target train cars; spare both neutral cars.', 'Shoot escort aircraft before the final required car to reach the total.', '10+ enemies overall.')],
    13: [step('< 4:30', 'from mission start', 'Eradicate the nano-bites and disinfect the allied aircraft with the special bombs.', 'No extra kills required.')],
    14: [step('< 9:00', 'from mission start', 'Destroy the armory without radar detection. Climb to the safe altitude whenever jamming stops.', 'No extra kills required.')],
    15: [total_step(22, 'Finish both hostile waves without hitting civilian aircraft.', 'Collect optional hostile kills before the last TGT; spare the news helicopters.')],
    16: [step('< 4:00', 'from mission start', 'Shoot down all 12 hostile fighters.', 'Every fighter must be destroyed; no additional cleanup.')],
    17: [step('Before final TGT', 'no separate A cutoff published', 'Finish the carrier after clearing the fighters.', 'Destroy all 12 optional fighters: 9 XFA-36As and 3 R-103s.')],
    18: [total_step(21, 'Destroy the final escape aircraft after collecting enough kills.')],
    19: [step('< 3:00', 'from mission start', 'Destroy all grounded required aircraft before takeoff.', 'Take optional enemies before the final TGT to reach the total.', '15+ enemies overall.')],
    20: [
        step('Until 3:30', 'from mission start', 'Keep at least one initial required target alive so the hydrofoil launches.', 'Collect optional enemies toward the 24 total while waiting.'),
        step('< 0:45', 'from hydrofoil appearance', 'Sink the required hydrofoil to open Target Acquisition.', 'Finish any needed optional kills before sinking the required boat.', '24+ enemies overall.'),
    ],
    21: [
        step('< 3:00', 'from mission start', 'Photograph all 4 hangars to trigger the full reinforcements.', 'Collect optional enemies toward the 20 total; the photo deadline applies to the hangars.'),
        total_step(20, 'Finish the reinforcement targets.'),
    ],
    22: [step('< 5:00', 'from mission start', 'Destroy the power plants and exposed core.', 'Take optional enemies before the final TGT to reach the total.', '18+ enemies overall.')],
    23: [total_step(9, 'Complete the required interception.', 'Take optional escorts before the final TGT to reach the total.')],
    24: [step('By completion', 'no separate A cutoff published', 'Destroy all 6 required R-531 Moburas.', 'Destroy at least 2 other enemies.', '8+ enemies overall; do not take the Keith-rescue route on this visit.')],
    25: [
        step('< 1:30', 'shuttle interception clock', 'Shoot down the required R-808 before it lands.', 'Optional kills do not replace the shuttle interception.'),
        total_step(17, 'Complete the remaining objectives; verify A on the result screen.', 'Destroy all available optional hostiles. The published 17-kill threshold conflicts with the wiki enemy count.'),
    ],
    26: [
        step('Throughout escort', '', 'Lose fewer than 4 Antlions.', 'Take optional hostiles toward the 12 total while protecting the Antlions.'),
        step('Before escape', 'R-352 interception', 'Shoot down the required R-352 before it escapes.', 'Finish needed optional kills before the final TGT.', '12+ enemies overall.'),
    ],
    27: [step('< 6:00', 'from mission start', 'Complete the required bombing objectives before the missile-launch outcome.', 'Take optional enemies before the final TGT to reach the total.', '30+ enemies overall.')],
    28: [step('< 9:00', 'from mission start', 'Destroy the required submarines and ships before departure.', 'Take optional enemies before the final TGT to reach the total.', '30+ enemies overall.')],
    29: [total_step(50, 'Complete the required targets.', 'Collect optional aircraft, ship weapons and ground targets before the final TGT.')],
    30: [
        step('Before carrier clear', '', 'Destroy the carrier after gathering enough kills.', 'Collect escort kills toward the 8 total before the carrier’s last TGT.'),
        step('< 3:00', 'from X-49 appearance', 'Inflict the required damage on the X-49 to open Geofront Attack.', 'The optional kills belong to the preceding carrier phase.', '8+ enemies overall.'),
    ],
    31: [step('< 4:00', 'from mission start', 'Complete the required objectives and finish.', 'No extra kills required.')],
    32: [total_step(6, 'Complete both main targets.', 'Take optional fighter escorts before the final main target to reach the total.')],
    33: [step('< 5:00', 'from aircraft-control change', 'Complete the remaining targets after taking control of a Geopelia.', 'No extra kills required.')],
    34: [
        step('Before update', '', 'Clear the required ground targets after collecting kills.', 'Take optional enemies toward the 29 total; the 3 escaping helicopters come next.'),
        step('< 1:30', 'from helicopter update', 'Destroy all 3 required escaping V-22Bs.', 'Collect needed optional kills before this timed chase.', '29+ enemies overall.'),
    ],
    35: [
        total_step(37, 'Complete the submarine attack and protect the carrier.', 'Take optional enemies before the last submarine TGT to reach the total.'),
        step('Before impact', 'launched cruise missile', 'Intercept the cruise missile before it hits the carrier.', 'No cleanup during this interception.'),
    ],
    36: [total_step(21, 'Destroy the escape aircraft after collecting enough kills.')],
    37: [step('Before final TGT', 'no separate A cutoff published', 'Complete the main objectives after clearing the escorts.', 'Destroy all 10 optional fighters: 3 R-103s, 2 Su-43s and 5 XFA-36As.')],
    38: [step('< 3:00', 'mission completion', 'Complete both required phases.', 'No extra kills required.')],
    39: [
        step('< 4:00', 'from mission start', 'Shoot down both initial required RF-12A2s.', 'No optional cleanup in this initial interception.'),
        step('Before final TGT', 'base attack', 'Complete the required base objectives.', 'Destroy all 3 oil tanks and 4 radar sites, plus enough other enemies for A. This opens Guardian Angel.', '21+ enemies overall.'),
    ],
    40: [
        step('< 3:00', 'from mission start', 'Shoot down all 7 initial F-22Cs and protect the shuttle.', 'No extra kills for this deadline.'),
        step('After update', 'shuttle escort', 'Destroy the next required fighter squadron; keep the shuttle safe.', 'No separate optional-kill total required.'),
    ],
    41: [
        step('< 2:30', 'combat clock', 'Destroy all 4 required satellites.', 'No extra kills required.'),
        step('After combat', 're-entry', 'Complete the re-entry alignment.', 'No enemy targets in this phase.'),
    ],
    42: [total_step(24, 'Keep enemy ships away from the satellite; preserve at least one original recovery unit.', 'Take optional enemies before the last TGT to reach the total.')],
    43: [total_step(12, 'Stay below the radar ceiling and remain undetected.', 'Collect optional ground targets before the last required radar to reach the total.')],
    44: [total_step(31)],
    45: [total_step(23, 'Complete the required targets.', 'Collect optional fighter kills before the final TGT to reach the total.')],
    46: [step('< 3:00', 'from mission start', 'Inflict the required damage and finish.', 'No extra kills required.')],
    47: [step('< 5:30', 'from mission start', 'Complete all required objectives, including the generator phase.', 'No extra kills required.')],
    48: [
        step('Before carrier update', '', 'Clear the initial required fighters after collecting kills.', 'Collect optional fighters toward the 17 total before the carrier phase.'),
        step('< 1:30', 'from carrier update', 'Destroy all 4 required Sphyrna target points to open Radio Silence.', 'Finish any needed optional kills before the carrier’s last TGT.', '17+ enemies overall.'),
    ],
    49: [step('< 4:00', 'from mission start', 'Complete the required objectives and finish.', 'No extra kills required.')],
    50: [step('Before final TGT', 'no separate A cutoff published', 'Finish the carrier after clearing the aircraft.', 'Destroy every optional aircraft before the carrier’s last target point.', 'All 11 enemies must be destroyed.')],
    51: [step('< 4:00', 'from mission start', 'Reach the end of the tunnel.', 'No hostile targets in this mission.')],
    52: [step('< 9:00', 'from mission start', 'Complete both main targets.', 'No extra kills required.')],
}

# Every exception replaces or extends the A-rank plan for this particular visit.
# Do not display contradictory A cleanup during intentional lower-grade branches.
ROUTE_MILESTONES = {
    (3, 7): [step('At the opening choice', '', 'Return to base immediately to open Fragile Cargo; a lower grade is intended.', 'No combat cleanup on this visit.')],
    (2, 9): MILESTONES[9] + [step('After initial combat', '', 'Shoot Fiona’s aircraft to stay with UPEO.', 'No extra kills needed for the choice.')],
    (3, 9): MILESTONES[9] + [step('After initial combat', '', 'Shoot the R-101U to protect Fiona and join Neucom.', 'No extra kills needed for the choice.')],
    (5, 39): [MILESTONES[39][0], step('Before final TGT', 'base attack', 'Complete the required targets while leaving at least one oil tank or radar intact. Take D to open Zero Gravity.', 'Do not clear all 7 oil-tank / radar targets. No A-rank cleanup on this visit.')],
    (8, 20): [step('< 3:30', 'from mission start', 'Destroy all initial required targets before the hydrofoil update to open Partners.', 'Skip optional cleanup; the A rank was saved on the earlier visit.')],
    (9, 24): [step('During Keith’s distress call', '', 'Shoot down the R-311 pursuing Keith. Take D to open Welcoming Committee.', 'Skip the Mobura A-rank cleanup on this visit.')],
    (12, 34): [step('After 1:30', 'from helicopter update', 'Leave an escaping target alive past 90 seconds to open Liquidation; a lower grade is intended.', 'No A-rank cleanup on this replay.')],
}
