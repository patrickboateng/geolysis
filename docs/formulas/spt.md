# SPT Formulas

## Overburden Pressure Corrections

$(N_1)_{60} = C_N \cdot N_{60}$

$C_N \le 2$

See description of symbols
[below](#description-of-symbols-used-in-spt-corrections).

!!! note

    `60` is used in this case to represent `60%` hammer
     efficiency and can be any percentage of hammer efficiency
     e.g. $N_{55}$ for `55%` hammer efficiency.

### Gibbs & Holtz (1957)

$C_N = \dfrac{350}{\sigma_o + 70} \, \sigma_o \le 280kN/m^2$

!!! note

    $\frac{N_c}{N_{60}}$ should lie between 0.45 and 2.0, if
    $\frac{N_c}{N_{60}}$ is greater than 2.0, :math:`N_c` should be
    divided by 2.0 to obtain the design value used in finding the
    bearing capacity of the soil.

### Peck and Bazaraa (1969)

$
C_N = \dfrac{4}{1 + 0.0418 \cdot \sigma_o}, \,
\sigma_o \lt 71.8kN/m^2
$

$
C_N = \dfrac{4}{3.25 + 0.0104 \cdot \sigma_o},
\, \sigma_o \gt 71.8kN/m^2
$

$C_N = 1 \, , \, \sigma_o = 71.8kN/m^2$

### Peck et al. (1974)

$C_N = 0.77 \log \left(\dfrac{2000}{\sigma_o} \right)$

### Liao & Whitman (1986)

$C_N = \sqrt{\dfrac{100}{\sigma_o}}$

### Skemton (1986)

$C_N = \dfrac{2}{1 + 0.01044 \cdot \sigma_o}$

## Dilatancy Corrections

$(N_1)_{60 \, (CORR)} = 15 + \dfrac{1}{2}((N_1)_{60} - 15) \, , \, (N_1)_{60} \gt 15$

$(N_1)_{60 \, (CORR)} = (N_1)_{60} \, , \, (N_1)_{60} \le 15$

## Description of symbols used in SPT Corrections

| Symbol                 | Description                                        |
|------------------------|----------------------------------------------------|
| $(N_1)_{60}$           | SPT blow count corrected for overburden pressure   |
| $(N_1)_{60 \, (CORR)}$ | SPT blow count corrected for dilatancy             |
| $N_{60}$               | SPT blow count corrected for 60% hammer efficiency |
| $C_N$                  | Overburden pressure correction factor              |
| $\sigma_o$             | Effective overburden pressure at the test depth    |
