# Ultimate Bearing Capacity Formulas

Bearing capacity equation used in `hansen` and `vesic` methods.

$
q_u = cN_c s_c d_c i_c + qN_q s_q d_q i_q +
0.5 \gamma B N_{\gamma} s_{\gamma} d_{\gamma} i_{\gamma}
$

See description of symbols
[below](#description-of-symbols-used-in-bearing-capacity-equations).

## Hansen Bearing Capacity

### Bearing capacity factors

$N_c = \cot(\phi) \left(N_q - 1\right)$

$N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot e^{\pi \tan(\phi)}$

$N_{\gamma} = 1.8 \left(N_q - 1\right) \tan(\phi)$

### Shape factors

#### Shape factors for strip footing

$s_c = 1.0 \rightarrow \text{Strip footing}$

$s_q = 1.0 \rightarrow \text{Strip footing}$

$s_{\gamma} = 1.0 \rightarrow \text{Strip footing}$

#### Shape factors rectangular footing

$s_c = 1.0 + 0.2 \cdot \dfrac{B}{L} \rightarrow \text{Rectangular footing}$

$s_q = 1.0 + 0.2 \cdot \frac{B}{L} \rightarrow \text{Rectangular footing}$

$
s_{\gamma} = 1.0 - 0.4 \frac{B}{L} \rightarrow
\text{Rectangular footing}
$

#### Shape factors square or circular footing

$s_c = 1.3 \rightarrow \text{Square or circular footing}$

$s_q = 1.2 \rightarrow \text{Square or circular footing}$

$s_{\gamma} = 0.8 \rightarrow \text{Square footing}$

$s_{\gamma} = 0.6 \rightarrow \text{Circular footing}$

### Depth factors

$d_c = 0.0 + 0.35 \cdot \dfrac{D_f}{B}$

$d_q = 1.0 + 0.35 \cdot \dfrac{D_f}{B}$

$d_{\gamma} = 1.0$

### Inclination factors

$i_c = 1 - \dfrac{\sin(\alpha)}{2cBL}$

$i_q = 1 - \dfrac{1.5 \cdot \sin(\alpha)}{\cos(\alpha)}$

$i_{\gamma} = I_q^2$

## Vesic Bearing Capacity

### Bearing capacity factors

$N_c = \cot(\phi) \left(N_q - 1\right)$

$
N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot
e^{\pi \tan(\phi)}
$

$N_{\gamma} = 2(N_q + 1) \tan(\phi)$

### Shape factors

#### Shape factors for strip footing

$s_c = 1.0 \rightarrow \text{Strip footing}$

$s_q = 1.0 \rightarrow \text{Strip footing}$

$s_{\gamma} = 1.0 \rightarrow \text{Strip footing}$

#### Shape factors for rectangular footing

$
s_c = 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c} \rightarrow
\text{Rectangular footing}
$

$
s_q = 1 + \dfrac{B}{L} \cdot \tan(\phi) \rightarrow
\text{Rectangular footing}
$

$
s_{\gamma} = 1.0 - 0.4 \dfrac{B}{L} \rightarrow
\text{Rectangular footing}
$

#### Shape factors for square or circular footing

$
s_c = 1 + \dfrac{N_q}{N_c} \rightarrow
\text{Square or circular footing}
$

$s_q = 1 + \tan(\phi) \rightarrow \text{Square or circular footing}$

$s_{\gamma} = 0.6 \rightarrow \text{Square or circular footing}$

### Depth factors

$d_c = 1 + 0.4 \dfrac{D_f}{B}$

$
d_q = 1 + 2 \tan(\phi) \cdot (1 - \sin(\phi))^2
\cdot \dfrac{D_f}{B}
$

$d_{\gamma} = 1.0$

### Inclination factors

$i_c = (1 - \dfrac{\alpha}{90})^2$

$i_q = (1 - \dfrac{\alpha}{90})^2$

$i_{\gamma} = \left(1 - \dfrac{\alpha}{\phi} \right)^2$

## Terzaghi Bearing Capacity

### Terzaghi Bearing Capacity for Strip footing

$q_u = cN_c + qN_q + 0.5 \gamma BN_{\gamma}$

See description of symbols
[below](#description-of-symbols-used-in-bearing-capacity-equations).

### Terzaghi Bearing Capacity for Circular footing

$q_u = 1.3cN_c + qN_q + 0.3 \gamma BN_{\gamma}$

See description of symbols
[below](#description-of-symbols-used-in-bearing-capacity-equations).

### Terzaghi Bearing Capacity for Square footing

$q_u = 1.3cN_c + qN_q + 0.4 \gamma BN_{\gamma}$

See description of symbols
[below](#description-of-symbols-used-in-bearing-capacity-equations).

### Terzaghi Bearing Capacity for Rectangular footing

$
q_u = \left(1 + 0.3 \cdot \dfrac{B}{L} \right) c N_c + qN_q +
\left(1 - 0.2 \cdot \dfrac{B}{L} \right) 0.5 B \gamma N_{\gamma}
$

See description of symbols
[below](#description-of-symbols-used-in-bearing-capacity-equations).

### Bearing capacity factors

$N_c = \cot(\phi) \cdot (N_q - 1)$

$
N_q = \dfrac{e^{(\frac{3\pi}{2} - \phi)\tan\phi}}
{2\cos^2(45 + \frac{\phi}{2})}
$

$N_{\gamma} =  (N_q - 1) \cdot \tan(1.4\phi)$

## Description of symbols used in bearing capacity equations

| Symbol                     | Unit            | Description                 |
|----------------------------|-----------------|-----------------------------|
| $q_u$                      | kPa or $kN/m^2$ | Ultimate bearing capacity   |
| $c$                        | kPa or $kN/m^2$ | Cohesion of soil            |
| $q$                        | kPa or $kN/m^2$ | Overburden pressure of soil |
| $\gamma$                   | $kN/m^3$        | Unit weight of soil         |
| $B$                        | m               | Width of foundation footing |
| $N_c$, $N_q$, $N_{\gamma}$ | –               | Bearing capacity factors    |
| $s_c$, $s_q$, $s_{\gamma}$ | –               | Shape factors               |
| $d_c$, $d_q$, $d_{\gamma}$ | –               | Depth factors               |
| $i_c$, $i_q$, $i_{\gamma}$ | –               | Inclination factors         |
