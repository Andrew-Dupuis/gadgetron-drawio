# Python code to illustrate parsing of Gadgetron Configuration XML files

import sys
import xml.etree.ElementTree as ET
  
def parseConfig(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    if root.tag == "configuration":
        readers = []
        for reader in root.find("readers"):
            #print(reader.tag, reader.attrib)
            new_reader = {}
            for child in reader:
                #print(child.tag, child.text)
                new_reader[child.tag] = child.text
            readers.append(new_reader)
        
        writers = []
        for writer in root.find("writers"):
            #print(writer.tag, writer.attrib)
            new_writer = {}
            for child in writer:
                #print(child.tag, child.text)
                new_writer[child.tag] = child.text
            writers.append(new_writer)

        gadgets = []
        for gadget in root.find("stream"):
            #print(gadget.tag, gadget.attrib)
            new_gadget = {}
            new_gadget["properties"] = []
            for child in gadget:
                if(child.tag == 'property'):
                    #print(child.tag, child.attrib)
                    property = {}
                    for property_child in child:
                        #print(property_child.tag, property_child.text)
                        property[property_child.tag] = property_child.text
                    new_gadget["properties"].append(property)
                else:
                    #print(child.tag, child.text)
                    new_gadget[child.tag] = child.text
            gadgets.append(new_gadget)
    
    if root.tag == "{http://gadgetron.sf.net/gadgetron}gadgetronStreamConfiguration":
        readers = []
        for reader in root.findall("{http://gadgetron.sf.net/gadgetron}reader"):
            #print(reader.tag, reader.attrib)
            new_reader = {}
            for child in reader:
                #print(child.tag, child.text)
                short_tag = child.tag.replace('{http://gadgetron.sf.net/gadgetron}','')
                new_reader[short_tag] = child.text
            readers.append(new_reader)
        
        writers = []
        for writer in root.findall("{http://gadgetron.sf.net/gadgetron}writer"):
            #print(writer.tag, writer.attrib)
            new_writer = {}
            for child in writer:
                #print(child.tag, child.text)
                short_tag = child.tag.replace('{http://gadgetron.sf.net/gadgetron}','')
                new_writer[short_tag] = child.text
            writers.append(new_writer)

        gadgets = []
        for gadget in root.findall("{http://gadgetron.sf.net/gadgetron}gadget"):
            new_gadget = {}
            new_gadget["properties"] = []
            for child in gadget:
                if(child.tag == '{http://gadgetron.sf.net/gadgetron}property'):
                    #print(child.tag, child.attrib)
                    property = {}
                    for property_child in child:
                        short_tag = property_child.tag.replace('{http://gadgetron.sf.net/gadgetron}','')
                        #print(short_tag, property_child.text)
                        property[short_tag] = property_child.text
                    new_gadget["properties"].append(property)
                else:
                    short_tag = child.tag.replace('{http://gadgetron.sf.net/gadgetron}','')
                    #print(short_tag, child.text)             
                    new_gadget[short_tag] = child.text
            gadgets.append(new_gadget)
    configuration = {}
    configuration['readers'] = readers
    configuration['writers'] = writers
    configuration['gadgets'] = gadgets
    return configuration
  
def saveToDrawIO(configuration, filename):
    blockWidth = 800
    blockHeight = 40
    propertyHeight = 20
    blockGap = 20

    # create the file structure
    mxGraphModel = ET.Element('mxGraphModel')
    root = ET.SubElement(mxGraphModel, 'root')
    base = ET.SubElement(root,'mxCell')
    base.set('id','0')
    parent = ET.SubElement(root,'mxCell')
    parent.set('id','1')
    parent.set('parent','0')

    nextBlockStartY = 0
    for idx, reader in enumerate(configuration['readers']):
        new_reader = ET.SubElement(root, 'mxCell')
        new_reader.set('id','reader'+str(idx))
        new_reader.set('value',reader['classname']+'\n('+reader['dll']+')')
        new_reader.set('style','fillColor=#d5e8d4;fontColor=#000000;')
        new_reader.set('parent','1')
        new_reader.set('vertex','1')
        geometry = ET.SubElement(new_reader,'mxGeometry')
        geometry.set('y', str(nextBlockStartY))
        geometry.set('width',str(blockWidth))
        geometry.set('height',str(blockHeight))
        geometry.set('as','geometry')
        nextBlockStartY = nextBlockStartY + blockHeight + blockGap

    for idx, gadget in enumerate(configuration['gadgets']):
        if idx>0:
            new_arrow = ET.SubElement(root,'mxCell')
            new_arrow.set('id', 'arrow'+str(idx))
            new_arrow.set('style','edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;')
            new_arrow.set('parent','1')
            new_arrow.set('source','gadget'+str(idx-1))        
            new_arrow.set('target','gadget'+str(idx)) 
            new_arrow.set('edge','1') 
            geometry = ET.SubElement(new_arrow,'mxGeometry')
            geometry.set('relative', '1')
            geometry.set('as','geometry')       
        new_gadget = ET.SubElement(root, 'mxCell')
        new_gadget.set('id','gadget'+str(idx))
        new_gadget.set('value',gadget['classname']+'\n('+gadget['dll']+')')
        new_gadget.set('parent','1')
        new_gadget.set('vertex','1')

        currentHeight = blockHeight
        if len(gadget['properties']) == 0:
            new_gadget.set('style','fillColor=#fff2cc;fontColor=#000000;align=center;')
        else:
            new_gadget.set('style','fillColor=#fff2cc;fontColor=#000000;align=left;spacingLeft=5;')
            currentHeight = propertyHeight*len(gadget['properties'])
            if(currentHeight < blockHeight):
                currentHeight = blockHeight

        geometry = ET.SubElement(new_gadget,'mxGeometry')
        geometry.set('y', str(nextBlockStartY))
        geometry.set('height',str(currentHeight))
        geometry.set('width',str(blockWidth))
        geometry.set('as','geometry')

        for idy, property in enumerate(gadget['properties']):
            new_property = ET.SubElement(root,'mxCell')
            new_property.set('id','gadget'+str(idx)+'property'+str(idy))
            new_property.set('value',str(property['name'])+': '+str(property['value']))
            new_property.set('style','fillColor=#ffffff;fontColor=#000000;align=left;spacingLeft=5;') 
            new_property.set('parent','gadget'+str(idx))
            new_property.set('vertex','1')
            geometry = ET.SubElement(new_property,'mxGeometry')
            geometry.set('x', str(blockWidth/2))
            geometry.set('y', str(propertyHeight * idy)) 
            geometry.set('width',str(blockWidth/2))
            geometry.set('height',str(propertyHeight))
            geometry.set('as','geometry')
        
        nextBlockStartY = nextBlockStartY + currentHeight + blockGap

    for idx, writer in enumerate(configuration['writers']):
        new_writer = ET.SubElement(root, 'mxCell')
        new_writer.set('id','writer'+str(idx))
        new_writer.set('value',writer['classname']+'\n('+writer['dll']+')')
        new_writer.set('style','fillColor=#f8cecc;fontColor=#000000;')
        new_writer.set('parent','1')
        new_writer.set('vertex','1')
        geometry = ET.SubElement(new_writer,'mxGeometry')
        geometry.set('y', str(nextBlockStartY))
        geometry.set('width',str(blockWidth))
        geometry.set('height',str(blockHeight))
        geometry.set('as','geometry')
        nextBlockStartY = nextBlockStartY + blockHeight + blockGap

    # create a new DrawIO XML file with the results
    mydata = ET.tostring(mxGraphModel, encoding='unicode')
    diagramFile = open(filename, "w")
    diagramFile.write(mydata)
     
def main():
    if len(sys.argv) > 1:
        inputFilePath = sys.argv[1]
        #inputFilePath = "examples/default.xml"
        outputFilePath = inputFilePath.replace('.xml', '_diagram.drawio')
        configuration = parseConfig(inputFilePath)
        saveToDrawIO(configuration, outputFilePath)
    else:
        print("Missing first argument: config.xml")

if __name__ == "__main__":
    main()