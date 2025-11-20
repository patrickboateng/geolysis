# Vesic Bearing Capacity

$$
q_u = cN_c s_c d_c i_c + qN_q s_q d_q i_q +
0.5 \gamma B N_{\gamma} s_{\gamma} d_{\gamma} i_{\gamma}
$$

## Bearing capacity factors

- $N_c = \cot(\phi) \left(N_q - 1\right)$
- $N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot
  e^{\pi \tan(\phi)}$
- $N_{\gamma} = 2(N_q + 1) \tan(\phi)$

## Shape factors

### Shape factors for strip footing

- $s_c = 1.0$
- $s_q = 1.0$
- $s_{\gamma} = 1.0$

### Shape factors for rectangular footing

- $s_c = 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c}$
- $s_q = 1 + \dfrac{B}{L} \cdot \tan(\phi)$
- $s_{\gamma} = 1.0 - 0.4 \dfrac{B}{L}$

### Shape factors for square or circular footing

- $s_c = 1 + \dfrac{N_q}{N_c}$
- $s_q = 1 + \tan(\phi)$
- $s_{\gamma} = 0.6$

## Depth factors

These equations were provided by Hansen (1970)

- For $\dfrac{D_f}{B} \le 1$
    - For $\phi = 0^{\circ}$
        - $d_c = 1 + 0.4 \dfrac{D_f}{B}$
        - $d_q = 1$
        - $d_{\gamma} = 1$

    - For $\phi \gt 0^{\circ} $
        - $d_c = d_q - \dfrac{1 - dq}{N_c \tan(\phi)}$
        - $d_q = 1 + 2 \tan(\phi) (1 - \sin(\phi)^2)(\dfrac{D_f}{B})$
        - $d_{\gamma} = 1$
- For $\dfrac{D_f}{B} \gt 1$
    - For $\phi = 0$
        - $d_c = 1 + 0.4 \cdot \underbrace{\tan^{-1}\left(\dfrac{D_f}{B}\right)}_{\text{radians}}$
        - $d_q = 1$
        - $d_{\gamma} = 1$
    - For $\phi \gt 0^{\circ}$
        - $d_c = d_q - \dfrac{1 - dq}{N_c \tan(\phi)}$
        - $d_q = 1 + 2 \tan(\phi) (1 - \sin(\phi)^2) \cdot
          \underbrace{\tan^{-1}\left(\dfrac{D_f}{B}\right)}_{\text{radians}}$
        - $d_{\gamma} = 1$

## Inclination factors

These equations were provided by Meyerhof (1963); Hanna and Meyerhof (1981)

- $i_c = i_q = \left (1 - \dfrac{\beta^{\circ}}{90^{\circ}}\right)^2$
- $i_{\gamma} = \left(1 - \dfrac{\beta}{\phi} \right)^2$

where $\beta = \text{inclination of the load on the foundation with respect to the vertical}$

$\beta$ should be in the same units as $\phi$ (degrees or radians)
for $i_{\gamma}$.
