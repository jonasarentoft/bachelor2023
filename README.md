# bachelor2023
### af Søren Bo Dall og Jonas Arentoft

## How To
* Læg data ind i data/raw
* Stil dig i src/ mappen
* Kør "make pipeline FILENAME='[INDSÆT FILNAVN HER]'"

## Overview
* **01_get_nodes_in_highways** 
    * Løber vejene i den angivne .xml fil igennem og udtrækker alle de noder på veje for hvem der har 'highway' som tag. Data bliver skrevet i filen nodesInHighways.txt, og bliver efterfølgende sorteret og skrevet i nodesInHighwaysSorted.txt

* **02_get_positions_of_nodes**
    * Løber noderne i den angivne .xml fil igennem og tjekker, om noden findes i nodesInHighwaysSorted.txt. Hvis ja, udtrækkes latitude og longtitude på noden, og data bliver skrevet i filen nodesAndPositions.txt, hvor hver linje har formatet (nodeID,lon,lat)

* **03_create_plot**
    * Bruger nodesAndPositions.txt filen til at plotte punkter

* **04_get_edges**
    * Løber vejene i den angivne .xml fil igennem og udtrækker endnu engang alle de noder på veje for hvem der har 'highway' som tag. Dernæst benyttes Binarcy Search til at slå op i nodesAndPosition.txt (02) for at udtrække latitude og longtitude på noderne, og endeligt bliver afstanden mellem de to noder beregnet.Data bliver skrevet i filen edges.txt, og bliver eftefølgende sorteret og skrevet i edgesSorted.txt, hvor hver linje har formatet (nodeID_1, nodeID_2, distance), og hvor der bliver skrevet en ekstra linje med (nodeID_2, nodeID_1, distance) hvis den pågældende vej ikke har 'oneway' som tag.



