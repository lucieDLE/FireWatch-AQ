# ============================================================================
#  Panel Introduction to Air Quality and Fires in California
# ============================================================================
INTRO_SECTION_1_HOOK_1 = """ 
**California's wildfire season is lengthening.**
Historically, the fire season occurs between May and October, however recent data show the
season starting sooner and ending later each year.[1](https://wfca.com/wildfire-articles/california-fire-season-in-depth-guide/)
"""

INTRO_SECTION_1_HOOK_2 ="""
**The scale of destruction is accelerating.**
According to the California Department of Forestry and Fire Protection reports, 14 of the 20
most destructive wildfires in California history occurred in the last decade alone.[2](https://www.fire.ca.gov/-/media/calfire-website/our-impact/fire-statistics/top-20-destructive-ca-wildfires.pdf)
"""

INTRO_SECTION_1_HOOK_3 = """
**The consequences extend far beyond the fire perimeter.**
Smoke can travel hundreds to thousands of miles, and according to the EPA, the health risk from
wildfire smoke persists for several days after the heaviest smoke events subside.[3](https://www.epa.gov/air-research/wildland-fire-research-human-health)
"""
INTRO_DASHBOARD_PRESENTATION = """This dashboard examines the air quality consequences of the 2025
California fire season, tracing the link between fire activity and pollutant exposure across the state.
"""

INTRO_SECTION_2_CARD_1 = """ The U.S. Air Quality Index (AQI) is an index used for communicating outdoor
air quality to the public . It translates complex pollutant concentrations into a single value to inform
the public. It translates complex pollutant concentration measurements into a single number on a 
0–500 scale, divided into six color-coded categories, each corresponding to a specific level of health
concern. When multiple pollutants are measured at a site, the highest individual AQI is used to report 
the overall air quality for that day[4](https://www.airnow.gov/aqi/aqi-basics/).
<br><br>
The AQI is defined by the **[United States Environmental Protection Agency](https://www.epa.gov) (EPA)**
under the authority of the Clean Air Act (1990), and is tied directly to the **National Ambient Air 
Quality Standards (NAAQS)**. NAAQS are concentration thresholds for each pollutant, which the EPA is required
to review every five years.
<br><br>
It is worth noting that other countries operate their own indices under different rules and pollutant sets. 
The **World Health Organization (WHO)** publishes separate guidelines that are stricter than NAAQS for several 
pollutants.[5](https://www.who.int/publications/i/item/9789240034228)[6](https://en.wikipedia.org/wiki/Air_quality_index)

"""


INTRO_SECTION_3_PM = """
Inhalable particles suspended in the air, composed of complex mixtures with diverse chemical and physical characteristics.

Classified by aerodynamic diameter, with PM2.5 and PM10 the most relevant for health monitoring.

The smaller the particle, the deeper it penetrates the respiratory system, making size the primary determinant of health impact[5](https://www.who.int/publications/i/item/9789240034228)[7](https://www.who.int/teams/environment-climate-change-and-health/air-quality-and-health/health-impacts/types-of-pollutants)
"""


INTRO_SECTION_3_PM25 = """
* Under 2.5 µm
* Primary fire smoke tracer
* Penetrates deep into lungs and enters bloodstream
"""

INTRO_SECTION_3_PM10 = """
* Between 2.5 µm and 10 µm
* Wider range of sources than PM2.5
* Less precise as a fire tracer
"""

INTRO_SECTION_3_O3 = """
* Formed when sunlight reacts with volatile organic compounds, CO, NOx from vehicles
* Peaks in hot summers
* No safe exposure level
"""

INTRO_SECTION_3_NO2 = """
* Produced by high-temperature combustion (heating, transport, industry)
* Important ozone precursor
* Amplifies smog formation
"""

INTRO_SECTION_3_CO = """
* From incomplete combustion of fuels
* Predominant ambient source is motor vehicles
"""

INTRO_SECTION_3_SO2 = """
* Released from burning fuels (heating, industry, power generation)
* Irritates airways
"""


INTRO_SECTION_5_WHY = [
"""
California presents one of the most complex and consequential air quality challenges in the United States[8-12]:

* The Central Valley (Fresno, Bakersfield) and South Coast (Los Angeles, San Diego) experience some of the highest air pollution levels in the entire United States.
* 5 of the 10 US cities most polluted (has improved since 2015)
* 88% of Californians live in a community with unhealthy air

Three structural factors drive it:
"""
]
INTRO_SECTION_5_FACTOR_1 = """
**Transportation**
* California's large population generate substantial vehicle emissions. 
* It is known that vehicles powered wby fossil fuels contributes significantly to pollution.
* The state has responded with the most aggressive zero-emission vehicle policy in the US, but the transition is ongoing.
"""

