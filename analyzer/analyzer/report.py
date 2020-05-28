import datetime
import xml.etree.ElementTree as ET
from typing import Dict, Any, List

import requests


class Report:
    __current_report = ET.Element('main')

    @staticmethod
    def __heading(title: str, level: int):
        node = ET.SubElement(Report.__current_report, f"h{level}")
        node.text = title
        return node

    @staticmethod
    def section(title: str):
        return Report.__heading(title, 2)

    @staticmethod
    def subsection(title: str):
        return Report.__heading(title, 3)

    @staticmethod
    def subsubsection(title: str):
        return Report.__heading(title, 4)

    @staticmethod
    def paragraph(title: str):
        return Report.__heading(title, 5)

    @staticmethod
    def code(content: str, inline: bool = True, parent: ET.Element = None) -> ET.Element:
        if inline:
            code = ET.SubElement(Report.__current_report if not parent else parent, 'pre')
            real_code = ET.SubElement(code, 'code')
            real_code.text = content
        else:
            code = ET.SubElement(Report.__current_report if not parent else parent, 'code')
            code.text = content
        return code

    @staticmethod
    def subparagraph(title: str):
        return Report.__heading(title, 6)

    @staticmethod
    def figure(source: str, caption: str = None):
        figure = ET.SubElement(Report.__current_report, 'figure', {'class': 'figure text-center w-100'})
        if caption:
            figcaption = ET.SubElement(figure, 'figcaption', {'class': 'figure-caption'})
            figcaption.text = caption
        img = ET.SubElement(figure, 'img', {'src': source, 'class': 'figure-img img-fluid', 'alt': caption})
        return figure

    @staticmethod
    def table(data: List[Dict[str, Any]], caption: str = None, id_col: str = None):
        div = ET.SubElement(Report.__current_report, 'div', {'class': 'table-responsive'})
        table = ET.SubElement(div, 'table', {'class': 'table table-striped'})

        if caption:
            caption_element = ET.SubElement(table, 'caption')
            caption_element.text = caption

        thead = ET.SubElement(table, 'thead')
        tr = ET.SubElement(thead, 'tr')
        for key in data[0]:
            th = ET.SubElement(tr, 'th', {'scope': 'col'})
            th.text = key
        tbody = ET.SubElement(table, 'tbody')
        for obj in data:
            tr = ET.SubElement(tbody, 'tr')
            for key in obj:
                td = ET.SubElement(tr, 'td') if key != id_col else ET.SubElement(tr, 'th', {'scope': 'row'})
                td.text = str(obj[key])

        return div

    @staticmethod
    def text(text: str = None):
        node = ET.SubElement(Report.__current_report, "p")
        if text:
            node.text = text
        return node

    @staticmethod
    def __header():
        header = ET.Element('header', {'class': "text-center"})
        title = ET.SubElement(header, 'h1')
        title.text = "Processing and Analysis Results"
        p = ET.SubElement(header, 'p')
        p.text = datetime.datetime.now().isoformat(sep=' ', timespec='minutes')
        ET.SubElement(header, 'hr')
        return header

    @staticmethod
    def html(file):
        html = ET.Element('html')
        head = ET.SubElement(html, 'head')
        ET.SubElement(head, 'meta', {'charset': 'UTF-8'})
        ET.SubElement(head, 'meta', {'name': "viewport", 'content': "width=device-width, initial-scale=1.0"})
        style = ET.SubElement(head, 'style')
        style.text = requests.get("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css").text
        style.text += r'''body {
                counter-reset: h2counter h3counter h4counter h5counter h6counter tableCounter figureCounter;
            }
            h1 {
                counter-reset: h2counter h3counter h4counter h5counter h6counter;
            }
            h2:before {
                content: counter(h2counter) ".\0000a0\0000a0";
                counter-increment: h2counter;
            }
            h2 {
                counter-reset: h3counter h4counter h5counter h6counter;
            }
            h3:before {
                content: counter(h2counter) "." counter(h3counter) ".\0000a0\0000a0";
                counter-increment: h3counter;
            }
            h3 {
                counter-reset: h4counter h5counter h6counter;
            }
            h4:before {
                content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) ".\0000a0\0000a0";
                counter-increment: h4counter;
            }
            h4 {
                counter-reset: h5counter h6counter;
            }
            h5:before {
                content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) ".\0000a0\0000a0";
                counter-increment: h5counter;
            }
            h5 {
                counter-reset: h6counter;
            }
            h6:before {
                content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) "." counter(h6counter) ".\0000a0\0000a0";
                counter-increment: h6counter;
            }
            caption {
                caption-side: top !important;
                text-align: center;
                counter-increment: tableCounter;
            }
            caption:before{
                font-weight: bold;
                content: "Table " counter(tableCounter) ".\0000a0\0000a0";
            }
            figcaption {
                counter-increment: figureCounter;
            }
            figcaption:before{
                font-weight: bold;
                content: "Figure " counter(figureCounter) ".\0000a0\0000a0";
            }
            '''
        body = ET.SubElement(html, 'body', {'class': 'container'})
        body.append(Report.__header())
        body.append(Report.__current_report)
        ET.ElementTree(html).write(file)
