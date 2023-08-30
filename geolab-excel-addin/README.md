# `geolab` Microsoft Excel Addin

Microsoft Excel Addin for [**geolab**](https://github.com/patrickboateng/geolab)

## Installation

**Note**: _All the instructions shown below were tested on **Microsoft Excel 2016** and **Windows
10**_

### Add Folder To Trusted Locations

Add this folder **C:\Users\username\AppData\Roaming\Microsoft\AddIns** to Microsoft Excel
**Trusted Locations** to prevent Excel from disabling the addin.

**Note**: _You can use any folder of choice but I highly recommend the folder above as it is
the default folder location for Microsoft Excel Addins. Make sure to turn on hidden items if
you are using the folder above on the File Explorer, as **AppData** is a hidden folder by default.
Follow the steps below to enable hidden items_.

```mermaid

     graph LR;
         A(Open file Explorer)-->B(Click on the View tab)
         B(Click on the View tab)-->C(Go to Show/hide ribbon)
         C(Go to Show/hide ribbon)-->D(Check Hidden items)
```

Follow the steps on Microsoft Support website [**here**](https://support.microsoft.com/en-us/office/add-remove-or-change-a-trusted-location-in-microsoft-office-7ee1cdc2-483e-4cbb-bcb3-4e7c67147fb4).
to add the folder to **Trusted Locations**. You can also follow [**this**](https://www.youtube.com/watch?v=AhnOU-ulqNg&t=7s)
video tutorial.

### Install Addin

- Download addin [here](https://github.com/patrickboateng/geolab/releases/tag/v1.0.0).
- Place the file (geolab-1.0.0-win-x64.xlam) into the folder you added to **Trusted Locations**.
- Follow [**this**](https://www.youtube.com/watch?v=reuU2zUsEPM) example video tutorial to load the addin.
  If you prefer reading, use [**this**](https://www.excelcampus.com/vba/how-to-install-an-excel-add-in-guide/)
  resource.

### Install Excel-DNA

**Note**: _This step is Optional but highly recommended, this provides intellisense on the custom functions_

- Download the **ExcelDna.IntelliSense64.xll** addin [here](https://github.com/Excel-DNA/IntelliSense/releases/tag/v1.4.2).
- Follow the same steps [**above**](#install-soil-classifier-addin)

## Documentation

_A comprehensive documentation is underway, for now use documentation provided in Microsoft Excel to learn about custom
functions_

The two functions provided are as follows:

- **AASHTO**
- **USCS**
