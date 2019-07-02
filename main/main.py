from jinja2 import Environment, FileSystemLoader
import os
import xml.etree.ElementTree as et
import re

def find_nth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)

fajlText = "[Cenovnik]"
prviIndex = find_nth(fajlText, ']', 1)
print(prviIndex)
fajlText = fajlText[0 : prviIndex] + ',\n Student' + fajlText[prviIndex:]
print(fajlText)
prviIndex = find_nth(fajlText, ']', 1)
fajlText = fajlText[0 : prviIndex] + ',\n Faktura' + fajlText[prviIndex:]
print(fajlText)
prviIndex = find_nth(fajlText, ']', 1)
fajlText = fajlText[0 : prviIndex] + ',\n Ocena' + fajlText[prviIndex:]
print(fajlText)

fajlText = "[Cenovnik]"
prviIndex = find_nth(fajlText, ']', 1)
print(prviIndex)
fajlText = fajlText[0 : prviIndex] + ",\n { path: 'cenovnik'  component: CenovnikComponent}" + fajlText[prviIndex:]
print(fajlText)
prviIndex = find_nth(fajlText, ']', 1)
fajlText = fajlText[0 : prviIndex] + ',\n Faktura' + fajlText[prviIndex:]
print(fajlText)
prviIndex = find_nth(fajlText, ']', 1)
fajlText = fajlText[0 : prviIndex] + ',\n Ocena' + fajlText[prviIndex:]
print(fajlText)


file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

