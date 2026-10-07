import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
# Rank requirements are paraphrased from the linked Japanese-version mission articles.
# A missing numeric timer means that the source does not publish a separate cutoff.
rows = [
 (1,'Awakening','10+ aircraft; unlock and complete the second wave.','3:00','Initial targets','Finish the four R-501 targets before 3:00 to trigger reinforcements. Take optional kills before the last red target.'),
 (2,'Bravado','23+ enemies, including the mission-update targets.','4:00','Initial radar sites','Destroy all eight radars by 3:59 to trigger the base targets. Optional aircraft and defenses count toward the total.'),
 (3,'Enter Dision','5,000+ training points before the mission update.','','Score based','The six practice targets give 1,800 points; earn at least 3,200 by following Dision closely. Then complete the container interception.'),
 (4,'Paper Tiger','23+ enemies and trigger the mission update.','3:00','Initial targets','Finish the first target group by 2:59. The faction decision occurs before the next normal save opportunity.'),
 (5,'Broken Truce','11+ enemies and complete the reinforcement phase.','3:00','Initial fighters','Destroy all four target F-15s by 2:59 to spawn the bombers. Slower completion gives Mission Over / D.'),
 (6,'Ghosts of the Past','8+ enemies and complete the secret-base objective.','','Pursuit / discovery','Stay below the canyon rim and follow, rather than shoot, the recon plane. Destroy the discovered base; this opens No Clearance.'),
 (7,'No Clearance','Follow Rena; trigger the second squadron and finish combat by the 5:00 mark.','5:00','Combat completion','Destroy the first four aircraft before 3:30 to spawn the six reinforcements. Returning to base opens Fragile Cargo but skips the A-rank combat clear.'),
 (8,'Fragile Cargo','Protect the airship, then sink the escaping hydrofoil quickly.','0:30','From hydrofoil appearance','Clear the structures in the airship’s path. Sink the hydrofoil within 30 seconds after it appears.'),
 (9,'Scylla and Charybdis','Shoot down all five initial target fighters.','3:00','Initial combat','Clear the initial five targets within three minutes. The subsequent choice sets the UPEO or Neucom route.'),
 (10,'Fates Intertwined','Complete the mission.','2:00','Whole mission','Finish under two minutes. Intercept the high-altitude targets promptly.'),
 (11,'Reaching for Stars','18+ enemies; destroy every Antlion before landing.','2:00','Antlion phase','Destroy the ten Antlions in under two minutes to spawn reinforcements. Finish the additional targets after collecting enough kills.'),
 (12,'One-Way Ticket','10+ enemies; preserve the two neutral train cars.','5:00','Whole mission','Destroy the target train cars by 4:59. Use the escort aircraft to reach the required kill total.'),
 (13,'Bug Hunt','Eradicate the nano-bites and disinfect the allied aircraft.','4:30','Whole mission','Use the special anti-nano-bite bombs; the final disinfection is part of the completion time.'),
 (14,'Pawns in the Game','Destroy the armory without being detected by radar.','9:00','Whole mission','Finish under nine minutes. When jamming stops, climb above the indicated safe altitude before attacking again.'),
 (15,'Damage Control','22+ enemies; do not hit civilian aircraft.','','Kill / protection based','Avoid the news helicopters. Finish both hostile waves after collecting enough optional kills.'),
 (16,'Broken Wings','Shoot down all twelve hostile fighters.','4:00','Whole mission','The completion threshold is four minutes.'),
 (17,'Sphyrna','Destroy all twelve optional fighters before finishing the carrier.','','Kill based','Nine XFA-36As and three R-103s must be destroyed in addition to the carrier’s target points.'),
 (18,'A Canopy of Stars','21+ enemies, then complete the final objective.','','Kill based','Collect optional kills before destroying the final escape aircraft.'),
 (19,'Soldier of Fortune','15+ enemies, including all grounded target aircraft.','3:00','Before aircraft takeoff','Finish the targets before three minutes. Letting them take off changes the outcome to Mission Over / D.'),
 (20,'Megafloat','24+ enemies; if the target hydrofoil launches, sink it.','0:45','From hydrofoil appearance','The hydrofoil phase starts at 3:30 if initial targets remain. Destroy the target boat within 45 seconds. Finishing before 3:30 instead leads to Partners.'),
 (21,'Target Acquisition','Photograph all hangars in time and destroy 20+ enemies.','3:00','Photography phase','Complete all four hangar scans before three minutes to get the full reinforcements; the kill requirement spans the mission.'),
 (22,'Partners','18+ enemies and complete all objectives.','5:00','Whole mission','Destroy the power plants and exposed core before five minutes; missiles cannot guide here.'),
 (23,'Tainted Peace','9+ enemies, then complete the target interception.','','Kill based','Collect the optional kills before the final target ends the mission.'),
 (24,'Stratosphere','8+ enemies; complete the Mobura interception.','','Kill / route based','Destroy the six R-531s plus at least two other enemies. Saving Keith instead produces a D-rank route to Welcoming Committee.'),
 (25,'Welcoming Committee','Published requirement: 17+ enemies and intercept the shuttle before it lands.','1:30','Shuttle interception only','Destroy the R-808 by 1:29, then finish the remaining targets. The published enemy list and 17+ threshold do not fully reconcile; destroy every available hostile and verify the result screen.'),
 (26,'Technology Transfer','12+ enemies; lose fewer than four Antlions.','','Escort / escape based','Protect the Antlions, then shoot down the R-352 before it escapes. Losing every Antlion gives D.'),
 (27,'Claustrophobia','30+ enemies and complete the bombing objectives.','6:00','Whole mission','Finish before six minutes; a late missile-launch outcome gives Mission Over / D.'),
 (28,'Dilemma','30+ enemies and complete the dock attack.','9:00','Departure gate','Destroy the submarines and ships before their nine-minute departure. The final follow decision determines the ending route.'),
 (29,'Betrayal','50+ destroyed targets and complete the mission.','','Kill based','Collect optional aircraft, ship weapons, and ground targets before finishing the last required objective.'),
 (30,'Heart of the Serpent','8+ enemies and inflict enough damage on the X-49.','3:00','From X-49 appearance','After the carrier phase, meet the X-49 damage threshold within three minutes. This opens Geofront Attack; being late skips it and gives D.'),
 (31,'Geofront Attack','Complete the mission.','4:00','Whole mission','Finish under four minutes. This mission is reached by meeting the timed damage gate in Heart of the Serpent.'),
 (32,'Casualties of War','6+ enemies and complete both main targets.','','Kill based','Destroy enough of the optional fighter escorts before finishing the main targets.'),
 (33,'Geopelia','Complete the remaining targets after the aircraft-control change.','5:00','From control change','The five-minute A-rank window starts when you take control of a Geopelia, not at the original mission start.'),
 (34,'The Orientation','29+ enemies and all three escaping target V-22Bs.','1:30','From helicopter update','Finish the escaping targets within 90 seconds for the A route. A separate replay leaving a target alive past 90 seconds opens Liquidation.'),
 (35,'Liquidation','37+ enemies; protect the carrier from the cruise missile.','','Kill / interception based','Complete the submarine attack, then intercept the launched missile before impact.'),
 (36,'Archnemesis','21+ enemies and complete the final target.','','Kill based','Gather optional kills before destroying the escape aircraft.'),
 (37,'Memory Error','Destroy all ten optional fighter targets and complete the main objectives.','','Kill based','The optional group is three R-103s, two Su-43s, and five XFA-36As.'),
 (38,'Electrosphere','Complete both phases of the mission.','3:00','Mission completion','The guide lists a three-minute completion threshold. Do not confuse this with the five-minute export-version requirement.'),
 (39,'Power for Life','21+ enemies, including all three oil tanks and four radar sites.','4:00','Initial RF-12A2 phase','Clear the initial pair in under four minutes. Destroy every oil tank and radar before the last main target for Guardian Angel. Leaving any of the seven intact produces D and opens Zero Gravity.'),
 (40,'Guardian Angel','Protect the shuttle and shoot down the first two fighter squadrons.','3:00','Initial seven F-22Cs','All seven initial fighters must be down in under three minutes for A. Four minutes is the separate mission-update boundary.'),
 (41,'Zero Gravity','Destroy all four satellites.','2:30','Whole combat phase','A-rank cutoff: 2:30. Hard failure occurs at 3:00. Complete the re-entry alignment afterward.'),
 (42,'The Prize','24+ enemies; at least one original recovery unit must survive.','','Escort / arrival based','Keep the enemy ships away from the satellite and preserve part of the first recovery squadron.'),
 (43,'Utopian Dreams','12+ enemies and remain undetected by radar.','','Kill / stealth based','Stay below the stated radar ceiling; collect optional ground targets before the last radar. The final decision chooses Fiona or Cynthia.'),
 (44,'Reality Distortion','31+ enemies and complete the mission.','','Kill based','Collect optional enemies as well as the required targets.'),
 (45,'Counterrevolution','23+ enemies and complete the mission.','','Kill based','Collect optional fighter kills before finishing the final main target.'),
 (46,'Pursuit','Inflict the required damage and finish the mission.','3:00','Whole mission','Complete the damage objective in under three minutes.'),
 (47,'Self Awareness','Complete the mission.','5:30','Whole mission','Finish under five minutes thirty seconds, including the generator phase.'),
 (48,'Resistance','17+ enemies and destroy all four carrier target points quickly.','1:30','From carrier mission update','Complete the four Sphyrna points within 90 seconds of the update to open Radio Silence. A late finish skips it and gives D.'),
 (49,'Radio Silence','Complete the mission.','4:00','Whole mission','Finish under four minutes.'),
 (50,'Revenge','Destroy all eleven enemies and complete the mission.','','Kill based','Clear the optional aircraft before the carrier’s last target point.'),
 (51,'Tunnel Vision','Reach the end of the tunnel.','4:00','Whole mission','Complete the tunnel flight within four minutes. There are no hostile targets to farm.'),
 (52,'Sole Survivor','Complete both main targets.','9:00','Whole mission','Finish under nine minutes.'),
]

