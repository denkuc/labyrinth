import glob
import json
import re


class ProjectBuilder:
    def __init__(self, sources_folder_path: str):
        self.__sources_folder_path = sources_folder_path

    def get_content(self) -> str:
        prepared_content = ''
        # prepared_content = self.__get_and_add_imports(prepared_content)
        prepared_content = self.__get_and_add_classes(prepared_content)

        return prepared_content

    def __get_and_add_imports(self, content: str) -> str:
        collected_imports = self.__read_directory_and_collect_imports()
        for collected_import in collected_imports:
            if content != '':
                content += "\n"

            content += collected_import

        return content

    def __read_directory_and_collect_imports(self):
        collected_imports = set()
        for file_path in glob.iglob(self.__sources_folder_path + '**/**', recursive=True):
            if not self.__is_applicable_file(file_path):
                continue

            imports_from_file = self.__collect_imports_from_file(file_path)
            for import_from_file in imports_from_file:
                collected_imports.add(import_from_file)

        return collected_imports

    def __collect_imports_from_file(self, file_path: str) -> set:
        collected_imports = set()
        file_resource = open(file_path, 'r')
        file_content = file_resource.read()
        file_resource.close()

        from_import_regex = r'^from (.*) import (.*)'
        import_regex = r'^import (.*)'

        from_import_result = re.findall(from_import_regex, file_content, re.MULTILINE)
        import_result = re.findall(import_regex, file_content, re.MULTILINE)

        for from_import_item in from_import_result:
            if self.__is_internal_import(from_import_item[0]):
                continue

            import_line = 'from {} import {}'.format(from_import_item[0], from_import_item[1])

            collected_imports.add(import_line)

        for import_item in import_result:
            if self.__is_internal_import(import_item):
                continue

            import_line = 'import {}'.format(import_item)

            collected_imports.add(import_line)

        return collected_imports

    @staticmethod
    def __is_internal_import(import_line: str) -> bool:
        internal_import_folders = ['entity', 'common', 'logic', 'service']

        for internal_import_folder in internal_import_folders:
            if import_line.find(internal_import_folder) > -1:
                return True

        return False

    def __get_and_add_classes(self, content: str) -> str:
        files_info_tree = self.__read_directory_and_build_files_info_tree()
        for file_info in files_info_tree:
            if content != '':
                content += "\r\n\n"

            content += file_info['class_content']

        return content

    def __is_applicable_file(self, file_path: str) -> bool:
        if file_path.find('.py') == -1:
            return False

        if file_path.find('__init__.py') > -1:
            return False

        return True

    def __read_directory_and_build_files_info_tree(self):
        files_info_tree = {}
        for file_path in glob.iglob(self.__sources_folder_path + '**/**', recursive=True):
            if not self.__is_applicable_file(file_path):
                continue

            file_infos = self.__get_file_infos(file_path)
            for key, value in file_infos.items():
                files_info_tree[key] = value

        for file_info in files_info_tree.values():
            self.__setup_dependencies(file_info, files_info_tree.keys())

        files_info_tree = self.__update_position(files_info_tree)

        sorted_files_info_tree = sorted(files_info_tree.values(), key=lambda d: d['position'])

        return sorted_files_info_tree

    def __get_file_infos(self, file_path: str):
        file_infos = {}
        file_resource = open(file_path, 'r')
        file_content = file_resource.read()
        file_resource.close()

        find_classes_result = re.findall(r'class ([a-zA-Z]+)', file_content, re.MULTILINE)
        position = 0
        for class_name in find_classes_result:
            file_infos[class_name] = {
                'path': file_path,
                'class_name': class_name,
                'class_content': self.__get_class_content(class_name, file_content),
                'dependencies': [],
                'position': position
            }
            position = position + 1

        return file_infos

    @staticmethod
    def __setup_dependencies(file_info: dict, class_name_list):
        for class_name in class_name_list:
            if class_name == file_info['class_name']:
                continue

            if file_info['class_content'].find(class_name) == -1:
                continue

            if file_info['class_content'].find('"{}"'.format(class_name)) > -1:
                continue

            if file_info['class_content'].find("'{}'".format(class_name)) > -1:
                continue

            file_info['dependencies'].append(class_name)

    def __update_position(self, files_info_tree: dict):
        is_position_updated = False
        for class_name, file_info in files_info_tree.items():
            if len(file_info['dependencies']) == 0:
                continue

            position = file_info['position']
            for dependency_name in file_info['dependencies']:
                dependency_position = files_info_tree[dependency_name]['position']
                if dependency_position >= position:
                    position = dependency_position + 1

            if file_info['position'] != position:
                file_info['position'] = position
                is_position_updated = True

        if is_position_updated is True:
            return self.__update_position(files_info_tree)

        return files_info_tree

    @staticmethod
    def __get_class_content(class_name: str, file_content: str):
        class_content_regex_with_multi_classes = r'class {}(.*?):(.*)(class)'.format(class_name)
        class_content_regex_with_one_class = r'class {}(.*?):(.*)'.format(class_name)

        class_content = ''
        find_class_content_result = re.search(class_content_regex_with_multi_classes, file_content, re.S)
        if not find_class_content_result:
            find_class_content_result = re.search(class_content_regex_with_one_class, file_content, re.S)
            if find_class_content_result:
                class_content = find_class_content_result.group(0)
        else:
            class_content = find_class_content_result.group(0)
            # need to remove last class text
            class_content = class_content[0:-5]

        class_content = class_content.strip()

        return class_content


if __name__ == '__main__':
    project_builder = ProjectBuilder('labyrinth')

    template_file_resource = open('main.template.py', 'r')
    template_file_content = template_file_resource.read()
    template_file_resource.close()

    result_file_resource = open('main.py', 'w')
    result_file_resource.write(template_file_content.replace('{placeholder}', project_builder.get_content()))
    result_file_resource.close()
