from kipy import KiCad

from kipy.board_types import (
    BoardLayer,
    Zone,
    
)
from kipy.common_types import PolygonWithHoles, base_types_pb2
from kipy.geometry import PolyLine, PolyLineNode
from kipy.util import from_mm
from kipy.proto.common.commands import GetItems
class PCBA_handler:
    def __init__(self, pcb_file):
        try:
            self.__kicad = KiCad()
            self.__version = self.__kicad.get_version()
            print(self.__version)
            self.__board = self.__kicad.get_board()
            self.__projectName = self.__board.get_project().name
            print("Opening project : " + self.__projectName)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de KiCAD: {e}")
            return

        try:
            self.__commit = self.__kicad.get_board().begin_commit()
        
            self.__footprints = self.__kicad.get_board().get_footprints()

            print(f"Number of footprints: {len(self.__footprints)}")

        # 🔒 Verrouiller toutes les empreintes
            for footprint in self.__footprints:
                if(footprint.reference_field.text.value == "SW2"):
                    footprint.locked = True
    
                #footprint.locked = True
            #print(f"Footprint {footprint.reference_field.text.value} locked.")
        except Exception as e:
            print(f"Erreur lors de l'accès aux empreintes: {e}")
    def begin(self):
        kicad = KiCad()
        board = kicad.get_board()
        board.add_to_selection(id)
        request = GetItems()
        print(dir(request))  # Affiche les options disponibles
        #request.types.append("footprint") # Remplace par la référence du composant que tu veux récupérer

        response = board.get_items(request)
        if response.items:
            print("OK")
        #f[50].locked = True
        #print(f[50].proto)
        #f[50].proto.locked = True;
        """for fo in f:
            print(fo)
            print(fo.proto.)
            print(fo.datasheet_field.text.value)
            fo.datasheet_field.text.value = "TETS"""

        outline = PolyLine()
        outline.append(PolyLineNode.from_xy(from_mm(100), from_mm(100)))
        outline.append(PolyLineNode.from_xy(from_mm(110), from_mm(100)))
        outline.append(PolyLineNode.from_xy(from_mm(110), from_mm(110)))
        outline.append(PolyLineNode.from_xy(from_mm(100), from_mm(110)))
        outline.append(PolyLineNode.from_xy(from_mm(100), from_mm(100)))
        polygon = PolygonWithHoles()
        polygon.outline = outline
        zone = Zone()
        zone.layers = [BoardLayer.BL_F_Cu, BoardLayer.BL_B_Cu]
        zone.outline = polygon
        board.create_items(zone)

    def end(self):
        try:
            self.__kicad.get_board().push_commit(self.__commit, "Locked footprints")
            #self.__kicad.get_board().save()
            self.__kicad.get_board().save_as("Base.kicad_pcb", True)
            print("Modifications enregistrées.")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des modifications: {e}")


# Exécution
pcba = PCBA_handler("Base.kicad_pcb")
pcba.begin()  
  
