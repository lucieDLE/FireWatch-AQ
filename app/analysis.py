# ============================================================================
#  Panel Introduction to Air Quality and Fires in California
# ============================================================================
INTRO_SECTION_1_HOOK_1 = """ 
**California's wildfire season is lengthening.**

Historically, the fire season occurs between May and October, however recent data show the
season starting sooner and ending later each year[1](https://wfca.com/wildfire-articles/california-fire-season-in-depth-guide/).
"""

INTRO_SECTION_1_HOOK_2 ="""
**The scale of destruction is accelerating.**

According to the California Department of Forestry and Fire Protection, 14 of the 20
most destructive wildfires occurred in the last decade[2](https://www.fire.ca.gov/-/media/calfire-website/our-impact/fire-statistics/top-20-destructive-ca-wildfires.pdf).
"""

INTRO_SECTION_1_HOOK_3 = """
**The consequences extend far beyond the fire perimeter.**

Wildfire smoke can travel hundreds to thousands of miles, and the health risk can persists for several days
after a fire event[3](https://www.epa.gov/air-research/wildland-fire-research-human-health).
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
pollutants.[5](https://www.who.int/publications/i/item/9789240034228),[6](https://en.wikipedia.org/wiki/Air_quality_index)

"""


INTRO_SECTION_3_PM = """
* Inhalable particles suspended in the air, composed of complex mixtures with diverse chemical and physical characteristics.
* Classified by diameter, with PM2.5 and PM10 the most relevant for health monitoring.
* The smaller the particle, the deeper it penetrates the respiratory system[5](https://www.who.int/publications/i/item/9789240034228),[7](https://www.who.int/teams/environment-climate-change-and-health/air-quality-and-health/health-impacts/types-of-pollutants)
"""


INTRO_SECTION_3_PM25 = """
* Under 2.5 µm
* Primary fire smoke tracer
* Penetrates into lungs and bloodstream
"""

INTRO_SECTION_3_PM10 = """
* Between 2.5 µm and 10 µm
* Wider range of sources than PM2.5
* Less precise as a fire tracer
"""

INTRO_SECTION_3_O3 = """
* Formed when sunlight reacts with VOCs, CO, NOx from vehicles
* Peaks in hot summers
* No safe exposure level
"""

INTRO_SECTION_3_NO2 = """
* Produced by high-temperature combustion
* Important ozone precursor
* Amplifies smog formation
"""

INTRO_SECTION_3_CO = """
* Incomplete combustion of fuels
* Predominant source is motor vehicles
* Reduces oxygen delivery
"""

INTRO_SECTION_3_SO2 = """
* Released from burning fuels
* Creates P2.5 if chemical reaction
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
* Large population generate vehicle emissions
* Vehicles powered by fossil fuels contributes to pollution
* Has responded with zero-emission vehicle policy
"""

INTRO_SECTION_5_FACTOR_2 = """
**Climate**
* Warm, dry climate with low rainfall 
* Perfect conditions for wildfire ignition and ozone formation
* Wildfire activity has increased sharply
"""
INTRO_SECTION_5_FACTOR_3 = """
**Geography**
* Many large cities sit in basins enclosed by mountains
* Mountains block horizontal wind dispersal
* Prevents the warm polluted air from rising and escaping
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
California alone accounts for the largest share of daily monitoring records in 2025. This reflects two factors: 
1) California is one of the most polluted states in the US[11](https://en.wikipedia.org/wiki/Pollution_in_California) 
and 2) invested heavily in monitoring infrastructure to track and improve its air quality.
"""
]


PANEL_AIR_CARD_MONITORS_2 = [ """Ozone and PM2.5 are the most monitored pollutant""", 
"""
They are known to be the deadliest and most widespread air pollutants in the US, driving the majority
of pollution-attributable disease and premature mortality[13](https://www.stateofglobalair.org/sites/default/files/documents/2024-06/soga-2024-report_0.pdf).
"""
]

