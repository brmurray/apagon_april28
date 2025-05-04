# apagon_april28

> *Last Update: May 4, 2025 @ 1945 CEST*

On April 28, 2025, the Iberian penisula suffered the largest and widest power outage in its history. The proximate and contributing causes are still under investigation, and no authoritative report as been issued as of this writing. This repo, sponsored by the [LEMUR Lab](https://lemuruniovi.com/) at [Universidad de Oviedo](https://www.uniovi.es/), is a central collection point for relevant, publically-sharable data about the event.


# So what happened?
Check out the [reports](reports/) folder for a colorful presentation and ["Detailed Analysis"](detailed_analysis.md) for especially nerdy content.

_Our best timeline (all times CEST)_
- **06:00:00** - Transmission export capacity Spain -> France is reduced to ~1.8GW (typically ~2.6GW). 
- **12:00:00 or earlier** - Frequency oscillations, (T=~4.3s) observed in the Iberian transmission grid.
- **12:19:30.0** - Frequency oscillations significantly worsen for ~3 minutes, then apparently decay around 12:22:00pm.
- **12:32:57.3** - Major rapid frequency dip in Iberian grid is not apparent in other markets. The Iberian grid reovers briefly but frequencies decline across the continent for ~ 15 seconds until...
- **12:33.16.5** - Fast, irreversible frequency drop starts at 12:33:16.5. Likely some large source tripped and started the cascade of “15GW in 5 seconds”.


# What do we _not_ know?
- The Spanish government insists that a cyberattack is not to blame. LEMUR believes that there are perfectly plausable technical explanations for the outage, and thus we have no specific reason to question the government's assertion. Nevertheless, the generally public will not know the cybersecurity details any time soon, if ever.
- The Spanish government has also ruled out human error and extraordinary meterological conditions as root causes, and we ignore them for the sames reasons as above.
- Very detailed information about the physical conditions of the grid and market operations will be necessary for a root-cause analysis. We don't have access to that data. Instead, we're pursuing a humble, transparent analysis using whatever public information we can collect.

# What can we infer?
- The Spanish grid was operating with a very high ratio of solar energy at the time. Inverter-based resources (solar and batteries but also some flavors of wind and hydropower) have no synchronous interia, so the overall inertia of the Iberian grid was quite low on the morning of April 28.
- None of the individual operating characteristics of the Iberian grid on the morning of April 28 were unprecedented, or even extraordinary. It probably too the day's unique blend of vulnerablilities and unfortunate events to cause the blackout.
- Inter-area frequency oscillations are especially difficult to predict and manage, and an area of active research in the field. 


# What would we like to know?
Help us tune our models! Here's a wishlist of data:

- High-resolution (<100ms) frequency measurements from any point on the Iberian or French transmissiong grid.
- Very high resolution (<10ms) measurements of any voltage or current waveform from equipment that was directly connected to the grid before 12:33pm, regardless of connection voltage.
- Information about behind-the-meter/self-consumption solar PV and battery systems (ratings, location, any time series data).
- Data market conditions, especially FFR bids.

# How can you help?
- Get in touch! lemur_a_uniovi.es
- Contribute data! Fork -> add to a new folder under `data`, and open a pull request.
- See [repo_org.md](repo_org.md) for details about this repo.