INTRO_SECTION_5_FACTOR_2 = """
**Climate**
* A warm, dry climate with low annual rainfall creates ideal conditions for both wildfire ignition and ozone formation. T
* The Central Valley experiences extremely hot, dry summers with intensifying drought, extending the fire season and amplifying heat-driven ozone peaks. 
* Wildfire activity has increased sharply as conditions become hotter and drier.
"""
INTRO_SECTION_5_FACTOR_3 = """
**Geography**
* Many of California's largest cities sit in basins enclosed by mountain ranges (Los Angeles, San Diego, Fresno). Mountains trap air pollution .
* The surrounding mountains block horizontal wind dispersal, preventing the warm polluted air from rising and escaping.
"""

# ============================================================================
#  Panel AIR ANALYSIS:
# ============================================================================

PANEL_AIR_OVERVIEW= """
This panel characterizes the national air quality monitoring landscape in 2025, combining three views:
the air quality monitoring coverage by state and pollutant, the geographic distribution of standard 
exceedances at county level, and a pollutant-by-pollutant comparison between the six most and least 
polluted states. 
"""

PANEL_AIR_CARD_MONITORS_1 = [ """Monitoring density is highly uneven across the country""", 
"""
California alone accounts for the largest share of daily monitoring records in 2025, and lower-coverage
states like Vermont, Rhode Island, or Puerto Rico. This reflects two factors: 1) California is one of
the most polluted states in the US [[1](https://en.wikipedia.org/wiki/Pollution_in_California)] and 2) invested heavily in monitoring
infrastructure to track and improve its air quality. 
"""
]


PANEL_AIR_CARD_MONITORS_2 = [ """Ozone and PM 2.5 are the two most monitored pollutant""", 
"""
They are known to be the deadliest and most widespread air pollutants in the US, driving the majority
of pollution-attributable disease and premature mortality[[2]
(https://www.stateofglobalair.org/sites/default/files/documents/2024-06/soga-2024-report_0.pdf)].
"""
]

PANEL_AIR_CARD_MAP = ["""A strong southwest cluster""",
"""
California, Arizona, and Texas account for the largest number and size of orange bubbles, confirming
their designation as worst-performing states. Exceedances in California are clustered in two zones: 
the Central Valley (Fresno, Kern, Tulare counties), and Southern California (Los Angeles, San Bernardino,
Riverside). By contrast, the best-performing states (Washington, Idaho, and Mississippi) show 
predominantly green bubbles with few or no exceedance records.
"""
]


PANEL_AIR_CARD_BOXPLOT_1 = ["""PM2.5 and ozone are the primary drivers""",
"""
California's PM2.5 distribution is the most skewed of any state shown: The upper quartile extends well
beyond it and extreme outliers reach above 250 µg/m³, which are consistent with acute wildfire smoke
events. However the Ozone median daily maximum is already at or above the 0.07 ppm threshold, meaning
exceedances are not driven by isolated spikes but by a structural, persistent elevation across the 
measurement period. Texas and Arizona show a similar ozone pattern, consistent with high solar radiation
and precursor emissions from petrochemical and transportation sources respectively.
"""
]

PANEL_AIR_CARD_BOXPLOT_2 = ["""NO, SO, CO present no risk""",
"""
Three pollutants show effectively no exceedance risk in any of the six states. Carbon monoxide, sulfur
and nitrogen dioxide stays well under NAAQS threshold, showing that the air quality burden is driven 
by ozone and fine particulate matter (PM10 and PM2.5).
"""
]

PANEL_AIR_CARD_NOTE=[ """A note on interpretation""", 
""" 
"Best-performing" state status reflects the aggregate performance of existing monitoring sites, it 
does not guarantee clean air everywhere within that state. Sparse monitoring networks can miss 
localized hotspots entirely, whether near industrial facilities, busy highways, or wildfire-prone 
areas with no nearby sensor. The absence of exceedance records in a state is not proof of clean air,
it may simply reflect the absence of a monitor in specific place."""
]


# ============================================================================
#  Panel 2: FIRE ANALYSIS
# ============================================================================

PANEL_FIRE_OVERVIEW=""" 
Panel 2 examines California's 2025 wildfire season through two lenses: the spatial distribution of 
fire intensity across counties, and the signature of each major fire event on air pollutants. The 
central finding is that fires do not affect all pollutants equally and that PM2.5 is the most direct 
and sensitive indicator of wildfire smoke.
"""


