from xlsxwriter import Workbook
from PIL import Image
from conf import OUT_DIRECTORY, C_MULTI, R_MULTI
import os
import sys

def convertToExcel(res, output_filename = "Result.xlsx", sheet_name = "Products", font = "Times New Roman", row_height = 200, picture_width = 50, picture_key = "picture", column_alpha = "F"):
    try:
        try:
            os.makedirs(OUT_DIRECTORY, exist_ok = True)
        except:
            pass  

        # opening a new file
        ordered_list = list(res[0].keys())
        wb=Workbook(OUT_DIRECTORY + "/" + output_filename, {'strings_to_urls': False})
        ws=wb.add_worksheet(sheet_name)

        # formatting for headers and rest of content
        head = wb.add_format({'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': font})
        content = wb.add_format({'text_wrap': True, 'valign': 'vcenter', 'align': 'center', 'border': 1, 'font_name': font})

        # declare widths of each column
        setTo = {
            "vendor_name": 18,
            "product_name": 18,
            "product_category": 18,
            "product_code": 18,
            "brand": 18,
            "product_type": 18,
            "made_in": 18,
            "average_rating":22,
            picture_key: picture_width,
            "description_and_specs": 35,
            "dimensions": 30,
            "material": 25,
            "warranty": 25,
            "product_link": 40
        }

        # set height of header row
        ws.set_row(0, 20, head)

        # set width of columns
        for i in setTo:
            ind = ordered_list.index(i)
            ws.set_column(ind, ind, setTo[i], content)

        # append header
        first_row=0
        for header in ordered_list:
            col=ordered_list.index(header)
            ws.write(first_row, col, header)

        # append rows
        row=1
        for player in res:
            for _key,_value in player.items():
                url = None
                if _key == picture_key:
                    url = _value
                    if url == "":
                        url = None
                    seti = None
                else:
                    seti = _value
                col=ordered_list.index(_key)
                ws.set_row(row, row_height, content)
                ws.write(row, col, seti)
                if url is not None:
                    size = Image.open(url).size
                    cell_size = (picture_width * C_MULTI, row_height*R_MULTI)
                    di = {
                        "x_scale": cell_size[0]/size[0] / 1.5,
                        "y_scale": cell_size[1]/size[1] / 1.5,
                    }
                    ws.insert_image(f"{column_alpha}{row + 1}", url, di)
            row+=1
        wb.close()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit()
    except Exception as e:
        print("Failed to convert to excel")
        print("Exception: ", e)