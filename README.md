# `soil_classifier`: A Python Package and Microsoft Excel Add-In for soil classification.

`soil_classifier` uses **Unified Soil Classification System (USCS)** and the **American Association of State Highway and Transportation Officials (AASHTO)** system to classify soils.

It is important to characterize soils to be able to assess their engineering properties such as:

- Bearing capacity
- Compressibility
- Permeability

**Particle Size Distribution (PSD)** and **Atterberg Limits** are tests developed for characterizing soils quality.

# Particle Size Distribution (PSD)

The range of particle sizes in a sample of material is referred to as the particle size distribution. It is commonly measured using sieve analysis techniques, which entail using a stack of sieves to measure the size of the particles in a sample and graphing the results to illustrate the distribution of the particle sizes. The particle size distribution can provide important information about the materials' physical characteristics.

## Soil type based on Particle Size

<table>
    <thead>
        <tr>
            <th>Designation</th>
            <th>Category</th>
            <th>Particle Size (mm)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Boulders</td>
            <td></td>
            <td>> 200</td>
        </tr>
        <tr>
            <td>Cobbles</td>
            <td></td>
            <td>60 - 200</td>
        </tr>
        <tr>
            <td rowspan="3">Gravel</td>
            <td>Coarse</td>
            <td>20 - 60</td>
        </tr>
        <tr>
            <td>Medium</td>
            <td>6 - 20</td>
        </tr>
        <tr>
            <td>Fine</td>
            <td>2 - 6</td>
        </tr>
        <tr>
            <td rowspan="3">Sand</td>
            <td>Coarse</td>
            <td>0.6 - 2</td>
        </tr>
        <tr>
            <td>Medium</td>
            <td>0.2 - 0.6</td>
        </tr>
        <tr>
            <td>Fine</td>
            <td>0.06 - 0.2</td>
        </tr>
        <tr>
            <td rowspan="3">Silt</td>
            <td>Coarse</td>
            <td>0.02 - 0.06</td>
        </tr>
        <tr>
            <td>Medium</td>
            <td>0.006 - 0.02</td>
        </tr>
        <tr>
            <td>Fine</td>
            <td>0.002 - 0.006</td>
        </tr>
        <tr>
            <td>Clay</td>
            <td>Fine</td>
            <td>< 0.002</td>
        <tr>
    </tbody>
</table>

The distribution of grain sizes affects the engineering properties of the soil.

- A single grain-sized soil cannot be compacted to a high density, which results in a lesser shear strength.
- Soils with grains spanning a wide size distribution can be compacted to a high density resulting in a high shear strength.

# Sieves commonly used for Particle Size Distribution

<table>
    <thead>
        <tr>
            <th>BS Sieve Designation</th>
            <th>ASTM Designation</th>
            <th>Aperture (mm)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1 in</td>
            <td></td>
            <td>26.5</td>
        </tr>
        <tr>
            <td>$\frac{3}{4}$ in</td>
            <td></td>
            <td>19.0</td>
        </tr>
        <tr>
            <td>$\frac{1}{2} in$</td>
            <td>0.53 in</td>
            <td>13.2 mm</td>
        </tr>
        <tr>
            <td>$\frac{3}{8} in$</td>
            <td>$\frac{3}{8} in$</td>
            <td>9.5 mm</td>
        </tr>
        <tr>
            <td>$\frac{1}{4} in$</td>
            <td>0.265 in</td>
            <td>6.7 mm</td>
        </tr>
        <tr>
            <td>$\frac{3}{16} in$</td>
            <td>No. 4</td>
            <td>4.75 mm</td>
        </tr>
        <tr>
            <td>No. 7</td>
            <td>No. 8</td>
            <td>2.36</td>
        </tr>
        <tr>
            <td>No. 14</td>
            <td>No. 16</td>
            <td>1.18</td>
        </tr>
        <tr>
            <td>No. 25</td>
            <td>No. 30</td>
            <td>600 $\mu m$</td>
        </tr>
        <tr>
            <td>No. 36</td>
            <td>No. 40</td>
            <td>425 $\mu m$</td>
        </tr>
        <tr>
            <td>No. 52</td>
            <td>No. 50</td>
            <td>300 $\mu m$</td>
        </tr>
        <tr>
            <td>No. 72</td>
            <td>No. 70</td>
            <td>212 $\mu m$</td>
        </tr>
        <tr>
            <td>No. 100</td>
            <td>No. 100</td>
            <td>150 $\mu m$</td>
        </tr>
        <tr>
            <td>No. 200</td>
            <td>No. 200</td>
            <td>75 $\mu m$</td>
        </tr>
    </tbody>
</table>

# Unified Soil Classification System (USCS)

_brief description underway_

# American Association of State Highway and Transportation Officials (AASHTO)

_brief description underway_