PANEL_FIRE_CARD_COUNTY=[ """Most fire events are geographically concentrated""", 
""" 
The map shows fire activity score (weighted by fire category and intensity) peaking sharply in
Fresno, San Luis Obispo, and Santa Barbara counties. Los Angeles county's score is moderate despite
hosting the Palisades and Eaton fires. This reflects the weighting by fire category: large, 
high-radiative power fires burning through wildland vegetation in the central Sierra Nevada dominate
the score metric over the faster-moving but shorter-lived LA fires.
"""
]

PANEL_FIRE_CARD_TOP10=[ """The top 10 fires are distributed across four distinct county""", 
f""" 
At roughly 130,000 estimated burnt acres, Gifford (Santa Barbara) is nearly 60\% larger than the 
second-ranked Madre fire (San Luis Obispo, ~80,000 acres) and more than twice the size of Garnet 
(Fresno, ~60,000 acres). The remaining fires (SALT 14-2, Palisades, Butler, Green, Eaton, Dillon, Hughes)
cluster tightly in the 10,000–25,000 acre range. This long-tailed distribution has an important 
signification: a small number of extreme events account for the majority of total burnt area, while
most fire events are comparatively minor by size. It also highlights that burnt area is a poor metric 
for human impact: for example the Palisades fire caused billions in structural damage despite ranking 
fifth by area.
"""
]

PANEL_FIRE_BOXPLOT_PM25=[ """PM2.5 is the most fire responsive pollutant""", 
""" 
The 99th percentile PM2.5 AQI tracks fire events more precisely than any other pollutant, with clean
spikes at Palisades (January, 8th), and a dramatic peak during the Garnet period (September) that 
exceeds 250 AQI. With the median and Q1–Q3  low and stable throughout the year, confirm that these 
extremes are spatially concentrated near fire sites rather than a statewide baseline shift.
"""
]


PANEL_FIRE_BOXPLOT_PM10=[ """PM10 displays year-round volatility""", 
""" 
Unlike PM2.5, the PM10 99th percentile shows frequent sharp spikes throughout January, March, May, 
and November (periods with no significant fire activity). This reflects PM10's broader source profile: 
agricultural tillage, road dust, construction, and desert wind events all contribute coarse particles 
that PM2.5 monitoring would not capture. The Palisade event do appear in PM10, but the signal is not 
as separable as for PM2.5. This is for this reason, that for fire impact analysis, we will primarily 
focus on PM2.5."""
]

PANEL_FIRE_BOXPLOT_O3=[ """Ozone levels are mostly driven by seasonality""",
""" 
The ozone curve is the most visually distinct of the four: it rises steadily from a winter floor of
~25-50 AQI in January to sustained peaks above 150–190 AQI from June through September, then falls 
sharply back toward baseline in October. This pattern is driven by solar radiation intensity and 
temperature not by fire occurrence. The January Palisades fire produces zero visible ozone response. 
The summer fire cluster (Madre, Gifford, Garnet) coincides with ozone's seasonal maximum, making it 
impossible to detects if fire has an effect on ozone (or the opposite) fire amplification from background 
photochemical production without a counterfactual model.
"""
]

POLLUTANT_PANEL_MAP = {
    'PM2.5': PANEL_FIRE_BOXPLOT_PM25,
    'PM10':  PANEL_FIRE_BOXPLOT_PM10,
    'Ozone': PANEL_FIRE_BOXPLOT_O3,
}

# ============================================================================
#  Panel 3: EVENT ANALYSIS
# ============================================================================

PANEL_EVENT_OVERVIEW_PREAMBLE = """
This panel provides an event-level deep dive into individual California wildfires and their measurable
impact on nearby air quality monitoring stations. Select a fire event from the dropdown to load its
perimeter map, fire progression timeline, and AQI curves from the two nearest monitoring zones.
The map shows the fire perimeter evolving day by day alongside the AQI color-coded readings at each
monitoring station. The burning area and fire perimeter chart below quantifies fire growth and contraction over the event window.
The two AQI time series on the right show how individual monitoring sites responded to the fire within each zone.
Reading the two zones together reveals the smoke transport direction:
"""

PANEL_EVENT_OVERVIEW_FIRES = """Four fires are available :
- Gifford (August, Santa Barbara)
- Madre (July, San Luis Obispo coast),
- Garnet (September, Fresno) .
- Palisades (January, Los Angeles basin)
"""

PANEL_EVENT_OVERVIEW_ABBREVIATIONS = """**Abbreviations:**
- San Luis Obispo (SLO)
- Los Angeles (LA)
- Santa Barbara (SB)
"""



