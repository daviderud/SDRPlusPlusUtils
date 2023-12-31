# SDRPlusPlusUtils
 Utilities for SDRPlusPlus

 # import_FMSuite
Tool to import in SDRPlusPlus (https://github.com/AlexandreRouma/SDRPlusPlus/) a database of the SDRSharp (https://airspy.com/download/) plugin *FMSuite* (https://www.freqmgrsuite.com/).

The script is made to import bookmarks in the advanced bookmark manager by Darau Blé (https://github.com/darauble/bookmark_manager). However, it is compatible aswell with the standard SDR++ frequency manager module.

Tested version 2.0 with Python 3.10, SDRPlusPlus 1.1.0 and FMSuite 2.3. Bookmarks manager 0.1.7.

Run the script `import_FMSuite.py` with Python interpreter.

Select the FMSuite database (in `SDRsharp\Plugins\FMSuite\FMSuite.Databases`), select the output filename.

Then in SDRPlusPlus, in the bookmarks manager or frequency manager, select "Import" button. Create a new group beforehand is useful but not mandatory.

 # Netherlands frequency band plan
 
It's a work in progress. Merged into main (https://github.com/AlexandreRouma/SDRPlusPlus/blob/master/root/res/bandplans/netherlands.json).

I use the following colors in the `root/config.json`:

```json
...
    "bandColors": {
        "amateur": "#FF0000FF",
        "amateur1": "#CC0000FF",
        "aviation": "#00FF00FF",
        "broadcast": "#0000FFFF",
        "marine": "#00FFFFFF",
        "marine1": "#00CCCCFF",
        "military": "#FFFF00FF",
        "satellite": "#909090FF",
        "satellite1": "#505050FF",
        "utility": "#FFFF00FF",
        "utility1": "#AAAA00FF"
    },
    "bandPlan": "Netherlands",
    "bandPlanEnabled": true,
...
```