positions = {1:(690,0),2:(690,1),3:(690,2),4:(690,3),5:(230,4),6:(230,5),7:(230,6),8:(230,7),9:(230,8),
            19:(1050,4),20:(1050,5),21:(930,6),22:(1170,6),23:(1050,7),24:(1050,8),25:(930,9),26:(1170,9),27:(930,10),28:(1050,11),
            29:(930,12),30:(930,13),31:(930,14),32:(930,15),33:(930,16),34:(1170,12),35:(1170,13),36:(1170,14),37:(1170,15),38:(1170,16),
            39:(580,9),40:(460,10),41:(700,10),42:(460,11),43:(580,12),44:(460,13),45:(460,14),46:(460,15),47:(460,16),48:(700,13),49:(700,14),50:(700,15),51:(700,16),52:(700,17)}
for i in range(10,19): positions[i]=(150,i-1)
endings={18:'UPEO',33:'General Resource',38:'Ouroboros · via General',47:'Ouroboros · via Neucom',52:'Neucom'}
checkpoints={3:'S1: retain this post-mission save until all UPEO and Neucom routes are complete.',6:'S2: keep this until the UPEO ending; its replay covers BOTH the No Clearance and Scylla choices.',9:'On the Neucom branch only: replace S2 here. Keep it through the Neucom ending; its replay covers BOTH the Power for Life and Utopian Dreams forks.',19:'S2: replace the finished Neucom checkpoint here to revisit Megafloat.',23:'After both Megafloat branches: replace S2 here. Keep it through the General Resource ending; its replay covers BOTH Stratosphere and Dilemma.',28:'On the Ouroboros branch, after the General Resource ending: replace S2 here to revisit The Orientation.'}
M=[]
for id,title,rank,timer,clock,note in rows:
    faction='Prologue' if id<=4 else 'UPEO' if id<=18 else 'General Resource' if id<=33 else 'Ouroboros · General' if id<=38 else 'Ouroboros · Neucom' if 44<=id<=47 else 'Neucom'
    slug={20:'Megafloat_(mission)',33:'Geopelia_(mission)',38:'Electrosphere_(mission)',48:'Resistance_(AC3)'}.get(id,title.replace(' ','_'))
    domain='acecombat.fandom.com' if id in [44] else 'acecombat.wiki.gg'
    sources=[{'label':'JP mission guide','url':f'https://{domain}/wiki/{slug}'}]
    if id in [2,25,28]:sources.append({'label':'Jerrold’s JP walkthrough','url':'https://gamefaqs.gamespot.com/ps/196536-ace-combat-3-electrosphere/faqs/5035'})
    M.append(dict(id=id,title=title,faction=faction,rank=rank,timer=timer,clock=clock,note=note,source=sources,x=positions[id][0],y=positions[id][1],ending=endings.get(id),checkpoint=checkpoints.get(id),caution=(id==25)))

