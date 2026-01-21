# About
The Primo RPA robot Linux uses elements of the package to automate the processing of Open Document Format for Office Applications (ODF) and Office Open XML (also informally known as OOXML) document and workbook files.

# How to Use
In Primo RPA studio Linux, create a project that will be executed by  Primo RPA robot Linux. Install this package via the ".Dependencies -> Manage Dependencies" menu; the "ODF/OXML - Documents" and "ODF/OXML - Tables"  nodes with package elements will appear in Elements tree . 
### Documents
The "ODF document" element is a container for all other elements that are children of the "ODF/OXML - Documents" node. This element is used to connect to ODF/OXML document.  
In pure code projects use the element as follows:

```
//wf: [LTools.Common.Model.WorkflowData] parent algorithm link
//fileName - File path: [String] Path to a text document file (c:\folder\file.odt)
//bytes - Byte array: [byte[]] Document byte array
//pass - Password: [String] Document password
Primo.Office.OdfOxml.WordApp app = Primo.Office.OdfOxml.WordApp.Init(wf, fileName, [interop], [pass]);
Primo.Office.OdfOxml.WordApp app = Primo.Office.OdfOxml.WordApp.Init(wf, bytes, [interop], [pass]);
```

All other child elements of the "RDF/TO XML - Documents" node should be placed inside the "ODF document" container to process the document.
"Find text"	element in pure code:

```
//Searches for specified text in a document. 
//Properties
//app - [Primo.Office.OdfOxml.WordApp] ODF document application
//text - Text: [String] Text
List<int> idxs = app.FindText(text);
```
### Workbooks
The "ODF workbook" element is a container for all other elements that are children of the "ODF/OXML - Tables" node. This element is used to connect to ODF/OXML workbook.  
In pure code projects use the element as follows:

```
//wf: [LTools.Common.Model.WorkflowData] parent algorithm link
//fileName - File path: [String] Path to workbook document (c:\folder\file.ods)
//bytes - Byte array: [byte[]] Workbook bytes array
//csvDel - Delimiter: [String] Column delimiter
//interop - [LTools.Office.Model.InteropTypes] Driver: Connection driver type
//pass - Password: [String] Document password
Primo.Office.OdfOxml.ExcelApp app = Primo.Office.OdfOxml.ExcelApp.Init(wf, fileName, [csvDel], [interop], [loadAddIns], [isAttach], [pass]);
Primo.Office.OdfOxml.ExcelApp app = Primo.Office.OdfOxml.ExcelApp.Init(wf, bytes, [csvDel], [interop], [loadAddIns], [pass]);
```

All other child elements of the "RDF/TO XML - Tables" node should be placed inside the "ODF workbook" container to process the document.  
"Add sheet"	element in pure code:

```
//Element creates a new sheet in a workbook. 
//Properties
//app - [Primo.Office.OdfOxml.ExcelApp] Workbook application
//sheet - Name: [String] Sheet name
//sheetIdx - Index: [Int32] Sheet index
app.SheetAdd(sheet, [sheetIdx]);
```

# Key Features

- A large set of elements for diverse and high-quality processing of documents and workbooks
- High performance
- To use the package, Primo RPA Studio Linux must be installed, 
[details](https://docs.primo-rpa.ru/primo-rpa/primo-rpa-studio-linux/overview)

# Main Types

- Primo.Office.OdfOxml.WordApp
- Primo.Office.OdfOxml.ExcelApp

# Feedback

 Bug reports and contributions are welcome at [Primo RPA chat](https://t.me/primo_RPA_chat)