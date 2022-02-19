# blender-one-key-export
Blender plugin (operators) to export selection (and children) as fbx.
Those operators are designed with a very specific worlflow in mind.


## How to use

Press "F3" and type "One Key Exporter" then you can either use the "Snowdrop" or "Substaince Painter" export.

### Snowdrop

Every object with no parent in your selection get exported with all its children in a dedicated .fbx file named after the root object and placed next to the .blend file.
All their children, even if not selected or hidden, will be in their respective FBX file and forced visible.

### Substance Painter

Every object selected object and their children will be exported as one .fbx file in a "workfiles" directory next to the .blend file.
Any object containing "_col", "_scol" or "_mcol" (not case sensitive) will be ignored.
Every object with more than one UV will only keep its second UV in the export.
The .fbx file will be named after the first selected object with no parent, and if there is more than one, any suffix starting with "_" will be stripped from the name.
For example if you selected three root objects, "PROP_42_A", "PROP_42_B" and "PROP_42_C", the exported file will be named "PROP_42".