E=[]
def edge(a,b,label='',skip=False):E.append(dict(a=a,b=b,label=label,skip=skip))
for a,b in [(1,2),(2,3),(3,4),(5,6),(8,9),*[(i,i+1) for i in range(10,18)],(19,20),(21,23),(22,23),(23,24),(25,27),(27,28),(26,28),(29,30),(31,32),(32,33),(35,36),(36,37),(37,38),(40,42),(42,43),(41,43),(44,45),(45,46),(46,47),(49,50),(50,51),(51,52)]:edge(a,b)
for a,b,label,skip in [
 (4,5,'Stay with UPEO / follow Fiona',False),(4,19,'Follow Dision',False),
 (6,7,'Discover and destroy the secret base',False),(6,8,'Fail the pursuit / skip the base',True),
 (7,9,'Follow Rena and finish combat',True),(7,8,'Return to base',False),
 (9,10,'Obey UPEO orders / do not protect Fiona',False),(9,39,'Protect Fiona: shoot the R-101U',False),
 (20,21,'Wait for 3:30; destroy target hydrofoil',False),(20,22,'Finish before 3:30 OR let hydrofoil escape',False),
 (24,25,'Save Keith: destroy his pursuing R-311 (D)',False),(24,26,'Destroy the R-531 Moburas (A route)',False),
 (28,29,'Stay with Keith / General Resource',False),(28,34,'Follow Dision / join Ouroboros',False),
 (30,31,'Damage X-49 enough within 3:00 of appearance',False),(30,32,'Miss the three-minute damage gate (D)',True),
 (34,35,'Leave an escaping target alive for 1:30',False),(34,36,'Destroy all escaping targets within 1:30',True),
 (39,40,'Destroy all 3 oil tanks + 4 radar sites',False),(39,41,'Leave at least one of those seven intact (D)',False),
 (43,44,'Follow Cynthia / join Ouroboros',False),(43,48,'Stay with Fiona / Neucom',False),
 (48,49,'Destroy all four carrier points within 1:30',False),(48,50,'Take longer than 1:30 (D)',True)]:edge(a,b,label,skip)

