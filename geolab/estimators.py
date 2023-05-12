def friction_angle(spt_n60: float) -> float:
    r"""Internal angle of friction.

    $$\phi = 27.1 + 0.3 \times N_{60} - 0.00054 \times (N_{60})^2$$

    Args:
        spt_n60: The SPT N-value corrected for 60% hammer efficiency.

    Returns:
        The internal angle of friction in degrees.
    """
    return 27.1 + 0.3 * spt_n60 - 0.00054 * (spt_n60**2)