PANEL_AIR_CARD_MAP = ["""A strong southwest cluster""",
"""
California, Arizona, and Texas account for the largest number and size of orange bubbles, confirming
their designation as worst-performing states. 

Exceedances in California are clustered in two zones: 
the Central Valley (Fresno, Kern, Tulare counties), and Southern California (Los Angeles, San Bernardino,
Riverside). 

By contrast, the best-performing states (Washington, Idaho, and Mississippi) show 
predominantly green bubbles with few or no exceedance records.
"""
]


PANEL_AIR_CARD_BOXPLOT_1 = ["""PM2.5 and ozone are the primary drivers""",
"""
California's PM2.5 distribution extremely skewed: The 4th quartile extends well
beyond the limit threshold and extreme outliers reach almost 100 µg/m³. 
However, the Ozone median is almost at the 0.07 ppm threshold, meaning
exceedances are not driven by isolated spikes but by a structural, persistent pollution. 
Texas and Arizona show similar ozone and PM2.5 patterns, consistent with high solar radiation
and emissions from petrochemical and transportation sources.
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
The map shows fire activity score peaking sharply in Fresno, San Luis Obispo, and Santa Maria counties. 
Los Angeles county's score is moderate despite hosting the Palisades and Eaton fires. 

This reflects the fire category: large fires burning through wildland vegetation dominate
the score metric over the faster-moving but shorter-lived LA fires.
"""
]

PANEL_FIRE_CARD_TOP10=[ """The top 10 fires are distributed across four distinct county""", 
f""" 
At roughly 130,000 estimated burnt acres, Gifford (Santa Maria) is nearly 60\% larger than
the Madre fire (San Luis Obispo, ~80,000 acres) and more than twice the size of Garnet 
(Fresno, ~60,000 acres). The remaining fires cluster tightly in the 10,000–25,000 acre range. 

This long-tailed distribution shows that a small number of extreme events account for the majority
of total burnt area, while most fire events are comparatively minor by size. 

It also highlights that burnt area is a poor metric for human impact: Palisades fire caused billions 
in structural damage despite ranking fifth by area.
"""
]

PANEL_FIRE_BOXPLOT_PM25=[ """PM2.5 is the most fire responsive pollutant""", 
""" 
The 99th percentile PM2.5 AQI tracks fire events more precisely than any other pollutant, with clean
spikes at Palisades (January, 8th) Garnet period (September.

With the median and Q1–Q3  low and stable throughout the year, confirm that these 
extremes are spatially concentrated near fire sites rather than a statewide baseline shift.
"""
]


PANEL_FIRE_BOXPLOT_PM10=[ """PM10 displays year-round volatility""", 
""" 
Unlike PM2.5, the PM10 99th percentile shows frequent sharp spikes throughout periods with 
and without significant fire activity.

This reflects PM10's broader source profile: agricultural tillage, road dust, construction, 
and desert wind events all contribute coarse particles that PM2.5 monitoring would not capture.
"""
]

