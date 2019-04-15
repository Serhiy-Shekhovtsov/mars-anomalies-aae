#!/bin/bash

echo "Creating folder..."
mkdir ./curiosity_landing_site

echo "Downloading ESP_028269_1755_RED1_1.IMG"
wget -r -nH --cut-dirs=5 --no-parent --reject="index.html*" https://hirise-pds.lpl.arizona.edu/PDS/EDR/ESP/ORB_028200_028299/ESP_028269_1755/ESP_028269_1755_RED1_1.IMG -P ./curiosity_landing_site

echo "Downloading ESP_028269_1755_RED3_1.IMG"
wget -r -nH --cut-dirs=5 --no-parent --reject="index.html*" https://hirise-pds.lpl.arizona.edu/PDS/EDR/ESP/ORB_028200_028299/ESP_028269_1755/ESP_028269_1755_RED3_1.IMG -P ./curiosity_landing_site
echo "Done!"

