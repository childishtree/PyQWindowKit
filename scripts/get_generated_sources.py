
import sys
import os
import xml.etree.ElementTree as ET

def get_generated_sources(xml_path, output_dir_prefix):
    if not os.path.exists(xml_path):
        return ""
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError:
        return ""
    
    package_name = root.attrib.get('package', '').lower()
    sources = []
    
    # Module wrapper is always generated
    sources.append(f"{output_dir_prefix}/{package_name}_module_wrapper.cpp")
    
    def process_element(element, current_ns=""):
        for child in element:
            if child.tag == 'namespace-type':
                ns_name = child.attrib.get('name', '')
                # Shiboken flattens namespaces in filenames: ns1_ns2_classname_wrapper.cpp
                new_ns = f"{current_ns}_{ns_name}" if current_ns else ns_name
                process_element(child, new_ns)
            elif child.tag in ('object-type', 'value-type', 'interface-type'):
                class_name = child.attrib.get('name', '')
                full_name = f"{current_ns}_{class_name}" if current_ns else class_name
                # Filenames are lowercase
                filename = f"{output_dir_prefix}/{full_name.lower()}_wrapper.cpp"
                sources.append(filename)
            
    process_element(root)
    
    # Return cmake list (semicolon separated)
    return ";".join(sources)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("")
        sys.exit(0)
    
    xml_file = sys.argv[1]
    prefix = sys.argv[2]
    
    # Ensure forward slashes for CMake compatibility
    prefix = prefix.replace("\\", "/")
    
    print(get_generated_sources(xml_file, prefix))
