from lxml import etree

def xml_validator(xml_path: str, xsd_path: str) -> bool:

    xml_doc = etree.parse(xml_path)
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    result = xmlschema.validate(xml_doc)

    return result


def validate(xml_file, xsd_file):
    return xml_validator(xml_file, xsd_file)