PANEL_FIRE_BOXPLOT_O3=[ """Ozone levels are mostly driven by seasonality""",
""" 
The ozone curve is the most visually distinct: it rises steadily from January to sustained peaks
above 150–190 AQI between June and September, then falls back in October. 

This pattern is driven by solar radiation intensity and temperature not by fire occurrence. 
The January Palisades fire produces zero visible ozone response. The summer fire cluster (Madre, Gifford, Garnet)
coincides with ozone's seasonal maximum, making it impossible to detects if fire has an effect on ozone (or the opposite).
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
- Gifford (August, Santa Maria)
- Madre (July, San Luis Obispo coast),
- Garnet (September, Fresno) .
- Palisades (January, Los Angeles basin)
"""

PANEL_EVENT_OVERVIEW_ABBREVIATIONS = """**Abbreviations:**
- San Luis Obispo (SLO)
- Los Angeles (LA)
- Santa Maria (SM)
"""



#  Palisades
PANEL_EVENT_PALISADES_DESCRIPTION=[ """ EVENT DESCRIPTION """, 
""" 
The Palisades fire ignited on January 7, 2025 in the Pacific Palisades neighborhood of Los Angeles, 
driven by extreme wind conditions. It represents the first major air quality event of the 
2025 fire season. Two monitoring zones are tracked: Los Angeles basin (primary impact zone) 
and San Luis Obispo/Santa Maria (reference zone).
"""
]


PANEL_EVENT_PALISADES_ANALYSIS_SITE_1=[ """The AQI response in LA was fast, severe, and spatially contained""", 
""" 
All six LA sites spiked sharply between January 8 and 10, reaching peaks of 150-175
AQI ("unhealthy for all" category), before returning rapidly to baseline levels by January 12-13. 
Pasadena and LA-North Main Street recorded the highest values.

It has been reported that the very high PM2.5, were mostly coming from lead[14](https://www.cdc.gov/mmwr/volumes/74/wr/mm7405a4.htm?s_cid=mm7405a4_w) due to building, pipes,
electronic equipment having lead paint.
"""
]


PANEL_EVENT_PALISADES_ANALYSIS_SITE_2=[ """ The SLO/SM reference zone shows near-zero response throughout the entire event. """, 
""" 
All six SLO/SM monitors remained flat between 10-40 AQI across the full observation window, a clean
confirmation that the Palisades smoke plume was carried into the LA basin."""
]


#  Madre
PANEL_EVENT_MADRE_DESCRIPTION=[ """ EVENT DESCRIPTION """, 
""" 
The Madre fire burned in San Luis Obispo County in the first week of July. 
It is geographically positioned between the two monitoring zones: 
SLO/Santa Maria to the northwest and Los Angeles to the southeast. 

The fire coincides with the July 4th
national holiday, introducing a significant confounding source for one monitoring zone.
"""
]


PANEL_EVENT_MADRE_ANALYSIS_SITE_1=[ """The SLO/Santa Maria monitors show a moderate, fire-consistent response""", 
""" 
Most sites saw gradual increase from july 2nd to a broad peak of ~55–65 AQI around July 4–5, then 
declined steadily through July 7–8. This gradual increase/decrease is the expected signature of a 
nearby fire burning at moderate intensity. No SLO/SM site 
breached the "unhealthy for sensitive groups" which means the fire had little impact on the population (near monitoring sites).
"""
]


PANEL_EVENT_MADRE_ANALYSIS_SITE_2=[ """Los Angeles monitors show mixed response""", 
""" 
Most sites shows a sharp, high-amplitude spike specifically on July 5, with West Los Angeles and 
Compton reaching 160+ AQI ( "unhealthy for all" category), before collapsing back to ~50 by July 7. 

The spike is concentrated on July 4–5 and is not preceded by a gradual 
rise like the SLO monitors are. July 4th fireworks are a well-documented annual driver of acute 
PM2.5 and PM10 elevation, the spike cannot be cleanly attributed to the Madre fire without ruling out the holiday. 
"""
]

#  Gifford
PANEL_EVENT_GIFFORD_DESCRIPTION=[ """ EVENT DESCRIPTION """,
"""
The Gifford fire in Santa Maria County was the largest fire of the 2025 by
estimated burnt area (~130,000 acres). It burned two weeks after the
Madre fire and in the same location but at a much larger scale. The panel covers July 31–August 22,
with the same two monitoring zones as Madre: SLO/Santa Maria and Los Angeles.
"""
]


PANEL_EVENT_GIFFORD_ANALYSIS_SITE_1=[ """Despite being the largest fire of the season, Gifford produced the least local AQI impact""",
"""
SLO/SM monitors began at ~30–40 AQI rising to a broad peak of ~60–65 around August 3–6 without 
breaking into the unhealthy for sensitive group category. This shows small smoke exposure (near monitoring sites)
rather than sharp spikes seen in other events, highlighting a possible wind/geographic effect on smoke transport."""
]


PANEL_EVENT_GIFFORD_ANALYSIS_SITE_2=[ """Los Angeles monitors show sustained moderate elevation with no dramatic spikes""",
"""
LA sites ranged between 50-75 AQI throughout August 3–12, with no site breaching the "unhealthy
for sensitive groups" threshold during this window. The temporal pattern tracks loosely with the
SLO sites, suggesting a possible smoke transport, but the LA signal is too small to
attribute it to Gifford alone given the basin's persistent summer background pollution.
"""
]


# Garnet
PANEL_EVENT_GARNET_DESCRIPTION=[ """ EVENT DESCRIPTION """,
"""
The Garnet fire burned in Fresno County in end of August 2025, reaching approximately 60,000 acres.
Its geographic position places it between two fundamentally different atmospheric environments:
the Central Valley (Fresno basin, to the west) and the Owens Valley / Inyo county high desert (to the east).
The contrast between these two monitoring zones produces the most analytically striking spatial asymmetry
in the dataset.
"""
]


PANEL_EVENT_GARNET_ANALYSIS_SITE_2=[ """The Owens Valley monitors experienced a catastrophic AQI spike""",
"""
The Owens Valley monitors experienced a huge AQI spike. On September 7, the Sierra National Forest
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


PANEL_EVENT_PALISADES_SATELLITE=[""" Palisades Fire """, 
"""
The satellite imagery confirms the previous analysis and offers an explanation for the city's relatively rapid AQI recovery: 
prevailing winds carried the smoke plume offshore over the Pacific Ocean, effectively ventilating the LA basin. 

Without this favorable wind pattern, the dense smoke visible in the imagery would likely have stayed in LA far longer.
"""
]

PANEL_EVENT_MADRE_SATELLITE=[""" Madre Fire """, 
"""
The satellite imagery confirm the previous analysis: the smoke plume remains concentrated over the SLO/Santa Maria
corridor throughout the event. 

The elevated AQI readings observed in Los Angeles during this period appear attributable
to July 4th fireworks rather than wildfire smoke transport, as the imagery shows no smoke plume reaching the LA basin.
"""
]

PANEL_EVENT_GIFFORD_SATELLITE=["""Gifford Fire """, 
"""
Gifford stands out as the most complex event in this study. Several observations emerge from the imagery:

- The wind direction shifted repeatedly throughout the event, causing the smoke plume to change trajectory across multiple days. 
Plume density varied significantly, with notably heavier smoke visible on August 3rd and during the August 10–12 period compared to other days.

- Most intriguing, the plume visibly reaches the SLO/Santa Maria area on certain days, yet this does not show on the monitor readings.
It does raise questions about whether the smoke was at higher altitudes, or whether the monitors missed the smoke.

- Finally, the imagery suggests that a 3rd monitoring site positioned between the two existing stations could have captured smoke impacts around 
    August 2nd.

"""
]

PANEL_EVENT_GARNET_SATELLITE=[""" Garnet Fire """,
"""
The imagery reveals a remarkably dense smoke plume extending eastward well into Nevada, demonstrating that the 
fire's air quality impact extended far beyond California. This event is an illustration of how wind patterns impact smoke transport.
"""
]


FIRE_EVENT_PANEL_MAP = {
    'PALISADES': (PANEL_EVENT_PALISADES_DESCRIPTION, PANEL_EVENT_PALISADES_ANALYSIS_SITE_1, PANEL_EVENT_PALISADES_ANALYSIS_SITE_2,  PANEL_EVENT_PALISADES_SATELLITE),
    'Madre':     (PANEL_EVENT_MADRE_DESCRIPTION,     PANEL_EVENT_MADRE_ANALYSIS_SITE_1,     PANEL_EVENT_MADRE_ANALYSIS_SITE_2,  PANEL_EVENT_MADRE_SATELLITE),
    'Gifford':   (PANEL_EVENT_GIFFORD_DESCRIPTION,   PANEL_EVENT_GIFFORD_ANALYSIS_SITE_1,   PANEL_EVENT_GIFFORD_ANALYSIS_SITE_2,  PANEL_EVENT_GIFFORD_SATELLITE),
    'Garnet':    (PANEL_EVENT_GARNET_DESCRIPTION,    PANEL_EVENT_GARNET_ANALYSIS_SITE_1,    PANEL_EVENT_GARNET_ANALYSIS_SITE_2,  PANEL_EVENT_GARNET_SATELLITE),
}


# ============================================================================
#  Panel 5: BEHIND THE DATA (methodology / data cleaning)
# ============================================================================
# Placeholder #TODO: do the analysis

PANEL_EXPLORE_OVERVIEW = """
This tab is an optional but important part of the analysis. The first section examines the methodology
and limitations of the current US AQI. The second section explores the original fire satellite dataset
categories and walks through the key data cleaning steps.
"""
# --- rethinking the AQI ---
PANEL_EXPLORE_EPA_CARD = """ 
- One number: the **highest** individual pollutant AQI
- All other pollutants are **discarded**
"""

PANEL_EXPLORE_EPA       = """
The AQI used in public health reporting is fundamentally flawed. By definition, it reports only the maximum 
AQI value across all pollutants. However, the air quality is significantly different when PM2.5 = 177 and 
O3 = 35 compared to PM2.5 = 177 and O3 = 140 (values from the Palisades event). The Ozone levels are 
substantially higher with serious health consequences, but remain hidden behind the dominant PM2.5 reading.

This is known as the **co-exposure effect**, and it is a well-documented limitation of the AQI.
A more complete approach would report all pollutants simultaneously, but this sacrifices the simplicity
that makes the AQI useful to the general public.

"""

PANEL_EXPLORE_SUMAQI    = """
In this project, we add to the maximum-pollutant AQI (primary exceedance) all secondary
exceedances, (AQI values above 50). To avoid inflating the score,
we subtract the baseline value of 50 from each secondary exceedance. 

For most days and most locations, a single pollutant dominates and the maximum is a reasonable metric for air quality.
Co-exposure is relatively rare under normal conditions, which suggests the AQI is a good methodology
overall. However, wildfires and other adverse events make co-exposure more frequent, and that is 
precisely showing the importance of revising the AQI.
"""

PANEL_EXPLORE_SUMAQI_EXAMPLE = """
In the example below: The EPA maximum reported is 113, corresponding to the PM2.5 levels. Using the sum AQI, 
we add to the PM25 the PM10 exceedance of 6 (56 - 50) and the O3 exceedance of 51 (101 - 50), giving
a composite score of 170 ("Unhealthy for All") instead of the original 113 ("Unhealthy for Sensitive Groups").

"""

PANEL_EXPLORE_PIE       = """
A second issue, introduced in the 2nd panel, is the problem of monitoring coverage. 
This graph shows the number of pollutants captured by each monitor on each day. 

About a third of monitors record only a single pollutant, which has two important implications:
The true air quality at that location on that day cannot be fully assessed and the co-exposure 
effects cannot be adequately detected or reported.
"""
PANEL_EXPLORE_MISCLASS  = """
These three plots investigate the differences between the two methods across the dataset.

The bar chart shows that the sum AQI pushed readings into a higher category in a meaningful
number of cases. The two most impactful reclassifications are **Moderate → Unhealthy for Sensitive Groups**
and **Unhealthy for Sensitive Groups → Unhealthy for All**. These are cases where people were told conditions 
were  safe to go outside when they should have stayed indoors. The **Unhealthy → Very Unhealthy** shift 
is less critical in practice, as both categories recommend remaining inside.

It should be noted that these counts span all monitored locations in California over an entire year,
so the absolute number of affected days remains relatively small. This confirms that the current EPA 
AQI is, in general, a reliable metric for communicating air quality to the public.

"""

PANEL_WORST_MISSCLASS = """
The two figures display 4 days where the sum AQI pushed a site two categories higher, 
with 3 out of 4 pollutants simultaneously exceeding recommended thresholds. 

These cases highlight 
the importance of revisiting the AQI methodology for high-pollution areas: Bakersfield is consistently
ranked among the worst cities for ozone[9](https://www.lung.org/getmedia/3575a218-b54e-4dfe-8d91-892276870a14/california-sota-2025-fact-sheet.pdf),
and Calexico appears in 3 of these 4 most severely misclassified days.
"""



# ============================================================================
#  Public Health Impact tab
# ============================================================================

PUBLIC_HEALTH_WHY = """
PM2.5 is a major component of wildfire smoke and the primary driver of its health effects. 
These particles are small enough to penetrate deep into the lungs, and the smallest ultrafine 
fraction can cross into the bloodstream, reaching the heart, brain, and other organs. Compared 
to PM2.5 from other sources such as traffic or industrial emissions, wildfire smoke PM2.5 tends 
to be smaller in size and richer in oxidative compounds, making it potentially more harmful[5].
"""


PUBLIC_HEALTH_SHORT_TERM = """
Short-term exposure to wildfire-related PM2.5 (days to weeks) has been strongly and consistently 
linked to worsening respiratory conditions. Studies show increased severity of asthma and chronic 
obstructive pulmonary disease, higher rates of inflammation and infections including bronchitis
and pneumonia, and sharp rises in emergency department visits and hospital admissions[1,2,4].

The cardiovascular system is also affected in the short term. Research has documented increases in 
emergency department visits for heart attacks (myocardial infarction), strokes, and heart failure 
during and shortly after wildfire smoke episodes[1,4].

Based on U.S. data from 2008 to 2012, Fann et al. estimated that short-term exposure to wildfire-related
PM2.5 results in between 5,200 and 8,500 respiratory hospital admissions and between 1,500 and 2,500 
premature deaths annually across the country[3]. These numbers are likely to increase as wildfires
become more frequent and intense.
"""


PUBLIC_HEALTH_LONG_TERM = """
It is equally important to consider the long-term consequences of PM2.5 exposure, including cumulative 
exposures across multi-day events or multiple consecutive fire seasons.

The EPA's 2019 Integrated Science Assessment for Particulate Matter concluded that there is a likely 
causal relationship between long-term PM2.5 exposure and respiratory effects, specifically asthma 
development in children and lung function decline in adults. Studies have also shown that respiratory 
health improves when PM2.5 concentrations decline, reinforcing the link and highlighting the importance
of reducing PM2.5 exposure [4].

There is strong evidence associating long-term PM2.5 exposure with cardiovascular mortality, including 
deaths from stroke and ischemic heart disease [4].

Evidence regarding the nervous system is more limited, primarily due to the small number of studies available, 
but the existing research generally supports a positive association between long-term PM2.5 exposure and 
neurological effects such as cognitive decline and depression [4].

Long-term exposure to wildfires that burn a mixture of natural vegetation and synthetic materials 
(homes, vehicles, ...) may contribute to an elevated overall lifetime risk for heart disease, lung disease, 
and cancer, in addition to releasing other pollutants like lead, cadmium, and asbestos [1].
"""


PUBLIC_HEALTH_BEYOND = """
The economic costs of wildfire have escalated dramatically in recent times. From 2014 to 2023, wildfires 
globally caused approximately $106 billion in economic losses and $74 billion in insured losses [12]. 
The January 2025 Los Angeles wildfires, which destroyed over 12,000 structures in some of the most expensive 
areas in the country, have produced preliminary cost estimates exceeding $250 billion[12].

The level of suffering is not only limited to financial losses but also to the negative impact that wildfires
impose on the physical and mental wellbeing of survivors. The mental health consequences of property loss 
and displacement can trigger mental health disorders and illnesses. [5] Many wildfire survivors report 
elevated levels of anxiety, depression, stress, sleep difficulties, and post-traumatic stress disorder (PTSD)
symptoms [8,9], and these can last for years and decades, with children and teenagers having a higher risk of
contracting a trauma-related disorder.

A lesser known but equally important impact of wildfires is on drinking-water systems. Fire damages water 
distribution infrastructure, and heat can cause pipes to break and/or leak chemicals directly into the 
water supply [11,10]. The 2018 Camp Fire affected 13 different water systems, and more than 40,000 people
received a boil-water advisory [10]. More than 100 toxic compounds have been identified in post-fire 
drinking water[11].

In addition to being costly and hard to assess, it takes time to fix water distribution systems. 
Seven months after the Camp Fire, some homes were still receiving contaminated water, and levels of 
contaminants can be so high that it was not certain that boiling was sufficient[10,11].
"""


PUBLIC_HEALTH_CLIMATE = """
Wildfires now burn at least twice as much tree cover as they did two decades ago, with fire accounting
for roughly 33% of global tree cover loss in recent years. When forests burn, they release stored carbon, 
further accelerating climate change. Extreme heat events are already five times more likely than 150 years ago, 
creating drier landscapes and ideal conditions for larger, more frequent fires [12]. Research has shown that 
limiting greenhouse gas emissions, and thereby constraining global temperature rise, could reduce wildfire 
smoke exposure by up to 60% [6].

Furthermore, what has already been observed in California, a lengthening fire season and increasing fire 
frequency is now part of a global pattern. Projections show that virtually no region of the world will 
be spared from rising wildfire risk, including high-latitude areas previously considered low-risk. 
Beyond direct health effects, increased wildfire activity also threatens agricultural systems through 
crop heat stress affecting staple crops such as soybean, wheat, and maize[6,7].
"""


PUBLIC_HEALTH_SUBTITLE = (
    "How wildfire-driven PM2.5 exposure affects respiratory, cardiovascular, and "
    "neurological health and what climate projections mean for future risk."
)

# ============================================================================
#  Sources
# ============================================================================

# Each entry is the markdown body for a numbered reference; the list index + 1
# gives the citation number and its anchor id (src-1, src-2, ...).
SOURCES = [
    "California fire season guide — [wfca.com](https://wfca.com/wildfire-articles/california-fire-season-in-depth-guide/)",
    "CalFire — Top 20 Most Destructive California Wildfires — [fire.ca.gov](https://www.fire.ca.gov/-/media/calfire-website/our-impact/fire-statistics/top-20-destructive-ca-wildfires.pdf)",
    "EPA — Wildland Fire Research: Human Health — [epa.gov](https://www.epa.gov/air-research/wildland-fire-research-human-health)",
    "AirNow — AQI Basics — [airnow.gov](https://www.airnow.gov/aqi/aqi-basics/)",
    "WHO — Air Quality Guidelines 2021 — [who.int](https://www.who.int/publications/i/item/9789240034228)",
    "Wikipedia — Air Quality Index — [wikipedia.org](https://en.wikipedia.org/wiki/Air_quality_index)",
    "WHO — Types of Pollutants — [who.int](https://www.who.int/teams/environment-climate-change-and-health/air-quality-and-health/health-impacts/types-of-pollutants)",
    "EPA — California Air & Transportation Initiative (CATI) — [epa.gov](https://www.epa.gov/cati/about)",
    "American Lung Association — California State of the Air 2025 — [lung.org](https://www.lung.org/getmedia/3575a218-b54e-4dfe-8d91-892276870a14/california-sota-2025-fact-sheet.pdf)",
    "Earth.org — Air Pollution in California — [earth.org](https://earth.org/air-pollution-in-california)",
    "Wikipedia — Pollution in California — [wikipedia.org](https://en.wikipedia.org/wiki/Pollution_in_California)",
    "Wikipedia — San Joaquin Valley — [wikipedia.org](https://en.wikipedia.org/wiki/San_Joaquin_Valley)",
    "Health Effects Institute — State of Global Air 2024 — [stateofglobalair.org](https://www.stateofglobalair.org/sites/default/files/documents/2024-06/soga-2024-report_0.pdf)",
    "CDC MMWR — Lead exposure during the 2025 Los Angeles wildfires — [cdc.gov](https://www.cdc.gov/mmwr/volumes/74/wr/mm7405a4.htm?s_cid=mm7405a4_w)",
]


PUBLIC_HEALTH_SOURCES = [
    "CARB, *Camp Fire Air Quality Data Analysis*, July 2021 - [Camp_Fire_report_July2021](https://ww2.arb.ca.gov/sites/default/files/2021-07/Camp_Fire_report_July2021.pdf)",
    "Delfino, R. J. et al. \"The relationship of respiratory and cardiovascular hospital admissions to the southern California wildfires of 2003.\" *Occupational and Environmental Medicine* vol. 66,3 (2009) - [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC4176821/)",
    "Fann, Neal et al. \"The health impacts and economic value of wildland fire episodes in the U.S.: 2008-2012.\" *The Science of the Total Environment* vol. 610-611 (2018) - [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6117838/)",
    "U.S. EPA, *Integrated Science Assessment for Particulate Matter* - [www.epa.gov/isa](https://www.epa.gov/isa/integrated-science-assessment-isa-particulate-matter)",
    "Xu, Rongbin et al. \"Wildfires, Global Climate Change, and Human Health.\" *The New England Journal of Medicine* vol. 383,22 (2020) - [nejm.org](https://www.nejm.org/doi/10.1056/NEJMsr2028985?url_ver=Z39.88-2003&rfr_id=ori:rid:crossref.org&rfr_dat=cr_pub%20%200pubmed)",
    "Sun, Qiaohong, et al. \"Global heat stress on health, wildfires, and agricultural crops under different levels of climate warming.\" *Environment International* 128 (2019) - [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0160412018328654?via%3Dihub)",
    "Jiao, Anqi, et al. \"Associations between short-term exposure to wildfire particulate matter and respiratory outcomes: a systematic review.\" *Science of the Total Environment* 907 (2024) - [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S004896972306761X)",
    "Isaac, Fadia, et al. \"Differences in anxiety, insomnia, and trauma symptoms in wildfire survivors from Australia, Canada, and the United States of America.\" *International Journal of Environmental Research and Public Health* 21.1 (2023) - [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10815777/)",
    "To, Patricia, Ejemai Eboreime, and Vincent I. O. Agyapong. \"The impact of wildfires on mental health: a scoping review.\" *Behavioral Sciences* 11.9 (2021) - [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8466569/)",
    "Olson, Steve, ed. *Implications of the California Wildfires for Health, Communities, and Preparedness: Proceedings of a Workshop*. National Academies Press, 2020 - [nationalacademies.org](https://www.nationalacademies.org/read/25622/chapter/5#45)",
    "Proctor, Caitlin R., et al. \"Wildfire caused widespread drinking water distribution network contamination.\" *AWWA Water Science* 2.4 (2020) - [awwa.onlinelibrary.wiley.com](https://awwa.onlinelibrary.wiley.com/doi/full/10.1002/aws2.1183)",
    "UNDRR, *Global Assessment Report on Disaster Risk Reduction 2025: Resilience Pays*, United Nations, 2025 - [undrr.org](https://www.undrr.org/gar/gar2025)",
]