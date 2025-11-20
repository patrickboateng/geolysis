# Terzaghi Bearing Capacity

## Bearing capacity factors

- $N_c = \cot(\phi) \cdot (N_q - 1)$
- $N_q = \dfrac{e^{(\frac{3\pi}{2} - \phi)\tan\phi}}
  {2\cos^2(45 + \frac{\phi}{2})}
  $
- $N_{\gamma} =  (N_q - 1) \cdot \tan(1.4\phi) \rightarrow \text{Meyerhof (1963)}$

There are other equations for $N_{\gamma}$ by different authors which can be
found below:

- $N_{\gamma} = 1.5(N_q - 1) \cdot \tan(\phi) \rightarrow \text{Hansen (1970)}$
- $N_{\gamma} = 2(N_q + 1) \cdot \tan(\phi) \rightarrow \text{Vesic (1973)}$


## Terzaghi Bearing Capacity for Strip footing

$$q_u = cN_c + qN_q + 0.5 \gamma BN_{\gamma}$$

## Terzaghi Bearing Capacity for Circular footing

$$q_u = 1.3cN_c + qN_q + 0.3 \gamma BN_{\gamma}$$

## Terzaghi Bearing Capacity for Square footing

$$q_u = 1.3cN_c + qN_q + 0.4 \gamma BN_{\gamma}$$

## Terzaghi Bearing Capacity for Rectangular footing

$$
q_u = \left(1 + 0.3 \cdot \dfrac{B}{L} \right) c N_c + qN_q +
\left(1 - 0.2 \cdot \dfrac{B}{L} \right) 0.5 B \gamma N_{\gamma}
$$