# Every checkpoint refers to the mission JUST FINISHED, as requested.
plans=[
 ('Establish the root checkpoint','A-rank 01, Awakening, and 02, Bravado. Then A-rank 03, Enter Dision; save after it to S1. Keep S1 until the first three endings are finished.',3,1,'Root: after 03 → Paper Tiger',[1,2,3],[],[]),
 ('Reach the UPEO checkpoint','In 04, stay with UPEO / follow Fiona. A-rank 04–06; in Ghosts of the Past, discover and destroy the secret base. Save after 06 to S2.',6,2,'After 06 → No Clearance',[4,5,6],[],['4-5','6-7']),
 ('Finish UPEO directly','In 07, follow Rena and A-rank the full combat. You proceed directly to 09. Stay with UPEO there; A-rank 09–18. Save the ending to S3. Keep S1 and S2. Mission 08 comes on the next leg.',18,3,'Completed UPEO ending',[7,*range(9,19)],[],['7-9','9-10']),
 ('Reload S2: visit Fragile Cargo, then join Neucom','Load S2 (after 06). In 07, return to base; this lower-rank replay is intentional. A-rank 08 and 09; in 09 protect Fiona by shooting the R-101U. Overwrite S2 after 09, on the Neucom route.',9,2,'After 09 · Neucom → Power for Life',[8,9],[7],['7-8','9-39']),
 ('Finish Neucom’s ending','A-rank 39 by destroying all 3 oil tanks + 4 radar sites. Continue 40 → 42 → 43; stay with Fiona in 43. A-rank 48–52, meeting the 90-second carrier gate in 48 to include 49. Save the ending to S4; keep S2.',52,4,'Completed Neucom ending',[39,40,42,43,48,49,50,51,52],[],['39-40','43-48','48-49']),
 ('Reload S2: visit space, then finish Neucom → Ouroboros','Load S2 (after 09). In 39, leave at least one oil tank / radar intact for the deliberate D route. A-rank 41, then 43 and follow Cynthia. A-rank 44–47. Overwrite S2 throughout this last branch, keeping its ending there.',47,2,'Completed Ouroboros · via Neucom ending',[41,43,44,45,46,47],[39],['39-41','43-44']),
 ('Reload S1: switch to General Resource','Load S1 (after 03). Replay 04 and follow Dision. A-rank 19; overwrite S1 after each mission. Keep the after-19 checkpoint for the Megafloat fork.',19,1,'After 19 → Megafloat',[4,19],[],['4-19']),
 ('Visit Target Acquisition','In 20, keep an initial target alive until 3:30, then sink the target hydrofoil within 45 seconds; get 24+ kills for A. Save to S5. A-rank 21 and overwrite S5 before reloading.',21,5,'After 21 → Tainted Peace',[20,21],[],['20-21']),
 ('Reload S1: visit Partners','Load S1 (after 19). Finish 20 before 3:30 to reach 22. Letting the hydrofoil escape also works; A is already recorded. A-rank 22 and 23, overwriting S1 after each mission.',23,1,'After 23 → Stratosphere',[22,23],[],['20-22']),
 ('Help Keith; finish General Resource','In 24, shoot down the R-311 attacking Keith and accept D. A-rank 25 → 27 → 28; stay with Keith in 28. A-rank 29–33, meeting the three-minute X-49 damage gate in 30 to include 31. Overwrite S5 after every mission, keeping the ending there. Keep S1.',33,5,'Completed General Resource ending',[25,27,28,29,30,31,32,33],[24],['24-25','28-29','30-31']),
 ('Reload S1: bank Stratosphere A, then join Ouroboros','Load S1 (after 23). A-rank 24 by destroying the Moburas plus two other enemies. A-rank 26 and 28; follow Dision in 28. Overwrite S1 after each mission, ending on the Ouroboros side.',28,1,'After 28 · Ouroboros → The Orientation',[24,26,28],[],['24-26','28-34']),
 ('Bank The Orientation’s A rank','In 34, destroy 29+ enemies and all three escaping target V-22Bs within 90 seconds of the update. Save after 34 to S6. Do not fly 36 yet: the reload next will bring you back to it.',34,6,'Rolling: after 34 → Archnemesis',[34],[],['34-36']),
 ('Reload S1: visit Liquidation and finish','Load S1 (after 28). Replay 34, leaving an escaping target alive past 90 seconds. A-rank 35–38. Overwrite S1 after each mission, including the post-credits system save. All five endings and all 52 A ranks are now covered, provided 01 was also A.',38,1,'Completed Ouroboros · via General ending',[35,36,37,38],[34],['34-35']),
]
P=[]
for i,(title,body,after,slot,label,clears,lower,branches) in enumerate(plans):
    P.append(dict(id=i,title=title,body=body,after=after,slot=slot,saveLabel=label,clears=clears,lower=lower,branches=branches))