#  Palisades
PANEL_EVENT_PALISADES_DESCRIPTION=[ """ EVENT DESCRIPTION """, 
""" 
The Palisades fire ignited on January 7, 2025 in the Pacific Palisades neighborhood of Los Angeles, 
driven by extreme Santa Ana wind conditions. It represents the first major air quality event of the 
2025 fire season and the only significant wintertime fire in the dataset. Two monitoring zones are 
tracked: Los Angeles basin (primary impact zone) and San Luis Obispo/Santa Barbara (reference zone).
"""
]


PANEL_EVENT_PALISADES_ANALYSIS_SITE_1=[ """The AQI response in LA was fast, severe, and spatially contained""", 
""" 
All six LA basin monitoring sites spiked sharply between January 8 and 10, reaching peaks of 150-175
AQI ("unhealthy for all" category), before returning rapidly to baseline levels by January 12-13. 
Pasadena and LA-North Main Street recorded the highest values. Coastal sites like Signal Hill and 
West Los Angeles peaked lower (~100-125).

It has been reported that the very high PM2.5, were mostly coming from lead
[2][https://www.cdc.gov/mmwr/volumes/74/wr/mm7405a4.htm?s_cid=mm7405a4_w] due to building, pipes, 
electronic equipment having lead paint.
"""
]


PANEL_EVENT_PALISADES_ANALYSIS_SITE_2=[ """ The SLO/SB reference zone shows near-zero response throughout the entire event. """, 
""" 
All six SLO/SB monitors remained flat between 10-40 AQI across the full observation window, a clean
confirmation that the Palisades smoke plume was carried into the LA basin."""
]


#  Madre
PANEL_EVENT_MADRE_DESCRIPTION=[ """ EVENT DESCRIPTION """, 
""" 
The Madre fire burned in San Luis Obispo County along the Los Padres National Forest boundary starting
in the first week of July. It is geographically positioned between the two monitoring zones: 
SLO/Santa Barbara to the northwest and Los Angeles to the southeast. The fire coincides with the July 4th
national holiday, introducing a significant confounding source for one monitoring zone.
"""
]


PANEL_EVENT_MADRE_ANALYSIS_SITE_1=[ """The SLO/Santa Barbara monitors show a moderate, fire-consistent response""", 
""" 
Most sites saw gradual increase from july 2nd to a broad peak of ~55–65 AQI around July 4–5, then 
declined steadily through July 7–8 as the fire was contained (see perimeter). This gradual elevation 
profile is the expected signature of a nearby fire burning at moderate intensity. No SLO/SB site 
breached the "unhealthy for sensitive groups" which meand the fire had little impact on the population.
"""
]


PANEL_EVENT_MADRE_ANALYSIS_SITE_2=[ """Los Angeles monitors show mixed response""", 
""" 
Most sites shows a sharp, high-amplitude spike specifically on July 5, with West Los Angeles and 
Compton reaching 160+ AQI ( "unhealthy for all" category), before collapsing back to ~50 by July 7. 
The critical detail is that this spike is concentrated on July 4–5 and is not preceded by a gradual 
rise the way the SLO monitors are. July 4th fireworks are a well-documented annual driver of acute 
PM2.5 and PM10 elevation in the LA basin, and the timing of this spike is essentially indistinguishable 
from that source. It cannot be cleanly attributed to the Madre fire without ruling out the holiday 
effect via a year-over-year comparison of July 4–5 LA AQI on non-fire years. The SLO signal is more 
analytically trustworthy for characterizing the Madre fire's direct air quality impact.
"""
]

#  Gifford
PANEL_EVENT_GIFFORD_DESCRIPTION=[ """ EVENT DESCRIPTION """,
"""
The Gifford fire in Santa Barbara County was the largest fire of the 2025 California season by
estimated burnt area (~130,000 acres). It burned through late July and August two weeks after the
Madre fire and in the same location but at a much larger scale. The panel covers July 31–August 22,
centered on the fire's active phase, with the same two monitoring zones as Madre: SLO/Santa Barbara
(proximate) and Los Angeles (distal).
"""
]


PANEL_EVENT_GIFFORD_ANALYSIS_SITE_1=[ """Despite being the largest fire of the season, Gifford produced the least local AQI impact""",
"""
SLO/SB monitors began elevated at ~30–40 AQI from the very start of the observation window (July 31),
rising to a broad peak of ~60–65 around August 3–6 without breaking into the unhealthy for sensitive
group category. This shows small smoke exposure rather than the sharp catastrophic spikes seen in
other events."""
]


