# Timing Corners

Timing corners describe operating conditions under which a cell library has been characterized. Digital timing is not a single number because transistor speed, wire behavior, and cell delay change with process variation, supply voltage, and temperature.

## Process, Voltage, and Temperature

Process captures manufacturing variation. A fast process corner generally models devices that switch faster than nominal, while a slow process corner models devices that switch more slowly.

Voltage changes available drive strength and delay. Higher voltage often speeds up switching, while lower voltage usually increases delay and can tighten timing margins.

Temperature affects mobility, threshold behavior, leakage, and resistance. Depending on the device and operating region, hotter or colder conditions can change delay and power in different ways.

## Why Corners Matter

Implementation tools need to know whether timing closes across the range of conditions the design must survive. A path that passes at one corner can fail at another. Setup, hold, clock-to-output, recovery/removal, and power analysis can all be corner-dependent.

## Current Boundary

M1 through M4 do not ingest real Sky130 corners. The current timing-table fixtures are synthetic and do not contain characterized PVT data. M4 can describe timing-table axes and dimensions, but it does not perform static timing analysis or claim real corner coverage.

Real Sky130 read-only ingestion is deferred to M5, after the Liberty parser, standard-cell atlas, and timing-table explorer have clearer tested boundaries.