templateNames = ['model', 'controller', 'service', 'repository', 'html', 'ts', 'angService', 'css']
for tn in templateNames:

    templateName = tn + '.txt'

    template = env.get_template(templateName)

    xml_file = os.path.join('C:/Users/Dragisa/Desktop/fakt2.xml')
    tree = et.parse(xml_file)
    root = tree.getroot()

    primitiveTypes = {}

    # extracting types
    for child in root:
        if child.attrib['{http://schema.omg.org/spec/XMI/2.1}type'] == 'uml:PrimitiveType':
            primitiveTypes[child.attrib['{http://schema.omg.org/spec/XMI/2.1}id']] = child.attrib['name']

    #print(primitiveTypes)

    classesWithFields = {}
    classesWithIds = {}

    for child in root:
        #print(child.attrib)
        if (child.attrib['{http://schema.omg.org/spec/XMI/2.1}type'] == 'uml:Class'):
            #sacuvaj id klase i naziv
            classesWithIds[child.attrib['{http://schema.omg.org/spec/XMI/2.1}id']] = child.attrib['name']
            #sacuvaj id klase i naziv end
            fields = []
            for c in child:  #ovo su polja klase
                field = {}
                field[c.attrib['name']] = primitiveTypes[c.attrib['type']]
                fields.append(field)
            classesWithFields[child.attrib['name']] = fields
            fields = []

    print("Classes with fields: ")
    print(classesWithFields)
    print("____________________________________________________________________________________________")
    print(classesWithIds)

    associations = []

    for child in root:
        if child.attrib['{http://schema.omg.org/spec/XMI/2.1}type'] == 'uml:Association':
            one = ''
            many = ''
            for ch in child:
                for c in ch:
                    if c.tag == 'upperValue' and c.attrib['value'] == '1':
                        one = classesWithIds[ch.attrib['type']]
                    if c.tag == 'upperValue' and c.attrib['value'] == '*':
                        many = classesWithIds[ch.attrib['type']]
            if one != '' and many != '':
                print("One: " + one + " Many: " + many)
                associations.append({many : one})

    print("Asocijacije")
    print(associations)

    def putDash(input):
        # regex [A-Z][a-z]* means any string starting
        # with capital character followed by many
        # lowercase letters
        words = re.findall('[A-Z][a-z]*', input)

        # Change first letter of each word into lower
        # case
        result = []
        for word in words:
            word = chr(ord(word[0]) + 32) + word[1:]
            result.append(word)
        return '-'.join(result)
    print ('------------------------------')
    print (classesWithFields)
    print ('------------------------------')
    for tempClassKey in classesWithFields:

        vezice = []
        veze = []
        vezeImports = []
        for ass in associations:
            for k, v in ass.items():
                if k == tempClassKey:
                    vezice.append(v[0].lower() + v[1:] + "Id")
                    veze.append({v : v[0].lower() + v[1:] + "Id"})
                    vezeImports.append({v : putDash(v)})
        print("Vezice")
        print(vezeImports)

        clsObj = tempClassKey[0].lower() + tempClassKey[1:]
        output = template.render(className=tempClassKey, fields = classesWithFields[tempClassKey], clsObj = clsObj,
                                 classNameDash = putDash(tempClassKey).lower(), vezice = vezice, veze = veze, vezeImports = vezeImports, specOpen="{{", specClose="}}")
        filePath = ''
        if tn == 'css':
            angularClassName = putDash(tempClassKey).lower()
            if not os.path.exists(r'C:/Users/Dragisa/Desktop/mbrs/src/app/' + angularClassName):
                os.makedirs(r'C:/Users/Dragisa/Desktop/mbrs/src/app/' + angularClassName)
            filePath = os.path.join('C:/Users/Dragisa/Desktop/mbrs/src/app/' + angularClassName, angularClassName + '.component.css')
        elif tn == 'html' or tn == 'ts' or tn == 'angService':
            if not os.path.exists(r'C:/Users/Dragisa/Desktop/mbrs/src/app/' + putDash(tempClassKey).lower()):
                os.makedirs(r'C:/Users/Dragisa/Desktop/mbrs/src/app/' + putDash(tempClassKey).lower())
            angularClassName = putDash(tempClassKey).lower()
            if tn == 'angService':
                filePath = os.path.join('C:/Users/Dragisa/Desktop/mbrs/src/app/' + angularClassName, angularClassName + '.service.ts')
            else:
                filePath = os.path.join('C:/Users/Dragisa/Desktop/mbrs/src/app/' + angularClassName, angularClassName + '.component.' + tn)
        else:
            if not os.path.exists(r'C:/Users/Dragisa/Desktop/generator/generator/src/main/java/com/mbrs/generator/' + tn):
                os.makedirs(r'C:/Users/Dragisa/Desktop/generator/generator/src/main/java/com/mbrs/generator/' + tn)

            javaClassName = ''
            if tn == 'model':
                javaClassName = tempClassKey
            else:
                javaClassName = tempClassKey + tn.title()

            if os.path.exists(r'C:/Users/Dragisa/Desktop/generator/generator/src/main/java/com/mbrs/generator/' + tn + '/' + javaClassName+'.java'):
                existing = open(r'C:/Users/Dragisa/Desktop/generator/generator/src/main/java/com/mbrs/generator/' + tn + '/' + javaClassName+'.java', 'r')
                if existing.read() != output:
                    test_number = int(input("Da li zelite da pregazite postojeci fajl koji je drugaciji od default fajla (1 za Da, 2 za NE): "))
                    if test_number == 1:
                        filePath = os.path.join('C:/Users/Dragisa/Desktop/generator/generator/src/main/java/com/mbrs/generator/' + tn,javaClassName + '.java')
            else:
                filePath = os.path.join('C:/Users/Dragisa/Desktop/generator/generator/src/main/java/com/mbrs/generator/' + tn, javaClassName+'.java')


        if filePath == '':
            print("Ostavicemo sve kao sto je bilo ranije")
        else:
            file = open(filePath, "w")
            file.write(output)
            file.close()


    nekiNaziv = "StavkaCenovnika"


    def putSpace(input):
        # regex [A-Z][a-z]* means any string starting
        # with capital character followed by many
        # lowercase letters
        words = re.findall('[A-Z][a-z]*', input)

        # Change first letter of each word into lower
        # case
        result = []
        for word in words:
            word = chr(ord(word[0]) + 32) + word[1:]
            result.append(word)
        print(' '.join(result))



    putDash(nekiNaziv)






