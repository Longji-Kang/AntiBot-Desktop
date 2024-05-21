import joblib
import pickle
import os
import pefile
import array
import math

class AiScanner:
    def __init__(self, def_file):
        self.classifier = joblib.load(f'Definitions/{def_file}')
    
        with open('Definitions/features.pkl', 'rb') as file:
            contents = file.read()
            self.features = pickle.loads(contents)

    def aiScan(self, file):
        data = self.get_info(file)
        reader_features = list(map(lambda d:data[d], self.features))
    
        result = self.classifier.predict([reader_features])[0]

        return result

    def get_info(self, file):
        resolver = {}
        pickle_reader = pefile.PE(file)
        resolver['Machine'] = pickle_reader.FILE_HEADER.Machine
        resolver['SizeOfOptionalHeader'] = pickle_reader.FILE_HEADER.SizeOfOptionalHeader
        resolver['Characteristics'] = pickle_reader.FILE_HEADER.Characteristics
        resolver['MajorLinkerVersion'] = pickle_reader.OPTIONAL_HEADER.MajorLinkerVersion
        resolver['MinorLinkerVersion'] = pickle_reader.OPTIONAL_HEADER.MinorLinkerVersion
        resolver['SizeOfCode'] = pickle_reader.OPTIONAL_HEADER.SizeOfCode
        resolver['SizeOfInitializedData'] = pickle_reader.OPTIONAL_HEADER.SizeOfInitializedData
        resolver['SizeOfUninitializedData'] = pickle_reader.OPTIONAL_HEADER.SizeOfUninitializedData
        resolver['AddressOfEntryPoint'] = pickle_reader.OPTIONAL_HEADER.AddressOfEntryPoint
        resolver['BaseOfCode'] = pickle_reader.OPTIONAL_HEADER.BaseOfCode
        try:
            resolver['BaseOfData'] = pickle_reader.OPTIONAL_HEADER.BaseOfData
        except AttributeError:
            resolver['BaseOfData'] = 0
        resolver['ImageBase'] = pickle_reader.OPTIONAL_HEADER.ImageBase
        resolver['SectionAlignment'] = pickle_reader.OPTIONAL_HEADER.SectionAlignment
        resolver['FileAlignment'] = pickle_reader.OPTIONAL_HEADER.FileAlignment
        resolver['MajorOperatingSystemVersion'] = pickle_reader.OPTIONAL_HEADER.MajorOperatingSystemVersion
        resolver['MinorOperatingSystemVersion'] = pickle_reader.OPTIONAL_HEADER.MinorOperatingSystemVersion
        resolver['MajorImageVersion'] = pickle_reader.OPTIONAL_HEADER.MajorImageVersion
        resolver['MinorImageVersion'] = pickle_reader.OPTIONAL_HEADER.MinorImageVersion
        resolver['MajorSubsystemVersion'] = pickle_reader.OPTIONAL_HEADER.MajorSubsystemVersion
        resolver['MinorSubsystemVersion'] = pickle_reader.OPTIONAL_HEADER.MinorSubsystemVersion
        resolver['SizeOfImage'] = pickle_reader.OPTIONAL_HEADER.SizeOfImage
        resolver['SizeOfHeaders'] = pickle_reader.OPTIONAL_HEADER.SizeOfHeaders
        resolver['CheckSum'] = pickle_reader.OPTIONAL_HEADER.CheckSum
        resolver['Subsystem'] = pickle_reader.OPTIONAL_HEADER.Subsystem
        resolver['DllCharacteristics'] = pickle_reader.OPTIONAL_HEADER.DllCharacteristics
        resolver['SizeOfStackReserve'] = pickle_reader.OPTIONAL_HEADER.SizeOfStackReserve
        resolver['SizeOfStackCommit'] = pickle_reader.OPTIONAL_HEADER.SizeOfStackCommit
        resolver['SizeOfHeapReserve'] = pickle_reader.OPTIONAL_HEADER.SizeOfHeapReserve
        resolver['SizeOfHeapCommit'] = pickle_reader.OPTIONAL_HEADER.SizeOfHeapCommit
        resolver['LoaderFlags'] = pickle_reader.OPTIONAL_HEADER.LoaderFlags
        resolver['NumberOfRvaAndSizes'] = pickle_reader.OPTIONAL_HEADER.NumberOfRvaAndSizes

        resolver['SectionsNb'] = len(pickle_reader.sections)
        entropy = list(map(lambda x:x.get_entropy(), pickle_reader.sections))
        resolver['SectionsMeanEntropy'] = sum(entropy)/float(len((entropy)))
        resolver['SectionsMinEntropy'] = min(entropy)
        resolver['SectionsMaxEntropy'] = max(entropy)
        raw_sizes = list(map(lambda x:x.SizeOfRawData, pickle_reader.sections))
        resolver['SectionsMeanRawsize'] = sum(raw_sizes)/float(len((raw_sizes)))
        resolver['SectionsMinRawsize'] = min(raw_sizes)
        resolver['SectionsMaxRawsize'] = max(raw_sizes)
        virtual_sizes = list(map(lambda x:x.Misc_VirtualSize, pickle_reader.sections))
        resolver['SectionsMeanVirtualsize'] = sum(virtual_sizes)/float(len(virtual_sizes))
        resolver['SectionsMinVirtualsize'] = min(virtual_sizes)
        resolver['SectionMaxVirtualsize'] = max(virtual_sizes)

        try:
            resolver['ImportsNbDLL'] = len(pickle_reader.DIRECTORY_ENTRY_IMPORT)
            imports = sum([x.imports for x in pickle_reader.DIRECTORY_ENTRY_IMPORT], [])
            resolver['ImportsNb'] = len(imports)
            resolver['ImportsNbOrdinal'] = 0
        except AttributeError:
            resolver['ImportsNbDLL'] = 0
            resolver['ImportsNb'] = 0
            resolver['ImportsNbOrdinal'] = 0

        try:
            resolver['ExportNb'] = len(pickle_reader.DIRECTORY_ENTRY_EXPORT.symbols)
        except AttributeError:
            resolver['ExportNb'] = 0
        resources= self.data_resources(pickle_reader)
        resolver['ResourcesNb'] = len(resources)
        if len(resources)> 0:
            entropy = list(map(lambda x:x[0], resources))
            resolver['ResourcesMeanEntropy'] = sum(entropy)/float(len(entropy))
            resolver['ResourcesMinEntropy'] = min(entropy)
            resolver['ResourcesMaxEntropy'] = max(entropy)
            sizes = list(map(lambda x:x[1], resources))
            resolver['ResourcesMeanSize'] = sum(sizes)/float(len(sizes))
            resolver['ResourcesMinSize'] = min(sizes)
            resolver['ResourcesMaxSize'] = max(sizes)
        else:
            resolver['ResourcesNb'] = 0
            resolver['ResourcesMeanEntropy'] = 0
            resolver['ResourcesMinEntropy'] = 0
            resolver['ResourcesMaxEntropy'] = 0
            resolver['ResourcesMeanSize'] = 0
            resolver['ResourcesMinSize'] = 0
            resolver['ResourcesMaxSize'] = 0

        try:
            resolver['LoadConfigurationSize'] = pickle_reader.DIRECTORY_ENTRY_LOAD_CONFIG.struct.Size
        except AttributeError:
            resolver['LoadConfigurationSize'] = 0


        # Version configuration size
        try:
            version_infos = self.version_data(pickle_reader)
            resolver['VersionInformationSize'] = len(version_infos.keys())
        except AttributeError:
            resolver['VersionInformationSize'] = 0

        pefile.PE.close(pickle_reader)
        return resolver
        
    
    def version_data(self, pickle_reader):
        result = {}
        for fileinfo in pickle_reader.FileInfo:
            if fileinfo.Key == 'StringFileInfo':
                for st in fileinfo.StringTable:
                    for entry in st.entries.items():
                        result[entry[0]] = entry[1]
            if fileinfo.Key == 'VarFileInfo':
                for var in fileinfo.Var:
                    result[var.entry.items()[0][0]] = var.entry.items()[0][1]
        if hasattr(pickle_reader, 'VS_FIXEDFILEINFO'):
            result['flags'] = pickle_reader.VS_FIXEDFILEINFO.FileFlags
            result['os'] = pickle_reader.VS_FIXEDFILEINFO.FileOS
            result['type'] = pickle_reader.VS_FIXEDFILEINFO.FileType
            result['file_version'] = pickle_reader.VS_FIXEDFILEINFO.FileVersionLS
            result['product_version'] = pickle_reader.VS_FIXEDFILEINFO.ProductVersionLS
            result['signature'] = pickle_reader.VS_FIXEDFILEINFO.Signature
            result['struct_version'] = pickle_reader.VS_FIXEDFILEINFO.StrucVersion
        return result
    
    def data_resources(self, pickle_reader):
        resources = []
        if hasattr(pickle_reader, 'DIRECTORY_ENTRY_RESOURCE'):
            try:
                for resource_type in pickle_reader.DIRECTORY_ENTRY_RESOURCE.entries:
                    if hasattr(resource_type, 'directory'):
                        for resource_id in resource_type.directory.entries:
                            if hasattr(resource_id, 'directory'):
                                for resource_lang in resource_id.directory.entries:
                                    data = pickle_reader.get_data(resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                                    size = resource_lang.data.struct.Size
                                    entropy = self.get_file_entropy(data)

                                    resources.append([entropy, size])
            except Exception as e:
                return resources
        return resources
    
    def get_entropy(self, data):
        if len(data) == 0:
            return 0.0
        occurences = array.array('L', [0]*256)
        for x in data:
            occurences[x if isinstance(x, int) else ord(x)] += 1

        entropy = 0
        for x in occurences:
            if x:
                p_x = float(x) / len(data)
                entropy -= p_x*math.log(p_x, 2)

        return entropy