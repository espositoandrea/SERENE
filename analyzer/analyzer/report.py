import datetime
import xml.etree.ElementTree as ET

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
    def paragraph(text: str):
        node = ET.SubElement(Report.__current_report, "p")
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
                counter-reset: h2counter h3counter h4counter h5counter h6counter;
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
            }'''
        body = ET.SubElement(html, 'body', {'class': 'container'})
        body.append(Report.__header())
        body.append(Report.__current_report)
        ET.ElementTree(html).write(file)
