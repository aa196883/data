#!/usr/bin/env python3
"""
Script to remove "CRBC, " from the <source> tag in MusicXML files.
"""

import sys
import os
import xml.etree.ElementTree as ET

def remove_crbc_from_source(musicxml_file):
    """Remove CRBC from source tag in MusicXML file."""
    try:
        tree = ET.parse(musicxml_file)
        root = tree.getroot()
        modified = False
        
        # Find the source element in identification
        for identification in root.findall('.//identification'):
            source = identification.find('source')
            if source is not None and source.text:
                if 'CRBC' in source.text:
                    source.text = source.text.replace('CRBC, ', '')
                    modified = True
        
        if modified:
            tree.write(musicxml_file, encoding='UTF-8', xml_declaration=True)
            print(f"Updated: {musicxml_file}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {musicxml_file}: {e}", file=sys.stderr)
        return False

def main():
    musicxml_dir = 'musicxml'
    
    if not os.path.isdir(musicxml_dir):
        print(f"Error: Directory {musicxml_dir} not found", file=sys.stderr)
        sys.exit(1)
    
    count = 0
    for filename in os.listdir(musicxml_dir):
        if filename.endswith('.musicxml'):
            filepath = os.path.join(musicxml_dir, filename)
            if remove_crbc_from_source(filepath):
                count += 1
    
    print(f"\nTotal files updated: {count}")

if __name__ == "__main__":
    main()
