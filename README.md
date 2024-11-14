# geolysis

> [!NOTE]
> Active development of `geolysis` occurs on the `dev` branch. For more
> information for the lastest features of `geolysis`, switch to the
> `dev` branch.

`geolysis` is your one-stop shop for all your geotechnical engineering
solutions, ranging from site investigation and laboratory test analysis
to advanced geotechnical designs.

`geolysis` is divided into four (4) main parts:

1. `geolyis.core (Python)`

   `geolysis.core` is an open-source Python package that provides features for
   analyzing geotechnical results obtained from field and laboratory tests.
   `geolysis.core` is designed specifically to assist developers in building
   applications that can solve complex geotechnical problems.

   Whether you're working on soil mechanics, rock mechanics, or any other
   geotechnical field, `geolysis.core` provides a powerful set of tools that can
   help you design and develop robust solutions. With an intuitive API and a
   wide range of features, this software is an essential tool for anyone who
   needs to work with geotechnical data on a regular basis. Whether you're a
   seasoned geotechnical engineer or a new developer just getting started in the
   field, `geolysis.core` is the ideal solution for all your software
   development needs.

   Some of the features implemented so far include soil classification, standard
   penetration test analysis (such as SPT N-design and SPT N-value corrections),
   and calculating the allowable bearing capacity of soils from Standard
   Penetration Test N-values. There are more features underway, which include
   settlement analysis, ultimate bearing capacity analysis, etc.

   `geolysis.core` is the foundation application on which other parts of the
   application will depend. Developers can also use `geolysis.core` to power
   their applications.

1. `geolysis.gui (Qt, PySide6)`

   `geolysis.gui` is a Graphical User Interface (GUI) which will enable users to
   graphically interact with `geolysis`. Users will be able to input data and
   view generated plots, such as `PSD` curves, `Atterberg Limits` plots,
   `Compaction` curves, etc within the application.

1. `geolysis.excel (Javascript/TypeScript & Others)`

   `geolysis.excel` provides a Microsoft Excel add-in for simple geotechnical
   analysis. _More on this later._

1. `geolysis.ai (Python, Pytorch & Others)`

   `geolysis.ai` explores the use of Artificial Intelligence (**AI**) in
   enhancing productivity in Geotechnical Engineering.

## Motivation

`geolysis` is a software solution that aims to support geotechnical engineers in
their daily work by providing a set of tools that makes them perform their tasks
in a more efficient and effective manner.

Moreover, the platform is designed to educate civil engineering students,
especially those who specialize in geotechnical engineering, by exposing them to
industry-relevant tools and techniques that will help them become industry-ready
professionals as soon as they graduate.

With `geolysis`, users will be better equipped to handle geotechnical
challenges, make informed decisions, and improve their overall productivity.

<!-- See the [Quick start section] of the docs for more examples. -->