assert {r['id'] for r in M}==set(range(1,53))
assert set(sum([p['clears'] for p in P],[]))|{1,2}==set(range(1,53))
assert len({(e['a'],e['b']) for e in E})==len(E)
sequence=[3,4,5,6,7,*range(9,19),7,8,9,39,40,42,43,48,49,50,51,52,39,41,43,44,45,46,47,4,19,20,21,20,22,23,24,25,27,28,29,30,31,32,33,24,26,28,34,34,35,36,37,38]
assert len(sequence)==59
groups = [
    [1,2,3], [4,5,6], [7,*range(9,19)], [7,8,9],
    [39,40,42,43,*range(48,53)], [39,41,43,*range(44,48)],
    [4,19], [20,21], [20,22,23], [24,25,27,28,*range(29,34)],
    [24,26,28], [34], [34,35,36,37,38],
]
reloads = {3:(2,6,''), 5:(2,9,'Neucom route'), 6:(1,3,''),
           8:(1,19,''), 10:(1,23,''), 12:(1,28,'Ouroboros route')}
time_targets = {
    1:'Under 3:00 · first four targets', 2:'Under 4:00 · eight radars',
    3:'—', 4:'Under 3:00 · first target group', 5:'Under 3:00 · first four fighters',
    7:'First four: under 3:30 · finish: under 5:00',
    8:'Under 0:30 · from hydrofoil appearance', 9:'Under 3:00 · first five fighters',
    11:'Under 2:00 · ten Antlions', 19:'Under 3:00 · before takeoff',
    20:'Under 0:45 · from hydrofoil appearance', 21:'Under 3:00 · all hangar photos',
    25:'Under 1:30 · shuttle interception', 28:'Under 9:00 · before ships depart',
    30:'Under 3:00 · from X-49 appearance', 33:'Under 5:00 · from aircraft-control change',
    34:'Under 1:30 · from escaping-target update', 39:'Under 4:00 · first two RF-12A2s',
    40:'Under 3:00 · first seven F-22Cs', 41:'Under 2:30 · all four satellites',
    48:'Under 1:30 · from carrier update',
}
decisions = {
    (1,4):'Stay with UPEO; follow Fiona.',
    (1,6):'Follow the recon plane; discover and destroy the secret base.',
    (2,7):'Follow Rena; finish the full combat for A.',
    (2,9):'Stay with UPEO; obey orders.',
    (3,7):'Return to base. A lower grade is intentional.',
    (3,9):'Protect Fiona: shoot down the R-101U; join Neucom.',
    (4,39):'Destroy all three oil tanks and all four radar sites.',
    (4,43):'Stay with Fiona.',
    (4,48):'Destroy all four carrier points within 1:30 to reach Radio Silence.',
    (5,39):'Leave at least one oil tank or radar intact. Accept D.',
    (5,43):'Follow Cynthia; join Ouroboros.',
    (6,4):'Follow Dision; join General Resource.',
    (7,20):'Keep an initial target alive until 3:30; then sink the target hydrofoil.',
    (8,20):'Finish initial targets before 3:30 → Partners. Any rank; A is already saved.',
    (9,24):'Save Keith: shoot his pursuing R-311. Accept D.',
    (9,28):'Stay with Keith / General Resource.',
    (9,30):'Damage the X-49 enough within 3:00 to reach Geofront Attack.',
    (10,24):'Destroy all six R-531 Moburas; take the A route.',
    (10,28):'Follow Dision; join Ouroboros.',
    (11,34):'Destroy all three escaping V-22B targets within 1:30 for A.',
    (12,34):'Leave an escaping target alive past 1:30. A lower grade is intentional.',
}
actions=[]
visits={}
lookup={m['id']:m for m in M}
for leg, group in enumerate(groups):
    if leg in reloads:
        slot,after,route=reloads[leg]
        actions.append(dict(id=f'load-{len([a for a in actions if a["type"]=="load"])+1}',
                            type='load',slot=slot,after=after,route=route,legacyLeg=leg))
    for n in group:
        m=lookup[n]
        visits[n]=visits.get(n,0)+1
        target=time_targets.get(n, f'Under {m["timer"]} · whole mission' if m['timer'] else '—')
        if (leg,n)==(3,7): target='— · return immediately'
        if (leg,n)==(8,20): target='Under 3:30 · initial targets'
        if (leg,n)==(12,34): target='Wait past 1:30 · from escaping-target update'
        rank='D' if n in P[leg]['lower'] else 'any' if (leg,n)==(8,20) else 'A'
        save=dict(slot=P[leg]['slot'],after=n,label=f'After {n:02d} {m["title"]}',ending=False)
        if n==group[-1]:
            save=dict(slot=P[leg]['slot'],after=n,label=P[leg]['saveLabel'],ending=bool(m['ending']))
        actions.append(dict(id=f'mission-{n:02d}-{visits[n]}',type='mission',mission=n,
                            visit=visits[n],time=target,decision=decisions.get((leg,n),''),
                            rank=rank,save=save,ending=m['ending'],legacyLeg=leg))

