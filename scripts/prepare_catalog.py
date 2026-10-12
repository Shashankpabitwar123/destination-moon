from pathlib import Path
import json,re,datetime,hashlib,csv,io
from dateutil.parser import parse
P=Path(__file__).resolve().parents[1];S=P/'source'
rows=json.loads((S/'nasa-rows.json').read_text());chron=json.loads((S/'chronicle-lunar.json').read_text());fetched={d['url']:d for d in json.loads((S/'fetched-index.json').read_text())}
PDF='https://science.nasa.gov/wp-content/uploads/2023/09/DSC_monograph24.pdf'
NASA='https://science.nasa.gov/moon/missions/'
# Parent mission grain; component payloads are described in their parent record.
exclude={'Pioneer P-1':'Ground-pad accident; no launch attempt','Lunokhod 1':'Included in Luna 17','Lunokhod 2':'Included in Luna 21','Yutu':'Included in Chang’e 3','PFS-1':'Included in Apollo 15','PFS-2':'Included in Apollo 16','Emirates Lunar Mission':'Rashid rover carried by Hakuto-R Mission 1'}
fixdates={'Pioneer 3':'1958-12-06','Ranger 4':'1962-04-23','Ranger 5':'1962-10-18',"Chang'e 3":'2013-12-01','Blue Ghost 1':'2025-01-15','ARTEMIS-THEMIS':'2007-02-17'}
unnamed={1:('Luna E-1 No.1',2),3:('Luna E-1 No.2',4),5:('Luna E-1 No.3',6),9:('Luna E-1A',10),14:('Luna E-3 No.1',15),15:('Luna E-3 No.2',16),21:('Luna E-6 No.2',36),22:('Luna E-6 No.3',37),25:('Luna E-6 No.6',42),26:('Luna E-6 No.5',45),31:('Luna E-6 No.8',54),55:('Luna E-6LS No.112',94),60:('Luna E-8 No.201',104),62:('Luna E-8-5 No.402',110),70:('Luna E-8-5 No.405',117)}
short={'Lunar Orbi ter 1':'Lunar Orbiter 1','SELENE (Kaguya)':'Kaguya','Lunar Reconnaissance Orbiter (LRO)':'LRO','Gravity Recovery and Interior Laboratory (GRAIL)':'GRAIL','Lunar Atmosphere and Dust Environment Explorer (LADEE)':'LADEE','Danuri (Korean Pathfinder Lunar Orbiter)':'Danuri',"Chang'e 5-Test Vehicle":"Chang’e 5-T1","Chang'e 4 and Yutu 2":"Chang’e 4",'ARTEMIS-THEMIS':'ARTEMIS probes','Hakuto-R Mission 1':'Hakuto-R M1','Peregrine Mission 1':'Peregrine M1'}
# Editorial summaries preserve objectives/outcomes, not necessarily every subsystem success.
custom={
'Pioneer 0':('First attempt at the Moon','Test a lunar orbiter and study the Moon and its environment.','The booster exploded shortly after liftoff. The spacecraft never reached the Moon.'),
'Luna E-1 No.1':('A launch cut short','Send an instrumented probe to strike the Moon.','Booster vibrations caused the rocket to break apart during ascent.'),
'Pioneer 1':('Science despite a setback','Orbit the Moon and study its environment.','Insufficient launch speed prevented a lunar encounter, but the probe returned useful near-Earth data.'),
'Luna E-1 No.2':('A second launch failure','Send a probe to the Moon for an intentional impact.','Resonant vibrations again destroyed the launch vehicle before it could leave Earth.'),
'Pioneer 2':('An engine failed to fire','Place a scientific probe in lunar orbit.','The upper-stage engine failed to ignite; the probe reentered Earth’s atmosphere.'),
'Luna E-1 No.3':('Engine trouble on ascent','Reach the Moon with an instrumented impact probe.','A main-engine pump problem caused premature cutoff. The probe did not reach escape speed.'),
'Pioneer 3':('The Moon stayed out of reach','Fly past the Moon and measure radiation along the way.','An early engine cutoff left too little speed for a Moon flyby. Radiation measurements still helped reveal Earth’s radiation belts.'),
'Luna 1':('A miss became a first','Strike the Moon and measure particles and magnetic fields along the route.','Missed its intended impact but became the first spacecraft to pass the Moon and enter solar orbit.'),
'Pioneer 4':('America reached deep space','Fly close to the Moon and test an optical sensor.','Passed too far away to trigger the optical experiment, but returned radiation data and escaped Earth’s gravity.'),
'Luna E-1A':('Guidance failure','Reach the lunar surface with an impact probe.','A guidance gyroscope failed during ascent; the wayward launch vehicle was destroyed by ground command.'),
'Luna 2':('First contact with the Moon','Strike the Moon and investigate the space environment.','Became the first human-made object to reach another celestial body. Its impact was intentional.'),
'Luna 3':('First views of the far side','Photograph the side of the Moon hidden from Earth.','Returned the first far-side images, revealing previously unseen terrain.'),
'Pioneer P-3':('Lost during launch','Orbit the Moon and study radiation, magnetic fields and the lunar surface.','The protective nose fairing broke apart during ascent, destroying the payload.'),
'Luna E-3 No.1':('Too little speed','Return more detailed photographs of the Moon’s far side.','Premature upper-stage cutoff left insufficient speed. The spacecraft fell back toward Earth.'),
'Luna E-3 No.2':('Lost near the launch site','Photograph the Moon’s far side with an improved probe.','The launch vehicle broke apart seconds after liftoff.'),
'Pioneer P-30':('An orbiter lost on ascent','Orbit the Moon and measure its environment.','The second stage shut down early and the third stage did not fire. The probe reentered Earth’s atmosphere.'),
'Pioneer P-31':('The final early Pioneer attempt','Enter lunar orbit to study radiation and magnetic fields.','The Atlas-Able booster exploded during ascent; the planned lunar orbit was never reached.'),
'Ranger 3':('A missed encounter','Photograph the Moon during descent and deliver an instrument capsule.','Guidance and control failures sent it past the Moon. It returned no lunar pictures.'),
'Ranger 4':('Reached the Moon, but silent','Take descent photographs and deliver a seismometer capsule.','A computer power failure prevented planned operations. It struck the far side without returning the intended science.'),
'Ranger 5':('Power lost on the way','Photograph the lunar surface and deliver instruments.','An electrical malfunction exhausted battery power. The unresponsive spacecraft passed the Moon.'),
'Luna 4':('A landing attempt flew past','Demonstrate a soft landing and send pictures from the surface.','An attitude-control failure prevented the planned course correction, so the spacecraft missed the Moon.'),
'Ranger 6':('On target, without pictures','Return close-up photographs before an intentional lunar impact.','Reached its target, but a short circuit disabled the camera system and no pictures were returned.'),
'Ranger 7':('The Moon in close-up','Photograph the lunar surface before a planned impact.','Returned thousands of close-up images, helping planners assess the lunar surface.'),
'Ranger 8':('Surveying future landing sites','Photograph the Moon during descent to an intentional impact.','Returned more than 7,000 photographs near the Sea of Tranquility.'),
'Ranger 9':('A televised lunar approach','Photograph the Alphonsus crater region before impact.','Returned detailed descent images that were also broadcast to television audiences.'),
'Luna 5':('A landing became a crash','Test a soft landing on the Moon.','Attitude-control and braking problems prevented a soft landing; the spacecraft struck the surface.'),
'Luna 6':('The engine kept firing','Demonstrate a soft lunar landing.','A course-correction engine failed to shut down on time, sending the craft past the Moon.'),
'Zond 3':('More of the hidden hemisphere','Photograph the far side and test deep-space spacecraft systems.','Returned photographs of additional far-side terrain and demonstrated deep-space communications.'),
'Luna 7':('Braking never began','Soft-land a camera capsule on the lunar surface.','Lost attitude control before braking. Its main engine did not fire and the craft crashed.'),
'Luna 8':('An airbag upset the landing','Demonstrate a cushioned soft landing on the Moon.','An airbag problem upset the craft’s attitude. Inadequate braking led to a crash.'),
'Luna 9':('First soft landing','Land a camera capsule safely and photograph the lunar surface.','Achieved the first successful soft landing on the Moon and sent back surface panoramas.'),
'Luna 10':('First lunar orbiter','Enter orbit and study the Moon from above.','Became the first spacecraft to orbit the Moon.'),
'Surveyor 1':('America’s first soft landing','Demonstrate landing technology and photograph the surface.','Landed successfully and returned surface images that supported planning for Apollo.'),
'Surveyor 2':('A failed thruster','Soft-land and study the lunar surface.','A thruster failed during a course correction. The spacecraft spun out of control and crashed.'),
'Surveyor 3':('Testing the ground for Apollo','Study surface properties and test soil with a sampling tool.','Its successful surface tests helped assess whether lunar soil could support an Apollo lander.'),
'Surveyor 4':('Contact lost before touchdown','Soft-land and investigate lunar soil.','Radio contact stopped just before the planned landing and was never restored.'),
'Surveyor 5':('Chemistry on another world','Analyze lunar soil and photograph the surface.','Survived a propulsion leak and performed the first in-place chemical analysis of lunar soil.'),
'Surveyor 6':('A small hop on the Moon','Study the surface and demonstrate lander operations.','Landed, returned images and briefly lifted off again to demonstrate a short surface hop.'),
'Surveyor 7':('Exploring the highlands','Investigate lunar highland soil and surface conditions.','Completed surface observations in highland terrain, extending the Surveyor science programme.'),
'Zond 5':('Life around the Moon','Test a circumlunar flight and Earth return with biological specimens.','Carried living organisms around the Moon and recovered them on Earth.'),
'Zond 6':('The return was not survivable','Test a circumlunar flight and recover biological specimens.','Flew around the Moon, but depressurization and a landing failure prevented recovery of living cargo.'),
'Luna 15':('Orbit achieved; samples lost','Collect lunar soil and return it to Earth.','Reached lunar orbit but crashed during descent. No samples returned.'),
'Luna 16':('Robotic samples returned','Collect lunar soil and return it automatically to Earth.','Completed the first robotic return of samples from the Moon.'),
'Luna 17':('A rover explored the Moon','Deliver Lunokhod 1 to investigate the surface.','Landed successfully and deployed the Lunokhod 1 rover.'),
'Luna 21':('Lunokhod 2 on the surface','Deliver a rover to explore and photograph the Moon.','Successfully landed and deployed Lunokhod 2 for surface exploration.'),
'Luna 23':('Landing achieved; sampling failed','Drill into the lunar surface and return a sample.','Landed, but damage prevented the intended sample return.'),
'Luna 24':('A deep lunar sample','Drill for lunar material and return it to Earth.','Successfully returned a drilled sample of lunar soil.'),
'Hiten':('Japan reached the Moon','Test lunar navigation and orbital flight.','Completed a pioneering Japanese lunar mission, including flybys and lunar orbit.'),
'Clementine':('Mapping the Moon anew','Test spacecraft sensors and map the lunar surface.','Completed its lunar mapping objectives; a later asteroid encounter was cancelled after a malfunction.'),
'Lunar Prospector':('Searching for polar ice','Map lunar composition and investigate possible polar ice.','Returned evidence consistent with water ice near both poles and mapped lunar composition.'),
'SMART-1':('Electric propulsion to the Moon','Test solar-electric propulsion and compact scientific instruments.','Completed its technology demonstrations and lunar science programme.'),
'GRAIL':('Gravity revealed the interior','Use two spacecraft to map variations in lunar gravity.','The twin probes mapped the gravity field in unprecedented detail.'),
'LADEE':('Studying a thin atmosphere','Measure the Moon’s tenuous atmosphere and dust environment.','Completed lunar atmospheric observations before a planned impact.'),
'LCROSS':('An impact exposed water','Search for water ice by observing material thrown up from a polar impact.','Detected water in ejecta from the deliberately targeted impact.'),
'LRO':('A detailed atlas of the Moon','Map the lunar surface and characterize sites for future exploration.','Produced extensive maps and scientific observations. Success does not mean that all operations have ended.'),
'ARTEMIS probes':('Two probes redirected','Study the Moon’s interaction with the solar wind.','Two THEMIS spacecraft moved from their original Earth mission into lunar orbit in 2011.'),
'Chandrayaan-1':('Evidence of lunar water','Map lunar composition and study the surface from orbit.','Its instruments contributed to the discovery of water and hydroxyl on the lunar surface.'),
'Chandrayaan-2':('Orbiter success; lander lost','Orbit the Moon and deliver a lander and rover.','The orbiter achieved useful science, but the Vikram lander did not soft-land. The combined mission is classified as partial.'),
'Chandrayaan-3':('India landed near the south pole','Demonstrate a safe landing, rover motion and surface science.','The lander and rover completed their core surface demonstrations.'),
'SLIM':('A pinpoint landing','Demonstrate a precise lunar landing and observe surface rocks.','Achieved its precision-landing objective and rock observations despite an awkward landing attitude.'),
'Beresheet':('A private landing attempt','Demonstrate a privately developed lunar landing.','Reached lunar orbit but crashed during its descent.'),
'Hakuto-R M1':('Orbit reached; landing failed','Deliver commercial payloads and the Rashid rover to the surface.','Completed the cruise and lunar orbit phases but failed to make a soft landing.'),
'Peregrine M1':('A fuel leak ended the attempt','Deliver scientific payloads to the lunar surface.','A propulsion problem prevented a lunar landing. The spacecraft returned to Earth’s atmosphere.'),
'IM-1':('A landing with limitations','Deliver instruments and demonstrate a commercial lunar landing.','Reached the surface but tipped over, limiting communications and surface operations.'),
'IM-2':('A short surface mission','Deliver instruments to investigate the lunar south-polar region.','Landed on its side in a crater, severely limiting the planned surface science.'),
'Blue Ghost 1':('Science through a lunar day','Deliver and operate scientific instruments on the Moon.','Landed successfully and completed its surface mission in March 2025.'),
'Artemis I':('Orion’s uncrewed proving flight','Test the SLS rocket and Orion spacecraft around the Moon.','Completed an uncrewed lunar flight and returned safely to Earth.'),
'Artemis II':('People returned around the Moon','Test Orion with a crew during a lunar flyby.','Four astronauts flew around the Moon and returned safely to Earth in April 2026.')}
custom.update(json.loads((P/'data/editorial-additions.json').read_text()))
def dt(s):return parse(s.replace('Sept.','Sep.').replace('1//','1/').replace(',', ' '),fuzzy=True,default=datetime.datetime(2000,1,1)).date().isoformat()
def display(s):return datetime.date.fromisoformat(s).strftime('%-d %B %Y')
chbyn={d['number']:d for d in chron};catalog=[];corrections=[]
for i,r in enumerate(rows):
 raw,country,launch,arrival,typ,outcome=r['cells']
 if raw in exclude:continue
 name=short.get(raw,raw).replace("Chang'e",'Chang’e')
 ch=None
 if i in unnamed:name,num=unnamed[i];ch=chbyn[num]
 else:
  exact=[c for c in chron if raw in c['name'] or (name in c['name'] and len(name)>5)]
  if exact and not name.startswith('Apollo'):ch=exact[0]
 date=fixdates.get(raw,dt(launch))
 if i==15:date='1960-04-19'
 if raw in fixdates or i==15:corrections.append({'mission':name,'field':'Launch','source_value':launch,'value':date})
 if raw=='Lunar Orbi ter 1':ch=chbyn[71]
 if raw=='Pioneer P-3':ch=chbyn[13]
 if raw=='Pioneer P-30':ch=chbyn[17]
 if raw=='Pioneer P-31':ch=chbyn[20]
 if raw=='Luna 1':ch=chbyn[8]
 if raw=='Hiten':ch=chbyn[175]
 country_short=country.split(' (')[0];operator=country.split('(',1)[1].rstrip(')') if '(' in country else {'USA':'NASA','USSR':'Soviet space programme','India':'ISRO','Japan':'JAXA','China':'CNSA','Russia':'Roscosmos','Europe':'ESA','South Korea':'KARI'}.get(country,'Unavailable')
 if raw=='Pioneer 0':operator='US Air Force'
 if country=='Europe':country_short='Europe / ESA'
 if country=='USSR':country_full='Soviet Union'
 elif country_short=='USA':country_full='United States'
 else:country_full=country_short
 status='Failed' if 'unsuccessful' in outcome.lower() else 'Partial' if 'partial' in outcome.lower() else 'Successful'
 if name in ['IM-1','IM-2','Chandrayaan-2']:status='Partial'
 if name=='SLIM':status='Successful'
 if name in ['Lunar Orbiter 3','Lunar Orbiter 4']:status='Successful'
 if name=='Luna 21':typ='Lander / Rover'
 if name=='Luna E-6LS No.112':typ='Orbiter'
 if name=='Luna 11':status='Partial'
 if name=='Chandrayaan-2':typ='Orbiter / Lander / Rover'
 if raw=='ARTEMIS-THEMIS':typ='Orbiters'
 if name.startswith('Apollo'):typ='Crewed orbiter' if name in ['Apollo 8','Apollo 10'] else 'Crewed landing'
 if name=='Artemis II':typ='Crewed flyby'
 purpose={'Impact':'Send a probe toward the Moon for an intentional impact.','Orbiter':'Study the Moon from orbit.','Orbiters':'Study the Moon using orbiting spacecraft.','Lander':'Land instruments safely on the lunar surface.','Rover':'Explore the surface with a robotic rover.','Flyby':'Study the Moon during a close flyby.','Sample Return':'Collect lunar material and return it to Earth.','Orbiter/Sample Return':'Enter lunar orbit, collect samples and return them to Earth.','Sample Return Mission':'Collect lunar material and return it to Earth.','Lander, Rover':'Land a rover for surface exploration.','Lander and Rover':'Land instruments and a rover on the Moon.','Orbiter/Impact':'Study the Moon from orbit, with a later impact.','Orbiter/impactor':'Orbit and investigate the Moon.'}.get(typ,'Explore the Moon and demonstrate spacecraft technology.')
 result=outcome.replace('(Active Mission) ','')
 if result=='Unsuccessful':result='The main lunar objective was not achieved. A detailed failure explanation is unavailable in the summary record.'
 elif result.lower() in ['successful','success']:result='The source catalogue records the mission as successful.'
 elif result.lower()=='partial success':result='Some objectives were achieved, but the planned mission was not fully completed.'
 headline={'Successful':'A successful lunar mission','Partial':'Some objectives achieved','Failed':'The objective was not reached'}[status]
 if name in custom:headline,purpose,result=custom[name]
 if name.startswith('Lunar Orbiter'):
  headline='Surveying the Moon from orbit';purpose='Photograph the lunar surface for science and landing-site assessment.';result='Returned lunar photographs and achieved the mission’s core objectives.'
 if name.startswith('Apollo'):
  n=name.split()[-1]
  purpose='Explore the lunar surface, deploy experiments and return samples.'
  headline='Exploring the lunar surface';result='Astronauts landed, conducted surface science and returned safely to Earth.'
  if n=='8':headline='First people in lunar orbit';purpose='Test crewed lunar flight and orbit the Moon.';result='Three astronauts became the first people to orbit the Moon and returned safely.'
  if n=='10':headline='A rehearsal for landing';purpose='Rehearse lunar landing operations without touching down.';result='Tested the lunar module close to the surface and returned the crew safely.'
  if n=='11':headline='First footsteps on the Moon'
  if n=='13':headline='A safe return after crisis';purpose='Land astronauts on the Moon and collect samples.';result='An oxygen-tank failure forced the landing to be cancelled. The crew returned safely.'
 # Read history: direct mission page if available, else a matching PDF section; modern secondary histories audited separately.
 url=next((u for u in r['links'] if fetched.get(u,{}).get('status')==200 and '/mission/' in u),'')
 candidate='https://science.nasa.gov/mission/'+name.lower().replace(' ','-')+'/'
 if fetched.get(candidate,{}).get('status')==200:url=candidate
 if ch and not url:url=PDF+'#page='+str(ch['page'])
 if name=='Luna 3':url='https://www.nasa.gov/history/60-years-ago-luna-2-makes-impact-in-moon-race/'
 if name=='SLIM':url='https://global.jaxa.jp/press/2024/08/20240826-1_e.html'
 if name=='Chandrayaan-3':url='https://www.isro.gov.in/Chandrayaan3_Details.html'
 if name=='Artemis II':url='https://www.nasa.gov/mission/artemis-ii/'
 if name=='Blue Ghost 1':url='https://www.nasa.gov/news-release/nasa-science-continues-after-fireflys-first-moon-mission-concludes/'
 if name=='Hakuto-R M1':url='https://www.ispace-inc.com/mission-1/'
 if not url:
  slug={'Kaguya':'SELENE',"Chang’e 1":'Chang%27e_1',"Chang’e 2":'Chang%27e_2',"Chang’e 3":'Chang%27e_3',"Chang’e 4":'Chang%27e_4',"Chang’e 5":'Chang%27e_5',"Chang’e 6":'Chang%27e_6',"Chang’e 5-T1":'Chang%27e_5-T1','Queqiao':'Queqiao_relay_satellite','Danuri':'Danuri','Luna 25':'Luna_25','Peregrine M1':'Peregrine_Mission_One','IM-1':'IM-1','IM-2':'IM-2'}.get(name,name.replace(' ','_'))
  url='https://en.wikipedia.org/wiki/'+slug
 histnote='Mission history in English; NASA / agency source' if 'wikipedia' not in url else 'Mission history in English; Wikipedia (secondary source)'
 if '#page=' in url:histnote='NASA Deep Space Chronicle, PDF page '+url.split('=')[-1]+'; English'
 datearrival=''
 if arrival and arrival!='N/A' and len(arrival)>4:
  try:datearrival=dt(arrival)
  except:pass
 if name=='Ranger 6':datearrival='1964-02-02'
 if name=='Ranger 4':datearrival='1962-04-26'
 if name=='Ranger 5':datearrival='1962-10-21'
 if name=='SLIM':datearrival='2024-01-19'
 if name=='Hakuto-R M1':datearrival='2023-04-25'
 if name=='Chandrayaan-2':datearrival='2019-08-20'
 if name=='Luna E-3 No.2':datearrival=''
 if name=='Luna 15':datearrival='1969-07-17'
 if name=='Chandrayaan-1':datearrival='2008-11-08'
 # Fact highlights are mission-specific where documented, with honest fallback facts rather than invented metrics.
 days=(datetime.date.fromisoformat(datearrival)-datetime.date.fromisoformat(date)).days if datearrival else None
 h1='Unavailable' if days is None else str(days)+(' day' if days==1 else ' days')
 l1='encounter date in source' if not datearrival else 'between launch and event dates'
 h2='Robotic';l2='mission crew type'
 if name.startswith('Apollo'):h2='3';l2='astronauts aboard'
 if name=='Artemis II':h2='4';l2='astronauts aboard'
 if ch:
  m=re.search(r'Spacecraft Mass:\s*(.*?)\s*Mission Design',ch['text'])
  if m:
   mass=re.match(r'(?:c\.\s*)?([\d,.]+)\s*(kg|kilograms)',m[1])
   if mass:h2=('~' if m[1].startswith('c.') else '')+mass[1]+' kg';l2='mass incl. upper stage' if 'upper stage' in m[1] else 'spacecraft mass (source)'
 if name=='Luna 3':h1='29';l1='photographs taken';h2='~70%';l2='of the far side photographed'
 if name=='Luna 2':h1='First';l1='human-made object on the Moon'
 if name=='Luna 9':h1='First';l1='successful lunar soft landing'
 if name=='Luna 10':h1='First';l1='spacecraft in lunar orbit'
 if name=='GRAIL':h2='2';l2='spacecraft: Ebb and Flow'
 if name=='ARTEMIS probes':h1='2011';l1='entered lunar orbit';h2='2';l2='repurposed THEMIS probes'
 if name=='Ranger 7':h2='4,308';l2='photographs returned'
 if name=='Ranger 8':h2='7,137';l2='photographs returned'
 if name=='Ranger 9':h2='5,814';l2='photographs returned'
 m2label='Lunar encounter' if datearrival else 'No arrival recorded'
 # Arrival column mixes flyby, orbit insertion and landing; never infer landing from mission type.
 if name in ['Apollo 8','Apollo 10','Apollo 12','Apollo 14','Apollo 15','Apollo 16','Apollo 17','Chandrayaan-1','Chandrayaan-2','Luna 15']:m2label='Entered lunar orbit'
 if name=='Apollo 11':m2label='Moon landing'
 if name in ['SLIM','Hakuto-R M1','Blue Ghost 1','IM-1','IM-2','Chandrayaan-3']:m2label='Landing / attempt'
 if name=='Luna 3':m2label='Moon flyby'
 if name=='Chandrayaan-2':m2label='Entered lunar orbit'
 m3date='';m3label='No later date in source'
 if name=='Luna 3':m3date='1959-10-07';m3label='Photos taken'
 if name=='Artemis II':m3date='2026-04-10';m3label='Returned to Earth'
 if name=='SLIM':m3date='2024-08-23';m3label='Operations ended'
 if name=='Blue Ghost 1':m3date='2025-03-16';m3label='Surface mission ended'
 imageurl='https://science.nasa.gov/resource/first-close-up-of-the-far-side-of-moon/' if name=='Luna 3' else NASA
 d={'ID':f'M{i+1:03d}','Name':name,'FullName':raw if raw!='Unnamed Luna' else name,'LaunchDate':date,'LaunchDisplay':display(date),'Year':int(date[:4]),'Country':country_short,'CountryFull':country_full,'Operator':operator,'Status':status,'MissionType':typ,'Headline':headline,'Purpose':purpose,'Result':result,'Summary':result,'Highlight1':h1,'Highlight1Label':l1,'Highlight2':h2,'Highlight2Label':l2,'Milestone1Date':date,'Milestone1Label':'Launched','Milestone2Date':datearrival,'Milestone2Label':m2label,'Milestone3Date':m3date,'Milestone3Label':m3label,'ReadURL':url,'ReadingNote':histnote,'SecondURL':imageurl,'SecondLabel':'View original image ↗' if name=='Luna 3' else 'View source catalogue ↗','SourceURL':NASA,'SourceOutcome':outcome,'SourceLaunch':launch,'ReviewDate':'2026-10-11','ChronicleNumber':ch['number'] if ch else 0,'ChroniclePage':ch['page'] if ch else 0,'OperatingState':'Not tracked; outcome is distinct from current operations'}
 catalog.append(d)
catalog.sort(key=lambda x:(x['LaunchDate'],x['ID']))
for i,d in enumerate(catalog,1):d['Order']=i
(P/'data/catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False));(P/'data/exclusions.json').write_text(json.dumps(exclude,indent=2,ensure_ascii=False));(P/'data/corrections.json').write_text(json.dumps(corrections,indent=2))
print('records',len(catalog));print('status', {s:sum(d['Status']==s for d in catalog) for s in ['Successful','Partial','Failed','Ongoing']});print('history needing fetch',[(d['Name'],d['ReadURL']) for d in catalog if d['ReadURL'] not in fetched and '#page=' not in d['ReadURL']])
