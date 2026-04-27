# Standard Cells

Standard cells are pre-designed logic building blocks used by digital ASIC flows. A cell library contains gates such as inverters, NANDs, NORs, multiplexers, latches, and flip-flops. Each cell has a logical view for synthesis and timing, and a physical view for placement, routing, and layout verification.

## Metadata That Matters

The first metadata to inspect is intentionally simple:

- Cell name: usually encodes function and variant.
- Area: a normalized physical cost used by implementation tools.
- Pins: named connection points such as `A`, `B`, `Y`, `D`, `Q`, or `CLK`.
- Pin direction: input, output, clock-like input, or other role.
- Function: Boolean behavior for simple combinational outputs.
- Timing arcs: relationships such as input-to-output delay or clock-to-output timing.

This project begins with these fields because they are visible in small fixtures and can be validated without large PDK dependencies.

## Combinational and Sequential Cells

Combinational cells compute outputs from current inputs. An inverter-like cell has an input pin and an output pin whose function is the logical inverse of the input. NAND, NOR, and mux cells follow the same broad idea with more pins and different Boolean expressions.

Sequential cells store state. A simplified D flip-flop has a clock pin, a data pin, and an output pin. Its Liberty metadata can include timing relationships such as setup checks from data to clock and clock-to-output arcs.

## Naming and Drive Strength

Cell names often include function and drive-strength hints, such as an inverter family with multiple `X1`, `X2`, or `X4` variants. The exact naming convention belongs to a specific library. In M1, names are synthetic and educational, so they should be read as realistic-looking examples rather than Sky130 facts.