PANEL_EVENT_GIFFORD_ANALYSIS_SITE_2=[ """Los Angeles monitors show sustained moderate elevation with no dramatic spikes""",
"""
LA sites ranged between 50-75 AQI throughout August 3–12, with no site breaching the "unhealthy
for sensitive groups" threshold during this window. The temporal pattern tracks loosely with the
SLO sites, suggesting some smoke transport southeastward, but the LA signal is too small to
attribute it to Gifford alone given the basin's persistent summer background pollution.
"""
]


# Garnet
PANEL_EVENT_GARNET_DESCRIPTION=[ """ EVENT DESCRIPTION """,
"""
The Garnet fire burned in Fresno County in end of August 2025, reaching approximately 60,000 estimated
acres. Its geographic position places it between two fundamentally different atmospheric environments:
the Central Valley (Fresno basin, to the west) and the Owens Valley / Inyo county high desert (to the east).
The contrast between these two monitoring zones produces the most analytically striking spatial asymmetry
in the dataset.
"""
]


PANEL_EVENT_GARNET_ANALYSIS_SITE_2=[ """The Owens Valley monitors experienced a catastrophic AQI spike""",
"""
The Owens Valley monitors experienced a catastrophic AQI spike. On September 7, the Sierra National Forest
monitoring zone spiked to 275+ AQI, deeply into the "hazardous" range, before collapsing back to 10-20 by
September 12–14. The spike is essentially instantaneous in onset and recovers almost as sharply. This
profile could be triggered by a rapid change in wind direction.
"""
]


PANEL_EVENT_GARNET_ANALYSIS_SITE_1=[ """The Fresno monitors, despite being in the same county as the fire, showed little impact""",
"""
Six Fresno basin sites peaked at approximately 75-85 AQI around September 7–9, reaching "unhealthy
for sensitive groups," but an order of magnitude lower than the other site.

This spatial asymmetry can be driven by different wind pattern, elevation, and terrain topology,
which are not the scope of this project.
"""
]

FIRE_EVENT_PANEL_MAP = {
    'PALISADES': (PANEL_EVENT_PALISADES_DESCRIPTION, PANEL_EVENT_PALISADES_ANALYSIS_SITE_1, PANEL_EVENT_PALISADES_ANALYSIS_SITE_2),
    'Madre':     (PANEL_EVENT_MADRE_DESCRIPTION,     PANEL_EVENT_MADRE_ANALYSIS_SITE_1,     PANEL_EVENT_MADRE_ANALYSIS_SITE_2),
    'Gifford':   (PANEL_EVENT_GIFFORD_DESCRIPTION,   PANEL_EVENT_GIFFORD_ANALYSIS_SITE_1,   PANEL_EVENT_GIFFORD_ANALYSIS_SITE_2),
    'Garnet':    (PANEL_EVENT_GARNET_DESCRIPTION,    PANEL_EVENT_GARNET_ANALYSIS_SITE_1,    PANEL_EVENT_GARNET_ANALYSIS_SITE_2),
}


SOURCES_MD = """
**[1]** California fire season guide — [wfca.com](https://wfca.com/wildfire-articles/california-fire-season-in-depth-guide/)

**[2]** CalFire — Top 20 Most Destructive California Wildfires — [fire.ca.gov](https://www.fire.ca.gov/-/media/calfire-website/our-impact/fire-statistics/top-20-destructive-ca-wildfires.pdf)

**[3]** EPA — Wildland Fire Research: Human Health — [epa.gov](https://www.epa.gov/air-research/wildland-fire-research-human-health)

**[4]** AirNow — AQI Basics — [airnow.gov](https://www.airnow.gov/aqi/aqi-basics/)

**[5]** WHO — Air Quality Guidelines 2021 — [who.int](https://www.who.int/publications/i/item/9789240034228)

**[6]** Wikipedia — Air Quality Index — [wikipedia.org](https://en.wikipedia.org/wiki/Air_quality_index)

**[7]** WHO — Types of Pollutants — [who.int](https://www.who.int/teams/environment-climate-change-and-health/air-quality-and-health/health-impacts/types-of-pollutants)

**[8]** EPA — California Air & Transportation Initiative (CATI) — [epa.gov](https://www.epa.gov/cati/about)

**[9]** American Lung Association — California State of the Air 2025 — [lung.org](https://www.lung.org/getmedia/3575a218-b54e-4dfe-8d91-892276870a14/california-sota-2025-fact-sheet.pdf)

**[10]** Earth.org — Air Pollution in California — [earth.org](https://earth.org/air-pollution-in-california)

**[11]** Wikipedia — Pollution in California — [wikipedia.org](https://en.wikipedia.org/wiki/Pollution_in_California)

**[12]** Wikipedia — San Joaquin Valley — [wikipedia.org](https://en.wikipedia.org/wiki/San_Joaquin_Valley)
"""