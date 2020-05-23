import xml.etree.ElementTree as ET

class Target:
    name = ""
    testType = ""
    path = ""

    def __init__(self):
        super().__init__()
        self.name = ""
        self.testType = ""
        self.path = ""

def LoadTargetsFromConfig(configXmlFile):
    config_tree = ET.parse(configXmlFile)
    config_root = config_tree.getroot()
    test_targets = config_root.findall(".//TestTarget");
    test_target = test_targets[0]
    test_target_path = test_target.attrib["Path"]

    return LoadTargets(test_target_path)

def LoadTargets(targetXmlFile):
    target_tree = ET.parse(targetXmlFile)
    target_root = target_tree.getroot()
    unittests = target_root.findall("UnitTest")

    targets = list()
    for unittest in unittests:
        target = Target()
        target.name = unittest.attrib["name"]
        target.testType = unittest.attrib["ext"]
        target.path = unittest.attrib["path"]
        targets.append(target)

    return targets

if __name__ == '__main__':
    targets = LoadTargetsFromConfig(".//UnitTextAutoRun_config.xml")

    for target in targets:
        print(target.path, target.name + "." + target.testType)
