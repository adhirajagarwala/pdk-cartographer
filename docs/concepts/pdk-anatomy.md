# PDK Anatomy

A process design kit, or PDK, is the contract between a semiconductor manufacturing process and the design tools used to build chips for that process. It packages technology rules, device models, layout abstractions, standard-cell data, verification decks, and documentation so that design intent can be checked against the limits of a real fabrication process.

`pdk-cartographer` treats a PDK as an engineering object to inspect carefully, not as a magic folder of files. The goal is to understand what each artifact is responsible for, where tool flows consume it, and what conclusions are safe to draw from it.

## Logical and Physical Artifacts

Logical artifacts describe behavior and constraints that digital implementation tools need before looking at final geometry. Liberty files are a central example: they describe standard-cell metadata such as cell names, pin directions, Boolean functions, area, timing arcs, timing tables, and power data. Synthesis, static timing analysis, and optimization tools use Liberty data to reason about cells and paths.

Physical artifacts describe geometry and manufacturing constraints. LEF files describe physical abstracts for place-and-route, while technology LEF describes routing layers, via rules, and process-level layout information. GDS contains detailed mask geometry. DRC decks define design-rule checks, and LVS decks help compare layout connectivity against the schematic or netlist. SPICE models describe transistor-level electrical behavior for circuit simulation.

These categories overlap in real flows. A standard cell is useful because its logical Liberty view and physical LEF/GDS views refer to the same implementation from different tool perspectives.

## M1 Focus

M1 focuses only on tiny synthetic Liberty fixtures. It does not download Sky130, ingest real Sky130 libraries, parse LEF/DEF/GDS, run DRC/LVS, install OpenLane/OpenROAD, or claim silicon-level validation. This keeps the first milestone testable and honest: understand the shape of Liberty metadata before touching larger real PDK files.
