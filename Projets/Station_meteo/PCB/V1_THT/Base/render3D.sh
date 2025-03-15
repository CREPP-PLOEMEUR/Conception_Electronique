#!/bin/bash

# Trouver le fichier .kicad_pcb
pcb_file=$(ls *.kicad_pcb 2>/dev/null | head -n 1)

if [ -z "$pcb_file" ]; then
    echo "Aucun fichier .kicad_pcb trouvé dans le répertoire courant."
    exit 1
fi

echo "Fichier PCB trouvé : $pcb_file"
mkdir -p 3D_Gallery

# Définir les différentes vues
declare -A views
views=(
    [Top]="0,0,0"
    [Bottom]="180,0,0"
    
    [Side]="270,0,0"
    [Left]="270,0,90"
    [Right]="270,0,-90"
    [Front]="270,0,180"

    [Iso_1]="315,0,45"
    [Iso_2]="225,0,45"
    [Iso_3]="135,0,45"
    [Iso_4]="45,0,45"
)

# Générer les rendus
for name in "${!views[@]}"; do
    output_file="3D_Gallery/${name}.png"
    rotation="${views[$name]}"
    echo "Rendering $name view..."
    kicad-cli pcb render --floor --quality high --zoom 1.0 --rotate "$rotation" -o "$output_file" "$pcb_file"
done
