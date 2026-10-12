# Catalogue and interpretation

Reviewed 11 October 2026. This is a finite portfolio dataset, not a live mission feed.

## Inventory and grain
The source inventory is NASA Science's [Moon Missions](https://science.nasa.gov/moon/missions/) table (123 rows in the captured snapshot). NASA describes this as major missions; the table omits some secondary payloads, launch attempts and recent missions. We retain 116 records after excluding Pioneer P-1's ground-pad accident and consolidating Lunokhod 1, Lunokhod 2, Yutu, PFS-1, PFS-2 and the Emirates Rashid rover into their carrier missions. This count must not be used as the total number of all launches toward the Moon. For example, CAPSTONE, Queqiao-2, Resilience, Lunar Trailblazer and some Zond-era attempts are outside this source inventory.

One icon denotes a **mission record**, not a unique booster launch or every spacecraft on that launch. GRAIL and ARTEMIS probes each represent a paired mission. ARTEMIS probes are sorted by their original THEMIS launch (2007); their lunar repurposing is explained in the detail panel. Multiple missions can share a launch vehicle, so summing icons is not a launch count. Country denotes the attributed mission country/organisation, not launch location; USSR is historical, and Europe/ESA is an organisational grouping.

## Outcomes
- Successful: the source's primary lunar objective was achieved. This does not require every subsystem or extended objective to succeed.
- Partial: meaningful objectives were achieved, while major intended objectives were not completed.
- Failed: the main intended lunar objective was not achieved.
- Ongoing: the outcome is pending. This is distinct from being operational after achieving success.

These are curated classifications, not a universal international taxonomy. The raw source outcome remains in `SourceOutcome`. Decisions that differ from the summary table: Chandrayaan-2 is partial at the combined orbiter/lander/rover grain; Luna 11 is partial because lunar imaging failed despite other science; Lunar Orbiters 3 and 4 are successful based on their detailed mission histories; SLIM is successful based on JAXA's assessment that its primary objectives were achieved. IM-1/IM-2 remain partial because surface operation was limited after landing. Planned missions are not included. There are no pending outcomes in the current selected inventory; successful missions can still be operating.

## Dates and highlights
Dates come from mission histories and the NASA summary. Launch dates are ISO-normalized, but the dashboard shows calendar dates, not times. Historical sources can use different civil-day conventions; the dataset does not claim timestamp-level UTC uniformity. Launch and arrival dates are not interchangeable. The milestone label says lunar encounter unless a more specific event is supported; Apollo orbit insertion is not labelled landing.

Documented corrections include Pioneer 3's 6 December 1958 launch; Luna E-3 No.2's 19 April 1960 launch; Ranger 4's 23 April 1962 launch; Ranger 5's 18 October 1962 launch; Ranger 6's 2 February 1964 arrival; Luna 15's 17 July 1969 orbit insertion; Chandrayaan-1's 8 November 2008 orbit insertion; Chang'e 3's 1 December 2013 launch; Blue Ghost 1's 15 January 2025 launch; ARTEMIS probes' 17 February 2007 original launch. Apollo 12's punctuation was normalized to preserve 1969 in the date parser. SLIM and Hakuto-R M1 display their landing/attempt milestones rather than orbit arrival dates. Source-specific corrections live in `prepare_catalog.py`; the raw launch text is retained per record.

The first highlight uses a documented special result where available; otherwise it is the number of **calendar days between launch and the displayed recorded event**, not total mission duration or precise transit time. Missing encounter dates say Unavailable. The second highlight uses documented spacecraft mass, images, crew/probe counts, or the known robotic crew type. A tilde marks an approximate value. Masses retain the historical NASA chronology's definitions (including upper stages where expressly identified), so they are descriptive facts, not an apples-to-apples spacecraft comparison. Unknown additional milestones are blank rather than invented.

Luna 3's 29 photographs and approximately 70% far-side coverage are taken from NASA's historical image description. That coverage is of the **far side**, not 70% of the whole Moon. It was a flyby camera mission, not a landing.

## Sources and links
- NASA Science mission catalogue and individual mission histories; mission pages are linked record by record.
- NASA [Deep Space Chronicle](https://science.nasa.gov/wp-content/uploads/2023/09/DSC_monograph24.pdf), numbered mission entries for early Soviet missions and spacecraft facts. PDF links use physical PDF page numbers; the reader may need to scroll to the numbered entry when a page contains several missions.
- JAXA's SLIM conclusion, ISRO's Chandrayaan-3 details, ispace's Mission 1 page, NASA Apollo/Artemis histories and NASA's Blue Ghost mission conclusion.
- Fourteen modern mission histories use Wikipedia as a clearly labelled secondary source. These were readable through the web retrieval tool; direct scripted requests received HTTP 403.

The detailed dated reading-link ledger records the destination, title, method and evidence for all 116 records. HTTP 200 alone was not treated as proof: legacy NSSDCA spacecraft URLs returned an error page and were replaced. The common second link is deliberately the source catalogue, not a claimed mission-specific photograph. Luna 3 has a separately verified original-image link.

## Visual interpretation
The coloured rocket is a consistent navigation symbol, not the actual launch vehicle. Dots and the status legend reinforce the same outcome; tooltips state it in words. Selection uses a neutral outline and does not replace the outcome colour.

The Moon is illustrative generated artwork. Trajectory overlays indicate the **mission type**, not reconstructed paths, landing sites or exact geometry. Failed missions are labelled as intended types. No visual trajectory implies a failed mission reached the Moon. The right panel's date is the selected mission launch date, while the footer's review date is the catalogue snapshot date.