assert [a['mission'] for a in actions if a['type']=='mission']==[1,2]+sequence
assert len(actions)==67
assert {a['mission'] for a in actions if a.get('rank')=='A'}==set(range(1,53))
# Label the first use of each slot as fresh, and validate every later reload.
slots={}
for a in actions:
    if a['type']=='load': assert slots[a['slot']]==a['after']
    else:
        slot=a['save']['slot']
        a['save']['mode']='overwrite' if slot in slots else 'fresh'
        slots[slot]=a['mission']
assert slots=={1:38,2:47,3:18,4:52,5:33,6:34}

data=dict(missions=M,edges=E,actions=actions,sequence=[1,2]+sequence,
          researchDate='2026-10-06',schemaVersion=2)
theme=(ROOT/'theme.css').read_text()
background=(ROOT/'background.js').read_text()
def themed(name):
    return (ROOT/name).read_text().replace('/*__THEME__*/',theme).replace('/*__BACKGROUND__*/',background)
template=themed('template.html')
out=ROOT.parent/'index.html'
out.write_text(template.replace('/*__DATA__*/', 'const DATA='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';'))
print(f'{out}: {out.stat().st_size:,} bytes; {len(M)} missions, {len(actions)} checklist actions')

reference=[]
for m in M:
    links=' · '.join(f'<a href="{escape(s["url"],quote=True)}" rel="noopener">{escape(s["label"])}</a>' for s in m['source'])
    reference.append(f'<section class="reference-section" id="mission-{m["id"]}"><h2>{m["id"]:02d} · {escape(m["title"])}</h2>'
                     f'<p><b>A rank:</b> {escape(m["rank"])}</p>'
                     f'<p><b>Clock:</b> {escape(m["timer"] or "No separate cutoff published")} · {escape(m["clock"])}</p>'
                     f'<p>{escape(m["note"])}</p><p class="sources">{links}</p></section>')
ref_template=themed('reference.html')
(ROOT.parent/'ranks.html').write_text(ref_template.replace('<!--__MISSIONS__-->','\n'.join(reference)))
