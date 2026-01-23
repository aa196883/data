#!/bin/bash
echo Adding metadata to $1!

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if metadata TSV needs to be regenerated from Excel
if [ ! -f "$SCRIPT_DIR/cadic_metadata.tsv" ] || [ "$SCRIPT_DIR/Skrid-Cadic.xlsx" -nt "$SCRIPT_DIR/cadic_metadata.tsv" ]; then
  echo "Generating metadata from Excel file..."
  python3 "$SCRIPT_DIR/extract_metadata.py"
  if [ $? -ne 0 ]; then
    echo "Error: Failed to extract metadata from Excel file"
    exit 1
  fi
fi

# Extract filename without path and extension
BASENAME=$(basename "$1" .musicxml)
# Extract SKRID-FICHIER code (format: Cadic-M-XXXXX+I-XXXXX-XXX -> M-XXXXX+I-XXXXX-XXX)
FICHIER_CODE=$(echo "$BASENAME" | sed 's/^Cadic-//')

# Get link from TSV file
LIEN=$(grep "^${FICHIER_CODE}" "$SCRIPT_DIR/cadic_metadata.tsv" | cut -f2)

# Extract version number (last 3 digits of filename)
VERSION=$(echo "$FICHIER_CODE" | grep -oE '[0-9]{3}$')

#################################
# ADD TITLE FROM <credit-words>
#################################

# extract first <credit-words>
TITLE=$(sed -n 's:.*<credit-words>\(.*\)</credit-words>.*:\1:p' "$1" | head -n 1)

if [ -n "$TITLE" ]; then
  if grep -q '<work-title>' "$1" ; then
    # replace existing work-title
    sed -r -i \
      "s|<work-title>.*</work-title>|<work-title>$TITLE</work-title>|g" \
      "$1"
  else
    # insert work/work-title after <score-partwise>
    sed -r -i \
      "s|<score-partwise>|<score-partwise><work><work-title>$TITLE</work-title></work>|" \
      "$1"
  fi
else
  echo "No <credit-words> found, skipping title"
fi

#################################
# ADDING THE COMPOSER
#################################

if grep -q '<creator type=\"composer\">' "$1" ;
then
  sed -r -i -e \
    's|<creator type="composer">.*</creator>|<creator type="composer">Collecté par François Cadic</creator><creator type="collection">François Cadic</creator>|g' \
    "$1"
else 
  sed -r -i -e \
    's|</identification>|<creator type="composer">Collecté par François Cadic</creator><creator type="collection">François Cadic</creator></identification>|g' \
    "$1"
fi

#################################
# ADDING THE SOURCE
#################################

# Build source string with link and version
if [ -n "$LIEN" ] && [ -n "$VERSION" ]; then
  SOURCE_TEXT="Chansons populaires de Bretagne (1899-1929) - François Cadic, CRBC, Dastum, PUR, 2010 - $LIEN - version $VERSION"
else
  SOURCE_TEXT="Chansons populaires de Bretagne (1899-1929) - François Cadic, CRBC, Dastum, PUR, 2010"
fi

if grep -q '<source>' "$1" ;
then
  sed -r -i -e \
    "s|<source>.*</source>|<source>$SOURCE_TEXT</source>|g" \
    "$1"
else 
  sed -r -i -e \
    "s|</identification>|<source>$SOURCE_TEXT</source></identification>|g" \
    "$1"
fi
