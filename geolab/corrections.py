def spt_n60(
    recorded_spt_nvalue: int,
    hammer_efficiency: float = 0.575,
    borehole_diameter_cor: float = 1,
    sampler_cor: float = 1,
    rod_length_cor: float = 0.75,
) -> float:
    r"""SPT N-value corrected for field procedures.

    $$N_{60} = \dfrac{E_m \times C_B \times C_s \times C_R \times N_r}{0.6}$$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        hammer_efficiency: Hammer Efficiency. Defaults to 0.575.
        borehole_diameter_cor: Borehole Diameter Correction. Defaults to 1.
        sampler_cor: Sampler Correction. Defaults to 1.
        rod_length_cor: Rod Length Correction. Defaults to 0.75.

    Returns:
        SPT N-value corrected for 60% hammer efficiency.
    """
    first_expr = (
        hammer_efficiency
        * borehole_diameter_cor
        * sampler_cor
        * rod_length_cor
        * recorded_spt_nvalue
    )

    return first_expr / 0.6
