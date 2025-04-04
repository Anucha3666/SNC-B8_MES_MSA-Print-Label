import os
import shutil
import uuid
from datetime import datetime

import requests

from app.types import TREQ_PostPrintLabel
from app.utils import extract_number, find_part_code


def generate_zpl_label(data_request: TREQ_PostPrintLabel):
    content = data_request.get('form_data', {})
    num = extract_number(data_request['serial_number'])
    num_move_x = 700 - (len(str(num)) * 12)
    part_code = str(content.get('model', '')).split()[0]
    part_code_len = len(str(part_code))
    if (part_code_len < 9):
        part_code_size =  "80"
        part_code_move_y = "326"
        part_code_move_x = 600 - (len(str(part_code)) * 18)
    else:
        part_code_size =  "50"
        part_code_move_y = "334"
        part_code_move_x = 600 - (len(str(part_code)) * 12)
    part_name = str(content.get('model', ''))[len(part_code):len(content.get('model', ''))]
    quantityStd_move_x = 650 - (len(str(content.get('quantityStd', 0))) * 40)

    zpl_content = """
    ^XA
    ^PW818
    ^LL1080
    ^FO130,34^GB5,76,5^FS
    ^FO30,30^GFA,1080,1080,12,,O01C1E,O07E1F8,O0FE3FC,N03FF3FF,N07FF3FF8,M01IF3FFE,M03IF3IF,M0JF3IFC,L01JF3IFE,L07JF3JF8,L0KF3JFC,K03KF3KF,K07KF3KF8,J01LF3KFE,J03LF3LF,J0MF3LFC,I01MF3LFE,I07MF3MF,I0NF3MFC,003NF3MFE,007NF3NF8,01OF3NFC,03OF3OF,07OF3OF,:03OF3OF,03OF3NFE,00OF3NFC,007NF3NF,001NF3MFE,060NF3MF838,0F83MF3MF07C,1FC1MF3LFC1FE,1FF07LF3LF87FE,1FF83LF3KFE0FFE,1FFE0LF3KFC3FFE,1IF07KF3KF07FFE,1IFC1KF3JFE1IFE,1IFE0KF3JF83IFE,1JF83JF3JF0JFE,1JFC1JF3IFC1JFE,1KF07IF3IF87JFE,1KF83IF3FFE0KFE,1KFE0IF3FFC3KFE,1LF07FF3FF07KFE,1LFC1FF3FE1LFC,0LFE0FE3F83LFC,07LF83E1F0MF,01LFC1C0C1LFE,00MFJ07LF8,003LF8I0MF,061LFE003LFC1,0F07LF007LF87C,1FC3LFC1LFE0FE,1FE0LFE1LFC3FE,1FF87KFE3LF07FE,1FFC1LF3KFE1FFE,1IF0LF3KF83FFE,1IF83KF3KF0IFE,1IFE1KF3JFC1IFE,1JF07JF3JF87IFE,1JFC3JF3IFE0JFE,1JFE0JF3IFC3JFC,0KF87IF3IF07JFC,07JFC1IF3FFE1KF,01KF0IF3FF83JFE,00KFC3FF3FF0KF8,003JFE1FF3FC1KF,001KF87E3F87JFC,I07JFC3E1E0KF8,I03KFJ03JFE,J0KF8I07JFC,J07JFE001KF,J01KF003JFE,K0KFC0KF8,K03JFE1KF,K01JFE3JFC,L07JF3JF8,L03JF3IFE,M0JF3IFC,M07IF3IF,M01IF3FFE,N0IF3FF8,N03FF3FF,N01FF3FC,O07E3F8,O03E1E,,:^FS
    ^FO150,40^A0N,50,50^FDMES B8^FS
    ^FO150,95^A0N,25,25^FDManufacturing Execution System B8^FS
    ^FO30,138^GB760,2,2^FS
    ^FO30,138^GB2,259,2^FS
    ^FO430,138^GB2,259,2^FS
    ^FO790,138^GB2,259,2^FS
    ^FO30,190^GB760,2,2^FS
    ^FO30,235^GB760,2,2^FS
    ^FO30,285^GB760,2,2^FS
    ^FO30,396^GB760,2,2^FS
    ^FO40,205^A0N,25,25^FDSupplier : SNC SERENITY COMPANY^FS
    ^FO40,295^A0N,25,25^FDPart Name : ^FS
    ^FO440,295^A0N,25,25^FDPart Code :^FS
    ^FO580,410^A0N,25,25^FDQuantity (Unit) :^FS
    ^FO40,410^A0N,25,25^FDPicture of Part :^FS
    """
    zpl_content += f"^FO{num_move_x},50^A0N,60,60^FD{num}^FS" # 12
    zpl_content += f"""
    ^FO40,155^A0N,25,25^FDCustomer : {content.get('customerName', '-')}^FS
    ^FO440,155^A0N,25,25^FDModel : {str(content.get('model', '')).split()[-1]}^FS
    ^FO440,205^A0N,25,25^FDJob No : {content.get('jobOrder', '-')}^FS
    ^FO40,253^A0N,25,25^FDOrder : {content.get('producer', '-')}^FS
    ^FO440,253^A0N,25,25^FDDate : {content.get('date', '-')}^FS
    ^FO40,340^A0N,35,35^FD{part_name}^FS
    ^FO580,580^BQN,2,7,10^FDQA,{data_request['serial_number']}^FS
    ^FO580,580^BQN,2,7,10^FDQA,{data_request['serial_number']}^FS
    ^FO40,780^A0N,30,30^FD{data_request['serial_number']} ({content.get('color', '-')})^FS
    """
    zpl_content += f"^FO{part_code_move_x},{part_code_move_y}^A0N,{part_code_size},{part_code_size}^FD{part_code}^FS" # 10
    zpl_content += f"^FO{quantityStd_move_x},450^A0N,150,150^FD{content.get('quantityStd', '-')}^FS" # 35

    if content.get('model', '-') == "2292333 Panel pattern Y1G" :
        zpl_content += "^FO40,460^GFA,17100,17100,57,,:S07QF8,Q03VF8003FC,Q0FET0RF,P018gH0PF,P018gM03OF,P018gR03NFC,Q08gW03LF,P018hH07IFC,P018hL07LF,P01hR07NF,P014hU01NFC,P014i07MFE,P01CS03E001ChL0NF8,P03CS0CI0E7hP07MFE,P03CS08K08hS01NF,P03CR018K04hX0NF8,P03ES0CJ016iH03MF8,P03ES04K08iL01LFEF0018,P03ES04J028iP07MFC,P027S04K0CiT07IFE,P023S04K0CiW07F8,P02AS04001804iY0C,P0228R04004024iY03,P0278R061F0024iY01,P02FCR02EI024j08,P027CR02080024j08,P065CR02080024j0C,P067E8Q0208I04j04,P063ECQ02K04j04,P063F4Q02K04j04,P073ECQ02K06iX0204,P051F4Q02K06j04,P0D1F4Q03040012j04,P0D0F6Q01040012j04,P058FAQ01040012j04,P0686BQ01040012j04,P018488P01040012j04,P01F0C4P01040012j04,P01F04Q01040012j06,P01F842P01040012j06,P01B861P03K02j06,P018C208O018J03j06,P0184204O018J03j02,P0102102P0F2I06j02,P0103001P03JFCj02,P0103I08jU02,P03028004jU02,P0302C002jU02,P0306C031jU02,P0204A0388jT02,P0204B03C4jT02,P0204982A2jT02,P020588391jT02,P0605047088jS02,P0605027FC4jS02,P060D033C62jS03,P0409019C31jS03,P040900C2188jR03,P040900610C4jR01,P040B0030872jR01,P0C0A00185F1jR01,P0C0AI0C3F88jQ01,P081AI0638A4jQ01,P0812I031CF2jQ01,P0812I018FD9jQ01,P0812J0C7FC8jP01,P0816J0637E4jP01,O01814J0313F2jP01,O01814J0181F9jP01,O01034K0C0FC8jO01,O01024K0607C4jO01,O01024K0303EjP01,O0102CK0181F2jO01,O0102CL040F9jO018O03028L0207C8jN018O03068L0107C8jN018O02068M083E4jL06018O02048M061EjL01FC08O02048M030C2jK038E08O02058M018jM030608O0205O0C01jK010608O0605O06jM01FE08O060DO03008jK07C08O040DO01808jN08O0409P04jP08O0409P0204jN08O040BP0184jN08O040AQ084jN08O0C0AQ04jO08O0C1AQ06jO08O0812Q022jN08::O0816Q032jN08O0814Q032jN08N01814Q032jM018N01834Q032jM018N01024Q072jM01,N01024Q062jM01,:N0102CQ062jM01,N01028Q062jM01,N03028Q062jM01,N03068Q062jM03,N02048Q0E2jM02,N02048Q0C2jM02,N02048P03C2jM02,N02058P0C42jM02,N0605Q0C42jM02,N0605Q0942jM02,N060DQ08CjN06,N0409Q08jO06,N0409Q08jO04,N040BP018jO04,N040BP01304jM04,N0C0AP010C4jM04,N0C1AP010E4jM04,N0C1AP010A4jM04,N0812P010A4jM0C,N0812P030A4jM08,N0816P030A4jM08,N0814P020EjN08,M01814P021EjN08,M01834P0216jN08,M01824P02148jM08,M01024P02148jL018,M01024P06148jL01,M0102CP06148jL01,M03028P04148jL01,:M03068P043CjM01,M03048P042CjM01,M02048P0429jM03,M02048P0C29jM02,M02058P0829jM02,M0605Q09E9jM02,M0605Q0CF9jM02,M060DQ0678jM02,M0609Q019jN02,M0409Q01CjN06,M0409Q0182jM04,M040BQ0182jM04,M0C0AQ0182jM04,:M0C1AQ018jN04,M0812Q038jN04,M0812Q038jN0C,M0812Q03jO08,M0816Q0304jM08,L01814Q0304jM08,:L01034Q0FjO08,L01024P033jO08,L01024P033jN018,L01024P03AjN01,L0102CP01E08jL01,L03028Q0708jL01,L03028Q0308jL01,L02068Q03CjM01,L02048P01FCjM01,L02048P0FBCjM03,L02058O01DFCjM03,L02058O011FDjM02,L0605P011CDjM02,L060DP031C9jM02,L040DP0317CjM02,L0409P0211FjM02,L0409P02103EjL06,L040BP0230038jK04,L040BP03A0018jK04,L0C0AQ0EI08jK04,L0C1AQ020018jK04,L081AQ060018jK04,L0812Q060018jK04,L0812P03E0018jK0C,L0816P07E001jL08,L0814P044001jL08,K01814P044001jL08,K01834P0C4003jL08,K01024P0C4003jL08,K01024P084003jL08,K01024P08JFjK018,K0102CP08E7FEjK01,K01028P08FCFEjK01,K03028P088F86jK01,K03068P0C80FEjK01,K02048P0480C6jK01,K02048P03807EjK01,K02048P0183FEjK03,K02058P0107ECjK02,K0205Q030FACjK02,K0605Q0789F8jK02,K0E0DQ0DF91jL02,K0C09Q0608jM02,J01C09Q0308jM02,J07409Q01CAjM06,J0440BQ01BAjM04,J0CC0AQ019AjM04,J0CC0AQ0182jM04,J08C1AQ0182jM04,J08812Q038jN04,J0E812Q03jO0C,J08816Q0304jM0C,I018816Q0304jM08,I015814Q0304jM08,I015834Q0304jM08,I035834Q0304jM08,I021024Q07jO08,I021024P01EjN018,I02302CP06208jL01,:I063028P04A08jL01,I073C78P04608jL01,I071FE8P04jO01,I07I0CP048jN01,I0FI0FFCN0CE1jM03,I0F88380FFEL0C71jM02,I0783FCI0IF8I08F9jM02,I07E7E4K03IF08F9jM02,I07E43CN03C8F9jM02,I07EC34O078FjN02,I03CE1CO078FjN02,I03E21CO0C8D2jM06,I03E718O091D2jM04,I03E308N0191D2jM04,I03F188N0191F2jM04,I01F1C8N0191BjN04,I01F8E8O091AjN04,I01F868O091A4jM04,J0FC3CO0B3A4jM0C,J0BC3IFEL0A3A4jM08,J0FC1C007FF8I0A3E4jM08,J05C0EJ01FFE0A36jN08,J07C07M07FE34jN08,J02C0388M0E748jM08,J03001CEM0EF48jL018,J01I0EBM0C7C8jL018,K0800798L043CjM01,K0C001CCL061CjM01,K04I0E6L078jN01,K02I0718K06C1jM01,K030023CCK0461jM01,K018030E6K04E1jM03,L0803871K06CjN02,L040383CCJ06CjN02,L0207C0E6J02C2jM02,L010730798I03C2jM02,M087181CCI03CjN02,M0470C0F3I03CjN02,M03387039C003C4jM06,M019E180E600384jM04,N0CF0607180184jM04,N0678301CC018jN04,N031E180730188jM04,N01CF08038C388jM04,O067D800E6388jM0C,O031FE003B58jN0C,O01CFF801FD1jN08,P063FE00691jN08,P030F38016jO08,Q0C78F0042jN08,Q063E1E002jN08,Q018F82004jM018,R0E3E3004jM01,R038FF008jM01,S0C3F008jM01,S070201jN01,S01E002jN01,T0380CjN03,U0FFjO03,V0FCjN02,W0FEjM02,X07F8jK02,g0FF8jI02,gH0FFCjG02,gJ0IFiY06,gL03FFEiV04,gO07FFEiS04,gR07IFiP04,gU07IF8iL04,gX03IFCiI04,hH0JFi0C,hK03IFChV08,hN01JF8hR08,hR07IFEhO08,hV0JF8hK08,hY03IFEhG018,iI0JF8gW018,iL01JFgT01,iP07IFEgP01,iT0KFgL02,iX07KFCg06,jI03NFS0C,jP03TF,,:::^FS"
    elif content.get('model', '-') == "2142553  Panel pattern Y1N"  :
        zpl_content += "^FO40,460^GFA,16872,16872,57,,::J0kKFC,J0kLFE,J0gMF7F7iUF7FC,I01IFC3gIFBiWFDE,I077C0MFP07NFB8iO01LFB8,I0LF03LFCNF7JF83iTFC7F9FC,001B800MF007FCM01JFgV01gFEU01KFC7E,0036L03LFEjSF1F,007CR0EFChN01gFEg0FFDD80078Q03FEjQ01FF7800F8Q07FjS03B6800FQ01DCjT0DF801EQ03FjU07F801EQ07EjU03F,014Q0F8jU03F,03CQ0FjV01E,03CP01FjV01E,03CP036jV01E,03CP03CjV01E,028P068jV01E,028P078jV01E,028P078jV014,028P05jW014,:078P0FjW014,::::::078P0AjW014,::078O01EjW014,:05P01EjW014,:::05P014jW014,:::0FP014jW014,0F00KFC003CjW014,0NFE003CjW014,0NF7003CjW014,0DDC7IFBF003CjW014,0CF7KFD803CjW014,0EFFEI0F7803CjW014,0FF04I0F7803CjW014,0FFBCI0A7802CjW014,0EFFCI0A78028jW014,0IFCI0A78028jW014,0DFFJ0A78028jW014,0D7CJ0A78028jW014,0D7CI01E78078jW014,0D3CI01E70078jW014,0D3CI01E50078jW014,:0FBCI01E50078jW014,0F9CI01E50078jW014,0F9CI01ED0078jW014,0F9CI01EF0078jW014,::1F88I01EF005jX014,:::1FC8I01EF00FjX014,1FC8I016F00FjX014,1FC8I014F01F8jW014,1FE8I014F01F8jW014,1FE8I014F00F8jW014,1BE8I014F00FjX014,1BF8I014F00FjX014,:1AF8I03CA00FjX014,:1AF8I03CA00AjX014,::::1A78I03CA00AjX014,1A78I03DE00AjX014,1A78I03DE01EjX014,:1A38I03DE01EjX014,:1B38I03DE01EjX014,:1F38I03DE01EjX014,1F1J03DE01F8jW014,:3F38I03DE01F8jW014,3F3EI03DE01F8jW014,3F36I03DE01EjX014,3F3EI03DE01EjX014,3F1AI03DE01EjX014,3F1AI03DE01CjX014,3F1AI03DE014jX014,3F1AI02DE014jX014,3F1AI029E014jX014,::3F9AI029E014jX014,:3F9AI029E03CjX014,3FBEI029E03CjX014,3FFEI029E03CjX014,3FFCI029E03CjX014,3F9J029603CjX014,3F9J029401CjX014,3F9J029403CjX014,3FDJ029403CjX014,::3FDJ079403CjX014,3FFJ079403CjX014,:::37FJ079403CjX014,:35FJ079403CjX014,:::35FJ07BC03CjX014,::::35FCI07BC03CjX014,3DFCI07BC03CjX014,3DFEI07BC03CjX014,09FEI07BC03CjX014,:09FEI07BC02CjX014,09FEI07BC028jX014,1IF8007FC0FCjX01C,1D7F800FBC0BCjX016,1IF8007FC0FCjX01C,0BFEI07BC03CjX014,::::0BFCI07BC03CjX014,:0BFJ07BC03CjX014,:09FJ07BC03CjX014,:09FJ079403CjX014,:1DFJ079403CjX014,:1FFJ079403CjX014,::::::::1FDJ079603CjX014,1F9J079E03CjX014,1F9J029E014jX014,::1FFCI029E014jX014,1FFEI029E014jX014,:1F9EI029E014jX014,1F9AI029E014jX014,::3F1AI029E014jX014,::3F1AI02DE016jX014,3F1AI03DE01EjX014,::3F3EI03DE01EjX014,:3F3CI03DE01EjX014,371J03DE01EjX014,3738I03DE01EjX014,::3F38I03DE01EjX014,:3F78I03DE01EjX014,1A78I03DE01EjX014,:1A78I03DE00AjX014,1A78I03DA00AjX014,1AF8I03CA00AjX014,::::1AF8I03CA00FjX014,:1AF8I014F00FjX014,1BF8I014F00FjX014,:1BE8I014F00FjX014,::1BC8I014F00FjX014,1BC8I01EF00FjX014,1B88I01EF005jX014,1F88I01EF005jX014,::1F9CI01EF005jX014,1F9CI01EF0078jW014,:0F9CI01ED0078jW014,0F9CI01E50078jW014,:0FBCI01E50078jW014,0F3CI01E50078jW014,0D3CI01E50078jW014,0D7CI01E78078jW014,0D7CI01E78028jW014,0D7EJ0A78028jW014,0DFFCI0A78028jW014,0IFCI0A78028jW014,:0FF04I0E7803CjW014,0FC44I0F7803CjW014,0CNF803CjW014,0DECLF803CjW014,0JFC5FFB003CjW014,0OF003CjW014,0F3LFE003CjW014,0FL0FI014jW014,0FP014jW014,05P014jW014,::05P01EjW014,::::078O01EjW014,078P0AjW014,:::078P0FjW014,:::::028P05jW014,:028P078jV014,:028P078jV01E,028P03CjV01E,03CP03CjV01E,03CP01EjV07E,03CP01BjV0FE,014Q0D8jU07E,01EQ06CjU07F,01EQ037jU07D801BQ01F8jT0FF800FR0EEjS01F7800F8Q03FCjR0I78006CQ01EF8jP03DDF8003ER07DjRF79F,001FN03JFBhKFCgL03YFE3F,I0DCJ03KF803NFCL0iUFE78FE,I07F003IF03TFC0267gQFEgL03YF7FC,I03BIFE1JFCO0PF8gI01gUF8R0FDIF,I03JF80UF733IFC79iWFC,I037JFU0OF8gK0gUF8R0JF,I01kLF,,:::^FS"

    return zpl_content + "^XZ"

def read_zpl_file(file_path):
    try:
        with open(file_path, 'r') as file:  # Changed from 'r+' to 'r'
            return file.read()
    except Exception as e:
        print(f"An error occurred while reading the ZPL file: {e}")
        return ""
