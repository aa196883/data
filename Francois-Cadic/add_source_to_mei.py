#!/usr/bin/env python3
"""
Script to extract <source> tag from MusicXML and insert it into MEI <sourceDesc>.
"""

import sys
import xml.etree.ElementTree as ET

# Register MEI namespace to preserve default namespace in output
ET.register_namespace('', 'http://www.music-encoding.org/ns/mei')

def extract_source_from_musicxml(musicxml_file):
    """Extract source text from MusicXML file."""
    try:
        tree = ET.parse(musicxml_file)
        root = tree.getroot()
        
        # Find the source element in identification
        for identification in root.findall('.//identification'):
            source = identification.find('source')
            if source is not None and source.text:
                return source.text.strip()
        return None
    except Exception as e:
        print(f"Error reading MusicXML file: {e}", file=sys.stderr)
        return None

def insert_source_into_mei(mei_file, source_text):
    """Insert source text into MEI file's sourceDesc and pgFooter."""
    try:
        # Parse MEI file with namespace
        tree = ET.parse(mei_file)
        root = tree.getroot()
        
        # MEI namespace
        ns = {'mei': 'http://www.music-encoding.org/ns/mei'}
        
        # Find fileDesc
        file_desc = root.find('.//mei:fileDesc', ns)
        if file_desc is None:
            print("Error: fileDesc not found in MEI file", file=sys.stderr)
            return False
        
        # Check if sourceDesc already exists
        source_desc = file_desc.find('mei:sourceDesc', ns)
        if source_desc is not None:
            # Remove existing sourceDesc
            file_desc.remove(source_desc)
        
        # Create new sourceDesc element
        source_desc = ET.Element('{http://www.music-encoding.org/ns/mei}sourceDesc')
        source_element = ET.Element('{http://www.music-encoding.org/ns/mei}source')
        source_element.text = source_text
        source_desc.append(source_element)
        
        # Insert sourceDesc after pubStmt (or at the end of fileDesc)
        pub_stmt = file_desc.find('mei:pubStmt', ns)
        if pub_stmt is not None:
            # Insert after pubStmt
            pub_stmt_index = list(file_desc).index(pub_stmt)
            file_desc.insert(pub_stmt_index + 1, source_desc)
        else:
            # Append at the end
            file_desc.append(source_desc)
        
        # Add source to pgFooter for rendering
        # Find the scoreDef element
        score_def = root.find('.//mei:scoreDef', ns)
        if score_def is not None:
            # Check if pgFoot already exists
            pg_foot = score_def.find('mei:pgFoot', ns)
            if pg_foot is None:
                # Create pgFoot element
                pg_foot = ET.Element('{http://www.music-encoding.org/ns/mei}pgFoot')
                pg_foot.set('{http://www.w3.org/XML/1998/namespace}id', 'pgfoot_source')
                # Insert pgFoot after pgHead if it exists, or at the beginning
                pg_head = score_def.find('mei:pgHead', ns)
                if pg_head is not None:
                    pg_head_index = list(score_def).index(pg_head)
                    score_def.insert(pg_head_index + 1, pg_foot)
                else:
                    score_def.insert(0, pg_foot)
            
            # Split source text into multiple lines (max 3 lines)
            # Split on " - " to break into logical parts
            parts = source_text.split(' - ')
            
            # Group parts into 3 lines with first two parts on line 1
            if len(parts) <= 2:
                lines = parts
            elif len(parts) == 3:
                line1 = parts[0] + ' - ' + parts[1]
                line2 = parts[2]
                lines = [line1, line2]
            else:
                # For 4 or more parts: combine first two on line 1
                line1 = parts[0] + ' - ' + parts[1]
                line2 = parts[2]
                line3 = ' - '.join(parts[3:])
                lines = [line1, line2, line3]
            
            # Create a rend element for each line
            for line in lines:
                rend = ET.Element('{http://www.music-encoding.org/ns/mei}rend')
                rend.set('halign', 'center')
                rend.set('valign', 'bottom')
                rend.set('fontsize', 'small')
                rend.text = line.strip()
                pg_foot.append(rend)
        
        # Write back to file
        tree.write(mei_file, encoding='UTF-8', xml_declaration=True)
        return True
        
    except Exception as e:
        print(f"Error processing MEI file: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: add_source_to_mei.py <musicxml_file> <mei_file>", file=sys.stderr)
        sys.exit(1)
    
    musicxml_file = sys.argv[1]
    mei_file = sys.argv[2]
    
    # Extract source from MusicXML
    source_text = extract_source_from_musicxml(musicxml_file)
    if source_text is None:
        print(f"Warning: No source found in {musicxml_file}", file=sys.stderr)
        sys.exit(0)  # Not an error, just no source to add
    
    # Insert into MEI
    if insert_source_into_mei(mei_file, source_text):
        print(f"Successfully added source to {mei_file}")
    else:
        print(f"Failed to add source to {mei_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
